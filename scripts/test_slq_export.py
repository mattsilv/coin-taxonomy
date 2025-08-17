#!/usr/bin/env python3
"""
Test export of Standing Liberty Quarter Type I/II varieties
"""

import sqlite3
import json
import os

def test_slq_export():
    """Test export of Standing Liberty Quarter type varieties"""
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    print("🔍 Testing Standing Liberty Quarter type export...")
    
    # Get Standing Liberty quarters from database
    cursor.execute('''
        SELECT 
            coin_id, series_name, year, mint, business_strikes, 
            variety_suffix, rarity, notes, distinguishing_features
        FROM coins 
        WHERE series_name LIKE '%Standing Liberty%'
        ORDER BY year, coin_id
    ''')
    
    coins = cursor.fetchall()
    
    print(f"\n📊 Standing Liberty Quarters in database ({len(coins)} coins):")
    for coin in coins:
        coin_id, series, year, mint, mintage, suffix, rarity, notes, features = coin
        print(f"  📍 {coin_id}")
        print(f"     Year-Mint: {year}-{mint}")
        print(f"     Mintage: {mintage:,}")
        print(f"     Type: {suffix}")
        print(f"     Rarity: {rarity}")
        print(f"     Notes: {notes[:60]}...")
        
        # Parse features if available
        try:
            if features:
                features_data = json.loads(features)
                print(f"     Features: {', '.join(features_data[:2])}...")
        except:
            pass
        print()
    
    # Test JSON export format for variety suffixes
    print("🧪 Testing JSON export format:")
    
    for coin in coins:
        coin_id, series, year, mint, mintage, suffix, rarity, notes, features = coin
        
        # Parse features
        try:
            features_data = json.loads(features) if features else []
        except:
            features_data = []
        
        # Create coin record as it would appear in JSON
        coin_record = {
            "coin_id": coin_id,
            "year": year,
            "mint": mint,
            "business_strikes": mintage,
            "rarity": rarity,
            "distinguishing_features": features_data,
            "notes": notes
        }
        
        print(f"  📄 {coin_id}:")
        print(f"     JSON: {json.dumps(coin_record, indent=6)}")
        print()
    
    conn.close()
    
    # Summary analysis
    type1_coins = [c for c in coins if c[5] == 'TYPE1']
    type2_coins = [c for c in coins if c[5] == 'TYPE2']
    
    print("✅ Standing Liberty Quarter export test completed!")
    print(f"\nVariety Summary:")
    print(f"- Type I coins: {len(type1_coins)} (bare-breasted design)")
    print(f"- Type II coins: {len(type2_coins)} (chain mail covering)")
    print(f"- Total SLQ varieties: {len(coins)}")
    
    print(f"\nType I Examples:")
    for coin in type1_coins:
        print(f"  📍 {coin[0]}: {coin[2]}-{coin[3]} ({coin[4]:,} minted)")
    
    print(f"\nType II Examples:")
    for coin in type2_coins:
        print(f"  📍 {coin[0]}: {coin[2]}-{coin[3]} ({coin[4]:,} minted)")
    
    print(f"\nPrice tracking benefits:")
    print(f"- Accurate Type I vs Type II pricing")
    print(f"- 1917 dual types enable precise market values")
    print(f"- Each type has distinct design characteristics")

if __name__ == "__main__":
    test_slq_export()