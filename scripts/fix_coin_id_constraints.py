#!/usr/bin/env python3
"""
Fix Coin ID Constraints for Edge Cases

The initial implementation was too restrictive for edge cases like:
- Japanese era names in TYPE field (OSA instead of 4 letters)
- Large denomination abbreviations (100T, MPC5)
- Complex mint codes (ECCB, etc.)

This script updates the constraint to be more flexible while maintaining format integrity.
"""

import sqlite3
from datetime import datetime


def get_database_connection():
    """Get connection to the coins database."""
    return sqlite3.connect('database/coins.db')


def backup_database():
    """Create a backup of the database before making changes."""
    import shutil
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'backups/coins_backup_constraint_fix_{timestamp}.db'
    shutil.copy('database/coins.db', backup_path)
    print(f"✅ Database backed up to {backup_path}")
    return backup_path


def update_coin_id_constraint(conn):
    """Update the coin_id constraint to handle edge cases properly."""
    print("🔧 Updating coin_id constraint for edge case support...")
    
    cursor = conn.cursor()
    
    # Create new table with more flexible constraint
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
            category TEXT,
            issuer TEXT,
            series_year TEXT,
            calendar_type TEXT,
            original_date TEXT,
            
            -- Updated flexible constraint for international currencies and edge cases
            CONSTRAINT valid_coin_id_format CHECK (
                -- Basic 4-part structure: COUNTRY-TYPE-YEAR-MINT
                coin_id GLOB '*-*-*-*' AND
                -- No empty parts
                coin_id NOT GLOB '*--*' AND
                coin_id NOT GLOB '-*' AND
                coin_id NOT GLOB '*-' AND
                -- Must have exactly 3 dashes
                (length(coin_id) - length(replace(coin_id, '-', ''))) = 3
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
    print("✅ Updated coin_id constraint to handle edge cases")


def test_edge_case_formats(conn):
    """Test that edge case formats now work."""
    cursor = conn.cursor()
    
    print("🔍 Testing edge case ID formats...")
    
    # Test cases that should now work
    test_ids = [
        'US-CENT-1909-S',     # Standard US format
        'JP-YEN-1970-OSA',    # Japanese with 3-char mint  
        'DE-NG50-1921-BER',   # German Notgeld
        'ZW-100T-2008-RBZ',   # Zimbabwe hyperinflation
        'US-MPC5-1970-DOD',   # Military Payment Certificate
        'EU-EURO-2002-A',     # Euro standard
        'XCD-DOLR-2000-ECCB', # Multi-nation with 4-char mint
        'CN-YUAN-1980-BEI',   # Chinese standard
        'CA-MAPL-2020-W'      # Canadian bullion
    ]
    
    for test_id in test_ids:
        try:
            # Test if the constraint allows this format
            cursor.execute("""
                SELECT CASE 
                    WHEN ? GLOB '*-*-*-*' AND
                         ? NOT GLOB '*--*' AND
                         ? NOT GLOB '-*' AND
                         ? NOT GLOB '*-' AND
                         (length(?) - length(replace(?, '-', ''))) = 3
                    THEN 1 ELSE 0 END
            """, (test_id, test_id, test_id, test_id, test_id, test_id))
            
            result = cursor.fetchone()[0]
            if result:
                print(f"  ✅ Format validation passed: {test_id}")
            else:
                print(f"  ❌ Format validation failed: {test_id}")
                
        except Exception as e:
            print(f"  ❌ Error testing {test_id}: {e}")


def main():
    """Main function to fix coin ID constraints."""
    print("🚀 Starting Coin ID Constraint Fix for Edge Cases")
    
    # Create backup
    backup_path = backup_database()
    
    try:
        # Connect to database
        conn = get_database_connection()
        
        # Update constraint
        update_coin_id_constraint(conn)
        
        # Test edge case formats
        test_edge_case_formats(conn)
        
        # Close connection
        conn.close()
        
        print("\n🎉 Coin ID Constraint Fix Complete!")
        print("✅ Database now supports edge cases like:")
        print("  • Japanese era coins (JP-YEN-1970-OSA)")
        print("  • German Notgeld (DE-NG50-1921-BER)")
        print("  • Hyperinflation notes (ZW-100T-2008-RBZ)")
        print("  • Military Payment Certificates (US-MPC5-1970-DOD)")
        print("  • Multi-nation currencies (XCD-DOLR-2000-ECCB)")
        print(f"\n💾 Database backup available at: {backup_path}")
        
    except Exception as e:
        print(f"\n❌ Constraint fix failed: {e}")
        print(f"💾 Database backup available for restore at: {backup_path}")
        raise


if __name__ == "__main__":
    main()