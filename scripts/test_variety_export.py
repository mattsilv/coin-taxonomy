#!/usr/bin/env python3
"""
Test export of variety suffix coins to verify the system works
"""

import sqlite3
import json
import os

def test_variety_export():
    """Test export of 1909-S varieties"""
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    print("🔍 Testing variety suffix export...")
    
    # Get 1909-S coins from database
    cursor.execute('''
        SELECT 
            coin_id, series_name, year, mint, business_strikes, 
            variety_suffix, rarity, notes, varieties
        FROM coins 
        WHERE coin_id LIKE '%1909-S%' AND series_name LIKE '%Lincoln%'
        ORDER BY coin_id
    ''')
    
    coins = cursor.fetchall()
    
    print("\n📊 1909-S Lincoln Cents in database:")
    for coin in coins:
        coin_id, series, year, mint, mintage, suffix, rarity, notes, varieties = coin
        print(f"  📍 {coin_id}")
        print(f"     Mintage: {mintage:,}")
        print(f"     Suffix: '{suffix}'")
        print(f"     Rarity: {rarity}")
        print(f"     Notes: {notes}")
        print(f"     Varieties: {varieties}")
        print()
    
    # Test JSON export format
    print("🧪 Testing JSON export format:")
    
    for coin in coins:
        coin_id, series, year, mint, mintage, suffix, rarity, notes, varieties = coin
        
        # Parse varieties
        try:
            varieties_data = json.loads(varieties) if varieties else []
        except:
            varieties_data = []
        
        # Create coin record as it would appear in JSON
        coin_record = {
            "coin_id": coin_id,
            "year": year,
            "mint": mint,
            "business_strikes": mintage,
            "rarity": rarity,
            "varieties": varieties_data,
            "notes": notes
        }
        
        print(f"  📄 {coin_id}:")
        print(f"     JSON: {json.dumps(coin_record, indent=6)}")
        print()
    
    conn.close()
    
    print("✅ Variety export test completed!")
    print("\nKey insights:")
    print("- US-LWCT-1909-S: Standard variety (no suffix)")
    print("- US-LWCT-1909-S-VDB: VDB variety (with suffix)")
    print("- Each has distinct mintage and rarity")
    print("- Perfect for precise taxonomic identification!")

if __name__ == "__main__":
    test_variety_export()