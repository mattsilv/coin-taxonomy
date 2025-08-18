#!/usr/bin/env python3
"""
Add Sample Paper Currency Data for Testing

This script adds sample paper currency records to test the new paper currency
support added in Phase 1 of Issue #23.

Usage:
    python scripts/add_sample_paper_currency.py
    python scripts/add_sample_paper_currency.py --dry-run
"""

import sqlite3
import json
import argparse
from datetime import datetime

class SamplePaperCurrencyAdder:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        
    def get_sample_paper_currency_data(self):
        """Get sample paper currency data for testing."""
        return [
            {
                # US-P001-1957-A format: Country-Type-Year-Authority
                "issue_id": "US-P001-1957-A",
                "object_type": "banknote",
                "series_id": "us_paper_1_dollar",
                "country_code": "US",
                "authority_name": "Federal Reserve Bank of Boston",
                "monetary_system": "decimal",
                "currency_unit": "dollar",
                "face_value": 1.0,
                "unit_name": "dollar",
                "common_names": json.dumps(["one dollar bill", "single", "buck"]),
                "system_fraction": "1 dollar",
                "issue_year": 1957,
                "mint_id": "A",  # Federal Reserve Bank district letter
                "date_range_start": 1957,
                "date_range_end": 1963,
                "authority_period": json.dumps({
                    "entity_type": "federal_reserve_system", 
                    "leader": {"name": "William McChesney Martin Jr.", "title": "Chairman of Federal Reserve"}
                }),
                "specifications": json.dumps({
                    "width_mm": 156,
                    "height_mm": 66,
                    "thickness_mm": 0.11,
                    "weight_grams": 1.0
                }),
                "sides": json.dumps({
                    "obverse": {
                        "design": "George Washington portrait",
                        "designer": "Gilbert Stuart (portrait basis)",
                        "elements": ["presidential portrait", "serial numbers", "treasury seal", "federal reserve seal"]
                    },
                    "reverse": {
                        "design": "Great Seal of the United States",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["pyramid with eye", "eagle with shield", "IN GOD WE TRUST motto"]
                    }
                }),
                "mintage": json.dumps({
                    "total_printed": 500000000,
                    "series_1957": 350000000,
                    "series_1957A": 150000000
                }),
                "rarity": "common",
                "varieties": json.dumps([
                    {
                        "variety_id": "1957_regular",
                        "name": "Series 1957",
                        "description": "Original series 1957 issue",
                        "estimated_mintage": 350000000
                    },
                    {
                        "variety_id": "1957A_star",
                        "name": "Series 1957A Star Note",
                        "description": "Replacement note with star in serial number",
                        "estimated_mintage": 2000000
                    }
                ]),
                "source_citation": "Bureau of Engraving and Printing Production Records",
                "notes": "First small-size silver certificate series to feature 'IN GOD WE TRUST'",
                "metadata": json.dumps({
                    "collection_significance": "Post-war design standardization",
                    "historical_context": "Cold War era currency"
                }),
                
                # Paper currency specific fields
                "signature_combination": "Ivy Baker Priest / George M. Humphrey",
                "seal_color": "blue",
                "block_letter": "A",
                "serial_number_type": "8_digit_standard",
                "size_format": "small_size",
                "paper_type": "cotton_linen_blend",
                "watermark": None,
                "security_features": json.dumps([
                    "distinctive_paper",
                    "special_inks", 
                    "fine_line_printing",
                    "serial_numbers"
                ]),
                "printing_method": "intaglio",
                "series_designation": "Series 1957A",
                
                # Visual descriptions
                "obverse_description": "Portrait of George Washington in center, Federal Reserve Bank seal on left, Treasury seal on right, serial numbers in green ink",
                "reverse_description": "Great Seal of the United States with pyramid and all-seeing eye on left, eagle with shield and banner on right",
                "distinguishing_features": json.dumps([
                    "Blue treasury seal",
                    "Blue serial numbers", 
                    "Series 1957A designation",
                    "Federal Reserve Bank of Boston seal"
                ]),
                "identification_keywords": json.dumps([
                    "silver certificate",
                    "george washington",
                    "blue seal",
                    "series 1957A",
                    "federal reserve boston"
                ]),
                "seller_name": "Heritage Auctions"
            },
            {
                # $5 Federal Reserve Note
                "issue_id": "US-P005-1963-B",
                "object_type": "banknote", 
                "series_id": "us_paper_5_dollar",
                "country_code": "US",
                "authority_name": "Federal Reserve Bank of New York",
                "monetary_system": "decimal",
                "currency_unit": "dollar",
                "face_value": 5.0,
                "unit_name": "dollar",
                "common_names": json.dumps(["five dollar bill", "fiver", "lincoln"]),
                "system_fraction": "5 dollars",
                "issue_year": 1963,
                "mint_id": "B",
                "date_range_start": 1963,
                "date_range_end": 1969,
                "authority_period": json.dumps({
                    "entity_type": "federal_reserve_system",
                    "leader": {"name": "William McChesney Martin Jr.", "title": "Chairman of Federal Reserve"}
                }),
                "specifications": json.dumps({
                    "width_mm": 156,
                    "height_mm": 66,
                    "thickness_mm": 0.11,
                    "weight_grams": 1.0
                }),
                "sides": json.dumps({
                    "obverse": {
                        "design": "Abraham Lincoln portrait",
                        "designer": "Daniel Chester French (portrait basis)",
                        "elements": ["presidential portrait", "serial numbers", "treasury seal", "federal reserve seal"]
                    },
                    "reverse": {
                        "design": "Lincoln Memorial",
                        "designer": "Bureau of Engraving and Printing",
                        "elements": ["lincoln memorial building", "lincoln statue inside", "wreath design"]
                    }
                }),
                "mintage": json.dumps({
                    "total_printed": 800000000,
                    "series_1963": 800000000
                }),
                "rarity": "common",
                "varieties": json.dumps([
                    {
                        "variety_id": "1963_regular",
                        "name": "Series 1963",
                        "description": "Standard Federal Reserve Note",
                        "estimated_mintage": 800000000
                    }
                ]),
                "source_citation": "Federal Reserve Bank of New York Records",
                "notes": "Last series before 1976 bicentennial modifications",
                "metadata": json.dumps({
                    "collection_significance": "Pre-bicentennial standard design",
                    "historical_context": "Civil rights era currency"
                }),
                
                # Paper currency specific fields
                "signature_combination": "Kathryn O'Hay Granahan / C. Douglas Dillon",
                "seal_color": "green",
                "block_letter": "B",
                "serial_number_type": "8_digit_standard",
                "size_format": "small_size",
                "paper_type": "cotton_linen_blend",
                "watermark": None,
                "security_features": json.dumps([
                    "distinctive_paper",
                    "special_inks",
                    "fine_line_printing",
                    "serial_numbers",
                    "micro_printing"
                ]),
                "printing_method": "intaglio",
                "series_designation": "Series 1963",
                
                # Visual descriptions  
                "obverse_description": "Portrait of Abraham Lincoln in center, Federal Reserve Bank seal on left, Treasury seal on right, serial numbers in green ink",
                "reverse_description": "Lincoln Memorial building with Lincoln statue visible inside, ornate border design",
                "distinguishing_features": json.dumps([
                    "Green treasury seal",
                    "Green serial numbers",
                    "Series 1963 designation", 
                    "Federal Reserve Bank of New York seal",
                    "Lincoln Memorial on reverse"
                ]),
                "identification_keywords": json.dumps([
                    "federal reserve note",
                    "abraham lincoln",
                    "green seal",
                    "series 1963",
                    "lincoln memorial",
                    "federal reserve new york"
                ]),
                "seller_name": "Stack's Bowers"
            }
        ]
    
    def add_sample_data(self, dry_run=False):
        """Add sample paper currency data to the database."""
        print("💵 Adding sample paper currency data for testing...")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No data will be added")
            sample_data = self.get_sample_paper_currency_data()
            for item in sample_data:
                print(f"   Would add: {item['issue_id']} - {item['face_value']} dollar bill")
            return True
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            sample_data = self.get_sample_paper_currency_data()
            
            for item in sample_data:
                # Check if already exists
                cursor.execute("SELECT COUNT(*) FROM issues WHERE issue_id = ?", (item['issue_id'],))
                if cursor.fetchone()[0] > 0:
                    print(f"   → Already exists: {item['issue_id']}")
                    continue
                
                # Insert the paper currency record
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
                    item['issue_id'], item['object_type'], item['series_id'], item['country_code'],
                    item['authority_name'], item['monetary_system'], item['currency_unit'],
                    item['face_value'], item['unit_name'], item['common_names'], item['system_fraction'],
                    item['issue_year'], item['mint_id'], item['date_range_start'], item['date_range_end'],
                    item['authority_period'], item['specifications'], item['sides'], item['mintage'],
                    item['rarity'], item['varieties'], item['source_citation'], item['notes'],
                    item['metadata'], item['signature_combination'], item['seal_color'],
                    item['block_letter'], item['serial_number_type'], item['size_format'],
                    item['paper_type'], item['watermark'], item['security_features'],
                    item['printing_method'], item['series_designation'], item['obverse_description'],
                    item['reverse_description'], item['distinguishing_features'],
                    item['identification_keywords'], item['seller_name']
                ))
                
                print(f"   ✅ Added: {item['issue_id']} - ${item['face_value']} {item['series_designation']}")
            
            conn.commit()
            
            # Verify the data was added
            cursor.execute("SELECT COUNT(*) FROM issues WHERE object_type = 'banknote'")
            banknote_count = cursor.fetchone()[0]
            print(f"✅ Sample data added. Total banknotes in database: {banknote_count}")
            
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error adding sample data: {e}")
            return False
        finally:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='Add sample paper currency data for testing')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be added without making changes')
    args = parser.parse_args()
    
    adder = SamplePaperCurrencyAdder()
    
    try:
        success = adder.add_sample_data(dry_run=args.dry_run)
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Failed to add sample data: {e}")
        return 1

if __name__ == "__main__":
    exit(main())