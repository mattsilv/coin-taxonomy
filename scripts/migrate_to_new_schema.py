#!/usr/bin/env python3
"""
Migrate database schema to match new JSON structure
CRITICAL: This updates the database to be the source of truth
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

def backup_database():
    """Create backup before migration"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/coins_pre_schema_migration_{timestamp}.db"
    os.makedirs("backups", exist_ok=True)
    
    # Copy database
    import shutil
    shutil.copy2("database/coins.db", backup_path)
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path

def create_new_schema(conn):
    """Create new table with updated schema"""
    cursor = conn.cursor()
    
    # Create new table with correct schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coins_new (
        coin_id TEXT PRIMARY KEY,
        series_id TEXT NOT NULL,
        country TEXT NOT NULL,
        denomination TEXT NOT NULL,
        series_name TEXT NOT NULL,
        year INTEGER NOT NULL,
        mint TEXT NOT NULL,
        business_strikes INTEGER,
        proof_strikes INTEGER,
        rarity TEXT,
        composition JSON,
        weight_grams REAL,
        diameter_mm REAL,
        varieties JSON,
        source_citation TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    print("✅ New schema created")

def populate_from_json_files(conn):
    """Populate new table from current JSON files (which have correct structure)"""
    cursor = conn.cursor()
    
    records_inserted = 0
    json_dir = Path('data/us/coins/')
    
    for filename in json_dir.glob('*.json'):
        if filename.name == 'cents_old.json':
            continue
            
        with open(filename) as f:
            data = json.load(f)
        
        country = data['country']
        denomination = data['denomination']
        
        for series in data['series']:
            series_id = series.get('series_id')
            series_name = series.get('series_name')
            
            if not series_id:
                print(f"⚠️ Missing series_id in {filename.name}, series: {series_name}")
                continue
                
            if 'coins' not in series:
                print(f"⚠️ No coins array in {filename.name}, series: {series_name}")
                continue
                
            for coin in series['coins']:
                coin_id = coin.get('coin_id')
                if not coin_id:
                    print(f"⚠️ Missing coin_id in {filename.name}")
                    continue
                
                # Extract composition and weight from series data
                composition = None
                weight_grams = None
                diameter_mm = None
                
                if 'composition_periods' in series:
                    # Find matching composition period
                    year = coin.get('year')
                    for period in series['composition_periods']:
                        date_range = period.get('date_range', {})
                        start = date_range.get('start')
                        end = date_range.get('end', 'present')
                        
                        if start and year >= start:
                            if end == 'present' or year <= end:
                                composition = json.dumps({
                                    'alloy_name': period.get('alloy_name'),
                                    'alloy': period.get('alloy', {})
                                })
                                weight = period.get('weight', {})
                                weight_grams = weight.get('grams')
                                break
                
                if 'specifications' in series:
                    specs = series['specifications']
                    diameter_mm = specs.get('diameter_mm')
                
                # Insert record
                cursor.execute("""
                INSERT OR REPLACE INTO coins_new (
                    coin_id, series_id, country, denomination, series_name,
                    year, mint, business_strikes, proof_strikes, rarity,
                    composition, weight_grams, diameter_mm, varieties,
                    source_citation, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    coin_id,
                    series_id,
                    country,
                    denomination,
                    series_name,
                    coin.get('year'),
                    coin.get('mint'),
                    coin.get('business_strikes'),
                    coin.get('proof_strikes'),
                    coin.get('rarity'),
                    composition,
                    weight_grams,
                    diameter_mm,
                    json.dumps(coin.get('varieties', [])),
                    coin.get('source_citation'),
                    coin.get('notes')
                ))
                records_inserted += 1
    
    print(f"✅ Inserted {records_inserted} records from JSON files")
    return records_inserted

def finalize_migration(conn):
    """Replace old table with new one"""
    cursor = conn.cursor()
    
    # Drop old table and rename new one
    cursor.execute("DROP TABLE IF EXISTS coins")
    cursor.execute("ALTER TABLE coins_new RENAME TO coins")
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_coins_series_id ON coins(series_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_coins_year ON coins(year)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_coins_mint ON coins(mint)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_coins_rarity ON coins(rarity)")
    
    print("✅ Migration finalized - old table replaced")

def main():
    print("=== DATABASE SCHEMA MIGRATION ===\n")
    print("This will migrate the database to match the new JSON structure")
    print("The database will become the source of truth after this migration\n")
    
    try:
        # Backup
        backup_path = backup_database()
        
        # Connect and migrate
        conn = sqlite3.connect('database/coins.db')
        
        create_new_schema(conn)
        record_count = populate_from_json_files(conn)
        finalize_migration(conn)
        
        conn.commit()
        conn.close()
        
        print(f"\n=== MIGRATION COMPLETE ===")
        print(f"✅ {record_count} records migrated")
        print(f"✅ Database schema updated")
        print(f"✅ Backup available: {backup_path}")
        print(f"\n🎯 Database is now the SOURCE OF TRUTH")
        print(f"🎯 Use scripts/export_db.py to generate JSON files")
        
    except Exception as e:
        print(f"❌ MIGRATION FAILED: {e}")
        print(f"💾 Database backup available for restore: {backup_path}")
        raise

if __name__ == "__main__":
    main()