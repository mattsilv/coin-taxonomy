#!/usr/bin/env python3
"""
Quick export of just cents to test variety suffix in JSON
"""

import sqlite3
import json
import os

def export_cents_with_varieties():
    """Export cents denomination with variety support"""
    
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    print("📄 Exporting cents with variety suffix support...")
    
    # Get cents data
    cursor.execute('''
        SELECT 
            coin_id, series_id, series_name, year, mint,
            business_strikes, proof_strikes, rarity,
            composition, weight_grams, diameter_mm,
            varieties, source_citation, notes,
            obverse_description, reverse_description,
            distinguishing_features, identification_keywords, common_names,
            COALESCE(variety_suffix, '') as variety_suffix
        FROM coins
        WHERE denomination = 'Cents'
        ORDER BY year, series_name, mint, coin_id
    ''')
    
    rows = cursor.fetchall()
    print(f"Found {len(rows)} cent coins")
    
    # Group by series
    series_dict = {}
    
    for row in rows:
        coin_id = row[0]
        series_id = row[1] 
        series_name = row[2]
        year = row[3]
        mint = row[4]
        variety_suffix = row[19]  # New variety_suffix column
        
        print(f"Processing: {coin_id} (suffix: '{variety_suffix}')")
        
        # Parse JSON fields
        composition = json.loads(row[8]) if row[8] else {}
        varieties = json.loads(row[11]) if row[11] else []
        distinguishing_features = json.loads(row[16]) if row[16] else []
        identification_keywords = json.loads(row[17]) if row[17] else []
        common_names = json.loads(row[18]) if row[18] else []
        
        coin = {
            "coin_id": coin_id,
            "year": year,
            "mint": mint,
            "business_strikes": row[5],
            "proof_strikes": row[6],
            "rarity": row[7],
            "composition": composition,
            "weight_grams": row[9],
            "diameter_mm": row[10],
            "varieties": varieties,
            "source_citation": row[12],
            "notes": row[13],
            "obverse_description": row[14],
            "reverse_description": row[15],
            "distinguishing_features": distinguishing_features,
            "identification_keywords": identification_keywords,
            "common_names": common_names
        }
        
        # Group by series
        if series_name not in series_dict:
            series_dict[series_name] = {
                "series_id": series_id,
                "series_name": series_name,
                "coins": []
            }
        
        series_dict[series_name]["coins"].append(coin)
    
    # Create final structure
    output = {
        "country": "US",
        "denomination": "Cents", 
        "face_value": 0.01,
        "series": list(series_dict.values())
    }
    
    # Save to file
    output_file = "data/us/coins/cents_with_varieties.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Exported cents to: {output_file}")
    
    # Show 1909-S examples
    print("\n🔍 1909-S varieties in export:")
    for series in output["series"]:
        if "Lincoln" in series["series_name"]:
            for coin in series["coins"]:
                if "1909" in coin["coin_id"] and "S" in coin["coin_id"]:
                    print(f"  📍 {coin['coin_id']}: {coin['business_strikes']:,} strikes")
    
    conn.close()
    return output_file

if __name__ == "__main__":
    export_cents_with_varieties()