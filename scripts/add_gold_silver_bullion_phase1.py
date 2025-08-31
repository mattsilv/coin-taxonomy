#!/usr/bin/env python3
"""
Phase 1: Add historical gold commemoratives and pattern pieces.
Part of Issue #37 - Historical Patterns & Commemoratives
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

def add_phase1_coins():
    """Add historical commemoratives and patterns to database."""
    
    db_path = Path(__file__).parent.parent / "database" / "coins.db"
    
    # Saint-Gaudens Ultra High Relief Pattern (STLA)
    stla_coins = [
        {
            "coin_id": "US-STLA-1907-P",
            "series_id": "stla",
            "country": "US",
            "denomination": "Double Eagles",
            "series_name": "Saint-Gaudens Ultra High Relief",
            "year": 1907,
            "mint": "P",
            "business_strikes": 24,
            "proof_strikes": 0,
            "composition": json.dumps({
                "gold": 0.900,
                "copper": 0.100
            }),
            "weight_grams": 33.436,
            "diameter_mm": 34.0,
            "obverse_description": "Liberty standing with torch and olive branch, Capitol building in background, MCMVII date",
            "reverse_description": "Flying eagle over sun with rays, E PLURIBUS UNUM, UNITED STATES OF AMERICA TWENTY DOLLARS",
            "notes": "Ultra High Relief pattern, Roman numerals MCMVII"
        }
    ]
    
    # Gold Commemoratives MCMVII (GCMM)
    gcmm_coins = [
        {
            "coin_id": "US-GCMM-2009-W",
            "series_id": "gcmm",
            "country": "US",
            "denomination": "Double Eagles",
            "series_name": "Ultra High Relief Gold Commemorative",
            "year": 2009,
            "mint": "W",
            "business_strikes": 114427,
            "proof_strikes": 0,
            "composition": json.dumps({
                "gold": 0.9999
            }),
            "weight_grams": 31.108,
            "diameter_mm": 27.0,
            "obverse_description": "Liberty standing with torch and olive branch, Capitol building in background, MMIX date",
            "reverse_description": "Flying eagle over sun with rays, E PLURIBUS UNUM, UNITED STATES OF AMERICA TWENTY DOLLARS",
            "notes": "Ultra High Relief commemorative, .9999 fine gold"
        }
    ]
    
    # Combine all Phase 1 coins
    all_coins = stla_coins + gcmm_coins
    
    # Insert into database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    inserted_count = 0
    skipped_count = 0
    
    for coin in all_coins:
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
            print(f"✅ Added: {coin['coin_id']}")
        except sqlite3.IntegrityError:
            skipped_count += 1
            print(f"⏭️  Skipped (already exists): {coin['coin_id']}")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Phase 1 Summary:")
    print(f"   Added: {inserted_count} coins")
    print(f"   Skipped: {skipped_count} coins")
    
    return inserted_count > 0

if __name__ == "__main__":
    success = add_phase1_coins()
    if success:
        print("\n✨ Phase 1 complete! Run export_from_database.py to generate JSON files.")