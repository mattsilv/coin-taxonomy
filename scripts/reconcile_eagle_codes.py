#!/usr/bin/env python3
"""
Reconcile legacy American Gold Eagle series codes to match the
weight suffix convention.

Fixes Issue #133: https://github.com/mattsilv/coin-taxonomy/issues/133

Renames (in order to avoid UNIQUE constraint conflicts):
  1. AGET -> AGEQ  (1/4 oz, frees the AGET slot)
  2. AGES -> AGET  (1/10 oz, takes the freed slot)
  3. AGEF -> AGEH  (1/2 oz, independent)

Also cleans up corrupted duplicate entries from Issue #129:
  - AGE( (duplicate of AGEO)
  - AME1 (duplicate of AGES/AGET after rename)
  - AME2 (duplicate of AGEF/AGEH after rename)
  - AME3 (duplicate of AGET/AGEQ after rename)
"""

import argparse
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path("database/coins.db")
BACKUP_DIR = Path("backups")

# Ordered renames: AGET->AGEQ must happen first to free the slot
# Each tuple: (old_abbrev, new_abbrev, expected_series_id)
RENAMES = [
    ("AGET", "AGEQ", "american_gold_eagle_quarter_oz"),   # 1/4 oz: frees AGET slot
    ("AGES", "AGET", "american_gold_eagle_tenth_oz"),      # 1/10 oz: takes freed AGET slot
    ("AGEF", "AGEH", "american_gold_eagle_half_oz"),       # 1/2 oz: independent
]

# Corrupted entries to delete (duplicates from Issue #129)
CORRUPTED_ENTRIES = ["AGE(", "AME1", "AME2", "AME3"]


def create_backup():
    """Create a timestamped backup of the database."""
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"coins_backup_{ts}.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def preflight_checks(cursor):
    """Verify expected database state before migration. Returns set of renames to skip."""
    print("\n--- Pre-flight checks ---")
    errors = []
    skip_renames = set()

    # Check source codes exist (if target already exists with correct series_id, skip rename)
    for old, new, expected_sid in RENAMES:
        cursor.execute(
            "SELECT series_id FROM series_registry WHERE series_abbreviation = ?",
            (old,),
        )
        source_row = cursor.fetchone()

        cursor.execute(
            "SELECT series_id FROM series_registry WHERE series_abbreviation = ?",
            (new,),
        )
        target_row = cursor.fetchone()

        if target_row and target_row[0] == expected_sid:
            # Target has the correct series_id — rename already completed
            print(f"  SKIP: {old} -> {new} already done ({expected_sid})")
            skip_renames.add((old, new, expected_sid))
        elif not source_row and not target_row:
            errors.append(f"Source '{old}' missing and target '{new}' doesn't exist either")
        elif source_row and target_row and target_row[0] != expected_sid:
            errors.append(f"Target code '{new}' exists with unexpected series_id: {target_row[0]}")
        elif source_row and source_row[0] == expected_sid:
            # Source exists with correct series_id — rename needed
            pass
        elif not source_row:
            errors.append(f"Source '{old}' not found")

    # Check no coin_inventory entries for affected coin_ids
    for old, new, sid in RENAMES:
        if (old, new, sid) in skip_renames:
            continue
        cursor.execute(
            "SELECT COUNT(*) FROM coin_inventory WHERE coin_id LIKE ?",
            (f"%-{old}-%",),
        )
        count = cursor.fetchone()[0]
        if count > 0:
            errors.append(
                f"coin_inventory has {count} entries for '{old}' — manual handling required"
            )

    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        return None

    print("  All pre-flight checks passed")
    return skip_renames
    return True


def run_migration(dry_run=False):
    """Run the Eagle code reconciliation migration."""
    if not dry_run:
        backup_path = create_backup()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF")

    skip_renames = preflight_checks(cursor)
    if skip_renames is None:
        print("\nPre-flight checks failed. Aborting.")
        conn.close()
        sys.exit(1)

    if dry_run:
        print("\n--- DRY RUN MODE (no changes will be made) ---")

    try:
        # Step 1: Rename Eagle codes (ordered to avoid UNIQUE conflicts)
        print("\n--- Step 1: Rename Eagle codes ---")
        for old_abbrev, new_abbrev, expected_sid in RENAMES:
            if (old_abbrev, new_abbrev, expected_sid) in skip_renames:
                print(f"  {old_abbrev} -> {new_abbrev}: already done, skipping")
                continue

            # Get series info
            cursor.execute(
                "SELECT series_id, series_name FROM series_registry WHERE series_abbreviation = ?",
                (old_abbrev,),
            )
            row = cursor.fetchone()
            series_id, series_name = row

            # Count affected rows
            cursor.execute(
                "SELECT COUNT(*) FROM coins WHERE coin_id LIKE ?",
                (f"%-{old_abbrev}-%",),
            )
            coin_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM issues WHERE issue_id LIKE ?",
                (f"%-{old_abbrev}-%",),
            )
            issue_count = cursor.fetchone()[0]

            print(
                f"  {old_abbrev} -> {new_abbrev} ({series_name}): {coin_count} coins, {issue_count} issues"
            )

            if dry_run:
                continue

            # Rename in series_registry
            cursor.execute(
                "UPDATE series_registry SET series_abbreviation = ? WHERE series_abbreviation = ?",
                (new_abbrev, old_abbrev),
            )

            # Rename coin_ids in coins table
            cursor.execute(
                "SELECT coin_id FROM coins WHERE coin_id LIKE ?",
                (f"%-{old_abbrev}-%",),
            )
            for (coin_id,) in cursor.fetchall():
                new_coin_id = coin_id.replace(f"-{old_abbrev}-", f"-{new_abbrev}-", 1)
                cursor.execute(
                    "UPDATE coins SET coin_id = ? WHERE coin_id = ?",
                    (new_coin_id, coin_id),
                )
                print(f"    coin: {coin_id} -> {new_coin_id}")

            # Rename issue_ids in issues table
            cursor.execute(
                "SELECT issue_id FROM issues WHERE issue_id LIKE ?",
                (f"%-{old_abbrev}-%",),
            )
            for (issue_id,) in cursor.fetchall():
                new_issue_id = issue_id.replace(
                    f"-{old_abbrev}-", f"-{new_abbrev}-", 1
                )
                cursor.execute(
                    "UPDATE issues SET issue_id = ? WHERE issue_id = ?",
                    (new_issue_id, issue_id),
                )
                print(f"    issue: {issue_id} -> {new_issue_id}")

            # Populate aliases field with old code
            cursor.execute(
                "UPDATE series_registry SET aliases = json_array(?) WHERE series_abbreviation = ?",
                (old_abbrev, new_abbrev),
            )
            print(f"    alias: {new_abbrev}.aliases = [\"{old_abbrev}\"]")

        # Step 2: Delete corrupted duplicate entries
        print("\n--- Step 2: Delete corrupted entries ---")
        for abbrev in CORRUPTED_ENTRIES:
            cursor.execute(
                "SELECT series_id FROM series_registry WHERE series_abbreviation = ?",
                (abbrev,),
            )
            row = cursor.fetchone()
            if not row:
                print(f"  Skip: '{abbrev}' not found")
                continue

            series_id = row[0]

            # Count issues
            cursor.execute(
                "SELECT COUNT(*) FROM issues WHERE series_id = ?",
                (series_id,),
            )
            issue_count = cursor.fetchone()[0]

            # Count coins
            cursor.execute(
                "SELECT COUNT(*) FROM coins WHERE coin_id LIKE ?",
                (f"%-{abbrev}-%",),
            )
            coin_count = cursor.fetchone()[0]

            print(
                f"  Delete '{abbrev}' ({series_id}): {coin_count} coins, {issue_count} issues"
            )

            if dry_run:
                continue

            # Delete issues first (FK dependency)
            cursor.execute(
                "DELETE FROM issues WHERE series_id = ?",
                (series_id,),
            )

            # Delete coins with this abbreviation
            cursor.execute(
                "DELETE FROM coins WHERE coin_id LIKE ?",
                (f"%-{abbrev}-%",),
            )

            # Delete series_registry entry
            cursor.execute(
                "DELETE FROM series_registry WHERE series_abbreviation = ?",
                (abbrev,),
            )

        if dry_run:
            print("\n--- Dry run complete. No changes made. ---")
            conn.close()
            return

        # Commit
        conn.commit()
        print("\n--- Migration committed ---")

        # Post-flight verification
        print("\n--- Post-flight verification ---")

        # Verify new codes exist
        for _, new_abbrev, _ in RENAMES:
            cursor.execute(
                "SELECT series_abbreviation, series_name, aliases FROM series_registry WHERE series_abbreviation = ?",
                (new_abbrev,),
            )
            row = cursor.fetchone()
            if row:
                print(f"  OK: {row[0]} = {row[1]} (aliases: {row[2]})")
            else:
                print(f"  FAIL: {new_abbrev} not found!")

        # Verify old codes are gone (skip codes that are also rename targets)
        new_codes = {new for _, new, _ in RENAMES}
        for old_abbrev, _, _ in RENAMES:
            if old_abbrev in new_codes:
                print(f"  OK: '{old_abbrev}' reused as target (circular rename)")
                continue
            cursor.execute(
                "SELECT COUNT(*) FROM series_registry WHERE series_abbreviation = ?",
                (old_abbrev,),
            )
            if cursor.fetchone()[0] > 0:
                print(f"  FAIL: Old code '{old_abbrev}' still exists!")
            else:
                print(f"  OK: '{old_abbrev}' removed")

        # Verify corrupted entries are gone
        for abbrev in CORRUPTED_ENTRIES:
            cursor.execute(
                "SELECT COUNT(*) FROM series_registry WHERE series_abbreviation = ?",
                (abbrev,),
            )
            if cursor.fetchone()[0] > 0:
                print(f"  FAIL: Corrupted '{abbrev}' still exists!")
            else:
                print(f"  OK: '{abbrev}' removed")

        # Verify coin_ids match new codes
        cursor.execute(
            "SELECT coin_id FROM coins WHERE coin_id LIKE 'US-AGE%' ORDER BY coin_id"
        )
        print(f"\n  Current Eagle coin_ids:")
        for (cid,) in cursor.fetchall():
            print(f"    {cid}")

        # Check FK violations
        cursor.execute("SELECT COUNT(*) FROM pragma_foreign_key_check()")
        fk_count = cursor.fetchone()[0]
        print(f"\n  FK violations: {fk_count}")

    except Exception as e:
        conn.rollback()
        print(f"\nERROR: {e}")
        if not dry_run:
            print(f"Transaction rolled back. Restore from backup: {backup_path}")
        conn.close()
        sys.exit(1)

    conn.close()
    print("\nMigration complete. Run export to regenerate JSON:")
    print("  uv run python scripts/export_from_database.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reconcile legacy Eagle series codes to match weight suffix convention"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without modifying the database",
    )
    args = parser.parse_args()
    run_migration(dry_run=args.dry_run)
