#!/usr/bin/env python3
"""
Fix malformed coin IDs in database.

Issues fixed:
- Lowercase letters in variety suffixes (e.g., '110oz' -> '110OZ')
- All suffixes must be uppercase alphanumeric only

Usage:
    uv run python scripts/fix_malformed_bullion_ids.py --dry-run
    uv run python scripts/fix_malformed_bullion_ids.py
"""

import argparse
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("database/coins.db")


def find_malformed_ids(conn):
    """Find all coin_ids with lowercase letters."""
    cursor = conn.cursor()
    cursor.execute("SELECT coin_id FROM coins")
    malformed = []
    for (coin_id,) in cursor.fetchall():
        if any(c.islower() for c in coin_id):
            malformed.append(coin_id)
    return malformed


def fix_coin_id(coin_id):
    """Convert coin_id to fully uppercase."""
    return coin_id.upper()


def main():
    parser = argparse.ArgumentParser(description="Fix malformed coin IDs")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying database")
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    malformed = find_malformed_ids(conn)

    if not malformed:
        print("No malformed IDs found.")
        conn.close()
        return

    print(f"Found {len(malformed)} malformed coin IDs")

    # Group by issue type
    fixes = []
    for old_id in malformed:
        new_id = fix_coin_id(old_id)
        if old_id != new_id:
            fixes.append((old_id, new_id))

    print(f"\nFixes to apply: {len(fixes)}")
    for old_id, new_id in fixes[:10]:
        print(f"  {old_id} -> {new_id}")
    if len(fixes) > 10:
        print(f"  ... and {len(fixes) - 10} more")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        conn.close()
        return

    # Check for conflicts (new_id already exists)
    cursor = conn.cursor()
    conflicts = []
    for old_id, new_id in fixes:
        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (new_id,))
        if cursor.fetchone():
            conflicts.append((old_id, new_id))

    if conflicts:
        print(f"\nWARNING: {len(conflicts)} conflicts (target ID already exists):")
        for old_id, new_id in conflicts[:5]:
            print(f"  {old_id} -> {new_id} (EXISTS)")
        print("Skipping conflicting IDs.")
        fixes = [(o, n) for o, n in fixes if (o, n) not in conflicts]

    # Apply fixes
    cursor = conn.cursor()
    success = 0
    for old_id, new_id in fixes:
        try:
            cursor.execute("UPDATE coins SET coin_id = ? WHERE coin_id = ?", (new_id, old_id))
            success += 1
        except sqlite3.IntegrityError as e:
            print(f"  SKIP {old_id}: {e}")

    conn.commit()
    print(f"\nFixed {success}/{len(fixes)} coin IDs")

    # Verify no lowercase remains
    remaining = find_malformed_ids(conn)
    if remaining:
        print(f"WARNING: {len(remaining)} IDs still have lowercase letters")
        for r in remaining[:5]:
            print(f"  {r}")
    else:
        print("All coin IDs are now uppercase.")

    conn.close()


if __name__ == "__main__":
    main()
