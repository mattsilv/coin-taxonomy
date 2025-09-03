#!/usr/bin/env python3
"""
Implement Standardized Category Field (Issue #47)

Standardizes category/subcategory fields across the taxonomy system following 
professional numismatic standards (ANA, PCGS/NGC).

Primary Categories:
- coin: Struck metal pieces
- currency: Paper money (banknotes)
- token: Trade/transportation tokens  
- exonumia: Medals, badges, non-legal tender

Subcategories for Coins:
- circulation: Business strikes
- commemorative: Special commemoratives
- bullion: Investment grade (Eagles, Maple Leafs)
- pattern: Trial strikes
- proof: Proof strikes

Subcategories for Currency:
- federal: Federal Reserve Notes
- certificate: Silver/Gold certificates
- national: National Bank Notes
- obsolete: Obsolete banknotes
- confederate: Confederate currency
- fractional: Fractional currency
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import shutil


def backup_database():
    """Create backup before migration."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    source = Path('database/coins.db')
    backup = backup_dir / f'coins_backup_category_field_{timestamp}.db'
    
    shutil.copy(source, backup)
    print(f"✅ Database backed up to {backup}")
    return backup


def update_category_constraint(conn):
    """Add proper category constraint to coins table."""
    cursor = conn.cursor()
    
    print("🔧 Updating category constraint...")
    
    # Check if we need to update the constraint
    cursor.execute("""
        SELECT sql FROM sqlite_master 
        WHERE type='table' AND name='coins'
    """)
    
    table_sql = cursor.fetchone()[0]
    
    if 'CHECK (category IN' not in table_sql:
        # Need to recreate table with constraint
        print("  📝 Adding category validation constraint...")
        
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
                rarity TEXT CHECK(rarity IN ('key', 'semi-key', 'common', 'scarce')),
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
                category TEXT CHECK (category IN ('coin', 'currency', 'token', 'exonumia')),
                issuer TEXT,
                series_year TEXT,
                calendar_type TEXT,
                original_date TEXT,
                seller_name TEXT,
                variety_suffix TEXT DEFAULT '',
                subcategory TEXT CHECK (subcategory IN (
                    'circulation', 'commemorative', 'bullion', 'pattern', 'proof',
                    'federal', 'certificate', 'national', 'obsolete', 'confederate', 
                    'fractional', 'colonial'
                ) OR subcategory IS NULL),
                red_book_category_id TEXT REFERENCES red_book_categories(category_id),
                
                -- Keep existing flexible coin_id constraint
                CONSTRAINT valid_coin_id_format CHECK (
                    coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'
                )
            )
        """)
        
        # Copy data
        cursor.execute("INSERT INTO coins_new SELECT * FROM coins")
        
        # Drop old table and rename
        cursor.execute("DROP TABLE coins")
        cursor.execute("ALTER TABLE coins_new RENAME TO coins")
        
        # Recreate indexes
        cursor.execute("CREATE INDEX idx_coins_series ON coins(series_id)")
        cursor.execute("CREATE INDEX idx_coins_year ON coins(year)")
        cursor.execute("CREATE INDEX idx_coins_denomination ON coins(denomination)")
        cursor.execute("CREATE INDEX idx_coins_rarity ON coins(rarity)")
        cursor.execute("CREATE INDEX idx_coins_seller_name ON coins(seller_name)")
        cursor.execute("CREATE INDEX idx_coins_category ON coins(category)")
        cursor.execute("CREATE INDEX idx_coins_subcategory ON coins(subcategory)")
        
        print("  ✅ Category constraint added")
    else:
        print("  ✓ Category constraint already exists")


def standardize_category_values(conn):
    """Standardize existing category values to lowercase."""
    cursor = conn.cursor()
    
    print("📊 Standardizing category values...")
    
    # Update coins table categories to lowercase
    cursor.execute("""
        UPDATE coins 
        SET category = LOWER(category)
        WHERE category IS NOT NULL
    """)
    
    rows_updated = cursor.rowcount
    print(f"  ✅ Standardized {rows_updated} coin categories")
    
    # Synchronize issues.object_type with new standard
    cursor.execute("""
        UPDATE issues
        SET object_type = 'currency'
        WHERE object_type = 'banknote'
    """)
    
    rows_updated = cursor.rowcount
    print(f"  ✅ Updated {rows_updated} banknote entries to 'currency'")


def identify_currency_entries(conn):
    """Identify and mark paper currency entries."""
    cursor = conn.cursor()
    
    print("💵 Identifying currency entries...")
    
    # Look for paper money keywords in series names
    currency_keywords = [
        'Federal Reserve', 'Silver Certificate', 'Gold Certificate',
        'National Bank', 'Confederate', 'Fractional Currency',
        'Legal Tender', 'Treasury Note', 'Demand Note'
    ]
    
    for keyword in currency_keywords:
        cursor.execute("""
            UPDATE coins
            SET category = 'currency',
                subcategory = CASE
                    WHEN series_name LIKE '%Federal Reserve%' THEN 'federal'
                    WHEN series_name LIKE '%Silver Certificate%' THEN 'certificate'
                    WHEN series_name LIKE '%Gold Certificate%' THEN 'certificate'
                    WHEN series_name LIKE '%National Bank%' THEN 'national'
                    WHEN series_name LIKE '%Confederate%' THEN 'confederate'
                    WHEN series_name LIKE '%Fractional%' THEN 'fractional'
                    ELSE subcategory
                END
            WHERE series_name LIKE ?
            AND category != 'currency'
        """, (f'%{keyword}%',))
        
        if cursor.rowcount > 0:
            print(f"  ✅ Identified {cursor.rowcount} {keyword} entries")


def auto_classify_subcategories(conn):
    """Auto-classify subcategories based on series names."""
    cursor = conn.cursor()
    
    print("🏷️ Auto-classifying subcategories...")
    
    # Bullion coins
    bullion_patterns = [
        'American Silver Eagle', 'American Gold Eagle', 'Gold Buffalo',
        'Maple Leaf', 'Krugerrand', 'Britannia', 'Panda', 'Libertad'
    ]
    
    for pattern in bullion_patterns:
        cursor.execute("""
            UPDATE coins
            SET subcategory = 'bullion'
            WHERE series_name LIKE ?
            AND category = 'coin'
            AND subcategory IS NULL
        """, (f'%{pattern}%',))
        
        if cursor.rowcount > 0:
            print(f"  ✅ Classified {cursor.rowcount} {pattern} as bullion")
    
    # Commemorative coins
    cursor.execute("""
        UPDATE coins
        SET subcategory = 'commemorative'
        WHERE (series_name LIKE '%Commemorative%' OR series_name LIKE '%Anniversary%')
        AND category = 'coin'
        AND subcategory IS NULL
    """)
    
    if cursor.rowcount > 0:
        print(f"  ✅ Classified {cursor.rowcount} commemoratives")
    
    # Default circulation coins
    cursor.execute("""
        UPDATE coins
        SET subcategory = 'circulation'
        WHERE category = 'coin'
        AND subcategory IS NULL
    """)
    
    if cursor.rowcount > 0:
        print(f"  ✅ Set {cursor.rowcount} coins to circulation (default)")


def verify_migration(conn):
    """Verify migration results."""
    cursor = conn.cursor()
    
    print("\n📊 Migration Summary:")
    
    # Check coins table
    cursor.execute("""
        SELECT category, subcategory, COUNT(*) as count
        FROM coins
        GROUP BY category, subcategory
        ORDER BY category, subcategory
    """)
    
    print("\n  Coins Table:")
    for row in cursor.fetchall():
        category = row[0] or 'NULL'
        subcategory = row[1] or 'NULL'
        count = row[2]
        print(f"    {category:10} / {subcategory:15} : {count:5} entries")
    
    # Check issues table
    cursor.execute("""
        SELECT object_type, COUNT(*) as count
        FROM issues
        GROUP BY object_type
        ORDER BY object_type
    """)
    
    print("\n  Issues Table:")
    for row in cursor.fetchall():
        object_type = row[0]
        count = row[1]
        print(f"    {object_type:10} : {count:5} entries")
    
    # Validation checks
    print("\n🔍 Data Integrity Checks:")
    
    # Check for invalid categories
    cursor.execute("""
        SELECT COUNT(*) FROM coins
        WHERE category NOT IN ('coin', 'currency', 'token', 'exonumia')
        AND category IS NOT NULL
    """)
    
    invalid_count = cursor.fetchone()[0]
    if invalid_count > 0:
        print(f"  ⚠️ Found {invalid_count} coins with invalid categories")
    else:
        print(f"  ✅ All categories valid")
    
    # Check for mismatched types
    cursor.execute("""
        SELECT COUNT(*) FROM issues i
        WHERE i.object_type NOT IN ('coin', 'currency', 'token', 'exonumia')
    """)
    
    invalid_count = cursor.fetchone()[0]
    if invalid_count > 0:
        print(f"  ⚠️ Found {invalid_count} issues with invalid object_type")
    else:
        print(f"  ✅ All object_types valid")


def main():
    """Execute category field implementation."""
    print("🚀 Implementing Standardized Category Field (Issue #47)")
    print("=" * 60)
    
    # Backup database
    backup_path = backup_database()
    
    try:
        # Connect to database
        conn = sqlite3.connect('database/coins.db')
        
        # Run migration steps
        update_category_constraint(conn)
        standardize_category_values(conn)
        identify_currency_entries(conn)
        auto_classify_subcategories(conn)
        
        # Commit changes
        conn.commit()
        
        # Verify results
        verify_migration(conn)
        
        conn.close()
        
        print("\n✨ Migration Complete!")
        print("Next steps:")
        print("  1. Run export: uv run python scripts/export_from_database.py")
        print("  2. Test pre-commit: git add . && git commit")
        print("  3. Review generated JSON files")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print(f"Restore from backup: {backup_path}")
        raise


if __name__ == "__main__":
    main()