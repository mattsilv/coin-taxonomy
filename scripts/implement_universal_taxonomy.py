#!/usr/bin/env python3
"""
Implement Universal Currency Taxonomy - Phase 1

This script updates the database schema to support world currencies while maintaining
backward compatibility with existing US coin data.

Key changes:
1. Relax coin_id format constraint to support international currencies
2. Add optional schema evolution fields
3. Create lookup tables for country codes, TYPE codes, and mint facilities
4. Maintain existing US data integrity
"""

import sqlite3
import json
from datetime import datetime


def get_database_connection():
    """Get connection to the coins database."""
    return sqlite3.connect('database/coins.db')


def backup_database():
    """Create a backup of the database before making changes."""
    import shutil
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'backups/coins_backup_{timestamp}.db'
    shutil.copy('database/coins.db', backup_path)
    print(f"✅ Database backed up to {backup_path}")
    return backup_path


def update_coin_id_constraint(conn):
    """Update the coin_id constraint to support international currencies."""
    print("🔧 Updating coin_id constraint for international support...")
    
    # The CHECK constraint needs to be more flexible
    # New format: COUNTRY-TYPE-YEAR-MINT where:
    # - COUNTRY: 2-4 characters (US, EU, XCD, etc.)
    # - TYPE: 4 characters exactly
    # - YEAR: 4 digits or 0000
    # - MINT: 1-4 characters
    
    cursor = conn.cursor()
    
    # First, let's see the current constraint
    cursor.execute("PRAGMA table_info(coins)")
    print("Current table structure:", cursor.fetchall())
    
    # Create new table with updated constraint
    cursor.execute("""
        CREATE TABLE coins_new (
            coin_id TEXT PRIMARY KEY,
            series_id TEXT NOT NULL,
            country TEXT NOT NULL,
            denomination TEXT NOT NULL,
            series_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            mint TEXT NOT NULL,
            business_strikes INTEGER,
            proof_strikes INTEGER,
            rarity TEXT CHECK(rarity IN ("key", "semi-key", "common", "scarce")),
            composition JSON,
            weight_grams REAL,
            diameter_mm REAL,
            varieties JSON,
            source_citation TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            obverse_description TEXT NOT NULL,
            reverse_description TEXT NOT NULL,
            distinguishing_features TEXT NOT NULL,
            identification_keywords TEXT NOT NULL,
            common_names TEXT NOT NULL,
            
            -- Updated constraint to support international currencies
            CONSTRAINT valid_coin_id_format CHECK (
                coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                coin_id GLOB '[A-Z][A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'
            )
        )
    """)
    
    # Copy existing data
    cursor.execute("""
        INSERT INTO coins_new SELECT * FROM coins
    """)
    
    # Drop old table and rename new one
    cursor.execute("DROP TABLE coins")
    cursor.execute("ALTER TABLE coins_new RENAME TO coins")
    
    # Recreate indexes
    cursor.execute("CREATE INDEX idx_coins_series ON coins(series_id)")
    cursor.execute("CREATE INDEX idx_coins_year ON coins(year)")
    cursor.execute("CREATE INDEX idx_coins_denomination ON coins(denomination)")
    cursor.execute("CREATE INDEX idx_coins_rarity ON coins(rarity)")
    
    conn.commit()
    print("✅ Updated coin_id constraint to support international currencies")


def add_schema_evolution_fields(conn):
    """Add optional fields for enhanced taxonomy support."""
    print("🔧 Adding schema evolution fields...")
    
    cursor = conn.cursor()
    
    # Add new columns for Phase 2 functionality
    new_columns = [
        ("category", "TEXT", "COIN/BILL/TOKEN/SCRIP classification"),
        ("issuer", "TEXT", "For private/regional issues"),
        ("series_year", "TEXT", "For bills with series dates different from print year"),
        ("calendar_type", "TEXT", "GREGORIAN/ISLAMIC/JAPANESE_ERA for date conversion"),
        ("original_date", "TEXT", "Original date before conversion (e.g., 'Showa 55', 'AH 1332')")
    ]
    
    for column_name, column_type, description in new_columns:
        try:
            cursor.execute(f"ALTER TABLE coins ADD COLUMN {column_name} {column_type}")
            print(f"  ✅ Added {column_name} column - {description}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"  ⚠️  Column {column_name} already exists")
            else:
                raise
    
    # Set default values for existing US coins
    cursor.execute("""
        UPDATE coins 
        SET category = 'COIN', 
            calendar_type = 'GREGORIAN'
        WHERE category IS NULL
    """)
    
    conn.commit()
    print("✅ Schema evolution fields added successfully")


def create_reference_tables(conn):
    """Create lookup tables for country codes, TYPE standards, and facilities."""
    print("🔧 Creating reference tables...")
    
    cursor = conn.cursor()
    
    # Country codes reference table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS country_codes (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL, -- 'standard', 'multi-nation', 'special'
            description TEXT,
            iso_3166_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # TYPE codes reference table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS type_codes (
            code TEXT PRIMARY KEY,
            category TEXT NOT NULL, -- 'coin', 'bill', 'bullion', 'special'
            description TEXT NOT NULL,
            denomination_value REAL,
            currency_unit TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Mint facilities reference table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mint_facilities (
            code TEXT NOT NULL,
            country_code TEXT NOT NULL,
            name TEXT NOT NULL,
            location TEXT,
            type TEXT NOT NULL, -- 'mint', 'printing_bureau', 'private'
            active_period JSON, -- {"start": year, "end": year}
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (code, country_code)
        )
    """)
    
    conn.commit()
    print("✅ Reference tables created")


def populate_initial_reference_data(conn):
    """Populate reference tables with initial data from the best practice."""
    print("🔧 Populating reference tables with initial data...")
    
    cursor = conn.cursor()
    
    # Country codes
    country_data = [
        ('US', 'United States', 'standard', 'United States of America', 'US'),
        ('CA', 'Canada', 'standard', 'Canada', 'CA'),
        ('GB', 'Great Britain', 'standard', 'United Kingdom', 'GB'),
        ('DE', 'Germany', 'standard', 'Germany', 'DE'),
        ('CN', 'China', 'standard', 'People\'s Republic of China', 'CN'),
        ('JP', 'Japan', 'standard', 'Japan', 'JP'),
        ('AU', 'Australia', 'standard', 'Australia', 'AU'),
        ('FR', 'France', 'standard', 'France', 'FR'),
        ('IT', 'Italy', 'standard', 'Italy', 'IT'),
        ('ES', 'Spain', 'standard', 'Spain', 'ES'),
        ('EU', 'Euro Zone', 'multi-nation', 'European Union (19+ countries)', None),
        ('XCD', 'East Caribbean Dollar', 'multi-nation', 'Eastern Caribbean Central Bank (8 countries)', None),
        ('XOF', 'West African CFA Franc', 'multi-nation', 'West African Economic and Monetary Union', None),
        ('XAF', 'Central African CFA Franc', 'multi-nation', 'Central African Economic and Monetary Union', None),
        ('CSA', 'Confederate States', 'special', 'Confederate States of America', None),
        ('UN', 'United Nations', 'special', 'United Nations special issues', None),
        ('XX', 'Unknown', 'special', 'Unknown or unattributed items', None)
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO country_codes 
        (code, name, type, description, iso_3166_code) 
        VALUES (?, ?, ?, ?, ?)
    """, country_data)
    
    # Common TYPE codes for coins
    coin_type_data = [
        ('CENT', 'coin', 'Cent/Penny', 0.01, 'USD'),
        ('5CNT', 'coin', '5 cents/Nickel', 0.05, 'USD'),
        ('DIME', 'coin', '10 cents/Dime', 0.10, 'USD'),
        ('QRTR', 'coin', '25 cents/Quarter', 0.25, 'USD'),
        ('HALF', 'coin', '50 cents/Half Dollar', 0.50, 'USD'),
        ('DOLR', 'coin', 'Dollar coin', 1.00, 'USD'),
        ('EURO', 'coin', 'Euro coin', 1.00, 'EUR'),
        ('POUN', 'coin', 'Pound Sterling', 1.00, 'GBP'),
        ('YUAN', 'coin', 'Chinese Yuan', 1.00, 'CNY'),
        ('YEN', 'coin', 'Japanese Yen', 1.00, 'JPY'),
        ('RUBL', 'coin', 'Russian Ruble', 1.00, 'RUB')
    ]
    
    # Common TYPE codes for paper money
    bill_type_data = [
        ('FN01', 'bill', '$1 Federal Reserve Note', 1.00, 'USD'),
        ('FN05', 'bill', '$5 Federal Reserve Note', 5.00, 'USD'),
        ('FN10', 'bill', '$10 Federal Reserve Note', 10.00, 'USD'),
        ('FN20', 'bill', '$20 Federal Reserve Note', 20.00, 'USD'),
        ('FN50', 'bill', '$50 Federal Reserve Note', 50.00, 'USD'),
        ('FN100', 'bill', '$100 Federal Reserve Note', 100.00, 'USD'),
        ('SC05', 'bill', '$5 Silver Certificate', 5.00, 'USD'),
        ('GC20', 'bill', '$20 Gold Certificate', 20.00, 'USD')
    ]
    
    # Bullion TYPE codes
    bullion_type_data = [
        ('MAPL', 'bullion', 'Canadian Maple Leaf', 1.00, 'CAD'),
        ('PAN1', 'bullion', '1 oz Silver Panda', 1.00, 'CNY'),
        ('KRGD', 'bullion', 'Krugerrand', 1.00, 'ZAR'),
        ('PHIL', 'bullion', 'Austrian Philharmonic', 1.00, 'EUR'),
        ('AEGL', 'bullion', 'American Eagle', 1.00, 'USD'),
        ('SOVR', 'bullion', 'Gold Sovereign', 1.00, 'GBP')
    ]
    
    # Special TYPE codes
    special_type_data = [
        ('MPC5', 'special', 'Military Payment Certificate $5', 5.00, 'USD'),
        ('SCRP', 'special', 'Company Scrip', None, None),
        ('NG50', 'special', 'Notgeld 50 pfennig', 0.50, 'DEM'),
        ('100T', 'special', '100 Trillion (hyperinflation)', 100000000000000.00, None),
        ('1Q', 'special', '1 Quintillion (hyperinflation)', 1000000000000000000.00, None),
        ('TOKN', 'special', 'Token', None, None),
        ('MEDL', 'special', 'Medal', None, None)
    ]
    
    all_type_data = coin_type_data + bill_type_data + bullion_type_data + special_type_data
    
    cursor.executemany("""
        INSERT OR IGNORE INTO type_codes 
        (code, category, description, denomination_value, currency_unit) 
        VALUES (?, ?, ?, ?, ?)
    """, all_type_data)
    
    # US Mint facilities
    us_mint_data = [
        ('P', 'US', 'Philadelphia Mint', 'Philadelphia, PA', 'mint', 
         '{"start": 1792, "end": null}', 'First US mint, P mark added 1980'),
        ('D', 'US', 'Denver Mint', 'Denver, CO', 'mint', 
         '{"start": 1906, "end": null}', 'Opened 1906'),
        ('S', 'US', 'San Francisco Mint', 'San Francisco, CA', 'mint', 
         '{"start": 1854, "end": null}', 'Now mainly proofs'),
        ('W', 'US', 'West Point Mint', 'West Point, NY', 'mint', 
         '{"start": 1984, "end": null}', 'Bullion and commemoratives'),
        ('CC', 'US', 'Carson City Mint', 'Carson City, NV', 'mint', 
         '{"start": 1870, "end": 1893}', 'Historic silver dollar mint'),
        ('O', 'US', 'New Orleans Mint', 'New Orleans, LA', 'mint', 
         '{"start": 1838, "end": 1909}', 'Historic Southern mint'),
        ('BEP', 'US', 'Bureau of Engraving and Printing', 'Washington, DC / Fort Worth, TX', 'printing_bureau', 
         '{"start": 1862, "end": null}', 'US paper money printer')
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO mint_facilities 
        (code, country_code, name, location, type, active_period, notes) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, us_mint_data)
    
    conn.commit()
    print("✅ Reference tables populated with initial data")


def update_series_registry_for_international(conn):
    """Update series registry to support international currencies."""
    print("🔧 Updating series registry for international support...")
    
    cursor = conn.cursor()
    
    # Add country_code field if it doesn't exist
    try:
        cursor.execute("ALTER TABLE series_registry ADD COLUMN country_code TEXT DEFAULT 'US'")
        print("  ✅ Added country_code column to series_registry")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  ⚠️  Column country_code already exists in series_registry")
        else:
            raise
    
    # Update existing US series to have explicit country code
    cursor.execute("""
        UPDATE series_registry 
        SET country_code = 'US'
        WHERE country_code IS NULL OR country_code = ''
    """)
    
    conn.commit()
    print("✅ Series registry updated for international support")


def validate_implementation(conn):
    """Validate that the implementation maintains existing data integrity."""
    print("🔍 Validating implementation...")
    
    cursor = conn.cursor()
    
    # Check that all existing US coins still validate
    cursor.execute("SELECT COUNT(*) FROM coins WHERE coin_id NOT GLOB '*-*-*-*'")
    invalid_format = cursor.fetchone()[0]
    if invalid_format > 0:
        raise Exception(f"Found {invalid_format} coins with invalid ID format!")
    
    # Check that all existing coins have the new fields populated
    cursor.execute("SELECT COUNT(*) FROM coins WHERE category IS NULL")
    missing_category = cursor.fetchone()[0]
    if missing_category > 0:
        print(f"⚠️  Found {missing_category} coins missing category field")
    
    # Verify constraint allows both US and international formats
    test_ids = [
        'US-CENT-1909-S',  # Existing US format
        'EU-EURO-2002-A',  # European format
        'XCD-DOLR-2000-ECCB',  # Multi-nation format
        'CN-YUAN-1980-BEI'  # Asian format
    ]
    
    for test_id in test_ids:
        try:
            cursor.execute("SELECT ? GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR ? GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR ? GLOB '[A-Z][A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'", 
                           (test_id, test_id, test_id))
            result = cursor.fetchone()[0]
            if result:
                print(f"  ✅ ID format validation passed: {test_id}")
            else:
                print(f"  ❌ ID format validation failed: {test_id}")
        except Exception as e:
            print(f"  ❌ Error testing {test_id}: {e}")
    
    # Check reference table population
    cursor.execute("SELECT COUNT(*) FROM country_codes")
    country_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM type_codes")
    type_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM mint_facilities")
    mint_count = cursor.fetchone()[0]
    
    print(f"  📊 Reference data: {country_count} countries, {type_count} TYPE codes, {mint_count} facilities")
    
    conn.commit()
    print("✅ Implementation validation completed")


def main():
    """Main implementation function."""
    print("🚀 Starting Universal Currency Taxonomy Implementation - Phase 1")
    
    # Create backup
    backup_path = backup_database()
    
    try:
        # Connect to database
        conn = get_database_connection()
        
        # Execute implementation steps
        update_coin_id_constraint(conn)
        add_schema_evolution_fields(conn)
        create_reference_tables(conn)
        populate_initial_reference_data(conn)
        update_series_registry_for_international(conn)
        validate_implementation(conn)
        
        # Close connection
        conn.close()
        
        print("\n🎉 Universal Currency Taxonomy Implementation Complete!")
        print("\n📋 Summary of changes:")
        print("  • Updated coin_id constraint to support international currencies")
        print("  • Added schema evolution fields (category, issuer, series_year, etc.)")
        print("  • Created reference tables for country codes, TYPE codes, and facilities")
        print("  • Populated initial reference data from best practice")
        print("  • Maintained backward compatibility with existing US coins")
        print(f"\n💾 Database backup available at: {backup_path}")
        
    except Exception as e:
        print(f"\n❌ Implementation failed: {e}")
        print(f"💾 Database backup available for restore at: {backup_path}")
        raise


if __name__ == "__main__":
    main()