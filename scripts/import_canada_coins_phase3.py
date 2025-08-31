#!/usr/bin/env python3
"""
Import Canada Coins - Phase 3
Modern circulation coins (1968-present) and bullion series
Implements issue #42
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "coins.db"

def add_modern_circulation_coins():
    """Add modern Canadian circulation coins (1968-present)"""
    coins = []
    
    # Transitional Period Nickel Coins (1968-1999)
    # 5 cents nickel
    for year in range(1968, 2000):
        coins.append({
            'coin_id': f'CA-FIVE-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Five Cents',
            'series': '5 Cents Nickel',
            'composition': '99.9% Ni',
            'weight_grams': 4.54,
            'diameter_mm': 21.2,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Beaver on rock',
            'notes': 'Pure nickel composition period'
        })
    
    # Nickel Dollar (1968-1986)
    for year in range(1968, 1987):
        coins.append({
            'coin_id': f'CA-DOLR-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Dollars',
            'series': 'Nickel Dollar',
            'composition': '100% Ni',
            'weight_grams': 15.62,
            'diameter_mm': 32.13,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Voyageur canoe with bundle',
            'notes': 'Nickel dollar era'
        })
    
    # Loonie (1987-present)
    for year in range(1987, 2025):
        coins.append({
            'coin_id': f'CA-LOON-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Dollars',
            'series': 'Loonie',
            'composition': 'Bronze-plated nickel',
            'weight_grams': 7.0,
            'diameter_mm': 26.5,
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Common loon swimming',
            'designer': 'Robert-Ralph Carmichael',
            'notes': 'First circulation dollar coin'
        })
    
    # Toonie (1996-present)
    for year in range(1996, 2025):
        varieties = []
        if year == 1996:
            varieties.append({'name': 'Beaded pattern', 'premium': True, 'notes': 'Only 4 known examples'})
        
        coins.append({
            'coin_id': f'CA-TWOD-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Two Dollars',
            'series': 'Toonie',
            'composition': 'Bimetallic: Al-bronze core, nickel ring',
            'weight_grams': 7.3,
            'diameter_mm': 28.0,
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Polar bear on ice floe',
            'designer': 'Brent Townshend',
            'varieties': varieties,
            'notes': 'Bimetallic design'
        })
    
    # Multi-ply Steel Era (2000-present)
    # Updated compositions for all denominations
    
    # Steel penny (2000-2012)
    for year in range(2000, 2013):
        coins.append({
            'coin_id': f'CA-CENT-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Cents',
            'series': 'Steel Cent',
            'composition': 'Copper-plated steel',
            'weight_grams': 2.35,
            'diameter_mm': 19.05,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Two maple leaves on twig',
            'notes': 'Final years before discontinuation' if year >= 2010 else 'Multi-ply steel composition'
        })
    
    # Modern 5 cents (2000-present)
    for year in range(2000, 2025):
        coins.append({
            'coin_id': f'CA-FIVE-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Five Cents',
            'series': '5 Cents Steel',
            'composition': '94.5% steel, 3.5% Ni, 2% Cu plating',
            'weight_grams': 3.95,
            'diameter_mm': 21.2,
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Beaver on rock',
            'notes': 'Multi-ply plated steel'
        })
    
    # Modern dime (2000-present)
    for year in range(2000, 2025):
        coins.append({
            'coin_id': f'CA-DIME-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Ten Cents',
            'series': '10 Cents Steel',
            'composition': 'Multi-ply plated steel',
            'weight_grams': 1.75,
            'diameter_mm': 18.03,
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Bluenose schooner',
            'notes': 'Steel core with nickel plating'
        })
    
    # Modern quarter (2000-present)
    for year in range(2000, 2025):
        coins.append({
            'coin_id': f'CA-QRTR-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Twenty-Five Cents',
            'series': '25 Cents Steel',
            'composition': 'Multi-ply plated steel',
            'weight_grams': 4.4,
            'diameter_mm': 23.88,
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Caribou',
            'notes': 'Steel core with nickel plating'
        })
    
    # Modern half dollar (2000-present, limited mintage)
    for year in [2000, 2002, 2010, 2015, 2020]:
        coins.append({
            'coin_id': f'CA-HALF-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Fifty Cents',
            'series': '50 Cents Steel',
            'composition': 'Multi-ply plated steel',
            'weight_grams': 6.9,
            'diameter_mm': 27.13,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Canadian coat of arms',
            'notes': 'Limited mintage for collectors'
        })
    
    return coins

def add_bullion_coins():
    """Add Canadian bullion coin series"""
    coins = []
    
    # Gold Maple Leaf (1979-present)
    for year in range(1979, 2025):
        # 1 oz Gold Maple Leaf
        purity = '.999' if year < 1982 else '.9999'
        if year >= 1982:
            purity_note = '.99999 special editions available' if year >= 2007 else '.9999 fine'
        else:
            purity_note = '.999 fine'
            
        coins.append({
            'coin_id': f'CA-GMPL-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Gold Maple Leaf',
            'series': 'Gold Maple Leaf',
            'composition': f'{purity} Au',
            'weight_grams': 31.103,
            'diameter_mm': 30.0,
            'face_value': '$50',
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Single maple leaf',
            'notes': f'{purity_note}. Security features added 2013+' if year >= 2013 else purity_note
        })
        
        # Fractional sizes
        for size, face_val, weight in [('1/2 oz', '$20', 15.552), ('1/4 oz', '$10', 7.776), 
                                        ('1/10 oz', '$5', 3.110), ('1/20 oz', '$1', 1.555)]:
            if year >= 1982:  # Fractionals started in 1982
                coins.append({
                    'coin_id': f'CA-GMPL-{year}-P-{size.replace(" ", "").replace("/", "")}',
                    'year': year,
                    'mint': 'P',
                    'denomination': f'Gold Maple Leaf {size}',
                    'series': 'Gold Maple Leaf',
                    'composition': '.9999 Au',
                    'weight_grams': weight,
                    'face_value': face_val,
                    'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
                    'reverse_description': 'Single maple leaf',
                    'notes': f'Fractional {size}'
                })
    
    # Special: Big Maple Leaf (2007)
    coins.append({
        'coin_id': 'CA-BGML-2007-P',
        'year': 2007,
        'mint': 'P',
        'denomination': 'Big Maple Leaf',
        'series': 'Gold Maple Leaf',
        'composition': '.99999 Au',
        'weight_grams': 100000,  # 100 kg
        'diameter_mm': 530,
        'face_value': '$1,000,000',
        'obverse_description': 'Queen Elizabeth II bust right',
        'reverse_description': 'Single maple leaf',
        'notes': '100kg coin, only 5 examples minted',
        'rarity': 'unique'
    })
    
    # Silver Maple Leaf (1988-present)
    for year in range(1988, 2025):
        security_note = 'Radial lines and micro-engraved privy mark' if year >= 2014 else ''
        
        coins.append({
            'coin_id': f'CA-SMPL-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Silver Maple Leaf',
            'series': 'Silver Maple Leaf',
            'composition': '.9999 Ag',
            'weight_grams': 31.103,
            'diameter_mm': 38.0,
            'face_value': '$5',
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Single maple leaf',
            'notes': security_note if security_note else 'Standard bullion issue'
        })
        
        # Special Wildlife series (2011-2013)
        if year in [2011, 2012, 2013]:
            wildlife = {
                2011: ['Wolf', 'Grizzly'],
                2012: ['Cougar', 'Moose'],
                2013: ['Wood Bison', 'Pronghorn Antelope']
            }
            for animal in wildlife.get(year, []):
                coins.append({
                    'coin_id': f'CA-SMPL-{year}-P-{animal.replace(" ", "")}',
                    'year': year,
                    'mint': 'P',
                    'denomination': 'Silver Maple Leaf Wildlife',
                    'series': 'Silver Maple Leaf',
                    'composition': '.9999 Ag',
                    'weight_grams': 31.103,
                    'diameter_mm': 38.0,
                    'face_value': '$5',
                    'obverse_description': 'Queen Elizabeth II bust right',
                    'reverse_description': f'{animal} design',
                    'notes': f'Wildlife series - {animal}, limited mintage ~1,000,000'
                })
    
    # Platinum Maple Leaf (1988-present, with gaps)
    platinum_years = list(range(1988, 2003)) + [2009] + list(range(2011, 2025))
    for year in platinum_years:
        purity = '.9995' if year < 2009 else '.9999'
        
        coins.append({
            'coin_id': f'CA-PMPL-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Platinum Maple Leaf',
            'series': 'Platinum Maple Leaf',
            'composition': f'{purity} Pt',
            'weight_grams': 31.103,
            'diameter_mm': 30.0,
            'face_value': '$50',
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Single maple leaf',
            'notes': f'Production gap 2003-2008' if year == 2002 else f'{purity} fine platinum'
        })
    
    # Palladium Maple Leaf (2005-present, with gaps)
    palladium_years = [2005, 2006, 2007, 2009] + list(range(2015, 2025))
    for year in palladium_years:
        coins.append({
            'coin_id': f'CA-PDML-{year}-P',
            'year': year,
            'mint': 'P',
            'denomination': 'Palladium Maple Leaf',
            'series': 'Palladium Maple Leaf',
            'composition': '.9995 Pd',
            'weight_grams': 31.103,
            'diameter_mm': 30.0,
            'face_value': '$50',
            'obverse_description': 'Queen Elizabeth II bust right' if year < 2023 else 'King Charles III bust left',
            'reverse_description': 'Single maple leaf',
            'notes': 'Limited production palladium bullion'
        })
    
    return coins

def add_historical_gold_coins():
    """Add historical Canadian gold coins"""
    coins = []
    
    # $5 Gold (1912-1914)
    for year in range(1912, 1915):
        coins.append({
            'coin_id': f'CA-FIVE-{year}-C',
            'year': year,
            'mint': 'C',
            'denomination': 'Five Dollars',
            'series': '$5 Gold',
            'composition': '90% Au, 10% Cu',
            'weight_grams': 8.36,
            'diameter_mm': 21.6,
            'obverse_description': 'King George V bust left',
            'reverse_description': 'Shield with maple leaves',
            'notes': 'Withdrawn 1914, officially released 2012',
            'rarity': 'scarce'
        })
    
    # $10 Gold (1912-1914)
    for year in range(1912, 1915):
        coins.append({
            'coin_id': f'CA-TENG-{year}-C',
            'year': year,
            'mint': 'C',
            'denomination': 'Ten Dollars',
            'series': '$10 Gold',
            'composition': '90% Au, 10% Cu',
            'weight_grams': 16.72,
            'diameter_mm': 26.92,
            'obverse_description': 'King George V bust left',
            'reverse_description': 'Shield with maple leaves',
            'notes': 'Withdrawn 1914, officially released 2012',
            'rarity': 'scarce'
        })
    
    # British Sovereigns with C mint mark (1908-1919)
    for year in range(1908, 1920):
        if year == 1912 or year == 1915:
            continue  # No sovereigns these years
            
        rarity = 'key' if year == 1916 else 'scarce'
        notes = '~50 known examples, extremely rare' if year == 1916 else 'Ottawa mint, C mint mark'
        
        coins.append({
            'coin_id': f'CA-SOVR-{year}-C',
            'year': year,
            'mint': 'C',
            'denomination': 'Sovereign',
            'series': 'Ottawa Sovereign',
            'composition': '91.67% Au, 8.33% Cu',
            'weight_grams': 7.988,
            'diameter_mm': 22.05,
            'obverse_description': 'King George V bust left' if year >= 1911 else 'King Edward VII bust right',
            'reverse_description': 'St. George slaying dragon',
            'notes': notes,
            'rarity': rarity
        })
    
    return coins

def import_to_database(coins_data):
    """Import coins into the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    imported_count = 0
    skipped_count = 0
    
    for coin in coins_data:
        # Check if coin already exists
        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin['coin_id'],))
        if cursor.fetchone():
            print(f"Skipping existing coin: {coin['coin_id']}")
            skipped_count += 1
            continue
        
        # Handle variety - if there are varieties, store the first one's name
        variety = ''
        if coin.get('varieties'):
            variety = coin['varieties'][0].get('name', '')
        
        # Insert the coin
        cursor.execute("""
            INSERT INTO coins (
                coin_id, year, mint, denomination, series, variety, composition,
                weight_grams, diameter_mm, obverse_description, reverse_description,
                designer, edge, notes, rarity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'],
            coin['year'],
            coin['mint'],
            coin['denomination'],
            coin.get('series', ''),
            variety,
            coin.get('composition', ''),
            coin.get('weight_grams'),
            coin.get('diameter_mm'),
            coin.get('obverse_description', ''),
            coin.get('reverse_description', ''),
            coin.get('designer', ''),
            coin.get('edge', 'Reeded'),
            coin.get('notes', ''),
            coin.get('rarity', 'common')
        ))
        
        imported_count += 1
        
        if imported_count % 50 == 0:
            print(f"Imported {imported_count} coins...")
    
    conn.commit()
    conn.close()
    
    return imported_count, skipped_count

def main():
    """Main import function"""
    print("=" * 60)
    print("CANADA COINS IMPORT - PHASE 3")
    print("Modern Circulation (1968-present) & Bullion Series")
    print("=" * 60)
    
    # Collect all coins
    all_coins = []
    
    print("\n1. Preparing modern circulation coins...")
    modern_coins = add_modern_circulation_coins()
    all_coins.extend(modern_coins)
    print(f"   Prepared {len(modern_coins)} modern circulation coins")
    
    print("\n2. Preparing bullion series...")
    bullion_coins = add_bullion_coins()
    all_coins.extend(bullion_coins)
    print(f"   Prepared {len(bullion_coins)} bullion coins")
    
    print("\n3. Preparing historical gold coins...")
    gold_coins = add_historical_gold_coins()
    all_coins.extend(gold_coins)
    print(f"   Prepared {len(gold_coins)} historical gold coins")
    
    print(f"\nTotal coins to import: {len(all_coins)}")
    
    # Import to database
    print("\n4. Importing to database...")
    imported, skipped = import_to_database(all_coins)
    
    print("\n" + "=" * 60)
    print("IMPORT COMPLETE")
    print(f"Successfully imported: {imported} coins")
    print(f"Skipped (already exist): {skipped} coins")
    print("=" * 60)
    
    # Summary by series
    print("\nSummary by series:")
    series_count = {}
    for coin in all_coins:
        series = coin.get('series', 'Unknown')
        series_count[series] = series_count.get(series, 0) + 1
    
    for series, count in sorted(series_count.items()):
        print(f"  {series}: {count} coins")

if __name__ == "__main__":
    main()