#!/usr/bin/env python3
"""
Export staging data to JSON files for review.

This script generates JSON exports from staging tables to review
the impact of the historical coin backfill before applying to production.

Usage:
    python scripts/export_staging_json.py
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List

class StagingJSONExporter:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.output_dir = 'staging_exports'
        
    def ensure_output_dir(self):
        """Create output directory for staging exports."""
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 Output directory: {self.output_dir}/")
        
    def export_staging_summary(self):
        """Export high-level summary of staging data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get staging counts
            cursor.execute('SELECT COUNT(*) FROM coins_staging')
            staging_coins = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM coins')
            prod_coins = cursor.fetchone()[0]
            
            # Get year ranges
            cursor.execute('SELECT MIN(year), MAX(year) FROM coins_staging')
            staging_range = cursor.fetchone()
            
            cursor.execute('SELECT MIN(year), MAX(year) FROM coins')
            prod_range = cursor.fetchone()
            
            # Get 1800s coverage
            cursor.execute('SELECT COUNT(*) FROM coins_staging WHERE year < 1900')
            staging_1800s = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM coins WHERE year < 1900')
            prod_1800s = cursor.fetchone()[0]
            
            # Get series breakdown
            cursor.execute('''
                SELECT series_name, COUNT(*) as count, MIN(year) as start_year, MAX(year) as end_year
                FROM coins_staging 
                GROUP BY series_name 
                ORDER BY start_year, series_name
            ''')
            
            staging_series = []
            for row in cursor.fetchall():
                staging_series.append({
                    "series_name": row[0],
                    "coin_count": row[1], 
                    "year_range": f"{row[2]}-{row[3]}"
                })
            
            # Check for new series (not in production)
            cursor.execute('''
                SELECT DISTINCT s.series_name 
                FROM coins_staging s
                LEFT JOIN coins p ON s.series_name = p.series_name
                WHERE p.series_name IS NULL
                ORDER BY s.series_name
            ''')
            
            new_series = [row[0] for row in cursor.fetchall()]
            
            summary = {
                "export_timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_coins": {
                        "production": prod_coins,
                        "staging": staging_coins,
                        "difference": staging_coins - prod_coins
                    },
                    "year_coverage": {
                        "production_range": f"{prod_range[0]}-{prod_range[1]}",
                        "staging_range": f"{staging_range[0]}-{staging_range[1]}"
                    },
                    "historical_coverage_1800s": {
                        "production": prod_1800s,
                        "staging": staging_1800s,
                        "improvement": staging_1800s - prod_1800s,
                        "improvement_percentage": round(((staging_1800s - prod_1800s) / prod_1800s) * 100, 1)
                    }
                },
                "new_series_added": new_series,
                "all_series_in_staging": staging_series
            }
            
            # Write summary
            summary_path = os.path.join(self.output_dir, 'staging_summary.json')
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
                
            print(f"✅ Summary exported: {summary_path}")
            
            # Print key metrics
            print(f"\n📊 Key Staging Metrics:")
            print(f"   Total coins: {prod_coins} → {staging_coins} (+{staging_coins - prod_coins})")
            print(f"   Year range: {prod_range[0]}-{prod_range[1]} → {staging_range[0]}-{staging_range[1]}")
            print(f"   1800s coins: {prod_1800s} → {staging_1800s} (+{staging_1800s - prod_1800s})")
            print(f"   New series: {len(new_series)}")
            
            if new_series:
                print(f"   🆕 New series added: {', '.join(new_series[:3])}")
                if len(new_series) > 3:
                    print(f"      ... and {len(new_series) - 3} more")
                    
        except sqlite3.Error as e:
            print(f"❌ Error exporting summary: {e}")
        finally:
            conn.close()
            
        return summary
    
    def export_new_coins_detail(self):
        """Export detailed list of new coins added in staging."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get coins that are in staging but not in production
            cursor.execute('''
                SELECT 
                    s.coin_id, s.series_name, s.year, s.mint, s.denomination,
                    s.business_strikes, s.rarity, s.source_citation, s.notes
                FROM coins_staging s
                LEFT JOIN coins p ON s.coin_id = p.coin_id
                WHERE p.coin_id IS NULL
                ORDER BY s.year, s.series_name, s.mint
            ''')
            
            new_coins = []
            for row in cursor.fetchall():
                coin = {
                    "coin_id": row[0],
                    "series_name": row[1],
                    "year": row[2],
                    "mint": row[3],
                    "denomination": row[4],
                    "business_strikes": row[5],
                    "rarity": row[6],
                    "source_citation": row[7],
                    "notes": row[8]
                }
                new_coins.append(coin)
            
            # Group by decade for analysis
            by_decade = {}
            for coin in new_coins:
                decade = (coin['year'] // 10) * 10
                decade_key = f"{decade}s"
                if decade_key not in by_decade:
                    by_decade[decade_key] = []
                by_decade[decade_key].append(coin)
            
            detail_export = {
                "export_timestamp": datetime.now().isoformat(),
                "total_new_coins": len(new_coins),
                "new_coins_by_decade": by_decade,
                "all_new_coins": new_coins
            }
            
            # Write detailed export
            detail_path = os.path.join(self.output_dir, 'new_coins_detail.json')
            with open(detail_path, 'w') as f:
                json.dump(detail_export, f, indent=2)
                
            print(f"✅ New coins detail exported: {detail_path}")
            print(f"   📋 {len(new_coins)} new coins added")
            
            # Show decade breakdown
            print(f"   📊 By decade:")
            for decade, coins in sorted(by_decade.items()):
                print(f"      {decade}: {len(coins)} coins")
                
        except sqlite3.Error as e:
            print(f"❌ Error exporting new coins: {e}")
        finally:
            conn.close()
    
    def export_staging_complete(self):
        """Export complete staging dataset in same format as production exports."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get all staging coins grouped by denomination
            cursor.execute('''
                SELECT denomination, COUNT(*) 
                FROM coins_staging 
                GROUP BY denomination 
                ORDER BY denomination
            ''')
            
            denominations = cursor.fetchall()
            
            for denom_name, count in denominations:
                print(f"📄 Exporting {denom_name}: {count} coins")
                
                # Get all coins for this denomination
                cursor.execute('''
                    SELECT 
                        coin_id, series_id, series_name, year, mint,
                        business_strikes, proof_strikes, rarity,
                        composition, weight_grams, diameter_mm,
                        varieties, source_citation, notes
                    FROM coins_staging
                    WHERE denomination = ?
                    ORDER BY year, series_name, mint
                ''', (denom_name,))
                
                coins = []
                for row in cursor.fetchall():
                    coin = {
                        "coin_id": row[0],
                        "series_id": row[1], 
                        "series_name": row[2],
                        "year": row[3],
                        "mint": row[4],
                        "business_strikes": row[5],
                        "proof_strikes": row[6],
                        "rarity": row[7],
                        "composition": json.loads(row[8]) if row[8] else {},
                        "weight_grams": row[9],
                        "diameter_mm": row[10],
                        "varieties": json.loads(row[11]) if row[11] else [],
                        "source_citation": row[12],
                        "notes": row[13]
                    }
                    coins.append(coin)
                
                # Create export structure
                denom_export = {
                    "denomination": denom_name,
                    "total_coins": len(coins),
                    "export_timestamp": datetime.now().isoformat(),
                    "coins": coins
                }
                
                # Write denomination file
                filename = f"staging_{denom_name.lower().replace(' ', '_')}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(denom_export, f, indent=2)
                    
                print(f"   ✅ {filepath}")
                
        except sqlite3.Error as e:
            print(f"❌ Error exporting complete staging data: {e}")
        finally:
            conn.close()
    
    def run_all_exports(self):
        """Run all staging exports."""
        print("🚀 Starting staging JSON exports...")
        
        self.ensure_output_dir()
        
        # Export summary first
        summary = self.export_staging_summary()
        
        # Export new coins detail
        self.export_new_coins_detail()
        
        # Export complete staging data
        print(f"\n📦 Exporting complete staging datasets...")
        self.export_staging_complete()
        
        print(f"\n✅ All staging exports completed!")
        print(f"📁 Review files in: {self.output_dir}/")
        print(f"\n🔍 Key files to review:")
        print(f"   - staging_summary.json      (high-level metrics)")
        print(f"   - new_coins_detail.json     (detailed new coins)")
        print(f"   - staging_*.json           (complete datasets)")

def main():
    exporter = StagingJSONExporter()
    
    try:
        exporter.run_all_exports()
        return 0
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())