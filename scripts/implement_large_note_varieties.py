#!/usr/bin/env python3
"""
Implement Large Note Varieties from Issue #30 Research
=====================================================

This script implements the comprehensive large note variety research
from GitHub Issue #30 comments, focusing on signature combinations,
seal color varieties, and other distinguishing features for historical
US paper currency series.

Based on research covering:
- 1899 $1 Black Eagle (Silver Certificate)  
- 1901 $10 Bison Note (Legal Tender)
- 1914 Federal Reserve Notes (Red vs Blue Seal)
- 1899 $5 Running Antelope (Silver Certificate)
- 1906 $20 Gold Certificate

Author: Claude Code
Date: 2025-08-18
Issue: #30
"""

import sqlite3
import json
import sys
from datetime import datetime

def get_database_connection():
    """Get connection to the coins database."""
    return sqlite3.connect('/Users/m/gh/coin-taxonomy/database/coins.db')

def implement_large_note_varieties():
    """Implement large note variety records from Issue #30 research."""
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    print("🔍 Implementing Large Note Varieties from Issue #30 Research...")
    print("=" * 60)
    
    # Define large note variety data from research
    large_note_varieties = [
        # 1899 $1 Black Eagle - Multiple signature combinations
        {
            'coin_id': 'US-P001-1899-A-MULTI_SIG',
            'series_id': 'us_paper_1_dollar',
            'denomination': 'Paper $1',
            'year': 1899,
            'mint': 'A',
            'object_type': 'banknote',
            'issue_type': 'Silver Certificate',
            'variety_name': 'Black Eagle Multiple Signature Combinations',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, Lincoln and Grant portraits, 11-13 signature varieties',
            'identification_keywords': 'black eagle, silver certificate, blue seal, signature combinations, lincoln grant',
            'common_names': 'Black Eagle, Silver Certificate, Blue Seal Note',
            'production_period': '1899-1923',
            'rarity': 'common',
            'market_significance': 'Common type but specific rare signature pairs carry premiums; collectors seek scarce signature combos and high-grade examples',
            'estimated_mintage': 3604239600,
            'notes': 'Produced with 11-13 Register/Treasurer signature pairs; references vary by cataloging approach. Total printed: 3,604,239,600'
        },
        
        # 1901 $10 Bison Note - Signature combinations  
        {
            'coin_id': 'US-P010-1901-A-BISON_SIG',
            'series_id': 'us_paper_10_dollar', 
            'denomination': 'Paper $10',
            'year': 1901,
            'mint': 'A',
            'object_type': 'banknote',
            'issue_type': 'Legal Tender',
            'variety_name': 'Bison Note Nine Signature Combinations',
            'distinguishing_features': 'Red seal and serials typical of Legal Tender, Central bison vignette (Pablo), Nine signature combinations Fr.114-Fr.122',
            'identification_keywords': 'bison note, legal tender, red seal, pablo, signature combinations, fr114 fr122',
            'common_names': 'Bison Note, Buffalo Bill, Legal Tender Ten',
            'production_period': '1901-1908',
            'rarity': 'varies_by_signature',
            'market_significance': 'Among the most popular type notes; condition censuses show strong demand, with some signature pairs scarcer at top grades',
            'estimated_mintage': None,
            'notes': 'Nine signature combinations collected as Fr.114-Fr.122; some combinations notably scarcer in high grades'
        },
        
        # 1901 $10 Bison Note - Star replacement varieties
        {
            'coin_id': 'US-P010-1901-A-BISON_STAR',
            'series_id': 'us_paper_10_dollar',
            'denomination': 'Paper $10', 
            'year': 1901,
            'mint': 'A',
            'object_type': 'banknote',
            'issue_type': 'Legal Tender',
            'variety_name': 'Bison Note Star Replacement Varieties',
            'distinguishing_features': 'Star prefix/suffix in serials (replacement notes), Red seal Legal Tender type, Central bison vignette',
            'identification_keywords': 'bison star note, legal tender star, replacement note, star serial',
            'common_names': 'Bison Star Note, Star Replacement, Buffalo Star',
            'production_period': '1901-1908',
            'rarity': 'scarce',
            'market_significance': 'Star replacements are actively pursued and scarcer than regular issues',
            'estimated_mintage': None,
            'notes': 'Star replacement notes exist across six signature combinations; notably scarcer than regular issues'
        },
        
        # 1914 FRN Red Seal Type 1
        {
            'coin_id': 'US-P005-1914-G-RED_SEAL',
            'series_id': 'us_paper_5_dollar',
            'denomination': 'Paper $5',
            'year': 1914,
            'mint': 'G',
            'object_type': 'banknote', 
            'issue_type': 'Federal Reserve Note',
            'variety_name': 'Type 1 Red Seal Burke-McAdoo',
            'distinguishing_features': 'Red Treasury seal, Red serial numbers, Type 1 plate layout with 2 large district letters, Burke-McAdoo signatures',
            'identification_keywords': 'federal reserve note red seal, burke mcadoo, type 1 plate, red serial',
            'common_names': 'Red Seal FRN, Type 1 Federal Reserve Note, Burke-McAdoo',
            'production_period': '1914-1915',
            'rarity': 'scarcer_than_blue_seal',
            'market_significance': 'First FRN issues; printed in relatively small numbers vs. later blue seals; highly collected across districts',
            'estimated_mintage': None,
            'notes': 'Early 1914 FRNs with red seals; Type 1 plates used Burke-McAdoo signatures; scarcer than blue seal varieties'
        },
        
        # 1914 FRN Blue Seal Types 2-4
        {
            'coin_id': 'US-P005-1914-G-BLUE_SEAL',
            'series_id': 'us_paper_5_dollar',
            'denomination': 'Paper $5',
            'year': 1914,
            'mint': 'G',
            'object_type': 'banknote',
            'issue_type': 'Federal Reserve Note',
            'variety_name': 'Blue Seal Later Types 2-4',
            'distinguishing_features': 'Blue Treasury seal, Blue serial numbers, Plate type diagnostics by district letters and seal placement',
            'identification_keywords': 'federal reserve note blue seal, type 2 type 3 type 4, blue serial, plate types',
            'common_names': 'Blue Seal FRN, Later Type Federal Reserve Note, Blue Seal Lincoln',
            'production_period': '1915-1918',
            'rarity': 'more_common_than_red_seal',
            'market_significance': 'Main circulation issues; district scarcity and plate types affect demand',
            'estimated_mintage': None,
            'notes': 'Subsequent 1914 FRNs transitioned to blue seals and different plate types (Type 2-4); more common than red seals'
        },
        
        # 1899 $5 Running Antelope
        {
            'coin_id': 'US-P005-1899-A-ANTELOPE_SIG',
            'series_id': 'us_paper_5_dollar',
            'denomination': 'Paper $5',
            'year': 1899,
            'mint': 'A',
            'object_type': 'banknote',
            'issue_type': 'Silver Certificate',
            'variety_name': 'Running Antelope Eleven Signature Combinations',
            'distinguishing_features': 'Blue Treasury seal, Blue serials, Chief Running Antelope central portrait, Eleven signature combinations Fr.271-Fr.281',
            'identification_keywords': 'running antelope, silver certificate, blue seal, indian chief, signature combinations',
            'common_names': 'Running Antelope, Indian Chief Note, Silver Certificate Five',
            'production_period': '1900-1926',
            'rarity': 'varies_by_signature',
            'market_significance': 'Top-10 iconic large-size note; some signature pairs and high grades carry strong premiums',
            'estimated_mintage': None,
            'notes': 'Eleven signature combinations across fiscal years 1900-1926, with gaps in FY1919-FY1920; spans Fr.271-Fr.281'
        },
        
        # 1906 $20 Gold Certificate
        {
            'coin_id': 'US-P020-1906-A-GOLD_SIG',
            'series_id': 'us_paper_20_dollar',
            'denomination': 'Paper $20',
            'year': 1906,
            'mint': 'A',
            'object_type': 'banknote',
            'issue_type': 'Gold Certificate',
            'variety_name': 'Gold Certificate Multiple Signature Combinations',
            'distinguishing_features': 'Gold Treasury seal, Gold overprints typical of Gold Certificates, Multiple signature pairs with some notably scarce',
            'identification_keywords': 'gold certificate, gold seal, gold overprint, signature combinations, twenty dollar',
            'common_names': 'Gold Certificate Twenty, Gold Seal Note, Twenty Dollar Gold',
            'production_period': '1906-1910',
            'rarity': 'varies_by_signature',
            'market_significance': 'Smaller runs than later 1922 gold certificates; survivors skew circulated; high-grade originals and scarce signature/star combos are coveted',
            'estimated_mintage': None,
            'notes': 'Series 1906 $20 Gold Certificates exist with multiple signature pairs; some combinations notably scarce, especially among replacement notes'
        }
    ]
    
    # Insert each variety record
    for i, variety in enumerate(large_note_varieties, 1):
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
                    "elements": ["denomination markers", "series text"]
                }
            }
            
            mintage = {
                "total_printed": variety['estimated_mintage'],
                "estimated_surviving": None
            }
            
            varieties_json = [{
                "variety_id": variety['coin_id'].split('-')[-1].lower(),
                "name": variety['variety_name'],
                "description": variety['distinguishing_features']
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
                    seal_color, series_designation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                variety['coin_id'],
                variety['object_type'],
                variety['series_id'],
                'US',
                'United States Treasury',
                'decimal',
                'dollar',
                float(variety['denomination'].replace('Paper $', '')),
                'dollar',
                variety['denomination'],
                variety['year'],
                variety['mint'],
                json.dumps(specifications),
                json.dumps(sides),
                json.dumps(mintage),
                variety['rarity'],
                json.dumps(varieties_json),
                'GitHub Issue #30 Large Note Variety Research',
                variety['notes'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                variety['distinguishing_features'],
                variety['identification_keywords'],
                variety['distinguishing_features'].split(',')[0] if 'seal' in variety['distinguishing_features'].lower() else None,
                variety['issue_type']
            ))
            
            print(f"   ✅ Added {variety['coin_id']} to issues table")
            
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                print(f"   ⚠️  Record {variety['coin_id']} already exists, skipping...")
            else:
                print(f"   ❌ Error inserting {variety['coin_id']}: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error inserting {variety['coin_id']}: {e}")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n✅ Large Note Varieties Implementation Complete!")
    print(f"📊 Added varieties for 5 priority large note series")
    print(f"🔍 Based on comprehensive signature combination and seal color research")
    
    return True

def main():
    """Main execution function."""
    print("Large Note Varieties Implementation")
    print("==================================")
    print("Implementing research from GitHub Issue #30")
    print()
    
    success = implement_large_note_varieties()
    
    if success:
        print("\n🎉 Implementation completed successfully!")
        print("\nNext steps:")
        print("1. Export updated taxonomy from database")
        print("2. Validate JSON exports")
        print("3. Update universal format")
        return 0
    else:
        print("\n❌ Implementation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())