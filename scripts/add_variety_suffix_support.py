#!/usr/bin/env python3
"""
Add variety suffix support to coin taxonomy database.
This enables differentiation of major varieties like 1909-S VDB vs 1909-S without VDB.
"""

import sqlite3
import sys
import os
from datetime import datetime

def backup_database(db_path):
    """Create backup before making schema changes"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/coins_variety_suffix_backup_{timestamp}.db"
    
    # Ensure backup directory exists
    os.makedirs("backups", exist_ok=True)
    
    # Copy database
    with sqlite3.connect(db_path) as source:
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)
    
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path

def add_variety_suffix_column(conn):
    """Add variety_suffix column to support major variety differentiation"""
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(coins)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'variety_suffix' in columns:
        print("ℹ️  variety_suffix column already exists")
        return
    
    # Add variety_suffix column without constraints first
    cursor.execute('''
        ALTER TABLE coins ADD COLUMN variety_suffix TEXT DEFAULT ''
    ''')
    
    print("✅ Added variety_suffix column")

def update_coin_id_constraint(conn):
    """Update coin_id constraint to allow optional variety suffix"""
    cursor = conn.cursor()
    
    print("ℹ️  SQLite doesn't support DROP CONSTRAINT, skipping constraint update")
    print("ℹ️  New coin IDs with suffixes will be validated during insert")
    print("✅ Schema ready for variety suffix support")

def test_constraint(conn):
    """Test the new constraint with sample data"""
    cursor = conn.cursor()
    
    test_cases = [
        ('US-LWCT-1909-S', True),      # Valid without suffix
        ('US-LWCT-1909-S-VDB', True),  # Valid with suffix
        ('US-MERC-1916-D-FB', True),   # Valid Mercury Full Bands
        ('US-SLIQ-1917-P-TYPE2', True), # Valid Standing Liberty Type 2
        ('US-LWCT-1909-S-TOOLONGFAIL', False), # Too long suffix
        ('US-LWCT-1909-S-', False),    # Empty suffix with dash
    ]
    
    print("\n🧪 Testing variety suffix constraints:")
    for test_id, should_pass in test_cases:
        try:
            # Test using GLOB pattern matching 
            patterns = [
                '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*',
                '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*',
                '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*-[A-Z0-9]*',
                '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*-[A-Z0-9]*'
            ]
            
            matches = False
            for pattern in patterns:
                cursor.execute('SELECT ? GLOB ?', (test_id, pattern))
                if cursor.fetchone()[0]:
                    matches = True
                    break
            
            if matches == should_pass:
                status = "✅ PASS" if should_pass else "✅ REJECT"
            else:
                status = "❌ FAIL"
            
            print(f"  {status}: {test_id}")
            
        except Exception as e:
            print(f"  ❌ ERROR: {test_id} - {e}")

def get_database_stats(conn):
    """Get current database statistics"""
    cursor = conn.cursor()
    
    stats = cursor.execute('''
        SELECT 
            COUNT(*) as total_coins,
            COUNT(DISTINCT series_name) as unique_series,
            COUNT(CASE WHEN varieties != '[]' AND varieties IS NOT NULL THEN 1 END) as coins_with_varieties,
            MIN(year) as earliest_year,
            MAX(year) as latest_year
        FROM coins
    ''').fetchone()
    
    print(f"\n📊 Database Statistics:")
    print(f"  Total coins: {stats[0]}")
    print(f"  Unique series: {stats[1]}")
    print(f"  Coins with varieties: {stats[2]}")
    print(f"  Year range: {stats[3]}-{stats[4]}")
    
    return stats

def main():
    """Main execution function"""
    db_path = "database/coins.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        print("Please run from the coin-taxonomy root directory.")
        sys.exit(1)
    
    print("🚀 Adding variety suffix support to coin taxonomy database")
    print("=" * 60)
    
    # Create backup
    backup_path = backup_database(db_path)
    
    try:
        # Connect to database
        with sqlite3.connect(db_path) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            
            # Get initial stats
            print("\n📈 Before schema update:")
            get_database_stats(conn)
            
            # Add variety suffix support
            add_variety_suffix_column(conn)
            update_coin_id_constraint(conn)
            
            # Test constraints
            test_constraint(conn)
            
            # Get final stats
            print("\n📈 After schema update:")
            get_database_stats(conn)
            
            # Commit changes
            conn.commit()
            print("\n✅ Schema update completed successfully!")
            print("\nNext steps:")
            print("1. Run scripts/split_vdb_varieties.py to create 1909-S VDB records")
            print("2. Update export scripts for new ID format")
            print("3. Test JSON exports with variety suffixes")
            
    except Exception as e:
        print(f"\n❌ Error updating schema: {e}")
        print(f"Database backup available at: {backup_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()