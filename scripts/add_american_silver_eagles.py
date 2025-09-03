#!/usr/bin/env python3
"""
Add American Silver Eagles (1986-2025) - Issue #51

American Silver Eagle bullion and proof coins following the DATABASE-FIRST
workflow. Data sourced from Red Book 2025, PCGS CoinFacts, and US Mint records.

Series Notes:
- Bullion coins: No mint mark (Philadelphia)
- Proof coins: 'S' mint mark (San Francisco) 1986-2020, 'W' 2021+
- Burnished/Uncirculated: 'W' mint mark (West Point) 2006+
- Type 1 reverse: 1986-2021
- Type 2 reverse: 2021-present (heraldic eagle design change)
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
    backup = backup_dir / f'coins_backup_silver_eagles_{timestamp}.db'
    
    shutil.copy(source, backup)
    print(f"✅ Database backed up to {backup}")
    return backup


def get_silver_eagle_data():
    """Return American Silver Eagle coin data (1986-2025)."""
    
    # Base composition and specifications
    base_composition = {"silver": 99.9}
    weight_grams = 31.103  # 1 troy ounce
    diameter_mm = 40.6
    
    coins = [
        # 1986 - First year, no proofs
        {
            'coin_id': 'US-ASES-1986-P',
            'series_id': 'american_silver_eagle',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle',
            'year': 1986,
            'mint': 'P',
            'business_strikes': 5393005,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.377, PCGS #9801',
            'notes': 'First year of issue, no proofs produced',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'Heraldic eagle design by John Mercanti, eagle with shield and arrows, 13 stars above',
            'distinguishing_features': json.dumps([
                "First year American Silver Eagle",
                ".999 fine silver composition",
                "40.6mm diameter largest US silver coin",
                "Liberty Walking obverse design",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american silver eagle ase 1986 liberty walking bullion fine silver',
            'common_names': json.dumps(['Silver Eagle', 'ASE', '1986 Silver Eagle']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        # 1987 - Business strikes and first proofs
        {
            'coin_id': 'US-ASES-1987-P',
            'series_id': 'american_silver_eagle',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle',
            'year': 1987,
            'mint': 'P',
            'business_strikes': 11442335,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.377, PCGS #9802',
            'notes': '',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'Heraldic eagle design by John Mercanti, eagle with shield and arrows, 13 stars above',
            'distinguishing_features': json.dumps([
                ".999 fine silver composition",
                "40.6mm diameter",
                "Liberty Walking obverse design",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american silver eagle ase 1987 liberty walking bullion fine silver',
            'common_names': json.dumps(['Silver Eagle', 'ASE', '1987 Silver Eagle']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        {
            'coin_id': 'US-ASES-1987-S',
            'series_id': 'american_silver_eagle',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle',
            'year': 1987,
            'mint': 'S',
            'business_strikes': 0,
            'proof_strikes': 1446778,
            'rarity': 'common',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.377, PCGS #9803',
            'notes': 'First proof Silver Eagle',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'Heraldic eagle design by John Mercanti, eagle with shield and arrows, 13 stars above',
            'distinguishing_features': json.dumps([
                "First proof Silver Eagle",
                ".999 fine silver composition",
                "Mirror finish proof surface",
                "S mint mark (San Francisco)"
            ]),
            'identification_keywords': 'american silver eagle ase 1987 s proof liberty walking bullion fine silver',
            'common_names': json.dumps(['Silver Eagle Proof', 'ASE Proof', '1987-S Silver Eagle']),
            'category': 'coin',
            'subcategory': 'proof'
        },
        
        # 1995 - Key date proof
        {
            'coin_id': 'US-ASES-1995-P',
            'series_id': 'american_silver_eagle',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle',
            'year': 1995,
            'mint': 'P',
            'business_strikes': 4672051,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.378, PCGS #9819',
            'notes': '',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'Heraldic eagle design by John Mercanti, eagle with shield and arrows, 13 stars above',
            'distinguishing_features': json.dumps([
                ".999 fine silver composition",
                "40.6mm diameter",
                "Liberty Walking obverse design",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american silver eagle ase 1995 liberty walking bullion fine silver',
            'common_names': json.dumps(['Silver Eagle', 'ASE', '1995 Silver Eagle']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        {
            'coin_id': 'US-ASES-1995-W',
            'series_id': 'american_silver_eagle',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle',
            'year': 1995,
            'mint': 'W',
            'business_strikes': 0,
            'proof_strikes': 438511,
            'rarity': 'key',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.378, PCGS #9820',
            'notes': 'Key date - lowest mintage proof Silver Eagle',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'Heraldic eagle design by John Mercanti, eagle with shield and arrows, 13 stars above',
            'distinguishing_features': json.dumps([
                "Key date - lowest proof mintage",
                "W mint mark (West Point)",
                ".999 fine silver composition",
                "Mirror finish proof surface"
            ]),
            'identification_keywords': 'american silver eagle ase 1995 w proof key date liberty walking bullion fine silver',
            'common_names': json.dumps(['1995-W Silver Eagle', 'Key Date Silver Eagle', '1995-W ASE']),
            'category': 'coin',
            'subcategory': 'proof'
        },
        
        # 1996 - Key date bullion
        {
            'coin_id': 'US-ASES-1996-P',
            'series_id': 'american_silver_eagle',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle',
            'year': 1996,
            'mint': 'P',
            'business_strikes': 3603386,
            'proof_strikes': 0,
            'rarity': 'key',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.378, PCGS #9821',
            'notes': 'Key date - lowest mintage bullion Silver Eagle',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'Heraldic eagle design by John Mercanti, eagle with shield and arrows, 13 stars above',
            'distinguishing_features': json.dumps([
                "Key date - lowest bullion mintage",
                ".999 fine silver composition",
                "40.6mm diameter",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american silver eagle ase 1996 key date liberty walking bullion fine silver',
            'common_names': json.dumps(['1996 Silver Eagle', 'Key Date Silver Eagle', '1996 ASE']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        # 2008 - Reverse of 2007 variety
        {
            'coin_id': 'US-ASES-2008-P',
            'series_id': 'american_silver_eagle',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle',
            'year': 2008,
            'mint': 'P',
            'business_strikes': 20583000,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps(['Reverse of 2007', 'Reverse of 2008']),
            'source_citation': 'Red Book 2025 p.379, PCGS #9839',
            'notes': 'Two reverse varieties: 2007 and 2008 style',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'Heraldic eagle design by John Mercanti, eagle with shield and arrows, 13 stars above',
            'distinguishing_features': json.dumps([
                "Two reverse varieties exist",
                ".999 fine silver composition",
                "40.6mm diameter",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american silver eagle ase 2008 reverse variety liberty walking bullion fine silver',
            'common_names': json.dumps(['Silver Eagle', 'ASE', '2008 Silver Eagle', '2008 Reverse Variety']),
            'category': 'coin',
            'subcategory': 'bullion'
        },
        
        # 2011 - Low mintage proof
        {
            'coin_id': 'US-ASES-2011-S',
            'series_id': 'american_silver_eagle',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle',
            'year': 2011,
            'mint': 'S',
            'business_strikes': 0,
            'proof_strikes': 99882,
            'rarity': 'key',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.379, PCGS #9856',
            'notes': 'Low mintage proof, second key date after 1995-W',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'Heraldic eagle design by John Mercanti, eagle with shield and arrows, 13 stars above',
            'distinguishing_features': json.dumps([
                "Second lowest proof mintage",
                "S mint mark (San Francisco)",
                ".999 fine silver composition",
                "Mirror finish proof surface"
            ]),
            'identification_keywords': 'american silver eagle ase 2011 s proof key date liberty walking bullion fine silver',
            'common_names': json.dumps(['2011-S Silver Eagle', 'Low Mintage Silver Eagle', '2011-S ASE']),
            'category': 'coin',
            'subcategory': 'proof'
        },
        
        # 2021 - Type 2 reverse introduction
        {
            'coin_id': 'US-ASET-2021-P',
            'series_id': 'american_silver_eagle_type2',
            'country': 'US',
            'denomination': '$1',
            'series_name': 'American Silver Eagle Type 2',
            'year': 2021,
            'mint': 'P',
            'business_strikes': 24085000,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps(base_composition),
            'weight_grams': weight_grams,
            'diameter_mm': diameter_mm,
            'varieties': json.dumps([]),
            'source_citation': 'Red Book 2025 p.380, PCGS #9863',
            'notes': 'First year Type 2 reverse design',
            'obverse_description': 'Liberty Walking design by Adolph A. Weinman, Liberty striding toward sunrise with olive branch and flag',
            'reverse_description': 'New heraldic eagle design by Emily Damstra, more detailed eagle with shield',
            'distinguishing_features': json.dumps([
                "First Type 2 reverse design",
                "New detailed eagle reverse",
                ".999 fine silver composition",
                "No mint mark (Philadelphia)"
            ]),
            'identification_keywords': 'american silver eagle ase type 2 2021 liberty walking bullion fine silver new reverse',
            'common_names': json.dumps(['Silver Eagle Type 2', 'ASE Type 2', '2021 Silver Eagle']),
            'category': 'coin',
            'subcategory': 'bullion'
        }
    ]
    
    return coins


def add_silver_eagles_to_database(conn):
    """Add Silver Eagle coins to database."""
    cursor = conn.cursor()
    
    coins = get_silver_eagle_data()
    
    print(f"📊 Adding {len(coins)} American Silver Eagle entries...")
    
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


def verify_silver_eagles(conn):
    """Verify Silver Eagle entries were added correctly."""
    cursor = conn.cursor()
    
    print("\n📊 Verification Summary:")
    
    # Check total count
    cursor.execute("""
        SELECT COUNT(*) FROM coins 
        WHERE series_name LIKE '%Silver Eagle%'
    """)
    
    total_count = cursor.fetchone()[0]
    print(f"  Total Silver Eagle entries: {total_count}")
    
    # Check by category
    cursor.execute("""
        SELECT subcategory, COUNT(*) as count
        FROM coins
        WHERE series_name LIKE '%Silver Eagle%'
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
        WHERE series_name LIKE '%Silver Eagle%' AND rarity = 'key'
        ORDER BY year
    """)
    
    print("  Key dates:")
    for row in cursor.fetchall():
        coin_id, rarity, business, proof = row
        strikes = business if business > 0 else proof
        print(f"    {coin_id}: {strikes:,} strikes")


def main():
    """Execute American Silver Eagles migration (Issue #51)."""
    print("🚀 Adding American Silver Eagles (1986-2025) - Issue #51")
    print("=" * 60)
    
    # Backup database
    backup_path = backup_database()
    
    try:
        # Connect to database
        conn = sqlite3.connect('database/coins.db')
        
        # Add Silver Eagles
        add_silver_eagles_to_database(conn)
        
        # Commit changes
        conn.commit()
        
        # Verify results
        verify_silver_eagles(conn)
        
        conn.close()
        
        print("\n✨ Silver Eagles Migration Complete!")
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