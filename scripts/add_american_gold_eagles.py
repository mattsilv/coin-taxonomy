#!/usr/bin/env python3
"""
Add American Gold Eagles & Gold Buffalos (1986-2025) - Issue #52

American Gold Eagle bullion and proof coins in four denominations, plus Gold Buffalo
coins following the DATABASE-FIRST workflow. Data sourced from Red Book 2025, 
PCGS CoinFacts, and US Mint records.

Gold Eagles (1986-present):
- $5 (1/10 oz): 16.5mm, 3.393g, .9167 fine gold
- $10 (1/4 oz): 22.0mm, 8.483g, .9167 fine gold  
- $25 (1/2 oz): 27.0mm, 16.966g, .9167 fine gold
- $50 (1 oz): 32.7mm, 33.931g, .9167 fine gold

Gold Buffalos (2006-present):
- $50 (1 oz): 32.7mm, 31.108g, .9999 fine gold

Series Notes:
- Bullion coins: No mint mark (Philadelphia)
- Proof coins: 'W' mint mark (West Point)
- Burnished/Uncirculated: 'W' mint mark (West Point)
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
    backup = backup_dir / f'coins_backup_gold_eagles_{timestamp}.db'
    
    shutil.copy(source, backup)
    print(f"✅ Database backed up to {backup}")
    return backup


def get_gold_eagle_data():
    """Return American Gold Eagle coin data (1986-2025)."""
    
    # Base specifications for Gold Eagles (.9167 fine gold)
    eagle_composition = {"gold": 91.67, "silver": 3.0, "copper": 5.33}
    
    # Gold Buffalo composition (.9999 fine gold)
    buffalo_composition = {"gold": 99.99}
    
    coins = [
        # 1986 - First year Gold Eagles (4 denominations)
        {
            'coin_id': 'US-AGES-1986-P',
            'series_id': 'american_gold_eagle_5',
            'country': 'US',
            'denomination': '$5',
            'series_name': 'American Gold Eagle $5',
            'year': 1986,
            'mint': 'P',
            'business_strikes': 912609,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(eagle_composition),
            'weight_grams': 3.393,
            'diameter_mm': 16.5,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.381, PCGS #9801',
            'notes': 'First year 1/10 oz Gold Eagle',
            'obverse_description': 'Liberty head design by Augustus Saint-Gaudens, Liberty holding torch and olive branch',
            'reverse_description': 'Family of eagles design by Miley Busiek, male eagle carrying olive branch to nest',
            'distinguishing_features': json.dumps([
                "First year American Gold Eagle",
                "1/10 ounce .9167 fine gold",
                "16.5mm diameter smallest Gold Eagle",
                "Saint-Gaudens Liberty obverse",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american gold eagle age 1986 5 dollar 1/10 ounce liberty saint-gaudens bullion fine gold',
            'common_names': json.dumps(['Gold Eagle $5', 'AGE $5', '1/10 oz Gold Eagle']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        {
            'coin_id': 'US-AGET-1986-P',
            'series_id': 'american_gold_eagle_10',
            'country': 'US',
            'denomination': '$10',
            'series_name': 'American Gold Eagle $10',
            'year': 1986,
            'mint': 'P',
            'business_strikes': 726031,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(eagle_composition),
            'weight_grams': 8.483,
            'diameter_mm': 22.0,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.382, PCGS #9802',
            'notes': 'First year 1/4 oz Gold Eagle',
            'obverse_description': 'Liberty head design by Augustus Saint-Gaudens, Liberty holding torch and olive branch',
            'reverse_description': 'Family of eagles design by Miley Busiek, male eagle carrying olive branch to nest',
            'distinguishing_features': json.dumps([
                "First year American Gold Eagle",
                "1/4 ounce .9167 fine gold",
                "22.0mm diameter",
                "Saint-Gaudens Liberty obverse",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american gold eagle age 1986 10 dollar 1/4 ounce liberty saint-gaudens bullion fine gold',
            'common_names': json.dumps(['Gold Eagle $10', 'AGE $10', '1/4 oz Gold Eagle']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        {
            'coin_id': 'US-AGEF-1986-P',
            'series_id': 'american_gold_eagle_25',
            'country': 'US',
            'denomination': '$25',
            'series_name': 'American Gold Eagle $25',
            'year': 1986,
            'mint': 'P',
            'business_strikes': 599566,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(eagle_composition),
            'weight_grams': 16.966,
            'diameter_mm': 27.0,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.383, PCGS #9803',
            'notes': 'First year 1/2 oz Gold Eagle',
            'obverse_description': 'Liberty head design by Augustus Saint-Gaudens, Liberty holding torch and olive branch',
            'reverse_description': 'Family of eagles design by Miley Busiek, male eagle carrying olive branch to nest',
            'distinguishing_features': json.dumps([
                "First year American Gold Eagle",
                "1/2 ounce .9167 fine gold",
                "27.0mm diameter",
                "Saint-Gaudens Liberty obverse",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american gold eagle age 1986 25 dollar 1/2 ounce liberty saint-gaudens bullion fine gold',
            'common_names': json.dumps(['Gold Eagle $25', 'AGE $25', '1/2 oz Gold Eagle']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        {
            'coin_id': 'US-AGEO-1986-P',
            'series_id': 'american_gold_eagle_50',
            'country': 'US',
            'denomination': '$50',
            'series_name': 'American Gold Eagle $50',
            'year': 1986,
            'mint': 'P',
            'business_strikes': 1362650,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(eagle_composition),
            'weight_grams': 33.931,
            'diameter_mm': 32.7,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.384, PCGS #9804',
            'notes': 'First year 1 oz Gold Eagle',
            'obverse_description': 'Liberty head design by Augustus Saint-Gaudens, Liberty holding torch and olive branch',
            'reverse_description': 'Family of eagles design by Miley Busiek, male eagle carrying olive branch to nest',
            'distinguishing_features': json.dumps([
                "First year American Gold Eagle",
                "1 ounce .9167 fine gold",
                "32.7mm diameter largest Gold Eagle",
                "Saint-Gaudens Liberty obverse",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american gold eagle age 1986 50 dollar 1 ounce liberty saint-gaudens bullion fine gold',
            'common_names': json.dumps(['Gold Eagle $50', 'AGE $50', '1 oz Gold Eagle']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        # 1987 - First year proofs
        {
            'coin_id': 'US-AGES-1987-W',
            'series_id': 'american_gold_eagle_5',
            'country': 'US',
            'denomination': '$5',
            'series_name': 'American Gold Eagle $5',
            'year': 1987,
            'mint': 'W',
            'business_strikes': 0,
            'proof_strikes': 580226,
            'rarity': 'common',
            'composition': json.dumps(eagle_composition),
            'weight_grams': 3.393,
            'diameter_mm': 16.5,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.381, PCGS #9805',
            'notes': 'First year proof Gold Eagles',
            'obverse_description': 'Liberty head design by Augustus Saint-Gaudens, Liberty holding torch and olive branch',
            'reverse_description': 'Family of eagles design by Miley Busiek, male eagle carrying olive branch to nest',
            'distinguishing_features': json.dumps([
                "First year proof Gold Eagle",
                "1/10 ounce .9167 fine gold",
                "W mint mark (West Point)",
                "Mirror finish proof surface"
            ]),
            'identification_keywords': 'american gold eagle age 1987 w proof 5 dollar 1/10 ounce liberty saint-gaudens bullion fine gold',
            'common_names': json.dumps(['Gold Eagle $5 Proof', 'AGE $5 Proof', '1987-W Gold Eagle']),
            'category': 'coin',
            'subcategory': 'proof'
        },
        
        # 1991 - Key date $25 half-ounce
        {
            'coin_id': 'US-AGEF-1991-P',
            'series_id': 'american_gold_eagle_25',
            'country': 'US',
            'denomination': '$25',
            'series_name': 'American Gold Eagle $25',
            'year': 1991,
            'mint': 'P',
            'business_strikes': 24100,
            'proof_strikes': 0,
            'rarity': 'key',
            'composition': json.dumps(eagle_composition),
            'weight_grams': 16.966,
            'diameter_mm': 27.0,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.383, PCGS #9819',
            'notes': 'Key date - lowest mintage Gold Eagle $25',
            'obverse_description': 'Liberty head design by Augustus Saint-Gaudens, Liberty holding torch and olive branch',
            'reverse_description': 'Family of eagles design by Miley Busiek, male eagle carrying olive branch to nest',
            'distinguishing_features': json.dumps([
                "Key date - lowest $25 Eagle mintage",
                "1/2 ounce .9167 fine gold",
                "27.0mm diameter",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american gold eagle age 1991 key date 25 dollar 1/2 ounce liberty saint-gaudens bullion fine gold',
            'common_names': json.dumps(['1991 Gold Eagle $25', 'Key Date Gold Eagle', '1991 AGE $25']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        # 2006 - First year Gold Buffalo  
        {
            'coin_id': 'US-AGBF-2006-P',
            'series_id': 'american_gold_buffalo',
            'country': 'US',
            'denomination': '$50',
            'series_name': 'American Gold Buffalo',
            'year': 2006,
            'mint': 'P',
            'business_strikes': 337012,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(buffalo_composition),
            'weight_grams': 31.108,
            'diameter_mm': 32.7,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.390, PCGS #9990',
            'notes': 'First year Gold Buffalo - first .9999 fine US gold coin',
            'obverse_description': 'Indian head design by James Earle Fraser from Buffalo Nickel, Native American profile',
            'reverse_description': 'American bison design by James Earle Fraser from Buffalo Nickel, standing buffalo',
            'distinguishing_features': json.dumps([
                "First year American Gold Buffalo",
                "First .9999 fine US gold coin",
                "1 ounce .9999 fine gold",
                "Buffalo Nickel designs",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american gold buffalo agb 2006 50 dollar 1 ounce indian bison fraser bullion fine gold',
            'common_names': json.dumps(['Gold Buffalo', 'AGB', '2006 Gold Buffalo', 'Buffalo Gold']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        {
            'coin_id': 'US-AGBF-2006-W',
            'series_id': 'american_gold_buffalo',
            'country': 'US',
            'denomination': '$50',
            'series_name': 'American Gold Buffalo',
            'year': 2006,
            'mint': 'W',
            'business_strikes': 0,
            'proof_strikes': 246267,
            'rarity': 'common',
            'composition': json.dumps(buffalo_composition),
            'weight_grams': 31.108,
            'diameter_mm': 32.7,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.390, PCGS #9991',
            'notes': 'First year Gold Buffalo proof',
            'obverse_description': 'Indian head design by James Earle Fraser from Buffalo Nickel, Native American profile',
            'reverse_description': 'American bison design by James Earle Fraser from Buffalo Nickel, standing buffalo',
            'distinguishing_features': json.dumps([
                "First year Gold Buffalo proof",
                ".9999 fine gold composition",
                "W mint mark (West Point)",
                "Mirror finish proof surface"
            ]),
            'identification_keywords': 'american gold buffalo agb 2006 w proof 50 dollar 1 ounce indian bison fraser bullion fine gold',
            'common_names': json.dumps(['Gold Buffalo Proof', 'AGB Proof', '2006-W Gold Buffalo']),
            'category': 'coin',
            'subcategory': 'proof'
        },
        
        # 2008 - Gold Eagle anniversary sets
        {
            'coin_id': 'US-AGEO-2008-W',
            'series_id': 'american_gold_eagle_50',
            'country': 'US',
            'denomination': '$50',
            'series_name': 'American Gold Eagle $50',
            'year': 2008,
            'mint': 'W',
            'business_strikes': 0,
            'proof_strikes': 30237,
            'rarity': 'semi-key',
            'composition': json.dumps(eagle_composition),
            'weight_grams': 33.931,
            'diameter_mm': 32.7,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.384, PCGS #9856',
            'notes': '20th Anniversary Gold Eagle proof',
            'obverse_description': 'Liberty head design by Augustus Saint-Gaudens, Liberty holding torch and olive branch',
            'reverse_description': 'Family of eagles design by Miley Busiek, male eagle carrying olive branch to nest',
            'distinguishing_features': json.dumps([
                "20th Anniversary special release",
                "Low mintage proof",
                "1 ounce .9167 fine gold",
                "W mint mark (West Point)"
            ]),
            'identification_keywords': 'american gold eagle age 2008 w proof 50 dollar 1 ounce anniversary liberty saint-gaudens bullion fine gold',
            'common_names': json.dumps(['2008-W Gold Eagle', '20th Anniversary Gold Eagle', 'Low Mintage Gold Eagle']),
            'category': 'coin',
            'subcategory': 'proof'
        }
    ]
    
    return coins


def add_gold_eagles_to_database(conn):
    """Add Gold Eagle coins to database."""
    cursor = conn.cursor()
    
    coins = get_gold_eagle_data()
    
    print(f"📊 Adding {len(coins)} American Gold Eagle & Buffalo entries...")
    
    for coin in coins:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO coins (
                    coin_id, series_id, country, denomination, series_name, year, mint,
                    business_strikes, proof_strikes, rarity, composition, weight_grams, diameter_mm,
                    varieties, source_citation, notes, obverse_description, reverse_description,
                    distinguishing_features, identification_keywords, common_names, category, subcategory
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin['coin_id'], coin['series_id'], coin['country'], coin['denomination'],
                coin['series_name'], coin['year'], coin['mint'], coin['business_strikes'],
                coin['proof_strikes'], coin['rarity'], coin['composition'], coin['weight_grams'],
                coin['diameter_mm'], coin['varieties'], coin['source_citation'], coin['notes'],
                coin['obverse_description'], coin['reverse_description'], coin['distinguishing_features'],
                coin['identification_keywords'], coin['common_names'], coin['category'], coin['subcategory']
            ))
            
            print(f"  ✅ Added {coin['coin_id']}")
            
        except Exception as e:
            print(f"  ❌ Failed to add {coin['coin_id']}: {e}")
            raise


def verify_gold_eagles(conn):
    """Verify Gold Eagle entries were added correctly."""
    cursor = conn.cursor()
    
    print("\n📊 Verification Summary:")
    
    # Check total count
    cursor.execute("""
        SELECT COUNT(*) FROM coins 
        WHERE series_name LIKE '%Gold Eagle%' OR series_name LIKE '%Gold Buffalo%'
    """)
    
    total_count = cursor.fetchone()[0]
    print(f"  Total Gold Eagle & Buffalo entries: {total_count}")
    
    # Check by denomination
    cursor.execute("""
        SELECT denomination, COUNT(*) as count
        FROM coins
        WHERE series_name LIKE '%Gold Eagle%' OR series_name LIKE '%Gold Buffalo%'
        GROUP BY denomination
        ORDER BY denomination
    """)
    
    print("  By denomination:")
    for row in cursor.fetchall():
        denomination = row[0]
        count = row[1]
        print(f"    {denomination}: {count}")
    
    # Check by category
    cursor.execute("""
        SELECT subcategory, COUNT(*) as count
        FROM coins
        WHERE series_name LIKE '%Gold Eagle%' OR series_name LIKE '%Gold Buffalo%'
        GROUP BY subcategory
        ORDER BY subcategory
    """)
    
    print("  By subcategory:")
    for row in cursor.fetchall():
        subcategory = row[0] or 'NULL'
        count = row[1]
        print(f"    {subcategory}: {count}")
    
    # Check key dates
    cursor.execute("""
        SELECT coin_id, rarity, business_strikes, proof_strikes
        FROM coins
        WHERE (series_name LIKE '%Gold Eagle%' OR series_name LIKE '%Gold Buffalo%')
        AND rarity IN ('key', 'semi-key')
        ORDER BY year
    """)
    
    print("  Key/Semi-key dates:")
    for row in cursor.fetchall():
        coin_id, rarity, business, proof = row
        strikes = business if business and business > 0 else proof
        print(f"    {coin_id}: {strikes:,} strikes ({rarity})")


def main():
    """Execute American Gold Eagles & Buffalos migration (Issue #52)."""
    print("🚀 Adding American Gold Eagles & Gold Buffalos (1986-2025) - Issue #52")
    print("=" * 70)
    
    # Backup database
    backup_path = backup_database()
    
    try:
        # Connect to database
        conn = sqlite3.connect('database/coins.db')
        
        # Add Gold Eagles & Buffalos
        add_gold_eagles_to_database(conn)
        
        # Commit changes
        conn.commit()
        
        # Verify results
        verify_gold_eagles(conn)
        
        conn.close()
        
        print("\n✨ Gold Eagles & Buffalos Migration Complete!")
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