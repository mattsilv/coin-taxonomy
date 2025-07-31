#!/usr/bin/env python3
"""
AI-Optimized Taxonomy Validation
Validates the AI-optimized taxonomy format for correctness and completeness.
"""

import json
import os
from pathlib import Path

class AITaxonomyValidator:
    def __init__(self, taxonomy_file="data/ai-optimized/us_taxonomy.json"):
        self.taxonomy_file = Path(taxonomy_file)
        self.errors = []
        self.warnings = []
        
    def validate_format(self):
        """Validate the AI taxonomy file format and structure."""
        print("🤖 Validating AI-optimized taxonomy format...")
        
        # Check file exists
        if not self.taxonomy_file.exists():
            self.errors.append(f"AI taxonomy file not found: {self.taxonomy_file}")
            return False
        
        # Load and parse JSON
        try:
            with open(self.taxonomy_file, 'r') as f:
                taxonomy = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON format: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return False
        
        # Validate root structure
        self._validate_root_structure(taxonomy)
        
        # Validate coin entries
        if 'coins' in taxonomy:
            self._validate_coins(taxonomy['coins'])
        
        # Check for errors
        if self.errors:
            print(f"❌ Validation failed with {len(self.errors)} errors:")
            for error in self.errors:
                print(f"   • {error}")
            return False
        
        if self.warnings:
            print(f"⚠️  {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        print(f"✅ AI taxonomy validation passed")
        return True
    
    def _validate_root_structure(self, taxonomy):
        """Validate root-level structure."""
        required_fields = ['format', 'country', 'generated', 'total_coins', 'coins']
        
        for field in required_fields:
            if field not in taxonomy:
                self.errors.append(f"Missing required field: {field}")
        
        # Validate format version
        if taxonomy.get('format') != 'ai-taxonomy-v1':
            self.errors.append(f"Invalid format version: {taxonomy.get('format')}")
        
        # Validate country
        if taxonomy.get('country') != 'US':
            self.warnings.append(f"Unexpected country code: {taxonomy.get('country')}")
        
        # Validate total_coins matches array length
        total_coins = taxonomy.get('total_coins', 0)
        actual_count = len(taxonomy.get('coins', []))
        if total_coins != actual_count:
            self.errors.append(f"total_coins mismatch: declared {total_coins}, actual {actual_count}")
    
    def _validate_coins(self, coins):
        """Validate individual coin entries."""
        if not isinstance(coins, list):
            self.errors.append("'coins' must be an array")
            return
        
        coin_ids = set()
        
        for i, coin in enumerate(coins):
            if not isinstance(coin, dict):
                self.errors.append(f"Coin {i}: must be an object")
                continue
            
            # Validate required fields
            if 'id' not in coin:
                self.errors.append(f"Coin {i}: missing required 'id' field")
                continue
            
            coin_id = coin['id']
            
            # Check for duplicate IDs  
            if coin_id in coin_ids:
                self.errors.append(f"Duplicate coin ID: {coin_id}")
            coin_ids.add(coin_id)
            
            # Validate coin ID format
            self._validate_coin_id(coin_id, i)
            
            # Validate required fields
            required_fields = ['y', 'm', 's', 't']
            for field in required_fields:
                if field not in coin:
                    self.errors.append(f"Coin {coin_id}: missing required field '{field}'")
            
            # Validate field types and formats
            self._validate_coin_fields(coin, coin_id)
    
    def _validate_coin_id(self, coin_id, index):
        """Validate coin ID format: US-TYPE-YEAR-MINT"""
        parts = coin_id.split('-')
        
        if len(parts) != 4:
            self.errors.append(f"Coin {index}: invalid coin_id format '{coin_id}' - must have exactly 4 parts")
            return
        
        country, type_code, year, mint = parts
        
        # Validate country
        if country != 'US':
            self.errors.append(f"Coin {coin_id}: invalid country code '{country}'")
        
        # Validate type code (4 uppercase letters)
        if not (len(type_code) == 4 and type_code.isupper() and type_code.isalpha()):
            self.errors.append(f"Coin {coin_id}: invalid type code '{type_code}' - must be 4 uppercase letters")
        
        # Validate year (4 digits)
        if not (len(year) == 4 and year.isdigit()):
            self.errors.append(f"Coin {coin_id}: invalid year '{year}' - must be 4 digits")
        else:
            year_int = int(year)
            if year_int < 1793 or year_int > 2030:
                self.warnings.append(f"Coin {coin_id}: unusual year {year_int}")
        
        # Validate mint (1-2 uppercase letters)
        if not (1 <= len(mint) <= 2 and mint.isupper() and mint.isalpha()):
            self.errors.append(f"Coin {coin_id}: invalid mint code '{mint}' - must be 1-2 uppercase letters")
    
    def _validate_coin_fields(self, coin, coin_id):
        """Validate individual coin fields."""
        # Validate year
        if 'y' in coin:
            if not isinstance(coin['y'], int):
                self.errors.append(f"Coin {coin_id}: 'y' must be an integer")
        
        # Validate mint
        if 'm' in coin:
            if not isinstance(coin['m'], str):
                self.errors.append(f"Coin {coin_id}: 'm' must be a string")
        
        # Validate series name
        if 's' in coin:
            if not isinstance(coin['s'], str) or len(coin['s'].strip()) == 0:
                self.errors.append(f"Coin {coin_id}: 's' must be a non-empty string")
        
        # Validate type code
        if 't' in coin:
            if not isinstance(coin['t'], str) or len(coin['t']) != 4:
                self.errors.append(f"Coin {coin_id}: 't' must be a 4-character string")
        
        # Validate rarity (optional)
        if 'r' in coin:
            valid_rarities = ['key', 'semi-key', 'scarce']
            if coin['r'] not in valid_rarities:
                self.errors.append(f"Coin {coin_id}: 'r' must be one of {valid_rarities}")
        
        # Validate varieties (optional array)
        if 'v' in coin:
            if not isinstance(coin['v'], list):
                self.errors.append(f"Coin {coin_id}: 'v' must be an array")
            else:
                for j, variety in enumerate(coin['v']):
                    if not isinstance(variety, str):
                        self.errors.append(f"Coin {coin_id}: variety {j} must be a string")
        
        # Validate notes (optional string)
        if 'n' in coin:
            if not isinstance(coin['n'], str):
                self.errors.append(f"Coin {coin_id}: 'n' must be a string")
            elif len(coin['n']) > 200:  # Generous limit vs 100 char target
                self.warnings.append(f"Coin {coin_id}: 'n' is very long ({len(coin['n'])} chars)")
    
    def validate_completeness(self):
        """Validate that essential coin data is present."""
        print("🔍 Validating AI taxonomy completeness...")
        
        try:
            with open(self.taxonomy_file, 'r') as f:
                taxonomy = json.load(f)
        except:
            print("❌ Cannot validate completeness - file parsing failed")
            return False
        
        coins = taxonomy.get('coins', [])
        
        # Check for key series coverage
        type_codes = set()
        years = set()
        mints = set()
        key_dates = 0
        
        for coin in coins:
            if 't' in coin:
                type_codes.add(coin['t'])
            if 'y' in coin:
                years.add(coin['y'])
            if 'm' in coin:
                mints.add(coin['m'])
            if coin.get('r') == 'key':
                key_dates += 1
        
        print(f"📊 Coverage statistics:")
        print(f"   • {len(type_codes)} unique type codes")
        print(f"   • {len(years)} unique years ({min(years)} - {max(years)})")
        print(f"   • {len(mints)} unique mints")
        print(f"   • {key_dates} key dates identified")
        
        # Check for essential coverage
        if len(type_codes) < 10:
            self.warnings.append(f"Limited type code coverage: only {len(type_codes)} series")
        
        if max(years) - min(years) < 100:
            self.warnings.append(f"Limited year range: only {max(years) - min(years)} years")
        
        if key_dates == 0:
            self.warnings.append("No key dates identified")
        
        return True

def main():
    """Main validation function."""
    validator = AITaxonomyValidator()
    
    format_valid = validator.validate_format()
    completeness_valid = validator.validate_completeness()
    
    if format_valid and completeness_valid:
        print("\n✅ AI-optimized taxonomy validation completed successfully")
        return 0
    else:
        print("\n❌ AI-optimized taxonomy validation failed")
        return 1

if __name__ == "__main__":
    exit(main())