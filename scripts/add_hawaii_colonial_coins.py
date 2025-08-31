#!/usr/bin/env python3
"""
Add Hawaii Dime (1883) and Colonial Virginia coins to the database.

This script adds:
1. 1883 Hawaii Dime (Kingdom of Hawaii coinage)
2. Virginia Colonial Halfpenny (1773) 
3. Virginia Colonial Penny (1773 pattern)
4. Virginia Colonial Shilling (1774 pattern)

Usage:
    python scripts/add_hawaii_colonial_coins.py
    python scripts/add_hawaii_colonial_coins.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List

class HawaiiColonialBackfill:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None
        
    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_hawaii_colonial_backup_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")
    
    def get_hawaii_coins(self) -> List[Dict]:
        """Return Hawaii coinage data."""
        return [
            {
                "coin_id": "US-HWDI-1883-S",
                "series_id": "hawaii_dime",
                "series_name": "Hawaii Dime",
                "year": 1883,
                "mint": "S",
                "denomination": "Dimes",
                "business_strikes": 250000,
                "proof_strikes": 26,
                "rarity": "scarce",
                "composition": {"silver": 0.9, "copper": 0.1},
                "weight_grams": 2.5,
                "diameter_mm": 17.9,
                "varieties": [],
                "source_citation": "Red Book 2024, PCGS CoinFacts, Wikipedia",
                "notes": "Kingdom of Hawaii coinage under King Kalākaua",
                "obverse_description": "Right-facing bust of King Kalākaua with 'KALAKAUA I.' inscription and title",
                "reverse_description": "Wreath with 'UMI KENETA' (Hawaiian) and 'ONE DIME' below, royal motto 'Ua Mau ke Ea o ka ʻĀina i ka Pono' around",
                "distinguishing_features": [
                    "Kingdom of Hawaii coinage",
                    "Dated 1883 but struck 1883-1884",
                    "Designed by Charles E. Barber",
                    "Struck at San Francisco Mint",
                    "90% silver composition",
                    "Demonetized January 1, 1904",
                    "Most melted after withdrawal"
                ],
                "identification_keywords": [
                    "hawaii dime",
                    "kalakaua dime",
                    "1883 hawaii",
                    "hawaiian coinage",
                    "umi keneta",
                    "kingdom of hawaii",
                    "hawaiian silver",
                    "barber design"
                ],
                "common_names": [
                    "Hawaii Dime",
                    "1883 Hawaii Dime",
                    "Kalākaua Dime"
                ]
            }
        ]
    
    def get_colonial_coins(self) -> List[Dict]:
        """Return Colonial Virginia coinage data."""
        return [
            {
                "coin_id": "US-VHPW-1773-L",
                "series_id": "virginia_halfpenny", 
                "series_name": "Virginia Halfpenny",
                "year": 1773,
                "mint": "L",  # L for London (Tower Mint)
                "denomination": "Half Cents",
                "business_strikes": 670000,
                "proof_strikes": 0,
                "rarity": "scarce",
                "composition": {"copper": 1.0},
                "weight_grams": 7.78,  # 120 grains
                "diameter_mm": 25,
                "varieties": [
                    {
                        "variety_id": "VHPW-1773-L-WP-01",
                        "name": "With Period after GEORGIVS",
                        "description": "Period after GEORGIVS"
                    },
                    {
                        "variety_id": "VHPW-1773-L-NP-01", 
                        "name": "No Period after GEORGIVS",
                        "description": "No period after GEORGIVS"
                    }
                ],
                "source_citation": "APMEX Guide, Newman Numismatic Portal",
                "notes": "Colonial/Pre-Federal issue struck at Tower Mint, London",
                "obverse_description": "George III bust right with 'GEORGIVS III REX' legend",
                "reverse_description": "Crowned shield with 'VIR-GINIA' split by crown, date split '17-73'",
                "distinguishing_features": [
                    "Colonial Virginia coinage",
                    "Struck at Tower Mint, London",
                    "Authorized by Virginia Assembly 1773",
                    "Arrived in Virginia 1774",
                    "Distributed 1775",
                    "22 die pairs used",
                    "Many hoarded during Revolution",
                    "Two major obverse varieties"
                ],
                "identification_keywords": [
                    "virginia halfpenny",
                    "colonial virginia",
                    "1773 halfpenny",
                    "george iii",
                    "colonial copper",
                    "pre-federal",
                    "tower mint",
                    "virginia coinage"
                ],
                "common_names": [
                    "Virginia Halfpenny",
                    "1773 Virginia Halfpenny",
                    "Colonial Virginia Halfpenny"
                ]
            },
            {
                "coin_id": "US-VPEN-1773-L",
                "series_id": "virginia_penny",
                "series_name": "Virginia Penny",
                "year": 1773,
                "mint": "L",
                "denomination": "Cents",
                "business_strikes": 0,
                "proof_strikes": 30,  # Estimated 30 known
                "rarity": "key",
                "composition": {"copper": 1.0},
                "weight_grams": 15.56,  # Double the halfpenny
                "diameter_mm": 33,
                "varieties": [],
                "source_citation": "APMEX Guide, Newman Numismatic Portal",
                "notes": "Extremely rare pattern denomination",
                "obverse_description": "George III bust right with 'GEORGIVS III REX' legend",
                "reverse_description": "Crowned shield with 'VIRGINIA' and date '1773'",
                "distinguishing_features": [
                    "Pattern denomination",
                    "Extremely rare with ~30 known",
                    "Colonial Virginia coinage",
                    "Struck at Tower Mint, London",
                    "Not issued for circulation"
                ],
                "identification_keywords": [
                    "virginia penny",
                    "colonial pattern",
                    "1773 penny",
                    "virginia pattern",
                    "rare colonial",
                    "george iii"
                ],
                "common_names": [
                    "Virginia Penny",
                    "1773 Virginia Penny Pattern"
                ]
            },
            {
                "coin_id": "US-VSHL-1774-L",
                "series_id": "virginia_shilling",
                "series_name": "Virginia Shilling",
                "year": 1774,
                "mint": "L",
                "denomination": "Twenty Cents",  # Approximating shilling value
                "business_strikes": 0,
                "proof_strikes": 6,  # Estimated 6 known
                "rarity": "key",
                "composition": {"silver": 0.925},
                "weight_grams": 5.66,
                "diameter_mm": 25,
                "varieties": [],
                "source_citation": "APMEX Guide, Newman Numismatic Portal",
                "notes": "Extremely rare pattern/trial, approximately 6 known",
                "obverse_description": "George III bust right with 'GEORGIVS III REX' legend",
                "reverse_description": "Crowned shield with 'VIRGINIA' and date '1774'",
                "distinguishing_features": [
                    "Pattern/trial denomination",
                    "Extremely rare with ~6 known",
                    "Colonial Virginia coinage",
                    "Silver composition",
                    "Dated 1774",
                    "Not issued for circulation"
                ],
                "identification_keywords": [
                    "virginia shilling",
                    "colonial pattern",
                    "1774 shilling",
                    "virginia trial",
                    "rare colonial",
                    "silver colonial"
                ],
                "common_names": [
                    "Virginia Shilling",
                    "1774 Virginia Shilling Pattern"
                ]
            }
        ]
    
    def insert_coins_batch(self, coins: List[Dict], dry_run: bool = False):
        """Insert a batch of coins into the database."""
        if dry_run:
            print(f"DRY RUN: Would insert {len(coins)} coins:")
            for coin in coins:
                print(f"  - {coin['coin_id']}: {coin['series_name']} {coin['year']}")
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for coin in coins:
                # Prepare coin data with proper defaults
                coin_data = {
                    'coin_id': coin['coin_id'],
                    'series_id': coin['series_id'], 
                    'country': 'US',
                    'denomination': coin['denomination'],
                    'series_name': coin['series_name'],
                    'year': coin['year'],
                    'mint': coin['mint'],
                    'business_strikes': coin.get('business_strikes'),
                    'proof_strikes': coin.get('proof_strikes', 0),
                    'rarity': coin.get('rarity', 'common'),
                    'composition': json.dumps(coin.get('composition', {})),
                    'weight_grams': coin.get('weight_grams'),
                    'diameter_mm': coin.get('diameter_mm'),
                    'varieties': json.dumps(coin.get('varieties', [])),
                    'source_citation': coin.get('source_citation', 'Historical Research'),
                    'notes': coin.get('notes'),
                    'obverse_description': coin.get('obverse_description'),
                    'reverse_description': coin.get('reverse_description'),
                    'distinguishing_features': json.dumps(coin.get('distinguishing_features', [])),
                    'identification_keywords': json.dumps(coin.get('identification_keywords', [])),
                    'common_names': json.dumps(coin.get('common_names', []))
                }
                
                # Insert coin
                cursor.execute('''
                    INSERT OR REPLACE INTO coins (
                        coin_id, series_id, country, denomination, series_name,
                        year, mint, business_strikes, proof_strikes, rarity,
                        composition, weight_grams, diameter_mm, varieties,
                        source_citation, notes, obverse_description, reverse_description,
                        distinguishing_features, identification_keywords, common_names
                    ) VALUES (
                        :coin_id, :series_id, :country, :denomination, :series_name,
                        :year, :mint, :business_strikes, :proof_strikes, :rarity,
                        :composition, :weight_grams, :diameter_mm, :varieties,
                        :source_citation, :notes, :obverse_description, :reverse_description,
                        :distinguishing_features, :identification_keywords, :common_names
                    )
                ''', coin_data)
                
                print(f"✓ Inserted: {coin['coin_id']} - {coin['series_name']} {coin['year']}")
                
            conn.commit()
            print(f"✓ Successfully inserted {len(coins)} coins")
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f"✗ Database error: {e}")
            raise
        finally:
            conn.close()
    
    def run(self, dry_run: bool = False):
        """Execute the migration."""
        print("\n=== Adding Hawaii and Colonial Coins ===")
        
        if not dry_run:
            self.create_backup()
        
        # Get all coins
        hawaii_coins = self.get_hawaii_coins()
        colonial_coins = self.get_colonial_coins()
        all_coins = hawaii_coins + colonial_coins
        
        print(f"\nAdding {len(hawaii_coins)} Hawaii coin(s)")
        print(f"Adding {len(colonial_coins)} Colonial coin(s)")
        
        # Insert all coins
        self.insert_coins_batch(all_coins, dry_run)
        
        if not dry_run:
            print(f"\n✓ Migration completed. Backup: {self.backup_path}")

def main():
    parser = argparse.ArgumentParser(description='Add Hawaii and Colonial coins to database')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    
    args = parser.parse_args()
    
    backfill = HawaiiColonialBackfill()
    
    try:
        backfill.run(dry_run=args.dry_run)
        
        if not args.dry_run:
            print("\n✓ Migration completed. Run the following to update JSON exports:")
            print("  uv run python scripts/export_from_database.py")
            
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())