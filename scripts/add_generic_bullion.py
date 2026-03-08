#!/usr/bin/env python3
"""
Add generic bullion taxonomy entries for dealer price aggregation.

Adds ~18 new entries: generic bars/rounds, random-year Maple Leafs,
and junk silver bags.

Usage:
    uv run python scripts/add_generic_bullion.py
    uv run python scripts/add_generic_bullion.py --dry-run

Issue: #149
"""

import argparse
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

TARGET_DB = Path(__file__).parent.parent / "database" / "coins.db"

# New entries to add
# (coin_id, year, mint, denomination, series, variety, composition, weight_grams, notes)
NEW_ENTRIES = [
    # Generic silver bar - 1kg
    ("XX-GS1K-XXXX-X", "XXXX", "X", "No Face Value", "Generic Silver Bar (1 kg)", None,
     ".999 Ag", 1000.0, "Random brand 1 kg silver bar for dealer price aggregation"),

    # Generic gold bars - 10oz, 1g, 5g, 10g
    ("XX-GB10-XXXX-X", "XXXX", "X", "No Face Value", "Generic Gold Bar (10 oz)", None,
     ".999 Au", 311.035, "Random brand 10 oz gold bar for dealer price aggregation"),
    ("XX-GG1G-XXXX-X", "XXXX", "X", "No Face Value", "Generic Gold Bar (1 g)", None,
     ".999 Au", 1.0, "Random brand 1 gram gold bar for dealer price aggregation"),
    ("XX-GG5G-XXXX-X", "XXXX", "X", "No Face Value", "Generic Gold Bar (5 g)", None,
     ".999 Au", 5.0, "Random brand 5 gram gold bar for dealer price aggregation"),
    ("XX-G10G-XXXX-X", "XXXX", "X", "No Face Value", "Generic Gold Bar (10 g)", None,
     ".999 Au", 10.0, "Random brand 10 gram gold bar for dealer price aggregation"),

    # Random year Canadian Gold Maple Leaf (1oz, 1/2oz, 1/4oz, 1/10oz)
    ("CA-GMPL-XXXX-X", "XXXX", "X", "$50 CAD", "Gold Maple Leaf", None,
     ".9999 Au", 31.1035, "Random year Gold Maple Leaf 1 oz for dealer price aggregation"),
    ("CA-GMPL-XXXX-X-12OZ", "XXXX", "X", "$20 CAD", "Gold Maple Leaf", "1/2 oz",
     ".9999 Au", 15.5517, "Random year Gold Maple Leaf 1/2 oz for dealer price aggregation"),
    ("CA-GMPL-XXXX-X-14OZ", "XXXX", "X", "$10 CAD", "Gold Maple Leaf", "1/4 oz",
     ".9999 Au", 7.7759, "Random year Gold Maple Leaf 1/4 oz for dealer price aggregation"),
    ("CA-GMPL-XXXX-X-110OZ", "XXXX", "X", "$5 CAD", "Gold Maple Leaf", "1/10 oz",
     ".9999 Au", 3.1103, "Random year Gold Maple Leaf 1/10 oz for dealer price aggregation"),

    # Random year Canadian Silver Maple Leaf (1oz)
    ("CA-SMPL-XXXX-X", "XXXX", "X", "$5 CAD", "Silver Maple Leaf", None,
     ".9999 Ag", 31.1035, "Random year Silver Maple Leaf 1 oz for dealer price aggregation"),

    # Junk silver 90% bags
    ("US-JK90-XXXX-X-1FV", "XXXX", "X", "$1 Face Value", "90% Junk Silver", "$1 face",
     "90% Ag, 10% Cu", 25.0, "90% silver US coins, $1 face value bag for dealer price aggregation"),
    ("US-JK90-XXXX-X-100FV", "XXXX", "X", "$100 Face Value", "90% Junk Silver", "$100 face",
     "90% Ag, 10% Cu", 2500.0, "90% silver US coins, $100 face value bag for dealer price aggregation"),
    ("US-JK90-XXXX-X-500FV", "XXXX", "X", "$500 Face Value", "90% Junk Silver", "$500 face",
     "90% Ag, 10% Cu", 12500.0, "90% silver US coins, $500 face value bag for dealer price aggregation"),
    ("US-JK90-XXXX-X-1KFV", "XXXX", "X", "$1000 Face Value", "90% Junk Silver", "$1000 face",
     "90% Ag, 10% Cu", 25000.0, "90% silver US coins, $1000 face value bag for dealer price aggregation"),
]


def main():
    parser = argparse.ArgumentParser(description="Add generic bullion entries")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be added without modifying DB")
    args = parser.parse_args()

    if not TARGET_DB.exists():
        print(f"ERROR: Database not found at {TARGET_DB}")
        return

    # Backup
    if not args.dry_run:
        backup_path = TARGET_DB.parent / f"coins_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(TARGET_DB, backup_path)
        print(f"Backed up database to {backup_path}")

    conn = sqlite3.connect(TARGET_DB)
    cursor = conn.cursor()

    added = 0
    skipped = 0

    for entry in NEW_ENTRIES:
        coin_id = entry[0]
        cursor.execute("SELECT 1 FROM coins WHERE coin_id = ?", (coin_id,))
        if cursor.fetchone():
            print(f"  SKIP (exists): {coin_id}")
            skipped += 1
            continue

        if args.dry_run:
            print(f"  WOULD ADD: {coin_id} — {entry[4]}")
            added += 1
            continue

        cursor.execute("""
            INSERT INTO coins (coin_id, year, mint, denomination, series, variety,
                               composition, weight_grams, notes, rarity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'common')
        """, entry)
        print(f"  ADDED: {coin_id} — {entry[4]}")
        added += 1

    if not args.dry_run:
        conn.commit()

    conn.close()

    action = "Would add" if args.dry_run else "Added"
    print(f"\n{action} {added} entries, skipped {skipped} existing")


if __name__ == "__main__":
    main()
