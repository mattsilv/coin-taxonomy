#!/usr/bin/env python3
"""
Add High-Liquidity Paper Currency Notes - Phase 2 of Issue #23

This script adds 5 specific high-liquidity paper currency notes:
1. 1899 Black Eagle $1 Silver Certificate (T.E. Burke signatures)
2. 1906 $20 Gold Certificate (Parker Burke signatures) 
3. 1899 $5 Silver Certificate Indian Chief (Running Antelope)
4. 1901 $10 Legal Tender Bison Note
5. 1915 $5 Federal Reserve Bank Note (Lincoln portrait)

Usage:
    python scripts/add_high_liquidity_paper_currency.py
    python scripts/add_high_liquidity_paper_currency.py --dry-run
"""

import sqlite3
import json
import argparse
from datetime import datetime

class HighLiquidityPaperCurrencyAdder:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        
    def get_high_liquidity_notes_data(self):
        """Get the 5 high-liquidity paper currency notes for Phase 2."""
        return [
            {
                # 1899 Black Eagle $1 Silver Certificate - T.E. Burke
                "issue_id": "US-P001-1899-A",
                "object_type": "banknote",
                "series_id": "us_paper_1_dollar",
                "country_code": "US",
                "authority_name": "United States Treasury",
                "monetary_system": "decimal",
                "currency_unit": "dollar",
                "face_value": 1.0,
                "unit_name": "dollar",
                "common_names": json.dumps(["Black Eagle", "one dollar silver certificate", "large size note"]),
                "system_fraction": "1 dollar",
                "issue_year": 1899,
                "mint_id": "A",  # Treasury authority
                "date_range_start": 1899,
                "date_range_end": 1923,
                "authority_period": json.dumps({
                    "entity_type": "united_states_treasury", 
                    "leader": {"name": "Lyman J. Gage", "title": "Secretary of the Treasury"}
                }),
                "specifications": json.dumps({
                    "width_mm": 187,  # 7.38 inches
                    "height_mm": 81,  # 3.18 inches
                    "thickness_mm": 0.11,
                    "weight_grams": 1.2
                }),
                "sides": json.dumps({
                    "obverse": {
                        "design": "Portrait of Martha Washington with black eagle",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["Martha Washington portrait", "black eagle vignette", "ornate borders", "blue seal", "blue serial numbers"]
                    },
                    "reverse": {
                        "design": "Ornate geometric patterns",
                        "designer": "Bureau of Engraving and Printing", 
                        "elements": ["complex geometric design", "large denomination markers", "silver certificate text"]
                    }
                }),
                "mintage": json.dumps({
                    "total_printed": 35000000,
                    "estimated_surviving": 8000
                }),
                "rarity": "scarce",
                "varieties": json.dumps([
                    {
                        "variety_id": "1899_lyons_roberts",
                        "name": "Lyons-Roberts Signatures",
                        "description": "Earlier signature combination",
                        "estimated_mintage": 15000000
                    },
                    {
                        "variety_id": "1899_lyons_treat",
                        "name": "Lyons-Treat Signatures", 
                        "description": "Mid-period signature combination",
                        "estimated_mintage": 12000000
                    },
                    {
                        "variety_id": "1899_vernon_treat",
                        "name": "Vernon-Treat Signatures",
                        "description": "Later signature combination",
                        "estimated_mintage": 8000000
                    }
                ]),
                "source_citation": "Friedberg Paper Money of the United States, 20th Edition",
                "notes": "Famous 'Black Eagle' note, last of the large-size ornate designs. Ranked #16 in '100 Greatest American Currency Notes'",
                "metadata": json.dumps({
                    "collection_significance": "Iconic large-size design, highly sought after",
                    "historical_context": "End of 19th century ornate currency design era",
                    "friedberg_number": "Fr-233"
                }),
                
                # Paper currency specific fields
                "signature_combination": "Vernon-Treat",
                "seal_color": "blue",
                "block_letter": "A",
                "serial_number_type": "8_digit_alpha_numeric",
                "size_format": "large_size",
                "paper_type": "cotton_linen_blend",
                "watermark": None,
                "security_features": json.dumps([
                    "distinctive_paper",
                    "blue_silk_fibers",
                    "intricate_engraving",
                    "complex_geometric_reverse"
                ]),
                "printing_method": "intaglio",
                "series_designation": "Series 1899",
                
                # Visual descriptions
                "obverse_description": "Portrait of Martha Washington in center-left, large black eagle vignette on right, ornate scrollwork throughout, blue Treasury seal lower left, blue serial numbers",
                "reverse_description": "Complex geometric pattern with large Roman numeral 'I' in center, ornate borders and flourishes, silver certificate obligation text",
                "distinguishing_features": json.dumps([
                    "Black eagle vignette (namesake feature)",
                    "Martha Washington portrait", 
                    "Large size format (7.38 x 3.18 inches)",
                    "Blue treasury seal and serial numbers",
                    "Ornate geometric reverse design",
                    "Series 1899 designation"
                ]),
                "identification_keywords": json.dumps([
                    "black eagle",
                    "martha washington", 
                    "silver certificate",
                    "large size",
                    "series 1899",
                    "blue seal",
                    "ornate design"
                ]),
                "seller_name": "Heritage Auctions"
            },
            {
                # 1906 $20 Gold Certificate - Parker Burke
                "issue_id": "US-P020-1906-A",
                "object_type": "banknote",
                "series_id": "us_paper_20_dollar",
                "country_code": "US", 
                "authority_name": "United States Treasury",
                "monetary_system": "decimal",
                "currency_unit": "dollar",
                "face_value": 20.0,
                "unit_name": "dollar",
                "common_names": json.dumps(["twenty dollar gold certificate", "horse blanket", "large size note"]),
                "system_fraction": "20 dollars",
                "issue_year": 1906,
                "mint_id": "A",
                "date_range_start": 1906,
                "date_range_end": 1922,
                "authority_period": json.dumps({
                    "entity_type": "united_states_treasury",
                    "leader": {"name": "Leslie M. Shaw", "title": "Secretary of the Treasury"}
                }),
                "specifications": json.dumps({
                    "width_mm": 187, 
                    "height_mm": 81,
                    "thickness_mm": 0.11,
                    "weight_grams": 1.2
                }),
                "sides": json.dumps({
                    "obverse": {
                        "design": "Portrait of George Washington",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["George Washington portrait", "gold seal", "gold serial numbers", "ornate borders"]
                    },
                    "reverse": {
                        "design": "Great Seal of the United States in golden orange",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["great seal eagle", "shield design", "golden orange background", "denomination twenty"]
                    }
                }),
                "mintage": json.dumps({
                    "total_printed": 15000000,
                    "estimated_surviving": 12000
                }),
                "rarity": "common",
                "varieties": json.dumps([
                    {
                        "variety_id": "1906_lyons_treat",
                        "name": "Lyons-Treat Signatures",
                        "description": "Early signature combination",
                        "estimated_mintage": 8000000
                    },
                    {
                        "variety_id": "1906_vernon_treat", 
                        "name": "Vernon-Treat Signatures",
                        "description": "Later signature combination",
                        "estimated_mintage": 7000000
                    }
                ]),
                "source_citation": "Standard Catalog of United States Paper Money, 30th Edition",
                "notes": "Third most common large size $20 bill. Part of last large-size gold certificate series",
                "metadata": json.dumps({
                    "collection_significance": "Popular large-size denomination",
                    "historical_context": "Gold standard era, pre-Federal Reserve",
                    "friedberg_number": "Fr-1186"
                }),
                
                # Paper currency specific fields
                "signature_combination": "Vernon-Treat",
                "seal_color": "gold",
                "block_letter": "A",
                "serial_number_type": "8_digit_alpha_numeric",
                "size_format": "large_size", 
                "paper_type": "cotton_linen_blend",
                "watermark": None,
                "security_features": json.dumps([
                    "distinctive_paper",
                    "gold_ink_seal",
                    "intricate_engraving",
                    "microprinting"
                ]),
                "printing_method": "intaglio",
                "series_designation": "Series 1906",
                
                # Visual descriptions
                "obverse_description": "Portrait of George Washington in center, gold Treasury seal on right, gold serial numbers, ornate border design",
                "reverse_description": "Great Seal of the United States in center with golden orange background, eagle with shield, 'Twenty Dollars' text around border",
                "distinguishing_features": json.dumps([
                    "George Washington portrait",
                    "Gold seal and serial numbers",
                    "Large size format", 
                    "Golden orange reverse design",
                    "Great Seal eagle on reverse",
                    "Series 1906 designation"
                ]),
                "identification_keywords": json.dumps([
                    "gold certificate",
                    "george washington",
                    "twenty dollars",
                    "gold seal",
                    "series 1906",
                    "large size",
                    "great seal"
                ]),
                "seller_name": "APMEX"
            },
            {
                # 1899 $5 Silver Certificate Indian Chief - Running Antelope
                "issue_id": "US-P005-1899-A",
                "object_type": "banknote",
                "series_id": "us_paper_5_dollar",
                "country_code": "US",
                "authority_name": "United States Treasury",
                "monetary_system": "decimal",
                "currency_unit": "dollar", 
                "face_value": 5.0,
                "unit_name": "dollar",
                "common_names": json.dumps(["Indian Chief Note", "Running Antelope", "five dollar silver certificate"]),
                "system_fraction": "5 dollars",
                "issue_year": 1899,
                "mint_id": "A",
                "date_range_start": 1899,
                "date_range_end": 1923,
                "authority_period": json.dumps({
                    "entity_type": "united_states_treasury",
                    "leader": {"name": "Lyman J. Gage", "title": "Secretary of the Treasury"}
                }),
                "specifications": json.dumps({
                    "width_mm": 187,
                    "height_mm": 81, 
                    "thickness_mm": 0.11,
                    "weight_grams": 1.2
                }),
                "sides": json.dumps({
                    "obverse": {
                        "design": "Portrait of Sioux Chief Running Antelope",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["Running Antelope portrait", "war bonnet headdress", "roman numeral V", "blue seal"]
                    },
                    "reverse": {
                        "design": "Ornate border with large Roman numeral V",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["large roman numeral V", "silver certificate obligation text", "ornate scrollwork"]
                    }
                }),
                "mintage": json.dumps({
                    "total_printed": 30000000,
                    "estimated_surviving": 25000
                }),
                "rarity": "common",
                "varieties": json.dumps([
                    {
                        "variety_id": "1899_lyons_roberts",
                        "name": "Lyons-Roberts Signatures",
                        "description": "Early signature combination, most common",
                        "estimated_mintage": 18000000
                    },
                    {
                        "variety_id": "1899_lyons_treat",
                        "name": "Lyons-Treat Signatures",
                        "description": "Later signature combination",
                        "estimated_mintage": 12000000
                    }
                ]),
                "source_citation": "A Guide Book of United States Paper Money, 6th Edition",
                "notes": "Only U.S. federal paper currency featuring a named Native American. Running Antelope was head chief of the Hunkpapa Lakota",
                "metadata": json.dumps({
                    "collection_significance": "Unique historical representation of Native American on U.S. currency",
                    "historical_context": "Running Antelope (1821-1896), Hunkpapa Lakota chief",
                    "friedberg_number": "Fr-281"
                }),
                
                # Paper currency specific fields
                "signature_combination": "Lyons-Roberts",
                "seal_color": "blue",
                "block_letter": "A", 
                "serial_number_type": "8_digit_alpha_numeric",
                "size_format": "large_size",
                "paper_type": "cotton_linen_blend",
                "watermark": None,
                "security_features": json.dumps([
                    "distinctive_paper",
                    "blue_silk_fibers",
                    "intricate_portrait_engraving",
                    "complex_border_design"
                ]),
                "printing_method": "intaglio",
                "series_designation": "Series 1899",
                
                # Visual descriptions
                "obverse_description": "Portrait of Chief Running Antelope in war bonnet on left, large Roman numeral 'V' in blue center, blue Treasury seal on right, blue serial numbers",
                "reverse_description": "Large Roman numeral 'V' in ornate center design, silver certificate obligation text, decorative scrollwork borders",
                "distinguishing_features": json.dumps([
                    "Chief Running Antelope portrait",
                    "War bonnet headdress",
                    "Only Native American on federal currency",
                    "Large Roman numeral V design", 
                    "Blue treasury seal",
                    "Series 1899 designation"
                ]),
                "identification_keywords": json.dumps([
                    "indian chief",
                    "running antelope",
                    "native american",
                    "silver certificate", 
                    "war bonnet",
                    "roman numeral v",
                    "series 1899"
                ]),
                "seller_name": "Littleton Coin Company"
            },
            {
                # 1901 $10 Legal Tender Bison Note
                "issue_id": "US-P010-1901-A",
                "object_type": "banknote", 
                "series_id": "us_paper_10_dollar",
                "country_code": "US",
                "authority_name": "United States Treasury",
                "monetary_system": "decimal",
                "currency_unit": "dollar",
                "face_value": 10.0,
                "unit_name": "dollar",
                "common_names": json.dumps(["Bison Note", "Buffalo Bill", "Lewis and Clark Note"]),
                "system_fraction": "10 dollars",
                "issue_year": 1901,
                "mint_id": "A",
                "date_range_start": 1901,
                "date_range_end": 1923,
                "authority_period": json.dumps({
                    "entity_type": "united_states_treasury",
                    "leader": {"name": "Lyman J. Gage", "title": "Secretary of the Treasury"}
                }),
                "specifications": json.dumps({
                    "width_mm": 187,
                    "height_mm": 81,
                    "thickness_mm": 0.11,
                    "weight_grams": 1.2
                }),
                "sides": json.dumps({
                    "obverse": {
                        "design": "American bison with Lewis and Clark portraits",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["american bison center", "meriwether lewis portrait left", "william clark portrait right", "red seal"]
                    },
                    "reverse": {
                        "design": "Female figure representing Columbia",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["columbia figure", "allegorical design", "denomination ten", "ornate borders"]
                    }
                }),
                "mintage": json.dumps({
                    "total_printed": 8000000,
                    "estimated_surviving": 4000
                }),
                "rarity": "scarce",
                "varieties": json.dumps([
                    {
                        "variety_id": "1901_lyons_roberts",
                        "name": "Lyons-Roberts Signatures",
                        "description": "Early signature combination",
                        "estimated_mintage": 4000000
                    },
                    {
                        "variety_id": "1901_lyons_treat",
                        "name": "Lyons-Treat Signatures", 
                        "description": "Later signature combination",
                        "estimated_mintage": 4000000
                    }
                ]),
                "source_citation": "100 Greatest American Currency Notes by Q. David Bowers",
                "notes": "Only federally issued note featuring American bison. Commemorates Lewis and Clark expedition",
                "metadata": json.dumps({
                    "collection_significance": "Extremely popular among collectors, iconic American wildlife design",
                    "historical_context": "Westward expansion era, Lewis and Clark expedition commemoration",
                    "friedberg_number": "Fr-122"
                }),
                
                # Paper currency specific fields
                "signature_combination": "Lyons-Roberts",
                "seal_color": "red",
                "block_letter": "A",
                "serial_number_type": "8_digit_alpha_numeric",
                "size_format": "large_size",
                "paper_type": "cotton_linen_blend",
                "watermark": None,
                "security_features": json.dumps([
                    "distinctive_paper",
                    "red_silk_fibers",
                    "detailed_wildlife_engraving",
                    "portrait_engravings"
                ]),
                "printing_method": "intaglio",
                "series_designation": "Series 1901",
                
                # Visual descriptions  
                "obverse_description": "Large American bison in center plains setting, portrait of Meriwether Lewis on left, portrait of William Clark on right, small red Treasury seal",
                "reverse_description": "Female allegorical figure of Columbia in center, ornate scrollwork and geometric designs, 'Ten Dollars' denomination markers",
                "distinguishing_features": json.dumps([
                    "American bison center vignette",
                    "Lewis and Clark explorer portraits",
                    "Only federal note with bison",
                    "Red treasury seal",
                    "Plains landscape setting",
                    "Series 1901 designation"
                ]),
                "identification_keywords": json.dumps([
                    "bison note",
                    "buffalo bill",
                    "american bison",
                    "lewis and clark",
                    "legal tender", 
                    "red seal",
                    "explorers"
                ]),
                "seller_name": "Chicago Gold Gallery"
            },
            {
                # 1914 $5 Federal Reserve Bank Note - Lincoln portrait (corrected from 1915)
                "issue_id": "US-P005-1914-G",
                "object_type": "banknote",
                "series_id": "us_paper_5_dollar", 
                "country_code": "US",
                "authority_name": "Federal Reserve Bank of Chicago",
                "monetary_system": "decimal",
                "currency_unit": "dollar",
                "face_value": 5.0,
                "unit_name": "dollar",
                "common_names": json.dumps(["five dollar federal reserve note", "lincoln note", "federal reserve bank note"]),
                "system_fraction": "5 dollars",
                "issue_year": 1914,
                "mint_id": "G",  # Chicago Federal Reserve Bank
                "date_range_start": 1914,
                "date_range_end": 1918,
                "authority_period": json.dumps({
                    "entity_type": "federal_reserve_system",
                    "leader": {"name": "Charles S. Hamlin", "title": "First Chairman of Federal Reserve Board"}
                }),
                "specifications": json.dumps({
                    "width_mm": 187,
                    "height_mm": 81,
                    "thickness_mm": 0.11,
                    "weight_grams": 1.2
                }),
                "sides": json.dumps({
                    "obverse": {
                        "design": "Portrait of Abraham Lincoln",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["abraham lincoln portrait", "federal reserve bank seal", "red or blue treasury seal", "bank charter information"]
                    },
                    "reverse": {
                        "design": "Vignettes of Columbus in sight of land and Landing of Pilgrims",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["columbus vignette", "pilgrim landing vignette", "denomination five", "federal reserve text"]
                    }
                }),
                "mintage": json.dumps({
                    "total_printed": 12000000,
                    "chicago_bank_printing": 1500000,
                    "estimated_surviving": 8000
                }),
                "rarity": "common",
                "varieties": json.dumps([
                    {
                        "variety_id": "1914_red_seal",
                        "name": "Red Seal Variety",
                        "description": "Earlier red seal version, scarcer",
                        "estimated_mintage": 3000000
                    },
                    {
                        "variety_id": "1914_blue_seal",
                        "name": "Blue Seal Variety", 
                        "description": "Later blue seal version, more common",
                        "estimated_mintage": 9000000
                    }
                ]),
                "source_citation": "Federal Reserve Bank Historical Records",
                "notes": "First Federal Reserve Bank Notes issued. Red seal varieties much scarcer than blue seal",
                "metadata": json.dumps({
                    "collection_significance": "Historic first Federal Reserve Bank Note series",
                    "historical_context": "Establishment of Federal Reserve System in 1913",
                    "friedberg_number": "Fr-832"
                }),
                
                # Paper currency specific fields
                "signature_combination": "Burke-McAdoo",
                "seal_color": "blue",  # Blue seal variety (more common)
                "block_letter": "G",
                "serial_number_type": "8_digit_alpha_numeric",
                "size_format": "large_size",
                "paper_type": "cotton_linen_blend", 
                "watermark": None,
                "security_features": json.dumps([
                    "distinctive_paper",
                    "federal_reserve_bank_seal",
                    "dual_authority_seals",
                    "bank_charter_number"
                ]),
                "printing_method": "intaglio",
                "series_designation": "Series 1914",
                
                # Visual descriptions
                "obverse_description": "Portrait of Abraham Lincoln in center, Federal Reserve Bank of Chicago seal on left, blue Treasury seal on right, bank charter and district information",
                "reverse_description": "Vignette of Columbus sighting land on left, Landing of Pilgrims vignette on right, 'Five Dollars' denomination text",
                "distinguishing_features": json.dumps([
                    "Abraham Lincoln portrait",
                    "First Federal Reserve Bank Notes",
                    "Dual bank and treasury seals",
                    "Chicago Federal Reserve Bank G designation",
                    "Columbus and Pilgrim vignettes on reverse",
                    "Series 1914 designation"
                ]),
                "identification_keywords": json.dumps([
                    "federal reserve bank note",
                    "abraham lincoln",
                    "chicago federal reserve",
                    "series 1914",
                    "columbus vignette",
                    "pilgrim landing",
                    "blue seal"
                ]),
                "seller_name": "Golden Eagle Coins"
            }
        ]
    
    def add_signature_combinations(self):
        """Add required signature combinations to the database."""
        signatures = [
            {
                "signature_id": "vernon_treat_1899",
                "denomination": "$1", 
                "series_year": 1899,
                "treasurer_signature": "Bruce Vernon",
                "secretary_signature": "Charles J. Treat",
                "position_titles": json.dumps(["Treasurer of the United States", "Secretary of the Treasury"]),
                "period_start": 1899,
                "period_end": 1905,
                "notes": "Common on 1899 Silver Certificates"
            },
            {
                "signature_id": "lyons_roberts_1899",
                "denomination": "$5",
                "series_year": 1899,
                "treasurer_signature": "Judson W. Lyons", 
                "secretary_signature": "Ellis H. Roberts",
                "position_titles": json.dumps(["Treasurer of the United States", "Secretary of the Treasury"]),
                "period_start": 1898,
                "period_end": 1905,
                "notes": "Common on 1899 Indian Chief notes"
            },
            {
                "signature_id": "lyons_treat_1901",
                "denomination": "$10",
                "series_year": 1901,
                "treasurer_signature": "Judson W. Lyons",
                "secretary_signature": "Charles J. Treat", 
                "position_titles": json.dumps(["Treasurer of the United States", "Secretary of the Treasury"]),
                "period_start": 1901,
                "period_end": 1905,
                "notes": "Common on 1901 Bison notes"
            },
            {
                "signature_id": "burke_mcadoo_1914",
                "denomination": "$5", 
                "series_year": 1914,
                "treasurer_signature": "Thomas E. Burke",
                "secretary_signature": "William G. McAdoo",
                "position_titles": json.dumps(["Treasurer of the United States", "Secretary of the Treasury"]),
                "period_start": 1913,
                "period_end": 1921,
                "notes": "Federal Reserve Bank Note signatures"
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for sig in signatures:
                cursor.execute("SELECT COUNT(*) FROM paper_currency_signatures WHERE signature_id = ?", (sig['signature_id'],))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO paper_currency_signatures (
                            signature_id, denomination, series_year, treasurer_signature,
                            secretary_signature, position_titles, period_start, period_end, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        sig['signature_id'], sig['denomination'], sig['series_year'],
                        sig['treasurer_signature'], sig['secretary_signature'], 
                        sig['position_titles'], sig['period_start'], sig['period_end'], sig['notes']
                    ))
                    print(f"   ✅ Added signature: {sig['treasurer_signature']}-{sig['secretary_signature']}")
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"❌ Error adding signatures: {e}")
        finally:
            conn.close()
    
    def add_seal_colors(self):
        """Add additional seal colors needed for historical notes."""
        colors = [
            {
                "color_id": "gold",
                "color_name": "Gold",
                "description": "Gold Certificate seal color",
                "hex_color": "#FFD700",
                "introduced_year": 1865,
                "discontinued_year": 1933,
                "denominations": json.dumps(["$10", "$20", "$50", "$100", "$500", "$1000"]),
                "notes": "Used exclusively for Gold Certificates"
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for color in colors:
                cursor.execute("SELECT COUNT(*) FROM paper_currency_seal_colors WHERE color_id = ?", (color['color_id'],))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO paper_currency_seal_colors (
                            color_id, color_name, description, hex_color, introduced_year,
                            discontinued_year, denominations, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        color['color_id'], color['color_name'], color['description'],
                        color['hex_color'], color['introduced_year'], color['discontinued_year'],
                        color['denominations'], color['notes']
                    ))
                    print(f"   ✅ Added seal color: {color['color_name']}")
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"❌ Error adding seal colors: {e}")
        finally:
            conn.close()
    
    def add_authorities(self):
        """Add Treasury authority for pre-Federal Reserve notes."""
        authorities = [
            {
                "authority_id": "us_treasury_a",
                "authority_name": "United States Treasury",
                "authority_type": "treasury_department",
                "location": "Washington, D.C.",
                "district_number": 1,
                "district_letter": "A",
                "operational_period": json.dumps({"start": 1862, "end": None}),
                "notes": "Primary issuing authority for early paper currency"
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for auth in authorities:
                cursor.execute("SELECT COUNT(*) FROM paper_currency_authorities WHERE authority_id = ?", (auth['authority_id'],))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO paper_currency_authorities (
                            authority_id, authority_name, authority_type, location,
                            district_number, district_letter, operational_period, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        auth['authority_id'], auth['authority_name'], auth['authority_type'],
                        auth['location'], auth['district_number'], auth['district_letter'],
                        auth['operational_period'], auth['notes']
                    ))
                    print(f"   ✅ Added authority: {auth['authority_name']}")
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"❌ Error adding authorities: {e}")
        finally:
            conn.close()
    
    def add_high_liquidity_notes(self, dry_run=False):
        """Add the 5 high-liquidity paper currency notes to the database."""
        print("💰 Adding high-liquidity paper currency notes (Phase 2)...")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No data will be added")
            notes_data = self.get_high_liquidity_notes_data()
            for note in notes_data:
                print(f"   Would add: {note['issue_id']} - ${note['face_value']} {note['series_designation']}")
            return True
        
        # First add required reference data
        print("📚 Adding required reference data...")
        self.add_signature_combinations()
        self.add_seal_colors()
        self.add_authorities()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            notes_data = self.get_high_liquidity_notes_data()
            
            for note in notes_data:
                # Check if already exists
                cursor.execute("SELECT COUNT(*) FROM issues WHERE issue_id = ?", (note['issue_id'],))
                if cursor.fetchone()[0] > 0:
                    print(f"   → Already exists: {note['issue_id']}")
                    continue
                
                # Insert the high-liquidity note
                cursor.execute('''
                    INSERT INTO issues (
                        issue_id, object_type, series_id, country_code, authority_name,
                        monetary_system, currency_unit, face_value, unit_name, common_names,
                        system_fraction, issue_year, mint_id, date_range_start, date_range_end,
                        authority_period, specifications, sides, mintage, rarity, varieties,
                        source_citation, notes, metadata, signature_combination, seal_color,
                        block_letter, serial_number_type, size_format, paper_type, watermark,
                        security_features, printing_method, series_designation, obverse_description,
                        reverse_description, distinguishing_features, identification_keywords,
                        seller_name
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    note['issue_id'], note['object_type'], note['series_id'], note['country_code'],
                    note['authority_name'], note['monetary_system'], note['currency_unit'],
                    note['face_value'], note['unit_name'], note['common_names'], note['system_fraction'],
                    note['issue_year'], note['mint_id'], note['date_range_start'], note['date_range_end'],
                    note['authority_period'], note['specifications'], note['sides'], note['mintage'],
                    note['rarity'], note['varieties'], note['source_citation'], note['notes'],
                    note['metadata'], note['signature_combination'], note['seal_color'],
                    note['block_letter'], note['serial_number_type'], note['size_format'],
                    note['paper_type'], note['watermark'], note['security_features'],
                    note['printing_method'], note['series_designation'], note['obverse_description'],
                    note['reverse_description'], note['distinguishing_features'],
                    note['identification_keywords'], note['seller_name']
                ))
                
                print(f"   ✅ Added: {note['issue_id']} - ${note['face_value']} {note['series_designation']}")
                print(f"      Features: {', '.join(json.loads(note['distinguishing_features'])[:3])}")
            
            conn.commit()
            
            # Verify the data was added
            cursor.execute("SELECT COUNT(*) FROM issues WHERE object_type = 'banknote'")
            banknote_count = cursor.fetchone()[0]
            print(f"✅ High-liquidity notes added. Total banknotes in database: {banknote_count}")
            
            # Show summary of added notes
            cursor.execute('''
                SELECT issue_id, face_value, series_designation, common_names 
                FROM issues 
                WHERE object_type = 'banknote' AND issue_year BETWEEN 1899 AND 1920
                ORDER BY face_value, issue_year
            ''')
            results = cursor.fetchall()
            print("\n📋 High-Liquidity Paper Currency Notes Summary:")
            for result in results:
                issue_id, face_value, series, common_names = result
                names = json.loads(common_names)[0] if common_names else "Note"
                print(f"   • {issue_id}: ${int(face_value)} {series} ({names})")
            
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error adding high-liquidity notes: {e}")
            return False
        finally:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='Add high-liquidity paper currency notes for Phase 2')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be added without making changes')
    args = parser.parse_args()
    
    adder = HighLiquidityPaperCurrencyAdder()
    
    try:
        success = adder.add_high_liquidity_notes(dry_run=args.dry_run)
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Failed to add high-liquidity notes: {e}")
        return 1

if __name__ == "__main__":
    exit(main())