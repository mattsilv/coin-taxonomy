#!/usr/bin/env python3
"""
Fix coin IDs to match COUNTRY-TYPE-YEAR-MINT format by removing variety suffixes
and moving variety information to the varieties field.
"""

import sqlite3
import json
import os

def main():
    print("🔧 Fixing coin ID format violations...")
    
    db_path = "database/coins.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Find all coins with invalid ID formats (more than 4 parts)
        cursor.execute("""
            SELECT coin_id, year, mint, series_id, 
                   notes, varieties
            FROM coins 
            WHERE LENGTH(coin_id) - LENGTH(REPLACE(coin_id, '-', '')) > 3
        """)
        
        invalid_coins = cursor.fetchall()
        print(f"📊 Found {len(invalid_coins)} coins with invalid ID formats")
        
        fixes = []
        for coin_id, year, mint, series_id, notes, varieties_json in invalid_coins:
            parts = coin_id.split('-')
            if len(parts) > 4:
                # Extract the base ID and variety suffix
                country, type_code, year_str, mint = parts[:4]
                variety_suffix = '-'.join(parts[4:])
                
                # Create the corrected base ID
                correct_id = f"{country}-{type_code}-{year_str}-{mint}"
                
                # Parse existing varieties
                existing_varieties = []
                if varieties_json:
                    try:
                        existing_varieties = json.loads(varieties_json)
                    except:
                        existing_varieties = []
                
                # Create variety entry for the suffix
                variety_name = ""
                variety_desc = ""
                
                if variety_suffix == "War":
                    variety_name = "Wartime Silver"
                    variety_desc = "35% silver wartime composition"
                elif variety_suffix == "DDO":
                    variety_name = "Doubled Die Obverse"
                    variety_desc = "Dramatic doubling visible on obverse"
                elif variety_suffix == "DDR":
                    variety_name = "Doubled Die Reverse"
                    variety_desc = "Strong doubling on reverse elements"
                elif variety_suffix == "FB":
                    variety_name = "Full Bands"
                    variety_desc = "Complete torch bands variety"
                elif variety_suffix == "Rev":
                    variety_name = "Reverse Mint Mark"
                    variety_desc = "Mint mark on reverse (late 1917)"
                elif variety_suffix == "Obv":
                    variety_name = "Obverse Mint Mark"
                    variety_desc = "Mint mark on obverse (early 1917)"
                else:
                    variety_name = variety_suffix
                    variety_desc = f"Variety: {variety_suffix}"
                
                # Add the variety to the array
                variety_entry = {
                    "variety_id": f"{correct_id}-{variety_suffix}",
                    "name": variety_name,
                    "description": variety_desc
                }
                
                existing_varieties.append(variety_entry)
                
                fixes.append({
                    'old_id': coin_id,
                    'new_id': correct_id,
                    'varieties': json.dumps(existing_varieties)
                })
        
        print(f"🔧 Preparing {len(fixes)} ID fixes...")
        
        # Apply the fixes
        for fix in fixes:
            # Check if the corrected ID already exists
            cursor.execute("SELECT COUNT(*) FROM coins WHERE coin_id = ?", (fix['new_id'],))
            existing_count = cursor.fetchone()[0]
            
            if existing_count > 0:
                # Update existing record to add varieties
                cursor.execute("""
                    UPDATE coins 
                    SET varieties = ?
                    WHERE coin_id = ?
                """, (fix['varieties'], fix['new_id']))
                
                # Delete the duplicate with wrong ID
                cursor.execute("DELETE FROM coins WHERE coin_id = ?", (fix['old_id'],))
                print(f"  ✅ Merged {fix['old_id']} into existing {fix['new_id']}")
            else:
                # Update the coin ID and add varieties
                cursor.execute("""
                    UPDATE coins 
                    SET coin_id = ?, varieties = ?
                    WHERE coin_id = ?
                """, (fix['new_id'], fix['varieties'], fix['old_id']))
                print(f"  ✅ Fixed {fix['old_id']} → {fix['new_id']}")
        
        # Commit changes
        conn.commit()
        print(f"✅ Successfully fixed {len(fixes)} coin ID format violations")
        
        # Verify the fixes
        cursor.execute("""
            SELECT COUNT(*) FROM coins 
            WHERE LENGTH(coin_id) - LENGTH(REPLACE(coin_id, '-', '')) > 3
        """)
        remaining_invalid = cursor.fetchone()[0]
        
        if remaining_invalid == 0:
            print("✅ All coin IDs now follow the correct COUNTRY-TYPE-YEAR-MINT format")
        else:
            print(f"⚠️  {remaining_invalid} invalid coin IDs still remain")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()