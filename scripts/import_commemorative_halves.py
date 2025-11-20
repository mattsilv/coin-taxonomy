#!/usr/bin/env python3
"""
Import US Commemorative Half Dollars into the database.
Reads from data/us/coins/commemorative_half_dollars.json and imports all coins.
"""

import sqlite3
import json
from typing import Dict, Any

class CommemHalvesImporter:
    def __init__(self, db_path='coins.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close database connection."""
        self.conn.commit()
        self.conn.close()

    def insert_coin(self, coin_data: Dict[str, Any], series_name: str) -> bool:
        """Insert a single coin into the database."""
        try:
            # Calculate total mintage
            business = coin_data.get('business_strikes') or 0
            proof = coin_data.get('proof_strikes') or 0
            total = business + proof if (business or proof) else None

            # Prepare composition (convert dict to JSON string)
            composition_dict = coin_data.get('composition', {})
            composition = json.dumps(composition_dict) if composition_dict else None

            self.cursor.execute('''
                INSERT INTO coins (
                    coin_id, year, mint, denomination, series,
                    business_strikes, proof_strikes, total_mintage,
                    composition, weight_grams, diameter_mm,
                    designer, obverse_description, reverse_description,
                    rarity, notes, source_citation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coin_data['coin_id'],
                str(coin_data['year']),
                coin_data['mint'],
                'Commemorative Half Dollar',  # Standardized denomination
                series_name,
                business if business else None,
                proof if proof else None,
                total,
                composition,
                coin_data.get('weight_grams'),
                coin_data.get('diameter_mm'),
                coin_data.get('designer'),
                coin_data.get('obverse_description'),
                coin_data.get('reverse_description'),
                coin_data.get('rarity'),
                coin_data.get('notes'),
                coin_data.get('source_citation')
            ))
            return True
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                print(f"   ⚠️  Coin already exists: {coin_data['coin_id']}")
            else:
                print(f"   ❌ Error inserting {coin_data['coin_id']}: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Unexpected error inserting {coin_data['coin_id']}: {e}")
            return False

    def import_from_json(self, json_path='data/us/coins/commemorative_half_dollars.json'):
        """Import all commemorative half dollars from JSON file."""
        print(f"\n📊 Importing US Commemorative Half Dollars from {json_path}")

        # Load JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)

        total_coins = 0
        total_series = 0
        imported = 0
        skipped = 0

        # Process each series
        for series in data.get('series', []):
            series_name = series.get('series_name') or series.get('series_id', 'Unknown')
            coins = series.get('coins', [])

            if not coins:
                continue

            total_series += 1
            print(f"\n  📁 Series: {series_name} ({len(coins)} coins)")

            # Process each coin in the series
            for coin in coins:
                total_coins += 1
                if self.insert_coin(coin, series_name):
                    imported += 1
                    print(f"    ✅ {coin['coin_id']}")
                else:
                    skipped += 1

        self.conn.commit()

        # Print summary
        print(f"\n{'='*60}")
        print(f"📊 Import Summary")
        print(f"{'='*60}")
        print(f"  Series processed: {total_series}")
        print(f"  Total coins:      {total_coins}")
        print(f"  Imported:         {imported}")
        print(f"  Skipped:          {skipped}")
        print(f"{'='*60}\n")

        return imported

def main():
    """Main import function."""
    importer = CommemHalvesImporter()

    try:
        imported = importer.import_from_json()
        print(f"✅ Successfully imported {imported} commemorative half dollars")
    except Exception as e:
        print(f"❌ Error during import: {e}")
        raise
    finally:
        importer.close()

if __name__ == '__main__':
    main()
