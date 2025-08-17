#!/usr/bin/env python3
"""
Test export of Mercury Dime Full Bands (FB) varieties
"""

import sqlite3
import json
import os

def test_mercury_fb_export():
    """Test export of Mercury FB varieties"""
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    print("🔍 Testing Mercury Dime Full Bands export...")
    
    # Get Mercury dimes from database
    cursor.execute('''
        SELECT 
            coin_id, series_name, year, mint, business_strikes, 
            variety_suffix, rarity, notes, distinguishing_features
        FROM coins 
        WHERE series_name LIKE '%Mercury%'
        ORDER BY year, mint, variety_suffix
    ''')
    
    coins = cursor.fetchall()
    
    print(f"\n📊 Mercury Dimes in database ({len(coins)} coins):")
    
    regular_coins = []
    fb_coins = []
    
    for coin in coins:
        coin_id, series, year, mint, mintage, suffix, rarity, notes, features = coin
        
        if suffix == 'FB':
            fb_coins.append(coin)
            print(f"  🔸 {coin_id} (FB variety)")
        else:
            regular_coins.append(coin)
            print(f"  📍 {coin_id} (Regular)")
        
        print(f"     Year-Mint: {year}-{mint}")
        print(f"     Mintage: {mintage:,}")
        if suffix == 'FB':
            print(f"     FB criteria: Full separation, no bridging, MS60+")
        print()
    
    # Test JSON export format for key dates
    print("🧪 Testing JSON export format for key FB varieties:")
    
    key_dates = ['1916-D', '1921-P', '1926-S', '1931-D', '1945-P']
    
    for coin in fb_coins:
        coin_id, series, year, mint, mintage, suffix, rarity, notes, features = coin
        date_mint = f"{year}-{mint}"
        
        if any(key_date in date_mint for key_date in key_dates):
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
                "variety_suffix": suffix,
                "distinguishing_features": features_data,
                "notes": notes
            }
            
            print(f"  📄 {coin_id} (Key FB variety):")
            print(f"     JSON: {json.dumps(coin_record, indent=6)}")
            print()
    
    conn.close()
    
    # Summary analysis
    print("✅ Mercury Dime FB export test completed!")
    print(f"\nVariety Summary:")
    print(f"- Regular Mercury dimes: {len(regular_coins)}")
    print(f"- FB varieties: {len(fb_coins)}")
    print(f"- Total Mercury records: {len(coins)}")
    
    print(f"\nKey FB Varieties for taxonomic identification:")
    key_fb = [c for c in fb_coins if any(key in f"{c[2]}-{c[3]}" for key in key_dates)]
    for coin in key_fb:
        coin_id, series, year, mint, mintage, suffix, rarity, notes, features = coin
        print(f"  🎯 {coin_id}: {year}-{mint} FB variety")
    
    print(f"\nTaxonomic identification benefits:")
    print(f"- Separate identification for FB vs regular strikes")
    print(f"- FB varieties are significantly rarer than regular strikes")
    print(f"- Precise variety classification for collectors")
    
    # Show pairing examples
    print(f"\nPairing Examples (Regular vs FB):")
    for regular in regular_coins[:5]:  # Show first 5 examples
        regular_id = regular[0]
        fb_id = regular_id + '-FB'
        fb_match = next((c for c in fb_coins if c[0] == fb_id), None)
        if fb_match:
            print(f"  📍 {regular_id} vs 🔸 {fb_id}")

if __name__ == "__main__":
    test_mercury_fb_export()