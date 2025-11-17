#!/usr/bin/env python3
"""
Add Mexican Libertad Bullion (Gold & Silver) - Issue #66

Mexican Libertad bullion coins following the established American Eagle pattern.
Data sourced from validated libertad-research1.md with cross-references.

Gold Libertads (5 sizes):
- 1/20 oz, 1/10 oz, 1/4 oz, 1/2 oz, 1 oz
- Fineness: .900 (1981-1990), .999 (1991+)
- Design: Old angel (1981-1999), New angel (2000+)

Silver Libertads (8 sizes):
- 1/20 oz, 1/10 oz, 1/4 oz, 1/2 oz, 1 oz, 2 oz, 5 oz, 1 kg
- Fineness: .999 (all years)
- Design: Old angel (1982-1995), New angel (1996+)

Series Notes:
- All minted at Mexico City (MO mint mark)
- Multiple variants: BU, Proof, Reverse Proof, Antiqued (silver only)
- No face value (bullion valued by metal content)
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
    backup = backup_dir / f'coins_backup_libertads_{timestamp}.db'

    shutil.copy(source, backup)
    print(f"✅ Database backed up to {backup}")
    return backup


def get_gold_libertad_1oz_data():
    """Return Mexican Gold Libertad 1 oz coin data."""
    # Composition changes based on year
    composition_900 = {"gold": 90.0, "copper": 10.0}  # 1981-1990
    composition_999 = {"gold": 99.9}  # 1991+

    # Mintage data from libertad-research1.md (canonical source)
    bu_mintages = {
        1981: 596000, 1991: 109193, 1992: 46281, 1993: 73881, 1994: 1000,
        2000: 2370, 2002: 15000, 2003: 500, 2004: 3000, 2005: 3000,
        2006: 4000, 2007: 2500, 2008: 800, 2009: 6200, 2010: 4000,
        2011: 3000, 2012: 3000, 2013: 2350, 2014: 4050, 2015: 4800,
        2016: 4100, 2017: 900, 2018: 2050, 2019: 2000, 2020: 1100,
        2021: 1050, 2022: 1900
    }

    proof_mintages = {
        1989: 704, 2004: 1800, 2005: 570, 2006: 520, 2007: 500, 2008: 500,
        2009: 600, 2010: 600, 2011: 1100, 2013: 400, 2014: 250, 2015: 500,
        2016: 2100, 2017: 600, 2018: 1000, 2019: 750, 2020: 250, 2021: 500,
        2022: 1300
    }

    rp_mintages = {
        2018: 1000, 2019: 500, 2020: 250, 2021: 500, 2022: 500
    }

    coins = []

    # BU strikes
    for year, mintage in bu_mintages.items():
        composition = composition_900 if year <= 1990 else composition_999
        fineness = ".900" if year <= 1990 else ".999"
        angel_type = "old angel (front-facing)" if year <= 1999 else "new angel (3/4 profile)"
        obverse = "Simple coat of arms" if year <= 1999 else "Current coat of arms with 10 historical versions"

        coins.append({
            'coin_id': f'MX-MLGO-{year}-MO',
            'year': str(year),
            'mint': 'MO',
            'denomination': 'No Face Value',
            'series': 'Mexican Libertad Gold 1 oz',
            'variety': None,
            'composition': json.dumps(composition),
            'weight_grams': 31.1,
            'diameter_mm': 34.5,
            'edge': 'Reeded',
            'designer': 'Based on 1921 Centenario design',
            'obverse_description': f'{obverse}',
            'reverse_description': f'Winged Victoria (Angel of Independence) with volcanoes Popocatépetl and Iztaccihuatl ({angel_type})',
            'business_strikes': mintage,
            'proof_strikes': 0,
            'total_mintage': mintage,
            'notes': f'{fineness} fine gold, {angel_type}',
            'rarity': 'key' if mintage <= 1000 else 'common',
            'source_citation': 'Libertad Research (libertad-research1.md), Banco de México'
        })

    # Proof strikes
    for year, mintage in proof_mintages.items():
        composition = composition_900 if year <= 1990 else composition_999
        fineness = ".900" if year <= 1990 else ".999"
        angel_type = "old angel (front-facing)" if year <= 1999 else "new angel (3/4 profile)"
        obverse = "Simple coat of arms" if year <= 1999 else "Current coat of arms with 10 historical versions"

        coins.append({
            'coin_id': f'MX-MLGO-{year}-MO-P',
            'year': str(year),
            'mint': 'MO',
            'denomination': 'No Face Value',
            'series': 'Mexican Libertad Gold 1 oz',
            'variety': 'Proof',
            'composition': json.dumps(composition),
            'weight_grams': 31.1,
            'diameter_mm': 34.5,
            'edge': 'Reeded',
            'designer': 'Based on 1921 Centenario design',
            'obverse_description': f'{obverse}',
            'reverse_description': f'Winged Victoria with frosted finish on polished background ({angel_type})',
            'business_strikes': 0,
            'proof_strikes': mintage,
            'total_mintage': mintage,
            'notes': f'Proof finish - {fineness} fine gold, {angel_type}',
            'rarity': 'common',
            'source_citation': 'Libertad Research (libertad-research1.md), Banco de México'
        })

    # Reverse Proof strikes
    for year, mintage in rp_mintages.items():
        coins.append({
            'coin_id': f'MX-MLGO-{year}-MO-RP',
            'year': str(year),
            'mint': 'MO',
            'denomination': 'No Face Value',
            'series': 'Mexican Libertad Gold 1 oz',
            'variety': 'Reverse Proof',
            'composition': json.dumps(composition_999),
            'weight_grams': 31.1,
            'diameter_mm': 34.5,
            'edge': 'Reeded',
            'designer': 'Based on 1921 Centenario design',
            'obverse_description': 'Current coat of arms with 10 historical versions',
            'reverse_description': 'Winged Victoria with polished finish on frosted background (new angel)',
            'business_strikes': 0,
            'proof_strikes': mintage,
            'total_mintage': mintage,
            'notes': 'Reverse Proof finish - .999 fine gold, new angel',
            'rarity': 'common',
            'source_citation': 'Libertad Research (libertad-research1.md), Banco de México'
        })

    return coins


def get_silver_libertad_1oz_data():
    """Return Mexican Silver Libertad 1 oz coin data (1982-2022)."""
    composition = {"silver": 99.9}

    # Mintage data from libertad-research1.md (canonical source)
    bu_mintages = {
        1982: 1050000, 1983: 1002200, 1984: 1015500, 1985: 2017000, 1986: 1699426,
        1987: 500000, 1988: 1000000, 1989: 1396500, 1990: 1200000, 1991: 1650518,
        1992: 2458000, 1993: 1000000, 1994: 400000, 1995: 500000, 1996: 300000,
        1997: 100000, 1998: 67000, 1999: 95000, 2000: 455000, 2001: 385000,
        2002: 955000, 2003: 200000, 2004: 550000, 2005: 600000, 2006: 300000,
        2007: 200000, 2008: 950000, 2009: 1650000, 2010: 1000000, 2011: 1200000,
        2012: 746400, 2013: 774100, 2014: 429200, 2015: 901500, 2016: 1437500,
        2017: 636000, 2018: 300000, 2019: 402000, 2020: 300000, 2021: 450000,
        2022: 350000
    }

    proof_mintages = {
        2016: 13250, 2019: 5500, 2020: 5850, 2021: 3450, 2022: 3400
    }

    rp_mintages = {
        2015: 1500, 2016: 1500, 2019: 1000, 2020: 1000, 2021: 1000, 2022: 1000
    }

    antique_mintages = {
        2018: 40000, 2019: 1000
    }

    coins = []

    # BU strikes
    for year, mintage in bu_mintages.items():
        angel_type = "old angel (front-facing)" if year <= 1995 else "new angel (3/4 profile)"
        obverse = "Simple coat of arms" if year <= 1995 else "Current coat of arms with 10 historical versions"
        size_note = "Smaller diameter, greater thickness" if year <= 1995 else "Current size specifications"

        coins.append({
            'coin_id': f'MX-MLSO-{year}-MO',
            'year': str(year),
            'mint': 'MO',
            'denomination': 'No Face Value',
            'series': 'Mexican Libertad Silver 1 oz',
            'variety': None,
            'composition': json.dumps(composition),
            'weight_grams': 31.103,
            'diameter_mm': 40.0,
            'edge': 'Reeded',
            'designer': 'Based on 1921 Centenario design',
            'obverse_description': f'{obverse}',
            'reverse_description': f'Winged Victoria (Angel of Independence) with volcanoes ({angel_type})',
            'business_strikes': mintage,
            'proof_strikes': 0,
            'total_mintage': mintage,
            'notes': f'.999 fine silver, {angel_type}, {size_note}',
            'rarity': 'common',
            'source_citation': 'Libertad Research (libertad-research1.md), Banco de México'
        })

    # Proof strikes
    for year, mintage in proof_mintages.items():
        coins.append({
            'coin_id': f'MX-MLSO-{year}-MO-P',
            'year': str(year),
            'mint': 'MO',
            'denomination': 'No Face Value',
            'series': 'Mexican Libertad Silver 1 oz',
            'variety': 'Proof',
            'composition': json.dumps(composition),
            'weight_grams': 31.103,
            'diameter_mm': 40.0,
            'edge': 'Reeded',
            'designer': 'Based on 1921 Centenario design',
            'obverse_description': 'Current coat of arms with 10 historical versions',
            'reverse_description': 'Winged Victoria with frosted finish on polished background',
            'business_strikes': 0,
            'proof_strikes': mintage,
            'total_mintage': mintage,
            'notes': 'Proof finish - .999 fine silver, new angel',
            'rarity': 'common',
            'source_citation': 'Libertad Research (libertad-research1.md), Banco de México'
        })

    # Reverse Proof strikes
    for year, mintage in rp_mintages.items():
        coins.append({
            'coin_id': f'MX-MLSO-{year}-MO-RP',
            'year': str(year),
            'mint': 'MO',
            'denomination': 'No Face Value',
            'series': 'Mexican Libertad Silver 1 oz',
            'variety': 'Reverse Proof',
            'composition': json.dumps(composition),
            'weight_grams': 31.103,
            'diameter_mm': 40.0,
            'edge': 'Reeded',
            'designer': 'Based on 1921 Centenario design',
            'obverse_description': 'Current coat of arms with 10 historical versions',
            'reverse_description': 'Winged Victoria with polished finish on frosted background',
            'business_strikes': 0,
            'proof_strikes': mintage,
            'total_mintage': mintage,
            'notes': 'Reverse Proof finish - .999 fine silver',
            'rarity': 'common',
            'source_citation': 'Libertad Research (libertad-research1.md), Banco de México'
        })

    # Antiqued finish strikes
    for year, mintage in antique_mintages.items():
        coins.append({
            'coin_id': f'MX-MLSO-{year}-MO-AF',
            'year': str(year),
            'mint': 'MO',
            'denomination': 'No Face Value',
            'series': 'Mexican Libertad Silver 1 oz',
            'variety': 'Antiqued Finish',
            'composition': json.dumps(composition),
            'weight_grams': 31.103,
            'diameter_mm': 40.0,
            'edge': 'Reeded',
            'designer': 'Based on 1921 Centenario design',
            'obverse_description': 'Current coat of arms with 10 historical versions',
            'reverse_description': 'Winged Victoria with antiqued finish',
            'business_strikes': mintage,
            'proof_strikes': 0,
            'total_mintage': mintage,
            'notes': 'Antiqued finish - .999 fine silver, limited release',
            'rarity': 'common',
            'source_citation': 'Libertad Research (libertad-research1.md), Banco de México'
        })

    return coins


def add_libertads_to_database(conn):
    """Add Libertad coins to database."""
    cursor = conn.cursor()

    # Collect all coin data
    all_coins = []
    all_coins.extend(get_gold_libertad_1oz_data())
    all_coins.extend(get_silver_libertad_1oz_data())

    print(f"📊 Adding {len(all_coins)} Mexican Libertad entries...")
    print(f"  Gold 1 oz entries: {len(get_gold_libertad_1oz_data())}")
    print(f"  Silver 1 oz entries: {len(get_silver_libertad_1oz_data())}")

    for coin in all_coins:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO coins (
                    coin_id, year, mint, denomination, series, variety,
                    composition, weight_grams, diameter_mm, edge, designer,
                    obverse_description, reverse_description,
                    business_strikes, proof_strikes, total_mintage,
                    notes, rarity, source_citation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin['coin_id'], coin['year'], coin['mint'], coin['denomination'],
                coin['series'], coin['variety'], coin['composition'], coin['weight_grams'],
                coin['diameter_mm'], coin['edge'], coin['designer'],
                coin['obverse_description'], coin['reverse_description'],
                coin['business_strikes'], coin['proof_strikes'], coin['total_mintage'],
                coin['notes'], coin['rarity'], coin['source_citation']
            ))

            print(f"  ✅ Added {coin['coin_id']}")

        except Exception as e:
            print(f"  ❌ Failed to add {coin['coin_id']}: {e}")
            raise


def verify_libertads(conn):
    """Verify Libertad entries were added correctly."""
    cursor = conn.cursor()

    print("\n📊 Verification Summary:")

    # Check total count
    cursor.execute("""
        SELECT COUNT(*) FROM coins
        WHERE series LIKE '%Libertad%'
    """)

    total_count = cursor.fetchone()[0]
    print(f"  Total Libertad entries: {total_count}")

    # Check by metal
    cursor.execute("""
        SELECT
            CASE
                WHEN series LIKE '%Gold%' THEN 'Gold'
                WHEN series LIKE '%Silver%' THEN 'Silver'
                ELSE 'Other'
            END as metal,
            COUNT(*) as count
        FROM coins
        WHERE series LIKE '%Libertad%'
        GROUP BY metal
        ORDER BY metal
    """)

    print("  By metal:")
    for row in cursor.fetchall():
        metal, count = row
        print(f"    {metal}: {count}")

    # Check by variety
    cursor.execute("""
        SELECT variety, COUNT(*) as count
        FROM coins
        WHERE series LIKE '%Libertad%'
        GROUP BY variety
        ORDER BY variety
    """)

    print("  By variety:")
    for row in cursor.fetchall():
        variety = row[0] or 'BU/Standard'
        count = row[1]
        print(f"    {variety}: {count}")

    # Check year range
    cursor.execute("""
        SELECT MIN(year), MAX(year)
        FROM coins
        WHERE series LIKE '%Libertad%'
    """)

    min_year, max_year = cursor.fetchone()
    print(f"  Year range: {min_year}-{max_year}")

    # Check key dates (low mintage)
    cursor.execute("""
        SELECT coin_id, rarity, business_strikes, proof_strikes
        FROM coins
        WHERE series LIKE '%Libertad%'
        AND rarity = 'key'
        ORDER BY year
    """)

    key_dates = cursor.fetchall()
    if key_dates:
        print("  Key dates:")
        for row in key_dates:
            coin_id, rarity, business, proof = row
            strikes = business if business and business > 0 else proof
            print(f"    {coin_id}: {strikes:,} strikes ({rarity})")


def main():
    """Execute Mexican Libertad migration (Issue #66)."""
    print("🚀 Adding Mexican Libertad Bullion (Gold & Silver) - Issue #66")
    print("=" * 70)

    # Backup database
    backup_path = backup_database()

    try:
        # Connect to database
        conn = sqlite3.connect('database/coins.db')

        # Add Libertads
        add_libertads_to_database(conn)

        # Commit changes
        conn.commit()

        # Verify results
        verify_libertads(conn)

        conn.close()

        print("\n✨ Mexican Libertad Migration Complete!")
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
