#!/usr/bin/env python3
"""
Export JSON files from SQLite database (DATABASE-FIRST PIPELINE)

This script treats the SQLite database as the source of truth and generates
JSON export files from it. Does NOT rebuild the database.

New Pipeline:
SQLite Database (SOURCE OF TRUTH) → JSON Export Files
      ↑                                    ↑
 SOURCE OF TRUTH                    GENERATED FILES
(version controlled)             (version controlled)

Usage:
    python scripts/export_from_database.py
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

class DatabaseExporter:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.output_dir = 'data/us/coins'
        
    def ensure_output_dir(self):
        """Ensure output directory exists."""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs('data/us/references', exist_ok=True)
        
    def export_coins_by_denomination(self):
        """Export coins grouped by denomination to separate JSON files."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("📊 Exporting coins by denomination from database...")
            
            # Get all denominations
            cursor.execute('''
                SELECT DISTINCT denomination, COUNT(*) as count
                FROM coins 
                GROUP BY denomination 
                ORDER BY denomination
            ''')
            
            denominations = cursor.fetchall()
            
            for denom_name, count in denominations:
                print(f"📄 Exporting {denom_name}: {count} coins")
                
                # Get all coins for this denomination with series grouping
                cursor.execute('''
                    SELECT 
                        coin_id, series_id, series_name, year, mint,
                        business_strikes, proof_strikes, rarity,
                        composition, weight_grams, diameter_mm,
                        varieties, source_citation, notes,
                        country
                    FROM coins
                    WHERE denomination = ?
                    ORDER BY year, series_name, mint
                ''', (denom_name,))
                
                rows = cursor.fetchall()
                
                # Group coins by series
                series_data = {}
                face_value = self.get_face_value(denom_name)
                
                for row in rows:
                    series_id = row[1]
                    series_name = row[2]
                    
                    if series_id not in series_data:
                        series_data[series_id] = {
                            'series_name': series_name,
                            'coins': [],
                            'years': []
                        }
                    
                    # Parse JSON fields
                    composition = json.loads(row[8]) if row[8] else {}
                    varieties = json.loads(row[11]) if row[11] else []
                    
                    coin = {
                        "coin_id": row[0],
                        "year": row[3],
                        "mint": row[4],
                        "business_strikes": row[5],
                        "proof_strikes": row[6],
                        "rarity": row[7],
                        "composition": composition,
                        "varieties": varieties
                    }
                    
                    # Only include non-null values
                    if row[9] is not None:  # weight_grams
                        coin["weight_grams"] = row[9]
                    if row[10] is not None:  # diameter_mm
                        coin["diameter_mm"] = row[10]
                    if row[12] and row[12].strip():  # source_citation
                        coin["source_citation"] = row[12]
                    if row[13] and row[13].strip():  # notes
                        coin["notes"] = row[13]
                    
                    series_data[series_id]['coins'].append(coin)
                    series_data[series_id]['years'].append(row[3])
                
                # Create series entries
                series_list = []
                for series_id, data in series_data.items():
                    years = data['years']
                    coins = data['coins']
                    
                    # Determine composition periods from coins
                    comp_periods = self.extract_composition_periods(coins)
                    
                    series_entry = {
                        "series_id": series_id,
                        "series_name": data['series_name'],
                        "official_name": data['series_name'],
                        "years": {
                            "start": min(years),
                            "end": max(years)
                        },
                        "specifications": self.get_specifications(coins),
                        "composition_periods": comp_periods,
                        "coins": coins
                    }
                    series_list.append(series_entry)
                
                # Sort series by start year
                series_list.sort(key=lambda x: x['years']['start'])
                
                # Create file structure
                file_data = {
                    "country": "US",
                    "denomination": denom_name,
                    "face_value": face_value,
                    "series": series_list
                }
                
                # Write JSON file
                filename = self.get_filename(denom_name)
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(file_data, f, indent=2)
                    
                print(f"   ✅ {filepath}")
                
        except sqlite3.Error as e:
            print(f"❌ Error exporting coins: {e}")
        finally:
            conn.close()
    
    def get_face_value(self, denomination: str) -> float:
        """Get face value for denomination."""
        face_values = {
            'Half Cents': 0.005,
            'Cents': 0.01,
            'Nickels': 0.05,
            'Dimes': 0.10,
            'Twenty Cents': 0.20,
            'Quarters': 0.25,
            'Half Dollars': 0.50,
            'Dollars': 1.00,
            'Trade Dollars': 1.00
        }
        return face_values.get(denomination, 1.00)
    
    def get_filename(self, denomination: str) -> str:
        """Get filename for denomination."""
        filenames = {
            'Half Cents': 'half_cents.json',
            'Cents': 'cents.json',
            'Nickels': 'nickels.json',
            'Dimes': 'dimes.json',
            'Twenty Cents': 'twenty_cents.json',
            'Quarters': 'quarters.json',
            'Half Dollars': 'half_dollars.json',
            'Dollars': 'dollars.json',
            'Trade Dollars': 'trade_dollars.json'
        }
        return filenames.get(denomination, f"{denomination.lower().replace(' ', '_')}.json")
    
    def get_specifications(self, coins: List[Dict]) -> Dict:
        """Extract specifications from coins."""
        # Get specs from first coin that has them
        specs = {"edge": "plain"}  # Default assumption
        
        for coin in coins:
            if coin.get('diameter_mm'):
                specs["diameter_mm"] = coin.get('diameter_mm')
                break
        
        # Only include fields that have values
        return specs
    
    def extract_composition_periods(self, coins: List[Dict]) -> List[Dict]:
        """Extract composition periods from coin data."""
        periods = []
        compositions_seen = {}
        
        for coin in coins:
            comp = coin.get('composition', {})
            if not comp:
                continue
                
            alloy_name = comp.get('alloy_name', 'Unknown')
            year = coin['year']
            
            if alloy_name not in compositions_seen:
                compositions_seen[alloy_name] = {
                    'alloy': comp.get('alloy', {}),
                    'weight_grams': coin.get('weight_grams'),
                    'years': []
                }
            
            compositions_seen[alloy_name]['years'].append(year)
        
        # Create periods
        for alloy_name, data in compositions_seen.items():
            years = data['years']
            if years:
                period = {
                    "date_range": {
                        "start": min(years),
                        "end": max(years)
                    },
                    "alloy_name": alloy_name,
                    "alloy": data['alloy']
                }
                
                # Only include weight if we have data
                if data['weight_grams'] is not None:
                    period["weight"] = {
                        "grams": data['weight_grams']
                    }
                periods.append(period)
        
        # Sort by start year
        periods.sort(key=lambda x: x['date_range']['start'])
        
        # If no periods found, create a default one
        if not periods and coins:
            years = [coin['year'] for coin in coins]
            periods = [{
                "date_range": {
                    "start": min(years),
                    "end": max(years)
                },
                "alloy_name": "Historical",
                "alloy": {}
            }]
        
        return periods
    
    def export_complete_file(self):
        """Export complete us_coins_complete.json file."""
        print("📄 Exporting complete US coins file...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT COUNT(*) as total,
                       MIN(year) as earliest,
                       MAX(year) as latest
                FROM coins
            ''')
            
            stats = cursor.fetchone()
            
            # Get all coins
            cursor.execute('''
                SELECT 
                    coin_id, series_id, series_name, denomination,
                    year, mint, business_strikes, proof_strikes, rarity,
                    composition, weight_grams, diameter_mm,
                    varieties, source_citation, notes, country
                FROM coins
                ORDER BY year, denomination, series_name, mint
            ''')
            
            coins = []
            for row in cursor.fetchall():
                coin = {
                    "coin_id": row[0],
                    "series_id": row[1],
                    "series_name": row[2],
                    "denomination": row[3],
                    "year": row[4],
                    "mint": row[5],
                    "business_strikes": row[6],
                    "proof_strikes": row[7],
                    "rarity": row[8],
                    "composition": json.loads(row[9]) if row[9] else {},
                    "weight_grams": row[10],
                    "diameter_mm": row[11],
                    "varieties": json.loads(row[12]) if row[12] else [],
                    "source_citation": row[13],
                    "notes": row[14],
                    "country": row[15]
                }
                coins.append(coin)
            
            complete_data = {
                "taxonomy_version": "1.1",
                "generated_at": datetime.now().isoformat(),
                "total_coins": stats[0],
                "year_range": {
                    "earliest": stats[1],
                    "latest": stats[2]
                },
                "coins": coins
            }
            
            filepath = 'data/us/us_coins_complete.json'
            with open(filepath, 'w') as f:
                json.dump(complete_data, f, indent=2)
                
            print(f"   ✅ {filepath}")
            
        except sqlite3.Error as e:
            print(f"❌ Error exporting complete file: {e}")
        finally:
            conn.close()
    
    def export_ai_taxonomy(self):
        """Export AI-optimized taxonomy with minimal token usage."""
        print("🤖 Exporting AI-optimized taxonomy...")
        
        # Import and use the AI taxonomy exporter
        try:
            from export_ai_taxonomy import AITaxonomyExporter
            ai_exporter = AITaxonomyExporter(db_path=self.db_path)
            output_file, coin_count = ai_exporter.export_ai_taxonomy()
            
            # Calculate file size
            file_size = output_file.stat().st_size
            print(f"   ✅ data/ai-optimized/us_taxonomy.json ({file_size:,} bytes)")
            
        except ImportError:
            print("   ⚠️  AI taxonomy exporter not found, skipping...")
        except Exception as e:
            print(f"   ❌ Error exporting AI taxonomy: {e}")
    
    def run_export(self):
        """Run complete export from database."""
        print("🚀 Starting database-first export...")
        print("📊 SQLite Database → JSON Export Files")
        
        # Check database exists
        if not os.path.exists(self.db_path):
            print(f"❌ Database not found: {self.db_path}")
            return False
        
        # Check database has data
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM coins')
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            print("❌ Database is empty")
            return False
            
        print(f"📊 Found {count} coins in database")
        
        self.ensure_output_dir()
        
        # Export by denomination
        self.export_coins_by_denomination()
        
        # Export complete file
        self.export_complete_file()
        
        # Export AI-optimized taxonomy
        self.export_ai_taxonomy()
        
        print(f"\n✅ Database-first export completed!")
        print(f"📁 {count} coins exported to JSON files")
        
        return True

def main():
    exporter = DatabaseExporter()
    
    try:
        success = exporter.run_export()
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())