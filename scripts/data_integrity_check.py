#!/usr/bin/env python3
"""
Data integrity check script for coin taxonomy database vs JSON files
"""

import sqlite3
import json
import os
from pathlib import Path

def check_database_structure():
    """Check database schema and record count"""
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement
    
    # Get table schema
    cursor.execute("PRAGMA table_info(coins)")
    columns = cursor.fetchall()
    print('Database schema:')
    for col in columns:
        print(f'  {col[1]} ({col[2]})')
    
    print()
    
    # Count records
    cursor.execute('SELECT COUNT(*) FROM coins')
    db_count = cursor.fetchone()[0]
    print(f'Database records: {db_count}')
    
    # Sample records
    cursor.execute('SELECT coin_id, year, mint, series FROM coins LIMIT 5')
    sample_records = cursor.fetchall()
    print('\nSample database records:')
    for record in sample_records:
        print(f'  {record[0]}: {record[1]}-{record[2]} ({record[3]})')
    
    # Check category field compliance - Skip if columns don't exist
    print('\n🏷️ Category Field Validation:')
    
    # Check if category columns exist
    cursor.execute("PRAGMA table_info(coins)")
    columns = [col[1] for col in cursor.fetchall()]
    
    valid_categories = {'coin', 'currency', 'token', 'exonumia'}
    valid_subcategories = {
        'circulation', 'commemorative', 'bullion', 'pattern', 'proof',
        'federal', 'certificate', 'national', 'obsolete', 'confederate', 
        'fractional', 'colonial'
    }
    
    if 'category' in columns and 'subcategory' in columns:
        # Check for valid categories
        cursor.execute("""
            SELECT category, subcategory, COUNT(*) as count
            FROM coins
            GROUP BY category, subcategory
            ORDER BY category, subcategory
        """)
        
        category_errors = []
        for row in cursor.fetchall():
            category = row[0]
            subcategory = row[1]
            count = row[2]
            
            if category and category not in valid_categories:
                category_errors.append(f"Invalid category '{category}': {count} coins")
            
            if subcategory and subcategory not in valid_subcategories:
                category_errors.append(f"Invalid subcategory '{subcategory}': {count} coins")
        
        if category_errors:
            print("  ⚠️ Category validation issues:")
            for error in category_errors:
                print(f"    - {error}")
        else:
            print("  ✅ All categories and subcategories are valid")
    else:
        print("  ⚠️ Category/subcategory columns not present in database schema")
    
    # Check issues table object_type
    cursor.execute("""
        SELECT object_type, COUNT(*) as count
        FROM issues
        GROUP BY object_type
    """)
    
    for row in cursor.fetchall():
        object_type = row[0]
        count = row[1]
        if object_type not in valid_categories:
            print(f"  ⚠️ Issues table has invalid object_type '{object_type}': {count} entries")
    
    conn.close()
    return db_count

def check_json_files():
    """Check JSON file records and structure"""
    json_count = 0
    coins_data = []
    
    json_dir = Path('data/us/coins/')
    for filename in json_dir.glob('*.json'):
        if filename.name == 'cents_old.json':
            continue
            
        with open(filename) as f:
            data = json.load(f)
            
        print(f'\nChecking {filename.name}:')
        for series in data['series']:
            series_name = series.get('series_name', series.get('series_id', 'Unknown'))
            
            if 'coins' in series:
                # New structure
                coin_count = len(series['coins'])
                json_count += coin_count
                print(f'  {series_name}: {coin_count} coins (new structure)')
                
                # Sample coins
                for coin in series['coins'][:3]:
                    coin_id = coin.get('coin_id', 'No ID')
                    year = coin.get('year', 'No year')
                    mint = coin.get('mint', 'No mint')
                    coins_data.append((coin_id, year, mint, series_name))
                    
            elif 'mintages' in series:
                # Old structure
                coin_count = 0
                for year_data in series['mintages'].values():
                    coin_count += len(year_data)
                json_count += coin_count
                print(f'  {series_name}: {coin_count} coins (old structure)')
    
    print(f'\nTotal JSON file records: {json_count}')
    
    print('\nSample JSON records:')
    for record in coins_data[:5]:
        print(f'  {record[0]}: {record[1]}-{record[2]} ({record[3]})')
    
    return json_count

def main():
    print("=== COIN TAXONOMY DATA INTEGRITY CHECK ===\n")
    
    try:
        db_count = check_database_structure()
        json_count = check_json_files()
        
        print(f"\n=== SUMMARY ===")
        print(f"Database records: {db_count}")
        print(f"JSON file records: {json_count}")
        print(f"Difference: {abs(db_count - json_count)}")
        
        if db_count == json_count:
            print("✅ DATA INTEGRITY: Database and JSON files are in sync")
        else:
            print("⚠️  DATA INTEGRITY: Database and JSON files are OUT OF SYNC")
            print("   This indicates the database needs to be updated or JSON files regenerated")
            
    except Exception as e:
        print(f"❌ ERROR during integrity check: {e}")

if __name__ == "__main__":
    main()