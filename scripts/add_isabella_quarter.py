#!/usr/bin/env python3
"""
Migration Script: Add Isabella Quarter (1893) - Issue #60

This script adds the Isabella Quarter, the first and only commemorative
quarter from the Classic Commemorative era (1892-1954).

Historical significance:
- Issued for the World's Columbian Exposition
- Features Queen Isabella of Spain
- First US coin to feature a foreign monarch
- Mintage: 24,214 pieces

Usage:
    uv run python scripts/add_isabella_quarter.py
    uv run python scripts/add_isabella_quarter.py --dry-run
"""

import sqlite3
import os
import argparse
from datetime import datetime

class IsabellaQuarterMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_isabella_quarter_{timestamp}.db"

        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def get_isabella_quarter(self):
        """Return Isabella Quarter coin data."""
        return {
            'coin_id': 'US-ISAB-1893-P',
            'year': 1893,
            'mint': 'P',
            'denomination': 'Commemorative Quarters',
            'series': "World's Columbian Exposition - Isabella Quarter",
            'variety': None,
            'composition': '90% Silver, 10% Copper',
            'weight_grams': 6.25,
            'diameter_mm': 24.3,
            'edge': 'Reeded',
            'designer': 'Charles E. Barber',
            'obverse_description': 'Queen Isabella of Spain with crown and scepter',
            'reverse_description': 'Kneeling woman with distaff and spindle',
            'business_strikes': 24214,
            'proof_strikes': None,
            'total_mintage': 24214,
            'notes': 'First commemorative quarter; first US coin featuring a foreign monarch; issued for World\'s Columbian Exposition',
            'rarity': 'key',
            'source_citation': 'Issue #60 CSV data; PCGS CoinFacts'
        }

    def insert_coin(self, conn, coin_data, dry_run=False):
        """Insert coin into database."""
        if dry_run:
            print(f"  [DRY RUN] Would insert: {coin_data['coin_id']}")
            return

        cursor = conn.cursor()

        insert_sql = """
        INSERT INTO coins (
            coin_id, year, mint, denomination, series, variety,
            composition, weight_grams, diameter_mm, edge, designer,
            obverse_description, reverse_description,
            business_strikes, proof_strikes, total_mintage,
            notes, rarity, source_citation
        ) VALUES (
            :coin_id, :year, :mint, :denomination, :series, :variety,
            :composition, :weight_grams, :diameter_mm, :edge, :designer,
            :obverse_description, :reverse_description,
            :business_strikes, :proof_strikes, :total_mintage,
            :notes, :rarity, :source_citation
        )
        """

        try:
            cursor.execute(insert_sql, coin_data)
            print(f"  ✓ Inserted: {coin_data['coin_id']} - {coin_data['series']}")
        except sqlite3.IntegrityError as e:
            print(f"  ⚠ Skipped {coin_data['coin_id']}: {e}")

    def run_migration(self, dry_run=False):
        """Execute the migration."""
        print("=" * 70)
        print("Add Isabella Quarter (1893) - Issue #60")
        print("=" * 70)
        print()

        if not dry_run:
            self.create_backup()
            print()

        # Connect to database
        conn = sqlite3.connect(self.db_path)

        try:
            # Get coin data
            coin = self.get_isabella_quarter()

            print("Adding Isabella Quarter:")
            print("-" * 70)
            print(f"  Coin ID: {coin['coin_id']}")
            print(f"  Year: {coin['year']}")
            print(f"  Mint: {coin['mint']}")
            print(f"  Denomination: {coin['denomination']}")
            print(f"  Series: {coin['series']}")
            print(f"  Mintage: {coin['total_mintage']:,}")
            print(f"  Composition: {coin['composition']}")
            print(f"  Weight: {coin['weight_grams']}g")
            print(f"  Diameter: {coin['diameter_mm']}mm")
            print(f"  Designer: {coin['designer']}")
            print(f"  Rarity: {coin['rarity']}")
            print()

            # Insert coin
            self.insert_coin(conn, coin, dry_run)

            if not dry_run:
                conn.commit()
                print()
                print("✓ Migration complete!")
                print()
                print("Next steps:")
                print("  1. Run: uv run python scripts/export_from_database.py")
                print("  2. Review generated JSON files")
                print("  3. Commit: git add . && git commit -m 'Add Isabella Quarter - Issue #60'")
            else:
                print()
                print("✓ Dry run complete - no changes made")

        except Exception as e:
            conn.rollback()
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            conn.close()

        return True

def main():
    parser = argparse.ArgumentParser(description='Add Isabella Quarter to database')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    args = parser.parse_args()

    migration = IsabellaQuarterMigration()
    success = migration.run_migration(dry_run=args.dry_run)

    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
