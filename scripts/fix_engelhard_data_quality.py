#!/usr/bin/env python3
"""
Fix Engelhard and vintage bar data quality issues.
Part of taxonomy bulletproofing audit.

Fixes:
1. series_registry: type='coin' → 'bullion' for all Engelhard entries
2. series_registry: Remove stale ENG/ENG1-10 entries that don't match coins table
3. coins table: denomination='Engelhard Bullion' → 'No Face Value'
4. Also fixes type for other private mint bars (JMTB, SCOT, SUNM, ENGP, ENG5, E100)
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path


DB_PATH = Path("database/coins.db")
BACKUP_DIR = Path("backups")


def main():
    # Backup
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"coins_backup_{ts}.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup: {backup_path}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # === Fix 1: Update Engelhard series_registry type to 'bullion' ===
    print("\n=== Fix 1: series_registry type='coin' → 'bullion' for Engelhard ===")
    cur.execute(
        "SELECT series_abbreviation, series_name, type FROM series_registry "
        "WHERE series_abbreviation LIKE 'EN%' AND type='coin'"
    )
    rows = cur.fetchall()
    for r in rows:
        print(f"  {r['series_abbreviation']}: {r['series_name']} → bullion")

    cur.execute(
        "UPDATE series_registry SET type='bullion' "
        "WHERE series_abbreviation LIKE 'EN%' AND type='coin'"
    )
    print(f"  Updated {cur.rowcount} entries")

    # === Fix 2: Remove stale series_registry entries ===
    # The coins table uses EN01-EN72 but registry has ENG/ENG1-10/EN10
    # which are orphaned. Remove them.
    print("\n=== Fix 2: Remove stale Engelhard series_registry entries ===")
    stale_codes = []
    cur.execute(
        "SELECT series_abbreviation FROM series_registry "
        "WHERE series_abbreviation LIKE 'ENG%' OR series_abbreviation = 'EN10'"
    )
    for r in cur.fetchall():
        code = r['series_abbreviation']
        # Check if any coin actually uses this code
        cur.execute(
            "SELECT COUNT(*) as cnt FROM coins WHERE coin_id LIKE ?",
            (f"%-{code}-%",)
        )
        count = cur.fetchone()['cnt']
        if count == 0:
            stale_codes.append(code)
            print(f"  {code}: no coins use this code → removing")
        else:
            print(f"  {code}: {count} coins use this code → keeping")

    if stale_codes:
        placeholders = ",".join("?" * len(stale_codes))
        cur.execute(
            f"DELETE FROM series_registry WHERE series_abbreviation IN ({placeholders})",
            stale_codes,
        )
        print(f"  Removed {cur.rowcount} stale entries")

    # === Fix 3: Fix denomination in coins table ===
    print("\n=== Fix 3: denomination='Engelhard Bullion' → 'No Face Value' ===")
    cur.execute(
        "SELECT COUNT(*) as cnt FROM coins WHERE denomination='Engelhard Bullion'"
    )
    count = cur.fetchone()['cnt']
    print(f"  Found {count} entries with 'Engelhard Bullion' denomination")

    cur.execute(
        "UPDATE coins SET denomination='No Face Value' "
        "WHERE denomination='Engelhard Bullion'"
    )
    print(f"  Updated {cur.rowcount} entries")

    # === Fix 4: Fix other private mint bars type in series_registry ===
    print("\n=== Fix 4: Fix other bar series type to 'bullion' ===")
    bar_codes = ["ENGP", "ENG5", "E100", "JMTB", "SCOT", "SUNM"]
    for code in bar_codes:
        cur.execute(
            "SELECT series_abbreviation, series_name, type FROM series_registry "
            "WHERE series_abbreviation=?",
            (code,),
        )
        row = cur.fetchone()
        if row and row['type'] != 'bullion':
            print(f"  {code}: {row['series_name']} type='{row['type']}' → 'bullion'")
            cur.execute(
                "UPDATE series_registry SET type='bullion' WHERE series_abbreviation=?",
                (code,),
            )

    # === Summary ===
    print("\n=== Summary ===")
    cur.execute(
        "SELECT COUNT(*) as cnt FROM series_registry WHERE type='bullion'"
    )
    print(f"  Total bullion series in registry: {cur.fetchone()['cnt']}")

    cur.execute(
        "SELECT COUNT(*) as cnt FROM coins WHERE denomination='Engelhard Bullion'"
    )
    remaining = cur.fetchone()['cnt']
    print(f"  Remaining 'Engelhard Bullion' denominations: {remaining}")

    conn.commit()
    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
