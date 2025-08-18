#!/usr/bin/env python3
"""
Implementation script for Standing Liberty Quarter Type I/II splits
Based on Issue #28 research data
"""

import sqlite3
import json
from datetime import datetime

def implement_slq_type_splits():
    """
    Implement Standing Liberty Quarter Type I/II splits based on Issue #28 research
    
    Research findings:
    - 1916: Type I only
    - 1917 P/D/S: Both Type I and Type II (mid-February 1917 design change)
    - 1918-1930: Type II only
    
    Mintage data from Issue #28:
    - 1917-P Type I: 8,740,000
    - 1917-P Type II: 13,880,000
    - 1917-S Type II: 5,522,000
    - 1917-D: Both types (exact split TBD)
    """
    
    conn = sqlite3.connect('/Users/m/gh/coin-taxonomy/database/coins.db')
    cursor = conn.cursor()
    
    print("🎯 Implementing Standing Liberty Quarter Type I/II splits from Issue #28...")
    
    # Check current 1917 records
    cursor.execute("""
        SELECT coin_id, year, mint, business_strikes, varieties 
        FROM coins 
        WHERE series_name = 'Standing Liberty Quarter' AND year = 1917
        ORDER BY mint, coin_id
    """)
    current_1917_records = cursor.fetchall()
    
    print(f"📊 Found {len(current_1917_records)} existing 1917 SLQ records:")
    for record in current_1917_records:
        print(f"   {record[0]} - {record[2]} mint, mintage: {record[3]}")
    
    # Implementation plan based on Issue #28 research
    type_splits_to_add = [
        # 1917-D Type I and Type II (both types confirmed, exact split TBD)
        {
            'coin_id': 'US-SLIQ-1917-D-TYPE1',
            'mint': 'D',
            'type': 'Type I',
            'business_strikes': None,  # Split TBD - need exact figures
            'diagnostics': 'Bare breast Liberty, eagle lower on reverse, 13 stars only',
            'design_period': 'January-February 1917'
        },
        {
            'coin_id': 'US-SLIQ-1917-D-TYPE2', 
            'mint': 'D',
            'type': 'Type II',
            'business_strikes': None,  # Split TBD
            'diagnostics': 'Chainmail covering torso, eagle repositioned higher, 3 additional stars below eagle',
            'design_period': 'Mid-February 1917 onward'
        },
        # 1917-S Type I and Type II
        {
            'coin_id': 'US-SLIQ-1917-S-TYPE1',
            'mint': 'S',
            'type': 'Type I', 
            'business_strikes': None,  # Type I total = Total S mintage - 5,522,000 Type II
            'diagnostics': 'Bare breast Liberty, eagle lower on reverse, 13 stars only',
            'design_period': 'January-February 1917'
        },
        {
            'coin_id': 'US-SLIQ-1917-S-TYPE2',
            'mint': 'S',
            'type': 'Type II',
            'business_strikes': 5522000,  # From Issue #28 research
            'diagnostics': 'Chainmail covering torso, eagle repositioned higher, 3 additional stars below eagle', 
            'design_period': 'Mid-February 1917 onward'
        }
    ]
    
    # Update existing 1917-P records with proper mintage splits from Issue #28
    print("\n📝 Updating 1917-P Type I/II mintage data...")
    
    cursor.execute("""
        UPDATE coins 
        SET business_strikes = 8740000,
            notes = 'Type I: Bare breast Liberty, struck January-February 1917 before design change'
        WHERE coin_id = 'US-SLIQ-1917-P-TYPE1'
    """)
    
    cursor.execute("""
        UPDATE coins
        SET business_strikes = 13880000,
            notes = 'Type II: Chainmail covering torso, struck mid-February 1917 onward'  
        WHERE coin_id = 'US-SLIQ-1917-P-TYPE2'
    """)
    
    print("   ✅ Updated 1917-P Type I: 8,740,000 mintage")
    print("   ✅ Updated 1917-P Type II: 13,880,000 mintage")
    
    # Add new 1917-D and 1917-S Type I/II records
    print("\n🆕 Adding new 1917-D and 1917-S Type I/II records...")
    
    for split in type_splits_to_add:
        # Check if record already exists
        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (split['coin_id'],))
        if cursor.fetchone():
            print(f"   ⚠️  {split['coin_id']} already exists, skipping")
            continue
            
        # Create variety JSON for type designation
        varieties = [{
            'variety_id': f"type_{split['type'].lower().replace(' ', '_')}",
            'name': split['type'],
            'description': split['diagnostics'],
            'design_period': split['design_period']
        }]
        
        # Prepare data in proper JSON format matching existing records
        distinguishing_features = []
        identification_keywords = ["standing liberty quarter", "standing quarter", split['type'].lower()]
        common_names = [f"Standing Liberty Quarter {split['type']}", "Standing Quarter"]
        
        if "Type I" in split['type']:
            distinguishing_features = ["Liberty's right breast exposed", "Eagle positioned lower on reverse", "Original 13 stars under eagle"]
            identification_keywords.extend(["type 1 quarter", "bare breast", "exposed liberty"])
        else:
            distinguishing_features = ["Chainmail covering Liberty's torso", "Eagle repositioned higher", "Three additional stars below eagle"]
            identification_keywords.extend(["type 2 quarter", "chainmail", "covered liberty"])
        
        # Insert new record
        insert_sql = """
            INSERT INTO coins (
                coin_id, series_id, country, denomination, series_name, year, mint,
                business_strikes, rarity, obverse_description, reverse_description,
                distinguishing_features, identification_keywords, common_names,
                varieties, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            split['coin_id'],
            'standing_liberty_quarter',
            'US', 
            'Quarters',
            'Standing Liberty Quarter',
            1917,
            split['mint'],
            split['business_strikes'],
            'common',  # Will be updated based on actual rarity
            f"Standing Liberty {split['type']} - " + split['diagnostics'],
            f"Eagle design {split['type']} - " + split['diagnostics'],
            json.dumps(distinguishing_features),
            json.dumps(identification_keywords),
            json.dumps(common_names),
            json.dumps(varieties),
            f"Standing Liberty Quarter {split['type']} - {split['design_period']}"
        )
        
        cursor.execute(insert_sql, values)
        print(f"   ✅ Added {split['coin_id']} ({split['type']})")
    
    # Verify implementation
    print("\n🔍 Verifying complete 1917 Type I/II implementation...")
    cursor.execute("""
        SELECT coin_id, mint, business_strikes, notes
        FROM coins 
        WHERE series_name = 'Standing Liberty Quarter' AND year = 1917
        ORDER BY mint, coin_id
    """)
    
    final_records = cursor.fetchall()
    print(f"📊 Final 1917 SLQ records ({len(final_records)} total):")
    for record in final_records:
        mintage = f"{record[2]:,}" if record[2] else "TBD"
        print(f"   {record[0]} - Mintage: {mintage}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Standing Liberty Quarter Type I/II splits implementation complete!")
    print("\n📋 Summary from Issue #28:")
    print("   - 1916: Type I only (already correct)")
    print("   - 1917-P: Type I (8.74M) + Type II (13.88M) ✅")
    print("   - 1917-D: Type I + Type II ✅ (exact split TBD)")
    print("   - 1917-S: Type I + Type II (5.52M) ✅ (Type I split TBD)")
    print("   - 1918-1930: Type II only (future implementation)")
    
    return True

if __name__ == "__main__":
    implement_slq_type_splits()