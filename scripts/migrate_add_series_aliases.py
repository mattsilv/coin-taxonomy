#!/usr/bin/env python3
"""
Database Migration: Add Series Aliases

Adds an aliases column to series_registry for alternative series names,
enabling downstream consumers to match by shortened names.

Example: "Albany Charter" → "Albany, New York, Charter"

Usage:
    uv run python scripts/migrate_add_series_aliases.py
    uv run python scripts/migrate_add_series_aliases.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
import shutil

# Commemorative half dollar alias mappings
# Maps canonical series_name → list of alternative names
COMMEMORATIVE_ALIASES = {
    "Alabama Centennial": ["Alabama"],
    "Alabama Centennial 2X2": ["Alabama 2X2"],
    "Albany, New York, Charter": ["Albany Charter", "Albany"],
    "Arkansas Centennial": ["Arkansas"],
    "Arkansas-Robinson": ["Robinson", "Arkansas Robinson"],
    "Battle of Antietam": ["Antietam Anniversary", "Antietam"],
    "Battle of Gettysburg": ["Gettysburg Anniversary", "Gettysburg"],
    "Booker T. Washington": ["Booker T Washington", "BTW"],
    "Bridgeport, Connecticut, Centennial": ["Bridgeport Centennial", "Bridgeport"],
    "California Diamond Jubilee": ["California Jubilee"],
    "California-Pacific Exposition": ["San Diego", "California Pacific"],
    "Carver/Washington": ["Carver-Washington", "Washington-Carver", "Carver Washington"],
    "Cincinnati Music Center": ["Cincinnati"],
    "Cleveland Centennial": ["Cleveland-Great Lakes", "Cleveland"],
    "Columbia, South Carolina, Sesquicentennial": ["Columbia South Carolina", "Columbia SC"],
    "Connecticut Tercentenary": ["Connecticut"],
    "Daniel Boone Bicentennial": ["Daniel Boone", "Boone"],
    "Delaware Tercentenary": ["Delaware"],
    "Elgin, Illinois, Centennial": ["Elgin Centennial", "Elgin"],
    "Fort Vancouver Centennial": ["Fort Vancouver"],
    "Grant Memorial": ["Grant"],
    "Grant Memorial with Star": ["Grant Star"],
    "Hawaiian Sesquicentennial": ["Hawaiian", "Hawaii"],
    "Hudson, New York, Sesquicentennial": ["Hudson Sesquicentennial", "Hudson"],
    "Huguenot-Walloon Tercentenary": ["Huguenot-Walloon", "Huguenot"],
    "Illinois Centennial": ["Illinois"],
    "Iowa Statehood Centennial": ["Iowa Centennial", "Iowa"],
    "Lafayette Dollar": ["Lafayette"],
    "Lexington-Concord Sesquicentennial": ["Lexington-Concord", "Lexington"],
    "Long Island Tercentenary": ["Long Island"],
    "Lynchburg, Virginia, Sesquicentennial": ["Lynchburg Sesquicentennial", "Lynchburg"],
    "Maine Centennial": ["Maine"],
    "Maryland Tercentenary": ["Maryland"],
    "Missouri Centennial": ["Missouri"],
    "Missouri Centennial 2★4": ["Missouri 2x4", "Missouri Star"],
    "Monroe Doctrine Centennial": ["Monroe Doctrine", "Monroe"],
    "New Rochelle, New York, 250th Anniversary": ["New Rochelle"],
    "Norfolk, Virginia, Bicentennial": ["Norfolk Bicentennial", "Norfolk"],
    "Old Spanish Trail": ["Spanish Trail"],
    "Oregon Trail Memorial": ["Oregon Trail", "Oregon"],
    "Panama-Pacific International Exposition": ["Panama-Pacific", "Pan-Pac"],
    "Pilgrim Tercentenary": ["Pilgrim"],
    "Providence, Rhode Island, Tercentenary": ["Rhode Island", "Providence"],
    "Roanoke Island": ["Roanoke"],
    "San Francisco-Oakland Bay Bridge": ["Bay Bridge", "SF-Oakland"],
    "Sesquicentennial of American Independence": ["Sesquicentennial", "1926 Sesqui"],
    "Stone Mountain Memorial": ["Stone Mountain"],
    "Texas Centennial": ["Texas"],
    "Vermont Sesquicentennial": ["Vermont"],
    "Wisconsin Territorial Centennial": ["Wisconsin Territorial", "Wisconsin"],
    "World's Columbian Exposition": ["Columbian Exposition", "Columbian Half", "Columbian"],
    "World's Columbian Exposition - Isabella Quarter": ["Isabella Quarter", "Isabella"],
    "York County, Maine, Tercentenary": ["York County"],
}


class SeriesAliasesMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_pre_series_aliases_{timestamp}.db"

        if os.path.exists(self.db_path):
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def add_aliases_column(self, conn, dry_run=False):
        """Add aliases column to series_registry table."""
        cursor = conn.cursor()

        # Check if column already exists
        cursor.execute("PRAGMA table_info(series_registry)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'aliases' in columns:
            print("✓ aliases column already exists")
            return

        if dry_run:
            print("\nDRY RUN: Would add aliases column to series_registry")
            print("  ALTER TABLE series_registry ADD COLUMN aliases JSON")
            return

        print("\nAdding aliases column to series_registry...")
        cursor.execute("ALTER TABLE series_registry ADD COLUMN aliases JSON")
        print("✓ aliases column added")

    def populate_aliases(self, conn, dry_run=False):
        """Populate aliases for commemorative half dollars."""
        cursor = conn.cursor()

        if dry_run:
            print("\nDRY RUN: Would populate aliases for commemorative half dollars:")
            for series_name, aliases in COMMEMORATIVE_ALIASES.items():
                print(f"  {series_name}: {aliases}")
            return

        print("\nPopulating aliases for commemorative half dollars...")
        updated = 0
        not_found = []

        for series_name, aliases in COMMEMORATIVE_ALIASES.items():
            aliases_json = json.dumps(aliases)
            cursor.execute('''
                UPDATE series_registry
                SET aliases = ?, updated_at = CURRENT_TIMESTAMP
                WHERE series_name = ? AND denomination LIKE '%Commemorative%Half%'
            ''', (aliases_json, series_name))

            if cursor.rowcount > 0:
                updated += 1
                print(f"  ✓ {series_name}")
            else:
                not_found.append(series_name)

        print(f"\n✓ Updated {updated} series with aliases")

        if not_found:
            print(f"\n⚠ Not found in registry ({len(not_found)}):")
            for name in not_found:
                print(f"  - {name}")

    def verify_aliases(self, conn):
        """Verify aliases were populated correctly."""
        cursor = conn.cursor()

        cursor.execute('''
            SELECT series_name, aliases
            FROM series_registry
            WHERE denomination LIKE '%Commemorative%Half%' AND aliases IS NOT NULL
            ORDER BY series_name
        ''')

        rows = cursor.fetchall()
        print(f"\n✓ {len(rows)} series have aliases:")
        for name, aliases_json in rows[:5]:
            aliases = json.loads(aliases_json) if aliases_json else []
            print(f"  {name}: {aliases}")
        if len(rows) > 5:
            print(f"  ... and {len(rows) - 5} more")

    def run(self, dry_run=False):
        """Execute the migration."""
        print("=" * 60)
        print("Series Aliases Migration")
        print("=" * 60)

        if not dry_run:
            self.create_backup()

        conn = sqlite3.connect(self.db_path)

        try:
            self.add_aliases_column(conn, dry_run)
            self.populate_aliases(conn, dry_run)

            if not dry_run:
                conn.commit()
                self.verify_aliases(conn)
                print("\n✓ Migration completed successfully")
            else:
                print("\n✓ DRY RUN completed - no changes made")
        finally:
            conn.close()


def main():
    parser = argparse.ArgumentParser(description='Add series aliases to database')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without making changes')
    args = parser.parse_args()

    migration = SeriesAliasesMigration()
    migration.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
