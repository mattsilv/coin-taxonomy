#!/usr/bin/env python3
"""
Add missing bullion taxonomy codes for price comparison.
Issue #130

Adds 11 bullion product codes needed by the u2-server price comparison system:
- GB-BGBO: British Gold Britannia 1 oz
- GB-BGBT: British Gold Britannia 1/10 oz
- GB-BSBO: British Silver Britannia 1 oz
- XX-GNSR: Generic Silver Round 1 oz
- XX-GSB1: Generic Silver Bar 1 oz
- XX-GSB5: Generic Silver Bar 5 oz
- XX-GS10: Generic Silver Bar 10 oz
- XX-G100: Generic Silver Bar 100 oz
- US-JS90: Junk Silver 90% ($10 Face Value)
- US-APEO: American Platinum Eagle 1 oz
- XX-GNGB: Generic Gold Bar 1 oz

Each includes a XXXX entry for random year bullion purchases.
"""

import sqlite3
import json
import shutil
from datetime import datetime
from pathlib import Path

BULLION_SERIES = [
    # --- British Britannias ---
    {
        "country": "GB",
        "code": "BGBO",
        "name": "British Gold Britannia (1 oz)",
        "series_id": "british_gold_britannia_1oz",
        "denomination": "100 Pounds",
        "start_year": 1987,
        "end_year": None,
        "weight_grams": 31.1035,
        "diameter_mm": 32.69,
        "composition": ".9999 Au",
        "edge": "Reeded",
        "designer": "Royal Mint",
        "obverse": "Monarch portrait, '100 POUNDS', 'ELIZABETH II' or 'CHARLES III', date",
        "reverse": "Britannia standing with trident and shield, 'BRITANNIA', '1 OZ 9999 FINE GOLD'",
        "aliases": ["Gold Britannia", "Brit Gold", "Royal Mint Gold Britannia", "1 oz Gold Britannia"],
        "series_group": "Britannia",
        "mint": "RM",
        "type": "bullion",
    },
    {
        "country": "GB",
        "code": "BGBT",
        "name": "British Gold Britannia (1/10 oz)",
        "series_id": "british_gold_britannia_110oz",
        "denomination": "10 Pounds",
        "start_year": 1987,
        "end_year": None,
        "weight_grams": 3.1103,
        "diameter_mm": 16.50,
        "composition": ".9999 Au",
        "edge": "Reeded",
        "designer": "Royal Mint",
        "obverse": "Monarch portrait, '10 POUNDS', date",
        "reverse": "Britannia standing with trident and shield, '1/10 OZ 9999 FINE GOLD'",
        "aliases": ["1/10 oz Gold Britannia", "Tenth oz Britannia"],
        "series_group": "Britannia",
        "mint": "RM",
        "type": "bullion",
    },
    {
        "country": "GB",
        "code": "BSBO",
        "name": "British Silver Britannia (1 oz)",
        "series_id": "british_silver_britannia_1oz",
        "denomination": "2 Pounds",
        "start_year": 1997,
        "end_year": None,
        "weight_grams": 31.1035,
        "diameter_mm": 38.61,
        "composition": ".999 Ag",
        "edge": "Reeded",
        "designer": "Royal Mint",
        "obverse": "Monarch portrait, '2 POUNDS', date",
        "reverse": "Britannia standing with trident and shield, 'BRITANNIA', '1 OZ 999 FINE SILVER'",
        "aliases": ["Silver Britannia", "Brit Silver", "Royal Mint Silver Britannia", "1 oz Silver Britannia"],
        "series_group": "Britannia",
        "mint": "RM",
        "type": "bullion",
    },
    # --- Generic Silver ---
    {
        "country": "XX",
        "code": "GNSR",
        "name": "Generic Silver Round (1 oz)",
        "series_id": "generic_silver_round_1oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": None,
        "weight_grams": 31.1035,
        "diameter_mm": 39.0,
        "composition": ".999 Ag",
        "edge": "Varies",
        "designer": "Various private mints",
        "obverse": "Various designs by private mints",
        "reverse": "Various designs, '.999 Fine Silver', '1 Troy Oz'",
        "aliases": ["Silver Round", ".999 Silver Round", "Generic Silver Round", "1 oz Silver Round"],
        "series_group": "Generic Silver",
        "mint": "X",
        "type": "bullion",
        "notes": "Generic 1 oz .999 silver rounds from various private mints. Valued by metal content only.",
    },
    {
        "country": "XX",
        "code": "GSB1",
        "name": "Generic Silver Bar (1 oz)",
        "series_id": "generic_silver_bar_1oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": None,
        "weight_grams": 31.1035,
        "diameter_mm": None,
        "composition": ".999 Ag",
        "edge": None,
        "designer": "Various private mints",
        "obverse": "Various designs or plain",
        "reverse": "Various designs, '.999 Fine Silver', '1 Troy Oz'",
        "aliases": ["1 oz Silver Bar", ".999 Silver Bar", "Silver Bar"],
        "series_group": "Generic Silver",
        "mint": "X",
        "type": "bullion",
        "notes": "Generic 1 oz .999 silver bar from various private mints.",
    },
    {
        "country": "XX",
        "code": "GSB5",
        "name": "Generic Silver Bar (5 oz)",
        "series_id": "generic_silver_bar_5oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": None,
        "weight_grams": 155.517,
        "diameter_mm": None,
        "composition": ".999 Ag",
        "edge": None,
        "designer": "Various private mints",
        "obverse": "Various designs or plain",
        "reverse": "Various designs, '.999 Fine Silver', '5 Troy Oz'",
        "aliases": ["5 oz Silver Bar", "Silver Bar 5 oz"],
        "series_group": "Generic Silver",
        "mint": "X",
        "type": "bullion",
        "notes": "Generic 5 oz .999 silver bar from various private mints.",
    },
    {
        "country": "XX",
        "code": "GS10",
        "name": "Generic Silver Bar (10 oz)",
        "series_id": "generic_silver_bar_10oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": None,
        "weight_grams": 311.035,
        "diameter_mm": None,
        "composition": ".999 Ag",
        "edge": None,
        "designer": "Various private mints",
        "obverse": "Various designs or plain",
        "reverse": "Various designs, '.999 Fine Silver', '10 Troy Oz'",
        "aliases": ["10 oz Silver Bar", "Silver Bar 10 oz"],
        "series_group": "Generic Silver",
        "mint": "X",
        "type": "bullion",
        "notes": "Generic 10 oz .999 silver bar from various private mints.",
    },
    {
        "country": "XX",
        "code": "G100",
        "name": "Generic Silver Bar (100 oz)",
        "series_id": "generic_silver_bar_100oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": None,
        "weight_grams": 3110.35,
        "diameter_mm": None,
        "composition": ".999 Ag",
        "edge": None,
        "designer": "Various private mints",
        "obverse": "Various designs or plain",
        "reverse": "Various designs, '.999 Fine Silver', '100 Troy Oz'",
        "aliases": ["100 oz Silver Bar", "Silver Bar 100 oz"],
        "series_group": "Generic Silver",
        "mint": "X",
        "type": "bullion",
        "notes": "Generic 100 oz .999 silver bar from various private mints.",
    },
    # --- Junk Silver ---
    {
        "country": "US",
        "code": "JS90",
        "name": "Junk Silver 90% ($10 Face Value)",
        "series_id": "junk_silver_90pct",
        "denomination": "$10 Face Value",
        "start_year": 1892,
        "end_year": None,
        "weight_grams": 715.0,
        "diameter_mm": None,
        "composition": ".900 Ag (mixed denominations)",
        "edge": None,
        "designer": "Various (US Mint)",
        "obverse": "Mixed pre-1965 US silver coins (dimes, quarters, half dollars)",
        "reverse": "Mixed pre-1965 US silver coins",
        "aliases": ["Junk Silver", "90% Silver", "Constitutional Silver", "$10 FV Silver", "Pre-1965 Silver", "90% Silver Bag"],
        "series_group": None,
        "mint": "X",
        "type": "bullion",
        "notes": "Bag of pre-1965 US 90% silver coins (dimes, quarters, half dollars). $10 face value contains approximately 7.15 troy oz silver content. Valued by metal content.",
    },
    # --- American Platinum Eagle ---
    {
        "country": "US",
        "code": "APEO",
        "name": "American Platinum Eagle (1 oz)",
        "series_id": "american_platinum_eagle_1oz",
        "denomination": "$100",
        "start_year": 1997,
        "end_year": None,
        "weight_grams": 31.1035,
        "diameter_mm": 32.70,
        "composition": ".9995 Pt",
        "edge": "Reeded",
        "designer": "US Mint",
        "obverse": "Statue of Liberty head, 'LIBERTY', 'IN GOD WE TRUST', date, 'E PLURIBUS UNUM'",
        "reverse": "Eagle soaring over sun (varies by year for proof), '$100', '1 OZ.', '.9995 PLATINUM'",
        "aliases": ["Platinum Eagle", "American Platinum Eagle", "APE", "1 oz Platinum Eagle"],
        "series_group": "American Eagle",
        "mint": "W",
        "type": "bullion",
    },
    # --- Generic Gold Bar ---
    {
        "country": "XX",
        "code": "GNGB",
        "name": "Generic Gold Bar (1 oz)",
        "series_id": "generic_gold_bar_1oz",
        "denomination": "No Face Value",
        "start_year": 1970,
        "end_year": None,
        "weight_grams": 31.1035,
        "diameter_mm": None,
        "composition": ".999 Au",
        "edge": None,
        "designer": "Various private mints",
        "obverse": "Various designs or plain",
        "reverse": "Various designs, '.999 Fine Gold', '1 Troy Oz'",
        "aliases": ["Gold Bar", "1 oz Gold Bar", ".999 Gold Bar", "Generic Gold Bar"],
        "series_group": "Generic Gold",
        "mint": "X",
        "type": "bullion",
        "notes": "Generic 1 oz .999 gold bar from various private mints. Valued by metal content only.",
    },
]


def add_missing_bullion(conn):
    """Add missing bullion series to database."""
    cursor = conn.cursor()
    added = 0

    for series in BULLION_SERIES:
        country = series["country"]
        code = series["code"]
        name = series["name"]
        coin_id = f"{country}-{code}-XXXX-{series['mint']}"
        print(f"Adding {name} ({coin_id})...")

        # Add to series_registry
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases, series_group
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            series["series_id"],
            name,
            code,
            country,
            series["denomination"],
            series["start_year"],
            series["end_year"],
            f"Bullion, {series['weight_grams']}g, {series['composition']}",
            name,
            series["type"],
            json.dumps(series["aliases"]),
            series.get("series_group"),
        ))

        # Add XXXX entry for random year bullion
        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, notes, rarity,
                source_citation
            ) VALUES (?, 'XXXX', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', 'Official mint specifications')
        """, (
            coin_id,
            series["mint"],
            series["denomination"],
            name,
            series["composition"],
            series["weight_grams"],
            series["diameter_mm"],
            series["edge"],
            series["designer"],
            series["obverse"],
            series["reverse"],
            f"Random year bullion - valued by metal content. {series.get('notes', '')}".strip(),
        ))

        added += 1
        print(f"  -> Added series_registry entry and bullion entry {coin_id}")

    conn.commit()
    print(f"\n{added} bullion series added successfully")


def verify(conn):
    """Verify all entries were added."""
    cursor = conn.cursor()
    codes = [s["code"] for s in BULLION_SERIES]

    cursor.execute(
        f"SELECT series_abbreviation FROM series_registry WHERE series_abbreviation IN ({','.join('?' * len(codes))})",
        codes,
    )
    found_series = {row[0] for row in cursor.fetchall()}

    coin_ids = [f"{s['country']}-{s['code']}-XXXX-{s['mint']}" for s in BULLION_SERIES]
    cursor.execute(
        f"SELECT coin_id FROM coins WHERE coin_id IN ({','.join('?' * len(coin_ids))})",
        coin_ids,
    )
    found_coins = {row[0] for row in cursor.fetchall()}

    print(f"\nVerification:")
    print(f"  series_registry: {len(found_series)}/{len(codes)} entries found")
    print(f"  coins table:     {len(found_coins)}/{len(coin_ids)} entries found")

    missing_series = set(codes) - found_series
    missing_coins = set(coin_ids) - found_coins
    if missing_series:
        print(f"  MISSING series: {missing_series}")
    if missing_coins:
        print(f"  MISSING coins: {missing_coins}")

    return len(missing_series) == 0 and len(missing_coins) == 0


def main():
    db_path = Path(__file__).parent.parent / "database" / "coins.db"

    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return 1

    # Create backup
    backup_dir = Path(__file__).parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / f"coins_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}\n")

    conn = sqlite3.connect(db_path)
    try:
        add_missing_bullion(conn)
        success = verify(conn)
        if not success:
            print("\nVerification failed!")
            return 1
    finally:
        conn.close()

    print("\nNext step: uv run python scripts/export_from_database.py")
    return 0


if __name__ == "__main__":
    exit(main())
