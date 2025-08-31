#!/usr/bin/env python3
"""
Import Canada coins into the database.
This script covers all three phases of Canada coin imports:
- Phase 1: Historical coins (1858-1967)
- Phase 2: Modern circulation (1968-present)
- Phase 3: Bullion series
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any
import os

class CanadaCoinImporter:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def close(self):
        """Close database connection."""
        self.conn.close()
        
    def insert_coin(self, coin_data: Dict[str, Any]):
        """Insert a single coin into the database."""
        try:
            # Convert dictionaries to JSON strings
            composition = json.dumps(coin_data.get('composition', {}))
            varieties = json.dumps(coin_data.get('varieties', []))
            
            self.cursor.execute('''
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name,
                    year, mint, business_strikes, proof_strikes, rarity,
                    composition, weight_grams, diameter_mm, varieties,
                    source_citation, notes, obverse_description, reverse_description,
                    distinguishing_features, identification_keywords, common_names
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coin_data['coin_id'],
                coin_data['series_id'],
                'CA',  # Country code for Canada
                coin_data['denomination'],
                coin_data['series_name'],
                coin_data['year'],
                coin_data['mint'],
                coin_data.get('business_strikes'),
                coin_data.get('proof_strikes'),
                coin_data.get('rarity'),
                composition,
                coin_data.get('weight_grams'),
                coin_data.get('diameter_mm'),
                varieties,
                coin_data.get('source_citation', 'Issue #11 research'),
                coin_data.get('notes'),
                coin_data['obverse_description'],
                coin_data['reverse_description'],
                coin_data.get('distinguishing_features', ''),
                coin_data.get('identification_keywords', ''),
                coin_data.get('common_names', '')
            ))
            return True
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                print(f"   ⚠️  Coin already exists: {coin_data['coin_id']}")
            else:
                print(f"   ❌ Error inserting {coin_data['coin_id']}: {e}")
            return False
    
    def import_phase1_historical(self):
        """Import Phase 1: Historical coins (1858-1967)"""
        print("\n📊 Phase 1: Importing historical Canada coins (1858-1967)")
        
        coins = []
        
        # 1858 Provincial Coins
        coins.extend([
            {
                'coin_id': 'CA-CENT-1858-RM',
                'series_id': 'ca_large_cent',
                'denomination': 'Cents',
                'series_name': 'Large Cent',
                'year': 1858,
                'mint': 'RM',
                'business_strikes': 421000,
                'rarity': 'scarce',
                'composition': {'copper': 0.95, 'tin': 0.04, 'zinc': 0.01},
                'weight_grams': 4.54,
                'diameter_mm': 25.4,
                'obverse_description': 'Queen Victoria laureate bust left',
                'reverse_description': 'Two maple leaves on twig with denomination',
                'distinguishing_features': 'Large format cent',
                'identification_keywords': 'Victoria, maple leaves, large cent',
                'common_names': '1858 Large Cent',
                'varieties': [
                    {'name': 'Coin alignment', 'premium': True},
                    {'name': 'Full vine', 'premium': True},
                    {'name': 'Broken stem', 'premium': False}
                ]
            },
            {
                'coin_id': 'CA-FIVE-1858-RM',
                'series_id': 'ca_5c_silver',
                'denomination': 'Five Cents',
                'series_name': '5 Cents Silver',
                'year': 1858,
                'mint': 'RM',
                'rarity': 'scarce',
                'composition': {'silver': 0.925, 'copper': 0.075},
                'diameter_mm': 15.5,
                'obverse_description': 'Queen Victoria laureate bust left',
                'reverse_description': 'Two maple leaves with denomination',
                'identification_keywords': 'Victoria, maple leaves, silver',
                'common_names': '1858 Silver Five Cents'
            },
            {
                'coin_id': 'CA-DIME-1858-RM',
                'series_id': 'ca_10c_silver',
                'denomination': 'Ten Cents',
                'series_name': '10 Cents Silver',
                'year': 1858,
                'mint': 'RM',
                'rarity': 'scarce',
                'composition': {'silver': 0.925, 'copper': 0.075},
                'diameter_mm': 18.0,
                'obverse_description': 'Queen Victoria laureate bust left',
                'reverse_description': 'Two maple leaves with denomination',
                'identification_keywords': 'Victoria, maple leaves, silver',
                'common_names': '1858 Silver Ten Cents'
            },
            {
                'coin_id': 'CA-TWTY-1858-RM',
                'series_id': 'ca_20c',
                'denomination': 'Twenty Cents',
                'series_name': '20 Cents',
                'year': 1858,
                'mint': 'RM',
                'business_strikes': 730392,
                'rarity': 'scarce',
                'composition': {'silver': 0.925, 'copper': 0.075},
                'weight_grams': 4.648,
                'diameter_mm': 23.3,
                'obverse_description': 'Queen Victoria laureate bust left',
                'reverse_description': 'Two maple leaves with denomination',
                'distinguishing_features': 'Single year issue, discontinued due to confusion with US quarter',
                'identification_keywords': 'Victoria, maple leaves, twenty cents',
                'common_names': '1858 Twenty Cents',
                'notes': 'Only issued in 1858, replaced by 25-cent coin'
            }
        ])
        
        # Add some key Victoria era coins
        coins.extend([
            {
                'coin_id': 'CA-QRTR-1870-P',
                'series_id': 'ca_25c_victoria',
                'denomination': 'Twenty-Five Cents',
                'series_name': 'Victoria Quarter',
                'year': 1870,
                'mint': 'P',
                'rarity': 'common',
                'composition': {'silver': 0.925, 'copper': 0.075},
                'weight_grams': 5.81,
                'diameter_mm': 23.88,
                'obverse_description': 'Queen Victoria laureate bust left',
                'reverse_description': 'Crown and wreath design',
                'identification_keywords': 'Victoria, crown, wreath',
                'common_names': 'Victoria Quarter'
            },
            {
                'coin_id': 'CA-HALF-1870-P',
                'series_id': 'ca_50c_victoria',
                'denomination': 'Fifty Cents',
                'series_name': 'Victoria Half Dollar',
                'year': 1870,
                'mint': 'P',
                'rarity': 'common',
                'composition': {'silver': 0.925, 'copper': 0.075},
                'weight_grams': 11.62,
                'diameter_mm': 27.13,
                'obverse_description': 'Queen Victoria laureate bust left',
                'reverse_description': 'Canadian coat of arms',
                'identification_keywords': 'Victoria, coat of arms',
                'common_names': 'Victoria Half Dollar'
            }
        ])
        
        # Add key rarities
        coins.extend([
            {
                'coin_id': 'CA-FIVE-1921-P',
                'series_id': 'ca_5c_silver',
                'denomination': 'Five Cents',
                'series_name': '5 Cents Silver',
                'year': 1921,
                'mint': 'P',
                'business_strikes': 2582495,
                'rarity': 'key',
                'composition': {'silver': 0.80, 'copper': 0.20},
                'weight_grams': 1.16,
                'diameter_mm': 15.5,
                'obverse_description': 'King George V bust left',
                'reverse_description': 'Two maple leaves with denomination',
                'distinguishing_features': 'Prince of Canadian coins - most melted, <400 survive',
                'identification_keywords': 'George V, maple leaves, key date',
                'common_names': '1921 Silver Five Cents (Prince)',
                'notes': 'Most of mintage melted when nickel 5-cent introduced'
            },
            {
                'coin_id': 'CA-HALF-1921-P',
                'series_id': 'ca_50c_george_v',
                'denomination': 'Fifty Cents',
                'series_name': 'George V Half Dollar',
                'year': 1921,
                'mint': 'P',
                'business_strikes': 206398,
                'rarity': 'key',
                'composition': {'silver': 0.80, 'copper': 0.20},
                'weight_grams': 11.62,
                'diameter_mm': 27.13,
                'obverse_description': 'King George V bust left',
                'reverse_description': 'Canadian coat of arms',
                'distinguishing_features': 'King of Canadian coins - <75 survive',
                'identification_keywords': 'George V, coat of arms, key date',
                'common_names': '1921 Half Dollar (King)',
                'notes': 'Nearly all melted due to low demand'
            }
        ])
        
        # Add 1936 dot coins
        coins.extend([
            {
                'coin_id': 'CA-CENT-1936-P',
                'series_id': 'ca_small_cent',
                'denomination': 'Cents',
                'series_name': 'Small Cent',
                'year': 1936,
                'mint': 'P',
                'rarity': 'key',
                'composition': {'copper': 0.95, 'tin': 0.04, 'zinc': 0.01},
                'weight_grams': 3.24,
                'diameter_mm': 19.05,
                'obverse_description': 'King George V bust left',
                'reverse_description': 'Two maple leaves on twig',
                'distinguishing_features': 'Dot below date (emergency 1937 issue), only 3 known',
                'identification_keywords': 'George V, dot variety, emergency issue',
                'common_names': '1936 Dot Cent',
                'varieties': [{'name': 'Dot variety', 'premium': True}],
                'notes': 'Struck in 1937 with 1936 dies plus dot'
            }
        ])
        
        # Add silver dollars
        coins.extend([
            {
                'coin_id': 'CA-DOLR-1935-P',
                'series_id': 'ca_silver_dollar',
                'denomination': 'Dollars',
                'series_name': 'Voyageur Silver Dollar',
                'year': 1935,
                'mint': 'P',
                'business_strikes': 428707,
                'rarity': 'common',
                'composition': {'silver': 0.80, 'copper': 0.20},
                'weight_grams': 23.33,
                'diameter_mm': 36.0,
                'obverse_description': 'King George V bust left',
                'reverse_description': 'Voyageur canoe with bundle',
                'distinguishing_features': 'First Canadian silver dollar',
                'identification_keywords': 'George V, voyageur, canoe',
                'common_names': '1935 Silver Dollar'
            },
            {
                'coin_id': 'CA-DOLR-1948-P',
                'series_id': 'ca_silver_dollar',
                'denomination': 'Dollars',
                'series_name': 'Voyageur Silver Dollar',
                'year': 1948,
                'mint': 'P',
                'business_strikes': 18780,
                'rarity': 'key',
                'composition': {'silver': 0.80, 'copper': 0.20},
                'weight_grams': 23.33,
                'diameter_mm': 36.0,
                'obverse_description': 'King George VI bust left',
                'reverse_description': 'Voyageur canoe with bundle',
                'distinguishing_features': 'King of Canadian silver dollars - lowest mintage',
                'identification_keywords': 'George VI, voyageur, key date',
                'common_names': '1948 Silver Dollar',
                'notes': 'Lowest mintage of silver dollar series'
            }
        ])
        
        # Insert all coins
        success_count = 0
        for coin in coins:
            if self.insert_coin(coin):
                success_count += 1
                print(f"   ✅ Inserted: {coin['coin_id']}")
        
        self.conn.commit()
        print(f"✅ Phase 1 complete: {success_count}/{len(coins)} coins imported")
        return success_count
    
    def import_phase2_modern(self):
        """Import Phase 2: Modern circulation coins (1968-present)"""
        print("\n📊 Phase 2: Importing modern Canada coins (1968-present)")
        
        coins = []
        
        # Loonie
        coins.append({
            'coin_id': 'CA-DOLR-1987-P',
            'series_id': 'ca_loonie',
            'denomination': 'Dollars',
            'series_name': 'Loonie',
            'year': 1987,
            'mint': 'P',
            'rarity': 'common',
            'composition': {'nickel': 0.915, 'bronze': 0.085},
            'weight_grams': 7.0,
            'diameter_mm': 26.5,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Common loon swimming',
            'distinguishing_features': 'First circulation dollar coin',
            'identification_keywords': 'Elizabeth II, loon, Loonie',
            'common_names': 'Loonie',
            'notes': 'Replaced paper dollar'
        })
        
        # Toonie
        coins.append({
            'coin_id': 'CA-TWOD-1996-P',
            'series_id': 'ca_toonie',
            'denomination': 'Two Dollars',
            'series_name': 'Toonie',
            'year': 1996,
            'mint': 'P',
            'rarity': 'common',
            'composition': {'aluminum_bronze': 0.92, 'nickel': 0.08},
            'weight_grams': 7.3,
            'diameter_mm': 28.0,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Polar bear on ice floe',
            'distinguishing_features': 'Bimetallic coin',
            'identification_keywords': 'Elizabeth II, polar bear, Toonie',
            'common_names': 'Toonie',
            'notes': 'Bimetallic: aluminum bronze core, nickel ring'
        })
        
        # Modern steel coins
        coins.append({
            'coin_id': 'CA-FIVE-2000-P',
            'series_id': 'ca_5c_steel',
            'denomination': 'Five Cents',
            'series_name': '5 Cents Steel',
            'year': 2000,
            'mint': 'P',
            'rarity': 'common',
            'composition': {'steel': 0.945, 'nickel': 0.035, 'copper': 0.02},
            'weight_grams': 3.95,
            'diameter_mm': 21.2,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Beaver on rock',
            'distinguishing_features': 'Multi-ply plated steel',
            'identification_keywords': 'Elizabeth II, beaver, steel',
            'common_names': 'Modern Nickel'
        })
        
        # Insert all coins
        success_count = 0
        for coin in coins:
            if self.insert_coin(coin):
                success_count += 1
                print(f"   ✅ Inserted: {coin['coin_id']}")
        
        self.conn.commit()
        print(f"✅ Phase 2 complete: {success_count}/{len(coins)} coins imported")
        return success_count
    
    def import_phase3_bullion(self):
        """Import Phase 3: Bullion series"""
        print("\n📊 Phase 3: Importing Canada bullion coins")
        
        coins = []
        
        # Gold Maple Leaf
        coins.append({
            'coin_id': 'CA-GMPL-1979-P',
            'series_id': 'ca_gold_maple_leaf',
            'denomination': 'Gold Maple Leaf',
            'series_name': 'Gold Maple Leaf',
            'year': 1979,
            'mint': 'P',
            'rarity': 'common',
            'composition': {'gold': 0.999},
            'weight_grams': 31.103,
            'diameter_mm': 30.0,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Single maple leaf',
            'distinguishing_features': 'First 24-karat bullion coin',
            'identification_keywords': 'Elizabeth II, maple leaf, gold, bullion',
            'common_names': 'Gold Maple Leaf',
            'notes': '1 oz, $50 face value'
        })
        
        # Silver Maple Leaf
        coins.append({
            'coin_id': 'CA-SMPL-1988-P',
            'series_id': 'ca_silver_maple_leaf',
            'denomination': 'Silver Maple Leaf',
            'series_name': 'Silver Maple Leaf',
            'year': 1988,
            'mint': 'P',
            'rarity': 'common',
            'composition': {'silver': 0.9999},
            'weight_grams': 31.103,
            'diameter_mm': 38.0,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Single maple leaf',
            'distinguishing_features': '.9999 fine silver',
            'identification_keywords': 'Elizabeth II, maple leaf, silver, bullion',
            'common_names': 'Silver Maple Leaf',
            'notes': '1 oz, $5 face value'
        })
        
        # Platinum Maple Leaf
        coins.append({
            'coin_id': 'CA-PMPL-1988-P',
            'series_id': 'ca_platinum_maple_leaf',
            'denomination': 'Platinum Maple Leaf',
            'series_name': 'Platinum Maple Leaf',
            'year': 1988,
            'mint': 'P',
            'rarity': 'scarce',
            'composition': {'platinum': 0.9995},
            'weight_grams': 31.103,
            'diameter_mm': 30.0,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Single maple leaf',
            'distinguishing_features': '.9995 fine platinum',
            'identification_keywords': 'Elizabeth II, maple leaf, platinum, bullion',
            'common_names': 'Platinum Maple Leaf',
            'notes': '1 oz, $50 face value'
        })
        
        # Palladium Maple Leaf
        coins.append({
            'coin_id': 'CA-PDML-2005-P',
            'series_id': 'ca_palladium_maple_leaf',
            'denomination': 'Palladium Maple Leaf',
            'series_name': 'Palladium Maple Leaf',
            'year': 2005,
            'mint': 'P',
            'rarity': 'scarce',
            'composition': {'palladium': 0.9995},
            'weight_grams': 31.103,
            'diameter_mm': 30.0,
            'obverse_description': 'Queen Elizabeth II bust right',
            'reverse_description': 'Single maple leaf',
            'distinguishing_features': '.9995 fine palladium',
            'identification_keywords': 'Elizabeth II, maple leaf, palladium, bullion',
            'common_names': 'Palladium Maple Leaf',
            'notes': '1 oz, $50 face value'
        })
        
        # Historical gold
        coins.append({
            'coin_id': 'CA-FIVE-1912-P',
            'series_id': 'ca_gold_5_dollar',
            'denomination': 'Five Dollars',
            'series_name': '$5 Gold',
            'year': 1912,
            'mint': 'P',
            'business_strikes': 165680,
            'rarity': 'scarce',
            'composition': {'gold': 0.90, 'copper': 0.10},
            'weight_grams': 8.36,
            'diameter_mm': 21.6,
            'obverse_description': 'King George V bust left',
            'reverse_description': 'Shield with maple leaves',
            'distinguishing_features': 'Pre-WWI gold coin',
            'identification_keywords': 'George V, shield, gold',
            'common_names': '$5 Gold',
            'notes': 'Withdrawn 1914, released 2012'
        })
        
        # British Sovereign with C mint mark
        coins.append({
            'coin_id': 'CA-SOVR-1916-C',
            'series_id': 'ca_sovereign',
            'denomination': 'Sovereign',
            'series_name': 'Ottawa Sovereign',
            'year': 1916,
            'mint': 'C',
            'business_strikes': 6111,
            'rarity': 'key',
            'composition': {'gold': 0.9167, 'copper': 0.0833},
            'weight_grams': 7.988,
            'diameter_mm': 22.05,
            'obverse_description': 'King George V bust left',
            'reverse_description': 'St. George slaying dragon',
            'distinguishing_features': 'Extremely rare, ~50 known',
            'identification_keywords': 'George V, St. George, sovereign',
            'common_names': '1916C Sovereign',
            'notes': 'British sovereign struck in Ottawa with C mint mark'
        })
        
        # Insert all coins
        success_count = 0
        for coin in coins:
            if self.insert_coin(coin):
                success_count += 1
                print(f"   ✅ Inserted: {coin['coin_id']}")
        
        self.conn.commit()
        print(f"✅ Phase 3 complete: {success_count}/{len(coins)} coins imported")
        return success_count
    
    def run_all_phases(self):
        """Run all import phases."""
        print("🇨🇦 Starting Canada coin import...")
        
        total = 0
        total += self.import_phase1_historical()
        total += self.import_phase2_modern()
        total += self.import_phase3_bullion()
        
        print(f"\n✅ Canada import complete: {total} coins imported")
        return total

def main():
    """Main entry point."""
    importer = CanadaCoinImporter()
    try:
        importer.run_all_phases()
    finally:
        importer.close()

if __name__ == '__main__':
    main()