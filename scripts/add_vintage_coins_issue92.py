#!/usr/bin/env python3
"""
Add vintage US type coins and world silver series to the coin taxonomy database.
Issue #92

Adds Vintage US Type Coins:
- US-LGCT: US Large Cent (1793-1857)
- US-DRPT: Draped Bust Cent (1796-1807)
- US-CAPB: Capped Bust Cent (1807-1839)
- US-CLHC: Classic Head Cent (1808-1836)
- US-STHF: Seated Liberty Half Dollar (1839-1891)
- US-STQT: Seated Liberty Quarter (1838-1891)

Adds World Silver Coins:
- SG-SGLN: Singapore Lunar Series (2010+)
- CA-POLR: Canadian Polar Bear 1 oz (2019+)
- DE-GERM: Germania Series 1 oz (2019+)

Adds Bar/Pour Manufacturers:
- CH-PAMP: PAMP Suisse Bars
- CH-VALC: Valcambi Bars
- US-SUNM: Sunshine Mint

Bullion coins get XXXX-X entries for random year purchases.
Vintage US coins get sample year entries (no XXXX pattern - year matters for value).
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import shutil

# Vintage US Type Coins (copper cents - year matters for value, no XXXX pattern)
VINTAGE_US_COINS = [
    {
        "country": "US",
        "code": "LGCT",
        "name": "US Large Cent",
        "denomination": "Cents",
        "start_year": 1793,
        "end_year": 1857,
        "weight_grams": 10.89,  # Varied over time: 13.48g early, 10.89g later
        "diameter_mm": 29.0,
        "edge": "Plain",
        "composition": {"copper": 100},
        "designer": "Various (Scot, Reich, Gobrecht)",
        "mint_mark": "P",
        "obverse": "Liberty head design (various types: Flowing Hair, Liberty Cap, Draped Bust, Classic Head, Coronet)",
        "reverse": "Wreath design surrounding 'ONE CENT', 'UNITED STATES OF AMERICA'",
        "aliases": ["Large Penny", "Copper Cent", "Big Cent"],
        "notes": "US copper cent minted 1793-1857. Multiple design types. Replaced by Flying Eagle Cent.",
        "sample_year": 1820,
    },
    {
        "country": "US",
        "code": "DRPT",
        "name": "Draped Bust Cent",
        "denomination": "Cents",
        "start_year": 1796,
        "end_year": 1807,
        "weight_grams": 10.89,
        "diameter_mm": 29.0,
        "edge": "Plain",
        "composition": {"copper": 100},
        "designer": "Robert Scot",
        "mint_mark": "P",
        "obverse": "Liberty facing right with draped bust, hair tied with ribbon, 'LIBERTY' above, date below",
        "reverse": "Wreath encircling 'ONE CENT', 'UNITED STATES OF AMERICA' around",
        "aliases": ["Draped Bust", "DB Cent"],
        "notes": "Classic early American cent design. Large cents only (no small cents in this era).",
        "sample_year": 1800,
    },
    {
        "country": "US",
        "code": "CAPB",
        "name": "Capped Bust Cent",
        "denomination": "Cents",
        "start_year": 1807,
        "end_year": 1814,
        "weight_grams": 10.89,
        "diameter_mm": 29.0,
        "edge": "Plain",
        "composition": {"copper": 100},
        "designer": "John Reich",
        "mint_mark": "P",
        "obverse": "Liberty facing left wearing cap, 'LIBERTY' on headband, stars around, date below",
        "reverse": "Wreath encircling 'ONE CENT', 'UNITED STATES OF AMERICA' around",
        "aliases": ["Capped Bust", "Classic Head Large Cent"],
        "notes": "Short-lived design by John Reich. Minting paused 1815-1816 due to copper shortage.",
        "sample_year": 1810,
    },
    {
        "country": "US",
        "code": "CLHC",
        "name": "Classic Head Cent",
        "denomination": "Cents",
        "start_year": 1808,
        "end_year": 1836,
        "weight_grams": 10.89,
        "diameter_mm": 29.0,
        "edge": "Plain",
        "composition": {"copper": 100},
        "designer": "John Reich",
        "mint_mark": "P",
        "obverse": "Liberty head with coronet inscribed 'LIBERTY', stars around, date below",
        "reverse": "Wreath encircling 'ONE CENT', 'UNITED STATES OF AMERICA' around",
        "aliases": ["Classic Head", "Coronet Head Cent", "Matron Head"],
        "notes": "Also known as Coronet or Matron Head. Large cent design 1816-1839.",
        "sample_year": 1825,
    },
    {
        "country": "US",
        "code": "STHF",
        "name": "Seated Liberty Half Dollar",
        "denomination": "Half Dollars",
        "start_year": 1839,
        "end_year": 1891,
        "weight_grams": 12.44,
        "diameter_mm": 30.6,
        "edge": "Reeded",
        "composition": {"silver": 90, "copper": 10},
        "designer": "Christian Gobrecht",
        "mint_mark": "P",
        "obverse": "Liberty seated on rock, holding shield with 'LIBERTY' and pole with liberty cap, 13 stars around, date below",
        "reverse": "Eagle with shield on breast, 'UNITED STATES OF AMERICA', 'HALF DOL.' below",
        "aliases": ["Seated Half", "Liberty Seated Half", "Seated Liberty 50c"],
        "notes": "Multiple varieties: No Motto (1839-1866), With Motto (1866-1891). Branch mints: O, S, CC.",
        "sample_year": 1855,
    },
    {
        "country": "US",
        "code": "STQT",
        "name": "Seated Liberty Quarter",
        "denomination": "Quarters",
        "start_year": 1838,
        "end_year": 1891,
        "weight_grams": 6.22,
        "diameter_mm": 24.3,
        "edge": "Reeded",
        "composition": {"silver": 90, "copper": 10},
        "designer": "Christian Gobrecht",
        "mint_mark": "P",
        "obverse": "Liberty seated on rock, holding shield with 'LIBERTY' and pole with liberty cap, 13 stars around, date below",
        "reverse": "Eagle with shield on breast, 'UNITED STATES OF AMERICA', 'QUAR. DOL.' below",
        "aliases": ["Seated Quarter", "Liberty Seated Quarter", "Seated Liberty 25c"],
        "notes": "Multiple varieties: No Motto (1838-1866), With Motto (1866-1891). Branch mints: O, S, CC.",
        "sample_year": 1855,
    },
]

# World Silver Bullion (XXXX pattern for random year)
WORLD_SILVER_SERIES = [
    {
        "country": "SG",
        "code": "SGLN",
        "name": "Singapore Lunar Series 1 oz",
        "denomination": "Two Dollars",
        "start_year": 2010,
        "end_year": None,
        "weight_oz": 1.0,
        "weight_grams": 31.1035,
        "diameter_mm": 40.0,
        "edge": "Reeded",
        "composition": {"silver": 99.9},
        "designer": "Singapore Mint",
        "mint_mark": "X",
        "obverse": "Singapore national crest, 'SINGAPORE', denomination, date",
        "reverse": "Chinese Zodiac animal design (changes annually), '1 oz 999 FINE SILVER'",
        "aliases": ["Singapore Lunar", "Singapore Zodiac", "SG Lunar"],
        "notes": "Annual Chinese Zodiac series. Minted by Singapore Mint. Limited mintages.",
    },
    {
        "country": "CA",
        "code": "POLR",
        "name": "Canadian Polar Bear 1 oz",
        "denomination": "Five Dollars",
        "start_year": 2019,
        "end_year": None,
        "weight_oz": 1.0,
        "weight_grams": 31.1035,
        "diameter_mm": 38.0,
        "edge": "Reeded",
        "composition": {"silver": 99.99},
        "designer": "Royal Canadian Mint",
        "mint_mark": "X",
        "obverse": "King Charles III effigy (2024+) or Queen Elizabeth II, 'CANADA', '5 DOLLARS', date",
        "reverse": "Polar bear design, '1 OZ FINE SILVER 9999 ARGENT PUR'",
        "aliases": ["Polar Bear", "Canadian Polar Bear", "RCM Polar Bear"],
        "notes": "Royal Canadian Mint bullion series. Design may vary by year.",
    },
    {
        "country": "DE",
        "code": "GERM",
        "name": "Germania 1 oz",
        "denomination": "Five Mark",
        "start_year": 2019,
        "end_year": None,
        "weight_oz": 1.0,
        "weight_grams": 31.1035,
        "diameter_mm": 40.0,
        "edge": "Reeded",
        "composition": {"silver": 99.9},
        "designer": "Germania Mint",
        "mint_mark": "X",
        "obverse": "Germania personification (female warrior with shield), denomination, date",
        "reverse": "Double-headed eagle design, '1 OZ', '.999 FINE SILVER'",
        "aliases": ["Germania", "Germania Mint", "German Silver"],
        "notes": "Private mint series featuring Germanic mythology. Popular collectible bullion.",
    },
]

# Bar/Pour Manufacturers (XXXX pattern)
BAR_SERIES = [
    {
        "country": "CH",
        "code": "PAMP",
        "name": "PAMP Suisse Silver Bar",
        "denomination": "No Face Value",
        "start_year": 1977,
        "end_year": None,
        "weight_oz": 1.0,
        "weight_grams": 31.1035,
        "diameter_mm": None,
        "edge": "Plain",
        "composition": {"silver": 99.9},
        "designer": "PAMP Suisse",
        "mint_mark": "X",
        "obverse": "PAMP logo, Lady Fortuna design, serial number, weight, '.999 FINE SILVER'",
        "reverse": "Assay certificate information or blank",
        "aliases": ["PAMP", "PAMP Bar", "Fortuna Bar", "Lady Fortuna"],
        "notes": "Swiss refiner. Lady Fortuna design iconic. Available in 1oz, 5oz, 10oz, 100oz, 1kg.",
    },
    {
        "country": "CH",
        "code": "VALC",
        "name": "Valcambi Silver Bar",
        "denomination": "No Face Value",
        "start_year": 1961,
        "end_year": None,
        "weight_oz": 1.0,
        "weight_grams": 31.1035,
        "diameter_mm": None,
        "edge": "Plain",
        "composition": {"silver": 99.9},
        "designer": "Valcambi Suisse",
        "mint_mark": "X",
        "obverse": "Valcambi logo, serial number, weight, '.999 FINE SILVER'",
        "reverse": "Blank or Valcambi hallmark",
        "aliases": ["Valcambi", "Valcambi Suisse", "Valcambi Bar"],
        "notes": "Swiss refiner owned by Rajesh Exports. CombiBar breakable bars popular.",
    },
    {
        "country": "US",
        "code": "SUNM",
        "name": "Sunshine Mint Silver",
        "denomination": "No Face Value",
        "start_year": 1983,
        "end_year": None,
        "weight_oz": 1.0,
        "weight_grams": 31.1035,
        "diameter_mm": 39.0,  # For rounds
        "edge": "Reeded",
        "composition": {"silver": 99.9},
        "designer": "Sunshine Minting Inc.",
        "mint_mark": "X",
        "obverse": "Sunshine Mint logo (sun rays), 'SUNSHINE MINTING', weight, '.999 FINE SILVER'",
        "reverse": "Eagle design or blank (bars)",
        "aliases": ["Sunshine", "Sunshine Mint", "SMI Silver"],
        "notes": "Idaho-based mint. Known for security MintMark SI feature. Rounds and bars.",
    },
]


def backup_database(db_path):
    """Create timestamped backup of database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = db_path.parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / f"coins_backup_{timestamp}.db"
    shutil.copy(db_path, backup_path)
    print(f"Database backed up to: {backup_path}")
    return backup_path


def add_vintage_us_coins(conn):
    """Add vintage US coin series (no XXXX pattern - year matters)"""
    cursor = conn.cursor()
    added = 0

    for series in VINTAGE_US_COINS:
        country = series["country"]
        code = series["code"]
        name = series["name"]
        full_code = f"{country}-{code}"
        print(f"Adding {name} ({full_code})...")

        # Add to series_registry
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'coin', ?)
        """, (
            f"{name}__{series['denomination'].replace(' ', '_')}",
            name,
            code,
            country,
            series["denomination"],
            series["start_year"],
            series["end_year"],
            f"{list(series['composition'].keys())[0].title()} coin, {series['weight_grams']}g",
            name,
            json.dumps(series.get("aliases", [])),
        ))

        # Add sample year coin entry (vintage coins - year matters!)
        sample_year = series.get("sample_year", series["start_year"])
        mint_mark = series.get("mint_mark", "P")
        coin_id = f"{country}-{code}-{sample_year}-{mint_mark}"

        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, notes, rarity,
                source_citation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', ?)
        """, (
            coin_id,
            str(sample_year),
            mint_mark,
            series["denomination"],
            name,
            json.dumps(series["composition"]),
            series["weight_grams"],
            series.get("diameter_mm"),
            series.get("edge", "Plain"),
            series["designer"],
            series["obverse"],
            series["reverse"],
            series.get("notes", ""),
            f"Issue #92 - Vintage US Type Coins",
        ))

        added += 1
        print(f"  Added series_registry entry and sample coin {coin_id}")

    conn.commit()
    return added


def add_world_silver(conn):
    """Add world silver bullion series (XXXX pattern for random year)"""
    cursor = conn.cursor()
    added = 0

    for series in WORLD_SILVER_SERIES:
        country = series["country"]
        code = series["code"]
        name = series["name"]
        full_code = f"{country}-{code}"
        print(f"Adding {name} ({full_code})...")

        # Add to series_registry
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'coin', ?)
        """, (
            f"{name}__{series['denomination'].replace(' ', '_')}",
            name,
            code,
            country,
            series["denomination"],
            series["start_year"],
            series["end_year"],
            f"Bullion, {series['weight_oz']} oz {list(series['composition'].keys())[0]}",
            name,
            json.dumps(series.get("aliases", [])),
        ))

        # Add XXXX-X entry for random year bullion
        mint_mark = series.get("mint_mark", "X")
        xxxx_coin_id = f"{country}-{code}-XXXX-{mint_mark}"

        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, notes, rarity,
                source_citation
            ) VALUES (?, 'XXXX', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', ?)
        """, (
            xxxx_coin_id,
            mint_mark,
            series["denomination"],
            name,
            json.dumps(series["composition"]),
            series["weight_grams"],
            series.get("diameter_mm"),
            series.get("edge", "Reeded"),
            series["designer"],
            series["obverse"],
            series["reverse"],
            f"Random year bullion - valued by metal content. {series.get('notes', '')}".strip(),
            f"Issue #92 - World Silver",
        ))

        added += 1
        print(f"  Added series_registry entry and bullion entry {xxxx_coin_id}")

    conn.commit()
    return added


def add_bar_series(conn):
    """Add bar/pour manufacturer series (XXXX pattern)"""
    cursor = conn.cursor()
    added = 0

    for series in BAR_SERIES:
        country = series["country"]
        code = series["code"]
        name = series["name"]
        full_code = f"{country}-{code}"
        print(f"Adding {name} ({full_code})...")

        # Add to series_registry
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'coin', ?)
        """, (
            f"{name}__{series['denomination'].replace(' ', '_')}",
            name,
            code,
            country,
            series["denomination"],
            series["start_year"],
            series["end_year"],
            f"Bar/Pour, {series['weight_oz']} oz {list(series['composition'].keys())[0]}",
            name,
            json.dumps(series.get("aliases", [])),
        ))

        # Add XXXX-X entry for random bullion
        mint_mark = series.get("mint_mark", "X")
        xxxx_coin_id = f"{country}-{code}-XXXX-{mint_mark}"

        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, notes, rarity,
                source_citation
            ) VALUES (?, 'XXXX', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', ?)
        """, (
            xxxx_coin_id,
            mint_mark,
            series["denomination"],
            name,
            json.dumps(series["composition"]),
            series["weight_grams"],
            series.get("diameter_mm"),
            series.get("edge", "Plain"),
            series["designer"],
            series["obverse"],
            series["reverse"],
            f"Random year bullion - valued by metal content. {series.get('notes', '')}".strip(),
            f"Issue #92 - Bar/Pour Manufacturers",
        ))

        added += 1
        print(f"  Added series_registry entry and bar entry {xxxx_coin_id}")

    conn.commit()
    return added


def verify_additions(conn):
    """Verify all series were added correctly"""
    cursor = conn.cursor()

    # Expected codes
    expected_codes = ['LGCT', 'DRPT', 'CAPB', 'CLHC', 'STHF', 'STQT',  # US vintage
                      'SGLN', 'POLR', 'GERM',  # World silver
                      'PAMP', 'VALC', 'SUNM']  # Bars

    # Count new series
    placeholders = ','.join(['?' for _ in expected_codes])
    cursor.execute(f"""
        SELECT COUNT(*) FROM series_registry
        WHERE series_abbreviation IN ({placeholders})
    """, expected_codes)
    registry_count = cursor.fetchone()[0]

    # Count new coins
    cursor.execute(f"""
        SELECT COUNT(*) FROM coins
        WHERE coin_id LIKE '%-LGCT-%' OR coin_id LIKE '%-DRPT-%' OR coin_id LIKE '%-CAPB-%'
           OR coin_id LIKE '%-CLHC-%' OR coin_id LIKE '%-STHF-%' OR coin_id LIKE '%-STQT-%'
           OR coin_id LIKE '%-SGLN-%' OR coin_id LIKE '%-POLR-%' OR coin_id LIKE '%-GERM-%'
           OR coin_id LIKE '%-PAMP-%' OR coin_id LIKE '%-VALC-%' OR coin_id LIKE '%-SUNM-%'
    """)
    coin_count = cursor.fetchone()[0]

    print(f"\nVerification:")
    print(f"  Series registry entries: {registry_count} (expected: 12)")
    print(f"  Coin entries: {coin_count} (expected: 12)")

    # Show country breakdown
    cursor.execute(f"""
        SELECT DISTINCT country_code FROM series_registry
        WHERE series_abbreviation IN ({placeholders})
        ORDER BY country_code
    """, expected_codes)
    countries = [row[0] for row in cursor.fetchall()]
    print(f"  Countries: {', '.join(countries)}")

    return registry_count == 12 and coin_count == 12


def main():
    db_path = Path(__file__).parent.parent / "database" / "coins.db"

    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return 1

    # Backup database first
    backup_path = backup_database(db_path)

    conn = sqlite3.connect(db_path)
    try:
        print("\n=== Adding Vintage US Type Coins ===")
        vintage_count = add_vintage_us_coins(conn)

        print("\n=== Adding World Silver Coins ===")
        world_silver_count = add_world_silver(conn)

        print("\n=== Adding Bar/Pour Manufacturers ===")
        bar_count = add_bar_series(conn)

        print(f"\n{'='*50}")
        print(f"Added {vintage_count} vintage US type coin series")
        print(f"Added {world_silver_count} world silver coin series")
        print(f"Added {bar_count} bar/pour manufacturer series")
        print(f"Total: {vintage_count + world_silver_count + bar_count} series")

        if not verify_additions(conn):
            print("\nWarning: Verification counts don't match expected values")
            print(f"Backup available at: {backup_path}")

        print("\n=== Next Steps ===")
        print("1. Run: uv run python scripts/export_from_database.py")
        print("2. Run: uv run python scripts/validate_taxonomy.py")
        print("3. Commit changes with: git add . && git commit")

    except Exception as e:
        print(f"\nError: {e}")
        print(f"Restore from backup: {backup_path}")
        raise
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    exit(main())
