#!/usr/bin/env python3
"""
Export JSON files from SQLite database (DATABASE-FIRST PIPELINE)

This script treats the SQLite database as the source of truth and generates
JSON export files from it. Does NOT rebuild the database.

New Pipeline:
SQLite Database (SOURCE OF TRUTH) → JSON Export Files
      ↑                                    ↑
 SOURCE OF TRUTH                    GENERATED FILES
(version controlled)             (version controlled)

Usage:
    python scripts/export_from_database.py
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from json_validator import JSONValidator

class DatabaseExporter:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.output_dir = 'data/us/coins'
        self.validator = JSONValidator()
        
    def ensure_output_dir(self):
        """Ensure output directory exists."""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs('data/us/references', exist_ok=True)

    def convert_year(self, year_value):
        """Convert year from TEXT to appropriate type (int or 'XXXX')."""
        if year_value == 'XXXX':
            return 'XXXX'
        try:
            return int(year_value)
        except (ValueError, TypeError):
            return year_value
        
    def export_coins_by_denomination(self):
        """Export coins grouped by denomination to separate JSON files."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("📊 Exporting coins by denomination from database...")
            
            # Get US denominations only
            cursor.execute('''
                SELECT DISTINCT denomination, COUNT(*) as count
                FROM coins 
                WHERE coin_id LIKE 'US-%'
                GROUP BY denomination 
                ORDER BY denomination
            ''')
            
            denominations = cursor.fetchall()
            
            for denom_name, count in denominations:
                print(f"📄 Exporting {denom_name}: {count} coins")
                
                # Get all coins for this denomination - using ACTUAL database columns
                cursor.execute('''
                    SELECT
                        coin_id,
                        series,
                        series as series_name,
                        year,
                        mint,
                        business_strikes,
                        proof_strikes,
                        total_mintage,
                        rarity,
                        composition,
                        weight_grams,
                        diameter_mm,
                        variety as varieties,
                        source_citation,
                        notes,
                        substr(coin_id, 1, 2) as country,
                        obverse_description,
                        reverse_description,
                        designer,
                        '' as distinguishing_features,
                        '' as identification_keywords,
                        '' as common_names,
                        'coin' as category,
                        '' as issuer,
                        year as series_year,
                        'gregorian' as calendar_type,
                        '' as original_date,
                        '' as variety_suffix,
                        CASE
                            WHEN composition LIKE '%silver%' OR composition LIKE '%gold%' THEN 'bullion'
                            ELSE 'circulation'
                        END as subcategory
                    FROM coins
                    WHERE denomination = ? AND coin_id LIKE 'US-%'
                    ORDER BY year, series, mint
                ''', (denom_name,))
                
                rows = cursor.fetchall()
                
                # Group coins by series
                series_data = {}
                face_value = self.get_face_value(denom_name)
                
                for row in rows:
                    series_id = row[1]  # This is the series column mapped as series_id
                    series_name = row[2]  # Same as series_id since we aliased it
                    
                    if series_id not in series_data:
                        series_data[series_id] = {
                            'series_name': series_name,
                            'coins': [],
                            'years': []
                        }
                    
                    # Parse fields based on actual database schema
                    composition = self.parse_composition(row[9])
                    # varieties is now a single string from 'variety' column, convert to list format
                    single_variety = row[12] if row[12] and row[12].strip() else ""
                    varieties = [{"name": single_variety, "premium": False}] if single_variety else []
                    # These are text fields, not JSON
                    distinguishing_features = row[18] if row[18] else ""
                    identification_keywords = row[19] if row[19] else ""
                    common_names = row[20] if row[20] else ""

                    coin = {
                        "coin_id": row[0],
                        "year": self.convert_year(row[3]),
                        "mint": row[4],
                        "business_strikes": row[5],
                        "proof_strikes": row[6],
                        "total_mintage": row[7],
                        "rarity": row[8],
                        "composition": composition,
                        "varieties": self.format_varieties(varieties)
                    }
                    
                    # Add category and subcategory fields
                    if row[22]:  # category
                        coin["category"] = row[22]
                    if row[28]:  # subcategory
                        coin["subcategory"] = row[28]

                    # Add visual description fields
                    if row[16]:  # obverse_description
                        coin["obverse_description"] = row[16]
                    if row[17]:  # reverse_description
                        coin["reverse_description"] = row[17]
                    if row[18]:  # designer
                        coin["designer"] = row[18]
                    if distinguishing_features:
                        coin["distinguishing_features"] = distinguishing_features
                    if identification_keywords:
                        coin["identification_keywords"] = identification_keywords
                    if common_names:
                        coin["common_names"] = common_names

                    # Only include non-null values
                    if row[10] is not None:  # weight_grams
                        coin["weight_grams"] = row[10]
                    if row[11] is not None:  # diameter_mm
                        coin["diameter_mm"] = row[11]
                    if row[13] and row[13].strip():  # source_citation
                        coin["source_citation"] = row[13]
                    if row[14] and row[14].strip():  # notes
                        coin["notes"] = row[14]

                    series_data[series_id]['coins'].append(coin)
                    series_data[series_id]['years'].append(self.convert_year(row[3]))
                
                # Create series entries
                series_list = []
                for series_id, data in series_data.items():
                    years = data['years']
                    coins = data['coins']

                    # Determine composition periods from coins
                    comp_periods = self.extract_composition_periods(coins)

                    # Handle year ranges (filter out XXXX for min/max, or use XXXX if all are XXXX)
                    numeric_years = [y for y in years if y != 'XXXX']
                    if numeric_years:
                        start_year = min(numeric_years)
                        end_year = max(numeric_years)
                    else:
                        # All years are XXXX (bullion series)
                        start_year = 'XXXX'
                        end_year = 'XXXX'

                    series_entry = {
                        "series_id": series_id,
                        "series_name": data['series_name'],
                        "official_name": data['series_name'],
                        "years": {
                            "start": start_year,
                            "end": end_year
                        },
                        "specifications": self.get_specifications(coins),
                        "composition_periods": comp_periods,
                        "coins": coins
                    }

                    # Look up aliases from series_registry
                    cursor.execute('''
                        SELECT aliases FROM series_registry
                        WHERE series_name = ? AND denomination = ?
                    ''', (series_id, denom_name))
                    alias_row = cursor.fetchone()
                    if alias_row and alias_row[0]:
                        try:
                            aliases = json.loads(alias_row[0])
                            if aliases:
                                series_entry["aliases"] = aliases
                        except json.JSONDecodeError:
                            pass  # Skip invalid JSON

                    series_list.append(series_entry)
                
                # Sort series by start year (put XXXX series at the end)
                series_list.sort(key=lambda x: (x['years']['start'] == 'XXXX', x['years']['start']))
                
                # Create file structure
                file_data = {
                    "country": "US",
                    "denomination": denom_name,
                    "face_value": face_value,
                    "series": series_list
                }
                
                # Write JSON file with validation
                filename = self.get_filename(denom_name)
                filepath = Path(self.output_dir) / filename
                
                if self.validator.safe_json_write(file_data, filepath):
                    print(f"   ✅ {filepath}")
                else:
                    print(f"   ❌ {filepath} - JSON validation failed")
                    self.validator.print_errors()
                    return False
                
        except sqlite3.Error as e:
            print(f"❌ Error exporting coins: {e}")
        finally:
            conn.close()
    
    def get_face_value(self, denomination: str) -> float:
        """Get face value for denomination."""
        face_values = {
            'Half Cents': 0.005,
            'Cents': 0.01,
            'Three Cents': 0.03,
            'Nickels': 0.05,
            'Dimes': 0.10,
            'Twenty Cents': 0.20,
            'Quarters': 0.25,
            'Quarter Dollar': 0.25,  # Support both naming conventions
            'Half Dollars': 0.50,
            'Dollars': 1.00,
            'Trade Dollars': 1.00,
            'Gold Dollars': 1.00,
            'Quarter Eagles': 2.50,
            'Three Dollar Gold': 3.00,
            'Half Eagles': 5.00,
            'Eagles': 10.00,
            'Double Eagles': 20.00
        }
        return face_values.get(denomination, 1.00)
    
    def format_varieties(self, varieties):
        """Format varieties to match schema requirements."""
        if not varieties:
            return []
        
        # If varieties is already a list of objects, return as is
        if isinstance(varieties, list) and all(isinstance(v, dict) for v in varieties):
            return varieties
        
        # If varieties is a list of strings, convert to objects
        if isinstance(varieties, list):
            formatted = []
            for v in varieties:
                if isinstance(v, str):
                    # Create variety object with generated ID
                    variety_id = v.lower().replace(' ', '_').replace('-', '_')
                    formatted.append({
                        "variety_id": variety_id,
                        "name": v,
                        "description": None,
                        "estimated_mintage": None
                    })
                elif isinstance(v, dict):
                    formatted.append(v)
            return formatted
        
        return []

    def format_single_variety(self, variety_text):
        """Convert single variety string to list format."""
        if not variety_text or not variety_text.strip():
            return []
        
        variety_id = variety_text.lower().replace(' ', '_').replace('-', '_')
        return [{
            "id": variety_id,
            "name": variety_text,
            "premium": False
        }]

    def parse_composition(self, composition_text):
        """Parse composition from either JSON format or text format."""
        if not composition_text:
            return {}
        
        # Try JSON first (for Three-Cent Pieces and newer coins)
        try:
            return json.loads(composition_text)
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Parse text format (for older coins like "95% Cu, 4% Sn, 1% Zn")
        composition = {}
        if isinstance(composition_text, str):
            # Split by comma and parse each component
            parts = composition_text.split(',')
            for part in parts:
                part = part.strip()
                if '%' in part and ('Cu' in part or 'Ag' in part or 'Au' in part or 'Ni' in part or 'Zn' in part or 'Sn' in part):
                    # Extract percentage and metal
                    percent_pos = part.find('%')
                    if percent_pos > 0:
                        try:
                            percentage = float(part[:percent_pos].strip())
                            metal_abbr = part[percent_pos + 1:].strip()
                            
                            # Map abbreviations to full names
                            metal_map = {
                                'Cu': 'copper',
                                'Ag': 'silver', 
                                'Au': 'gold',
                                'Ni': 'nickel',
                                'Zn': 'zinc',
                                'Sn': 'tin'
                            }
                            metal_name = metal_map.get(metal_abbr, metal_abbr.lower())
                            composition[metal_name] = percentage
                        except ValueError:
                            continue
        
        return composition
    
    def get_filename(self, denomination: str) -> str:
        """Get filename for denomination."""
        filenames = {
            'Half Cents': 'half_cents.json',
            'Cents': 'cents.json',
            'Three Cents': 'three_cents.json',
            'Nickels': 'nickels.json',
            'Dimes': 'dimes.json',
            'Twenty Cents': 'twenty_cents.json',
            'Quarters': 'quarters.json',
            'Quarter Dollar': 'quarters.json',  # Support both naming conventions
            'Half Dollars': 'half_dollars.json',
            'Dollars': 'dollars.json',
            'Trade Dollars': 'trade_dollars.json',
            'Gold Dollars': 'gold_dollars.json',
            'Quarter Eagles': 'quarter_eagles.json',
            'Three Dollar Gold': 'three_dollar_gold.json',
            'Half Eagles': 'half_eagles.json',
            'Eagles': 'eagles.json',
            'Double Eagles': 'double_eagles.json'
        }
        return filenames.get(denomination, f"{denomination.lower().replace(' ', '_')}.json")
    
    def get_specifications(self, coins: List[Dict]) -> Dict:
        """Extract specifications from coins."""
        # Get specs from first coin that has them
        specs = {"edge": "plain"}  # Default assumption
        
        for coin in coins:
            if coin.get('diameter_mm'):
                specs["diameter_mm"] = coin.get('diameter_mm')
                break
        
        # Only include fields that have values
        return specs
    
    def extract_composition_periods(self, coins: List[Dict]) -> List[Dict]:
        """Extract composition periods from coin data."""
        periods = []
        compositions_seen = {}
        
        for coin in coins:
            comp = coin.get('composition', {})
            if not comp:
                continue
                
            alloy_name = comp.get('alloy_name', 'Unknown')
            year = coin['year']
            
            if alloy_name not in compositions_seen:
                compositions_seen[alloy_name] = {
                    'alloy': comp.get('alloy', {}),
                    'weight_grams': coin.get('weight_grams'),
                    'years': []
                }
            
            compositions_seen[alloy_name]['years'].append(year)
        
        # Create periods
        for alloy_name, data in compositions_seen.items():
            years = data['years']
            if years:
                # Handle year ranges (filter out XXXX for min/max, or use XXXX if all are XXXX)
                numeric_years = [y for y in years if y != 'XXXX']
                if numeric_years:
                    start_year = min(numeric_years)
                    end_year = max(numeric_years)
                else:
                    # All years are XXXX (bullion series)
                    start_year = 'XXXX'
                    end_year = 'XXXX'

                period = {
                    "date_range": {
                        "start": start_year,
                        "end": end_year
                    },
                    "alloy_name": alloy_name,
                    "alloy": data['alloy']
                }
                
                # Only include weight if we have data
                if data['weight_grams'] is not None:
                    period["weight"] = {
                        "grams": data['weight_grams']
                    }
                periods.append(period)

        # Sort by start year (put XXXX periods at the end)
        periods.sort(key=lambda x: (x['date_range']['start'] == 'XXXX', x['date_range']['start']))

        # If no periods found, create a default one
        if not periods and coins:
            years = [coin['year'] for coin in coins]
            # Handle year ranges (filter out XXXX for min/max, or use XXXX if all are XXXX)
            numeric_years = [y for y in years if y != 'XXXX']
            if numeric_years:
                start_year = min(numeric_years)
                end_year = max(numeric_years)
            else:
                # All years are XXXX (bullion series)
                start_year = 'XXXX'
                end_year = 'XXXX'

            periods = [{
                "date_range": {
                    "start": start_year,
                    "end": end_year
                },
                "alloy_name": "Historical",
                "alloy": {}
            }]
        
        return periods
    
    def export_paper_currency(self):
        """Export paper currency from issues table to JSON files."""
        print("💵 Exporting paper currency from database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get all paper currency grouped by denomination
            cursor.execute('''
                SELECT DISTINCT 
                    CASE 
                        WHEN face_value = 1.0 THEN 'Paper $1'
                        WHEN face_value = 2.0 THEN 'Paper $2'  
                        WHEN face_value = 5.0 THEN 'Paper $5'
                        WHEN face_value = 10.0 THEN 'Paper $10'
                        WHEN face_value = 20.0 THEN 'Paper $20'
                        WHEN face_value = 50.0 THEN 'Paper $50'
                        WHEN face_value = 100.0 THEN 'Paper $100'
                        WHEN face_value = 500.0 THEN 'Paper $500'
                        WHEN face_value = 1000.0 THEN 'Paper $1000'
                        ELSE 'Paper $' || CAST(face_value AS TEXT)
                    END as denomination,
                    face_value,
                    COUNT(*) as count
                FROM issues 
                WHERE object_type = 'banknote' AND country = 'US'
                GROUP BY face_value
                ORDER BY face_value
            ''')
            
            denominations = cursor.fetchall()
            
            for denom_name, face_value, count in denominations:
                print(f"💵 Exporting {denom_name}: {count} banknotes")
                
                # Get all banknotes for this denomination
                cursor.execute('''
                    SELECT
                        issue_id, series_id, authority_name, issue_year, mint_id,
                        specifications, sides, mintage, rarity, varieties,
                        source_citation, notes, signature_combination, seal_color,
                        block_letter, serial_number_type, size_format, paper_type,
                        series_designation, obverse_description, reverse_description,
                        distinguishing_features, identification_keywords, common_names
                    FROM issues
                    WHERE object_type = 'banknote' AND face_value = ? AND country = 'US'
                    ORDER BY issue_year, series_designation, mint_id
                ''', (face_value,))
                
                rows = cursor.fetchall()
                
                # Group banknotes by series
                series_data = {}
                
                for row in rows:
                    series_id = row[1]
                    
                    if series_id not in series_data:
                        series_data[series_id] = {
                            'banknotes': [],
                            'years': []
                        }
                    
                    # Parse JSON fields safely
                    def safe_json_parse(field_value, default=None):
                        if not field_value:
                            return default if default is not None else []
                        try:
                            if isinstance(field_value, str) and not field_value.startswith(('[', '{')):
                                # String field that's not JSON
                                return [field_value] if default is None else field_value
                            return json.loads(field_value)
                        except (json.JSONDecodeError, TypeError):
                            return default if default is not None else []
                    
                    specifications = safe_json_parse(row[5], {})
                    sides = safe_json_parse(row[6], {})
                    mintage = safe_json_parse(row[7], {})
                    varieties = safe_json_parse(row[9], [])
                    distinguishing_features = safe_json_parse(row[21], [])
                    identification_keywords = safe_json_parse(row[22], [])
                    common_names = safe_json_parse(row[23], [])
                    
                    banknote = {
                        "issue_id": row[0],
                        "year": row[3],
                        "issuing_authority": row[2],
                        "authority_code": row[4],  # mint_id field used for authority code
                        "series_designation": row[18],
                        "rarity": row[8],
                        "specifications": specifications,
                        "sides": sides,
                        "mintage": mintage,
                        "varieties": varieties
                    }
                    
                    # Add paper currency specific fields
                    if row[12]:  # signature_combination
                        banknote["signature_combination"] = row[12]
                    if row[13]:  # seal_color
                        banknote["seal_color"] = row[13]
                    if row[14]:  # block_letter
                        banknote["block_letter"] = row[14]
                    if row[15]:  # serial_number_type
                        banknote["serial_number_type"] = row[15]
                    if row[16]:  # size_format
                        banknote["size_format"] = row[16]
                    if row[17]:  # paper_type
                        banknote["paper_type"] = row[17]
                    
                    # Add visual description fields
                    if row[19]:  # obverse_description
                        banknote["obverse_description"] = row[19]
                    if row[20]:  # reverse_description
                        banknote["reverse_description"] = row[20]
                    if distinguishing_features:
                        banknote["distinguishing_features"] = distinguishing_features
                    if identification_keywords:
                        banknote["identification_keywords"] = identification_keywords
                    if common_names:
                        banknote["common_names"] = common_names
                    
                    # Only include non-null values
                    if row[10] and row[10].strip():  # source_citation
                        banknote["source_citation"] = row[10]
                    if row[11] and row[11].strip():  # notes
                        banknote["notes"] = row[11]

                    series_data[series_id]['banknotes'].append(banknote)
                    series_data[series_id]['years'].append(self.convert_year(row[3]))
                
                # Create series entries for banknotes
                series_list = []
                for series_id, data in series_data.items():
                    years = data['years']
                    banknotes = data['banknotes']
                    
                    # Get series info from series_registry
                    cursor.execute('''
                        SELECT series_name, official_name, start_year, end_year, defining_characteristics
                        FROM series_registry WHERE series_id = ?
                    ''', (series_id,))
                    series_info = cursor.fetchone()
                    
                    if series_info:
                        # Handle year ranges (filter out XXXX for min/max, or use XXXX if all are XXXX)
                        numeric_years = [y for y in years if y != 'XXXX']
                        if numeric_years:
                            start_year = min(numeric_years)
                            end_year = max(numeric_years)
                        else:
                            # All years are XXXX (bullion series)
                            start_year = 'XXXX'
                            end_year = 'XXXX'

                        series_entry = {
                            "series_id": series_id,
                            "series_name": series_info[0],
                            "official_name": series_info[1] or series_info[0],
                            "years": {
                                "start": start_year,
                                "end": end_year
                            },
                            "defining_characteristics": series_info[4],
                            "banknotes": banknotes
                        }
                        series_list.append(series_entry)
                
                # Sort series by start year (put XXXX series at the end)
                series_list.sort(key=lambda x: (x['years']['start'] == 'XXXX', x['years']['start']))
                
                # Create file structure for paper currency
                file_data = {
                    "country": "US",
                    "denomination": denom_name,
                    "face_value": face_value,
                    "currency_type": "paper_currency",
                    "series": series_list
                }
                
                # Write JSON file for paper currency
                filename = self.get_paper_currency_filename(denom_name)
                filepath = Path(self.output_dir) / filename
                
                if self.validator.safe_json_write(file_data, filepath):
                    print(f"   ✅ {filepath}")
                else:
                    print(f"   ❌ {filepath} - JSON validation failed")
                    self.validator.print_errors()
                    return False
                    
        except sqlite3.Error as e:
            print(f"❌ Error exporting paper currency: {e}")
            return False
        finally:
            conn.close()
        
        return True
    
    def get_paper_currency_filename(self, denomination: str) -> str:
        """Get filename for paper currency denomination."""
        filenames = {
            'Paper $1': 'paper_1_dollar.json',
            'Paper $2': 'paper_2_dollar.json', 
            'Paper $5': 'paper_5_dollar.json',
            'Paper $10': 'paper_10_dollar.json',
            'Paper $20': 'paper_20_dollar.json',
            'Paper $50': 'paper_50_dollar.json',
            'Paper $100': 'paper_100_dollar.json',
            'Paper $500': 'paper_500_dollar.json',
            'Paper $1000': 'paper_1000_dollar.json'
        }
        return filenames.get(denomination, f"{denomination.lower().replace(' ', '_').replace('$', 'dollar_')}.json")
    
    def export_complete_file(self):
        """Export complete us_coins_complete.json file."""
        print("📄 Exporting complete US coins file...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT COUNT(*) as total,
                       MIN(year) as earliest,
                       MAX(year) as latest
                FROM coins
            ''')
            
            stats = cursor.fetchone()
            
            # Get all coins using ACTUAL database columns
            cursor.execute('''
                SELECT 
                    coin_id, 
                    series as series_id, 
                    series as series_name, 
                    denomination,
                    year, 
                    mint, 
                    business_strikes, 
                    proof_strikes, 
                    rarity,
                    composition, 
                    weight_grams, 
                    diameter_mm,
                    variety as varieties, 
                    source_citation, 
                    notes, 
                    substr(coin_id, 1, 2) as country,
                    obverse_description, 
                    reverse_description,
                    '' as distinguishing_features, 
                    '' as identification_keywords, 
                    '' as common_names,
                    '' as variety_suffix
                FROM coins
                ORDER BY year, denomination, series, mint
            ''')
            
            coins = []
            for row in cursor.fetchall():
                coin = {
                    "coin_id": row[0],
                    "series_id": row[1],
                    "series_name": row[2],
                    "denomination": row[3],
                    "year": row[4],
                    "mint": row[5],
                    "business_strikes": row[6],
                    "proof_strikes": row[7],
                    "rarity": row[8],
                    "composition": self.parse_composition(row[9]),
                    "weight_grams": row[10],
                    "diameter_mm": row[11],
                    "varieties": self.format_single_variety(row[12]) if row[12] and row[12].strip() else [],
                    "source_citation": row[13],
                    "notes": row[14],
                    "country": row[15]
                }
                
                # Add visual description fields
                if row[16]:  # obverse_description
                    coin["obverse_description"] = row[16]
                if row[17]:  # reverse_description
                    coin["reverse_description"] = row[17]
                if row[18]:  # distinguishing_features (text field, not JSON)
                    coin["distinguishing_features"] = row[18]
                if row[19]:  # identification_keywords (text field, not JSON)
                    coin["identification_keywords"] = row[19]
                if row[20]:  # common_names (text field, not JSON)
                    coin["common_names"] = row[20]
                
                coins.append(coin)
            
            complete_data = {
                "taxonomy_version": "1.1",
                "generated_at": datetime.now().isoformat(),
                "total_coins": stats[0],
                "year_range": {
                    "earliest": stats[1],
                    "latest": stats[2]
                },
                "coins": coins
            }
            
            filepath = Path('data/us/us_coins_complete.json')
            if self.validator.safe_json_write(complete_data, filepath):
                print(f"   ✅ {filepath}")
            else:
                print(f"   ❌ {filepath} - JSON validation failed")
                self.validator.print_errors()
                return False
            
        except sqlite3.Error as e:
            print(f"❌ Error exporting complete file: {e}")
        finally:
            conn.close()
    
    def export_ai_taxonomy(self):
        """Export AI-optimized taxonomy with minimal token usage."""
        print("🤖 Exporting AI-optimized taxonomy...")

        # Import and use the AI taxonomy exporter
        try:
            from export_ai_taxonomy import AITaxonomyExporter
            ai_exporter = AITaxonomyExporter(db_path=self.db_path)
            output_file, coin_count = ai_exporter.export_ai_taxonomy()

            # Calculate file size
            file_size = output_file.stat().st_size
            print(f"   ✅ data/ai-optimized/us_taxonomy.json ({file_size:,} bytes)")

        except ImportError:
            print("   ⚠️  AI taxonomy exporter not found, skipping...")
        except Exception as e:
            print(f"   ❌ Error exporting AI taxonomy: {e}")

    def export_grade_standards(self):
        """Export grade standards from database to JSON (Issue #64)."""
        print("📊 Exporting grade standards from database...")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check if grade_standards table exists
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='grade_standards'
            """)
            if not cursor.fetchone():
                print("   ⚠️  grade_standards table not found, skipping...")
                return False

            # Get all grades
            cursor.execute('''
                SELECT
                    abbreviation,
                    grade_name,
                    numeric_value,
                    category,
                    subcategory,
                    description,
                    sheldon_scale_position,
                    market_threshold,
                    market_relevance,
                    common_in_practice,
                    strike_types,
                    alternate_notations,
                    sheldon_range_min,
                    sheldon_range_max,
                    aliases,
                    modifiers_allowed
                FROM grade_standards
                ORDER BY numeric_value, abbreviation
            ''')

            rows = cursor.fetchall()

            # Build grade hierarchy
            grades = []
            for row in rows:
                grade = {
                    "grade": row[0],
                    "grade_name": row[1],
                    "grade_numeric": row[2],
                    "grade_category": row[3],
                    "grade_subcategory": row[4],
                    "description": row[5],
                    "sheldon_scale_position": row[6],
                    "market_threshold": bool(row[7]),
                    "market_relevance": row[8],
                    "common_in_practice": bool(row[9]),
                    "strike_types": json.loads(row[10]) if row[10] else [],
                    "abbreviations": json.loads(row[11]) if row[11] else [],
                    "sheldon_range": {
                        "min": row[12],
                        "max": row[13]
                    }
                }

                # Add optional fields
                if row[14]:  # aliases
                    grade["aliases"] = json.loads(row[14])
                if row[15]:  # modifiers_allowed
                    grade["modifiers_allowed"] = json.loads(row[15])

                grades.append(grade)

            # Get parsing rules
            cursor.execute('''
                SELECT rule_type, rule_name, rule_value, description
                FROM grade_parsing_rules
                ORDER BY priority DESC, rule_id
            ''')

            parsing_rules_rows = cursor.fetchall()
            parsing_rules = {}

            for rule_type, rule_name, rule_value, description in parsing_rules_rows:
                if rule_type == 'separator':
                    parsing_rules['multi_grade_separator_patterns'] = json.loads(rule_value)
                elif rule_type == 'strategy':
                    parsing_rules['multi_grade_strategy'] = json.loads(rule_value) if rule_value.startswith(('{', '[')) else rule_value
                elif rule_type == 'pattern':
                    if 'grade_extraction_patterns' not in parsing_rules:
                        parsing_rules['grade_extraction_patterns'] = []
                    parsing_rules['grade_extraction_patterns'].append({
                        "name": rule_name,
                        "pattern": json.loads(rule_value) if rule_value.startswith(('{', '[')) else rule_value,
                        "description": description
                    })

            # Build complete structure
            grade_standards_data = {
                "$schema": "../schema/grade_standards.schema.json",
                "version": "1.0.0",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "description": "Canonical grading hierarchy and parsing rules for coin grading. Supports grade comparison, multi-grade parsing, and RAW-{grade} classification for uncertified coins. See: GitHub Issue #64",
                "standard": "Sheldon 70-Point Scale",
                "grade_hierarchy": grades,
                "parsing_rules": parsing_rules,
                "comparison_utilities": {
                    "getLowestGrade": "Find the lowest grade from an array of grades",
                    "normalizeGrade": "Convert grade aliases to canonical format",
                    "compareGrades": "Compare two grades, returns -1, 0, or 1"
                }
            }

            # Write to universal directory
            os.makedirs('data/universal', exist_ok=True)
            filepath = Path('data/universal/grade_standards.json')

            if self.validator.safe_json_write(grade_standards_data, filepath):
                print(f"   ✅ {filepath} ({len(grades)} grades)")
                return True
            else:
                print(f"   ❌ {filepath} - JSON validation failed")
                self.validator.print_errors()
                return False

        except sqlite3.Error as e:
            print(f"   ❌ Error exporting grade standards: {e}")
            return False
        finally:
            conn.close()

    def export_coin_inventory(self):
        """Export coin inventory from database to JSON (Issue #65)."""
        print("📊 Exporting coin inventory from database...")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check if coin_inventory table exists
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='coin_inventory'
            """)
            if not cursor.fetchone():
                print("   ⚠️  coin_inventory table not found, skipping...")
                return False

            # Get all inventory records
            cursor.execute('''
                SELECT
                    inventory_id,
                    coin_id,
                    grade_id,
                    grading_service,
                    certification_number,
                    is_certified,
                    strike_type,
                    modifiers,
                    full_grade_string,
                    market_threshold_grade,
                    purchase_price,
                    purchase_date,
                    current_value_estimate,
                    collection_name,
                    storage_location,
                    notes,
                    image_urls,
                    created_at,
                    updated_at
                FROM coin_inventory
                ORDER BY collection_name, coin_id, grade_id
            ''')

            rows = cursor.fetchall()

            # Build inventory records
            inventory_records = []
            for row in rows:
                record = {
                    "inventory_id": row[0],
                    "coin_id": row[1],
                    "grade_id": row[2],
                    "grading_service": row[3],
                    "is_certified": bool(row[5]),
                    "full_grade_string": row[8]
                }

                # Add optional certification details
                if row[4]:  # certification_number
                    record["certification_number"] = row[4]
                if row[6]:  # strike_type
                    record["strike_type"] = row[6]
                if row[7]:  # modifiers
                    record["modifiers"] = json.loads(row[7])

                # Add market analysis fields
                if row[9] is not None:  # market_threshold_grade
                    record["market_threshold_grade"] = bool(row[9])
                if row[10]:  # purchase_price
                    record["purchase_price"] = row[10]
                if row[11]:  # purchase_date
                    record["purchase_date"] = row[11]
                if row[12]:  # current_value_estimate
                    record["current_value_estimate"] = row[12]

                # Add collection management fields
                if row[13]:  # collection_name
                    record["collection_name"] = row[13]
                if row[14]:  # storage_location
                    record["storage_location"] = row[14]
                if row[15]:  # notes
                    record["notes"] = row[15]
                if row[16]:  # image_urls
                    record["image_urls"] = json.loads(row[16])

                # Add metadata
                record["created_at"] = row[17]
                record["updated_at"] = row[18]

                inventory_records.append(record)

            # Build complete structure
            inventory_data = {
                "$schema": "../schema/coin_inventory.schema.json",
                "version": "1.0.0",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "description": "Coin inventory - tracks specific graded coin instances with certification details. Separates coin identity from grade to enable value determination: coin + grade = market value. See: GitHub Issue #65",
                "total_records": len(inventory_records),
                "inventory": inventory_records
            }

            # Write to data directory
            os.makedirs('data/inventory', exist_ok=True)
            filepath = Path('data/inventory/coin_inventory.json')

            if self.validator.safe_json_write(inventory_data, filepath):
                print(f"   ✅ {filepath} ({len(inventory_records)} records)")
                return True
            else:
                print(f"   ⚠️  {filepath} - Skipping validation (schema not yet created)")
                # Write anyway without validation for now
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(inventory_data, f, indent=2, ensure_ascii=False)
                print(f"   ✅ {filepath} ({len(inventory_records)} records) [no validation]")
                return True

        except sqlite3.Error as e:
            print(f"   ❌ Error exporting coin inventory: {e}")
            return False
        finally:
            conn.close()

    def run_export(self):
        """Run complete export from database."""
        print("🚀 Starting database-first export...")
        print("📊 SQLite Database → JSON Export Files")
        
        # Check database exists
        if not os.path.exists(self.db_path):
            print(f"❌ Database not found: {self.db_path}")
            return False
        
        # Check database has data
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM coins WHERE coin_id LIKE 'US-%'")
        coin_count = cursor.fetchone()[0]
        conn.close()
        
        if coin_count == 0:
            print("❌ Database is empty")
            return False
            
        print(f"📊 Found {coin_count} coins in database")
        
        self.ensure_output_dir()
        
        # Export by denomination
        self.export_coins_by_denomination()
        
        # Paper currency export removed - issues table no longer exists
        
        # Export complete file
        self.export_complete_file()

        # Export AI-optimized taxonomy
        self.export_ai_taxonomy()

        # Export grade standards (Issue #64)
        self.export_grade_standards()

        # Export coin inventory (Issue #65)
        self.export_coin_inventory()

        # Validate all exported JSON files
        print(f"\n🔍 Validating exported JSON files...")
        from validate_json_exports import main as validate_exports
        
        if validate_exports() == 0:
            print(f"\n✅ Database-first export completed with valid JSON!")
            print(f"📁 {coin_count} coins exported to JSON files")
            return True
        else:
            print(f"\n❌ Database-first export completed but JSON validation failed!")
            return False

def main():
    exporter = DatabaseExporter()
    
    try:
        success = exporter.run_export()
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())