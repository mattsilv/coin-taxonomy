#!/usr/bin/env python3
"""
Add missing US coin series with correct year ranges.
Issue #75

Adds:
- EISE: Eisenhower Dollar (1971-1978)
- SLDI: Seated Liberty Dime (1837-1891)
- LWCT: Lincoln Wheat Cent (1909-1958)
- SACA: Sacagawea Dollar (2000-present)
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Missing US series definitions
MISSING_SERIES = [
    {
        "code": "EISE",
        "name": "Eisenhower Dollar",
        "denomination": "Dollars",
        "start_year": 1971,
        "end_year": 1978,
        "seed_year": 1971,
        "seed_mint": "P",
        "designer": "Frank Gasparro",
        "obverse": "Profile portrait of President Dwight D. Eisenhower facing left, 'LIBERTY' above, 'IN GOD WE TRUST' below, date at base",
        "reverse": "Apollo 11 mission insignia - bald eagle landing on moon with Earth in background, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'ONE DOLLAR'",
        "composition": {"copper": 75, "nickel": 25},  # Clad version
        "weight_grams": 22.68,
        "diameter_mm": 38.1,
        "edge": "Reeded",
        "aliases": ["Eisenhower", "Ike Dollar", "Ike"],
        "notes": "Available in clad and 40% silver versions. The reverse features the Apollo 11 moon landing mission insignia.",
    },
    {
        "code": "SLDI",
        "name": "Seated Liberty Dime",
        "denomination": "Dimes",
        "start_year": 1837,
        "end_year": 1891,
        "seed_year": 1837,
        "seed_mint": "P",
        "designer": "Christian Gobrecht",
        "obverse": "Liberty seated on rock, holding shield with 'LIBERTY' and pole with liberty cap, 13 stars around, date below",
        "reverse": "Wreath encircling 'ONE DIME', 'UNITED STATES OF AMERICA' around",
        "composition": {"silver": 90, "copper": 10},
        "weight_grams": 2.67,
        "diameter_mm": 17.9,
        "edge": "Reeded",
        "aliases": ["Seated Liberty", "Seated Dime", "Liberty Seated Dime"],
        "notes": "Multiple design variations: No Stars (1837-1838), Stars (1838-1860), Legend (1860-1891).",
    },
    {
        "code": "LWCT",
        "name": "Lincoln Wheat Cent",
        "denomination": "Cents",
        "start_year": 1909,
        "end_year": 1958,
        "seed_year": 1909,
        "seed_mint": "P",
        "designer": "Victor David Brenner",
        "obverse": "Profile bust of President Abraham Lincoln facing right, 'IN GOD WE TRUST' above, 'LIBERTY' at left, date at right",
        "reverse": "Two wheat stalks framing 'ONE CENT' and 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM' at top",
        "composition": {"copper": 95, "tin_zinc": 5},  # Bronze version
        "weight_grams": 3.11,
        "diameter_mm": 19.0,
        "edge": "Plain",
        "aliases": ["Lincoln Wheat", "Wheat Cent", "Wheaties", "Wheat Penny", "Lincoln Wheat Penny"],
        "notes": "1943 cents were struck in zinc-coated steel due to WWII copper shortage. VDB initials on 1909 reverse are highly collectible.",
    },
    {
        "code": "SACA",
        "name": "Sacagawea Dollar",
        "denomination": "Dollars",
        "start_year": 2000,
        "end_year": None,  # Ongoing (though design changed to Native American $1 in 2009)
        "seed_year": 2000,
        "seed_mint": "P",
        "designer": "Glenna Goodacre",
        "obverse": "Portrait of Sacagawea carrying infant son Jean Baptiste, 'LIBERTY' above, 'IN GOD WE TRUST' at left, date below",
        "reverse": "Soaring eagle surrounded by 17 stars, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'ONE DOLLAR'",
        "composition": {"copper": 88.5, "zinc": 6, "manganese": 3.5, "nickel": 2},  # Manganese brass
        "weight_grams": 8.1,
        "diameter_mm": 26.5,
        "edge": "Plain with lettering",
        "aliases": ["Sacagawea", "Golden Dollar", "Sac Dollar"],
        "notes": "Distinctive golden color from manganese brass composition. Continued as Native American $1 series from 2009 with changing reverses.",
    },
]


def add_missing_series(conn):
    """Add missing US series to database"""
    cursor = conn.cursor()

    for series in MISSING_SERIES:
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
            f"{name}__{series['denomination']}",
            name,
            code,
            series["denomination"],
            series["start_year"],
            series["end_year"],
            series.get("notes", f"US {series['denomination']} coin series"),
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
    print(f"\n✅ Added {len(MISSING_SERIES)} US series")


def main():
    db_path = Path(__file__).parent.parent / "database" / "coins.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return 1

    conn = sqlite3.connect(db_path)
    try:
        add_missing_series(conn)
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    exit(main())
