#!/usr/bin/env python3
"""
Initialize SQLite database from JSON data files.

This script reads the denomination-specific JSON files and populates
the coins table, which serves as the source for the universal migration.
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

def create_coins_table(conn):
    """Create the original coins table schema."""
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coins (
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
            
            CONSTRAINT valid_coin_id_format CHECK (
                coin_id GLOB 'US-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'
            )
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coins_series ON coins(series_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coins_year ON coins(year)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coins_denomination ON coins(denomination)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coins_rarity ON coins(rarity)')
    
    conn.commit()
    print("✓ Created coins table with proper schema")

def load_denomination_data(file_path):
    """Load coin data from a denomination JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    coins = []
    country = data['country']
    denomination = data['denomination']
    
    for series in data['series']:
        series_id = series['series_id']
        series_name = series['series_name']
        
        # Get specifications and composition data
        specs = series.get('specifications', {})
        diameter_mm = specs.get('diameter_mm')
        
        # Get composition periods for weight calculation
        comp_periods = series.get('composition_periods', [])
        
        for coin in series['coins']:
            # Find appropriate composition period for this coin's year
            year = coin['year']
            weight_grams = None
            composition = None
            
            for period in comp_periods:
                period_start = period['date_range']['start']
                period_end = period['date_range']['end']
                if period_start <= year <= period_end:
                    weight_grams = period.get('weight', {}).get('grams')
                    composition = {
                        'alloy_name': period.get('alloy_name'),
                        'alloy': period.get('alloy', {})
                    }
                    break
            
            coin_record = {
                'coin_id': coin['coin_id'],
                'series_id': series_id,
                'country': country,
                'denomination': denomination,
                'series_name': series_name,
                'year': year,
                'mint': coin['mint'],
                'business_strikes': coin.get('business_strikes'),
                'proof_strikes': coin.get('proof_strikes'),
                'rarity': coin.get('rarity'),
                'composition': json.dumps(composition) if composition else None,
                'weight_grams': weight_grams,
                'diameter_mm': diameter_mm,
                'varieties': json.dumps(coin.get('varieties', [])),
                'source_citation': coin.get('source_citation'),
                'notes': coin.get('notes'),
                'obverse_description': coin.get('obverse_description', ''),
                'reverse_description': coin.get('reverse_description', ''),
                'distinguishing_features': json.dumps(coin.get('distinguishing_features', [])),
                'identification_keywords': json.dumps(coin.get('identification_keywords', [])),
                'common_names': json.dumps(coin.get('common_names', []))
            }
            
            coins.append(coin_record)
    
    return coins

def populate_coins_table(conn):
    """Populate coins table from JSON denomination files."""
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM coins')
    
    data_dir = Path('data/us/coins')
    json_files = list(data_dir.glob('*.json'))
    
    all_coins = []
    
    for json_file in json_files:
        print(f"📖 Loading data from {json_file.name}...")
        coins = load_denomination_data(json_file)
        all_coins.extend(coins)
        print(f"  ➤ Found {len(coins)} coins")
    
    # Insert all coins
    print(f"💾 Inserting {len(all_coins)} coin records...")
    
    insert_sql = '''
        INSERT INTO coins (
            coin_id, series_id, country, denomination, series_name,
            year, mint, business_strikes, proof_strikes, rarity,
            composition, weight_grams, diameter_mm, varieties,
            source_citation, notes, obverse_description, reverse_description,
            distinguishing_features, identification_keywords, common_names
        ) VALUES (
            :coin_id, :series_id, :country, :denomination, :series_name,
            :year, :mint, :business_strikes, :proof_strikes, :rarity,
            :composition, :weight_grams, :diameter_mm, :varieties,
            :source_citation, :notes, :obverse_description, :reverse_description,
            :distinguishing_features, :identification_keywords, :common_names
        )
    '''
    
    cursor.executemany(insert_sql, all_coins)
    conn.commit()
    
    # Verify insertion
    cursor.execute('SELECT COUNT(*) FROM coins')
    count = cursor.fetchone()[0]
    print(f"✓ Successfully inserted {count} coin records")
    
    return count

def main():
    """Initialize database from JSON files."""
    print("🗄️  Database Initialization from JSON Data")
    print("=" * 50)
    
    # Ensure database directory exists
    db_dir = Path('database')
    db_dir.mkdir(exist_ok=True)
    
    db_path = db_dir / 'coins.db'
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    conn.execute('PRAGMA foreign_keys = ON')
    
    try:
        # Create tables
        create_coins_table(conn)
        
        # Populate with data
        coin_count = populate_coins_table(conn)
        
        print(f"\n🎉 Database initialization completed!")
        print(f"📊 Total coins in database: {coin_count}")
        print(f"💾 Database location: {db_path}")
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()