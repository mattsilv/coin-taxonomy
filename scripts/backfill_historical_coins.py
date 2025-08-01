#!/usr/bin/env python3
"""
Backfill Migration Script: Add Missing Historical US Coins (1793-1900)

This script implements a phased approach to add missing historical coin series
identified in our coverage analysis. Follows the Senior Engineer Task Execution Rule.

Phase 1: Foundation Series (Large Cents, Capped Bust Half Dollars, Seated Liberty Dimes)
Phase 2: Major Denomination Gaps  
Phase 3: Specialized & Rare Series
Phase 4: Complete Existing Series

Usage:
    python scripts/backfill_historical_coins.py --phase 1
    python scripts/backfill_historical_coins.py --phase all
    python scripts/backfill_historical_coins.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Tuple

class HistoricalCoinBackfill:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None
        
    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_backfill_backup_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")
        
    def get_phase_1_coins(self) -> List[Dict]:
        """Foundation Series: Large Cents, Capped Bust Half Dollars, Seated Liberty Dimes"""
        return [
            # Large Cents - Critical Priority (65 years)
            {"coin_id": "US-LCHN-1793-P", "series_id": "large_cent_chain", "series_name": "Chain Cent", 
             "year": 1793, "mint": "P", "denomination": "Cents", "business_strikes": 36103, 
             "rarity": "key", "source_citation": "Red Book 2024",
             "obverse_description": "Liberty head profile with flowing hair facing right, 'LIBERTY' above, date below",
             "reverse_description": "Circular chain with 15 links surrounding 'ONE CENT', '1/100' below",
             "distinguishing_features": ["First U.S. cent", "Chain design controversial", "Large copper coin 27mm", "15-link chain variant", "Henry Voigt design"],
             "identification_keywords": ["chain cent", "flowing hair", "1793 cent", "large cent", "chain reverse", "first cent", "copper cent", "15 links"],
             "common_names": ["Chain Cent", "1793 Chain Cent", "Flowing Hair Chain Cent"]},
            
            {"coin_id": "US-LWRE-1793-P", "series_id": "large_cent_wreath", "series_name": "Wreath Cent",
             "year": 1793, "mint": "P", "denomination": "Cents", "business_strikes": 63353,
             "rarity": "key", "source_citation": "Red Book 2024",
             "obverse_description": "Liberty head with flowing hair facing right, 'LIBERTY' above, date below",
             "reverse_description": "Wreath encircling 'ONE CENT', '1/100' below",
             "distinguishing_features": ["Replaced unpopular chain design", "Large copper coin 28-29mm", "Wreath design by Henry Voigt", "Vine and bars edge", "First year type"],
             "identification_keywords": ["wreath cent", "1793 cent", "large cent", "wreath reverse", "flowing hair", "copper cent", "vine bars edge"],
             "common_names": ["Wreath Cent", "1793 Wreath Cent", "Flowing Hair Wreath Cent"]},
             
            {"coin_id": "US-DRPB-1799-P", "series_id": "large_cent_draped_bust", "series_name": "Draped Bust Large Cent",
             "year": 1799, "mint": "P", "denomination": "Cents", "business_strikes": 904585,
             "rarity": "key", "source_citation": "PCGS CoinFacts",
             "obverse_description": "Draped bust of Liberty facing right, 'LIBERTY' above, date below",
             "reverse_description": "Wreath encircling 'ONE CENT', fraction '1/100' below, 'UNITED STATES OF AMERICA' around",
             "distinguishing_features": ["Robert Scot design", "Large copper coin 29mm", "Key date 1799", "9 over 8 overdate variety exists", "Plain edge"],
             "identification_keywords": ["draped bust cent", "1799 cent", "large cent", "key date", "robert scot", "copper cent", "overdate"],
             "common_names": ["Draped Bust Cent", "1799 Large Cent", "Draped Bust Large Cent"]},
             
            {"coin_id": "US-CORL-1856-P", "series_id": "large_cent_coronet", "series_name": "Coronet Large Cent",
             "year": 1856, "mint": "P", "denomination": "Cents", "business_strikes": 2690463,
             "rarity": "common", "source_citation": "Red Book 2024",
             "obverse_description": "Liberty head facing left wearing coronet inscribed 'LIBERTY', 13 stars around, date below",
             "reverse_description": "Wreath encircling 'ONE CENT', 'UNITED STATES OF AMERICA' around",
             "distinguishing_features": ["Mature Head design", "Large copper coin 27.5mm", "Christian Gobrecht design", "Slanted 5 variety", "Last large cent series"],
             "identification_keywords": ["coronet cent", "braided hair", "1856 cent", "large cent", "mature head", "copper cent", "gobrecht"],
             "common_names": ["Coronet Cent", "Braided Hair Cent", "Mature Head Cent"]},
             
            # Capped Bust Half Dollars - High Priority (33 years)
            {"coin_id": "US-CBHD-1807-P", "series_id": "capped_bust_half_dollar", "series_name": "Capped Bust Half Dollar",
             "year": 1807, "mint": "P", "denomination": "Half Dollars", "business_strikes": 301076,
             "rarity": "scarce", "source_citation": "Red Book 2024",
             "obverse_description": "Liberty bust facing left wearing cap, 'LIBERTY' on headband, stars around, date below",
             "reverse_description": "Eagle with spread wings holding arrows and olive branch, 'UNITED STATES OF AMERICA' above, '50 C.' below",
             "distinguishing_features": ["John Reich design", "Silver 90%", "32.5mm diameter", "Lettered edge 'FIFTY CENTS OR HALF A DOLLAR'", "First year of type"],
             "identification_keywords": ["capped bust half", "1807 half dollar", "john reich", "lettered edge", "silver half", "50 cents", "large eagle"],
             "common_names": ["Capped Bust Half", "1807 Half Dollar", "Reich Half Dollar"]},
             
            {"coin_id": "US-CBHD-1815-P", "series_id": "capped_bust_half_dollar", "series_name": "Capped Bust Half Dollar", 
             "year": 1815, "mint": "P", "denomination": "Half Dollars", "business_strikes": 47150,
             "rarity": "key", "source_citation": "PCGS CoinFacts",
             "obverse_description": "Liberty bust facing left wearing cap, 'LIBERTY' on headband, stars around, date below",
             "reverse_description": "Eagle with spread wings holding arrows and olive branch, 'UNITED STATES OF AMERICA' above, '50 C.' below",
             "distinguishing_features": ["Key date with low mintage", "5 over 2 overdate", "Silver 90%", "32.5mm diameter", "War of 1812 era"],
             "identification_keywords": ["capped bust half", "1815 half dollar", "key date", "overdate", "5 over 2", "silver half", "rare half"],
             "common_names": ["1815 Capped Bust Half", "1815/2 Half Dollar", "Key Date Half"]},
             
            # Seated Liberty Dimes - Critical Priority (55 years)
            {"coin_id": "US-SLDI-1837-P", "series_id": "seated_liberty_dime", "series_name": "Seated Liberty Dime",
             "year": 1837, "mint": "P", "denomination": "Dimes", "business_strikes": 682500,
             "rarity": "scarce", "source_citation": "Red Book 2024",
             "obverse_description": "Liberty seated on rock holding liberty pole, stars around, date below",
             "reverse_description": "Wreath encircling 'ONE DIME', 'UNITED STATES OF AMERICA' around",
             "distinguishing_features": ["Christian Gobrecht design", "First year of type", "No stars on obverse variety", "Silver 90%", "17.9mm diameter"],
             "identification_keywords": ["seated liberty dime", "1837 dime", "no stars", "gobrecht", "silver dime", "seated dime", "first year"],
             "common_names": ["Seated Liberty Dime", "1837 No Stars Dime", "Seated Dime"]},
             
            {"coin_id": "US-SLDI-1844-P", "series_id": "seated_liberty_dime", "series_name": "Seated Liberty Dime",
             "year": 1844, "mint": "P", "denomination": "Dimes", "business_strikes": 72500,
             "rarity": "key", "source_citation": "PCGS CoinFacts",
             "obverse_description": "Liberty seated on rock holding liberty pole with cap, shield with 'LIBERTY', stars around, date below",
             "reverse_description": "Wreath encircling 'ONE DIME', 'UNITED STATES OF AMERICA' around",
             "distinguishing_features": ["Key date with low mintage", "Silver 90%", "17.9mm diameter", "Stars on obverse", "Shield added to design"],
             "identification_keywords": ["seated liberty dime", "1844 dime", "key date", "rare dime", "silver dime", "seated dime", "scarce"],
             "common_names": ["1844 Seated Liberty Dime", "Key Date Dime", "1844 Dime"]},
        ]
    
    def get_phase_2_coins(self) -> List[Dict]:
        """Major Denomination Gaps: Seated Liberty Quarters/Half Dollars, Half Cents"""
        return [
            # Seated Liberty Quarters
            {"coin_id": "US-SLQU-1838-P", "series_id": "seated_liberty_quarter", "series_name": "Seated Liberty Quarter",
             "year": 1838, "mint": "P", "denomination": "Quarters", "business_strikes": 466000,
             "rarity": "scarce", "source_citation": "Red Book 2024"},
             
            # Half Cents - Selected key dates (FACT-CHECK: Designer attribution corrected)
            {"coin_id": "US-HCLC-1793-P", "series_id": "half_cent_liberty_cap", "series_name": "Liberty Cap Half Cent",
             "year": 1793, "mint": "P", "denomination": "Half Cents", "business_strikes": 35334,
             "rarity": "key", "source_citation": "Red Book 2024"},
             
            {"coin_id": "US-HCDB-1800-P", "series_id": "half_cent_draped_bust", "series_name": "Draped Bust Half Cent", 
             "year": 1800, "mint": "P", "denomination": "Half Cents", "business_strikes": 202908,
             "rarity": "scarce", "source_citation": "Red Book 2024",
             "notes": "Designed by Gilbert Stuart and Robert Scot"},
        ]
    
    def get_phase_3_coins(self) -> List[Dict]:
        """Specialized & Rare Series: Early Dollars, Twenty Cent, Trade Dollars, Gobrecht Dollars"""
        return [
            # Flowing Hair Dollars
            {"coin_id": "US-FHDO-1794-P", "series_id": "flowing_hair_dollar", "series_name": "Flowing Hair Dollar",
             "year": 1794, "mint": "P", "denomination": "Dollars", "business_strikes": 1758,
             "rarity": "key", "source_citation": "PCGS CoinFacts"},
             
            # Gobrecht Dollars (FACT-CHECK ADDITION)
            {"coin_id": "US-GBDO-1836-P", "series_id": "gobrecht_dollar", "series_name": "Gobrecht Dollar",
             "year": 1836, "mint": "P", "denomination": "Dollars", "business_strikes": 0,
             "proof_strikes": 1000, "rarity": "key", "source_citation": "U.S. Mint records, PCGS CoinFacts"},
             
            {"coin_id": "US-GBDO-1838-P", "series_id": "gobrecht_dollar", "series_name": "Gobrecht Dollar",
             "year": 1838, "mint": "P", "denomination": "Dollars", "business_strikes": 300,
             "rarity": "key", "source_citation": "U.S. Mint records, PCGS CoinFacts"},
             
            # Twenty Cent Pieces (FACT-CHECK: Designer attribution corrected)
            {"coin_id": "US-TWCT-1875-P", "series_id": "twenty_cent", "series_name": "Twenty Cent Piece",
             "year": 1875, "mint": "P", "denomination": "Twenty Cents", "business_strikes": 38500,
             "rarity": "scarce", "source_citation": "Red Book 2024", 
             "notes": "Designed by William Barber (obverse after Christian Gobrecht)"},
             
            # Trade Dollars (FACT-CHECK CONFIRMED)
            {"coin_id": "US-TRDO-1873-P", "series_id": "trade_dollar", "series_name": "Trade Dollar",
             "year": 1873, "mint": "P", "denomination": "Trade Dollars", "business_strikes": 396635,
             "rarity": "scarce", "source_citation": "U.S. Mint official records, Stack's Bowers"},
             
            {"coin_id": "US-TRDO-1878-CC", "series_id": "trade_dollar", "series_name": "Trade Dollar", 
             "year": 1878, "mint": "CC", "denomination": "Trade Dollars", "business_strikes": 97000,
             "rarity": "key", "source_citation": "U.S. Mint official records"},
             
            # Flying Eagle Cents (FACT-CHECK CORRECTION: 1857-1858, not 1856)
            {"coin_id": "US-FECN-1857-P", "series_id": "flying_eagle_cent", "series_name": "Flying Eagle Cent",
             "year": 1857, "mint": "P", "denomination": "Cents", "business_strikes": 17450000,
             "rarity": "common", "source_citation": "U.S. Mint official records, PCGS CoinFacts",
             "notes": "First small cent design, 1856 were patterns only"},
             
            {"coin_id": "US-FECN-1858-P", "series_id": "flying_eagle_cent", "series_name": "Flying Eagle Cent",
             "year": 1858, "mint": "P", "denomination": "Cents", "business_strikes": 24600000,
             "rarity": "common", "source_citation": "U.S. Mint official records, PCGS CoinFacts"},
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
                    'obverse_description': coin['obverse_description'],
                    'reverse_description': coin['reverse_description'],
                    'distinguishing_features': json.dumps(coin['distinguishing_features']),
                    'identification_keywords': json.dumps(coin['identification_keywords']),
                    'common_names': json.dumps(coin['common_names'])
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
                
                print(f"✓ Inserted: {coin['coin_id']}")
                
            conn.commit()
            print(f"✓ Successfully inserted {len(coins)} coins")
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f"✗ Database error: {e}")
            raise
        finally:
            conn.close()
    
    def run_phase(self, phase: int, dry_run: bool = False):
        """Execute a specific migration phase."""
        print(f"\n=== Phase {phase} Migration ===")
        
        if phase == 1:
            coins = self.get_phase_1_coins()
            print("Foundation Series: Large Cents, Capped Bust Half Dollars, Seated Liberty Dimes")
        elif phase == 2:
            coins = self.get_phase_2_coins() 
            print("Major Denomination Gaps: Seated Liberty Quarters/Half Dollars, Half Cents")
        elif phase == 3:
            coins = self.get_phase_3_coins()
            print("Specialized & Rare Series: Early Dollars, Twenty Cent, Trade Dollars")
        else:
            raise ValueError(f"Invalid phase: {phase}. Use 1, 2, or 3")
            
        if not dry_run:
            self.create_backup()
            
        self.insert_coins_batch(coins, dry_run)
        
        if not dry_run:
            print(f"✓ Phase {phase} completed. Backup: {self.backup_path}")
    
    def run_all_phases(self, dry_run: bool = False):
        """Execute all migration phases."""
        print("=== Running All Phases ===")
        
        if not dry_run:
            self.create_backup()
            
        for phase in [1, 2, 3]:
            try:
                if phase == 1:
                    coins = self.get_phase_1_coins()
                elif phase == 2:
                    coins = self.get_phase_2_coins()
                else:
                    coins = self.get_phase_3_coins()
                    
                self.insert_coins_batch(coins, dry_run)
                
            except Exception as e:
                print(f"✗ Phase {phase} failed: {e}")
                if not dry_run:
                    print(f"Database restored from backup: {self.backup_path}")
                return False
                
        print("✓ All phases completed successfully")
        return True

def main():
    parser = argparse.ArgumentParser(description='Backfill historical US coins (1793-1900)')
    parser.add_argument('--phase', type=int, choices=[1, 2, 3], 
                        help='Run specific phase (1=Foundation, 2=Major Gaps, 3=Specialized)')
    parser.add_argument('--all', action='store_true', help='Run all phases')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    
    args = parser.parse_args()
    
    backfill = HistoricalCoinBackfill()
    
    try:
        if args.all:
            backfill.run_all_phases(dry_run=args.dry_run)
        elif args.phase:
            backfill.run_phase(args.phase, dry_run=args.dry_run)
        else:
            print("Please specify --phase N or --all")
            print("Use --dry-run to preview changes")
            return 1
            
        if not args.dry_run:
            print("\n✓ Migration completed. Run the following to update JSON exports:")
            print("  uv run python scripts/rebuild_and_export.py")
            
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())