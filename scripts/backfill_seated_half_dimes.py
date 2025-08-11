#!/usr/bin/env python3
"""
Seated Liberty Half Dimes Backfill (1837-1873)
Based on dealer demand and market values provided
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import argparse

class SeatedHalfDimesBackfill:
    def __init__(self, db_path='database/coins.db', dry_run=False):
        self.db_path = db_path
        self.dry_run = dry_run
        
    def create_backup(self):
        """Create database backup before migration."""
        if self.dry_run:
            print("🔍 DRY RUN: Would create backup")
            return
            
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{backup_dir}/coins_half_dimes_backup_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ Backup created: {backup_path}")
    
    def get_seated_half_dimes(self) -> List[Dict]:
        """Get all Seated Liberty Half Dimes with market-based rarity."""
        coins = []
        
        # Market data with Good condition values to determine rarity
        # Key: >$100=key, $30-100=scarce, <$30=common
        market_data = {
            # Philadelphia Mint (no mintmark)
            1837: {"strikes": 1405000, "good_value": 40, "note": "First year of series"},
            1838: {"strikes": 2255000, "good_value": 18, "note": "No Drapery variety"},
            1839: {"strikes": 1034039, "good_value": 20, "note": "No Drapery variety"},
            1840: {"strikes": 1344085, "good_value": 20, "note": "No Drapery variety"},
            1841: {"strikes": 1150000, "good_value": 16, "note": "Drapery added"},
            1842: {"strikes": 815000, "good_value": 20, "note": "Standard design"},
            1843: {"strikes": 1165000, "good_value": 16, "note": ""},
            1844: {"strikes": 430000, "good_value": 16, "note": ""},
            1845: {"strikes": 1564000, "good_value": 16, "note": ""},
            1846: {"strikes": 27000, "good_value": 350, "note": "Very low mintage key date"},
            1847: {"strikes": 1274000, "good_value": 16, "note": ""},
            1848: {"strikes": 668000, "good_value": 16, "note": "Medium Date variety"},
            1849: {"strikes": 1309000, "good_value": 20, "note": "9 over 6 variety exists"},
            1850: {"strikes": 955000, "good_value": 18, "note": ""},
            1851: {"strikes": 781000, "good_value": 18, "note": ""},
            1852: {"strikes": 1000500, "good_value": 18, "note": ""},
            1853: {"strikes": 135000, "good_value": 35, "note": "Without Arrows variety"},
            1853.1: {"strikes": 13210020, "good_value": 20, "note": "With Arrows variety", "suffix": "A"},
            1854: {"strikes": 5740000, "good_value": 20, "note": "With Arrows"},
            1855: {"strikes": 1750000, "good_value": 20, "note": "Last year with Arrows"},
            1856: {"strikes": 4880000, "good_value": 18, "note": ""},
            1857: {"strikes": 7280000, "good_value": 18, "note": ""},
            1858: {"strikes": 3500000, "good_value": 18, "note": ""},
            1859: {"strikes": 340000, "good_value": 18, "note": ""},
            1860: {"strikes": 798000, "good_value": 16, "note": "Legend obverse begins"},
            1861: {"strikes": 3360000, "good_value": 16, "note": ""},
            1862: {"strikes": 1492000, "good_value": 25, "note": "Civil War year"},
            1863: {"strikes": 18000, "good_value": 160, "note": "Civil War low mintage"},
            1864: {"strikes": 48000, "good_value": 325, "note": "Civil War key date"},
            1865: {"strikes": 13000, "good_value": 275, "note": "Civil War key date"},
            1866: {"strikes": 10000, "good_value": 325, "note": "Post-war low mintage"},
            1867: {"strikes": 8000, "good_value": 450, "note": "Extremely low mintage"},
            1868: {"strikes": 88600, "good_value": 55, "note": ""},
            1869: {"strikes": 208000, "good_value": 16, "note": ""},
            1870: {"strikes": 535000, "good_value": 16, "note": ""},
            1871: {"strikes": 1873300, "good_value": 16, "note": ""},
            1872: {"strikes": 2947000, "good_value": 16, "note": "Mintmark below wreath"},
            1873: {"strikes": 712000, "good_value": 16, "note": "Last year of series"}
        }
        
        # New Orleans Mint data
        orleans_data = {
            1839: {"strikes": 1034039, "good_value": 20},
            1840: {"strikes": 1165000, "good_value": 20},
            1841: {"strikes": 815000, "good_value": 20},
            1842: {"strikes": 350000, "good_value": 30},
            1844: {"strikes": 220000, "good_value": 80},
            1848: {"strikes": 600000, "good_value": 22},
            1849: {"strikes": 140000, "good_value": 16},
            1850: {"strikes": 690000, "good_value": 25},
            1851: {"strikes": 860000, "good_value": 25},
            1852: {"strikes": 260000, "good_value": 30},
            1853: {"strikes": 160000, "good_value": 200, "note": "Without Arrows key date"},
            1853.1: {"strikes": 2200000, "good_value": 20, "note": "With Arrows"},
            1854: {"strikes": 1560000, "good_value": 20},
            1855: {"strikes": 600000, "good_value": 20},
            1856: {"strikes": 1100000, "good_value": 18},
            1857: {"strikes": 1380000, "good_value": 18},
            1858: {"strikes": 1660000, "good_value": 18},
            1859: {"strikes": 560000, "good_value": 20},
            1860: {"strikes": 1060000, "good_value": 16}
        }
        
        # San Francisco Mint data (starts 1863)
        sanfran_data = {
            1863: {"strikes": 100000, "good_value": 30},
            1864: {"strikes": 90000, "good_value": 45},
            1865: {"strikes": 120000, "good_value": 30},
            1866: {"strikes": 120000, "good_value": 30},
            1867: {"strikes": 120000, "good_value": 25},
            1868: {"strikes": 280000, "good_value": 16},
            1869: {"strikes": 230000, "good_value": 16},
            1871: {"strikes": 161000, "good_value": 18},
            1872: {"strikes": 837000, "good_value": 20},
            1873: {"strikes": 324000, "good_value": 16}
        }
        
        # Process Philadelphia Mint
        for year_key, data in market_data.items():
            year = int(year_key) if isinstance(year_key, int) else int(year_key)
            suffix = data.get("suffix", "")
            
            rarity = self.determine_rarity(data["good_value"])
            
            coin_id = f"US-SLHM-{year}-P"
            if suffix:
                coin_id = f"US-SLHM-{year}{suffix}-P"
            
            coin = self.create_coin_record(
                coin_id=coin_id,
                year=year,
                mint="P",
                strikes=data["strikes"],
                rarity=rarity,
                note=data.get("note", ""),
                good_value=data["good_value"]
            )
            coins.append(coin)
        
        # Process New Orleans Mint
        for year_key, data in orleans_data.items():
            year = int(year_key) if isinstance(year_key, int) else int(year_key)
            suffix = "A" if year_key == 1853.1 else ""
            
            rarity = self.determine_rarity(data["good_value"])
            
            coin_id = f"US-SLHM-{year}-O"
            if suffix:
                coin_id = f"US-SLHM-{year}{suffix}-O"
            
            coin = self.create_coin_record(
                coin_id=coin_id,
                year=year,
                mint="O",
                strikes=data["strikes"],
                rarity=rarity,
                note=data.get("note", "New Orleans Mint"),
                good_value=data["good_value"]
            )
            coins.append(coin)
        
        # Process San Francisco Mint
        for year, data in sanfran_data.items():
            rarity = self.determine_rarity(data["good_value"])
            
            coin = self.create_coin_record(
                coin_id=f"US-SLHM-{year}-S",
                year=year,
                mint="S",
                strikes=data["strikes"],
                rarity=rarity,
                note="San Francisco Mint",
                good_value=data["good_value"]
            )
            coins.append(coin)
        
        return coins
    
    def determine_rarity(self, good_value: int) -> str:
        """Determine rarity based on Good condition market value."""
        if good_value >= 100:
            return "key"
        elif good_value >= 30:
            return "scarce"
        else:
            return "common"
    
    def create_coin_record(self, coin_id: str, year: int, mint: str, strikes: int, 
                          rarity: str, note: str, good_value: int) -> Dict:
        """Create a complete coin record."""
        
        # Determine design variety
        if year <= 1840:
            variety = "No Drapery"
        elif 1853 in [year] and "Arrows" in note:
            variety = "With Arrows"
        elif 1853 in [year] and "Without" in note:
            variety = "Without Arrows"
        elif year >= 1854 and year <= 1855:
            variety = "With Arrows"
        elif year >= 1860:
            variety = "Legend Obverse"
        else:
            variety = "Standard"
        
        return {
            "coin_id": coin_id,
            "series_id": "seated_liberty_half_dime",
            "country": "US",
            "denomination": "Half Dimes",
            "series_name": "Seated Liberty Half Dime",
            "year": year,
            "mint": mint,
            "business_strikes": strikes,
            "proof_strikes": 0,
            "rarity": rarity,
            "composition": json.dumps({"silver": 0.90, "copper": 0.10}),
            "weight_grams": 1.24 if year < 1853 else 1.34 if "Arrows" in note else 1.24,
            "diameter_mm": 15.5,
            "varieties": json.dumps([variety]),
            "source_citation": "Red Book 2024, Dealer Market Values",
            "notes": f"{note}. Good condition value: ${good_value}",
            "obverse_description": self.get_obverse_description(year, variety),
            "reverse_description": self.get_reverse_description(year, mint),
            "distinguishing_features": json.dumps([
                "Christian Gobrecht design",
                "90% silver, 10% copper",
                "15.5mm diameter",
                "Reeded edge",
                variety,
                f"Mintmark {mint if mint != 'P' else 'none (Philadelphia)'}"
            ]),
            "identification_keywords": json.dumps([
                "seated liberty", "half dime", f"{year} half dime",
                "5 cents", "silver half dime", variety.lower(),
                f"{mint} mint" if mint != "P" else "philadelphia",
                "arrows" if "Arrows" in variety else "no arrows"
            ]),
            "common_names": json.dumps([
                "Seated Liberty Half Dime",
                f"{year} Half Dime",
                "5 Cent Silver"
            ])
        }
    
    def get_obverse_description(self, year: int, variety: str) -> str:
        """Get appropriate obverse description."""
        if variety == "No Drapery":
            return "Seated figure of Liberty holding pole with liberty cap, no drapery at elbow, 13 stars around, date below"
        elif variety == "Legend Obverse":
            return "Seated Liberty with 'UNITED STATES OF AMERICA' legend replacing stars, date below"
        elif "Arrows" in variety:
            return "Seated Liberty with arrows at date, holding pole with liberty cap and shield, 13 stars around"
        else:
            return "Seated figure of Liberty holding pole with liberty cap in left hand and shield in right, drapery at elbow, 13 stars around, date below"
    
    def get_reverse_description(self, year: int, mint: str) -> str:
        """Get appropriate reverse description."""
        mintmark_loc = "within wreath" if year < 1860 else "below wreath"
        
        if year < 1860:
            base = "Denomination 'HALF DIME' within wreath of cereal grains"
        else:
            base = "Denomination 'HALF DIME' within wreath"
        
        if mint != "P":
            return f"{base}, mintmark '{mint}' {mintmark_loc}"
        return base
    
    def insert_coins(self, coins: List[Dict]) -> int:
        """Insert coins into database."""
        if self.dry_run:
            print(f"\n🔍 DRY RUN: Would insert {len(coins)} coins")
            sample = min(5, len(coins))
            for coin in coins[:sample]:
                print(f"   - {coin['coin_id']}: {coin['series_name']} ({coin['year']})")
            if len(coins) > sample:
                print(f"   ... and {len(coins) - sample} more")
            return len(coins)
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        inserted = 0
        skipped = 0
        
        for coin in coins:
            try:
                cursor.execute("""
                    INSERT INTO coins (
                        coin_id, series_id, country, denomination, series_name,
                        year, mint, business_strikes, proof_strikes, rarity,
                        composition, weight_grams, diameter_mm, varieties,
                        source_citation, notes, obverse_description,
                        reverse_description, distinguishing_features,
                        identification_keywords, common_names
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    coin['coin_id'], coin['series_id'], coin['country'],
                    coin['denomination'], coin['series_name'], coin['year'],
                    coin['mint'], coin['business_strikes'], coin['proof_strikes'],
                    coin['rarity'], coin['composition'], coin['weight_grams'],
                    coin['diameter_mm'], coin['varieties'], coin['source_citation'],
                    coin['notes'], coin['obverse_description'], coin['reverse_description'],
                    coin['distinguishing_features'], coin['identification_keywords'],
                    coin['common_names']
                ))
                inserted += 1
                
            except sqlite3.IntegrityError as e:
                skipped += 1
                
        conn.commit()
        conn.close()
        
        print(f"✅ Inserted {inserted} coins")
        if skipped > 0:
            print(f"⚠️  Skipped {skipped} existing coins")
            
        return inserted
    
    def run_migration(self):
        """Execute the migration."""
        print("\n💰 SEATED LIBERTY HALF DIMES BACKFILL (1837-1873)")
        print("=" * 60)
        
        self.create_backup()
        
        print("\n📊 Preparing Seated Liberty Half Dimes data...")
        half_dimes = self.get_seated_half_dimes()
        
        # Count by mint
        mint_counts = {"P": 0, "O": 0, "S": 0}
        for coin in half_dimes:
            mint_counts[coin['mint']] += 1
        
        print(f"   • Total Half Dimes: {len(half_dimes)} coins")
        print(f"     - Philadelphia (P): {mint_counts['P']} coins")
        print(f"     - New Orleans (O): {mint_counts['O']} coins")
        print(f"     - San Francisco (S): {mint_counts['S']} coins")
        
        # Count rarities
        rarity_counts = {"common": 0, "scarce": 0, "key": 0}
        for coin in half_dimes:
            rarity_counts[coin['rarity']] += 1
        
        print(f"\n   Rarity distribution:")
        print(f"     - Common: {rarity_counts['common']} coins")
        print(f"     - Scarce: {rarity_counts['scarce']} coins")
        print(f"     - Key dates: {rarity_counts['key']} coins")
        
        print("\n💾 Inserting coins...")
        total_inserted = self.insert_coins(half_dimes)
        
        print(f"\n✅ MIGRATION COMPLETE: {total_inserted} Half Dimes added")
        
        if not self.dry_run:
            print("\n📝 Next steps:")
            print("   1. Run: uv run python scripts/export_from_database.py")
            print("   2. Commit: git add . && git commit")
        
        return total_inserted


def main():
    parser = argparse.ArgumentParser(description='Backfill Seated Liberty Half Dimes')
    parser.add_argument('--dry-run', action='store_true', help='Preview without modifying database')
    args = parser.parse_args()
    
    backfill = SeatedHalfDimesBackfill(dry_run=args.dry_run)
    backfill.run_migration()


if __name__ == "__main__":
    main()