#!/usr/bin/env python3
"""
Comprehensive U.S. Silver Coin Composition Verification and Corrections

This script addresses all issues identified in GitHub issue #15:
1. Add missing war nickels (1942-1945) - 35% silver
2. Complete half dollar composition history 
3. Add dimes clad composition (1965-present)
4. Fix pre-1837 silver fineness (89.24% standard)
5. Add three-cent silver denomination
6. Correct various weight and face value issues

Database-first workflow: All changes go to SQLite database as source of truth.
"""

import sqlite3
import json
from datetime import datetime
import sys

def connect_db():
    """Connect to the coins database"""
    return sqlite3.connect('database/coins.db')

def add_war_nickels(conn):
    """Add missing war nickels (1942-1945) with 35% silver composition"""
    print("=== ADDING WAR NICKELS (1942-1945) ===")
    
    cursor = conn.cursor()
    
    # War nickel composition: 35% silver, 56% copper, 9% manganese
    war_composition = {
        "alloy_name": "Wartime Silver",
        "alloy": {
            "silver": 0.35,
            "copper": 0.56,
            "manganese": 0.09
        }
    }
    
    # War nickels data (representative key dates)
    war_nickels = [
        {
            "coin_id": "US-JEFF-1942-P",
            "year": 1942,
            "mint": "P",
            "business_strikes": 49818000,  # Mid-year start
            "notes": "First year of wartime silver composition - mid-year change"
        },
        {
            "coin_id": "US-JEFF-1943-P", 
            "year": 1943,
            "mint": "P", 
            "business_strikes": 271165000,
            "notes": "Full year wartime silver composition"
        },
        {
            "coin_id": "US-JEFF-1944-P",
            "year": 1944,
            "mint": "P",
            "business_strikes": 119150000, 
            "notes": "Wartime silver composition continues"
        },
        {
            "coin_id": "US-JEFF-1945-P",
            "year": 1945,
            "mint": "P",
            "business_strikes": 119408100,
            "notes": "Final year of wartime silver composition"
        }
    ]
    
    for nickel in war_nickels:
        # Check if coin already exists
        cursor.execute('SELECT coin_id FROM coins WHERE coin_id = ?', (nickel["coin_id"],))
        if cursor.fetchone():
            print(f"  War nickel {nickel['coin_id']} already exists, updating composition...")
            cursor.execute('''
                UPDATE coins SET 
                    composition = ?,
                    notes = ?
                WHERE coin_id = ?
            ''', (json.dumps(war_composition), nickel["notes"], nickel["coin_id"]))
        else:
            print(f"  Adding war nickel {nickel['coin_id']}...")
            cursor.execute('''
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name,
                    year, mint, business_strikes, composition, weight_grams,
                    diameter_mm, notes, source_citation, rarity,
                    obverse_description, reverse_description,
                    distinguishing_features, identification_keywords, common_names,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nickel["coin_id"], "jefferson_nickel", "US", "Nickels", "Jefferson Nickel",
                nickel["year"], nickel["mint"], nickel["business_strikes"],
                json.dumps(war_composition), 5.0, 21.2,
                nickel["notes"], "U.S. Mint Records",
                "common" if nickel["year"] == 1943 else "scarce",
                "Thomas Jefferson profile facing left, 'LIBERTY' above, 'IN GOD WE TRUST' to left, date below",
                "Monticello (Jefferson's home) with steps, 'UNITED STATES OF AMERICA' above, 'FIVE CENTS' below, large mintmark above building",
                "35% silver composition (wartime only), Large mintmark over Monticello, Magnetic properties due to manganese",
                "war nickel, wartime nickel, silver nickel, jefferson nickel, 35% silver, magnetic nickel, large mintmark, monticello nickel",
                "War Nickel, Wartime Nickel, Silver Jefferson Nickel, Jefferson Five Cents",
                datetime.now()
            ))
    
    conn.commit()
    print(f"✓ Added/updated {len(war_nickels)} war nickels")

def fix_dimes_clad_composition(conn):
    """Add missing clad composition for dimes 1965-present"""
    print("=== FIXING DIMES CLAD COMPOSITION (1965-present) ===")
    
    cursor = conn.cursor()
    
    # Clad composition for dimes
    clad_composition = {
        "alloy_name": "Copper-Nickel Clad",
        "alloy": {
            "copper_core": 1.0,  # Pure copper core
            "cupronickel_cladding": 0.0833  # 75% Cu, 25% Ni cladding (8.33% of total)
        }
    }
    
    # Check for existing Roosevelt dimes 1965+ that need clad composition
    cursor.execute('''
        SELECT coin_id, year, composition 
        FROM coins 
        WHERE coin_id LIKE "US-ROOS%" AND year >= 1965 
        ORDER BY year
    ''')
    
    roosevelt_dimes = cursor.fetchall()
    updated_count = 0
    
    for coin_id, year, current_comp in roosevelt_dimes:
        current_composition = json.loads(current_comp) if current_comp else {}
        
        # If it's already clad, verify it's correct
        if current_composition.get("alloy_name") == "Clad":
            # Update to proper clad specification
            cursor.execute('''
                UPDATE coins SET 
                    composition = ?,
                    weight_grams = 2.268
                WHERE coin_id = ?
            ''', (json.dumps(clad_composition), coin_id))
            updated_count += 1
            print(f"  Updated {coin_id} to correct clad composition")
        elif not current_composition or current_composition.get("alloy_name") == "Silver":
            # This shouldn't happen for 1965+ but let's fix it
            if year >= 1965:
                cursor.execute('''
                    UPDATE coins SET 
                        composition = ?,
                        weight_grams = 2.268
                    WHERE coin_id = ?
                ''', (json.dumps(clad_composition), coin_id))
                updated_count += 1
                print(f"  Fixed {coin_id} from {current_composition.get('alloy_name', 'empty')} to clad")
    
    conn.commit()
    print(f"✓ Updated {updated_count} Roosevelt dimes to correct clad composition")

def fix_half_dollars_comprehensive(conn):
    """Complete half dollar composition history (1794-present)"""
    print("=== FIXING HALF DOLLARS COMPREHENSIVE COMPOSITION ===")
    
    cursor = conn.cursor()
    
    # Define all half dollar composition periods
    compositions = {
        # Pre-1837 early silver standard
        "early_silver": {
            "alloy_name": "Early Silver", 
            "alloy": {"silver": 0.8924, "copper": 0.1076}
        },
        # 1837-1964 standard silver
        "standard_silver": {
            "alloy_name": "Silver",
            "alloy": {"silver": 0.9, "copper": 0.1}
        },
        # 1965-1970 40% silver clad
        "silver_clad": {
            "alloy_name": "Silver Clad",
            "alloy": {
                "silver_cladding": 0.8,  # 80% Ag/20% Cu outer layers
                "copper_cladding": 0.2,
                "core_silver": 0.21,  # ~21% Ag/79% Cu core
                "core_copper": 0.79
            }
        },
        # 1971-present copper-nickel clad
        "cupronickel_clad": {
            "alloy_name": "Copper-Nickel Clad",
            "alloy": {
                "copper_core": 0.917,
                "cupronickel_cladding": 0.083
            }
        }
    }
    
    # Update existing half dollars with empty compositions
    cursor.execute('''
        SELECT coin_id, year, series_id, composition 
        FROM coins 
        WHERE (coin_id LIKE "%HD%" OR coin_id LIKE "%HALF%" OR denomination = "Half Dollars")
        ORDER BY year
    ''')
    
    half_dollars = cursor.fetchall()
    updated_count = 0
    
    for coin_id, year, series_id, current_comp in half_dollars:
        current_composition = json.loads(current_comp) if current_comp else {}
        new_composition = None
        new_weight = None
        
        # Determine correct composition and weight by year
        if year <= 1836:
            new_composition = compositions["early_silver"]
            new_weight = 13.48  # Early weight
        elif year <= 1964:
            new_composition = compositions["standard_silver"] 
            new_weight = 12.50  # Standard silver weight
        elif year <= 1970:
            new_composition = compositions["silver_clad"]
            new_weight = 11.5  # 40% silver clad weight
        else:  # 1971+
            new_composition = compositions["cupronickel_clad"]
            new_weight = 11.34  # Clad weight
        
        # Update if composition is empty or marked as "Unknown"/"Historical"
        if (not current_composition or 
            current_composition.get("alloy_name") in ["Unknown", "Historical", ""]):
            
            cursor.execute('''
                UPDATE coins SET 
                    composition = ?,
                    weight_grams = ?
                WHERE coin_id = ?
            ''', (json.dumps(new_composition), new_weight, coin_id))
            
            updated_count += 1
            print(f"  Updated {coin_id} ({year}) to {new_composition['alloy_name']}")
    
    conn.commit()
    print(f"✓ Updated {updated_count} half dollars with comprehensive compositions")

def fix_pre_1837_silver_standard(conn):
    """Fix pre-1837 silver fineness to 89.24% standard"""
    print("=== FIXING PRE-1837 SILVER FINENESS (89.24% STANDARD) ===")
    
    cursor = conn.cursor()
    
    # Early silver standard composition
    early_silver = {
        "alloy_name": "Early Silver",
        "alloy": {"silver": 0.8924, "copper": 0.1076}
    }
    
    # Find all pre-1837 silver coins with empty or incorrect compositions
    cursor.execute('''
        SELECT coin_id, year, denomination, composition 
        FROM coins 
        WHERE year <= 1837 
        AND (denomination IN ("Dimes", "Quarters", "Half Dollars", "Dollars", "Half Dimes"))
        AND (composition = "{}" OR composition IS NULL OR composition = "")
        ORDER BY year, denomination
    ''')
    
    early_coins = cursor.fetchall()
    updated_count = 0
    
    for coin_id, year, denomination, current_comp in early_coins:
        # Skip if already has proper composition
        if current_comp:
            try:
                comp_obj = json.loads(current_comp)
                if comp_obj.get("alloy", {}).get("silver") == 0.8924:
                    continue
            except:
                pass
        
        cursor.execute('''
            UPDATE coins SET composition = ?
            WHERE coin_id = ?
        ''', (json.dumps(early_silver), coin_id))
        
        updated_count += 1
        print(f"  Updated {coin_id} ({year} {denomination}) to early silver standard")
    
    conn.commit()
    print(f"✓ Updated {updated_count} pre-1837 coins to 89.24% silver standard")

def add_three_cent_silver(conn):
    """Add three-cent silver denomination (1851-1873)"""
    print("=== ADDING THREE-CENT SILVER DENOMINATION (1851-1873) ===")
    
    cursor = conn.cursor()
    
    # Check if already exists
    cursor.execute('SELECT COUNT(*) FROM coins WHERE coin_id LIKE "US-TRCS%"')
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"  Three-cent silver coins already exist ({existing_count} found)")
        return
    
    # Three-cent silver compositions
    type1_composition = {
        "alloy_name": "Type I Silver",
        "alloy": {"silver": 0.75, "copper": 0.25}
    }
    
    type2_composition = {
        "alloy_name": "Silver", 
        "alloy": {"silver": 0.9, "copper": 0.1}
    }
    
    # Representative three-cent silver coins (proper coin_id format)
    three_cent_coins = [
        {
            "coin_id": "US-TRCS-1851-P",
            "year": 1851,
            "composition": type1_composition,
            "notes": "First year - Type I, 75% silver",
            "business_strikes": 5447400
        },
        {
            "coin_id": "US-TRCS-1853-P", 
            "year": 1853,
            "composition": type1_composition,
            "notes": "Last year Type I - 75% silver",
            "business_strikes": 11400000
        },
        {
            "coin_id": "US-TRCS-1854-P",
            "year": 1854, 
            "composition": type2_composition,
            "notes": "First year Type II - 90% silver",
            "business_strikes": 671000
        },
        {
            "coin_id": "US-TRCS-1862-P",
            "year": 1862,
            "composition": type2_composition, 
            "notes": "Type III design - 90% silver",
            "business_strikes": 343000
        },
        {
            "coin_id": "US-TRCS-1873-P",
            "year": 1873,
            "composition": type2_composition,
            "notes": "Final year of three-cent silver",
            "business_strikes": 600
        }
    ]
    
    for coin in three_cent_coins:
        cursor.execute('''
            INSERT INTO coins (
                coin_id, series_id, country, denomination, series_name,
                year, mint, business_strikes, composition, weight_grams,
                diameter_mm, notes, source_citation, rarity,
                obverse_description, reverse_description,
                distinguishing_features, identification_keywords, common_names,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            coin["coin_id"], "three_cent_silver", "US", "Three Cents", "Three Cent Silver",
            coin["year"], "P", coin["business_strikes"],
            json.dumps(coin["composition"]), 0.80, 14.0,
            coin["notes"], "Red Book 2024",
            "key" if coin["business_strikes"] < 10000 else "scarce",
            "Six-pointed star with 'III' in center, 'UNITED STATES OF AMERICA' around, date below",
            "Roman numeral 'III' within C-shaped ornament of olive sprays, no legend", 
            "Tiny size (14mm), Silver composition varies by type, Six-pointed star design, Roman numeral III",
            "three cent silver, trime, 3 cent silver, tiny silver coin, star design, roman numeral three",
            "Three Cent Silver, Trime, Silver Trime, 3¢ Silver",
            datetime.now()
        ))
    
    conn.commit()
    print(f"✓ Added {len(three_cent_coins)} three-cent silver coins")

def fix_issues_table_face_values(conn):
    """Fix face values in issues table (half dimes should be 0.05, not 1.0)"""
    print("=== FIXING ISSUES TABLE FACE VALUES ===")
    
    cursor = conn.cursor()
    
    # Check current face values for half dimes
    cursor.execute('''
        SELECT issue_id, face_value, unit_name
        FROM issues 
        WHERE unit_name LIKE "%half dime%" OR unit_name LIKE "%Half Dime%"
    ''')
    
    half_dime_issues = cursor.fetchall()
    updated_count = 0
    
    for issue_id, face_value, unit_name in half_dime_issues:
        if face_value == 1.0:
            cursor.execute('''
                UPDATE issues SET face_value = 0.05 
                WHERE issue_id = ?
            ''', (issue_id,))
            updated_count += 1
            print(f"  Fixed {issue_id}: {unit_name} from {face_value} to 0.05")
    
    # Fix three-cent silver face value if it exists
    cursor.execute('''
        SELECT issue_id, face_value, unit_name
        FROM issues 
        WHERE unit_name LIKE "%three cent%" OR unit_name LIKE "%Three Cent%"
    ''')
    
    three_cent_issues = cursor.fetchall()
    
    for issue_id, face_value, unit_name in three_cent_issues:
        if face_value != 0.03:
            cursor.execute('''
                UPDATE issues SET face_value = 0.03
                WHERE issue_id = ?
            ''', (issue_id,))
            updated_count += 1
            print(f"  Fixed {issue_id}: {unit_name} from {face_value} to 0.03")
    
    conn.commit()
    if updated_count > 0:
        print(f"✓ Fixed {updated_count} face value issues")
    else:
        print("✓ No face value issues found in issues table")

def main():
    """Execute comprehensive composition corrections"""
    print("🔍 COMPREHENSIVE U.S. SILVER COIN COMPOSITION CORRECTIONS")
    print("=" * 60)
    
    conn = connect_db()
    
    try:
        # Phase 1: Critical Silver Periods
        print("\n📍 PHASE 1: CRITICAL SILVER PERIODS")
        add_war_nickels(conn)
        fix_dimes_clad_composition(conn)  
        fix_half_dollars_comprehensive(conn)
        
        # Phase 2: Historical Accuracy
        print("\n📍 PHASE 2: HISTORICAL ACCURACY")
        fix_pre_1837_silver_standard(conn)
        add_three_cent_silver(conn)
        fix_issues_table_face_values(conn)
        
        print("\n✅ ALL COMPOSITION CORRECTIONS COMPLETED")
        print("Database updated successfully - ready for export and validation")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        conn.rollback()
        sys.exit(1)
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()