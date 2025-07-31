#!/usr/bin/env python3
"""
Staging Version of Historical Coin Backfill Script

This script runs the migration on staging tables only for safe testing.
Inherits from the main backfill script but targets staging tables.

Usage:
    python scripts/backfill_staging_coins.py --phase 1
    python scripts/backfill_staging_coins.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Tuple

# Import the base class
import sys
sys.path.append(os.path.dirname(__file__))
from backfill_historical_coins import HistoricalCoinBackfill

class StagingHistoricalCoinBackfill(HistoricalCoinBackfill):
    def __init__(self, db_path='database/coins.db'):
        super().__init__(db_path)
        self.staging_mode = True
        
    def insert_coins_batch(self, coins: List[Dict], dry_run: bool = False):
        """Insert a batch of coins into STAGING tables."""
        if dry_run:
            print(f"DRY RUN (STAGING): Would insert {len(coins)} coins:")
            for coin in coins:
                print(f"  - {coin['coin_id']}: {coin['series_name']} {coin['year']}")
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print(f"🔧 Inserting {len(coins)} coins into STAGING tables...")
            
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
                    'notes': coin.get('notes')
                }
                
                # Insert into STAGING table
                cursor.execute('''
                    INSERT OR REPLACE INTO coins_staging (
                        coin_id, series_id, country, denomination, series_name,
                        year, mint, business_strikes, proof_strikes, rarity,
                        composition, weight_grams, diameter_mm, varieties,
                        source_citation, notes
                    ) VALUES (
                        :coin_id, :series_id, :country, :denomination, :series_name,
                        :year, :mint, :business_strikes, :proof_strikes, :rarity,
                        :composition, :weight_grams, :diameter_mm, :varieties,
                        :source_citation, :notes
                    )
                ''', coin_data)
                
                print(f"✅ Inserted (STAGING): {coin['coin_id']}")
                
            conn.commit()
            print(f"✅ Successfully inserted {len(coins)} coins into STAGING")
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f"❌ Database error: {e}")
            raise
        finally:
            conn.close()
    
    def get_staging_comparison(self):
        """Compare staging vs production coin counts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get production counts
            cursor.execute('SELECT COUNT(*) FROM coins')
            prod_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM coins_staging')
            staging_count = cursor.fetchone()[0]
            
            print(f"\n📊 Staging vs Production Comparison:")
            print(f"   Production coins: {prod_count}")
            print(f"   Staging coins:    {staging_count}")
            
            if staging_count > prod_count:
                new_coins = staging_count - prod_count
                increase_pct = (new_coins / prod_count) * 100
                print(f"   🆕 New coins in staging: {new_coins} (+{increase_pct:.1f}%)")
                
            # Show year range comparison
            cursor.execute('SELECT MIN(year), MAX(year) FROM coins')
            prod_range = cursor.fetchone()
            
            cursor.execute('SELECT MIN(year), MAX(year) FROM coins_staging')
            staging_range = cursor.fetchone()
            
            print(f"   Production year range: {prod_range[0]}-{prod_range[1]}")
            print(f"   Staging year range:    {staging_range[0]}-{staging_range[1]}")
            
            # Show 1800s coverage
            cursor.execute('SELECT COUNT(*) FROM coins WHERE year < 1900')
            prod_1800s = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM coins_staging WHERE year < 1900')
            staging_1800s = cursor.fetchone()[0]
            
            print(f"   1800s coins (prod):    {prod_1800s}")
            print(f"   1800s coins (staging): {staging_1800s}")
            
            if staging_1800s > prod_1800s:
                improvement = staging_1800s - prod_1800s
                print(f"   🏛️ 1800s improvement: +{improvement} coins")
                
        except sqlite3.Error as e:
            print(f"❌ Error comparing staging: {e}")
        finally:
            conn.close()
    
    def run_phase(self, phase: int, dry_run: bool = False):
        """Execute a specific migration phase on STAGING tables."""
        print(f"\n=== STAGING Phase {phase} Migration ===")
        
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
            
        self.insert_coins_batch(coins, dry_run)
        
        if not dry_run:
            self.get_staging_comparison()

def main():
    parser = argparse.ArgumentParser(description='Backfill historical US coins in STAGING environment')
    parser.add_argument('--phase', type=int, choices=[1, 2, 3], 
                        help='Run specific phase (1=Foundation, 2=Major Gaps, 3=Specialized)')
    parser.add_argument('--all', action='store_true', help='Run all phases')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--compare', action='store_true', help='Compare staging vs production')
    
    args = parser.parse_args()
    
    backfill = StagingHistoricalCoinBackfill()
    
    try:
        if args.compare:
            backfill.get_staging_comparison()
            
        elif args.all:
            for phase in [1, 2, 3]:
                backfill.run_phase(phase, dry_run=args.dry_run)
                
        elif args.phase:
            backfill.run_phase(args.phase, dry_run=args.dry_run)
            
        else:
            print("Please specify --phase N, --all, or --compare")
            print("Use --dry-run to preview changes")
            return 1
            
        if not args.dry_run and not args.compare:
            print("\n✅ STAGING migration completed!")
            print("Next steps:")
            print("  1. python scripts/export_staging_json.py  # Generate staging exports")
            print("  2. Review staging JSON files")
            print("  3. If satisfied, apply to production")
            
    except Exception as e:
        print(f"❌ STAGING migration failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())