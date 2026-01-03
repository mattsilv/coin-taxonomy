#!/usr/bin/env python3
"""
Add Fractional Mexican Libertad Type Codes - Issue #82

Adds separate type codes for fractional Mexican Libertad denominations,
following the American Gold Eagle pattern where each size gets its own 4-letter type code.

New Type Codes:
  Silver: MLSH (1/2oz), MLSQ (1/4oz), MLSD (1/10oz), MLST (1/20oz)
  Gold:   MLGH (1/2oz), MLGQ (1/4oz), MLGD (1/10oz), MLGT (1/20oz)

Uses XXXX year pattern for random-year bullion entries (AI classification).
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import shutil


# Database path
DB_PATH = Path(__file__).parent.parent / "database" / "coins.db"

# Fractional Libertad specifications
# Silver Libertads (.999 fine silver)
SILVER_FRACTIONALS = {
    "MLSH": {
        "denomination": "Mexican Libertad Silver 1/2 oz",
        "series": "Mexican Libertad Silver 1/2 oz",
        "weight_grams": 15.552,
        "diameter_mm": 33.0,
        "weight_oz": 0.5,
    },
    "MLSQ": {
        "denomination": "Mexican Libertad Silver 1/4 oz",
        "series": "Mexican Libertad Silver 1/4 oz",
        "weight_grams": 7.776,
        "diameter_mm": 27.0,
        "weight_oz": 0.25,
    },
    "MLSD": {
        "denomination": "Mexican Libertad Silver 1/10 oz",
        "series": "Mexican Libertad Silver 1/10 oz",
        "weight_grams": 3.110,
        "diameter_mm": 20.0,
        "weight_oz": 0.1,
    },
    "MLST": {
        "denomination": "Mexican Libertad Silver 1/20 oz",
        "series": "Mexican Libertad Silver 1/20 oz",
        "weight_grams": 1.555,
        "diameter_mm": 16.0,
        "weight_oz": 0.05,
    },
}

# Gold Libertads (.999 fine gold from 1991+)
GOLD_FRACTIONALS = {
    "MLGH": {
        "denomination": "Mexican Libertad Gold 1/2 oz",
        "series": "Mexican Libertad Gold 1/2 oz",
        "weight_grams": 15.552,
        "diameter_mm": 29.0,
        "weight_oz": 0.5,
    },
    "MLGQ": {
        "denomination": "Mexican Libertad Gold 1/4 oz",
        "series": "Mexican Libertad Gold 1/4 oz",
        "weight_grams": 7.776,
        "diameter_mm": 23.0,
        "weight_oz": 0.25,
    },
    "MLGD": {
        "denomination": "Mexican Libertad Gold 1/10 oz",
        "series": "Mexican Libertad Gold 1/10 oz",
        "weight_grams": 3.110,
        "diameter_mm": 16.0,
        "weight_oz": 0.1,
    },
    "MLGT": {
        "denomination": "Mexican Libertad Gold 1/20 oz",
        "series": "Mexican Libertad Gold 1/20 oz",
        "weight_grams": 1.555,
        "diameter_mm": 13.0,
        "weight_oz": 0.05,
    },
}


def backup_database():
    """Create backup before migration."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)

    backup = backup_dir / f'coins_backup_fractional_libertads_{timestamp}.db'
    shutil.copy(DB_PATH, backup)
    print(f"Database backed up to {backup}")
    return backup


def add_fractional_libertads(conn: sqlite3.Connection):
    """Add fractional Libertad coins to the database."""
    cursor = conn.cursor()
    coins_added = 0

    # Add Silver fractionals
    for type_code, specs in SILVER_FRACTIONALS.items():
        coin_id = f"MX-{type_code}-XXXX-MO"

        # Check if already exists
        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
        if cursor.fetchone():
            print(f"  Skipping {coin_id} - already exists")
            continue

        cursor.execute("""
            INSERT INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge,
                obverse_description, reverse_description,
                notes, rarity, source_citation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin_id,
            "XXXX",
            "MO",
            specs["denomination"],
            specs["series"],
            ".999 Ag",
            specs["weight_grams"],
            specs["diameter_mm"],
            "Reeded",
            "Winged Victory (Angel of Independence)",
            "Mexican coat of arms with eagle on cactus",
            f"Random year bullion ({specs['weight_oz']} oz silver)",
            "common",
            "Casa de Moneda de Mexico; findbullionprices.com"
        ))
        coins_added += 1
        print(f"  Added {coin_id}")

    # Add Gold fractionals
    for type_code, specs in GOLD_FRACTIONALS.items():
        coin_id = f"MX-{type_code}-XXXX-MO"

        # Check if already exists
        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
        if cursor.fetchone():
            print(f"  Skipping {coin_id} - already exists")
            continue

        cursor.execute("""
            INSERT INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge,
                obverse_description, reverse_description,
                notes, rarity, source_citation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin_id,
            "XXXX",
            "MO",
            specs["denomination"],
            specs["series"],
            ".999 Au",
            specs["weight_grams"],
            specs["diameter_mm"],
            "Reeded",
            "Winged Victory (Angel of Independence)",
            "Mexican coat of arms with eagle on cactus",
            f"Random year bullion ({specs['weight_oz']} oz gold)",
            "common",
            "Casa de Moneda de Mexico; findbullionprices.com"
        ))
        coins_added += 1
        print(f"  Added {coin_id}")

    conn.commit()
    return coins_added


def main():
    print("=" * 60)
    print("Adding Fractional Mexican Libertad Type Codes - Issue #82")
    print("=" * 60)

    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        return 1

    # Backup first
    backup_database()

    conn = sqlite3.connect(DB_PATH)

    try:
        print("\nAdding Silver Libertad fractional sizes...")
        print("  Type codes: MLSH (1/2oz), MLSQ (1/4oz), MLSD (1/10oz), MLST (1/20oz)")

        print("\nAdding Gold Libertad fractional sizes...")
        print("  Type codes: MLGH (1/2oz), MLGQ (1/4oz), MLGD (1/10oz), MLGT (1/20oz)")

        print("\nProcessing...")
        total = add_fractional_libertads(conn)

        print(f"\nTotal coins added: {total}")

        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT coin_id, denomination, series
            FROM coins
            WHERE coin_id LIKE 'MX-MLS%' OR coin_id LIKE 'MX-MLG%'
            ORDER BY coin_id
        """)

        print("\nAll Mexican Libertad entries in database:")
        print("-" * 60)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}")

    except Exception as e:
        print(f"ERROR: {e}")
        conn.rollback()
        return 1
    finally:
        conn.close()

    print("\n" + "=" * 60)
    print("Migration complete! Run 'uv run python scripts/export_from_database.py'")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit(main())
