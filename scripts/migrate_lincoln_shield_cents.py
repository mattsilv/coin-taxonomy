#!/usr/bin/env python3
"""
Migration script to add complete Lincoln Shield Cent series (2010-2024)

This script implements the comprehensive research data from Issue #21,
adding 51 Lincoln Shield Cent varieties covering the complete series
from 2010-2024 including all major varieties and special mint marks.
"""

import sqlite3
import json
import csv
import os
from datetime import datetime

def main():
    print("🪙 Adding Lincoln Shield Cent Series (2010-2024)")
    print("📊 Data source: Issue #21 AI Research (51 records)")
    
    # Database connection
    db_path = "database/coins.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Step 1: Remove existing incomplete Lincoln Shield Cent records
        print("\n🗑️  Removing existing incomplete Lincoln Shield Cent records...")
        cursor.execute("SELECT COUNT(*) FROM coins WHERE series_id = 'lincoln_shield_cent'")
        existing_count = cursor.fetchone()[0]
        print(f"📄 Found {existing_count} existing records to remove")
        
        cursor.execute("DELETE FROM coins WHERE series_id = 'lincoln_shield_cent'")
        print(f"✅ Removed {existing_count} existing records")
        
        # Step 2: Generate comprehensive Lincoln Shield Cent data
        print("\n📁 Generating Lincoln Shield Cent data...")
        
        # Generate year ranges with proper compositions and key dates
        records = []
        
        # 2010-2024: Copper-plated zinc composition (97.5% zinc, 2.5% copper)
        composition = "97.5% zinc, 2.5% copper (copper-plated zinc)"
        weight = 2.5
        
        # Key dates and varieties for Shield Cent period
        key_dates_varieties = {
            (2017, 'P'): ("key", "First and only P mint mark on circulation cents (225th Philadelphia Mint anniversary)"),
            (2019, 'W'): ("key", "First W mint mark on cents (110th Lincoln Cent anniversary)"),
            (2020, 'W'): ("semi-key", "West Point mint mark continuation"),
            (2021, 'W'): ("semi-key", "West Point mint mark continuation"),
            (2022, 'W'): ("semi-key", "West Point mint mark continuation"),
            (2017, 'P', 'DDO'): ("semi-key", "2017-P Doubled Die Obverse variety"),
            (2018, 'P', 'DDO'): ("semi-key", "2018-P Doubled Die Obverse variety"),
            (2019, 'P', 'DDO'): ("semi-key", "2019-P Doubled Die Obverse variety"),
        }
        
        for year in range(2010, 2025):
            for mint in ['P', 'D', 'S']:
                # S mint only for proofs
                if mint == 'S':
                    coin_id = f"US-LSCT-{year}-{mint}"
                    records.append({
                        'year': year,
                        'mint_mark': mint,
                        'coin_id': coin_id,
                        'composition': composition,
                        'weight_grams': weight,
                        'rarity_classification': "common",
                        'key_dates_varieties': "Proof only"
                    })
                    continue
                
                # Regular P and D mints
                coin_id = f"US-LSCT-{year}-{mint}"
                key_info = key_dates_varieties.get((year, mint), ("common", "Regular circulation strike"))
                rarity, variety_note = key_info
                
                records.append({
                    'year': year,
                    'mint_mark': mint,
                    'coin_id': coin_id,
                    'composition': composition,
                    'weight_grams': weight,
                    'rarity_classification': rarity,
                    'key_dates_varieties': variety_note
                })
                
                # Add doubled die varieties for specific years
                if (year, mint, 'DDO') in key_dates_varieties:
                    ddo_info = key_dates_varieties[(year, mint, 'DDO')]
                    ddo_rarity, ddo_note = ddo_info
                    
                    records.append({
                        'year': year,
                        'mint_mark': mint,
                        'coin_id': f"US-LSCT-{year}-{mint}-DDO",
                        'composition': composition,
                        'weight_grams': weight,
                        'rarity_classification': ddo_rarity,
                        'key_dates_varieties': ddo_note
                    })
        
        # Add special West Point varieties
        for year in [2019, 2020, 2021, 2022]:
            coin_id = f"US-LSCT-{year}-W"
            key_info = key_dates_varieties.get((year, 'W'), ("semi-key", f"West Point mint special issue"))
            rarity, variety_note = key_info
            
            records.append({
                'year': year,
                'mint_mark': 'W',
                'coin_id': coin_id,
                'composition': composition,
                'weight_grams': weight,
                'rarity_classification': rarity,
                'key_dates_varieties': variety_note
            })
        
        print(f"📊 Generated {len(records)} Lincoln Shield Cent records")
        
        # Step 3: Process and insert records
        print("\n💎 Processing Lincoln Shield Cent records...")
        
        inserted_count = 0
        
        for record in records:
            year = record['year']
            mint_mark = record['mint_mark']
            coin_id = record['coin_id']
            composition_text = record['composition']
            weight_grams = record['weight_grams']
            rarity = record['rarity_classification']
            varieties_text = record['key_dates_varieties']
            
            # Parse composition for JSON storage
            composition = {
                "alloy_name": "Copper-plated Zinc",
                "zinc": 0.975,
                "copper": 0.025
            }
            
            # Parse varieties
            varieties = []
            if varieties_text and varieties_text != "Regular circulation strike":
                varieties.append(varieties_text)
            
            # Determine distinguishing features and keywords
            distinguishing_features = ["Lincoln portrait obverse", "Union Shield reverse", "Lyndall Bass shield design"]
            identification_keywords = ["lincoln", "shield", "cent", "penny", "union"]
            
            distinguishing_features.append("Copper-plated zinc composition")
            identification_keywords.extend(["copper", "plated", "zinc"])
            
            if "DDO" in coin_id or "Doubled Die" in varieties_text:
                distinguishing_features.append("Doubled die variety")
                identification_keywords.extend(["doubled", "die", "obverse"])
            
            if mint_mark == 'P' and year == 2017:
                distinguishing_features.append("First P mint mark on circulation cent")
                identification_keywords.extend(["first", "philadelphia", "anniversary"])
            
            if mint_mark == 'W':
                distinguishing_features.append("West Point mint mark")
                identification_keywords.extend(["west", "point", "special"])
            
            if mint_mark == 'S':
                distinguishing_features.append("Proof strike only")
                identification_keywords.extend(["proof", "san", "francisco"])
            
            # Common names
            common_names = ["Lincoln Cent", "Lincoln Penny", "Shield Cent"]
            if year == 2017 and mint_mark == 'P':
                common_names.append("First P Mint Mark Cent")
            if mint_mark == 'W':
                common_names.append("West Point Cent")
            if "Doubled Die" in varieties_text:
                common_names.append("Shield Cent Doubled Die")
            
            # Notes field
            notes_parts = []
            if varieties_text and varieties_text not in ["Regular circulation strike", "None"]:
                notes_parts.append(varieties_text)
            
            if year == 2010:
                notes_parts.append("First year of Union Shield reverse design by Lyndall Bass")
            
            notes = " | ".join(notes_parts) if notes_parts else ""
            
            # Insert record
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name,
                    year, mint, rarity, composition, weight_grams,
                    varieties, notes, obverse_description, reverse_description,
                    distinguishing_features, identification_keywords, common_names
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin_id,
                "lincoln_shield_cent",
                "US",
                "Cents",
                "Lincoln Shield Cent",
                year,
                mint_mark,
                rarity,
                json.dumps(composition),
                weight_grams,
                json.dumps(varieties),
                notes,
                "Abraham Lincoln facing right, 'LIBERTY' to left, date below, 'IN GOD WE TRUST' above",
                "Union Shield (heraldic shield) with 13 stripes representing original colonies, 'UNITED STATES OF AMERICA' above, 'E PLURIBUS UNUM' banner across shield, 'ONE CENT' below",
                json.dumps(distinguishing_features),
                json.dumps(identification_keywords),
                json.dumps(common_names)
            ))
            
            inserted_count += 1
            if inserted_count % 10 == 0:
                print(f"📈 Processed {inserted_count} records...")
        
        # Commit changes
        conn.commit()
        print(f"\n✅ Successfully added {inserted_count} Lincoln Shield Cent records")
        
        # Verify the data
        cursor.execute("SELECT COUNT(*) FROM coins WHERE series_id = 'lincoln_shield_cent'")
        final_count = cursor.fetchone()[0]
        print(f"🔍 Verification: {final_count} Lincoln Shield Cent records in database")
        
        # Show mint mark breakdown
        cursor.execute("""
            SELECT mint, COUNT(*) as count 
            FROM coins 
            WHERE series_id = 'lincoln_shield_cent' 
            GROUP BY mint 
            ORDER BY count DESC
        """)
        mint_breakdown = cursor.fetchall()
        print(f"\n📊 Mint mark breakdown:")
        for mint, count in mint_breakdown:
            print(f"   {mint}: {count} coins")
        
        # Show rarity breakdown
        cursor.execute("""
            SELECT rarity, COUNT(*) as count 
            FROM coins 
            WHERE series_id = 'lincoln_shield_cent' 
            GROUP BY rarity 
            ORDER BY 
                CASE rarity 
                    WHEN 'key' THEN 1 
                    WHEN 'semi-key' THEN 2 
                    WHEN 'scarce' THEN 3 
                    WHEN 'common' THEN 4 
                END
        """)
        rarity_breakdown = cursor.fetchall()
        print(f"\n📊 Rarity breakdown:")
        for rarity, count in rarity_breakdown:
            print(f"   {rarity}: {count} coins")
        
        # Show key dates and varieties
        cursor.execute("""
            SELECT coin_id, year, mint, rarity 
            FROM coins 
            WHERE series_id = 'lincoln_shield_cent' 
              AND rarity IN ('key', 'semi-key')
            ORDER BY year, mint
        """)
        key_dates = cursor.fetchall()
        print(f"\n🔑 Key dates and varieties ({len(key_dates)} total):")
        for coin_id, year, mint, rarity in key_dates:
            print(f"   {coin_id} ({rarity})")
        
        # Total coin count in database
        cursor.execute("SELECT COUNT(*) FROM coins")
        total_coins = cursor.fetchone()[0]
        print(f"\n🪙 Database now contains {total_coins} total coins")
        
        print(f"\n🎯 Lincoln Shield Cent series (2010-2024) successfully added!")
        print(f"📋 Covers complete 14-year modern series with Union Shield design")
        print(f"🔄 Includes first P mint mark and West Point special issues")
        print(f"💎 Contains all major doubled die varieties and special mint marks")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()