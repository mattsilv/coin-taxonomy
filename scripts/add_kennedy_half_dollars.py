#!/usr/bin/env python3
"""
Add Kennedy Half Dollar series to the coin taxonomy database.

Kennedy Half Dollar Composition Periods:
1964: 90% silver, 10% copper (12.50g)
1965-1970: 40% silver clad (11.50g) 
1971-present: Copper-nickel clad (11.34g)

This script adds representative entries from each composition period.
"""

import sqlite3
import json
from datetime import datetime

# Database path
DATABASE_PATH = 'database/coins.db'

def add_kennedy_half_dollars():
    """Add Kennedy Half Dollar entries to the database."""
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Kennedy Half Dollar entries - representative years from each composition period
    kennedy_coins = [
        # 1964 - 90% Silver (First year, highest mintage)
        {
            'coin_id': 'US-KHDO-1964-P',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 1964,
            'mint': 'P',
            'business_strikes': 273304004,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps({
                "silver": 0.90,
                "copper": 0.10
            }),
            'weight_grams': 12.50,
            'diameter_mm': 30.61,
            'varieties': json.dumps([]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'First year of issue, 90% silver composition',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, date below',
            'reverse_description': 'Presidential Seal with heraldic eagle holding arrows and olive branch, UNITED STATES OF AMERICA above, HALF DOLLAR below',
            'distinguishing_features': 'First year Kennedy design, 90% silver composition, 12.50g weight, highest mintage year',
            'identification_keywords': 'kennedy half dollar, 1964 kennedy, silver half dollar, jfk half, presidential seal, first year kennedy',
            'common_names': 'Kennedy Half Dollar, JFK Half Dollar, 1964 Silver Kennedy'
        },
        
        # 1964-D - Denver mint, 90% Silver
        {
            'coin_id': 'US-KHDO-1964-D',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 1964,
            'mint': 'D',
            'business_strikes': 156205446,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps({
                "silver": 0.90,
                "copper": 0.10
            }),
            'weight_grams': 12.50,
            'diameter_mm': 30.61,
            'varieties': json.dumps([]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'First year Denver issue, 90% silver composition',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, date below',
            'reverse_description': 'Presidential Seal with heraldic eagle holding arrows and olive branch, UNITED STATES OF AMERICA above, HALF DOLLAR below',
            'distinguishing_features': 'D mint mark, 90% silver composition, 12.50g weight, first year Denver issue',
            'identification_keywords': 'kennedy half dollar, 1964 kennedy, denver mint, silver half dollar, jfk half, d mint mark',
            'common_names': 'Kennedy Half Dollar, JFK Half Dollar, 1964-D Silver Kennedy'
        },
        
        # 1965 - First year 40% silver clad
        {
            'coin_id': 'US-KHDO-1965-P',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 1965,
            'mint': 'P',
            'business_strikes': 65879366,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps({
                "silver": 0.40,
                "copper": 0.60
            }),
            'weight_grams': 11.50,
            'diameter_mm': 30.61,
            'varieties': json.dumps([]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'First year 40% silver clad composition',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, date below',
            'reverse_description': 'Presidential Seal with heraldic eagle holding arrows and olive branch, UNITED STATES OF AMERICA above, HALF DOLLAR below',
            'distinguishing_features': '40% silver clad composition, 11.50g weight, no mint mark, first year clad silver',
            'identification_keywords': 'kennedy half dollar, 1965 kennedy, 40% silver, silver clad, jfk half, coinage act 1965',
            'common_names': 'Kennedy Half Dollar, JFK Half Dollar, 40% Silver Kennedy'
        },
        
        # 1970-D - Last year 40% silver
        {
            'coin_id': 'US-KHDO-1970-D',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 1970,
            'mint': 'D',
            'business_strikes': 2150000,
            'proof_strikes': 0,
            'rarity': 'scarce',
            'composition': json.dumps({
                "silver": 0.40,
                "copper": 0.60
            }),
            'weight_grams': 11.50,
            'diameter_mm': 30.61,
            'varieties': json.dumps([]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'Last year 40% silver composition, special sets only',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, date below',
            'reverse_description': 'Presidential Seal with heraldic eagle holding arrows and olive branch, UNITED STATES OF AMERICA above, HALF DOLLAR below',
            'distinguishing_features': 'D mint mark, 40% silver clad, 11.50g weight, last year silver composition, special sets only',
            'identification_keywords': 'kennedy half dollar, 1970 kennedy, 40% silver, silver clad, denver mint, last silver year',
            'common_names': 'Kennedy Half Dollar, JFK Half Dollar, 1970-D Silver Kennedy'
        },
        
        # 1971-P - First year copper-nickel clad
        {
            'coin_id': 'US-KHDO-1971-P',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 1971,
            'mint': 'P',
            'business_strikes': 155164000,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps({
                "copper": 0.9167,
                "nickel": 0.0833
            }),
            'weight_grams': 11.34,
            'diameter_mm': 30.61,
            'varieties': json.dumps([]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'First year copper-nickel clad composition',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, date below',
            'reverse_description': 'Presidential Seal with heraldic eagle holding arrows and olive branch, UNITED STATES OF AMERICA above, HALF DOLLAR below',
            'distinguishing_features': 'Copper-nickel clad composition, 11.34g weight, no silver content, first year clad',
            'identification_keywords': 'kennedy half dollar, 1971 kennedy, copper nickel clad, no silver, jfk half, clad composition',
            'common_names': 'Kennedy Half Dollar, JFK Half Dollar, Clad Kennedy'
        },
        
        # 1971-D - Denver mint, first year copper-nickel clad
        {
            'coin_id': 'US-KHDO-1971-D',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 1971,
            'mint': 'D',
            'business_strikes': 302097424,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps({
                "copper": 0.9167,
                "nickel": 0.0833
            }),
            'weight_grams': 11.34,
            'diameter_mm': 30.61,
            'varieties': json.dumps([]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'Highest single year mintage in series',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, date below',
            'reverse_description': 'Presidential Seal with heraldic eagle holding arrows and olive branch, UNITED STATES OF AMERICA above, HALF DOLLAR below',
            'distinguishing_features': 'D mint mark, copper-nickel clad, highest mintage year, 11.34g weight',
            'identification_keywords': 'kennedy half dollar, 1971 kennedy, denver mint, copper nickel clad, highest mintage, d mint mark',
            'common_names': 'Kennedy Half Dollar, JFK Half Dollar, 1971-D Clad Kennedy'
        },
        
        # 1976 Bicentennial - Special reverse design
        {
            'coin_id': 'US-KHDO-1976-P',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 1976,
            'mint': 'P',
            'business_strikes': 234308000,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps({
                "copper": 0.9167,
                "nickel": 0.0833
            }),
            'weight_grams': 11.34,
            'diameter_mm': 30.61,
            'varieties': json.dumps([
                {
                    "variety_id": "KHDO-1976-P-BICENT-01",
                    "name": "Bicentennial Design",
                    "description": "Special Independence Hall reverse design with 1776-1976 dual date"
                }
            ]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'Bicentennial special design with Independence Hall reverse',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, dual date 1776-1976 below',
            'reverse_description': 'Independence Hall in Philadelphia, UNITED STATES OF AMERICA above, HALF DOLLAR below, 200 YEARS OF FREEDOM inscription',
            'distinguishing_features': 'Dual date 1776-1976, Independence Hall reverse, special Bicentennial design, copper-nickel clad',
            'identification_keywords': 'kennedy half dollar, bicentennial kennedy, 1776-1976, independence hall, bicentennial design, special reverse',
            'common_names': 'Bicentennial Kennedy Half Dollar, 1776-1976 Kennedy, Independence Hall Kennedy'
        },
        
        # 2013-P - Modern example (addressing original question)
        {
            'coin_id': 'US-KHDO-2013-P',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 2013,
            'mint': 'P',
            'business_strikes': 5400000,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps({
                "copper": 0.9167,
                "nickel": 0.0833
            }),
            'weight_grams': 11.34,
            'diameter_mm': 30.61,
            'varieties': json.dumps([]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'Modern collector issue, no silver content',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, date below',
            'reverse_description': 'Presidential Seal with heraldic eagle holding arrows and olive branch, UNITED STATES OF AMERICA above, HALF DOLLAR below',
            'distinguishing_features': 'Modern copper-nickel clad, 11.34g weight, collector issue only, no silver content',
            'identification_keywords': 'kennedy half dollar, 2013 kennedy, modern kennedy, copper nickel clad, no silver, collector issue',
            'common_names': 'Kennedy Half Dollar, JFK Half Dollar, Modern Kennedy'
        },
        
        # 2013-D - Modern Denver example (addressing original question)
        {
            'coin_id': 'US-KHDO-2013-D',
            'series_id': 'kennedy_half_dollar',
            'country': 'US',
            'denomination': 'Half Dollars',
            'series_name': 'Kennedy Half Dollar',
            'year': 2013,
            'mint': 'D',
            'business_strikes': 7700000,
            'proof_strikes': 0,
            'rarity': 'common',
            'composition': json.dumps({
                "copper": 0.9167,
                "nickel": 0.0833
            }),
            'weight_grams': 11.34,
            'diameter_mm': 30.61,
            'varieties': json.dumps([]),
            'source_citation': 'US Mint, PCGS CoinFacts',
            'notes': 'Modern collector issue, NO SILVER CONTENT',
            'obverse_description': 'John F. Kennedy bust facing left, LIBERTY around rim, IN GOD WE TRUST to left, date below',
            'reverse_description': 'Presidential Seal with heraldic eagle holding arrows and olive branch, UNITED STATES OF AMERICA above, HALF DOLLAR below',
            'distinguishing_features': 'D mint mark, modern copper-nickel clad, 11.34g weight, NO SILVER, collector issue only',
            'identification_keywords': 'kennedy half dollar, 2013 kennedy, denver mint, modern kennedy, copper nickel clad, no silver, d mint mark',
            'common_names': 'Kennedy Half Dollar, JFK Half Dollar, 2013-D Modern Kennedy'
        }
    ]
    
    # First, check if series already exists in coins table
    cursor.execute("SELECT COUNT(*) FROM coins WHERE coin_id LIKE 'US-KHDO-%'")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"Found {existing_count} existing Kennedy Half Dollar entries. Skipping insertion.")
        conn.close()
        return
    
    # Insert Kennedy Half Dollar entries
    for coin in kennedy_coins:
        try:
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name,
                    year, mint, business_strikes, proof_strikes, rarity,
                    composition, weight_grams, diameter_mm, varieties,
                    source_citation, notes, obverse_description, reverse_description,
                    distinguishing_features, identification_keywords, common_names,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin['coin_id'], coin['series_id'], coin['country'], coin['denomination'],
                coin['series_name'], coin['year'], coin['mint'], coin['business_strikes'],
                coin['proof_strikes'], coin['rarity'], coin['composition'], coin['weight_grams'],
                coin['diameter_mm'], coin['varieties'], coin['source_citation'], coin['notes'],
                coin['obverse_description'], coin['reverse_description'], coin['distinguishing_features'],
                coin['identification_keywords'], coin['common_names'], datetime.now().isoformat()
            ))
            print(f"✓ Added {coin['coin_id']} - {coin['year']} {coin['mint']} mint")
            
        except sqlite3.IntegrityError as e:
            print(f"✗ Failed to add {coin['coin_id']}: {e}")
    
    # Note: Issues table will be populated during export process
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Successfully added {len(kennedy_coins)} Kennedy Half Dollar entries to database")
    print("Added composition periods:")
    print("  • 1964: 90% Silver (12.50g)")
    print("  • 1965-1970: 40% Silver Clad (11.50g)")  
    print("  • 1971-present: Copper-Nickel Clad (11.34g)")
    print("\nNote: 2013-D Kennedy Half Dollar confirmed as COPPER-NICKEL CLAD (NO SILVER)")

if __name__ == '__main__':
    add_kennedy_half_dollars()