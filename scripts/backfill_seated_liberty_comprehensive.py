#!/usr/bin/env python3
"""
Comprehensive Backfill: Seated Liberty Series & Liberty Head Nickels
Based on market evidence and expert recommendations from Issue #8

Priority order (based on active listings):
1. Seated Liberty Half Dollars - 5 active listings
2. Seated Liberty Dimes - 2 active listings  
3. Liberty Head Nickels - 2 active listings (bulk collection)
4. Seated Liberty Dollars - 1 active listing
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import argparse

class SeatedLibertyBackfill:
    def __init__(self, db_path='database/coins.db', dry_run=False):
        self.db_path = db_path
        self.dry_run = dry_run
        self.backup_path = None
        
    def create_backup(self):
        """Create database backup before migration."""
        if self.dry_run:
            print("🔍 DRY RUN: Would create backup")
            return
            
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_seated_liberty_backup_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✅ Backup created: {self.backup_path}")
    
    def get_seated_liberty_half_dollars(self) -> List[Dict]:
        """Seated Liberty Half Dollars (1839-1891) - HIGHEST PRIORITY: 5 active listings"""
        coins = []
        
        # Key dates and varieties based on market demand
        key_years = {
            1839: {"rarity": "scarce", "strikes": 1435400, "note": "First year of type, No Drapery"},
            1840: {"rarity": "common", "strikes": 1435400, "note": "Small Letters variety"},
            1841: {"rarity": "common", "strikes": 310000},
            1842: {"rarity": "scarce", "strikes": 2012764, "note": "Small Date and Medium Date varieties"},
            1844: {"rarity": "scarce", "strikes": 2005000, "note": "O mint mark varieties"},
            1845: {"rarity": "common", "strikes": 589000},
            1846: {"rarity": "common", "strikes": 2210000, "note": "Medium Date variety"},
            1847: {"rarity": "common", "strikes": 1156000},
            1850: {"rarity": "common", "strikes": 227000},
            1851: {"rarity": "common", "strikes": 200750},
            1852: {"rarity": "scarce", "strikes": 77130, "note": "Low mintage"},
            1853: {"rarity": "key", "strikes": 3532708, "note": "Arrows and Rays variety"},
            1854: {"rarity": "common", "strikes": 2982000, "note": "Arrows variety"},
            1855: {"rarity": "scarce", "strikes": 759500, "note": "Last year with Arrows"},
            1856: {"rarity": "common", "strikes": 938000},
            1857: {"rarity": "common", "strikes": 1988000},
            1858: {"rarity": "common", "strikes": 4226000},
            1859: {"rarity": "common", "strikes": 748000},
            1860: {"rarity": "common", "strikes": 302700},
            1861: {"rarity": "common", "strikes": 2887400},
            1866: {"rarity": "key", "strikes": 744900, "note": "With Motto, first year"},
            1867: {"rarity": "scarce", "strikes": 449300},
            1868: {"rarity": "common", "strikes": 417600},
            1869: {"rarity": "common", "strikes": 795300},
            1870: {"rarity": "scarce", "strikes": 633900, "note": "CC mint mark key date"},
            1871: {"rarity": "common", "strikes": 1203600},
            1872: {"rarity": "common", "strikes": 880600},
            1873: {"rarity": "scarce", "strikes": 801800, "note": "Closed 3 and Open 3 varieties"},
            1874: {"rarity": "scarce", "strikes": 2359600, "note": "Arrows variety"},
            1875: {"rarity": "common", "strikes": 6026800},
            1876: {"rarity": "common", "strikes": 8418000},
            1877: {"rarity": "common", "strikes": 8304000},
            1878: {"rarity": "key", "strikes": 1377600, "note": "Low mintage key date"},
            1879: {"rarity": "key", "strikes": 4800, "note": "Extremely low mintage"},
            1880: {"rarity": "scarce", "strikes": 8400},
            1881: {"rarity": "scarce", "strikes": 10000},
            1882: {"rarity": "scarce", "strikes": 4400},
            1883: {"rarity": "scarce", "strikes": 8000},
            1884: {"rarity": "scarce", "strikes": 4400},
            1885: {"rarity": "scarce", "strikes": 5200},
            1886: {"rarity": "scarce", "strikes": 5000},
            1887: {"rarity": "scarce", "strikes": 5000},
            1888: {"rarity": "scarce", "strikes": 12001},
            1889: {"rarity": "scarce", "strikes": 12000},
            1890: {"rarity": "scarce", "strikes": 12000},
            1891: {"rarity": "common", "strikes": 200000, "note": "Last year of series"}
        }
        
        for year, info in key_years.items():
            coin = {
                "coin_id": f"US-SLHD-{year}-P",
                "series_id": "seated_liberty_half_dollar",
                "country": "US",
                "denomination": "Half Dollars",
                "series_name": "Seated Liberty Half Dollar",
                "year": year,
                "mint": "P",
                "business_strikes": info["strikes"],
                "proof_strikes": 0,
                "rarity": info["rarity"],
                "composition": json.dumps({"silver": 0.90, "copper": 0.10}),
                "weight_grams": 12.44,
                "diameter_mm": 30.6,
                "varieties": json.dumps([]),
                "source_citation": "Red Book 2024, PCGS CoinFacts",
                "notes": info.get("note", ""),
                "obverse_description": "Seated figure of Liberty holding pole with liberty cap in left hand and shield with 'LIBERTY' inscription in right hand, surrounded by 13 stars, date below",
                "reverse_description": "Heraldic eagle with spread wings holding arrows and olive branch, shield on breast, 'UNITED STATES OF AMERICA' above, 'HALF DOL.' below",
                "distinguishing_features": json.dumps([
                    "Christian Gobrecht design",
                    "90% silver composition",
                    "30.6mm diameter",
                    "Reeded edge",
                    "Liberty seated on rock",
                    "Shield with LIBERTY inscription",
                    info.get("note", "Standard design")
                ]),
                "identification_keywords": json.dumps([
                    "seated liberty", "half dollar", f"{year} half", "silver half",
                    "seated half", "liberty seated", "50 cents", "gobrecht design",
                    "arrows" if "Arrows" in info.get("note", "") else "no arrows",
                    "rays" if "Rays" in info.get("note", "") else "no rays"
                ]),
                "common_names": json.dumps([
                    "Seated Liberty Half Dollar",
                    f"{year} Seated Half",
                    "Liberty Seated Half"
                ])
            }
            coins.append(coin)
            
        return coins
    
    def get_seated_liberty_dimes(self) -> List[Dict]:
        """Seated Liberty Dimes (1837-1891) - Priority 2: 2 active listings"""
        coins = []
        
        key_years = {
            1837: {"rarity": "common", "strikes": 682500, "note": "First year, No Stars variety"},
            1838: {"rarity": "common", "strikes": 1992500, "note": "Stars added to obverse"},
            1840: {"rarity": "common", "strikes": 1358580, "note": "No Drapery variety"},
            1841: {"rarity": "common", "strikes": 1622500},
            1842: {"rarity": "common", "strikes": 1887500},
            1843: {"rarity": "common", "strikes": 1370000},
            1844: {"rarity": "scarce", "strikes": 72500, "note": "Low mintage"},
            1845: {"rarity": "common", "strikes": 1755000},
            1846: {"rarity": "scarce", "strikes": 31300, "note": "Very low mintage"},
            1847: {"rarity": "common", "strikes": 451500},
            1848: {"rarity": "common", "strikes": 451000},
            1849: {"rarity": "common", "strikes": 839000},
            1850: {"rarity": "common", "strikes": 1931500},
            1851: {"rarity": "common", "strikes": 1026500},
            1852: {"rarity": "common", "strikes": 1535500},
            1853: {"rarity": "common", "strikes": 12078010, "note": "With Arrows variety"},
            1854: {"rarity": "common", "strikes": 4470000},
            1855: {"rarity": "common", "strikes": 2075000, "note": "Last year with Arrows"},
            1856: {"rarity": "common", "strikes": 5780000},
            1858: {"rarity": "common", "strikes": 1540000},
            1859: {"rarity": "common", "strikes": 430000},
            1860: {"rarity": "common", "strikes": 606000, "note": "O mint available"},
            1861: {"rarity": "common", "strikes": 1883700},
            1863: {"rarity": "scarce", "strikes": 14000, "note": "Civil War low mintage"},
            1864: {"rarity": "scarce", "strikes": 11000, "note": "Civil War low mintage"},
            1865: {"rarity": "scarce", "strikes": 10000},
            1866: {"rarity": "scarce", "strikes": 8000},
            1867: {"rarity": "scarce", "strikes": 6000},
            1868: {"rarity": "common", "strikes": 464600},
            1869: {"rarity": "common", "strikes": 256600},
            1870: {"rarity": "common", "strikes": 470500},
            1871: {"rarity": "common", "strikes": 906750, "note": "CC mint available"},
            1872: {"rarity": "common", "strikes": 2395500},
            1873: {"rarity": "common", "strikes": 2377700, "note": "Closed 3 and Open 3"},
            1874: {"rarity": "common", "strikes": 2940000, "note": "With Arrows"},
            1875: {"rarity": "common", "strikes": 10350000},
            1876: {"rarity": "common", "strikes": 11450000},
            1877: {"rarity": "common", "strikes": 7310000},
            1878: {"rarity": "common", "strikes": 1677200},
            1879: {"rarity": "scarce", "strikes": 14000},
            1880: {"rarity": "scarce", "strikes": 36963},
            1881: {"rarity": "scarce", "strikes": 24000},
            1882: {"rarity": "common", "strikes": 3910000},
            1883: {"rarity": "common", "strikes": 7674673},
            1884: {"rarity": "common", "strikes": 3365505},
            1885: {"rarity": "common", "strikes": 2532497},
            1886: {"rarity": "common", "strikes": 6376684},
            1887: {"rarity": "common", "strikes": 11283229},
            1888: {"rarity": "common", "strikes": 5495655},
            1889: {"rarity": "common", "strikes": 7380000},
            1890: {"rarity": "common", "strikes": 9910951},
            1891: {"rarity": "common", "strikes": 15310000, "note": "Last year of series"}
        }
        
        for year, info in key_years.items():
            coin = {
                "coin_id": f"US-SLDI-{year}-P",
                "series_id": "seated_liberty_dime",
                "country": "US",
                "denomination": "Dimes",
                "series_name": "Seated Liberty Dime",
                "year": year,
                "mint": "P",
                "business_strikes": info["strikes"],
                "proof_strikes": 0,
                "rarity": info["rarity"],
                "composition": json.dumps({"silver": 0.90, "copper": 0.10}),
                "weight_grams": 2.49,
                "diameter_mm": 17.9,
                "varieties": json.dumps([]),
                "source_citation": "Red Book 2024, PCGS CoinFacts",
                "notes": info.get("note", ""),
                "obverse_description": "Seated figure of Liberty holding pole with liberty cap in left hand and shield in right hand, 13 stars around border, date below",
                "reverse_description": "Denomination 'ONE DIME' within wreath of laurel and agricultural products, 'UNITED STATES OF AMERICA' around",
                "distinguishing_features": json.dumps([
                    "Christian Gobrecht design",
                    "90% silver composition", 
                    "17.9mm diameter",
                    "Reeded edge",
                    "Liberty seated on rock",
                    info.get("note", "Standard design")
                ]),
                "identification_keywords": json.dumps([
                    "seated liberty", "dime", f"{year} dime", "silver dime",
                    "seated dime", "liberty seated", "10 cents", "one dime",
                    "arrows" if "Arrows" in info.get("note", "") else "no arrows"
                ]),
                "common_names": json.dumps([
                    "Seated Liberty Dime",
                    f"{year} Seated Dime",
                    "Liberty Seated Dime"
                ])
            }
            coins.append(coin)
            
        return coins
    
    def get_liberty_head_nickels(self) -> List[Dict]:
        """Liberty Head Nickels (1883-1913) - Priority 3: 2 active listings including bulk"""
        coins = []
        
        key_years = {
            1883: {"rarity": "key", "strikes": 5474300, "note": "No CENTS variety first"},
            1884: {"rarity": "scarce", "strikes": 11270000},
            1885: {"rarity": "key", "strikes": 1472700, "note": "Key date"},
            1886: {"rarity": "key", "strikes": 3326000, "note": "Key date"},
            1887: {"rarity": "common", "strikes": 15260692},
            1888: {"rarity": "common", "strikes": 10167901},
            1889: {"rarity": "common", "strikes": 15878025},
            1890: {"rarity": "common", "strikes": 16256532},
            1891: {"rarity": "common", "strikes": 16832000},
            1892: {"rarity": "common", "strikes": 11696897},
            1893: {"rarity": "common", "strikes": 13368000},
            1894: {"rarity": "common", "strikes": 5410500},
            1895: {"rarity": "common", "strikes": 9977822},
            1896: {"rarity": "common", "strikes": 8841058},
            1897: {"rarity": "common", "strikes": 20426797},
            1898: {"rarity": "common", "strikes": 12530292},
            1899: {"rarity": "common", "strikes": 26027000},
            1900: {"rarity": "common", "strikes": 27253733},
            1901: {"rarity": "common", "strikes": 26478228},
            1902: {"rarity": "common", "strikes": 31487581},
            1903: {"rarity": "common", "strikes": 28004935},
            1904: {"rarity": "common", "strikes": 21403167},
            1905: {"rarity": "common", "strikes": 29825124},
            1906: {"rarity": "common", "strikes": 38612000},
            1907: {"rarity": "common", "strikes": 39213325},
            1908: {"rarity": "common", "strikes": 22684557},
            1909: {"rarity": "common", "strikes": 11585763},
            1910: {"rarity": "common", "strikes": 30166948},
            1911: {"rarity": "common", "strikes": 39557639},
            1912: {"rarity": "common", "strikes": 26234569, "note": "D and S mints added"},
            1913: {"rarity": "key", "strikes": 5, "note": "Ultra rare, only 5 known"}
        }
        
        for year, info in key_years.items():
            coin = {
                "coin_id": f"US-LNIC-{year}-P",
                "series_id": "liberty_head_nickel",
                "country": "US",
                "denomination": "Nickels",
                "series_name": "Liberty Head Nickel",
                "year": year,
                "mint": "P",
                "business_strikes": info["strikes"],
                "proof_strikes": 0,
                "rarity": info["rarity"],
                "composition": json.dumps({"copper": 0.75, "nickel": 0.25}),
                "weight_grams": 5.0,
                "diameter_mm": 21.2,
                "varieties": json.dumps([]),
                "source_citation": "Red Book 2024, PCGS CoinFacts",
                "notes": info.get("note", ""),
                "obverse_description": "Liberty head facing left wearing coronet inscribed 'LIBERTY', 13 stars around border, date below",
                "reverse_description": "Large Roman numeral V (5) at center surrounded by wreath of cotton and corn, 'UNITED STATES OF AMERICA' above, 'CENTS' below (except 1883 No CENTS)",
                "distinguishing_features": json.dumps([
                    "Charles E. Barber design",
                    "75% copper, 25% nickel composition",
                    "21.2mm diameter",
                    "Plain edge",
                    "Also known as V Nickel",
                    info.get("note", "With CENTS variety")
                ]),
                "identification_keywords": json.dumps([
                    "liberty head", "nickel", f"{year} nickel", "v nickel",
                    "liberty nickel", "five cents", "barber nickel",
                    "no cents" if "No CENTS" in info.get("note", "") else "with cents"
                ]),
                "common_names": json.dumps([
                    "Liberty Head Nickel",
                    "V Nickel",
                    f"{year} Liberty Nickel"
                ])
            }
            coins.append(coin)
            
        return coins
    
    def get_seated_liberty_dollars(self) -> List[Dict]:
        """Seated Liberty Dollars (1840-1873) - Priority 4: 1 active listing"""
        coins = []
        
        key_years = {
            1840: {"rarity": "common", "strikes": 61005, "note": "First year of series"},
            1841: {"rarity": "common", "strikes": 173000},
            1842: {"rarity": "common", "strikes": 184618},
            1843: {"rarity": "common", "strikes": 165100},
            1844: {"rarity": "scarce", "strikes": 20000},
            1845: {"rarity": "scarce", "strikes": 24500},
            1846: {"rarity": "common", "strikes": 110600},
            1847: {"rarity": "common", "strikes": 140750},
            1848: {"rarity": "scarce", "strikes": 15000},
            1849: {"rarity": "common", "strikes": 62600},
            1850: {"rarity": "scarce", "strikes": 7500},
            1851: {"rarity": "key", "strikes": 1300, "note": "Key date, very low mintage"},
            1852: {"rarity": "key", "strikes": 1100, "note": "Key date, extremely low mintage"},
            1853: {"rarity": "scarce", "strikes": 46110},
            1854: {"rarity": "scarce", "strikes": 33140},
            1855: {"rarity": "scarce", "strikes": 26000},
            1856: {"rarity": "scarce", "strikes": 63500},
            1857: {"rarity": "scarce", "strikes": 94000},
            1858: {"rarity": "key", "strikes": 0, "note": "Proof only, about 300 made"},
            1859: {"rarity": "common", "strikes": 255700},
            1860: {"rarity": "common", "strikes": 217600, "note": "O mint available"},
            1861: {"rarity": "scarce", "strikes": 77500},
            1862: {"rarity": "scarce", "strikes": 11540},
            1863: {"rarity": "scarce", "strikes": 27200},
            1864: {"rarity": "scarce", "strikes": 30700},
            1865: {"rarity": "scarce", "strikes": 46500},
            1866: {"rarity": "scarce", "strikes": 48900, "note": "With Motto added"},
            1867: {"rarity": "scarce", "strikes": 46900},
            1868: {"rarity": "scarce", "strikes": 162100},
            1869: {"rarity": "common", "strikes": 423700},
            1870: {"rarity": "common", "strikes": 415000, "note": "CC mint key date"},
            1871: {"rarity": "common", "strikes": 1073800},
            1872: {"rarity": "common", "strikes": 1105500},
            1873: {"rarity": "common", "strikes": 293000, "note": "Last year, Closed 3 variety"}
        }
        
        for year, info in key_years.items():
            if info["strikes"] == 0 and "Proof only" in info.get("note", ""):
                continue  # Skip proof-only years for regular strikes
                
            coin = {
                "coin_id": f"US-SLDL-{year}-P",
                "series_id": "seated_liberty_dollar",
                "country": "US",
                "denomination": "Dollars",
                "series_name": "Seated Liberty Dollar",
                "year": year,
                "mint": "P",
                "business_strikes": info["strikes"],
                "proof_strikes": 0,
                "rarity": info["rarity"],
                "composition": json.dumps({"silver": 0.90, "copper": 0.10}),
                "weight_grams": 26.73,
                "diameter_mm": 38.1,
                "varieties": json.dumps([]),
                "source_citation": "Red Book 2024, PCGS CoinFacts",
                "notes": info.get("note", ""),
                "obverse_description": "Seated figure of Liberty holding pole with liberty cap in left hand and shield with 'LIBERTY' inscription in right hand, 13 stars around border, date below",
                "reverse_description": "Heraldic eagle with spread wings holding arrows in right talon and olive branch in left, shield on breast, 'UNITED STATES OF AMERICA' above, 'ONE DOL.' below",
                "distinguishing_features": json.dumps([
                    "Christian Gobrecht design",
                    "90% silver composition",
                    "38.1mm diameter",
                    "Reeded edge",
                    "Liberty seated on rock",
                    "Largest regular issue silver coin",
                    info.get("note", "Standard design")
                ]),
                "identification_keywords": json.dumps([
                    "seated liberty", "dollar", f"{year} dollar", "silver dollar",
                    "seated dollar", "liberty seated", "one dollar", "gobrecht design",
                    "motto" if "Motto" in info.get("note", "") else "no motto"
                ]),
                "common_names": json.dumps([
                    "Seated Liberty Dollar",
                    f"{year} Seated Dollar",
                    "Liberty Seated Dollar"
                ])
            }
            coins.append(coin)
            
        return coins
    
    def insert_coins(self, coins: List[Dict]) -> int:
        """Insert coins into database."""
        if self.dry_run:
            print(f"\n🔍 DRY RUN: Would insert {len(coins)} coins")
            for coin in coins[:5]:  # Show first 5 examples
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
                continue
                
        conn.commit()
        conn.close()
        
        print(f"✅ Inserted {inserted} coins")
        if skipped > 0:
            print(f"⚠️  Skipped {skipped} existing coins")
            
        return inserted
    
    def run_migration(self):
        """Execute the complete migration."""
        print("\n🏛️  SEATED LIBERTY & LIBERTY HEAD COMPREHENSIVE BACKFILL")
        print("=" * 60)
        
        # Create backup
        self.create_backup()
        
        # Get all coin data
        print("\n📊 Preparing coin data...")
        
        # Priority order based on market evidence
        seated_half_dollars = self.get_seated_liberty_half_dollars()
        print(f"   • Seated Liberty Half Dollars: {len(seated_half_dollars)} coins (5 active listings)")
        
        seated_dimes = self.get_seated_liberty_dimes()
        print(f"   • Seated Liberty Dimes: {len(seated_dimes)} coins (2 active listings)")
        
        liberty_nickels = self.get_liberty_head_nickels()
        print(f"   • Liberty Head Nickels: {len(liberty_nickels)} coins (2 active listings)")
        
        seated_dollars = self.get_seated_liberty_dollars()
        print(f"   • Seated Liberty Dollars: {len(seated_dollars)} coins (1 active listing)")
        
        # Insert in priority order
        print("\n💾 Inserting coins (priority order)...")
        
        total_inserted = 0
        total_inserted += self.insert_coins(seated_half_dollars)
        total_inserted += self.insert_coins(seated_dimes)
        total_inserted += self.insert_coins(liberty_nickels)
        total_inserted += self.insert_coins(seated_dollars)
        
        print(f"\n✅ MIGRATION COMPLETE: {total_inserted} total coins added")
        
        if not self.dry_run:
            print("\n📝 Next steps:")
            print("   1. Run: uv run python scripts/export_from_database.py")
            print("   2. Verify exports")
            print("   3. Commit: git add . && git commit -m '🏛️ Add Seated Liberty & Liberty Head series'")
        
        return total_inserted


def main():
    parser = argparse.ArgumentParser(description='Backfill Seated Liberty and Liberty Head series')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying database')
    args = parser.parse_args()
    
    backfill = SeatedLibertyBackfill(dry_run=args.dry_run)
    backfill.run_migration()


if __name__ == "__main__":
    main()