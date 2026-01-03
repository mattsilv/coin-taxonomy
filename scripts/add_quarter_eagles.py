#!/usr/bin/env python3
"""
Add US Quarter Eagle ($2.50 Gold) type codes to the coin taxonomy database.
Issue #76

Adds:
- LHQE: Liberty Head Quarter Eagle (1840-1907)
- IHQE: Indian Head Quarter Eagle (1908-1929)
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Quarter eagle series definitions
QUARTER_EAGLE_SERIES = [
    {
        "code": "LHQE",
        "name": "Liberty Head Quarter Eagle",
        "denomination": "$2.50",
        "start_year": 1840,
        "end_year": 1907,
        "seed_year": 1840,
        "seed_mint": "P",
        "designer": "Christian Gobrecht",
        "obverse": "Liberty head left wearing coronet inscribed 'LIBERTY', 13 stars around, date below",
        "reverse": "Heraldic eagle with shield, holding arrows and olive branch, 'UNITED STATES OF AMERICA' above, '$2.50 D.' below",
        "composition": {"gold": 90, "copper": 10},
        "weight_grams": 4.18,
        "diameter_mm": 18.0,
        "edge": "Reeded",
        "aliases": ["Liberty Quarter Eagle", "Liberty $2.50", "Coronet Quarter Eagle"],
        "notes": "The Liberty Head (Coronet) design was used for the $2.50 gold piece from 1840-1907. Earlier types (1796-1839) have different designs.",
    },
    {
        "code": "IHQE",
        "name": "Indian Head Quarter Eagle",
        "denomination": "$2.50",
        "start_year": 1908,
        "end_year": 1929,
        "seed_year": 1908,
        "seed_mint": "P",
        "designer": "Bela Lyon Pratt",
        "obverse": "Indian chief wearing feathered headdress facing left (incuse design), 13 stars at left, date at right, 'LIBERTY' above",
        "reverse": "Standing eagle on bundle of arrows with olive branch (incuse design), 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', '2 1/2 DOLLARS'",
        "composition": {"gold": 90, "copper": 10},
        "weight_grams": 4.18,
        "diameter_mm": 18.0,
        "edge": "Reeded",
        "aliases": ["Indian Quarter Eagle", "Indian $2.50", "Incuse Quarter Eagle"],
        "notes": "Unique incuse (recessed) design - the only regular-issue US coins with incuse design. Controversial when introduced but now highly prized by collectors.",
    },
]


def add_quarter_eagles(conn):
    """Add quarter eagle series to database"""
    cursor = conn.cursor()

    for series in QUARTER_EAGLE_SERIES:
        code = series["code"]
        name = series["name"]
        print(f"Adding {name} ({code})...")

        # Add to series_registry
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases
            ) VALUES (?, ?, ?, 'US', ?, ?, ?, ?, ?, 'coin', ?)
        """, (
            f"{name}__$2.50",
            name,
            code,
            series["denomination"],
            series["start_year"],
            series["end_year"],
            series.get("notes", f"US ${series['denomination']} gold coin"),
            name,
            json.dumps(series.get("aliases", [])),
        ))

        # Add seed coin
        coin_id = f"US-{code}-{series['seed_year']}-{series['seed_mint']}"
        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, notes, rarity,
                source_citation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', 'Red Book')
        """, (
            coin_id,
            str(series["seed_year"]),
            series["seed_mint"],
            series["denomination"],
            name,
            json.dumps(series["composition"]),
            series["weight_grams"],
            series["diameter_mm"],
            series["edge"],
            series["designer"],
            series["obverse"],
            series["reverse"],
            series.get("notes"),
        ))

        print(f"  ✓ Added series_registry entry and seed coin {coin_id}")

    conn.commit()
    print(f"\n✅ Added {len(QUARTER_EAGLE_SERIES)} quarter eagle series")


def main():
    db_path = Path(__file__).parent.parent / "database" / "coins.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return 1

    conn = sqlite3.connect(db_path)
    try:
        add_quarter_eagles(conn)
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    exit(main())
