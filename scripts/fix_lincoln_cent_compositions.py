#!/usr/bin/env python3
"""
Fix Lincoln cent composition data to match official specifications.

Key corrections:
1. Fix bronze vs brass mislabeling (bronze has tin, brass doesn't)
2. Add missing 1982 transition year coins (both compositions)
3. Fix 2009 Bicentennial composition (should be bronze for collector issues)
4. Update precise weights and compositions by period
"""

import sqlite3
import json
from datetime import datetime

def fix_lincoln_cent_compositions():
    """Fix Lincoln cent composition data according to official specifications."""
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    try:
        print("🔧 Fixing Lincoln cent composition data...")
        
        # 1. Fix 1944-1946 and 1962-1982 bronze composition (no tin)
        bronze_no_tin = {
            "alloy_name": "Bronze",
            "alloy": {"copper": 0.95, "zinc": 0.05}
        }
        
        print("📝 Updating 1944-1946 bronze composition (95% Cu, 5% Zn, no tin)...")
        cursor.execute("""
            UPDATE coins 
            SET composition = ?, weight_grams = 3.11
            WHERE series_id IN ('lincoln_wheat_cent') 
            AND year BETWEEN 1944 AND 1946
        """, (json.dumps(bronze_no_tin),))
        
        print("📝 Updating 1962-1982 bronze composition (95% Cu, 5% Zn, no tin)...")
        cursor.execute("""
            UPDATE coins 
            SET composition = ?, weight_grams = 3.11
            WHERE series_id IN ('lincoln_memorial_cent') 
            AND year BETWEEN 1962 AND 1981
        """, (json.dumps(bronze_no_tin),))
        
        # 2. Fix 1909-1942 and 1959-1962 bronze composition (with tin)
        bronze_with_tin = {
            "alloy_name": "Bronze",
            "alloy": {"copper": 0.95, "tin": 0.04, "zinc": 0.01}
        }
        
        print("📝 Updating 1909-1942 bronze composition (95% Cu, 4% Sn, 1% Zn)...")
        cursor.execute("""
            UPDATE coins 
            SET composition = ?, weight_grams = 3.11
            WHERE series_id = 'lincoln_wheat_cent' 
            AND year BETWEEN 1909 AND 1942
        """, (json.dumps(bronze_with_tin),))
        
        print("📝 Updating 1959-1962 bronze composition (95% Cu, 4% Sn, 1% Zn)...")
        cursor.execute("""
            UPDATE coins 
            SET composition = ?, weight_grams = 3.11
            WHERE series_id IN ('lincoln_wheat_cent', 'lincoln_memorial_cent') 
            AND year BETWEEN 1959 AND 1962
        """, (json.dumps(bronze_with_tin),))
        
        # 3. Add 1982 transition year coins (both compositions)
        print("➕ Adding 1982 transition year coins...")
        
        # 1982 Bronze (early year)
        bronze_1982 = {
            "alloy_name": "Bronze",
            "alloy": {"copper": 0.95, "zinc": 0.05}
        }
        
        # 1982 Copper-plated zinc (late year)  
        zinc_plated_1982 = {
            "alloy_name": "Copper-Plated Zinc",
            "alloy": {"zinc": 0.975, "copper": 0.025}
        }
        
        # Check if 1982 coins already exist
        cursor.execute("SELECT COUNT(*) FROM coins WHERE year = 1982 AND series_id = 'lincoln_memorial_cent'")
        existing_1982 = cursor.fetchone()[0]
        
        if existing_1982 == 0:
            # Insert 1982 Bronze variant
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name, 
                    year, mint, composition, weight_grams,
                    obverse_description, reverse_description, distinguishing_features,
                    identification_keywords, common_names, rarity, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'US-LMCT-1982-P', 'lincoln_memorial_cent', 'US', 'cent', 'Lincoln Memorial Cent',
                1982, 'P', json.dumps(bronze_1982), 3.11,
                'Abraham Lincoln bust facing right, \'LIBERTY\' to left, \'IN GOD WE TRUST\' above, date to right',
                'Lincoln Memorial building with columns, \'E PLURIBUS UNUM\' above, \'ONE CENT\' below',
                json.dumps(['Bronze composition (early 1982)', 'Transition year', 'Memorial building design']),
                json.dumps(['lincoln memorial cent', '1982 bronze', 'transition year', 'heavy penny']),
                json.dumps(['Lincoln Memorial Cent', 'Bronze Penny']), 
                'common', datetime.now().isoformat()
            ))
            
            # Insert 1982 Copper-plated zinc variant
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name, 
                    year, mint, composition, weight_grams,
                    obverse_description, reverse_description, distinguishing_features,
                    identification_keywords, common_names, rarity, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'US-LMCT-1982-D', 'lincoln_memorial_cent', 'US', 'cent', 'Lincoln Memorial Cent',
                1982, 'D', json.dumps(zinc_plated_1982), 2.50,
                'Abraham Lincoln bust facing right, \'LIBERTY\' to left, \'IN GOD WE TRUST\' above, date to right',
                'Lincoln Memorial building with columns, \'E PLURIBUS UNUM\' above, \'ONE CENT\' below',
                json.dumps(['Copper-plated zinc composition (late 1982)', 'Transition year', 'Lighter weight']),
                json.dumps(['lincoln memorial cent', '1982 zinc', 'transition year', 'light penny']),
                json.dumps(['Lincoln Memorial Cent', 'Zinc Penny']), 
                'common', datetime.now().isoformat()
            ))
        else:
            print(f"⚠️  1982 coins already exist ({existing_1982} found), skipping insert")
        
        # 4. Fix 2009 Bicentennial composition (collector issues should be bronze)
        print("📝 Updating 2009 Bicentennial composition to bronze (collector issue)...")
        cursor.execute("""
            UPDATE coins 
            SET composition = ?, weight_grams = 3.11
            WHERE series_id = 'lincoln_bicentennial_cent' 
            AND year = 2009
        """, (json.dumps(bronze_with_tin),))
        
        # 5. Update copper-plated zinc weight precision (2.50g not 2.5g)
        print("📝 Updating copper-plated zinc weight precision to 2.50g...")
        cursor.execute("""
            UPDATE coins 
            SET weight_grams = 2.50
            WHERE composition LIKE '%Copper-Plated Zinc%' 
            AND weight_grams = 2.5
        """)
        
        # Commit changes
        conn.commit()
        print("✅ Lincoln cent composition corrections completed successfully!")
        
        # Verify results
        print("\n📊 Verification - Lincoln cent compositions by year:")
        cursor.execute("""
            SELECT year, composition, weight_grams, COUNT(*) as count
            FROM coins 
            WHERE series_id IN ('lincoln_wheat_cent', 'lincoln_memorial_cent', 
                               'lincoln_shield_cent', 'lincoln_bicentennial_cent')
            GROUP BY year, composition, weight_grams
            ORDER BY year
        """)
        
        for row in cursor.fetchall():
            year, comp_json, weight, count = row
            comp = json.loads(comp_json)
            print(f"  {year}: {comp['alloy_name']} ({weight}g) - {count} coins")
            
    except Exception as e:
        conn.rollback()
        print(f"❌ Error fixing Lincoln cent compositions: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    fix_lincoln_cent_compositions()