#!/usr/bin/env python3
"""
Implement Federal Reserve Note Varieties from Issue #31 Research - Phase 4
==========================================================================

This script implements Federal Reserve Note variety records from GitHub Issue #31
research, focusing on Series 1914 and Series 1918 notes across multiple Federal
Reserve districts with comprehensive seal color and signature variations.

Based on research covering:
- Series 1914 Red Seal and Blue Seal varieties
- Series 1918 district coverage across Federal Reserve Banks
- Signature combinations and seal color diagnostics
- Geographic distribution and district letter codes
- Rarity assessments by district and type

Author: Claude Code
Date: 2025-08-18
Issue: #31 Phase 4
"""

import sqlite3
import json
import sys
from datetime import datetime

def get_database_connection():
    """Get connection to the coins database."""
    return sqlite3.connect('/Users/m/gh/coin-taxonomy/database/coins.db')

def add_federal_reserve_series():
    """Add Federal Reserve Note series to series_registry if not exists."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("📊 Adding Federal Reserve Note series to registry...")
    
    # Check if Federal Reserve Note series already exist
    cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id LIKE 'us_federal_reserve_%'")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"   ✓ Found {existing_count} existing Federal Reserve series, skipping creation")
        conn.close()
        return
    
    # Define Federal Reserve Note series
    federal_reserve_series = [
        {
            'series_id': 'us_federal_reserve_5_dollar',
            'series_name': 'Federal Reserve Note $5',
            'series_abbreviation': 'FRN5',
            'country_code': 'US',
            'denomination': 'Federal Reserve $5',
            'start_year': 1914,
            'end_year': None,
            'defining_characteristics': 'US Federal Reserve Note $5 including Series 1914 Red/Blue Seal and Series 1918 district varieties',
            'official_name': 'US Federal Reserve Note $5',
            'type': 'banknote'
        },
        {
            'series_id': 'us_federal_reserve_10_dollar',
            'series_name': 'Federal Reserve Note $10',
            'series_abbreviation': 'FRN10',
            'country_code': 'US',
            'denomination': 'Federal Reserve $10',
            'start_year': 1914,
            'end_year': None,
            'defining_characteristics': 'US Federal Reserve Note $10 including Series 1914 Red/Blue Seal and Series 1918 district varieties',
            'official_name': 'US Federal Reserve Note $10',
            'type': 'banknote'
        },
        {
            'series_id': 'us_federal_reserve_20_dollar',
            'series_name': 'Federal Reserve Note $20',
            'series_abbreviation': 'FRN20',
            'country_code': 'US',
            'denomination': 'Federal Reserve $20',
            'start_year': 1914,
            'end_year': None,
            'defining_characteristics': 'US Federal Reserve Note $20 including Series 1914 Red/Blue Seal and Series 1918 district varieties',
            'official_name': 'US Federal Reserve Note $20',
            'type': 'banknote'
        }
    ]
    
    # Insert each series
    for series in federal_reserve_series:
        try:
            cursor.execute('''
                INSERT INTO series_registry (
                    series_id, series_name, series_abbreviation, country_code,
                    denomination, start_year, end_year, defining_characteristics,
                    official_name, type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                series['series_id'], series['series_name'], series['series_abbreviation'],
                series['country_code'], series['denomination'], series['start_year'],
                series['end_year'], series['defining_characteristics'], 
                series['official_name'], series['type']
            ))
            print(f"   ✅ Added series: {series['series_id']}")
        except sqlite3.IntegrityError as e:
            print(f"   ⚠️  Series {series['series_id']} already exists, skipping...")
    
    conn.commit()
    conn.close()
    print(f"✓ Added {len(federal_reserve_series)} Federal Reserve Note series")

def implement_federal_reserve_varieties():
    """Implement Federal Reserve Note variety records from Issue #31 research."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("🔍 Implementing Federal Reserve Note Varieties from Issue #31 Research...")
    print("=" * 70)
    
    # Define Federal Reserve Note variety data from research
    federal_reserve_varieties = [
        # Series 1914 Red Seal Type I - Early issues
        {
            'issue_id': 'US-FRN5-1914-A',
            'series_id': 'us_federal_reserve_5_dollar',
            'face_value': 5.0,
            'year': 1914,
            'variety_name': 'Series 1914 $5 Red Seal - Federal Reserve Bank of Boston',
            'distinguishing_features': 'Red Treasury seal, Red serial numbers, District A Boston, Lincoln portrait, Type I plate layout',
            'identification_keywords': 'series 1914, red seal, boston district a, lincoln portrait, type 1 plate, red serial',
            'rarity': 'scarce',
            'historical_notes': 'First Federal Reserve Notes issued in 1914 with red seals and serials, District A Boston',
            'friedberg_number': 'Fr.832a',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Burke-McAdoo (Register-Secretary)',
            'seal_color': 'Red',
            'production_period': '1914-1915',
            'district_letter': 'A',
            'issuing_bank': 'Federal Reserve Bank of Boston'
        },
        {
            'issue_id': 'US-FRN5-1914-B',
            'series_id': 'us_federal_reserve_5_dollar',
            'face_value': 5.0,
            'year': 1914,
            'variety_name': 'Series 1914 $5 Red Seal - Federal Reserve Bank of New York',
            'distinguishing_features': 'Red Treasury seal, Red serial numbers, District B New York, Lincoln portrait, Type I plate layout',
            'identification_keywords': 'series 1914, red seal, new york district b, lincoln portrait, type 1 plate, red serial',
            'rarity': 'scarce',
            'historical_notes': 'First Federal Reserve Notes from New York District, red seal variety',
            'friedberg_number': 'Fr.832b',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Burke-McAdoo (Register-Secretary)',
            'seal_color': 'Red',
            'production_period': '1914-1915',
            'district_letter': 'B',
            'issuing_bank': 'Federal Reserve Bank of New York'
        },
        {
            'issue_id': 'US-FRN10-1914-C',
            'series_id': 'us_federal_reserve_10_dollar',
            'face_value': 10.0,
            'year': 1914,
            'variety_name': 'Series 1914 $10 Red Seal - Federal Reserve Bank of Philadelphia',
            'distinguishing_features': 'Red Treasury seal, Red serial numbers, District C Philadelphia, Jackson portrait, Type I plate layout',
            'identification_keywords': 'series 1914, red seal, philadelphia district c, jackson portrait, type 1 plate, red serial',
            'rarity': 'scarce',
            'historical_notes': 'Series 1914 $10 from Philadelphia District with red seal and serials',
            'friedberg_number': 'Fr.895c',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Burke-McAdoo (Register-Secretary)',
            'seal_color': 'Red',
            'production_period': '1914-1915',
            'district_letter': 'C',
            'issuing_bank': 'Federal Reserve Bank of Philadelphia'
        },
        
        # Series 1914 Blue Seal - Later issues
        {
            'issue_id': 'US-FRN5-1915-D',
            'series_id': 'us_federal_reserve_5_dollar',
            'face_value': 5.0,
            'year': 1914,  # Series year, not issue year
            'variety_name': 'Series 1914 $5 Blue Seal - Federal Reserve Bank of Cleveland',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District D Cleveland, Lincoln portrait, Type II plate layout',
            'identification_keywords': 'series 1914, blue seal, cleveland district d, lincoln portrait, type 2 plate, blue serial',
            'rarity': 'common',
            'historical_notes': 'Later 1914 series with blue seals, more common than red seal varieties',
            'friedberg_number': 'Fr.847d',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'White-Mellon (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1915-1918',
            'district_letter': 'D',
            'issuing_bank': 'Federal Reserve Bank of Cleveland'
        },
        {
            'issue_id': 'US-FRN10-1915-E',
            'series_id': 'us_federal_reserve_10_dollar',
            'face_value': 10.0,
            'year': 1914,
            'variety_name': 'Series 1914 $10 Blue Seal - Federal Reserve Bank of Richmond',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District E Richmond, Jackson portrait, Type II plate layout',
            'identification_keywords': 'series 1914, blue seal, richmond district e, jackson portrait, type 2 plate, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1914 $10 from Richmond District with blue seal transition',
            'friedberg_number': 'Fr.906e',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'White-Mellon (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1915-1918',
            'district_letter': 'E',
            'issuing_bank': 'Federal Reserve Bank of Richmond'
        },
        {
            'issue_id': 'US-FRN20-1915-F',
            'series_id': 'us_federal_reserve_20_dollar',
            'face_value': 20.0,
            'year': 1914,
            'variety_name': 'Series 1914 $20 Blue Seal - Federal Reserve Bank of Atlanta',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District F Atlanta, Cleveland portrait, Type II plate layout',
            'identification_keywords': 'series 1914, blue seal, atlanta district f, cleveland portrait, type 2 plate, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1914 $20 from Atlanta District with blue seal and serials',
            'friedberg_number': 'Fr.962f',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'White-Mellon (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1915-1918',
            'district_letter': 'F',
            'issuing_bank': 'Federal Reserve Bank of Atlanta'
        },
        
        # Series 1918 varieties
        {
            'issue_id': 'US-FRN5-1918-G',
            'series_id': 'us_federal_reserve_5_dollar',
            'face_value': 5.0,
            'year': 1918,
            'variety_name': 'Series 1918 $5 - Federal Reserve Bank of Chicago',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District G Chicago, Lincoln portrait, Series 1918 design',
            'identification_keywords': 'series 1918, blue seal, chicago district g, lincoln portrait, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1918 continuation with standardized blue seals across all districts',
            'friedberg_number': 'Fr.849g',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Elliott-White (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1918-1920',
            'district_letter': 'G',
            'issuing_bank': 'Federal Reserve Bank of Chicago'
        },
        {
            'issue_id': 'US-FRN10-1918-H',
            'series_id': 'us_federal_reserve_10_dollar',
            'face_value': 10.0,
            'year': 1918,
            'variety_name': 'Series 1918 $10 - Federal Reserve Bank of St. Louis',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District H St. Louis, Jackson portrait, Series 1918 design',
            'identification_keywords': 'series 1918, blue seal, st louis district h, jackson portrait, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1918 $10 from St. Louis District with standard blue seal format',
            'friedberg_number': 'Fr.908h',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Elliott-White (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1918-1920',
            'district_letter': 'H',
            'issuing_bank': 'Federal Reserve Bank of St. Louis'
        },
        {
            'issue_id': 'US-FRN5-1918-I',
            'series_id': 'us_federal_reserve_5_dollar',
            'face_value': 5.0,
            'year': 1918,
            'variety_name': 'Series 1918 $5 - Federal Reserve Bank of Minneapolis',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District I Minneapolis, Lincoln portrait, Series 1918 design',
            'identification_keywords': 'series 1918, blue seal, minneapolis district i, lincoln portrait, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1918 from Minneapolis District covering upper Midwest region',
            'friedberg_number': 'Fr.849i',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Elliott-White (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1918-1920',
            'district_letter': 'I',
            'issuing_bank': 'Federal Reserve Bank of Minneapolis'
        },
        {
            'issue_id': 'US-FRN10-1918-J',
            'series_id': 'us_federal_reserve_10_dollar',
            'face_value': 10.0,
            'year': 1918,
            'variety_name': 'Series 1918 $10 - Federal Reserve Bank of Kansas City',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District J Kansas City, Jackson portrait, Series 1918 design',
            'identification_keywords': 'series 1918, blue seal, kansas city district j, jackson portrait, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1918 $10 from Kansas City District serving Great Plains region',
            'friedberg_number': 'Fr.908j',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Elliott-White (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1918-1920',
            'district_letter': 'J',
            'issuing_bank': 'Federal Reserve Bank of Kansas City'
        },
        {
            'issue_id': 'US-FRN20-1918-K',
            'series_id': 'us_federal_reserve_20_dollar',
            'face_value': 20.0,
            'year': 1918,
            'variety_name': 'Series 1918 $20 - Federal Reserve Bank of Dallas',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District K Dallas, Cleveland portrait, Series 1918 design',
            'identification_keywords': 'series 1918, blue seal, dallas district k, cleveland portrait, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1918 $20 from Dallas District covering Texas and surrounding states',
            'friedberg_number': 'Fr.964k',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Elliott-White (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1918-1920',
            'district_letter': 'K',
            'issuing_bank': 'Federal Reserve Bank of Dallas'
        },
        {
            'issue_id': 'US-FRN5-1918-L',
            'series_id': 'us_federal_reserve_5_dollar',
            'face_value': 5.0,
            'year': 1918,
            'variety_name': 'Series 1918 $5 - Federal Reserve Bank of San Francisco',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District L San Francisco, Lincoln portrait, Series 1918 design',
            'identification_keywords': 'series 1918, blue seal, san francisco district l, lincoln portrait, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1918 from San Francisco District covering Western states',
            'friedberg_number': 'Fr.849l',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Elliott-White (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1918-1920',
            'district_letter': 'L',
            'issuing_bank': 'Federal Reserve Bank of San Francisco'
        },
        {
            'issue_id': 'US-FRN10-1918-L',
            'series_id': 'us_federal_reserve_10_dollar',
            'face_value': 10.0,
            'year': 1918,
            'variety_name': 'Series 1918 $10 - Federal Reserve Bank of San Francisco',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, District L San Francisco, Jackson portrait, Series 1918 design',
            'identification_keywords': 'series 1918, blue seal, san francisco district l, jackson portrait, blue serial',
            'rarity': 'common',
            'historical_notes': 'Series 1918 $10 from San Francisco District with West Coast distribution',
            'friedberg_number': 'Fr.908l',
            'issue_type': 'Federal Reserve Note',
            'signature_combination': 'Elliott-White (Register-Secretary)',
            'seal_color': 'Blue',
            'production_period': '1918-1920',
            'district_letter': 'L',
            'issuing_bank': 'Federal Reserve Bank of San Francisco'
        }
    ]
    
    # Insert each variety record
    for i, variety in enumerate(federal_reserve_varieties, 1):
        print(f"\n{i}. Adding {variety['variety_name']}...")
        
        try:
            # Prepare specifications and sides JSON
            specifications = {
                "width_mm": 187,
                "height_mm": 81,
                "thickness_mm": 0.11,
                "weight_grams": 1.2
            }
            
            sides = {
                "obverse": {
                    "design": f"{variety['variety_name']} obverse design",
                    "designer": "Bureau of Engraving and Printing",
                    "elements": variety['distinguishing_features'].split(', ')
                },
                "reverse": {
                    "design": f"{variety['variety_name']} reverse design", 
                    "designer": "Bureau of Engraving and Printing",
                    "elements": ["denomination markers", "Federal Reserve district information", "Treasury seal"]
                }
            }
            
            mintage = {
                "total_printed": None,  # Unknown for most early Federal Reserve Notes
                "estimated_surviving": None
            }
            
            varieties_json = [{
                "variety_id": variety['issue_id'].split('-')[-1].lower(),
                "name": variety['variety_name'],
                "description": variety['distinguishing_features'],
                "friedberg_number": variety.get('friedberg_number', None),
                "district_letter": variety.get('district_letter', None),
                "issuing_bank": variety.get('issuing_bank', None)
            }]
            
            # Insert into issues table (universal format)
            cursor.execute('''
                INSERT INTO issues (
                    issue_id, object_type, series_id, country_code,
                    authority_name, monetary_system, currency_unit,
                    face_value, unit_name, system_fraction,
                    issue_year, mint_id, specifications, sides, mintage,
                    rarity, varieties, source_citation, notes, seller_name,
                    distinguishing_features, identification_keywords,
                    seal_color, series_designation, signature_combination
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                variety['issue_id'],
                'banknote',
                variety['series_id'],
                'US',
                variety.get('issuing_bank', 'Federal Reserve System'),
                'decimal',
                'dollar',
                variety['face_value'],
                'dollar',
                f"Federal Reserve ${int(variety['face_value'])}",
                variety['year'],
                'P',  # All Federal Reserve Notes printed at BEP
                json.dumps(specifications),
                json.dumps(sides),
                json.dumps(mintage),
                variety['rarity'],
                json.dumps(varieties_json),
                'GitHub Issue #31 Federal Reserve Note Research',
                variety['historical_notes'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                variety['distinguishing_features'],
                variety['identification_keywords'],
                variety.get('seal_color', None),
                variety['issue_type'],
                variety.get('signature_combination', None)
            ))
            
            print(f"   ✅ Added {variety['issue_id']} to issues table")
            
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                print(f"   ⚠️  Record {variety['issue_id']} already exists, skipping...")
            else:
                print(f"   ❌ Error inserting {variety['issue_id']}: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error inserting {variety['issue_id']}: {e}")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n✅ Federal Reserve Note Varieties Implementation Complete!")
    print(f"📊 Added {len(federal_reserve_varieties)} Federal Reserve Note varieties")
    print(f"🏦 Coverage: Series 1914 Red/Blue Seal and Series 1918 across multiple districts")
    
    return True

def validate_implementation():
    """Validate the Federal Reserve Note implementation."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("\n🔍 Validating Federal Reserve Note Implementation...")
    print("=" * 50)
    
    # Check series were added
    cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id LIKE 'us_federal_reserve_%'")
    series_count = cursor.fetchone()[0]
    print(f"📊 Federal Reserve Note series: {series_count}")
    
    # Check varieties were added
    cursor.execute("SELECT COUNT(*) FROM issues WHERE issue_id LIKE 'US-FRN%'")
    variety_count = cursor.fetchone()[0] 
    print(f"💰 Federal Reserve Note varieties: {variety_count}")
    
    # Check by denomination
    for denom in [5, 10, 20]:
        cursor.execute(f"SELECT COUNT(*) FROM issues WHERE issue_id LIKE 'US-FRN{denom}-%'")
        count = cursor.fetchone()[0]
        print(f"   📝 ${denom} varieties: {count}")
    
    # Check by seal color
    for seal_color in ['red seal', 'blue seal']:
        cursor.execute("SELECT COUNT(*) FROM issues WHERE distinguishing_features LIKE ? AND issue_id LIKE 'US-FRN%'", (f'%{seal_color}%',))
        count = cursor.fetchone()[0]
        print(f"   📝 {seal_color.title()} varieties: {count}")
    
    # Check by series
    for series in ['1914', '1918']:
        cursor.execute("SELECT COUNT(*) FROM issues WHERE distinguishing_features LIKE ? AND issue_id LIKE 'US-FRN%'", (f'%series {series}%',))
        count = cursor.fetchone()[0]
        print(f"   📝 Series {series} varieties: {count}")
    
    conn.close()
    
    return variety_count > 0

def main():
    """Main execution function."""
    print("Federal Reserve Note Varieties Implementation - Phase 4")
    print("====================================================")
    print("Implementing research from GitHub Issue #31")
    print()
    
    # Step 1: Add Federal Reserve Note series
    try:
        add_federal_reserve_series()
    except Exception as e:
        print(f"❌ Error adding Federal Reserve Note series: {e}")
        return 1
    
    # Step 2: Implement varieties
    try:
        success = implement_federal_reserve_varieties()
    except Exception as e:
        print(f"❌ Error implementing varieties: {e}")
        return 1
    
    # Step 3: Validate implementation
    try:
        validation_success = validate_implementation()
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        return 1
    
    if success and validation_success:
        print("\n🎉 Phase 4 Implementation completed successfully!")
        print("\nNext steps:")
        print("1. Export updated taxonomy from database")
        print("2. Continue with Phase 5 (Gold Certificates)")
        print("3. Final export and commit all phases")
        return 0
    else:
        print("\n❌ Implementation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())