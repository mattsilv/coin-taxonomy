#!/usr/bin/env python3
"""
Add Modern Commemorative (MCOM) catch-all series code - Issue #88

This adds a catch-all series code for all 1982+ commemoratives. Individual series
can be broken out later (Washington 1982, Statue of Liberty 1986, etc.) as needed.

Modern US Commemorative denominations:
- $1 Silver (most common, 1982+)
- $5 Gold (1986+)
- 50c Clad (various programs)
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import shutil


def backup_database():
    """Create backup before migration."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)

    source = Path('database/coins.db')
    backup = backup_dir / f'coins_backup_mcom_{timestamp}.db'

    shutil.copy(source, backup)
    print(f"Database backed up to {backup}")
    return backup


def add_mcom_series(conn):
    """Add Modern Commemorative series entries to series_registry."""
    cursor = conn.cursor()

    # Modern Commemorative series definitions
    # Using different series_ids for each denomination but same abbreviation base
    mcom_series = [
        {
            'series_id': 'Modern Commemorative__Modern_Commemorative_Dollars',
            'series_name': 'Modern Commemorative',
            'series_abbreviation': 'MCOM',
            'country_code': 'US',
            'denomination': 'Modern Commemorative Dollars',
            'start_year': 1982,
            'end_year': None,  # Ongoing
            'defining_characteristics': 'Catch-all for 1982+ commemorative silver dollars until individual series defined. Includes all modern commemorative dollar programs from Washington 250th Anniversary (1982) to present.',
            'official_name': 'Modern Commemorative Dollar',
            'type': 'coin',
            'aliases': json.dumps(['Modern Comm', 'Commemorative', 'Modern Silver Commemorative']),
            'variety_suffixes': None
        },
        {
            'series_id': 'Modern Commemorative Gold__Modern_Commemorative_Gold',
            'series_name': 'Modern Commemorative Gold',
            'series_abbreviation': 'MCOG',
            'country_code': 'US',
            'denomination': 'Modern Commemorative Gold',
            'start_year': 1986,
            'end_year': None,  # Ongoing
            'defining_characteristics': 'Catch-all for 1986+ commemorative gold coins ($5, $10) until individual series defined. Includes all modern gold commemorative programs from Statue of Liberty (1986) to present.',
            'official_name': 'Modern Commemorative Gold',
            'type': 'coin',
            'aliases': json.dumps(['Gold Commemorative', 'Modern Gold Comm']),
            'variety_suffixes': None
        },
        {
            'series_id': 'Modern Commemorative Half__Modern_Commemorative_Half_Dollars',
            'series_name': 'Modern Commemorative Half',
            'series_abbreviation': 'MCOH',
            'country_code': 'US',
            'denomination': 'Modern Commemorative Half Dollars',
            'start_year': 1982,
            'end_year': None,  # Ongoing
            'defining_characteristics': 'Catch-all for 1982+ commemorative half dollars until individual series defined. Includes all modern clad half dollar commemorative programs.',
            'official_name': 'Modern Commemorative Half Dollar',
            'type': 'coin',
            'aliases': json.dumps(['Modern Comm Half', 'Commemorative Half']),
            'variety_suffixes': None
        }
    ]

    print(f"Adding {len(mcom_series)} Modern Commemorative series entries...")

    for series in mcom_series:
        try:
            cursor.execute("""
                INSERT INTO series_registry (
                    series_id, series_name, series_abbreviation, country_code,
                    denomination, start_year, end_year, defining_characteristics,
                    official_name, type, aliases, variety_suffixes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                series['series_id'],
                series['series_name'],
                series['series_abbreviation'],
                series['country_code'],
                series['denomination'],
                series['start_year'],
                series['end_year'],
                series['defining_characteristics'],
                series['official_name'],
                series['type'],
                series['aliases'],
                series['variety_suffixes']
            ))
            print(f"  Added {series['series_abbreviation']}: {series['series_name']} ({series['denomination']})")
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                print(f"  Skipped {series['series_abbreviation']}: already exists")
            else:
                raise


def verify_mcom_series(conn):
    """Verify MCOM series entries were added correctly."""
    cursor = conn.cursor()

    print("\nVerification Summary:")

    cursor.execute("""
        SELECT series_abbreviation, series_name, denomination, start_year
        FROM series_registry
        WHERE series_abbreviation LIKE 'MCO%'
        ORDER BY series_abbreviation
    """)

    results = cursor.fetchall()
    print(f"  Modern Commemorative series entries: {len(results)}")

    for row in results:
        abbrev, name, denom, start = row
        print(f"    {abbrev}: {name} ({denom}) - {start}+")


def main():
    """Execute Modern Commemorative series migration (Issue #88)."""
    print("Adding Modern Commemorative (MCOM) catch-all series - Issue #88")
    print("=" * 60)

    # Backup database
    backup_path = backup_database()

    try:
        # Connect to database
        conn = sqlite3.connect('database/coins.db')

        # Add MCOM series
        add_mcom_series(conn)

        # Commit changes
        conn.commit()

        # Verify results
        verify_mcom_series(conn)

        conn.close()

        print("\nModern Commemorative Series Migration Complete!")
        print("Next steps:")
        print("  1. Run export: uv run python scripts/export_from_database.py")
        print("  2. Commit all changes: git add . && git commit")
        print("  3. Create PR")

    except Exception as e:
        print(f"\nMigration failed: {e}")
        print(f"Restore from backup: {backup_path}")
        raise


if __name__ == "__main__":
    main()
