#!/usr/bin/env python3
"""
Builds SQLite database from JSON source files.
Handles multiple countries seamlessly.
"""

import json
import sqlite3
import glob
import os

def create_tables(conn):
    conn.executescript('''
        -- Main coin reference table
        CREATE TABLE IF NOT EXISTS coins (
            id TEXT PRIMARY KEY,
            country TEXT NOT NULL,
            denomination TEXT NOT NULL,
            series TEXT NOT NULL,
            year INTEGER NOT NULL,
            mint TEXT NOT NULL,
            
            -- Composition and specifications
            composition JSON,
            weight_grams REAL,
            diameter_mm REAL,
            
            -- Mintage data
            mintage INTEGER,
            proof_mintage INTEGER,
            
            -- Rarity and varieties
            key_date_status TEXT CHECK(key_date_status IN ('key', 'semi-key', 'common', 'scarce')),
            varieties JSON,
            
            -- Source attribution
            source_citation TEXT,
            
            -- Metadata
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Full-text search
        CREATE VIRTUAL TABLE IF NOT EXISTS coin_search 
        USING fts5(
            canonical_name, 
            search_terms,
            content=coins
        );
        
        -- Grade reference table
        CREATE TABLE IF NOT EXISTS grades (
            grade_word TEXT PRIMARY KEY,
            abbreviation TEXT,
            description TEXT,
            numeric_range TEXT,
            country TEXT
        );
        
        CREATE INDEX IF NOT EXISTS idx_coins_country ON coins(country);
        CREATE INDEX IF NOT EXISTS idx_coins_year_mint ON coins(year, mint);
        CREATE INDEX IF NOT EXISTS idx_coins_series ON coins(series);
    ''')

def import_country_data(conn, country_code):
    """Import all coin data for a specific country"""
    coin_files = glob.glob(f'data/{country_code}/coins/*.json')
    
    for filepath in coin_files:
        with open(filepath) as f:
            data = json.load(f)
        
        # Import each series in the file
        for series_data in data.get('series', []):
            import_series(conn, country_code, data['denomination'], series_data)
    
    # Import grade definitions if they exist
    grades_file = f'data/{country_code}/references/grades.json'
    if os.path.exists(grades_file):
        with open(grades_file) as f:
            grades_data = json.load(f)
        
        for grade, info in grades_data.get('grades', {}).items():
            conn.execute('''
                INSERT OR REPLACE INTO grades 
                (grade_word, abbreviation, description, numeric_range, country)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                grade,
                info.get('abbreviation'),
                info.get('description'),
                info.get('numeric_equivalent'),
                country_code.upper()
            ))

def import_series(conn, country, denomination, series_data):
    """Import a single series worth of coins"""
    series_name = series_data['series_name']
    
    # Get composition for different periods
    comp_periods = series_data.get('composition_periods', [])
    
    # Process mintages
    for year_str, mint_data in series_data.get('mintages', {}).items():
        year = int(year_str)
        
        # Find applicable composition
        composition = None
        weight = None
        for period in comp_periods:
            start = period['date_range']['start']
            end = period['date_range']['end']
            if end == 'present':
                end = 9999
            if start <= year <= end:
                composition = period['alloy']
                weight = period['weight'].get('grams')
                break
        
        # Insert coin for each mint
        for mint, details in mint_data.items():
            if details is None:
                continue
                
            coin_id = f"{country}-{year}-{mint}-{series_name.replace(' ', '_')}"
            
            conn.execute('''
                INSERT OR REPLACE INTO coins 
                (id, country, denomination, series, year, mint, 
                 composition, weight_grams, diameter_mm, mintage, 
                 proof_mintage, key_date_status, varieties, source_citation, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coin_id,
                country.upper(),
                denomination,
                series_name,
                year,
                mint,
                json.dumps(composition) if composition else None,
                weight,
                series_data.get('specifications', {}).get('diameter_mm'),
                details.get('mintage'),
                details.get('proof_mintage'),
                details.get('key_date_status'),
                json.dumps(details.get('varieties')) if details.get('varieties') else None,
                details.get('source_citation'),
                details.get('notes')
            ))

def build_search_index(conn):
    """Build search index for all countries"""
    conn.execute('''
        INSERT INTO coin_search (canonical_name, search_terms)
        SELECT 
            printf('%s %d-%s %s', country, year, mint, series) as canonical_name,
            printf('%s %d %s %s %s', country, year, mint, series, denomination) as search_terms
        FROM coins
    ''')

def main():
    print("Building database...")
    
    # Ensure database directory exists
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement
    create_tables(conn)
    
    # Import data for each country
    countries = [d for d in os.listdir('data') 
                 if os.path.isdir(f'data/{d}') and len(d) == 2]
    
    for country in countries:
        print(f"Importing {country.upper()} data...")
        import_country_data(conn, country)
    
    print("Building search index...")
    build_search_index(conn)
    
    conn.commit()
    
    # Print statistics
    stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT country) as countries,
            COUNT(DISTINCT series) as series,
            COUNT(*) as total_coins,
            MIN(year) as earliest,
            MAX(year) as latest
        FROM coins
    ''').fetchone()
    
    print(f"\nDatabase built successfully!")
    print(f"Countries: {stats[0]}")
    print(f"Series: {stats[1]}")
    print(f"Total coins: {stats[2]}")
    print(f"Year range: {stats[3]}-{stats[4]}")
    
    conn.close()

if __name__ == "__main__":
    main()