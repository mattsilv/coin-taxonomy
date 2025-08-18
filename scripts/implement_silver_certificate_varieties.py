#!/usr/bin/env python3
"""
Implement Silver Certificate Varieties from Issue #31 Research
==============================================================

This script implements comprehensive Silver Certificate variety research
from GitHub Issue #31, focusing on 1896 Educational Series and 1957 
final series varieties with complete signature combinations and Friedberg numbers.

Based on research covering:
- 1896 Educational Series: $1 History, $2 Science, $5 Electricity
- 1957 Final Series: Series 1957, 1957A, 1957B with star notes
- Complete Friedberg catalog mapping
- Signature combinations and treasury seal descriptions

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

def add_silver_certificate_series():
    """Add Silver Certificate series to series_registry if not exists."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("📊 Adding Silver Certificate series to registry...")
    
    # Check if Silver Certificate series already exist
    cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id LIKE 'us_silver_certificate_%'")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"   ✓ Found {existing_count} existing Silver Certificate series, skipping creation")
        conn.close()
        return
    
    # Define Silver Certificate series
    silver_certificate_series = [
        {
            'series_id': 'us_silver_certificate_1_dollar',
            'series_name': 'Silver Certificate $1',
            'series_abbreviation': 'SC1',
            'country_code': 'US',
            'denomination': 'Silver Certificate $1',
            'start_year': 1896,
            'end_year': 1957,
            'defining_characteristics': 'US Silver Certificate $1 including Educational Series and final 1957 series',
            'official_name': 'US Silver Certificate $1',
            'type': 'banknote'
        },
        {
            'series_id': 'us_silver_certificate_2_dollar',
            'series_name': 'Silver Certificate $2',
            'series_abbreviation': 'SC2',
            'country_code': 'US',
            'denomination': 'Silver Certificate $2',
            'start_year': 1896,
            'end_year': 1896,
            'defining_characteristics': 'US Silver Certificate $2 Educational Science series',
            'official_name': 'US Silver Certificate $2',
            'type': 'banknote'
        },
        {
            'series_id': 'us_silver_certificate_5_dollar',
            'series_name': 'Silver Certificate $5',
            'series_abbreviation': 'SC5',
            'country_code': 'US',
            'denomination': 'Silver Certificate $5',
            'start_year': 1896,
            'end_year': 1896,
            'defining_characteristics': 'US Silver Certificate $5 Educational Electricity series',
            'official_name': 'US Silver Certificate $5',
            'type': 'banknote'
        }
    ]
    
    # Insert each series
    for series in silver_certificate_series:
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
    print(f"✓ Added {len(silver_certificate_series)} Silver Certificate series")

def implement_silver_certificate_varieties():
    """Implement Silver Certificate variety records from Issue #31 research."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("🔍 Implementing Silver Certificate Varieties from Issue #31 Research...")
    print("=" * 70)
    
    # Define Silver Certificate variety data from research
    silver_certificate_varieties = [
        # 1896 Educational Series - $1 History Certificate
        {
            'issue_id': 'US-SC1-1896-P',
            'series_id': 'us_silver_certificate_1_dollar',
            'face_value': 1.0,
            'year': 1896,
            'variety_name': 'Educational Series $1 History - Tillman/Morgan',
            'distinguishing_features': 'Educational "History Instructing Youth" allegorical scene, blue seal, Tillman/Morgan signatures',
            'identification_keywords': 'educational series, history instructing youth, allegorical art, tillman morgan, blue seal, large size',
            'rarity': 'scarce',
            'historical_notes': 'Part of acclaimed 1896 Educational Series featuring allegorical art. History certificate shows female figure teaching young man.',
            'friedberg_number': 'Fr.224',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'John G. Tillman (Treasurer) / Daniel Morgan (Register)',
            'seal_color': 'Blue',
            'production_period': '1896'
        },
        {
            'issue_id': 'US-SC1-1897-P',
            'series_id': 'us_silver_certificate_1_dollar',
            'face_value': 1.0,
            'year': 1897,
            'variety_name': 'Educational Series $1 History - Bruce/Roberts',
            'distinguishing_features': 'Educational "History Instructing Youth" allegorical scene, blue seal, Bruce/Roberts signatures',
            'identification_keywords': 'educational series, history instructing youth, allegorical art, bruce roberts, blue seal, large size',
            'rarity': 'scarce',
            'historical_notes': 'Part of acclaimed 1896 Educational Series featuring allegorical art. Same design with different signature combination.',
            'friedberg_number': 'Fr.225',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Ellis H. Roberts (Treasurer) / Blanche K. Bruce (Register)',
            'seal_color': 'Blue',
            'production_period': '1897'
        },
        
        # 1896 Educational Series - $2 Science Certificate
        {
            'issue_id': 'US-SC2-1896-P',
            'series_id': 'us_silver_certificate_2_dollar',
            'face_value': 2.0,
            'year': 1896,
            'variety_name': 'Educational Series $2 Science - Tillman/Morgan',
            'distinguishing_features': 'Educational "Science Presenting Steam and Electricity" allegorical scene, blue seal, Tillman/Morgan signatures',
            'identification_keywords': 'educational series, science presenting steam electricity, allegorical art, tillman morgan, blue seal',
            'rarity': 'rare',
            'historical_notes': 'Part of acclaimed 1896 Educational Series. Science certificate shows female figure with steam engine and electrical equipment.',
            'friedberg_number': 'Fr.247',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'John G. Tillman (Treasurer) / Daniel Morgan (Register)',
            'seal_color': 'Blue',
            'production_period': '1896'
        },
        {
            'issue_id': 'US-SC2-1897-P',
            'series_id': 'us_silver_certificate_2_dollar',
            'face_value': 2.0,
            'year': 1897,
            'variety_name': 'Educational Series $2 Science - Bruce/Roberts',
            'distinguishing_features': 'Educational "Science Presenting Steam and Electricity" allegorical scene, blue seal, Bruce/Roberts signatures',
            'identification_keywords': 'educational series, science presenting steam electricity, allegorical art, bruce roberts, blue seal',
            'rarity': 'rare',
            'historical_notes': 'Part of acclaimed 1896 Educational Series. Science certificate with Bruce/Roberts signature combination.',
            'friedberg_number': 'Fr.248',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Ellis H. Roberts (Treasurer) / Blanche K. Bruce (Register)',
            'seal_color': 'Blue',
            'production_period': '1897'
        },
        
        # 1896 Educational Series - $5 Electricity Certificate
        {
            'issue_id': 'US-SC5-1896-P',
            'series_id': 'us_silver_certificate_5_dollar',
            'face_value': 5.0,
            'year': 1896,
            'variety_name': 'Educational Series $5 Electricity - Tillman/Morgan',
            'distinguishing_features': 'Educational "Electricity as the Dominant Force" allegorical scene, blue seal, Tillman/Morgan signatures',
            'identification_keywords': 'educational series, electricity dominant force, allegorical art, tillman morgan, blue seal',
            'rarity': 'rare',
            'historical_notes': 'Part of acclaimed 1896 Educational Series. Electricity certificate shows female figure with electrical equipment and lightning.',
            'friedberg_number': 'Fr.268',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'John G. Tillman (Treasurer) / Daniel Morgan (Register)',
            'seal_color': 'Blue',
            'production_period': '1896'
        },
        {
            'issue_id': 'US-SC5-1897-P',
            'series_id': 'us_silver_certificate_5_dollar',
            'face_value': 5.0,
            'year': 1897,
            'variety_name': 'Educational Series $5 Electricity - Bruce/Roberts',
            'distinguishing_features': 'Educational "Electricity as the Dominant Force" allegorical scene, blue seal, Bruce/Roberts signatures',
            'identification_keywords': 'educational series, electricity dominant force, allegorical art, bruce roberts, blue seal',
            'rarity': 'rare',
            'historical_notes': 'Part of acclaimed 1896 Educational Series. Electricity certificate with Bruce/Roberts signature combination.',
            'friedberg_number': 'Fr.269',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Ellis H. Roberts (Treasurer) / Blanche K. Bruce (Register)',
            'seal_color': 'Blue',
            'production_period': '1897'
        },
        {
            'issue_id': 'US-SC5-1898-P',
            'series_id': 'us_silver_certificate_5_dollar',
            'face_value': 5.0,
            'year': 1898,
            'variety_name': 'Educational Series $5 Electricity - Lyons/Roberts',
            'distinguishing_features': 'Educational "Electricity as the Dominant Force" allegorical scene, blue seal, Lyons/Roberts signatures',
            'identification_keywords': 'educational series, electricity dominant force, allegorical art, lyons roberts, blue seal',
            'rarity': 'rare',
            'historical_notes': 'Part of acclaimed 1896 Educational Series. Electricity certificate with Lyons/Roberts signature combination.',
            'friedberg_number': 'Fr.270',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Ellis H. Roberts (Treasurer) / Judson W. Lyons (Register)',
            'seal_color': 'Blue',
            'production_period': '1898'
        },
        
        # 1957 Final Silver Certificate Series
        {
            'issue_id': 'US-SC1-1957-P',
            'series_id': 'us_silver_certificate_1_dollar',
            'face_value': 1.0,
            'year': 1957,
            'variety_name': 'Series 1957 $1 Silver Certificate - Priest/Anderson',
            'distinguishing_features': 'Small-size format, George Washington portrait, blue seal, Priest/Anderson signatures, "SILVER CERTIFICATE" inscription',
            'identification_keywords': 'series 1957, washington portrait, blue seal, priest anderson, silver certificate, small size',
            'rarity': 'common',
            'historical_notes': 'Final series of Silver Certificates before discontinuation in 1964. Last notes redeemable in silver.',
            'friedberg_number': 'Fr.1619',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Ivy Baker Priest (Treasurer) / Robert B. Anderson (Secretary)',
            'seal_color': 'Blue',
            'production_period': '1957'
        },
        {
            'issue_id': 'US-SC1-1957-S',
            'series_id': 'us_silver_certificate_1_dollar',
            'face_value': 1.0,
            'year': 1957,
            'variety_name': 'Series 1957 $1 Silver Certificate Star Note - Priest/Anderson',
            'distinguishing_features': 'Small-size format, George Washington portrait, blue seal, Priest/Anderson signatures, star in serial number',
            'identification_keywords': 'series 1957, star note, washington portrait, blue seal, priest anderson, replacement note',
            'rarity': 'scarce',
            'historical_notes': 'Replacement note for defective 1957 Silver Certificates. Star serial numbers indicate replacement status.',
            'friedberg_number': 'Fr.1619*',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Ivy Baker Priest (Treasurer) / Robert B. Anderson (Secretary)',
            'seal_color': 'Blue',
            'production_period': '1957'
        },
        {
            'issue_id': 'US-SC1-1958-P',
            'series_id': 'us_silver_certificate_1_dollar',
            'face_value': 1.0,
            'year': 1957,
            'variety_name': 'Series 1957A $1 Silver Certificate - Smith/Dillon',
            'distinguishing_features': 'Small-size format, George Washington portrait, blue seal, Smith/Dillon signatures, "SILVER CERTIFICATE" inscription',
            'identification_keywords': 'series 1957a, washington portrait, blue seal, smith dillon, silver certificate, small size',
            'rarity': 'common',
            'historical_notes': 'Series 1957A continuation of final Silver Certificate series. Signature change due to Treasury personnel changes.',
            'friedberg_number': 'Fr.1620',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Elizabeth Rudel Smith (Treasurer) / C. Douglas Dillon (Secretary)',
            'seal_color': 'Blue',
            'production_period': '1957'
        },
        {
            'issue_id': 'US-SC1-1958-S',
            'series_id': 'us_silver_certificate_1_dollar',
            'face_value': 1.0,
            'year': 1957,
            'variety_name': 'Series 1957A $1 Silver Certificate Star Note - Smith/Dillon',
            'distinguishing_features': 'Small-size format, George Washington portrait, blue seal, Smith/Dillon signatures, star in serial number',
            'identification_keywords': 'series 1957a, star note, washington portrait, blue seal, smith dillon, replacement note',
            'rarity': 'scarce',
            'historical_notes': 'Replacement note for defective 1957A Silver Certificates. Star serial numbers indicate replacement status.',
            'friedberg_number': 'Fr.1620*',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Elizabeth Rudel Smith (Treasurer) / C. Douglas Dillon (Secretary)',
            'seal_color': 'Blue',
            'production_period': '1957'
        },
        {
            'issue_id': 'US-SC1-1959-P',
            'series_id': 'us_silver_certificate_1_dollar',
            'face_value': 1.0,
            'year': 1957,
            'variety_name': 'Series 1957B $1 Silver Certificate - Granahan/Dillon',
            'distinguishing_features': 'Small-size format, George Washington portrait, blue seal, Granahan/Dillon signatures, "SILVER CERTIFICATE" inscription',
            'identification_keywords': 'series 1957b, washington portrait, blue seal, granahan dillon, silver certificate, small size',
            'rarity': 'common',
            'historical_notes': 'Final subseries of Silver Certificates before 1964 discontinuation. Last notes redeemable in silver.',
            'friedberg_number': 'Fr.1621',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Kathryn O\'Hay Granahan (Treasurer) / C. Douglas Dillon (Secretary)',
            'seal_color': 'Blue',
            'production_period': '1957'
        },
        {
            'issue_id': 'US-SC1-1959-S',
            'series_id': 'us_silver_certificate_1_dollar',
            'face_value': 1.0,
            'year': 1957,
            'variety_name': 'Series 1957B $1 Silver Certificate Star Note - Granahan/Dillon',
            'distinguishing_features': 'Small-size format, George Washington portrait, blue seal, Granahan/Dillon signatures, star in serial number',
            'identification_keywords': 'series 1957b, star note, washington portrait, blue seal, granahan dillon, replacement note',
            'rarity': 'scarce',
            'historical_notes': 'Final replacement notes for Silver Certificates before discontinuation. Star serial numbers indicate replacement status.',
            'friedberg_number': 'Fr.1621*',
            'issue_type': 'Silver Certificate',
            'signature_combination': 'Kathryn O\'Hay Granahan (Treasurer) / C. Douglas Dillon (Secretary)',
            'seal_color': 'Blue',
            'production_period': '1957'
        }
    ]
    
    # Insert each variety record
    for variety in silver_certificate_varieties:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO issues (
                    issue_id, series_id, face_value, issue_year, variety_name, distinguishing_features,
                    identification_keywords, rarity, historical_notes, friedberg_number, issue_type,
                    signature_combination, seal_color, production_period
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                variety['issue_id'], variety['series_id'], variety['face_value'], variety['year'],
                variety['variety_name'], variety['distinguishing_features'], variety['identification_keywords'],
                variety['rarity'], variety['historical_notes'], variety['friedberg_number'], variety['issue_type'],
                variety['signature_combination'], variety['seal_color'], variety['production_period']
            ))
            print(f"   ✅ Added variety: {variety['issue_id']} - {variety['variety_name']}")
        except Exception as e:
            print(f"   ❌ Error adding variety {variety['issue_id']}: {e}")
    
    conn.commit()
    
    # Verify implementation
    cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id LIKE 'us_silver_certificate_%'")
    series_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM issues WHERE issue_id LIKE 'US-SC%'")
    variety_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM issues")
    total_issues = cursor.fetchone()[0]
    
    print(f"\n📊 Implementation Summary:")
    print(f"   ✅ Silver Certificate series: {series_count}")
    print(f"   ✅ Silver Certificate varieties: {variety_count}")
    print(f"   📈 Total issues in database: {total_issues}")
    
    conn.close()
    
    print("\n🎯 Silver Certificate varieties implementation complete!")
    print("   - 1896 Educational Series: $1 History, $2 Science, $5 Electricity")
    print("   - 1957 Final Series: Series 1957, 1957A, 1957B with star notes")
    print("   - All signature combinations and Friedberg numbers included")

def main():
    """Main implementation function."""
    try:
        # Add series first
        add_silver_certificate_series()
        
        # Then add varieties
        implement_silver_certificate_varieties()
        
        print("\n✅ Silver Certificate implementation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during implementation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()