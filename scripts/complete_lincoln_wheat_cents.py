#!/usr/bin/env python3
"""
Complete Lincoln Wheat Cent Series Migration (1909-1958)
Adds all missing years and mint marks for the Lincoln Wheat Cent series.
"""

import sqlite3
import json
from datetime import datetime

def get_db_connection():
    """Get database connection with foreign key support."""
    conn = sqlite3.connect('database/coins.db')
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def get_wheat_cent_specs(year):
    """Get specifications for Lincoln Wheat Cent by year."""
    # Composition changes over time
    if year <= 1942:
        composition = {"alloy_name": "Bronze", "alloy": {"copper": 0.95, "tin": 0.04, "zinc": 0.01}}
        weight = 3.11
    elif year == 1943:
        composition = {"alloy_name": "Steel with Zinc Coating", "alloy": {"steel": 0.99, "zinc_coating": 0.01}}
        weight = 2.70
    elif 1944 <= year <= 1962:
        composition = {"alloy_name": "Brass", "alloy": {"copper": 0.95, "zinc": 0.05}}
        weight = 3.11
    else:  # 1963-1982 (but wheat ends in 1958)
        composition = {"alloy_name": "Bronze", "alloy": {"copper": 0.95, "tin": 0.04, "zinc": 0.01}}
        weight = 3.11
    
    return {
        'composition': composition,
        'weight': weight,
        'diameter': 19.05,
        'obverse': 'Abraham Lincoln bust right with LIBERTY, IN GOD WE TRUST, date',
        'reverse': 'Two wheat stalks flanking ONE CENT and UNITED STATES OF AMERICA'
    }

def get_mint_marks_by_year(year):
    """Get applicable mint marks for each year."""
    mints = ['P']  # Philadelphia always produced
    
    if year >= 1909:
        mints.append('S')  # San Francisco started 1909
    if year >= 1911:
        mints.append('D')  # Denver started 1911
        
    # Special cases where certain mints didn't produce
    if year == 1922:
        mints = ['D']  # Only Denver produced cents in 1922
    if year == 1931:
        mints = ['P', 'S']  # No Denver cents in 1931
    if year == 1932 or year == 1933:
        mints = ['P']  # Only Philadelphia during Depression
        
    return mints

def get_rarity_for_year_mint(year, mint):
    """Determine rarity based on historical production data."""
    key_dates = {
        (1909, 'S'): 'key',      # 484,000 minted
        (1914, 'D'): 'key',      # 1,193,000 minted
        (1922, 'D'): 'semi-key', # No mint mark variety exists
        (1924, 'D'): 'semi-key', # 2,520,000 minted
        (1926, 'S'): 'semi-key', # 4,550,000 minted
        (1931, 'S'): 'key',      # 866,000 minted
        (1943, 'P'): 'key',      # Bronze variety (error)
        (1955, 'P'): 'semi-key', # Doubled die variety
    }
    
    if (year, mint) in key_dates:
        return key_dates[(year, mint)]
    
    # Early years generally scarcer
    if year <= 1915:
        return 'scarce' if mint != 'P' else 'common'
    
    return 'common'

def get_notes_for_year_mint(year, mint):
    """Get specific notes for key varieties and dates."""
    notes_map = {
        (1909, 'S'): 'First year San Francisco issue. Key date with only 484,000 minted.',
        (1914, 'D'): 'Second scarcest regular issue wheat cent. Only 1,193,000 minted.',
        (1922, 'D'): 'No mint mark variety exists due to filled die. Look for weak or missing D.',
        (1931, 'S'): 'Great Depression era rarity. Only 866,000 minted.',
        (1943, 'P'): 'Steel cent year. Bronze variety error worth $100,000+.',
        (1955, 'P'): 'Famous doubled die variety worth $1,000+ in circulated condition.',
    }
    
    return notes_map.get((year, mint), f'{year} Lincoln Wheat Cent from {get_mint_name(mint)}.')

def get_mint_name(mint_mark):
    """Get full mint name from mint mark."""
    mint_names = {
        'P': 'Philadelphia',
        'D': 'Denver', 
        'S': 'San Francisco'
    }
    return mint_names.get(mint_mark, 'Unknown')

def insert_wheat_cent_record(conn, year, mint):
    """Insert a single wheat cent record."""
    specs = get_wheat_cent_specs(year)
    coin_id = f'US-LWCT-{year}-{mint}'
    
    # Check if already exists
    cursor = conn.execute('SELECT coin_id FROM coins WHERE coin_id = ?', (coin_id,))
    if cursor.fetchone():
        print(f"  ⏭️  {coin_id} already exists, skipping")
        return False
    
    record = {
        'coin_id': coin_id,
        'series_id': 'lincoln_wheat_cent',
        'country': 'United States',
        'denomination': 'Cents',
        'series_name': 'Lincoln Wheat Cent',
        'year': year,
        'mint': mint,
        'business_strikes': None,
        'proof_strikes': None,
        'rarity': get_rarity_for_year_mint(year, mint),
        'composition': json.dumps(specs['composition']),
        'weight_grams': specs['weight'],
        'diameter_mm': specs['diameter'],
        'varieties': json.dumps([]),
        'source_citation': 'Red Book, PCGS CoinFacts',
        'notes': get_notes_for_year_mint(year, mint),
        'obverse_description': specs['obverse'],
        'reverse_description': specs['reverse'],
        'distinguishing_features': json.dumps([f'Wheat stalks on reverse', f'{year} date', f'{mint} mint mark' if mint != 'P' else 'No mint mark (Philadelphia)']),
        'identification_keywords': json.dumps(['lincoln', 'wheat', 'cent', 'penny', str(year), mint.lower()]),
        'common_names': json.dumps(['Wheat Penny', 'Wheat Cent', 'Lincoln Cent'])
    }
    
    # Insert record
    cursor = conn.execute('''
        INSERT INTO coins (
            coin_id, series_id, country, denomination, series_name, year, mint,
            business_strikes, proof_strikes, rarity, composition, weight_grams, diameter_mm,
            varieties, source_citation, notes, obverse_description, reverse_description,
            distinguishing_features, identification_keywords, common_names
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(record.values()))
    
    print(f"  ✅ Added {coin_id} ({get_rarity_for_year_mint(year, mint)})")
    return True

def main():
    """Add complete Lincoln Wheat Cent series (1909-1958)."""
    print("🌾 Adding Complete Lincoln Wheat Cent Series (1909-1958)")
    print("=" * 60)
    
    conn = get_db_connection()
    added_count = 0
    total_count = 0
    
    try:
        for year in range(1909, 1959):  # 1909-1958 inclusive
            print(f"\n📅 Processing {year}:")
            mint_marks = get_mint_marks_by_year(year)
            
            for mint in mint_marks:
                total_count += 1
                if insert_wheat_cent_record(conn, year, mint):
                    added_count += 1
        
        conn.commit()
        print(f"\n🎯 Migration Complete!")
        print(f"   📊 Added: {added_count} new records")
        print(f"   📊 Total processed: {total_count} records")
        print(f"   📊 Series span: 1909-1958 (50 years)")
        
        # Verify final count
        cursor = conn.execute('SELECT COUNT(*) FROM coins WHERE series_name = "Lincoln Wheat Cent"')
        final_count = cursor.fetchone()[0]
        print(f"   ✅ Database now contains {final_count} Lincoln Wheat Cent records")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()