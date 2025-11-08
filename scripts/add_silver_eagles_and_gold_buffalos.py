#!/usr/bin/env python3
"""
Add American Silver Eagles and Gold Buffalos to Taxonomy

Adds 2 major US bullion series:
- ASEA: American Silver Eagle 1 oz ($1 denomination)
- AGBF: American Gold Buffalo 1 oz ($50 denomination)

Each series gets a random year entry (XXXX pattern) for bullion trading.

Usage:
    uv run python scripts/add_silver_eagles_and_gold_buffalos.py
    uv run python scripts/add_silver_eagles_and_gold_buffalos.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import List, Dict

class BullionSeriesMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_bullion_backup_{timestamp}.db"

        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def get_bullion_series(self) -> List[Dict]:
        """Define the American Silver Eagle and Gold Buffalo series."""
        return [
            # American Silver Eagle
            {
                "series_id": "american_silver_eagle_1oz",
                "series_name": "American Silver Eagle (1 oz)",
                "series_abbreviation": "ASEA",
                "country_code": "US",
                "denomination": "$1",
                "start_year": 1986,
                "end_year": None,  # Still minted
                "defining_characteristics": json.dumps({
                    "weight_troy_oz": 1.0,
                    "weight_grams": 31.103,
                    "diameter_mm": 40.6,
                    "thickness_mm": 2.98,
                    "fineness": 0.999,
                    "silver_content_oz": 1.0,
                    "composition": {"silver": 99.9},
                    "edge": "reeded",
                    "designer": "Adolph A. Weinman (obverse), John Mercanti (reverse Type 1), Emily Damstra (reverse Type 2)"
                }),
                "official_name": "American Silver Eagle $1 One Ounce Silver Coin",
                "type": "bullion"
            },
            # American Gold Buffalo
            {
                "series_id": "american_gold_buffalo_1oz",
                "series_name": "American Gold Buffalo (1 oz)",
                "series_abbreviation": "AGBF",
                "country_code": "US",
                "denomination": "$50",
                "start_year": 2006,
                "end_year": None,  # Still minted
                "defining_characteristics": json.dumps({
                    "weight_troy_oz": 1.0,
                    "weight_grams": 31.108,
                    "diameter_mm": 32.7,
                    "thickness_mm": 2.95,
                    "fineness": 0.9999,
                    "gold_content_oz": 1.0,
                    "composition": {"gold": 99.99},
                    "edge": "reeded",
                    "designer": "James Earle Fraser (obverse and reverse, based on 1913 Buffalo Nickel)"
                }),
                "official_name": "American Buffalo $50 One Ounce Gold Coin",
                "type": "bullion"
            }
        ]

    def get_random_year_coins(self) -> List[Dict]:
        """Create random year (XXXX) entries for Silver Eagles and Gold Buffalos."""

        return [
            # American Silver Eagle
            {
                "coin_id": "US-ASEA-XXXX-X",
                "series": "American Silver Eagle (1 oz)",
                "year": "XXXX",
                "mint": "X",
                "denomination": "$1",
                "composition": json.dumps({"silver": 99.9}),
                "weight_grams": 31.103,
                "diameter_mm": 40.6,
                "edge": "Reeded",
                "designer": "Adolph A. Weinman (obverse), John Mercanti (reverse)",
                "obverse_description": "Walking Liberty design - Liberty striding toward sunrise, draped in American flag, with 'LIBERTY' inscription and date",
                "reverse_description": "Heraldic eagle with shield, olive branch, and arrows, 13 stars above, '1 OZ. FINE SILVER ~ ONE DOLLAR' inscription",
                "notes": "Random year bullion - 1 troy oz silver content, dealer's choice year, valued by metal content. Type 1 reverse (1986-2021) or Type 2 reverse (2021-present) may vary.",
                "rarity": "common",
                "source_citation": "US Mint specifications, bullion dealers"
            },
            # American Gold Buffalo
            {
                "coin_id": "US-AGBF-XXXX-X",
                "series": "American Gold Buffalo (1 oz)",
                "year": "XXXX",
                "mint": "X",
                "denomination": "$50",
                "composition": json.dumps({"gold": 99.99}),
                "weight_grams": 31.108,
                "diameter_mm": 32.7,
                "edge": "Reeded",
                "designer": "James Earle Fraser",
                "obverse_description": "Profile of Native American chief (based on composite of three chiefs), 'LIBERTY' above, date below",
                "reverse_description": "American bison (buffalo) standing on mound, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', '$50', '1 OZ. .9999 FINE GOLD'",
                "notes": "Random year bullion - 1 troy oz 24-karat gold content, dealer's choice year, valued by metal content. First .9999 fine (24-karat) gold coin from US Mint.",
                "rarity": "common",
                "source_citation": "US Mint specifications, bullion dealers"
            }
        ]

    def insert_series(self, series_list: List[Dict], dry_run: bool = False):
        """Insert series into series_registry table."""
        if dry_run:
            print(f"DRY RUN: Would insert {len(series_list)} series:")
            for series in series_list:
                print(f"  - {series['series_abbreviation']}: {series['series_name']}")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            for series in series_list:
                cursor.execute('''
                    INSERT OR REPLACE INTO series_registry (
                        series_id, series_name, series_abbreviation, country_code,
                        denomination, start_year, end_year, defining_characteristics,
                        official_name, type
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    series['series_id'],
                    series['series_name'],
                    series['series_name'],
                    series['country_code'],
                    series['denomination'],
                    series['start_year'],
                    series['end_year'],
                    series['defining_characteristics'],
                    series['official_name'],
                    series['type']
                ))

                print(f"✓ Inserted series: {series['series_abbreviation']} - {series['series_name']}")

            conn.commit()
            print(f"✓ Successfully inserted {len(series_list)} series")

        except sqlite3.Error as e:
            conn.rollback()
            print(f"✗ Database error inserting series: {e}")
            raise
        finally:
            conn.close()

    def insert_coins(self, coins: List[Dict], dry_run: bool = False):
        """Insert random year coins into coins table."""
        if dry_run:
            print(f"DRY RUN: Would insert {len(coins)} coins:")
            for coin in coins:
                print(f"  - {coin['coin_id']}: {coin['series']}")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            for coin in coins:
                cursor.execute('''
                    INSERT OR REPLACE INTO coins (
                        coin_id, year, mint, denomination, series,
                        composition, weight_grams, diameter_mm, edge, designer,
                        obverse_description, reverse_description,
                        notes, rarity, source_citation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    coin['coin_id'],
                    coin['year'],
                    coin['mint'],
                    coin['denomination'],
                    coin['series'],
                    coin['composition'],
                    coin['weight_grams'],
                    coin['diameter_mm'],
                    coin['edge'],
                    coin['designer'],
                    coin['obverse_description'],
                    coin['reverse_description'],
                    coin['notes'],
                    coin['rarity'],
                    coin['source_citation']
                ))

                print(f"✓ Inserted coin: {coin['coin_id']}")

            conn.commit()
            print(f"✓ Successfully inserted {len(coins)} coins")

        except sqlite3.Error as e:
            conn.rollback()
            print(f"✗ Database error inserting coins: {e}")
            raise
        finally:
            conn.close()

    def run(self, dry_run: bool = False):
        """Execute the full migration."""
        print("=== American Silver Eagle & Gold Buffalo Migration ===\n")

        if not dry_run:
            self.create_backup()

        # Step 1: Add series to registry
        print("\nStep 1: Adding series to series_registry...")
        series_list = self.get_bullion_series()
        self.insert_series(series_list, dry_run)

        # Step 2: Add random year coins
        print("\nStep 2: Adding random year (XXXX) coins...")
        coins = self.get_random_year_coins()
        self.insert_coins(coins, dry_run)

        if not dry_run:
            print(f"\n✓ Migration completed successfully")
            print(f"✓ Backup: {self.backup_path}")
            print("\nAdded series:")
            print("  - ASEA: American Silver Eagle (1 oz)")
            print("  - AGBF: American Gold Buffalo (1 oz)")
            print("\nNext steps:")
            print("  1. Run: uv run python scripts/export_from_database.py")
            print("  2. Commit changes: git add . && git commit -m 'Add Silver Eagles & Gold Buffalos - Issues #51, #52'")
        else:
            print("\n✓ Dry run completed (no changes made)")

def main():
    parser = argparse.ArgumentParser(
        description='Add American Silver Eagles and Gold Buffalos to taxonomy'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying'
    )

    args = parser.parse_args()

    migration = BullionSeriesMigration()

    try:
        migration.run(dry_run=args.dry_run)
        return 0
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
