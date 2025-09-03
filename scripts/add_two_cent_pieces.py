#!/usr/bin/env python3
"""
Add Two-Cent Pieces (1864-1873) to the coin taxonomy database
Data source: Red Book
Issue #49
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

def add_two_cent_pieces(conn):
    """Add Two-Cent Piece data to the database"""
    cursor = conn.cursor()
    
    # First, add to series_registry if not exists
    cursor.execute("""
        INSERT OR IGNORE INTO series_registry (
            series_id, series_name, series_abbreviation, country_code,
            denomination, start_year, end_year, defining_characteristics,
            official_name, type
        ) VALUES (
            'US-TWCT', 'Two-Cent Piece', 'TWCT', 'US',
            'Two Cents', 1864, 1873,
            'First US coin to bear the motto IN GOD WE TRUST',
            'Two-Cent Piece', 'coin'
        )
    """)
    
    # Two-Cent Pieces data from Red Book
    two_cent_data = [
        # Year, Mint, Business Strikes, Proof Strikes, Varieties/Notes
        (1864, 'P', 19822500, 100, 'Large Motto', None),  # Small Motto included in Large Motto total
        (1865, 'P', 13640000, 500, None, None),
        (1866, 'P', 3177000, 725, None, None),
        (1867, 'P', 2938750, 625, None, None),
        (1867, 'P', None, None, 'Doubled Die Obverse', 'DblDieObv'),  # Variety
        (1868, 'P', 2803750, 600, None, None),
        (1869, 'P', 1546500, 600, None, None),
        (1870, 'P', 861250, 1000, None, None),
        (1871, 'P', 721250, 960, None, None),
        (1872, 'P', 65000, 950, None, None),
        (1873, 'P', 0, 600, 'Close 3, Proof only', None),  # Proof only
        (1873, 'P', 0, None, 'Open 3, Alleged Restrike', 'Open3'),  # Restrike variety
    ]
    
    # Composition for Two-Cent Pieces
    composition = json.dumps({
        "copper": 95,
        "tin_zinc": 5
    })
    
    for year, mint, business, proof, notes, variety_suffix in two_cent_data:
        # Skip pure varieties (they'll be added to the varieties field)
        if variety_suffix == 'DblDieObv':
            continue
        if variety_suffix == 'Open3':
            continue
            
        # Determine coin_id
        coin_id = f"US-TWCT-{year}-{mint}"
        
        # Build varieties list
        varieties = []
        if year == 1864:
            varieties = ["Small Motto", "Large Motto"]
        elif year == 1867:
            varieties = ["Doubled Die Obverse"]
        elif year == 1873:
            if notes and "Close 3" in notes:
                varieties = ["Close 3"]
            else:
                varieties = ["Open 3 (Restrike)"]
        
        varieties_json = json.dumps(varieties) if varieties else None
        
        # Determine rarity
        rarity = "common"
        if year == 1872:
            rarity = "scarce"
        elif year == 1873:
            rarity = "scarce"
        elif year == 1871:
            rarity = "scarce"
        elif year == 1870:
            rarity = "scarce"
        
        # Insert coin
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series_id, country, denomination, series_name,
                year, mint, business_strikes, proof_strikes, rarity,
                composition, weight_grams, diameter_mm, varieties,
                source_citation, notes, created_at,
                obverse_description, reverse_description,
                distinguishing_features, identification_keywords, common_names,
                category, subcategory, red_book_category_id
            ) VALUES (
                ?, 'US-TWCT', 'US', 'Two Cents', 'Two-Cent Piece',
                ?, ?, ?, ?, ?,
                ?, 6.22, 23, ?,
                'Red Book 2024', ?, CURRENT_TIMESTAMP,
                'Shield with IN GOD WE TRUST banner above, date below',
                'Denomination TWO CENTS within wheat wreath, UNITED STATES OF AMERICA around',
                'First US coin with IN GOD WE TRUST motto',
                'two cent piece, 2 cent, shield',
                'Two-Cent Piece',
                'coin', 'circulation', 'TWO_CENTS'
            )
        """, (coin_id, year, mint, business, proof, rarity,
              composition, varieties_json, notes))
    
    conn.commit()
    print(f"✅ Added Two-Cent Pieces data to database")

def verify_data(conn):
    """Verify the Two-Cent Pieces were added correctly"""
    cursor = conn.cursor()
    
    # Count Two-Cent pieces
    cursor.execute("""
        SELECT COUNT(*) FROM coins 
        WHERE series_name = 'Two-Cent Piece'
    """)
    count = cursor.fetchone()[0]
    
    # Get summary
    cursor.execute("""
        SELECT year, mint, business_strikes, proof_strikes, varieties
        FROM coins 
        WHERE series_name = 'Two-Cent Piece'
        ORDER BY year, mint
    """)
    
    print(f"\n📊 Two-Cent Pieces Summary:")
    print(f"Total coins added: {count}")
    print("\nYear  Mint  Business     Proof   Varieties")
    print("-" * 50)
    
    for year, mint, business, proof, varieties in cursor.fetchall():
        var_list = json.loads(varieties) if varieties else []
        var_str = ', '.join(var_list) if var_list else ''
        business_str = f"{business:,}" if business else "0"
        proof_str = f"{proof:,}" if proof else "0"
        print(f"{year}  {mint}     {business_str:>10}  {proof_str:>6}  {var_str}")

def main():
    """Main execution"""
    print("🪙 Adding Two-Cent Pieces to Coin Taxonomy")
    print("=" * 60)
    
    # Connect to database
    db_path = Path("database/coins.db")
    conn = sqlite3.connect(db_path)
    
    try:
        # Add the data
        add_two_cent_pieces(conn)
        
        # Verify
        verify_data(conn)
        
        print("\n✅ Two-Cent Pieces successfully added!")
        print("   Issue #49 can be closed")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()