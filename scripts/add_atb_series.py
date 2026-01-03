#!/usr/bin/env python3
"""
Add America the Beautiful series to the database.

Addresses GitHub Issues #77 (ATB 5oz Silver Bullion) and #78 (ATB Quarters).

ATB Program ran from 2010-2021 with 56 designs (5 per year 2010-2020, 1 in 2021).
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "database" / "coins.db"

# ATB 5oz Silver Bullion (Issue #77)
ATB_5OZ_SERIES = {
    "type_code": "ATB5",
    "series_name": "America the Beautiful 5oz Silver",
    "denomination": "5oz Silver",
    "start_year": 2010,
    "end_year": 2021,
    "weight_grams": 155.52,  # 5 troy oz
    "diameter_mm": 76.2,  # 3 inches
    "composition": "99.9% Silver",
    "edge": "plain",
}

# ATB Quarters (Issue #78)
ATB_QUARTERS_SERIES = {
    "type_code": "ATBQ",
    "series_name": "America the Beautiful Quarters",
    "denomination": "Quarters",
    "start_year": 2010,
    "end_year": 2021,
    "weight_grams": 5.67,
    "diameter_mm": 24.26,
    "composition": "Clad",
    "edge": "reeded",
}

# Sample ATB designs for seed coins (first and last of the program)
ATB_SEED_COINS = [
    # First ATB design
    {"year": 2010, "name": "Hot Springs", "state": "AR"},
    # Last ATB design
    {"year": 2021, "name": "Tuskegee Airmen", "state": "AL"},
]


def add_series_registry_entry(cursor, series_info):
    """Add series to series_registry table."""
    series_id = f"US-{series_info['type_code']}"
    cursor.execute("""
        INSERT OR IGNORE INTO series_registry (
            series_id, series_name, series_abbreviation, country_code,
            denomination, start_year, end_year
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        series_id,
        series_info["series_name"],
        series_info["type_code"],
        "US",
        series_info["denomination"],
        series_info["start_year"],
        series_info["end_year"],
    ))
    return cursor.rowcount


def add_coin(cursor, coin_id, series_info, year, mint, notes=None):
    """Add a coin entry to the database."""
    cursor.execute("""
        INSERT OR IGNORE INTO coins (
            coin_id, year, mint, denomination, series,
            weight_grams, diameter_mm, composition, edge, notes,
            source_citation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        coin_id,
        str(year),
        mint,
        series_info["denomination"],
        series_info["series_name"],
        series_info["weight_grams"],
        series_info["diameter_mm"],
        series_info["composition"],
        series_info["edge"],
        notes,
        "Issue #77/#78 - America the Beautiful Series"
    ))
    return cursor.rowcount


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    stats = {"registry_added": 0, "coins_added": 0}

    print("=" * 60)
    print("Adding America the Beautiful Series")
    print("=" * 60)

    # Add ATB 5oz Silver Bullion (Issue #77)
    print("\n--- ATB 5oz Silver Bullion (Issue #77) ---")
    if add_series_registry_entry(cursor, ATB_5OZ_SERIES):
        stats["registry_added"] += 1
        print(f"✓ Added series_registry: {ATB_5OZ_SERIES['series_name']}")
    else:
        print(f"  (already exists: {ATB_5OZ_SERIES['series_name']})")

    # Add XXXX-P entry for random year 5oz bullion
    coin_id = f"US-{ATB_5OZ_SERIES['type_code']}-XXXX-P"
    if add_coin(cursor, coin_id, ATB_5OZ_SERIES, "XXXX", "P",
                "Random year bullion - 5oz silver"):
        stats["coins_added"] += 1
        print(f"✓ Added coin: {coin_id}")

    # Add sample year entries for 5oz
    for seed in ATB_SEED_COINS:
        coin_id = f"US-{ATB_5OZ_SERIES['type_code']}-{seed['year']}-P"
        notes = f"{seed['name']} National Park ({seed['state']})"
        if add_coin(cursor, coin_id, ATB_5OZ_SERIES, seed['year'], "P", notes):
            stats["coins_added"] += 1
            print(f"✓ Added coin: {coin_id} - {seed['name']}")

    # Add ATB Quarters (Issue #78)
    print("\n--- ATB Quarters (Issue #78) ---")
    if add_series_registry_entry(cursor, ATB_QUARTERS_SERIES):
        stats["registry_added"] += 1
        print(f"✓ Added series_registry: {ATB_QUARTERS_SERIES['series_name']}")
    else:
        print(f"  (already exists: {ATB_QUARTERS_SERIES['series_name']})")

    # Add seed coins for ATB Quarters (P and D mints)
    for seed in ATB_SEED_COINS:
        for mint in ["P", "D"]:
            coin_id = f"US-{ATB_QUARTERS_SERIES['type_code']}-{seed['year']}-{mint}"
            notes = f"{seed['name']} ({seed['state']})"
            if add_coin(cursor, coin_id, ATB_QUARTERS_SERIES, seed['year'], mint, notes):
                stats["coins_added"] += 1
                print(f"✓ Added coin: {coin_id}")

    conn.commit()

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Series registry entries added: {stats['registry_added']}")
    print(f"  Coins added: {stats['coins_added']}")
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    main()
