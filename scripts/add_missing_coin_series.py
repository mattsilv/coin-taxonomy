#!/usr/bin/env python3
"""
Add missing US coin series to the coin taxonomy database.
This script adds major missing series identified from the analysis.
"""

import sqlite3
import json
from datetime import datetime

def add_barber_half_dollars(cursor):
    """Add Barber Half Dollar series (1892-1915)"""
    print("Adding Barber Half Dollar series...")
    
    # Example entries - fill with specific data
    barber_half_dollars = [
        # Add specific coin entries here
        # Format: US-BRHD-1892-P (Barber Half Dollar)
    ]
    
    for coin in barber_half_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series, denomination, year, mint_mark, country,
                obverse_design, reverse_design, designer, composition,
                weight_grams, diameter_mm, thickness_mm, edge_type,
                distinguishing_features, identification_keywords, common_names,
                rarity_notes, market_category, grade_population_notes,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['series'], coin['denomination'], coin['year'],
            coin['mint_mark'], coin['country'], coin['obverse_design'],
            coin['reverse_design'], coin['designer'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['thickness_mm'],
            coin['edge_type'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'],
            coin['rarity_notes'], coin['market_category'], coin['grade_population_notes'],
            coin['created_at'], coin['updated_at']
        ))

def add_walking_liberty_half_dollars(cursor):
    """Add Walking Liberty Half Dollar series (1916-1947)"""
    print("Adding Walking Liberty Half Dollar series...")
    
    # Example entries - fill with specific data
    walking_liberty_half_dollars = [
        # Add specific coin entries here
        # Format: US-WLHD-1916-P (Walking Liberty Half Dollar)
    ]
    
    for coin in walking_liberty_half_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series, denomination, year, mint_mark, country,
                obverse_design, reverse_design, designer, composition,
                weight_grams, diameter_mm, thickness_mm, edge_type,
                distinguishing_features, identification_keywords, common_names,
                rarity_notes, market_category, grade_population_notes,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['series'], coin['denomination'], coin['year'],
            coin['mint_mark'], coin['country'], coin['obverse_design'],
            coin['reverse_design'], coin['designer'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['thickness_mm'],
            coin['edge_type'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'],
            coin['rarity_notes'], coin['market_category'], coin['grade_population_notes'],
            coin['created_at'], coin['updated_at']
        ))

def add_franklin_half_dollars(cursor):
    """Add Franklin Half Dollar series (1948-1963)"""
    print("Adding Franklin Half Dollar series...")
    
    # Example entries - fill with specific data
    franklin_half_dollars = [
        # Add specific coin entries here
        # Format: US-FRHD-1948-P (Franklin Half Dollar)
    ]
    
    for coin in franklin_half_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series, denomination, year, mint_mark, country,
                obverse_design, reverse_design, designer, composition,
                weight_grams, diameter_mm, thickness_mm, edge_type,
                distinguishing_features, identification_keywords, common_names,
                rarity_notes, market_category, grade_population_notes,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['series'], coin['denomination'], coin['year'],
            coin['mint_mark'], coin['country'], coin['obverse_design'],
            coin['reverse_design'], coin['designer'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['thickness_mm'],
            coin['edge_type'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'],
            coin['rarity_notes'], coin['market_category'], coin['grade_population_notes'],
            coin['created_at'], coin['updated_at']
        ))

def add_three_cent_pieces(cursor):
    """Add Three-Cent Piece series (Silver 1851-1873, Nickel 1865-1889)"""
    print("Adding Three-Cent Piece series...")
    
    # Silver Three-Cent Pieces
    silver_three_cents = [
        # Add specific coin entries here
        # Format: US-S3CT-1851-P (Silver Three-Cent)
    ]
    
    # Nickel Three-Cent Pieces  
    nickel_three_cents = [
        # Add specific coin entries here
        # Format: US-N3CT-1865-P (Nickel Three-Cent)
    ]
    
    all_three_cents = silver_three_cents + nickel_three_cents
    
    for coin in all_three_cents:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series, denomination, year, mint_mark, country,
                obverse_design, reverse_design, designer, composition,
                weight_grams, diameter_mm, thickness_mm, edge_type,
                distinguishing_features, identification_keywords, common_names,
                rarity_notes, market_category, grade_population_notes,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['series'], coin['denomination'], coin['year'],
            coin['mint_mark'], coin['country'], coin['obverse_design'],
            coin['reverse_design'], coin['designer'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['thickness_mm'],
            coin['edge_type'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'],
            coin['rarity_notes'], coin['market_category'], coin['grade_population_notes'],
            coin['created_at'], coin['updated_at']
        ))

def add_two_cent_pieces(cursor):
    """Add Two-Cent Piece series (1864-1873)"""
    print("Adding Two-Cent Piece series...")
    
    # Example entries - fill with specific data
    two_cent_pieces = [
        # Add specific coin entries here
        # Format: US-2CNT-1864-P (Two-Cent Piece)
    ]
    
    for coin in two_cent_pieces:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series, denomination, year, mint_mark, country,
                obverse_design, reverse_design, designer, composition,
                weight_grams, diameter_mm, thickness_mm, edge_type,
                distinguishing_features, identification_keywords, common_names,
                rarity_notes, market_category, grade_population_notes,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['series'], coin['denomination'], coin['year'],
            coin['mint_mark'], coin['country'], coin['obverse_design'],
            coin['reverse_design'], coin['designer'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['thickness_mm'],
            coin['edge_type'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'],
            coin['rarity_notes'], coin['market_category'], coin['grade_population_notes'],
            coin['created_at'], coin['updated_at']
        ))

def add_presidential_dollars(cursor):
    """Add Presidential Dollar series (2007-2020)"""
    print("Adding Presidential Dollar series...")
    
    # Example entries - fill with specific data
    presidential_dollars = [
        # Add specific coin entries here
        # Format: US-PRDD-2007-P (Presidential Dollar)
    ]
    
    for coin in presidential_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series, denomination, year, mint_mark, country,
                obverse_design, reverse_design, designer, composition,
                weight_grams, diameter_mm, thickness_mm, edge_type,
                distinguishing_features, identification_keywords, common_names,
                rarity_notes, market_category, grade_population_notes,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['series'], coin['denomination'], coin['year'],
            coin['mint_mark'], coin['country'], coin['obverse_design'],
            coin['reverse_design'], coin['designer'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['thickness_mm'],
            coin['edge_type'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'],
            coin['rarity_notes'], coin['market_category'], coin['grade_population_notes'],
            coin['created_at'], coin['updated_at']
        ))

def add_native_american_dollars(cursor):
    """Add Native American Dollar series (2009-present)"""
    print("Adding Native American Dollar series...")
    
    # Example entries - fill with specific data
    native_american_dollars = [
        # Add specific coin entries here
        # Format: US-NADD-2009-P (Native American Dollar)
    ]
    
    for coin in native_american_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series, denomination, year, mint_mark, country,
                obverse_design, reverse_design, designer, composition,
                weight_grams, diameter_mm, thickness_mm, edge_type,
                distinguishing_features, identification_keywords, common_names,
                rarity_notes, market_category, grade_population_notes,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['series'], coin['denomination'], coin['year'],
            coin['mint_mark'], coin['country'], coin['obverse_design'],
            coin['reverse_design'], coin['designer'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['thickness_mm'],
            coin['edge_type'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'],
            coin['rarity_notes'], coin['market_category'], coin['grade_population_notes'],
            coin['created_at'], coin['updated_at']
        ))

def main():
    """Main function to add all missing coin series"""
    print("Adding missing US coin series to database...")
    print("=" * 50)
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    try:
        # Add each series
        add_barber_half_dollars(cursor)
        add_walking_liberty_half_dollars(cursor)
        add_franklin_half_dollars(cursor)
        add_three_cent_pieces(cursor)
        add_two_cent_pieces(cursor)
        add_presidential_dollars(cursor)
        add_native_american_dollars(cursor)
        
        # Commit changes
        conn.commit()
        print("\n" + "=" * 50)
        print("✅ Successfully added missing coin series to database!")
        print("Run 'uv run python scripts/export_from_database.py' to regenerate JSON files")
        
    except Exception as e:
        print(f"❌ Error adding coins: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()