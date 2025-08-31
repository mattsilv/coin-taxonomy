#!/usr/bin/env python3
"""
Phase 3: Add silver bullion and trade dollars.
Part of Issue #39 - Silver Bullion & Trade Dollars
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

def add_phase3_coins():
    """Add silver bullion coins and trade dollars to database."""
    
    db_path = Path(__file__).parent.parent / "database" / "coins.db"
    
    coins_to_add = []
    
    # American Silver Eagle (ASEA)
    for year in range(1986, 2025):
        coins_to_add.append({
            "coin_id": f"US-ASEA-{year}-P",
            "series_id": "asea",
            "country": "US",
            "denomination": "Dollars",
            "series_name": "American Silver Eagle",
            "year": year,
            "mint": "P",
            "business_strikes": 0,
            "proof_strikes": 0,
            "composition": json.dumps({
                "silver": 0.999
            }),
            "weight_grams": 31.103,
            "diameter_mm": 40.6,
            "obverse_description": "Walking Liberty design by Adolph A. Weinman",
            "reverse_description": "Heraldic eagle with shield",
            "notes": "$1 face value, 1 troy oz .999 fine silver"
        })
        
        # West Point proofs
        if year >= 1986:
            coins_to_add.append({
                "coin_id": f"US-ASEA-{year}-W",
                "series_id": "asea",
                "country": "US",
                "denomination": "Dollars",
                "series_name": "American Silver Eagle",
                "year": year,
                "mint": "W",
                "business_strikes": 0,
                "proof_strikes": 0,
                "composition": json.dumps({
                    "silver": 0.999
                }),
                "weight_grams": 31.103,
                "diameter_mm": 40.6,
                "obverse_description": "Walking Liberty design by Adolph A. Weinman",
                "reverse_description": "Heraldic eagle with shield",
                "notes": "$1 face value, 1 troy oz .999 fine silver, Proof"
            })
    
    # America the Beautiful 5 oz Silver (ATBQ)
    for year in range(2010, 2022):
        # Multiple designs per year, using P mint as base
        coins_to_add.append({
            "coin_id": f"US-ATBQ-{year}-P",
            "series_id": "atbq",
            "country": "US",
            "denomination": "Quarters",
            "series_name": "America the Beautiful 5 oz Silver",
            "year": year,
            "mint": "P",
            "business_strikes": 0,
            "proof_strikes": 0,
            "composition": json.dumps({
                "silver": 0.999
            }),
            "weight_grams": 155.517,
            "diameter_mm": 76.2,
            "obverse_description": "George Washington portrait",
            "reverse_description": "National park or site design varies by issue",
            "notes": "25¢ face value, 5 troy oz .999 fine silver"
        })
    
    # Morgan Silver Dollar Commemorative (MSMC)
    morgan_commemorative_years = [2021, 2023, 2024]
    for year in morgan_commemorative_years:
        for mint in ["P", "D", "S", "W", "CC"]:
            coins_to_add.append({
                "coin_id": f"US-MSMC-{year}-{mint}",
                "series_id": "msmc",
                "country": "US",
                "denomination": "Dollars",
                "series_name": "Morgan Dollar Commemorative",
                "year": year,
                "mint": mint,
                "business_strikes": 0,
                "proof_strikes": 0,
                "composition": json.dumps({
                    "silver": 0.999
                }),
                "weight_grams": 26.73,
                "diameter_mm": 38.1,
                "obverse_description": "Liberty head left with LIBERTY on headband",
                "reverse_description": "Eagle with spread wings holding arrows and olive branch",
                "notes": "Modern commemorative with .999 fine silver"
            })
    
    # Peace Silver Dollar Commemorative (PSMC)
    peace_commemorative_years = [2021, 2023, 2024]
    for year in peace_commemorative_years:
        for mint in ["P", "D", "S", "W"]:
            coins_to_add.append({
                "coin_id": f"US-PSMC-{year}-{mint}",
                "series_id": "psmc",
                "country": "US",
                "denomination": "Dollars",
                "series_name": "Peace Dollar Commemorative",
                "year": year,
                "mint": mint,
                "business_strikes": 0,
                "proof_strikes": 0,
                "composition": json.dumps({
                    "silver": 0.999
                }),
                "weight_grams": 26.73,
                "diameter_mm": 38.1,
                "obverse_description": "Liberty head with radiate crown",
                "reverse_description": "Eagle perched on rock with PEACE inscription",
                "notes": "Modern commemorative with .999 fine silver"
            })
    
    # Trade Dollars (TRDO) - Historical
    trade_dollar_coins = []
    for year in range(1873, 1886):
        for mint in ["P", "S", "CC"]:
            if year <= 1878 or (year > 1878 and mint == "P"):  # Proofs only after 1878
                trade_dollar_coins.append({
                    "coin_id": f"US-TRDO-{year}-{mint}",
                    "series_id": "trdo",
                    "country": "US",
                    "denomination": "Trade Dollars",
                    "series_name": "Trade Dollar",
                    "year": year,
                    "mint": mint,
                    "business_strikes": 0,
                    "proof_strikes": 0,
                    "composition": json.dumps({
                        "silver": 0.900,
                        "copper": 0.100
                    }),
                    "weight_grams": 27.22,
                    "diameter_mm": 38.1,
                    "obverse_description": "Liberty seated on bale of merchandise facing left",
                    "reverse_description": "Eagle with spread wings, TRADE DOLLAR inscription",
                    "notes": "420 grains, .900 fine silver"
                })
    
    coins_to_add.extend(trade_dollar_coins)
    
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
    
    print(f"\n📊 Phase 3 Summary:")
    print(f"   Added: {inserted_count} silver bullion coins")
    print(f"   Skipped: {skipped_count} coins")
    
    return inserted_count > 0

if __name__ == "__main__":
    success = add_phase3_coins()
    if success:
        print("\n✨ Phase 3 complete! Run export_from_database.py to generate JSON files.")