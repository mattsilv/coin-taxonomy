#!/usr/bin/env python3
"""
Standing Liberty Quarter Implementation Script
Implements Type I and Type II varieties from GitHub Issue #28 research
"""

import sqlite3
import sys
from datetime import datetime

def connect_to_database():
    """Connect to the coins database"""
    return sqlite3.connect('database/coins.db')

def add_standing_liberty_series(cursor):
    """Add Standing Liberty Quarter series to series_registry"""
    
    series_data = {
        'series_id': 'us_standing_liberty_quarter',
        'series_name': 'Standing Liberty Quarter',
        'series_abbreviation': 'SLQ',
        'country_code': 'US',
        'denomination': 'Quarter Dollar',
        'start_year': 1916,
        'end_year': 1930,
        'defining_characteristics': 'Features Type I (1916-early 1917) and Type II (mid-1917-1930) varieties with different Full Head criteria',
        'official_name': 'Standing Liberty Quarter',
        'type': 'coin'
    }
    
    # Check if series already exists
    cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id = ?", (series_data['series_id'],))
    if cursor.fetchone()[0] > 0:
        print(f"Series {series_data['series_id']} already exists, skipping...")
        return
        
    # Insert series
    cursor.execute("""
        INSERT INTO series_registry (
            series_id, series_name, series_abbreviation, country_code, denomination,
            start_year, end_year, defining_characteristics, official_name, type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        series_data['series_id'], series_data['series_name'], series_data['series_abbreviation'],
        series_data['country_code'], series_data['denomination'], series_data['start_year'],
        series_data['end_year'], series_data['defining_characteristics'], series_data['official_name'],
        series_data['type']
    ))
    
    print(f"Added series: {series_data['series_name']}")

def add_standing_liberty_varieties(cursor):
    """Add Standing Liberty Quarter Type I and Type II varieties"""
    
    # 1917 Standing Liberty Quarter varieties with Type I/Type II suffixes
    standing_liberty_varieties = [
        {
            'issue_id': 'US-SLQ-1917-P-T1',
            'series_id': 'us_standing_liberty_quarter',
            'year': 1917,
            'mint_mark': 'P',
            'face_value': 0.25,
            'metal_composition': 'Silver (90% Ag, 10% Cu)',
            'weight_grams': 6.25,
            'diameter_mm': 24.3,
            'edge': 'Reeded',
            'designer': 'Hermon Atkins MacNeil',
            'obverse_description': 'Standing Liberty with exposed right breast, stars around border',
            'reverse_description': 'Eagle in flight lower on reverse, 13 stars around legends',
            'mintage': 8740000,
            'rarity_rating': 'Common',
            'type_designation': 'Type I',
            'distinguishing_features': 'Exposed breast, eagle positioned lower on reverse, 13 stars only',
            'full_head_criteria': 'Clear separation between hair cords and cap (Type I FH standard)',
            'design_notes': 'Original design released January 17, 1917, produced until mid-February redesign',
            'source_citation': 'GitHub Issue #28 Standing Liberty Quarter Research'
        },
        {
            'issue_id': 'US-SLQ-1917-P-T2',
            'series_id': 'us_standing_liberty_quarter',
            'year': 1917,
            'mint_mark': 'P',
            'face_value': 0.25,
            'metal_composition': 'Silver (90% Ag, 10% Cu)',
            'weight_grams': 6.25,
            'diameter_mm': 24.3,
            'edge': 'Reeded',
            'designer': 'Hermon Atkins MacNeil',
            'obverse_description': 'Standing Liberty with chainmail shirt covering torso',
            'reverse_description': 'Eagle repositioned higher/centered, three additional stars below eagle',
            'mintage': 13880000,
            'rarity_rating': 'Common',
            'type_designation': 'Type II',
            'distinguishing_features': 'Chainmail covering torso, eagle repositioned higher, 16 total stars (3 below eagle)',
            'full_head_criteria': 'Three complete helmet leaves, defined ear hole, full helmet bottom outline (Type II FH standard)',
            'design_notes': 'Redesigned mid-February 1917 after Congressional authorization July 9, 1917',
            'source_citation': 'GitHub Issue #28 Standing Liberty Quarter Research'
        },
        {
            'issue_id': 'US-SLQ-1917-D-T1',
            'series_id': 'us_standing_liberty_quarter',
            'year': 1917,
            'mint_mark': 'D',
            'face_value': 0.25,
            'metal_composition': 'Silver (90% Ag, 10% Cu)',
            'weight_grams': 6.25,
            'diameter_mm': 24.3,
            'edge': 'Reeded',
            'designer': 'Hermon Atkins MacNeil',
            'obverse_description': 'Standing Liberty with exposed right breast, stars around border',
            'reverse_description': 'Eagle in flight lower on reverse, 13 stars around legends',
            'mintage': None,  # Exact split not available in sources
            'rarity_rating': 'Scarce',
            'type_designation': 'Type I',
            'distinguishing_features': 'Exposed breast, eagle positioned lower on reverse, 13 stars only',
            'full_head_criteria': 'Clear separation between hair cords and cap (Type I FH standard)',
            'design_notes': 'Denver mint Type I variety, produced early 1917 before redesign',
            'source_citation': 'GitHub Issue #28 Standing Liberty Quarter Research'
        },
        {
            'issue_id': 'US-SLQ-1917-D-T2',
            'series_id': 'us_standing_liberty_quarter',
            'year': 1917,
            'mint_mark': 'D',
            'face_value': 0.25,
            'metal_composition': 'Silver (90% Ag, 10% Cu)',
            'weight_grams': 6.25,
            'diameter_mm': 24.3,
            'edge': 'Reeded',
            'designer': 'Hermon Atkins MacNeil',
            'obverse_description': 'Standing Liberty with chainmail shirt covering torso',
            'reverse_description': 'Eagle repositioned higher/centered, three additional stars below eagle',
            'mintage': None,  # Exact split not available in sources
            'rarity_rating': 'Common',
            'type_designation': 'Type II',
            'distinguishing_features': 'Chainmail covering torso, eagle repositioned higher, 16 total stars (3 below eagle)',
            'full_head_criteria': 'Three complete helmet leaves, defined ear hole, full helmet bottom outline (Type II FH standard)',
            'design_notes': 'Denver mint Type II variety, produced mid-1917 after redesign',
            'source_citation': 'GitHub Issue #28 Standing Liberty Quarter Research'
        },
        {
            'issue_id': 'US-SLQ-1917-S-T1',
            'series_id': 'us_standing_liberty_quarter',
            'year': 1917,
            'mint_mark': 'S',
            'face_value': 0.25,
            'metal_composition': 'Silver (90% Ag, 10% Cu)',
            'weight_grams': 6.25,
            'diameter_mm': 24.3,
            'edge': 'Reeded',
            'designer': 'Hermon Atkins MacNeil',
            'obverse_description': 'Standing Liberty with exposed right breast, stars around border',
            'reverse_description': 'Eagle in flight lower on reverse, 13 stars around legends',
            'mintage': None,  # Type I portion not specified, but preceded Type II
            'rarity_rating': 'Scarce',
            'type_designation': 'Type I',
            'distinguishing_features': 'Exposed breast, eagle positioned lower on reverse, 13 stars only',
            'full_head_criteria': 'Clear separation between hair cords and cap (Type I FH standard)',
            'design_notes': 'San Francisco mint Type I variety, preceded Type II redesign',
            'source_citation': 'GitHub Issue #28 Standing Liberty Quarter Research'
        },
        {
            'issue_id': 'US-SLQ-1917-S-T2',
            'series_id': 'us_standing_liberty_quarter',
            'year': 1917,
            'mint_mark': 'S',
            'face_value': 0.25,
            'metal_composition': 'Silver (90% Ag, 10% Cu)',
            'weight_grams': 6.25,
            'diameter_mm': 24.3,
            'edge': 'Reeded',
            'designer': 'Hermon Atkins MacNeil',
            'obverse_description': 'Standing Liberty with chainmail shirt covering torso',
            'reverse_description': 'Eagle repositioned higher/centered, three additional stars below eagle',
            'mintage': 5522000,
            'rarity_rating': 'Common',
            'type_designation': 'Type II',
            'distinguishing_features': 'Chainmail covering torso, eagle repositioned higher, 16 total stars (3 below eagle)',
            'full_head_criteria': 'Three complete helmet leaves, defined ear hole, full helmet bottom outline (Type II FH standard)',
            'design_notes': 'San Francisco mint Type II variety, 5,522,000 post-redesign mintage',
            'source_citation': 'GitHub Issue #28 Standing Liberty Quarter Research'
        },
    ]
    
    added_count = 0
    for variety in standing_liberty_varieties:
        # Check if variety already exists
        cursor.execute("SELECT COUNT(*) FROM issues WHERE issue_id = ?", (variety['issue_id'],))
        if cursor.fetchone()[0] > 0:
            print(f"Variety {variety['issue_id']} already exists, skipping...")
            continue
            
        # Insert variety using schema-compatible approach
        cursor.execute("""
            INSERT INTO issues (
                issue_id, object_type, series_id, country_code, authority_name, 
                monetary_system, currency_unit, face_value, unit_name, issue_year,
                mint_id, specifications, sides, mintage, rarity, 
                source_citation, notes, obverse_description, reverse_description,
                distinguishing_features, type_designation, full_head_criteria
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            variety['issue_id'], 
            'coin',  # object_type
            variety['series_id'], 
            'US',  # country_code
            'United States Mint',  # authority_name
            'decimal',  # monetary_system
            'USD',  # currency_unit
            variety['face_value'], 
            'Quarter Dollar',  # unit_name
            variety['year'],  # issue_year
            variety['mint_mark'],  # mint_id
            f'{{"weight_grams": {variety["weight_grams"]}, "diameter_mm": {variety["diameter_mm"]}, "edge": "{variety["edge"]}"}}',  # specifications JSON
            f'{{"obverse": {{"design": "{variety["obverse_description"]}", "designer": "{variety["designer"]}"}}, "reverse": {{"design": "{variety["reverse_description"]}", "designer": "{variety["designer"]}"}}}}',  # sides JSON
            f'{{"business_strikes": {variety["mintage"] if variety["mintage"] else "null"}}}',  # mintage JSON
            variety['rarity_rating'].lower(),  # rarity
            variety['source_citation'], 
            variety['design_notes'],  # notes
            variety['obverse_description'], 
            variety['reverse_description'],
            variety['distinguishing_features'], 
            variety['type_designation'], 
            variety['full_head_criteria']
        ))
        
        print(f"Added variety: {variety['issue_id']} - {variety['type_designation']}")
        added_count += 1
    
    return added_count

def validate_implementation(cursor):
    """Validate the Standing Liberty Quarter implementation"""
    
    # Check series was added
    cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id = 'us_standing_liberty_quarter'")
    series_count = cursor.fetchone()[0]
    
    # Check varieties were added
    cursor.execute("SELECT COUNT(*) FROM issues WHERE issue_id LIKE 'US-SLQ-1917-%'")
    variety_count = cursor.fetchone()[0]
    
    # Check Type I vs Type II distribution
    cursor.execute("SELECT type_designation, COUNT(*) FROM issues WHERE issue_id LIKE 'US-SLQ-1917-%' GROUP BY type_designation")
    type_distribution = cursor.fetchall()
    
    print(f"\nValidation Results:")
    print(f"Series added: {series_count}")
    print(f"1917 varieties added: {variety_count}")
    print(f"Type distribution: {dict(type_distribution)}")
    
    # Display mintage data for verification
    cursor.execute("""
        SELECT issue_id, type_designation, mint_id, mintage 
        FROM issues 
        WHERE issue_id LIKE 'US-SLQ-1917-%' 
        ORDER BY mint_id, type_designation
    """)
    
    print(f"\nMintage Summary:")
    for row in cursor.fetchall():
        issue_id, type_des, mint_mark, mintage_json = row
        # Parse JSON to get business_strikes
        if mintage_json and 'business_strikes' in mintage_json:
            import json
            mintage_data = json.loads(mintage_json)
            mintage = mintage_data.get('business_strikes')
            mintage_str = f"{mintage:,}" if mintage and mintage != 'null' else "Not specified"
        else:
            mintage_str = "Not specified"
        print(f"  {issue_id}: {mintage_str}")

def main():
    """Main implementation function"""
    print("Standing Liberty Quarter Implementation - GitHub Issue #28")
    print("=" * 60)
    
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        
        # Add series
        add_standing_liberty_series(cursor)
        
        # Add varieties
        variety_count = add_standing_liberty_varieties(cursor)
        
        # Validate implementation
        validate_implementation(cursor)
        
        # Commit changes
        conn.commit()
        print(f"\n✅ Successfully added {variety_count} Standing Liberty Quarter varieties")
        print(f"Implementation complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()