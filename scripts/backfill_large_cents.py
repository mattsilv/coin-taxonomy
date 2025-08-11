#!/usr/bin/env python3
"""
Large Cents Backfill (1793-1857)
Foundation series for early American coinage - critical for pattern recognition
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List
import argparse

class LargeCentsBackfill:
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
        backup_path = f"{backup_dir}/coins_large_cents_backup_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ Backup created: {backup_path}")
    
    def get_large_cents(self) -> List[Dict]:
        """Get all Large Cent varieties (1793-1857)"""
        coins = []
        
        # Flowing Hair (1793)
        coins.extend([
            {"coin_id": "US-LCHN-1793-P", "series_id": "large_cent_chain", "series_name": "Chain Cent",
             "year": 1793, "strikes": 36103, "rarity": "key", 
             "note": "First U.S. cent, AMERI. variety", "designer": "Henry Voigt"},
            {"coin_id": "US-LWRE-1793-P", "series_id": "large_cent_wreath", "series_name": "Wreath Cent",
             "year": 1793, "strikes": 63353, "rarity": "key",
             "note": "Vine and bars edge", "designer": "Adam Eckfeldt"},
            {"coin_id": "US-LLBC-1793-P", "series_id": "large_cent_liberty_cap", "series_name": "Liberty Cap Cent",
             "year": 1793, "strikes": 11056, "rarity": "key",
             "note": "Head of 1793", "designer": "Joseph Wright"}
        ])
        
        # Liberty Cap (1793-1796)
        for year in [1794, 1795, 1796]:
            strikes = {1794: 918521, 1795: 37000, 1796: 109825}
            coins.append({
                "coin_id": f"US-LLBC-{year}-P", "series_id": "large_cent_liberty_cap",
                "series_name": "Liberty Cap Cent", "year": year, "strikes": strikes[year],
                "rarity": "scarce", "note": f"Head of {year-1 if year == 1794 else year}",
                "designer": "Joseph Wright"
            })
        
        # Draped Bust (1796-1807)
        draped_years = {
            1796: 363375, 1797: 897510, 1798: 1841745, 1799: 904585, 1800: 2822175,
            1801: 1362837, 1802: 3435100, 1803: 3131691, 1804: 756838, 1805: 941116,
            1806: 348000, 1807: 829221
        }
        for year, strikes in draped_years.items():
            coins.append({
                "coin_id": f"US-DRPB-{year}-P", "series_id": "large_cent_draped_bust",
                "series_name": "Draped Bust Cent", "year": year, "strikes": strikes,
                "rarity": "scarce" if year in [1799, 1804] else "common",
                "note": "S-1 variety" if year == 1799 else "", "designer": "Robert Scot"
            })
        
        # Classic Head (1808-1814)
        classic_years = {
            1808: 1007000, 1809: 222867, 1810: 1458500, 1811: 218025,
            1812: 1075500, 1813: 418000, 1814: 357830
        }
        for year, strikes in classic_years.items():
            coins.append({
                "coin_id": f"US-CLHC-{year}-P", "series_id": "large_cent_classic_head",
                "series_name": "Classic Head Cent", "year": year, "strikes": strikes,
                "rarity": "common", "note": "", "designer": "John Reich"
            })
        
        # Coronet/Mature Head (1816-1857)
        coronet_years = {
            1816: 2820982, 1817: 3948400, 1818: 3167000, 1819: 2671000, 1820: 4407550,
            1821: 389000, 1822: 2072339, 1823: 855730, 1824: 1262000, 1825: 1461100,
            1826: 1517425, 1827: 2357732, 1828: 2260624, 1829: 1414500, 1830: 1711500,
            1831: 3359260, 1832: 2362000, 1833: 2739000, 1834: 1855100, 1835: 3878400,
            1836: 2111000, 1837: 5558300, 1838: 6370200, 1839: 3128661, 1840: 2462700,
            1841: 1597367, 1842: 2383390, 1843: 2425342, 1844: 2398752, 1845: 3894804,
            1846: 4120800, 1847: 6183669, 1848: 6415799, 1849: 4178500, 1850: 4426844,
            1851: 9889707, 1852: 5063094, 1853: 6641131, 1854: 4236156, 1855: 1574829,
            1856: 2690463, 1857: 333456
        }
        
        for year, strikes in coronet_years.items():
            rarity = "key" if year in [1821, 1823, 1857] else "scarce" if year < 1835 else "common"
            designer = "Robert Scot" if year <= 1835 else "Christian Gobrecht"
            note = "Small date" if year == 1857 else "Young Head" if year <= 1835 else "Mature Head"
            
            coins.append({
                "coin_id": f"US-CORL-{year}-P", "series_id": "large_cent_coronet",
                "series_name": "Coronet Cent", "year": year, "strikes": strikes,
                "rarity": rarity, "note": note, "designer": designer
            })
        
        # Build full coin records
        full_coins = []
        for coin_data in coins:
            full_coin = {
                "coin_id": coin_data["coin_id"],
                "series_id": coin_data["series_id"],
                "country": "US",
                "denomination": "Cents",
                "series_name": coin_data["series_name"],
                "year": coin_data["year"],
                "mint": "P",
                "business_strikes": coin_data["strikes"],
                "proof_strikes": 0,
                "rarity": coin_data["rarity"],
                "composition": json.dumps({"copper": 1.0}),
                "weight_grams": 13.48 if coin_data["year"] < 1795 else 10.89,
                "diameter_mm": 27 if coin_data["year"] < 1796 else 29,
                "varieties": json.dumps([]),
                "source_citation": "Red Book 2024, Sheldon Large Cent Attribution",
                "notes": coin_data["note"],
                "obverse_description": self.get_obverse_description(coin_data["series_name"], coin_data["year"]),
                "reverse_description": self.get_reverse_description(coin_data["series_name"], coin_data["year"]),
                "distinguishing_features": json.dumps(self.get_features(coin_data)),
                "identification_keywords": json.dumps(self.get_keywords(coin_data)),
                "common_names": json.dumps([
                    coin_data["series_name"],
                    f"{coin_data['year']} Large Cent",
                    "Penny" if coin_data["year"] > 1850 else "Cent"
                ])
            }
            full_coins.append(full_coin)
            
        return full_coins
    
    def get_obverse_description(self, series: str, year: int) -> str:
        """Get appropriate obverse description by series."""
        descriptions = {
            "Chain Cent": "Liberty head with flowing hair facing right, 'LIBERTY' above, date below",
            "Wreath Cent": "Liberty head with flowing hair facing right, 'LIBERTY' above, date below",
            "Liberty Cap Cent": "Liberty head facing right wearing liberty cap, 'LIBERTY' above, date below",
            "Draped Bust Cent": "Draped bust of Liberty facing right with flowing hair, 'LIBERTY' above, date below",
            "Classic Head Cent": "Liberty head facing left with band inscribed 'LIBERTY', 13 stars around, date below",
            "Coronet Cent": "Liberty head facing left wearing coronet inscribed 'LIBERTY', 13 stars around, date below"
        }
        return descriptions.get(series, "Liberty head design with date")
    
    def get_reverse_description(self, series: str, year: int) -> str:
        """Get appropriate reverse description by series."""
        descriptions = {
            "Chain Cent": "Chain with 15 links encircling 'ONE CENT', fraction '1/100' below, 'UNITED STATES OF AMERICA' around",
            "Wreath Cent": "Wreath encircling 'ONE CENT', fraction '1/100' below, 'UNITED STATES OF AMERICA' around edge",
            "Liberty Cap Cent": "Wreath encircling 'ONE CENT', 'UNITED STATES OF AMERICA' around",
            "Draped Bust Cent": "Wreath encircling 'ONE CENT', fraction '1/100' below, 'UNITED STATES OF AMERICA' around",
            "Classic Head Cent": "Continuous wreath encircling 'ONE CENT', 'UNITED STATES OF AMERICA' around",
            "Coronet Cent": "Wreath encircling 'ONE CENT', 'UNITED STATES OF AMERICA' around"
        }
        return descriptions.get(series, "Wreath design with denomination")
    
    def get_features(self, coin_data: Dict) -> List[str]:
        """Get distinguishing features for the coin."""
        features = [
            f"{coin_data['designer']} design" if coin_data.get('designer') else "Classic design",
            "100% copper composition",
            "Large copper coin (27-29mm)",
            "Plain edge" if coin_data["year"] < 1794 else "Lettered edge" if coin_data["year"] == 1793 else "Plain edge",
            coin_data["note"] if coin_data["note"] else f"{coin_data['series_name']} type"
        ]
        
        if coin_data["year"] == 1793:
            features.append("First year of U.S. coinage")
        elif coin_data["year"] == 1857:
            features.append("Last year of large cents")
            
        return features
    
    def get_keywords(self, coin_data: Dict) -> List[str]:
        """Get identification keywords for the coin."""
        keywords = [
            "large cent", coin_data["series_name"].lower(), f"{coin_data['year']} cent",
            "copper cent", "penny", "one cent"
        ]
        
        if "Chain" in coin_data["series_name"]:
            keywords.extend(["chain cent", "chain reverse", "flowing hair"])
        elif "Wreath" in coin_data["series_name"]:
            keywords.extend(["wreath cent", "wreath reverse"])
        elif "Liberty Cap" in coin_data["series_name"]:
            keywords.extend(["liberty cap", "cap cent"])
        elif "Draped" in coin_data["series_name"]:
            keywords.extend(["draped bust", "draped cent"])
        elif "Classic" in coin_data["series_name"]:
            keywords.extend(["classic head", "turban head"])
        elif "Coronet" in coin_data["series_name"]:
            keywords.extend(["coronet cent", "braided hair", "mature head" if coin_data["year"] > 1835 else "young head"])
            
        return keywords
    
    def insert_coins(self, coins: List[Dict]) -> int:
        """Insert coins into database."""
        if self.dry_run:
            print(f"\n🔍 DRY RUN: Would insert {len(coins)} coins")
            for coin in coins[:5]:
                print(f"   - {coin['coin_id']}: {coin['series_name']} ({coin['year']})")
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
                
            except sqlite3.IntegrityError:
                skipped += 1
                
        conn.commit()
        conn.close()
        
        print(f"✅ Inserted {inserted} coins")
        if skipped > 0:
            print(f"⚠️  Skipped {skipped} existing coins")
            
        return inserted
    
    def run_migration(self):
        """Execute the migration."""
        print("\n🪙  LARGE CENTS COMPREHENSIVE BACKFILL (1793-1857)")
        print("=" * 60)
        
        self.create_backup()
        
        print("\n📊 Preparing Large Cents data...")
        large_cents = self.get_large_cents()
        print(f"   • Total Large Cents: {len(large_cents)} coins (65 years)")
        
        # Count by series
        series_counts = {}
        for coin in large_cents:
            series = coin['series_name']
            series_counts[series] = series_counts.get(series, 0) + 1
        
        for series, count in series_counts.items():
            print(f"     - {series}: {count} coins")
        
        print("\n💾 Inserting coins...")
        total_inserted = self.insert_coins(large_cents)
        
        print(f"\n✅ MIGRATION COMPLETE: {total_inserted} Large Cents added")
        
        if not self.dry_run:
            print("\n📝 Next steps:")
            print("   1. Run: uv run python scripts/export_from_database.py")
            print("   2. Commit: git add . && git commit")
        
        return total_inserted


def main():
    parser = argparse.ArgumentParser(description='Backfill Large Cents (1793-1857)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without modifying database')
    args = parser.parse_args()
    
    backfill = LargeCentsBackfill(dry_run=args.dry_run)
    backfill.run_migration()


if __name__ == "__main__":
    main()