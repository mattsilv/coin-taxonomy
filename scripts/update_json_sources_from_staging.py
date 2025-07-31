#!/usr/bin/env python3
"""
Update JSON source files with historical coins from staging validation.

This script updates the JSON source files in data/us/coins/ to include
the historical coins we validated in staging, then triggers a rebuild.

Following our source of truth workflow:
JSON Source Files → Database → JSON Export Files
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class JSONSourceUpdater:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.json_dir = 'data/us/coins'
        
    def get_staging_coins_by_denomination(self) -> Dict[str, List[Dict]]:
        """Get new coins from staging grouped by denomination."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get coins that were in staging but not in original production
            # We'll identify them as coins from before 1864 (our original start year)
            cursor.execute('''
                SELECT 
                    coin_id, series_id, series_name, year, mint, denomination,
                    business_strikes, proof_strikes, rarity, composition,
                    weight_grams, diameter_mm, varieties, source_citation, notes
                FROM coins_staging 
                WHERE year < 1864 OR series_name IN (
                    'Flying Eagle Cent', 'Trade Dollar', 'Twenty Cent Piece', 'Gobrecht Dollar'
                )
                ORDER BY year, series_name, mint
            ''')
            
            staging_coins = {}
            for row in cursor.fetchall():
                coin = {
                    "coin_id": row[0],
                    "year": row[3],
                    "mint": row[4],
                    "business_strikes": row[6],
                    "proof_strikes": row[7],
                    "rarity": row[8],
                    "source_citation": row[13],
                    "notes": row[14],
                    "varieties": json.loads(row[12]) if row[12] else []
                }
                
                # Group by denomination
                denom = row[5]
                if denom not in staging_coins:
                    staging_coins[denom] = []
                staging_coins[denom].append({
                    "series_id": row[1],
                    "series_name": row[2], 
                    "coin": coin
                })
                
            return staging_coins
            
        except sqlite3.Error as e:
            print(f"❌ Error getting staging coins: {e}")
            return {}
        finally:
            conn.close()
    
    def update_json_file(self, filename: str, new_coins_data: List[Dict]):
        """Update a JSON source file with new historical coins."""
        filepath = os.path.join(self.json_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return False
            
        try:
            # Read existing JSON
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            print(f"📄 Updating {filename}...")
            
            # Group new coins by series
            series_coins = {}
            for item in new_coins_data:
                series_id = item['series_id']
                series_name = item['series_name']
                coin = item['coin']
                
                if series_id not in series_coins:
                    series_coins[series_id] = {
                        'series_name': series_name,
                        'coins': []
                    }
                series_coins[series_id]['coins'].append(coin)
            
            # Add new series to the JSON data
            for series_id, series_info in series_coins.items():
                series_name = series_info['series_name']
                coins = series_info['coins']
                
                # Create new series entry
                new_series = {
                    "series_id": series_id,
                    "series_name": series_name,
                    "official_name": series_name,
                    "years": {
                        "start": min(coin['year'] for coin in coins),
                        "end": max(coin['year'] for coin in coins)
                    },
                    "specifications": {
                        "diameter_mm": 19.05 if 'Cent' in series_name else None,
                        "thickness_mm": 1.5 if 'Cent' in series_name else None,
                        "edge": "plain"
                    },
                    "composition_periods": [
                        {
                            "date_range": {
                                "start": min(coin['year'] for coin in coins),
                                "end": max(coin['year'] for coin in coins)
                            },
                            "alloy_name": "Historical",
                            "alloy": {},
                            "weight": {"grams": None}
                        }
                    ],
                    "coins": coins
                }
                
                # Insert at beginning (chronological order)
                data['series'].insert(0, new_series)
                print(f"   ✅ Added {series_name}: {len(coins)} coins")
            
            # Write updated JSON
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                
            print(f"   ✅ Updated {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating {filename}: {e}")
            return False
    
    def run_update(self):
        """Update all JSON source files with staging data."""
        print("🔄 Updating JSON source files with historical coins...")
        
        # Get staging coins grouped by denomination
        staging_coins = self.get_staging_coins_by_denomination()
        
        if not staging_coins:
            print("❌ No staging coins found to update")
            return False
        
        print(f"📊 Found coins for {len(staging_coins)} denominations:")
        for denom, coins in staging_coins.items():
            print(f"   {denom}: {len(coins)} coins")
        
        # Update each denomination file
        success = True
        denomination_files = {
            'Cents': 'cents.json',
            'Dimes': 'dimes.json', 
            'Quarters': 'quarters.json',
            'Dollars': 'dollars.json',
            'Half Dollars': 'half_dollars.json',
            'Half Cents': 'half_cents.json',
            'Trade Dollars': 'trade_dollars.json',
            'Twenty Cents': 'twenty_cents.json'
        }
        
        for denom, coins_data in staging_coins.items():
            if denom in denomination_files:
                filename = denomination_files[denom]
                
                # For new denominations, create the file
                if not os.path.exists(os.path.join(self.json_dir, filename)):
                    self.create_new_denomination_file(filename, denom, coins_data)
                else:
                    success &= self.update_json_file(filename, coins_data)
        
        return success
    
    def create_new_denomination_file(self, filename: str, denomination: str, coins_data: List[Dict]):
        """Create a new denomination JSON file."""
        filepath = os.path.join(self.json_dir, filename)
        
        print(f"📄 Creating new file: {filename}...")
        
        try:
            # Determine face value based on denomination
            face_values = {
                'Half Cents': 0.005,
                'Twenty Cents': 0.20,
                'Trade Dollars': 1.00
            }
            
            face_value = face_values.get(denomination, 1.00)
            
            # Group by series
            series_data = {}
            for item in coins_data:
                series_id = item['series_id']
                if series_id not in series_data:
                    series_data[series_id] = {
                        'series_name': item['series_name'],
                        'coins': []
                    }
                series_data[series_id]['coins'].append(item['coin'])
            
            # Create series entries
            series_list = []
            for series_id, data in series_data.items():
                coins = data['coins']
                series_entry = {
                    "series_id": series_id,
                    "series_name": data['series_name'],
                    "official_name": data['series_name'],
                    "years": {
                        "start": min(coin['year'] for coin in coins),
                        "end": max(coin['year'] for coin in coins)
                    },
                    "specifications": {
                        "diameter_mm": None,
                        "thickness_mm": None,
                        "edge": "plain"
                    },
                    "composition_periods": [
                        {
                            "date_range": {
                                "start": min(coin['year'] for coin in coins),
                                "end": max(coin['year'] for coin in coins)
                            },
                            "alloy_name": "Historical",
                            "alloy": {},
                            "weight": {"grams": None}
                        }
                    ],
                    "coins": coins
                }
                series_list.append(series_entry)
            
            # Create file structure
            file_data = {
                "country": "US",
                "denomination": denomination,
                "face_value": face_value,
                "series": series_list
            }
            
            # Write new file
            with open(filepath, 'w') as f:
                json.dump(file_data, f, indent=2)
                
            print(f"   ✅ Created {filepath}")
            
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")

def main():
    updater = JSONSourceUpdater()
    
    try:
        success = updater.run_update()
        
        if success:
            print("\n✅ JSON source files updated successfully!")
            print("🔄 Now running complete rebuild...")
            
            # Run the rebuild process
            os.system("uv run python scripts/rebuild_and_export.py")
            
        else:
            print("\n❌ Failed to update JSON source files")
            return 1
            
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())