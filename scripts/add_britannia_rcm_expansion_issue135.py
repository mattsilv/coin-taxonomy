#!/usr/bin/env python3
"""
Add expanded Britannia sizes and RCM/Royal Mint 10oz bar codes.
Issue #135

Adds 6 new bullion entries using weight suffixes on existing series:
- GB-BSBO-XXXX-RM-2oz:  British Silver Britannia 2 oz
- GB-BSBO-XXXX-RM-10oz: British Silver Britannia 10 oz
- GB-BGBO-XXXX-RM-14oz: British Gold Britannia 1/4 oz
- GB-BGBO-XXXX-RM-12oz: British Gold Britannia 1/2 oz

New series:
- CA-RCMB-XXXX-P-10oz:  RCM Silver Bar 10 oz
- GB-RMSB-XXXX-RM-10oz: Royal Mint Silver Bar 10 oz
"""

import sqlite3
import json
import shutil
from datetime import datetime
from pathlib import Path

# New series to create
NEW_SERIES = [
    {
        "series_id": "rcm_silver_bar",
        "series_name": "RCM Silver Bar",
        "series_abbreviation": "RCMB",
        "country_code": "CA",
        "denomination": "Silver Bar",
        "start_year": 2000,
        "end_year": None,
        "defining_characteristics": "Bullion, .9999 Ag, Royal Canadian Mint branded bar",
        "official_name": "RCM Silver Bar",
        "type": "bullion",
        "aliases": ["RCM Silver Bar", "Royal Canadian Mint Silver Bar", "RCM Bar"],
        "variety_suffixes": ["10oz"],
        "series_group": "RCM Bars",
    },
    {
        "series_id": "royal_mint_silver_bar",
        "series_name": "Royal Mint Silver Bar",
        "series_abbreviation": "RMSB",
        "country_code": "GB",
        "denomination": "Silver Bar",
        "start_year": 2010,
        "end_year": None,
        "defining_characteristics": "Bullion, .999 Ag, Royal Mint branded bar",
        "official_name": "Royal Mint Silver Bar",
        "type": "bullion",
        "aliases": ["Royal Mint Silver Bar", "Royal Mint Bar", "Britannia Silver Bar"],
        "variety_suffixes": ["10oz"],
        "series_group": "Royal Mint Bars",
    },
]

# New coin entries (weight suffix coins on existing or new series)
NEW_COINS = [
    # Britannia Silver fractionals
    {
        "coin_id": "GB-BSBO-XXXX-RM-2oz",
        "mint": "RM",
        "denomination": "5 Pounds",
        "series": "British Silver Britannia (1 oz)",
        "composition": ".999 Ag",
        "weight_grams": 62.207,
        "diameter_mm": 38.61,
        "edge": "Reeded",
        "designer": "Royal Mint",
        "obverse": "Monarch portrait, '5 POUNDS', date",
        "reverse": "Britannia standing with trident and shield, 'BRITANNIA', '2 OZ 999 FINE SILVER'",
        "notes": "Random year bullion - 2 oz Silver Britannia. Valued by metal content.",
    },
    {
        "coin_id": "GB-BSBO-XXXX-RM-10oz",
        "mint": "RM",
        "denomination": "10 Pounds",
        "series": "British Silver Britannia (1 oz)",
        "composition": ".999 Ag",
        "weight_grams": 311.035,
        "diameter_mm": 65.0,
        "edge": "Reeded",
        "designer": "Royal Mint",
        "obverse": "Monarch portrait, '10 POUNDS', date",
        "reverse": "Britannia standing with trident and shield, 'BRITANNIA', '10 OZ 999 FINE SILVER'",
        "notes": "Random year bullion - 10 oz Silver Britannia. Valued by metal content.",
    },
    # Britannia Gold fractionals
    {
        "coin_id": "GB-BGBO-XXXX-RM-14oz",
        "mint": "RM",
        "denomination": "25 Pounds",
        "series": "British Gold Britannia (1 oz)",
        "composition": ".9999 Au",
        "weight_grams": 7.776,
        "diameter_mm": 22.00,
        "edge": "Reeded",
        "designer": "Royal Mint",
        "obverse": "Monarch portrait, '25 POUNDS', date",
        "reverse": "Britannia standing with trident and shield, 'BRITANNIA', '1/4 OZ 9999 FINE GOLD'",
        "notes": "Random year bullion - 1/4 oz Gold Britannia. Valued by metal content.",
    },
    {
        "coin_id": "GB-BGBO-XXXX-RM-12oz",
        "mint": "RM",
        "denomination": "50 Pounds",
        "series": "British Gold Britannia (1 oz)",
        "composition": ".9999 Au",
        "weight_grams": 15.552,
        "diameter_mm": 27.00,
        "edge": "Reeded",
        "designer": "Royal Mint",
        "obverse": "Monarch portrait, '50 POUNDS', date",
        "reverse": "Britannia standing with trident and shield, 'BRITANNIA', '1/2 OZ 9999 FINE GOLD'",
        "notes": "Random year bullion - 1/2 oz Gold Britannia. Valued by metal content.",
    },
    # RCM Silver Bar
    {
        "coin_id": "CA-RCMB-XXXX-P-10oz",
        "mint": "P",
        "denomination": "Silver Bar",
        "series": "RCM Silver Bar",
        "composition": ".9999 Ag",
        "weight_grams": 311.035,
        "diameter_mm": None,
        "edge": None,
        "designer": "Royal Canadian Mint",
        "obverse": "RCM logo, '.9999 Fine Silver', '10 oz'",
        "reverse": "Serial number, RCM hallmark",
        "notes": "Random year bullion - RCM branded 10 oz silver bar. Valued by metal content.",
    },
    # Royal Mint Silver Bar
    {
        "coin_id": "GB-RMSB-XXXX-RM-10oz",
        "mint": "RM",
        "denomination": "Silver Bar",
        "series": "Royal Mint Silver Bar",
        "composition": ".999 Ag",
        "weight_grams": 311.035,
        "diameter_mm": None,
        "edge": None,
        "designer": "Royal Mint",
        "obverse": "Royal Mint branding, '.999 Fine Silver', '10 oz'",
        "reverse": "Serial number, Royal Mint hallmark",
        "notes": "Random year bullion - Royal Mint branded 10 oz silver bar. Valued by metal content.",
    },
]

# Existing series to update with variety_suffixes
SERIES_UPDATES = [
    {"abbreviation": "BSBO", "variety_suffixes": ["2oz", "10oz"]},
    {"abbreviation": "BGBO", "variety_suffixes": ["14oz", "12oz"]},
]


def add_new_series(conn):
    """Insert new series_registry entries."""
    cursor = conn.cursor()
    for s in NEW_SERIES:
        print(f"Adding series: {s['series_abbreviation']} - {s['series_name']}")
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases, variety_suffixes, series_group
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["series_id"],
            s["series_name"],
            s["series_abbreviation"],
            s["country_code"],
            s["denomination"],
            s["start_year"],
            s["end_year"],
            s["defining_characteristics"],
            s["official_name"],
            s["type"],
            json.dumps(s["aliases"]),
            json.dumps(s["variety_suffixes"]),
            s["series_group"],
        ))
    conn.commit()


def update_existing_series(conn):
    """Update variety_suffixes on existing series."""
    cursor = conn.cursor()
    for u in SERIES_UPDATES:
        print(f"Updating variety_suffixes for {u['abbreviation']}: {u['variety_suffixes']}")
        cursor.execute("""
            UPDATE series_registry SET variety_suffixes = ?
            WHERE series_abbreviation = ?
        """, (json.dumps(u["variety_suffixes"]), u["abbreviation"]))
    conn.commit()


def add_new_coins(conn):
    """Insert new coin entries."""
    cursor = conn.cursor()
    for c in NEW_COINS:
        print(f"Adding coin: {c['coin_id']}")
        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, notes, rarity,
                source_citation
            ) VALUES (?, 'XXXX', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', 'Official mint specifications')
        """, (
            c["coin_id"],
            c["mint"],
            c["denomination"],
            c["series"],
            c["composition"],
            c["weight_grams"],
            c["diameter_mm"],
            c["edge"],
            c["designer"],
            c["obverse"],
            c["reverse"],
            c["notes"],
        ))
    conn.commit()


def verify(conn):
    """Verify all entries were added."""
    cursor = conn.cursor()

    # Check new series
    new_codes = [s["series_abbreviation"] for s in NEW_SERIES]
    cursor.execute(
        f"SELECT series_abbreviation FROM series_registry WHERE series_abbreviation IN ({','.join('?' * len(new_codes))})",
        new_codes,
    )
    found_series = {row[0] for row in cursor.fetchall()}

    # Check updated variety_suffixes
    for u in SERIES_UPDATES:
        cursor.execute(
            "SELECT variety_suffixes FROM series_registry WHERE series_abbreviation = ?",
            (u["abbreviation"],),
        )
        row = cursor.fetchone()
        if row and row[0]:
            print(f"  {u['abbreviation']} variety_suffixes: {row[0]}")
        else:
            print(f"  WARNING: {u['abbreviation']} variety_suffixes not set!")

    # Check new coins
    coin_ids = [c["coin_id"] for c in NEW_COINS]
    cursor.execute(
        f"SELECT coin_id FROM coins WHERE coin_id IN ({','.join('?' * len(coin_ids))})",
        coin_ids,
    )
    found_coins = {row[0] for row in cursor.fetchall()}

    print(f"\nVerification:")
    print(f"  New series:  {len(found_series)}/{len(new_codes)} entries found")
    print(f"  New coins:   {len(found_coins)}/{len(coin_ids)} entries found")

    missing_series = set(new_codes) - found_series
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
        add_new_series(conn)
        update_existing_series(conn)
        add_new_coins(conn)
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
