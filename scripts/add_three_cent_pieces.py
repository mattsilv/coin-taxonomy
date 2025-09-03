#!/usr/bin/env python3
"""
Three-Cent Pieces Migration (1851-1889)
Two distinct series: Silver (1851-1873) and Nickel (1865-1889)
Critical issue #50 - unique denomination highly sought by collectors
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List
import argparse

class ThreeCentPiecesMigration:
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
        backup_path = f"{backup_dir}/coins_three_cent_backup_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ Backup created: {backup_path}")
    
    def get_silver_three_cents(self) -> List[Dict]:
        """Get Silver Three-Cent pieces (1851-1873)."""
        coins = []
        
        # Type I Silver Three-Cent (1851-1853) - 75% silver, no outlines on star
        type1_mintages = {
            1851: {'P': 5447400, 'O': 720000},
            1852: {'P': 18663500, 'O': 720000}, 
            1853: {'P': 11400000, 'O': 1332000}
        }
        
        for year, mints in type1_mintages.items():
            for mint, mintage in mints.items():
                coins.append({
                    "coin_id": f"US-TCST-{year}-{mint}",
                    "series_id": "us-three-cent-silver-type1",
                    "series_name": "Silver Three-Cent Type I",
                    "year": year,
                    "mint": mint,
                    "business_strikes": mintage,
                    "proof_strikes": 0,
                    "rarity": "common",
                    "composition": {"silver": 75.0, "copper": 25.0},
                    "weight_grams": 0.80,
                    "diameter_mm": 14.0,
                    "type": "Type I",
                    "note": "No outlines on star, 75% silver"
                })
        
        # Type II Silver Three-Cent (1854-1858) - 90% silver, three outlines on star
        type2_mintages = {
            1854: 671000, 1855: 139000, 1856: 1458000, 
            1857: 1042000, 1858: 1604000
        }
        
        for year, mintage in type2_mintages.items():
            rarity = "key" if year == 1855 else "scarce" if mintage < 1000000 else "common"
            coins.append({
                "coin_id": f"US-TCST-{year}-P",
                "series_id": "us-three-cent-silver-type2", 
                "series_name": "Silver Three-Cent Type II",
                "year": year,
                "mint": "P",
                "business_strikes": mintage,
                "proof_strikes": 0,
                "rarity": rarity,
                "composition": {"silver": 90.0, "copper": 10.0},
                "weight_grams": 0.75,
                "diameter_mm": 14.0,
                "type": "Type II",
                "note": "Three outlines on star, 90% silver"
            })
        
        # Type III Silver Three-Cent (1859-1873) - 90% silver, two outlines on star
        type3_mintages = {
            1859: 365000, 1860: 287000, 1861: 498000, 1862: 343000,
            1863: 21000, 1864: 12000, 1865: 8000, 1866: 22000,
            1867: 4000, 1868: 4000, 1869: 5000, 1870: 4000,
            1871: 4000, 1872: 1000, 1873: 600
        }
        
        for year, mintage in type3_mintages.items():
            if year >= 1863:
                rarity = "key"
            elif mintage < 500000:
                rarity = "scarce"  
            else:
                rarity = "common"
                
            coins.append({
                "coin_id": f"US-TCST-{year}-P",
                "series_id": "us-three-cent-silver-type3",
                "series_name": "Silver Three-Cent Type III", 
                "year": year,
                "mint": "P",
                "business_strikes": mintage,
                "proof_strikes": 0,
                "rarity": rarity,
                "composition": {"silver": 90.0, "copper": 10.0},
                "weight_grams": 0.75,
                "diameter_mm": 14.0,
                "type": "Type III",
                "note": "Two outlines on star, 90% silver"
            })
            
        return coins
    
    def get_nickel_three_cents(self) -> List[Dict]:
        """Get Nickel Three-Cent pieces (1865-1889)."""
        coins = []
        
        # Nickel Three-Cent mintages by year
        mintages = {
            1865: 11382000, 1866: 4801000, 1867: 3915000, 1868: 3252000,
            1869: 1604000, 1870: 1335000, 1871: 604000, 1872: 862000,
            1873: 1173000, 1874: 700000, 1875: 228000, 1876: 162000,
            1877: 0,  # Proof only
            1878: 0,  # Proof only
            1879: 41000, 1880: 24000, 1881: 1077000, 1882: 25300,
            1883: 10609, 1884: 5642, 1885: 4790, 1886: 4290,
            1887: 5001, 1888: 41083, 1889: 21561
        }
        
        for year, mintage in mintages.items():
            # Determine rarity
            if year in [1877, 1878]:  # Proof only years
                rarity = "key"
                business = 0
                proof = 900 if year == 1877 else 2350
            elif year >= 1879:
                rarity = "key" 
                business = mintage
                proof = 0
            elif mintage < 500000:
                rarity = "scarce"
                business = mintage
                proof = 0
            else:
                rarity = "common"
                business = mintage 
                proof = 0
            
            coins.append({
                "coin_id": f"US-TCNT-{year}-P",
                "series_id": "us-three-cent-nickel",
                "series_name": "Nickel Three-Cent",
                "year": year, 
                "mint": "P",
                "business_strikes": business,
                "proof_strikes": proof,
                "rarity": rarity,
                "composition": {"copper": 75.0, "nickel": 25.0},
                "weight_grams": 1.94,
                "diameter_mm": 17.9,
                "type": "Nickel",
                "note": "75% copper, 25% nickel composition"
            })
            
        return coins
    
    def build_full_coin_record(self, coin_data: Dict) -> Dict:
        """Build complete coin record with all required fields."""
        series_type = coin_data["type"]
        
        # Build obverse/reverse descriptions
        if "Silver" in coin_data["series_name"]:
            obverse = f"Shield with 13 stars around, date below. {coin_data['note']}"
            reverse = "Large Roman numeral III within ornate 'C', 'UNITED STATES OF AMERICA' around"
        else:
            obverse = "Liberty head facing left, coronet inscribed 'LIBERTY', date below"
            reverse = "Large Roman numeral III within wreath, 'UNITED STATES OF AMERICA' around"
        
        # Build features and keywords
        features = [
            f"{series_type} composition",
            f"Diameter: {coin_data['diameter_mm']}mm",
            f"Weight: {coin_data['weight_grams']}g",
            coin_data["note"],
            "Unique three-cent denomination"
        ]
        
        keywords = [
            "three cent", "3 cent", coin_data["series_name"].lower(),
            f"{coin_data['year']} three cent", "trime" if "Silver" in coin_data["series_name"] else "nickel three cent"
        ]
        
        if "Silver" in coin_data["series_name"]:
            keywords.extend(["silver", "trime", "3cs"])
        else:
            keywords.extend(["nickel", "3cn"])
            
        common_names = [
            coin_data["series_name"],
            f"{coin_data['year']} Three-Cent",
            "Trime" if "Silver" in coin_data["series_name"] else "Nickel Three-Cent"
        ]
        
        return {
            "coin_id": coin_data["coin_id"],
            "year": coin_data["year"],
            "mint": coin_data["mint"], 
            "denomination": "Three Cents",
            "series": coin_data["series_name"],
            "variety": coin_data["type"],
            "business_strikes": coin_data["business_strikes"],
            "proof_strikes": coin_data["proof_strikes"],
            "rarity": coin_data["rarity"],
            "composition": json.dumps(coin_data["composition"]),
            "weight_grams": coin_data["weight_grams"],
            "diameter_mm": coin_data["diameter_mm"],
            "obverse_description": obverse,
            "reverse_description": reverse,
            "notes": coin_data["note"],
            "source_citation": "Red Book 2025, PCGS CoinFacts"
        }
    
    def insert_coins(self, coins: List[Dict]) -> int:
        """Insert coins into database."""
        if self.dry_run:
            print(f"\n🔍 DRY RUN: Would insert {len(coins)} coins")
            for coin in coins[:5]:
                print(f"   - {coin['coin_id']}: {coin['series']} ({coin['year']})")
            if len(coins) > 5:
                print(f"   ... and {len(coins) - 5} more")
            return len(coins)
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        inserted = 0
        skipped = 0
        
        for coin in coins:
            try:
                cursor.execute("""
                    INSERT INTO coins (
                        coin_id, year, mint, denomination, series, variety,
                        business_strikes, proof_strikes, rarity, composition,
                        weight_grams, diameter_mm, obverse_description,
                        reverse_description, notes, source_citation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    coin['coin_id'], coin['year'], coin['mint'], coin['denomination'],
                    coin['series'], coin['variety'], coin['business_strikes'],
                    coin['proof_strikes'], coin['rarity'], coin['composition'],
                    coin['weight_grams'], coin['diameter_mm'], coin['obverse_description'],
                    coin['reverse_description'], coin['notes'], coin['source_citation']
                ))
                inserted += 1
                
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    skipped += 1
                else:
                    print(f"❌ Error inserting {coin['coin_id']}: {e}")
                
        conn.commit()
        conn.close()
        
        print(f"✅ Inserted {inserted} coins")
        if skipped > 0:
            print(f"⚠️  Skipped {skipped} existing coins")
            
        return inserted
    
    def run_migration(self):
        """Execute the migration."""
        print("\n🪙  THREE-CENT PIECES MIGRATION (1851-1889)")
        print("=" * 60)
        
        self.create_backup()
        
        print("\n📊 Preparing Three-Cent Pieces data...")
        
        # Get silver three-cents
        silver_coins_data = self.get_silver_three_cents()
        silver_coins = [self.build_full_coin_record(coin) for coin in silver_coins_data]
        
        # Get nickel three-cents  
        nickel_coins_data = self.get_nickel_three_cents()
        nickel_coins = [self.build_full_coin_record(coin) for coin in nickel_coins_data]
        
        all_coins = silver_coins + nickel_coins
        
        print(f"   • Silver Three-Cent: {len(silver_coins)} coins (1851-1873)")
        print(f"   • Nickel Three-Cent: {len(nickel_coins)} coins (1865-1889)")
        print(f"   • Total Three-Cent Pieces: {len(all_coins)} coins")
        
        print("\n💾 Inserting coins...")
        total_inserted = self.insert_coins(all_coins)
        
        print(f"\n✅ MIGRATION COMPLETE: {total_inserted} Three-Cent Pieces added")
        
        if not self.dry_run:
            print("\n📝 Next steps:")
            print("   1. Run: uv run python scripts/export_from_database.py")
            print("   2. Commit: git add . && git commit -m 'Add Three-Cent Pieces (Issue #50)'")
        
        return total_inserted


def main():
    parser = argparse.ArgumentParser(description='Add Three-Cent Pieces (1851-1889)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without modifying database')
    args = parser.parse_args()
    
    migration = ThreeCentPiecesMigration(dry_run=args.dry_run)
    migration.run_migration()


if __name__ == "__main__":
    main()