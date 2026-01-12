#!/usr/bin/env python3
"""
Add world bullion and vintage bar categories to the coin taxonomy database.
Issue #90

Adds World Silver Coins:
- AU-ROOS: Australian Kangaroo Silver 1 oz (Perth Mint)
- AU-LUNR: Perth Lunar Series 1 oz
- AU-AEMU: Australian Emu 1 oz
- AU-KOAL: Australian Koala 1 oz
- GB-QBST: Queen's Beasts 2 oz (Royal Mint)
- AM-NOAH: Noah's Ark 1 oz (Armenian)
- KR-CHWO: Chiwoo Cheonwang 1 oz (KOMSCO)

Adds Vintage Bars/Pours:
- US-ENGP: Engelhard Prospector 1 oz rounds
- US-ENG5: Engelhard Bar 5 oz
- US-EN10: Engelhard Bar 10 oz
- US-E100: Engelhard Bar 100 oz
- US-JMTB: Johnson Matthey Bar (various weights)
- US-SCOT: Scottsdale Mint (stackers, poured)

Adds World Gold Catch-all:
- XX-WGLD: World Gold Sovereigns (catch-all for foreign gold)

Each includes a XXXX-X entry for random year bullion purchases.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import shutil

# World Silver Coins
WORLD_SILVER_SERIES = [
    {
        "country": "AU",
        "code": "ROOS",
        "name": "Australian Kangaroo Silver 1 oz",
        "denomination": "One Dollar",
        "start_year": 2016,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"silver": 99.99},
        "weight_grams": 31.1035,
        "diameter_mm": 40.6,
        "edge": "Reeded",
        "designer": "Perth Mint",
        "mint_mark": "P",
        "obverse": "King Charles III effigy (2024+) or Queen Elizabeth II, 'AUSTRALIA', '1 DOLLAR', date",
        "reverse": "Kangaroo design (changes annually), '1oz 9999 SILVER'",
        "aliases": ["Silver Kangaroo", "Australian Silver Kangaroo", "Roo"],
        "notes": "Perth Mint bullion coin. Design changes annually.",
    },
    {
        "country": "AU",
        "code": "LUNR",
        "name": "Perth Lunar Series",
        "denomination": "One Dollar",
        "start_year": 1999,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"silver": 99.99},
        "weight_grams": 31.1035,
        "diameter_mm": 40.6,
        "edge": "Reeded",
        "designer": "Perth Mint",
        "mint_mark": "P",
        "obverse": "Monarch effigy, 'AUSTRALIA', '1 DOLLAR', date",
        "reverse": "Chinese Zodiac animal (Dragon, Tiger, Rabbit, etc.), '1oz 9999 SILVER'",
        "aliases": ["Lunar Series", "Perth Lunar", "Lunar Silver"],
        "notes": "Features Chinese Zodiac animals. Series I (1999-2010), Series II (2008-2019), Series III (2020+).",
    },
    {
        "country": "AU",
        "code": "AEMU",
        "name": "Australian Emu 1 oz",
        "denomination": "One Dollar",
        "start_year": 2018,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"silver": 99.99},
        "weight_grams": 31.1035,
        "diameter_mm": 40.6,
        "edge": "Reeded",
        "designer": "Perth Mint",
        "mint_mark": "P",
        "obverse": "Monarch effigy, 'AUSTRALIA', '1 DOLLAR', date",
        "reverse": "Emu design, '1oz 9999 SILVER'",
        "aliases": ["Silver Emu", "Australian Emu"],
        "notes": "Limited mintage Perth Mint series. Highly collectible.",
    },
    {
        "country": "AU",
        "code": "KOAL",
        "name": "Australian Koala 1 oz",
        "denomination": "One Dollar",
        "start_year": 2007,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"silver": 99.99},
        "weight_grams": 31.1035,
        "diameter_mm": 40.6,
        "edge": "Reeded",
        "designer": "Perth Mint",
        "mint_mark": "P",
        "obverse": "Monarch effigy, 'AUSTRALIA', '1 DOLLAR', date",
        "reverse": "Koala design (changes annually), '1oz 9999 SILVER'",
        "aliases": ["Silver Koala", "Australian Koala"],
        "notes": "Perth Mint bullion coin. Design changes annually.",
    },
    {
        "country": "GB",
        "code": "QBST",
        "name": "Queen's Beasts 2 oz",
        "denomination": "Five Pounds",
        "start_year": 2016,
        "end_year": 2021,
        "weight_oz": 2.0,
        "composition": {"silver": 99.9},
        "weight_grams": 62.206,
        "diameter_mm": 38.61,
        "edge": "Reeded",
        "designer": "Royal Mint / Jody Clark",
        "mint_mark": "RM",
        "obverse": "Queen Elizabeth II effigy by Jody Clark, denomination",
        "reverse": "Heraldic beast design (Lion, Griffin, Dragon, Unicorn, etc.)",
        "aliases": ["Queen's Beasts", "Queens Beasts", "Royal Beasts"],
        "notes": "10-coin series featuring heraldic beasts from coronation ceremony. Completed 2021.",
    },
    {
        "country": "AM",
        "code": "NOAH",
        "name": "Noah's Ark 1 oz",
        "denomination": "500 Dram",
        "start_year": 2011,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"silver": 99.9},
        "weight_grams": 31.1035,
        "diameter_mm": 38.6,
        "edge": "Reeded",
        "designer": "Geiger Edelmetalle / Central Bank of Armenia",
        "mint_mark": "G",
        "obverse": "Armenian coat of arms, 'REPUBLIC OF ARMENIA', '500 DRAM', date",
        "reverse": "Noah's Ark with Mt. Ararat, dove with olive branch, '1 OZ', '.999 SILVER'",
        "aliases": ["Armenian Noah's Ark", "Noah Ark", "Armenia Silver"],
        "notes": "Legal tender of Armenia. Minted by Geiger Edelmetalle (Germany). Popular low-premium bullion.",
    },
    {
        "country": "KR",
        "code": "CHWO",
        "name": "Chiwoo Cheonwang 1 oz",
        "denomination": "1 Clay",
        "start_year": 2016,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"silver": 99.9},
        "weight_grams": 31.1035,
        "diameter_mm": 40.0,
        "edge": "Reeded",
        "designer": "KOMSCO (Korea Minting and Security Printing Corporation)",
        "mint_mark": "K",
        "obverse": "KOMSCO logo, 'REPUBLIC OF KOREA', '1 CLAY', date",
        "reverse": "Chiwoo Cheonwang (god of war) warrior design, '1oz', 'Ag .999'",
        "aliases": ["Chiwoo", "Korean Chiwoo", "South Korean Silver"],
        "notes": "Minted by KOMSCO. Design changes annually. Highly collectible Korean bullion.",
    },
]

# Vintage Bars and Pours
VINTAGE_BAR_SERIES = [
    {
        "country": "US",
        "code": "ENGP",
        "name": "Engelhard Prospector 1 oz",
        "denomination": "No Face Value",
        "start_year": 1982,
        "end_year": 1988,
        "weight_oz": 1.0,
        "composition": {"silver": 99.9},
        "weight_grams": 31.1035,
        "diameter_mm": 39.0,
        "edge": "Reeded",
        "designer": "Engelhard Corporation",
        "mint_mark": "X",
        "obverse": "Prospector panning for gold, 'ENGELHARD', '1 TROY OUNCE'",
        "reverse": "Eagle design, '.999+ FINE SILVER'",
        "aliases": ["Engelhard Prospector", "Prospector Round", "E Prospector"],
        "notes": "Collectible vintage silver rounds. Multiple varieties exist (Wide/Narrow date, etc.).",
    },
    {
        "country": "US",
        "code": "ENG5",
        "name": "Engelhard Bar 5 oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": 1988,
        "weight_oz": 5.0,
        "composition": {"silver": 99.9},
        "weight_grams": 155.517,
        "diameter_mm": None,
        "edge": "Plain",
        "designer": "Engelhard Corporation",
        "mint_mark": "X",
        "obverse": "Engelhard logo, serial number, '5 TROY OZ', '.999+ FINE SILVER'",
        "reverse": "Blank or Engelhard hallmark",
        "aliases": ["Engelhard 5oz", "Engelhard 5 oz Bar"],
        "notes": "Vintage poured and pressed silver bars. Multiple varieties (P-loaf, pressed). Highly collectible.",
    },
    {
        "country": "US",
        "code": "EN10",
        "name": "Engelhard Bar 10 oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": 1988,
        "weight_oz": 10.0,
        "composition": {"silver": 99.9},
        "weight_grams": 311.035,
        "diameter_mm": None,
        "edge": "Plain",
        "designer": "Engelhard Corporation",
        "mint_mark": "X",
        "obverse": "Engelhard logo, serial number, '10 TROY OZ', '.999+ FINE SILVER'",
        "reverse": "Blank or Engelhard hallmark",
        "aliases": ["Engelhard 10oz", "Engelhard 10 oz Bar"],
        "notes": "Vintage poured and pressed silver bars. Wide variety of hallmarks and configurations.",
    },
    {
        "country": "US",
        "code": "E100",
        "name": "Engelhard Bar 100 oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": 1988,
        "weight_oz": 100.0,
        "composition": {"silver": 99.9},
        "weight_grams": 3110.35,
        "diameter_mm": None,
        "edge": "Plain",
        "designer": "Engelhard Corporation",
        "mint_mark": "X",
        "obverse": "Engelhard logo, serial number, '100 TROY OZ', '.999+ FINE SILVER'",
        "reverse": "Blank or Engelhard hallmark",
        "aliases": ["Engelhard 100oz", "Engelhard 100 oz Bar", "Engelhard Monster Bar"],
        "notes": "Vintage 100oz bars. Investment grade silver. Serial numbered.",
    },
    {
        "country": "US",
        "code": "JMTB",
        "name": "Johnson Matthey Bar",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": None,
        "weight_oz": 1.0,  # Various weights, 1oz default
        "composition": {"silver": 99.9},
        "weight_grams": 31.1035,
        "diameter_mm": None,
        "edge": "Plain",
        "designer": "Johnson Matthey",
        "mint_mark": "X",
        "obverse": "Johnson Matthey logo, serial number, weight, '.999+ FINE SILVER'",
        "reverse": "Blank or JM hallmark",
        "aliases": ["JM Bar", "Johnson Matthey", "JM Silver"],
        "notes": "Classic refiner silver bars. Available in 1oz, 5oz, 10oz, 100oz. Multiple vintage varieties.",
    },
    {
        "country": "US",
        "code": "SCOT",
        "name": "Scottsdale Mint Silver",
        "denomination": "No Face Value",
        "start_year": 2005,
        "end_year": None,
        "weight_oz": 1.0,  # Various weights
        "composition": {"silver": 99.9},
        "weight_grams": 31.1035,
        "diameter_mm": None,
        "edge": "Plain",
        "designer": "Scottsdale Mint",
        "mint_mark": "X",
        "obverse": "Scottsdale Mint logo, weight, '.999 FINE SILVER'",
        "reverse": "Varies by product (Stacker, Chunky, Lion, etc.)",
        "aliases": ["Scottsdale Stacker", "Scottsdale Silver", "Chunky"],
        "notes": "Popular modern poured and pressed bars. Stackers, Chunky bars, and Lion series highly collected.",
    },
]

# World Gold Catch-all
WORLD_GOLD_SERIES = [
    {
        "country": "XX",
        "code": "WGLD",
        "name": "World Gold Sovereigns",
        "denomination": "Various",
        "start_year": 1800,
        "end_year": None,
        "weight_oz": 1.0,  # Varies
        "composition": {"gold": 91.67},  # Traditional sovereign 22k
        "weight_grams": 7.988,  # Traditional sovereign weight
        "diameter_mm": 22.05,  # Traditional sovereign diameter
        "edge": "Reeded",
        "designer": "Various",
        "mint_mark": "X",
        "obverse": "Various monarch/national designs",
        "reverse": "Various national designs (St. George, coat of arms, etc.)",
        "aliases": ["Foreign Gold", "World Gold", "Gold Sovereign", "Sovereign"],
        "notes": "Catch-all for foreign gold sovereigns and similar gold coins. Includes British, Australian, South African sovereigns, etc.",
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


def add_series_to_database(conn, series_list, category_name):
    """Add a list of series to the database"""
    cursor = conn.cursor()
    added = 0

    for series in series_list:
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

        # Handle None diameter (for bars)
        diameter = series.get("diameter_mm")

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
            diameter,
            series.get("edge", "Plain"),
            series["designer"],
            series["obverse"],
            series["reverse"],
            f"Random year bullion - valued by metal content. {series.get('notes', '')}".strip(),
            f"Issue #90 - {category_name}",
        ))

        added += 1
        print(f"  Added series_registry entry and bullion entry {xxxx_coin_id}")

    conn.commit()
    return added


def verify_additions(conn):
    """Verify all series were added correctly"""
    cursor = conn.cursor()

    # Count new series
    cursor.execute("""
        SELECT COUNT(*) FROM series_registry
        WHERE series_abbreviation IN ('ROOS', 'LUNR', 'AEMU', 'KOAL', 'QBST', 'NOAH', 'CHWO',
                                       'ENGP', 'ENG5', 'EN10', 'E100', 'JMTB', 'SCOT', 'WGLD')
    """)
    registry_count = cursor.fetchone()[0]

    # Count new coins
    cursor.execute("""
        SELECT COUNT(*) FROM coins
        WHERE coin_id LIKE '%-ROOS-%' OR coin_id LIKE '%-LUNR-%' OR coin_id LIKE '%-AEMU-%'
           OR coin_id LIKE '%-KOAL-%' OR coin_id LIKE '%-QBST-%' OR coin_id LIKE '%-NOAH-%'
           OR coin_id LIKE '%-CHWO-%' OR coin_id LIKE '%-ENGP-%' OR coin_id LIKE '%-ENG5-%'
           OR coin_id LIKE '%-EN10-%' OR coin_id LIKE '%-E100-%' OR coin_id LIKE '%-JMTB-%'
           OR coin_id LIKE '%-SCOT-%' OR coin_id LIKE '%-WGLD-%'
    """)
    coin_count = cursor.fetchone()[0]

    print(f"\nVerification:")
    print(f"  Series registry entries: {registry_count} (expected: 14)")
    print(f"  Coin entries: {coin_count} (expected: 14)")

    # Show country breakdown
    cursor.execute("""
        SELECT DISTINCT country_code FROM series_registry
        WHERE series_abbreviation IN ('ROOS', 'LUNR', 'AEMU', 'KOAL', 'QBST', 'NOAH', 'CHWO',
                                       'ENGP', 'ENG5', 'EN10', 'E100', 'JMTB', 'SCOT', 'WGLD')
        ORDER BY country_code
    """)
    countries = [row[0] for row in cursor.fetchall()]
    print(f"  Countries: {', '.join(countries)}")

    return registry_count == 14 and coin_count == 14


def main():
    db_path = Path(__file__).parent.parent / "database" / "coins.db"

    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return 1

    # Backup database first
    backup_path = backup_database(db_path)

    conn = sqlite3.connect(db_path)
    try:
        print("\n=== Adding World Silver Coins ===")
        world_silver_count = add_series_to_database(conn, WORLD_SILVER_SERIES, "World Silver Coins")

        print("\n=== Adding Vintage Bars/Pours ===")
        vintage_bar_count = add_series_to_database(conn, VINTAGE_BAR_SERIES, "Vintage Bars/Pours")

        print("\n=== Adding World Gold Catch-all ===")
        world_gold_count = add_series_to_database(conn, WORLD_GOLD_SERIES, "World Gold Catch-all")

        print(f"\n{'='*50}")
        print(f"Added {world_silver_count} world silver coin series")
        print(f"Added {vintage_bar_count} vintage bar/pour series")
        print(f"Added {world_gold_count} world gold catch-all series")
        print(f"Total: {world_silver_count + vintage_bar_count + world_gold_count} series")

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
