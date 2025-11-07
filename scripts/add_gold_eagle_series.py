#!/usr/bin/env python3
"""
Add American Gold Eagle Weight Variations to Taxonomy

Adds 4 distinct series for American Gold Eagle bullion in different weights:
- AGEO: 1 oz ($50 denomination)
- AGEF: 1/2 oz ($25 denomination)
- AGET: 1/4 oz ($10 denomination)
- AGES: 1/10 oz ($5 denomination)

Each series gets a random year entry (XXXX pattern) for bullion trading.

Usage:
    uv run python scripts/add_gold_eagle_series.py
    uv run python scripts/add_gold_eagle_series.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import List, Dict

class GoldEagleSeriesMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_gold_eagle_backup_{timestamp}.db"

        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def get_gold_eagle_series(self) -> List[Dict]:
        """Define the 4 American Gold Eagle series."""
        return [
            {
                "series_id": "american_gold_eagle_1oz",
                "series_name": "American Gold Eagle (1 oz)",
                "series_abbreviation": "AGEO",
                "country_code": "US",
                "denomination": "$50",
                "start_year": 1986,  # First year of Gold Eagles
                "end_year": None,    # Still minted
                "defining_characteristics": json.dumps({
                    "weight_troy_oz": 1.0,
                    "weight_grams": 31.103,
                    "diameter_mm": 32.7,
                    "thickness_mm": 2.87,
                    "fineness": 0.9167,
                    "gold_content_oz": 1.0,
                    "composition": {"gold": 91.67, "silver": 3.0, "copper": 5.33},
                    "edge": "reeded",
                    "designer": "Augustus Saint-Gaudens (obverse), Miley Busiek (reverse)"
                }),
                "official_name": "American Gold Eagle $50 One Ounce Gold Coin",
                "type": "bullion"
            },
            {
                "series_id": "american_gold_eagle_half_oz",
                "series_name": "American Gold Eagle (1/2 oz)",
                "series_abbreviation": "AGEF",
                "country_code": "US",
                "denomination": "$25",
                "start_year": 1986,
                "end_year": None,
                "defining_characteristics": json.dumps({
                    "weight_troy_oz": 0.5,
                    "weight_grams": 16.966,
                    "diameter_mm": 27.0,
                    "thickness_mm": 2.24,
                    "fineness": 0.9167,
                    "gold_content_oz": 0.5,
                    "composition": {"gold": 91.67, "silver": 3.0, "copper": 5.33},
                    "edge": "reeded",
                    "designer": "Augustus Saint-Gaudens (obverse), Miley Busiek (reverse)"
                }),
                "official_name": "American Gold Eagle $25 Half Ounce Gold Coin",
                "type": "bullion"
            },
            {
                "series_id": "american_gold_eagle_quarter_oz",
                "series_name": "American Gold Eagle (1/4 oz)",
                "series_abbreviation": "AGET",
                "country_code": "US",
                "denomination": "$10",
                "start_year": 1986,
                "end_year": None,
                "defining_characteristics": json.dumps({
                    "weight_troy_oz": 0.25,
                    "weight_grams": 8.483,
                    "diameter_mm": 22.0,
                    "thickness_mm": 1.83,
                    "fineness": 0.9167,
                    "gold_content_oz": 0.25,
                    "composition": {"gold": 91.67, "silver": 3.0, "copper": 5.33},
                    "edge": "reeded",
                    "designer": "Augustus Saint-Gaudens (obverse), Miley Busiek (reverse)"
                }),
                "official_name": "American Gold Eagle $10 Quarter Ounce Gold Coin",
                "type": "bullion"
            },
            {
                "series_id": "american_gold_eagle_tenth_oz",
                "series_name": "American Gold Eagle (1/10 oz)",
                "series_abbreviation": "AGES",
                "country_code": "US",
                "denomination": "$5",
                "start_year": 1986,
                "end_year": None,
                "defining_characteristics": json.dumps({
                    "weight_troy_oz": 0.1,
                    "weight_grams": 3.393,
                    "diameter_mm": 16.5,
                    "thickness_mm": 1.26,
                    "fineness": 0.9167,
                    "gold_content_oz": 0.1,
                    "composition": {"gold": 91.67, "silver": 3.0, "copper": 5.33},
                    "edge": "reeded",
                    "designer": "Augustus Saint-Gaudens (obverse), Miley Busiek (reverse)"
                }),
                "official_name": "American Gold Eagle $5 Tenth Ounce Gold Coin",
                "type": "bullion"
            }
        ]

    def get_random_year_coins(self) -> List[Dict]:
        """Create random year (XXXX) entries for each Gold Eagle weight."""
        base_description = {
            "obverse_description": "Lady Liberty striding forward with torch and olive branch, Capitol building in background, rays of sunlight",
            "reverse_description": "Male eagle carrying olive branch flying above nest with female eagle and eaglets",
        }

        return [
            {
                "coin_id": "US-AGEO-XXXX-X",
                "series": "American Gold Eagle (1 oz)",
                "year": "XXXX",
                "mint": "X",
                "denomination": "$50",
                "composition": json.dumps({"gold": 91.67, "silver": 3.0, "copper": 5.33}),
                "weight_grams": 31.103,
                "diameter_mm": 32.7,
                "edge": "Reeded",
                "designer": "Augustus Saint-Gaudens (obverse), Miley Busiek (reverse)",
                "notes": "Random year bullion - 1 troy oz gold content, dealer's choice year, valued by metal content",
                "rarity": "common",
                "source_citation": "US Mint specifications, bullion dealers",
                **base_description
            },
            {
                "coin_id": "US-AGEF-XXXX-X",
                "series": "American Gold Eagle (1/2 oz)",
                "year": "XXXX",
                "mint": "X",
                "denomination": "$25",
                "composition": json.dumps({"gold": 91.67, "silver": 3.0, "copper": 5.33}),
                "weight_grams": 16.966,
                "diameter_mm": 27.0,
                "edge": "Reeded",
                "designer": "Augustus Saint-Gaudens (obverse), Miley Busiek (reverse)",
                "notes": "Random year bullion - 1/2 troy oz gold content, dealer's choice year, valued by metal content",
                "rarity": "common",
                "source_citation": "US Mint specifications, bullion dealers",
                **base_description
            },
            {
                "coin_id": "US-AGET-XXXX-X",
                "series": "American Gold Eagle (1/4 oz)",
                "year": "XXXX",
                "mint": "X",
                "denomination": "$10",
                "composition": json.dumps({"gold": 91.67, "silver": 3.0, "copper": 5.33}),
                "weight_grams": 8.483,
                "diameter_mm": 22.0,
                "edge": "Reeded",
                "designer": "Augustus Saint-Gaudens (obverse), Miley Busiek (reverse)",
                "notes": "Random year bullion - 1/4 troy oz gold content, dealer's choice year, valued by metal content",
                "rarity": "common",
                "source_citation": "US Mint specifications, bullion dealers",
                **base_description
            },
            {
                "coin_id": "US-AGES-XXXX-X",
                "series": "American Gold Eagle (1/10 oz)",
                "year": "XXXX",
                "mint": "X",
                "denomination": "$5",
                "composition": json.dumps({"gold": 91.67, "silver": 3.0, "copper": 5.33}),
                "weight_grams": 3.393,
                "diameter_mm": 16.5,
                "edge": "Reeded",
                "designer": "Augustus Saint-Gaudens (obverse), Miley Busiek (reverse)",
                "notes": "Random year bullion - 1/10 troy oz gold content, dealer's choice year, valued by metal content",
                "rarity": "common",
                "source_citation": "US Mint specifications, bullion dealers",
                **base_description
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
                    series['series_abbreviation'],
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
        print("=== American Gold Eagle Series Migration ===\n")

        if not dry_run:
            self.create_backup()

        # Step 1: Add series to registry
        print("\nStep 1: Adding series to series_registry...")
        series_list = self.get_gold_eagle_series()
        self.insert_series(series_list, dry_run)

        # Step 2: Add random year coins
        print("\nStep 2: Adding random year (XXXX) coins...")
        coins = self.get_random_year_coins()
        self.insert_coins(coins, dry_run)

        if not dry_run:
            print(f"\n✓ Migration completed successfully")
            print(f"✓ Backup: {self.backup_path}")
            print("\nNext steps:")
            print("  1. Run: uv run python scripts/export_from_database.py")
            print("  2. Commit changes: git add . && git commit -m 'Add Gold Eagle weight variations - Issue #XX'")
        else:
            print("\n✓ Dry run completed (no changes made)")

def main():
    parser = argparse.ArgumentParser(
        description='Add American Gold Eagle weight variations to taxonomy'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying'
    )

    args = parser.parse_args()

    migration = GoldEagleSeriesMigration()

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
