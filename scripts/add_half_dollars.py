#!/usr/bin/env python3
"""
Add US Half Dollar type codes to the coin taxonomy database.
Issue #73

Adds:
- BARH: Barber Half Dollar (1892-1915)
- WLHD: Walking Liberty Half Dollar (1916-1947)
- FRNH: Franklin Half Dollar (1948-1963)
- KENH: Kennedy Half Dollar (1964-present)

This creates lightweight stubs with series_registry entries and seed coins
to establish type codes. Full year coverage comes from series_registry.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Half dollar series definitions
HALF_DOLLAR_SERIES = [
    {
        "code": "BARH",
        "name": "Barber Half Dollar",
        "start_year": 1892,
        "end_year": 1915,
        "seed_year": 1892,
        "seed_mint": "P",
        "designer": "Charles E. Barber",
        "obverse": "Liberty head right wearing Phrygian cap with laurel wreath, 'LIBERTY' on band, 'IN GOD WE TRUST' above, stars around, date below",
        "reverse": "Heraldic eagle with shield, E PLURIBUS UNUM on ribbon, 'UNITED STATES OF AMERICA' and 'HALF DOLLAR' around",
        "composition": {"silver": 90, "copper": 10},
        "weight_grams": 12.5,
        "diameter_mm": 30.6,
        "edge": "Reeded",
        "aliases": ["Barber", "Liberty Head Half"],
    },
    {
        "code": "WLHD",
        "name": "Walking Liberty Half Dollar",
        "start_year": 1916,
        "end_year": 1947,
        "seed_year": 1916,
        "seed_mint": "P",
        "designer": "Adolph A. Weinman",
        "obverse": "Full-length Liberty walking toward sunrise, draped in American flag, holding olive branches, 'LIBERTY' above, 'IN GOD WE TRUST' at right, date at base",
        "reverse": "Bald eagle perched on rock with wings raised, mountain pine branch emerging from rock, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'HALF DOLLAR'",
        "composition": {"silver": 90, "copper": 10},
        "weight_grams": 12.5,
        "diameter_mm": 30.6,
        "edge": "Reeded",
        "aliases": ["Walking Liberty", "Walker"],
    },
    {
        "code": "FRNH",
        "name": "Franklin Half Dollar",
        "start_year": 1948,
        "end_year": 1963,
        "seed_year": 1948,
        "seed_mint": "P",
        "designer": "John R. Sinnock",
        "obverse": "Profile bust of Benjamin Franklin facing right, 'LIBERTY' above, 'IN GOD WE TRUST' at right, date below",
        "reverse": "Liberty Bell with small eagle to right, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'HALF DOLLAR'",
        "composition": {"silver": 90, "copper": 10},
        "weight_grams": 12.5,
        "diameter_mm": 30.6,
        "edge": "Reeded",
        "aliases": ["Franklin", "Ben Franklin Half"],
    },
    {
        "code": "KENH",
        "name": "Kennedy Half Dollar",
        "start_year": 1964,
        "end_year": None,  # Ongoing series
        "seed_year": 1964,
        "seed_mint": "P",
        "designer": "Gilroy Roberts (obverse), Frank Gasparro (reverse)",
        "obverse": "Profile bust of President John F. Kennedy facing left, 'LIBERTY' above, 'IN GOD WE TRUST' below, date at base",
        "reverse": "Heraldic eagle based on Presidential Seal, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'HALF DOLLAR'",
        "composition": {"silver": 90, "copper": 10},  # 1964 composition
        "weight_grams": 12.5,
        "diameter_mm": 30.6,
        "edge": "Reeded",
        "aliases": ["Kennedy", "JFK Half"],
        "notes": "Composition changed over time: 90% silver (1964), 40% silver (1965-1970), copper-nickel clad (1971-present)",
    },
]


def add_half_dollars(conn):
    """Add half dollar series to database"""
    cursor = conn.cursor()

    for series in HALF_DOLLAR_SERIES:
        code = series["code"]
        name = series["name"]
        print(f"Adding {name} ({code})...")

        # Add to series_registry
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases
            ) VALUES (?, ?, ?, 'US', 'Half Dollars', ?, ?, ?, ?, 'coin', ?)
        """, (
            f"{name}__Half_Dollars",
            name,
            code,
            series["start_year"],
            series["end_year"],
            f"Classic US silver half dollar, {series['start_year']}-{series['end_year'] or 'present'}",
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
            ) VALUES (?, ?, ?, 'Half Dollars', ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', 'Red Book')
        """, (
            coin_id,
            str(series["seed_year"]),
            series["seed_mint"],
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
    print(f"\n✅ Added {len(HALF_DOLLAR_SERIES)} half dollar series")


def main():
    db_path = Path(__file__).parent.parent / "database" / "coins.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return 1

    conn = sqlite3.connect(db_path)
    try:
        add_half_dollars(conn)
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    exit(main())
