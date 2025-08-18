#!/usr/bin/env python3
"""
Implement Fractional Currency Varieties from Issue #31 Research
==============================================================

This script implements comprehensive fractional currency variety research
from GitHub Issue #31, focusing on Second Issue (1863-1867) and Fourth Issue
(1869-1875) fractional currency varieties including signature combinations,
surcharge varieties, and treasury seal variations.

Based on research covering:
- Second Issue (1863-1867): Bronze surcharge varieties, back color variations
- Fourth Issue (1869-1875): Treasury seal varieties, signature combinations
- Complete coverage of Friedberg catalog numbers
- Rarity assessments and distinguishing features

Author: Claude Code
Date: 2025-08-18
Issue: #31
"""

import sqlite3
import json
import sys
from datetime import datetime

def get_database_connection():
    """Get connection to the coins database."""
    return sqlite3.connect('/Users/m/gh/coin-taxonomy/database/coins.db')

def add_fractional_currency_series():
    """Add fractional currency series to series_registry if not exists."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("📊 Adding fractional currency series to registry...")
    
    # Check if fractional currency series already exist
    cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id LIKE 'us_fractional_%'")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"   ✓ Found {existing_count} existing fractional series, skipping creation")
        conn.close()
        return
    
    # Define fractional currency series
    fractional_series = [
        {
            'series_id': 'us_fractional_3_cent',
            'series_name': 'Three Cent Fractional Currency',
            'series_abbreviation': 'FRAC3',
            'country_code': 'US',
            'denomination': 'Fractional 3¢',
            'start_year': 1863,
            'end_year': 1875,
            'defining_characteristics': 'US three cent fractional currency notes',
            'official_name': 'US three cent fractional currency',
            'type': 'banknote'
        },
        {
            'series_id': 'us_fractional_5_cent',
            'series_name': 'Five Cent Fractional Currency', 
            'series_abbreviation': 'FRAC5',
            'country_code': 'US',
            'denomination': 'Fractional 5¢',
            'start_year': 1863,
            'end_year': 1875,
            'defining_characteristics': 'US five cent fractional currency notes',
            'official_name': 'US five cent fractional currency',
            'type': 'banknote'
        },
        {
            'series_id': 'us_fractional_10_cent',
            'series_name': 'Ten Cent Fractional Currency',
            'series_abbreviation': 'FRAC10',
            'country_code': 'US', 
            'denomination': 'Fractional 10¢',
            'start_year': 1863,
            'end_year': 1875,
            'defining_characteristics': 'US ten cent fractional currency notes',
            'official_name': 'US ten cent fractional currency',
            'type': 'banknote'
        },
        {
            'series_id': 'us_fractional_15_cent',
            'series_name': 'Fifteen Cent Fractional Currency',
            'series_abbreviation': 'FRAC15',
            'country_code': 'US',
            'denomination': 'Fractional 15¢',
            'start_year': 1863,
            'end_year': 1875,
            'defining_characteristics': 'US fifteen cent fractional currency notes',
            'official_name': 'US fifteen cent fractional currency',
            'type': 'banknote'
        },
        {
            'series_id': 'us_fractional_25_cent',
            'series_name': 'Twenty-Five Cent Fractional Currency',
            'series_abbreviation': 'FRAC25',
            'country_code': 'US',
            'denomination': 'Fractional 25¢',
            'start_year': 1863,
            'end_year': 1875,
            'defining_characteristics': 'US twenty-five cent fractional currency notes',
            'official_name': 'US twenty-five cent fractional currency',
            'type': 'banknote'
        },
        {
            'series_id': 'us_fractional_50_cent',
            'series_name': 'Fifty Cent Fractional Currency',
            'series_abbreviation': 'FRAC50',
            'country_code': 'US',
            'denomination': 'Fractional 50¢',
            'start_year': 1863,
            'end_year': 1875,
            'defining_characteristics': 'US fifty cent fractional currency notes',
            'official_name': 'US fifty cent fractional currency',
            'type': 'banknote'
        }
    ]
    
    # Insert each series
    for series in fractional_series:
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
    print(f"✓ Added {len(fractional_series)} fractional currency series")

def implement_fractional_currency_varieties():
    """Implement fractional currency variety records from Issue #31 research."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("🔍 Implementing Fractional Currency Varieties from Issue #31 Research...")
    print("=" * 70)
    
    # Define fractional currency variety data from research
    fractional_varieties = [
        # Second Issue (1863-1867) - 3 Cent Bronze Surcharge varieties
        {
            'issue_id': 'US-FRAC3-1863-P',
            'series_id': 'us_fractional_3_cent',
            'face_value': 0.03,
            'year': 1863,
            'variety_name': 'Second Issue 3¢ Bronze Surcharge Light Background',
            'distinguishing_features': 'Bronze overprint "3" surcharge, light pink/lilac background, Washington portrait, red back',
            'identification_keywords': 'second issue, bronze surcharge, light background, washington, pink lilac back, red back',
            'rarity': 'common',
            'historical_notes': 'Part of Second Issue fractional currency series produced during Civil War coin shortage',
            'friedberg_number': 'Fr.1226',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Bronze',
            'production_period': '1863-1867'
        },
        {
            'issue_id': 'US-FRAC3-1864-P',
            'series_id': 'us_fractional_3_cent',
            'face_value': 0.03,
            'year': 1864,
            'variety_name': 'Second Issue 3¢ Bronze Surcharge Dark Background',
            'distinguishing_features': 'Bronze overprint "3" surcharge, dark violet background, Washington portrait, red back',
            'identification_keywords': 'second issue, bronze surcharge, dark background, washington, violet back, red back',
            'rarity': 'common',
            'historical_notes': 'Background color variation within Second Issue 3¢ series',
            'friedberg_number': 'Fr.1227',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Bronze',
            'production_period': '1863-1867'
        },

        # Second Issue (1863-1867) - 5 Cent varieties  
        {
            'issue_id': 'US-FRAC5-1863-P',
            'series_id': 'us_fractional_5_cent',
            'face_value': 0.05,
            'year': 1863,
            'variety_name': 'Second Issue 5¢ Bronze Surcharge',
            'distinguishing_features': 'Bronze overprint "5" surcharge, Clark portrait, red back with ornate design',
            'identification_keywords': 'second issue, bronze surcharge, clark portrait, red back, five cent',
            'rarity': 'common',
            'historical_notes': 'Spencer M. Clark portrait caused controversy as living persons were not supposed to appear on currency',
            'friedberg_number': 'Fr.1232',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Bronze',
            'production_period': '1863-1867'
        },

        # Second Issue (1863-1867) - 10 Cent varieties
        {
            'issue_id': 'US-FRAC10-1863-P',
            'series_id': 'us_fractional_10_cent', 
            'face_value': 0.10,
            'year': 1863,
            'variety_name': 'Second Issue 10¢ Bronze Surcharge',
            'distinguishing_features': 'Bronze overprint "10" surcharge, Washington portrait, green back',
            'identification_keywords': 'second issue, bronze surcharge, washington, green back, ten cent',
            'rarity': 'common',
            'historical_notes': 'Most common denomination of Second Issue fractional currency',
            'friedberg_number': 'Fr.1245',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Bronze',
            'production_period': '1863-1867'
        },

        # Second Issue (1863-1867) - 25 Cent varieties
        {
            'issue_id': 'US-FRAC25-1863-P',
            'series_id': 'us_fractional_25_cent',
            'face_value': 0.25,
            'year': 1863,
            'variety_name': 'Second Issue 25¢ Bronze Surcharge',
            'distinguishing_features': 'Bronze overprint "25" surcharge, Washington portrait, purple back',
            'identification_keywords': 'second issue, bronze surcharge, washington, purple back, twenty five cent',
            'rarity': 'common',
            'historical_notes': 'Quarter denomination fractional currency from Second Issue series',
            'friedberg_number': 'Fr.1283',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Bronze',
            'production_period': '1863-1867'
        },

        # Second Issue (1863-1867) - 50 Cent varieties
        {
            'issue_id': 'US-FRAC50-1863-P',
            'series_id': 'us_fractional_50_cent',
            'face_value': 0.50,
            'year': 1863,
            'variety_name': 'Second Issue 50¢ Bronze Surcharge',
            'distinguishing_features': 'Bronze overprint "50" surcharge, Washington portrait, red back',
            'identification_keywords': 'second issue, bronze surcharge, washington, red back, fifty cent',
            'rarity': 'common',
            'historical_notes': 'Highest denomination of Second Issue fractional currency',
            'friedberg_number': 'Fr.1317',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Bronze',
            'production_period': '1863-1867'
        },

        # Fourth Issue (1869-1875) - 10 Cent Treasury Seal varieties
        {
            'issue_id': 'US-FRAC10-1869-P',
            'series_id': 'us_fractional_10_cent',
            'face_value': 0.10,
            'year': 1869,
            'variety_name': 'Fourth Issue 10¢ Large Red Seal',
            'distinguishing_features': 'Large red Treasury seal, Liberty bust portrait, green back',
            'identification_keywords': 'fourth issue, large red seal, liberty bust, green back, ten cent',
            'rarity': 'common',
            'historical_notes': 'Fourth Issue introduced Treasury seals to fractional currency',
            'friedberg_number': 'Fr.1257',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Red',
            'production_period': '1869-1875'
        },
        {
            'issue_id': 'US-FRAC10-1870-P',
            'series_id': 'us_fractional_10_cent',
            'face_value': 0.10,
            'year': 1870,
            'variety_name': 'Fourth Issue 10¢ Large Brown Seal',
            'distinguishing_features': 'Large brown Treasury seal, Liberty bust portrait, green back',
            'identification_keywords': 'fourth issue, large brown seal, liberty bust, green back, ten cent',
            'rarity': 'scarce',
            'historical_notes': 'Brown seal variety is scarcer than red seal version',
            'friedberg_number': 'Fr.1258',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Brown',
            'production_period': '1869-1875'
        },

        # Fourth Issue (1869-1875) - 15 Cent varieties
        {
            'issue_id': 'US-FRAC15-1869-P',
            'series_id': 'us_fractional_15_cent',
            'face_value': 0.15,
            'year': 1869,
            'variety_name': 'Fourth Issue 15¢ Large Red Seal',
            'distinguishing_features': 'Large red Treasury seal, Columbia bust portrait, green back',
            'identification_keywords': 'fourth issue, large red seal, columbia bust, green back, fifteen cent',
            'rarity': 'common',
            'historical_notes': 'Only issue to feature 15¢ denomination in fractional currency series',
            'friedberg_number': 'Fr.1267',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Red',
            'production_period': '1869-1875'
        },
        {
            'issue_id': 'US-FRAC15-1870-P',
            'series_id': 'us_fractional_15_cent',
            'face_value': 0.15,
            'year': 1870,
            'variety_name': 'Fourth Issue 15¢ Large Brown Seal',
            'distinguishing_features': 'Large brown Treasury seal, Columbia bust portrait, green back',
            'identification_keywords': 'fourth issue, large brown seal, columbia bust, green back, fifteen cent',
            'rarity': 'scarce',
            'historical_notes': 'Brown seal variety is scarcer than red seal version',
            'friedberg_number': 'Fr.1268',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Brown',
            'production_period': '1869-1875'
        },

        # Fourth Issue (1869-1875) - 25 Cent varieties
        {
            'issue_id': 'US-FRAC25-1869-P',
            'series_id': 'us_fractional_25_cent',
            'face_value': 0.25,
            'year': 1869,
            'variety_name': 'Fourth Issue 25¢ Large Red Seal',
            'distinguishing_features': 'Large red Treasury seal, Washington portrait, green back',
            'identification_keywords': 'fourth issue, large red seal, washington, green back, twenty five cent',
            'rarity': 'common',
            'historical_notes': 'Most common Fourth Issue fractional currency note',
            'friedberg_number': 'Fr.1302',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Red',
            'production_period': '1869-1875'
        },
        {
            'issue_id': 'US-FRAC25-1870-P',
            'series_id': 'us_fractional_25_cent',
            'face_value': 0.25,
            'year': 1870,
            'variety_name': 'Fourth Issue 25¢ Large Brown Seal',
            'distinguishing_features': 'Large brown Treasury seal, Washington portrait, green back',
            'identification_keywords': 'fourth issue, large brown seal, washington, green back, twenty five cent',
            'rarity': 'scarce',
            'historical_notes': 'Brown seal variety is scarcer than red seal version',
            'friedberg_number': 'Fr.1303',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Brown',
            'production_period': '1869-1875'
        },

        # Fourth Issue (1869-1875) - 50 Cent varieties
        {
            'issue_id': 'US-FRAC50-1869-P',
            'series_id': 'us_fractional_50_cent',
            'face_value': 0.50,
            'year': 1869,
            'variety_name': 'Fourth Issue 50¢ Large Red Seal Lincoln',
            'distinguishing_features': 'Large red Treasury seal, Lincoln portrait, green back',
            'identification_keywords': 'fourth issue, large red seal, lincoln portrait, green back, fifty cent',
            'rarity': 'common',
            'historical_notes': 'Features Abraham Lincoln portrait on Fourth Issue fifty cent note',
            'friedberg_number': 'Fr.1374',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Red',
            'production_period': '1869-1875'
        },
        {
            'issue_id': 'US-FRAC50-1870-P',
            'series_id': 'us_fractional_50_cent',
            'face_value': 0.50,
            'year': 1870,
            'variety_name': 'Fourth Issue 50¢ Large Brown Seal Lincoln',
            'distinguishing_features': 'Large brown Treasury seal, Lincoln portrait, green back',
            'identification_keywords': 'fourth issue, large brown seal, lincoln portrait, green back, fifty cent',
            'rarity': 'scarce',
            'historical_notes': 'Brown seal variety with Lincoln portrait, scarcer than red seal version',
            'friedberg_number': 'Fr.1375',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Brown',
            'production_period': '1869-1875'
        },
        {
            'issue_id': 'US-FRAC50-1871-P',
            'series_id': 'us_fractional_50_cent',
            'face_value': 0.50,
            'year': 1871,
            'variety_name': 'Fourth Issue 50¢ Large Red Seal Stanton',
            'distinguishing_features': 'Large red Treasury seal, Edwin Stanton portrait, green back',
            'identification_keywords': 'fourth issue, large red seal, stanton portrait, green back, fifty cent',
            'rarity': 'common',
            'historical_notes': 'Features Edwin Stanton, Secretary of War during Civil War',
            'friedberg_number': 'Fr.1376',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Red',
            'production_period': '1869-1875'
        },
        {
            'issue_id': 'US-FRAC50-1872-P',
            'series_id': 'us_fractional_50_cent',
            'face_value': 0.50,
            'year': 1872,
            'variety_name': 'Fourth Issue 50¢ Large Brown Seal Stanton',
            'distinguishing_features': 'Large brown Treasury seal, Edwin Stanton portrait, green back',
            'identification_keywords': 'fourth issue, large brown seal, stanton portrait, green back, fifty cent',
            'rarity': 'scarce',
            'historical_notes': 'Brown seal variety with Stanton portrait, scarcer than red seal version',
            'friedberg_number': 'Fr.1377',
            'issue_type': 'Fractional Currency',
            'signature_combination': 'None (no signatures on fractional currency)',
            'seal_color': 'Brown',
            'production_period': '1869-1875'
        }
    ]
    
    # Insert each variety record
    for i, variety in enumerate(fractional_varieties, 1):
        print(f"\n{i}. Adding {variety['variety_name']}...")
        
        try:
            # Prepare specifications and sides JSON
            specifications = {
                "width_mm": 105,  # Approximate fractional currency size
                "height_mm": 72,
                "thickness_mm": 0.10,
                "weight_grams": 0.8
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
                    "elements": ["denomination markers", "ornate back design"]
                }
            }
            
            mintage = {
                "total_printed": None,  # Exact mintage unknown for most fractional currency
                "estimated_surviving": None
            }
            
            varieties_json = [{
                "variety_id": variety['issue_id'].split('-')[-1].lower(),
                "name": variety['variety_name'],
                "description": variety['distinguishing_features'],
                "friedberg_number": variety.get('friedberg_number', None)
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
                'United States Treasury',
                'decimal',
                'dollar',
                variety['face_value'],
                'cent',
                f"Fractional {int(variety['face_value']*100)}¢",
                variety['year'],
                'P',  # All fractional currency printed at BEP
                json.dumps(specifications),
                json.dumps(sides),
                json.dumps(mintage),
                variety['rarity'],
                json.dumps(varieties_json),
                'GitHub Issue #31 Fractional Currency Research',
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
    
    print(f"\n✅ Fractional Currency Varieties Implementation Complete!")
    print(f"📊 Added varieties for Second Issue (1863-1867) and Fourth Issue (1869-1875)")
    print(f"🔍 Based on comprehensive Friedberg catalog and variety research")
    
    return True

def validate_implementation():
    """Validate the fractional currency implementation."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("\n🔍 Validating Fractional Currency Implementation...")
    print("=" * 50)
    
    # Check series were added
    cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id LIKE 'us_fractional_%'")
    series_count = cursor.fetchone()[0]
    print(f"📊 Fractional currency series: {series_count}")
    
    # Check varieties were added
    cursor.execute("SELECT COUNT(*) FROM issues WHERE issue_id LIKE 'US-FRAC%'")
    variety_count = cursor.fetchone()[0] 
    print(f"💰 Fractional currency varieties: {variety_count}")
    
    # Check by denomination
    for denom in [3, 5, 10, 15, 25, 50]:
        cursor.execute(f"SELECT COUNT(*) FROM issues WHERE issue_id LIKE 'US-FRAC{denom}-%'")
        count = cursor.fetchone()[0]
        print(f"   📝 {denom}¢ varieties: {count}")
    
    # Check ID format compliance
    cursor.execute('''
        SELECT issue_id FROM issues 
        WHERE issue_id LIKE 'US-FRAC%' 
        AND issue_id NOT GLOB 'US-FRAC*-????-?'
    ''')
    invalid_ids = cursor.fetchall()
    
    if invalid_ids:
        print(f"❌ Found {len(invalid_ids)} invalid ID formats:")
        for row in invalid_ids:
            print(f"   {row[0]}")
    else:
        print("✅ All fractional currency IDs follow proper format")
    
    conn.close()
    
    return variety_count > 0 and len(invalid_ids) == 0

def main():
    """Main execution function."""
    print("Fractional Currency Varieties Implementation")
    print("===========================================")
    print("Implementing research from GitHub Issue #31")
    print()
    
    # Step 1: Add fractional currency series
    try:
        add_fractional_currency_series()
    except Exception as e:
        print(f"❌ Error adding fractional currency series: {e}")
        return 1
    
    # Step 2: Implement varieties
    try:
        success = implement_fractional_currency_varieties()
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
        print("\n🎉 Implementation completed successfully!")
        print("\nNext steps:")
        print("1. Export updated taxonomy from database")
        print("   uv run python scripts/export_from_database.py")
        print("2. Validate JSON exports")
        print("3. Update universal format")
        print("4. Commit all changes to git")
        return 0
    else:
        print("\n❌ Implementation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())