#!/usr/bin/env python3
"""
Phase 2: Add modern US gold bullion coins.
Part of Issue #38 - Modern Gold Bullion Implementation
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

def add_phase2_coins():
    """Add modern gold bullion coins to database."""
    
    db_path = Path(__file__).parent.parent / "database" / "coins.db"
    
    coins_to_add = []
    
    # American Gold Eagle 1 oz (AGEO)
    for year in range(1986, 2025):
        coins_to_add.append({
            "coin_id": f"US-AGEO-{year}-W",
            "series_id": "ageo",
            "country": "US",
            "denomination": "Gold Dollars",
            "series_name": "American Gold Eagle 1 oz",
            "year": year,
            "mint": "W",
            "business_strikes": 0,  # Will be updated with actual mintages
            "proof_strikes": 0,
            "composition": json.dumps({
                "gold": 0.9167,
                "silver": 0.030,
                "copper": 0.0533
            }),
            "weight_grams": 33.931,
            "diameter_mm": 32.7,
            "obverse_description": "Liberty striding forward with torch and olive branch",
            "reverse_description": "Eagle family nest with male eagle carrying olive branch",
            "notes": "$50 face value, 1 troy oz gold"
        })
    
    # American Gold Eagle 1/2 oz (AGEH)
    for year in range(1986, 2025):
        coins_to_add.append({
            "coin_id": f"US-AGEH-{year}-W",
            "series_id": "ageh",
            "country": "US",
            "denomination": "Gold Dollars",
            "series_name": "American Gold Eagle 1/2 oz",
            "year": year,
            "mint": "W",
            "business_strikes": 0,
            "proof_strikes": 0,
            "composition": json.dumps({
                "gold": 0.9167,
                "silver": 0.030,
                "copper": 0.0533
            }),
            "weight_grams": 16.966,
            "diameter_mm": 27.0,
            "obverse_description": "Liberty striding forward with torch and olive branch",
            "reverse_description": "Eagle family nest with male eagle carrying olive branch",
            "notes": "$25 face value, 1/2 troy oz gold"
        })
    
    # American Gold Eagle 1/4 oz (AGEQ)
    for year in range(1986, 2025):
        coins_to_add.append({
            "coin_id": f"US-AGEQ-{year}-W",
            "series_id": "ageq",
            "country": "US",
            "denomination": "Gold Dollars",
            "series_name": "American Gold Eagle 1/4 oz",
            "year": year,
            "mint": "W",
            "business_strikes": 0,
            "proof_strikes": 0,
            "composition": json.dumps({
                "gold": 0.9167,
                "silver": 0.030,
                "copper": 0.0533
            }),
            "weight_grams": 8.483,
            "diameter_mm": 22.0,
            "obverse_description": "Liberty striding forward with torch and olive branch",
            "reverse_description": "Eagle family nest with male eagle carrying olive branch",
            "notes": "$10 face value, 1/4 troy oz gold"
        })
    
    # American Gold Eagle 1/10 oz (AGET)
    for year in range(1986, 2025):
        coins_to_add.append({
            "coin_id": f"US-AGET-{year}-W",
            "series_id": "aget",
            "country": "US",
            "denomination": "Gold Dollars",
            "series_name": "American Gold Eagle 1/10 oz",
            "year": year,
            "mint": "W",
            "business_strikes": 0,
            "proof_strikes": 0,
            "composition": json.dumps({
                "gold": 0.9167,
                "silver": 0.030,
                "copper": 0.0533
            }),
            "weight_grams": 3.393,
            "diameter_mm": 16.5,
            "obverse_description": "Liberty striding forward with torch and olive branch",
            "reverse_description": "Eagle family nest with male eagle carrying olive branch",
            "notes": "$5 face value, 1/10 troy oz gold"
        })
    
    # American Buffalo Gold 1 oz (AGBF)
    for year in range(2006, 2025):
        coins_to_add.append({
            "coin_id": f"US-AGBF-{year}-W",
            "series_id": "agbf",
            "country": "US",
            "denomination": "Gold Dollars",
            "series_name": "American Buffalo Gold",
            "year": year,
            "mint": "W",
            "business_strikes": 0,
            "proof_strikes": 0,
            "composition": json.dumps({
                "gold": 0.9999
            }),
            "weight_grams": 31.108,
            "diameter_mm": 32.7,
            "obverse_description": "Native American profile right, based on Buffalo Nickel design",
            "reverse_description": "American Bison standing left on mound",
            "notes": "$50 face value, .9999 fine gold"
        })
    
    # Insert into database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    inserted_count = 0
    skipped_count = 0
    
    for coin in coins_to_add:
        try:
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name,
                    year, mint, business_strikes, proof_strikes, composition,
                    weight_grams, diameter_mm, obverse_description, reverse_description, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin["coin_id"],
                coin["series_id"],
                coin["country"],
                coin["denomination"],
                coin["series_name"],
                coin["year"],
                coin["mint"],
                coin["business_strikes"],
                coin["proof_strikes"],
                coin["composition"],
                coin["weight_grams"],
                coin["diameter_mm"],
                coin["obverse_description"],
                coin["reverse_description"],
                coin["notes"]
            ))
            inserted_count += 1
            if inserted_count % 50 == 0:
                print(f"✅ Added {inserted_count} coins...")
        except sqlite3.IntegrityError:
            skipped_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Phase 2 Summary:")
    print(f"   Added: {inserted_count} modern gold bullion coins")
    print(f"   Skipped: {skipped_count} coins")
    
    return inserted_count > 0

if __name__ == "__main__":
    success = add_phase2_coins()
    if success:
        print("\n✨ Phase 2 complete! Run export_from_database.py to generate JSON files.")