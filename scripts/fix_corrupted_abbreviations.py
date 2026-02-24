#!/usr/bin/env python3
"""
Fix corrupted series_abbreviation values in series_registry and
update affected issue_ids in the issues table.

Fixes Issue #129: https://github.com/mattsilv/coin-taxonomy/issues/129

Corruption categories:
1. Paren artifacts: ASE(, AGE( → merge into correct entries
2. Dollar signs/spaces: $10, $5 , 10 , 25 , 5 C, 5 C1, 50
3. Full names as abbreviations: american_gold_buffalo_1oz, american_silver_eagle_1oz
4. Gold Maple Leaf: rename GOL/GOL1-4 to proper codes, delete dead GMLO
5. Dead entries with 0 issues: E100, etc.
"""

import shutil
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("database/coins.db")
BACKUP_DIR = Path("backups")


def create_backup():
    """Create a timestamped backup of the database."""
    BACKUP_DIR.mkdir(exist_ok=True)
    import datetime
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"coins_backup_{ts}.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


# Mapping: old_abbreviation -> new_abbreviation
# For simple renames (no merge needed)
RENAME_MAP = {
    # Canadian coins with special chars
    "$10": "TGLD",   # $10 Gold (CA, 1912-1914)
    "$5 ": "FGLD",   # $5 Gold (CA, 1912-1914)
    "10 ": "DIMS",   # 10 Cents Steel (CA, 2000-2024)
    "25 ": "QRTS",   # 25 Cents Steel (CA, 2000-2024)
    "5 C": "NICK",   # 5 Cents Nickel (CA, 1968-1999)
    "5 C1": "NICS",  # 5 Cents Steel (CA, 2000-2024)
    "50 ": "HLFS",   # 50 Cents Steel (CA, 2000-2020)
    # Gold Maple Leaf renames
    "GOL": "BGML",   # Big Maple Leaf (100kg)
    "GOL1": "GMLT",  # Gold Maple Leaf 1/10 oz
    "GOL2": "GMLH",  # Gold Maple Leaf 1/2 oz
    "GOL3": "GMLS",  # Gold Maple Leaf 1/20 oz (smallest)
    "GOL4": "GMLQ",  # Gold Maple Leaf 1/4 oz
}

# Merges: corrupted entry -> target series_id (already exists with correct abbreviation)
# Format: old_abbreviation -> (target_series_id, target_abbreviation)
MERGE_MAP = {
    "AGE(": ("american_gold_eagle_1oz", "AGEO"),
    "ASE(": ("american_silver_eagle_1oz", "ASEA"),
    "AME": ("american_gold_buffalo_1oz", "AGBF"),
}

# Full-name abbreviation entries that need their abbreviation fixed
# (these are the target series for merges, but their abbreviation is wrong)
FIX_FULL_NAME_ABBREVS = {
    "American Silver Eagle (1 oz)": "ASEA",  # series_id: american_silver_eagle_1oz
    "American Gold Buffalo (1 oz)": "AGBF",  # series_id: american_gold_buffalo_1oz
}

# Dead entries to delete (0 issues referencing them)
DELETE_DEAD = [
    "GMLO",  # Gold Maple Leaf 1 oz (dead duplicate)
    "E100",  # Engelhard Bar 100 oz (0 issues)
]


def fix_abbreviations():
    """Run the full migration."""
    backup_path = create_backup()
    print(f"\nStarting migration...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Disable FK checks during migration
    cursor.execute("PRAGMA foreign_keys = OFF")

    try:
        # Count FK violations before
        cursor.execute("SELECT COUNT(*) FROM pragma_foreign_key_check()")
        fk_before = cursor.fetchone()[0]
        print(f"FK violations before: {fk_before}")

        # Step 1: Fix full-name abbreviations on target series
        # (must happen before merges so the target has correct abbreviation)
        print("\n--- Step 1: Fix full-name abbreviations ---")
        for old_abbrev, new_abbrev in FIX_FULL_NAME_ABBREVS.items():
            cursor.execute(
                "SELECT series_id FROM series_registry WHERE series_abbreviation = ?",
                (old_abbrev,)
            )
            row = cursor.fetchone()
            if row:
                series_id = row[0]
                cursor.execute(
                    "UPDATE series_registry SET series_abbreviation = ? WHERE series_abbreviation = ?",
                    (new_abbrev, old_abbrev)
                )
                print(f"  Fixed: '{old_abbrev}' -> '{new_abbrev}' (series_id: {series_id})")
            else:
                print(f"  Skip: '{old_abbrev}' not found")

        # Step 2: Merge corrupted entries into correct target series
        print("\n--- Step 2: Merge corrupted entries ---")
        for old_abbrev, (target_series_id, target_abbrev) in MERGE_MAP.items():
            cursor.execute(
                "SELECT series_id FROM series_registry WHERE series_abbreviation = ?",
                (old_abbrev,)
            )
            row = cursor.fetchone()
            if not row:
                print(f"  Skip: '{old_abbrev}' not found")
                continue

            old_series_id = row[0]

            # Count affected issues
            cursor.execute(
                "SELECT COUNT(*) FROM issues WHERE series_id = ?",
                (old_series_id,)
            )
            issue_count = cursor.fetchone()[0]

            # Update issue series_id FK to point to target
            cursor.execute(
                "UPDATE issues SET series_id = ? WHERE series_id = ?",
                (target_series_id, old_series_id)
            )

            # Rename issue_ids: replace old abbreviation with target abbreviation
            cursor.execute(
                "SELECT issue_id FROM issues WHERE series_id = ? AND issue_id LIKE ?",
                (target_series_id, f"%-{old_abbrev}-%")
            )
            issues_to_rename = cursor.fetchall()
            for (issue_id,) in issues_to_rename:
                new_issue_id = issue_id.replace(f"-{old_abbrev}-", f"-{target_abbrev}-", 1)
                cursor.execute(
                    "UPDATE issues SET issue_id = ? WHERE issue_id = ?",
                    (new_issue_id, issue_id)
                )
                print(f"  Renamed issue: {issue_id} -> {new_issue_id}")

            # Delete the old series_registry entry
            cursor.execute(
                "DELETE FROM series_registry WHERE series_id = ?",
                (old_series_id,)
            )
            print(f"  Merged: '{old_abbrev}' ({old_series_id}) -> '{target_abbrev}' ({target_series_id}), {issue_count} issues moved")

        # Step 3: Simple renames
        print("\n--- Step 3: Rename corrupted abbreviations ---")
        for old_abbrev, new_abbrev in RENAME_MAP.items():
            # Check for collision
            cursor.execute(
                "SELECT series_id FROM series_registry WHERE series_abbreviation = ?",
                (new_abbrev,)
            )
            if cursor.fetchone():
                print(f"  ERROR: '{new_abbrev}' already exists! Skipping '{old_abbrev}'")
                continue

            cursor.execute(
                "SELECT series_id FROM series_registry WHERE series_abbreviation = ?",
                (old_abbrev,)
            )
            row = cursor.fetchone()
            if not row:
                print(f"  Skip: '{old_abbrev}' not found")
                continue

            series_id = row[0]

            # Rename abbreviation
            cursor.execute(
                "UPDATE series_registry SET series_abbreviation = ? WHERE series_abbreviation = ?",
                (new_abbrev, old_abbrev)
            )

            # Rename issue_ids
            cursor.execute(
                "SELECT issue_id FROM issues WHERE series_id = ?",
                (series_id,)
            )
            renamed = 0
            for (issue_id,) in cursor.fetchall():
                # Replace the abbreviation part in the issue_id
                # issue_id format: COUNTRY-TYPE-YEAR-MINT
                new_issue_id = issue_id.replace(f"-{old_abbrev}-", f"-{new_abbrev}-", 1)
                if new_issue_id != issue_id:
                    cursor.execute(
                        "UPDATE issues SET issue_id = ? WHERE issue_id = ?",
                        (new_issue_id, issue_id)
                    )
                    renamed += 1

            print(f"  Renamed: '{old_abbrev}' -> '{new_abbrev}' ({renamed} issue_ids updated)")

        # Step 4: Delete dead entries
        print("\n--- Step 4: Delete dead entries ---")
        for abbrev in DELETE_DEAD:
            cursor.execute(
                "SELECT series_id, (SELECT COUNT(*) FROM issues WHERE issues.series_id = series_registry.series_id) as cnt FROM series_registry WHERE series_abbreviation = ?",
                (abbrev,)
            )
            row = cursor.fetchone()
            if not row:
                print(f"  Skip: '{abbrev}' not found")
                continue

            series_id, issue_count = row
            if issue_count > 0:
                print(f"  SKIP: '{abbrev}' has {issue_count} issues, not deleting!")
                continue

            cursor.execute(
                "DELETE FROM series_registry WHERE series_abbreviation = ?",
                (abbrev,)
            )
            print(f"  Deleted: '{abbrev}' ({series_id})")

        # Commit all changes
        conn.commit()
        print("\n--- Migration committed ---")

        # Verify results
        print("\n--- Verification ---")

        # Check no corrupted abbreviations remain
        cursor.execute("""
            SELECT series_abbreviation FROM series_registry
            WHERE series_abbreviation NOT GLOB '[A-Z0-9][A-Z0-9]*'
               OR series_abbreviation GLOB '*[^A-Z0-9]*'
               OR length(series_abbreviation) > 4
               OR length(series_abbreviation) < 2
        """)
        bad = cursor.fetchall()
        if bad:
            print(f"  WARNING: {len(bad)} corrupted abbreviations remain: {[r[0] for r in bad]}")
        else:
            print("  All abbreviations are valid (2-4 uppercase alphanumeric)")

        # Check FK violations after
        cursor.execute("SELECT COUNT(*) FROM pragma_foreign_key_check()")
        fk_after = cursor.fetchone()[0]
        print(f"  FK violations: {fk_before} -> {fk_after} (delta: {fk_after - fk_before:+d})")

        # Count total series
        cursor.execute("SELECT COUNT(*) FROM series_registry")
        total = cursor.fetchone()[0]
        print(f"  Total series entries: {total}")

        # Check for issue_ids with bad format
        cursor.execute("""
            SELECT COUNT(*) FROM issues
            WHERE issue_id GLOB '*[^A-Z0-9-]*'
        """)
        bad_ids = cursor.fetchone()[0]
        print(f"  Issue IDs with special chars: {bad_ids}")

    except Exception as e:
        conn.rollback()
        print(f"\nERROR: {e}")
        print(f"Transaction rolled back. Restore from backup: {backup_path}")
        conn.close()
        sys.exit(1)

    conn.close()
    print("\nMigration complete. Run export to regenerate JSON:")
    print("  uv run python scripts/export_from_database.py")


if __name__ == "__main__":
    fix_abbreviations()
