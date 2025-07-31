#!/usr/bin/env python3
"""
Database schema migration to make visual description fields required.

This script updates the SQLite database schema to enforce that all visual 
description fields are NOT NULL, ensuring future coin entries must include 
complete visual descriptions.

WARNING: This migration is irreversible. Backup your database first.
"""

import sqlite3
import os
import sys
from datetime import datetime

def backup_database(db_path):
    """Create a backup of the database before migration."""
    backup_path = f"backups/coins_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    os.makedirs("backups", exist_ok=True)
    
    # Copy database file
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path

def check_visual_data_completeness(conn):
    """Check if all existing coins have complete visual descriptions."""
    cursor = conn.cursor()
    
    # Check for any missing visual description fields
    cursor.execute('''
        SELECT coin_id, 
               CASE WHEN obverse_description IS NULL OR obverse_description = '' THEN 'obverse_description' END as missing_obverse,
               CASE WHEN reverse_description IS NULL OR reverse_description = '' THEN 'reverse_description' END as missing_reverse,
               CASE WHEN distinguishing_features IS NULL OR distinguishing_features = '[]' THEN 'distinguishing_features' END as missing_features,
               CASE WHEN identification_keywords IS NULL OR identification_keywords = '[]' THEN 'identification_keywords' END as missing_keywords,
               CASE WHEN common_names IS NULL OR common_names = '[]' THEN 'common_names' END as missing_names
        FROM coins
        WHERE obverse_description IS NULL OR obverse_description = ''
           OR reverse_description IS NULL OR reverse_description = ''
           OR distinguishing_features IS NULL OR distinguishing_features = '[]'
           OR identification_keywords IS NULL OR identification_keywords = '[]'
           OR common_names IS NULL OR common_names = '[]'
    ''')
    
    missing_data = cursor.fetchall()
    
    if missing_data:
        print("❌ ERROR: Found coins with missing visual descriptions:")
        for row in missing_data:
            coin_id = row[0]
            missing_fields = [field for field in row[1:] if field is not None]
            print(f"  - {coin_id}: Missing {', '.join(missing_fields)}")
        return False
    
    print("✅ All existing coins have complete visual descriptions")
    return True

def update_schema(conn):
    """Update the database schema to make visual fields NOT NULL."""
    cursor = conn.cursor()
    
    print("🔄 Updating database schema...")
    
    # SQLite doesn't support ALTER COLUMN to add NOT NULL constraint directly
    # We need to recreate the table with the new constraints
    
    # First, get the current table schema
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='coins'")
    original_schema = cursor.fetchone()[0]
    print(f"📋 Current schema: {original_schema}")
    
    # Create new table with NOT NULL constraints for visual fields
    cursor.execute('''
        DROP TABLE IF EXISTS coins_new
    ''')
    
    cursor.execute('''
        CREATE TABLE coins_new (
            coin_id TEXT PRIMARY KEY,
            series_id TEXT NOT NULL,
            country TEXT NOT NULL DEFAULT 'US',
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
            
            CONSTRAINT valid_coin_id_format CHECK (
                coin_id GLOB 'US-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'
            )
        )
    ''')
    
    print("✅ Created new table with NOT NULL constraints")
    
    # Copy all data from old table to new table
    cursor.execute('''
        INSERT INTO coins_new 
        SELECT * FROM coins
    ''')
    
    print("✅ Copied all data to new table")
    
    # Drop old table and rename new table
    cursor.execute('DROP TABLE coins')
    cursor.execute('ALTER TABLE coins_new RENAME TO coins')
    
    print("✅ Schema migration completed")
    
    # Recreate indexes if they existed
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_coins_series_id ON coins(series_id)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_coins_year ON coins(year)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_coins_rarity ON coins(rarity)
    ''')
    
    print("✅ Recreated indexes")

def update_issues_table(conn):
    """Update the issues table schema if it exists."""
    cursor = conn.cursor()
    
    # Check if issues table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='issues'")
    if not cursor.fetchone():
        print("ℹ️  Issues table doesn't exist, skipping")
        return
    
    print("🔄 Updating issues table schema...")
    
    # Get current issues table schema
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='issues'")
    issues_schema = cursor.fetchone()
    if not issues_schema:
        print("ℹ️  No issues table found")
        return
    
    # Check if issues table has visual description fields
    cursor.execute("PRAGMA table_info(issues)")
    columns = [col[1] for col in cursor.fetchall()]
    
    visual_fields = ['obverse_description', 'reverse_description', 'distinguishing_features', 
                    'identification_keywords', 'common_names']
    
    if not all(field in columns for field in visual_fields):
        print("ℹ️  Issues table doesn't have visual description fields, skipping")
        return
    
    # Get the exact structure of the current issues table
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='issues'")
    issues_schema = cursor.fetchone()[0]
    
    # Create new issues table with the same structure but NOT NULL constraints for visual fields
    cursor.execute('DROP TABLE IF EXISTS issues_new')
    
    # Build the new table schema based on the existing one, adding NOT NULL to visual fields
    new_schema = issues_schema.replace(
        'obverse_description TEXT', 'obverse_description TEXT NOT NULL'
    ).replace(
        'reverse_description TEXT', 'reverse_description TEXT NOT NULL'
    ).replace(
        'distinguishing_features TEXT', 'distinguishing_features TEXT NOT NULL'
    ).replace(
        'identification_keywords TEXT', 'identification_keywords TEXT NOT NULL'
    ).replace(
        'CREATE TABLE issues', 'CREATE TABLE issues_new'
    )
    
    # Add common_names field if it doesn't exist
    if 'common_names' not in issues_schema:
        new_schema = new_schema.replace(
            'identification_keywords TEXT NOT NULL',
            'identification_keywords TEXT NOT NULL, common_names TEXT NOT NULL'
        )
    else:
        new_schema = new_schema.replace(
            'common_names TEXT', 'common_names TEXT NOT NULL'
        )
    
    cursor.execute(new_schema)
    
    # Copy data - need to handle the case where common_names might not exist
    if 'common_names' not in issues_schema:
        cursor.execute('''
            INSERT INTO issues_new 
            SELECT *, '["Unknown"]' as common_names FROM issues
        ''')
    else:
        cursor.execute('INSERT INTO issues_new SELECT * FROM issues')
    
    cursor.execute('DROP TABLE issues')
    cursor.execute('ALTER TABLE issues_new RENAME TO issues')
    
    print("✅ Issues table schema updated")

def main():
    """Main migration function."""
    db_path = "database/coins.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        sys.exit(1)
    
    print("🚀 Starting visual descriptions requirement migration...")
    print(f"📁 Database: {db_path}")
    
    # Create backup
    backup_path = backup_database(db_path)
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Check data completeness first
        if not check_visual_data_completeness(conn):
            print("\n❌ MIGRATION FAILED: Some coins are missing visual descriptions")
            print("Please ensure all coins have complete visual descriptions before running this migration")
            conn.close()
            sys.exit(1)
        
        # Update schema
        update_schema(conn)
        
        # Skip issues table update - it contains different data structure and records
        print("ℹ️  Skipping issues table - contains different record structure")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("\n🎉 Migration completed successfully!")
        print("✅ All visual description fields are now required for new coin entries")
        print(f"💾 Backup saved at: {backup_path}")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print(f"💾 Database backup available at: {backup_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()