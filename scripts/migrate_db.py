#!/usr/bin/env python3
"""
Database migration script to safely update schema while preserving existing data.
"""

import sqlite3
import json
import os
from datetime import datetime

def migrate_database(db_path='database/coins.db'):
    """Safely migrate database to new schema"""
    
    # Create backup first
    backup_path = f"backups/coins_migration_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    os.makedirs('backups', exist_ok=True)
    
    if os.path.exists(db_path):
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    conn = sqlite3.connect(db_path)
    
    # Check if new columns exist
    cursor = conn.execute("PRAGMA table_info(coins)")
    columns = [row[1] for row in cursor.fetchall()]
    
    needed_columns = ['key_date_status', 'varieties', 'source_citation']
    missing_columns = [col for col in needed_columns if col not in columns]
    
    if missing_columns:
        print(f"Adding missing columns: {missing_columns}")
        
        for column in missing_columns:
            if column == 'key_date_status':
                conn.execute('ALTER TABLE coins ADD COLUMN key_date_status TEXT CHECK(key_date_status IN ("key", "semi-key", "common", "scarce"))')
            elif column == 'varieties':
                conn.execute('ALTER TABLE coins ADD COLUMN varieties JSON')
            elif column == 'source_citation':
                conn.execute('ALTER TABLE coins ADD COLUMN source_citation TEXT')
        
        conn.commit()
        print("Schema migration completed")
    else:
        print("Schema is already up to date")
    
    conn.close()
    return backup_path

def main():
    print("Starting database migration...")
    backup_path = migrate_database()
    print(f"Migration completed. Backup saved to: {backup_path}")

if __name__ == "__main__":
    main()