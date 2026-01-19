#!/usr/bin/env python3
"""
Coin Entry Validation Module

Validates that coin entries include all required fields, including visual descriptions.
Used by migration scripts to ensure data completeness before database insertion.

Updated for Issue #113: Uses shared TaxonomyValidator for coin_id format validation.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Use the shared canonical validator (Issue #113)
from scripts.utils.taxonomy_validator import TaxonomyValidator

# Module-level validator instance
_taxonomy_validator = TaxonomyValidator()

class CoinEntryValidator:
    """Validates coin entry data for completeness and format."""
    
    REQUIRED_FIELDS = {
        'coin_id': str,
        'series_id': str, 
        'series_name': str,
        'year': int,
        'mint': str,
        'denomination': str,
        'country': str,
        # Visual description fields - NOW REQUIRED
        'obverse_description': str,
        'reverse_description': str,
        'distinguishing_features': list,
        'identification_keywords': list,
        'common_names': list
    }
    
    OPTIONAL_FIELDS = {
        'business_strikes': (int, type(None)),
        'proof_strikes': (int, type(None)),
        'rarity': (str, type(None)),
        'composition': (dict, str, type(None)),
        'weight_grams': (float, int, type(None)),
        'diameter_mm': (float, int, type(None)),
        'varieties': (list, str, type(None)),
        'source_citation': (str, type(None)),
        'notes': (str, type(None))
    }
    
    def validate_coin(self, coin_data: Dict) -> tuple[bool, List[str]]:
        """
        Validate a single coin entry.
        
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        for field, expected_type in self.REQUIRED_FIELDS.items():
            if field not in coin_data:
                errors.append(f"Missing required field: {field}")
                continue
                
            value = coin_data[field]
            if value is None or value == "":
                errors.append(f"Required field '{field}' cannot be empty")
                continue
                
            if not isinstance(value, expected_type):
                errors.append(f"Field '{field}' must be of type {expected_type.__name__}, got {type(value).__name__}")
        
        # Validate visual description fields specifically
        if 'obverse_description' in coin_data:
            if len(coin_data['obverse_description'].strip()) < 10:
                errors.append("obverse_description must be at least 10 characters")
                
        if 'reverse_description' in coin_data:
            if len(coin_data['reverse_description'].strip()) < 10:
                errors.append("reverse_description must be at least 10 characters")
                
        if 'distinguishing_features' in coin_data:
            features = coin_data['distinguishing_features']
            if isinstance(features, str):
                try:
                    features = json.loads(features)
                except json.JSONDecodeError:
                    errors.append("distinguishing_features must be valid JSON array")
            if isinstance(features, list) and len(features) == 0:
                errors.append("distinguishing_features cannot be empty array")
                
        if 'identification_keywords' in coin_data:
            keywords = coin_data['identification_keywords']
            if isinstance(keywords, str):
                try:
                    keywords = json.loads(keywords)
                except json.JSONDecodeError:
                    errors.append("identification_keywords must be valid JSON array")
            if isinstance(keywords, list) and len(keywords) == 0:
                errors.append("identification_keywords cannot be empty array")
                
        if 'common_names' in coin_data:
            names = coin_data['common_names']
            if isinstance(names, str):
                try:
                    names = json.loads(names)
                except json.JSONDecodeError:
                    errors.append("common_names must be valid JSON array")
            if isinstance(names, list) and len(names) == 0:
                errors.append("common_names cannot be empty array")
        
        # Validate coin_id format using shared TaxonomyValidator (Issue #113)
        if 'coin_id' in coin_data:
            coin_id = coin_data['coin_id']
            validation_errors, _ = _taxonomy_validator.validate_coin_id(coin_id)
            for ve in validation_errors:
                errors.append(f"{ve.field}: {ve.message} (got: {ve.value})")
        
        # Check optional fields types
        for field, expected_types in self.OPTIONAL_FIELDS.items():
            if field in coin_data:
                value = coin_data[field]
                if value is not None and not isinstance(value, expected_types):
                    type_names = [t.__name__ for t in expected_types if t is not type(None)]
                    errors.append(f"Field '{field}' must be one of types {type_names}, got {type(value).__name__}")
        
        return len(errors) == 0, errors
    
    def validate_batch(self, coins: List[Dict]) -> tuple[bool, Dict[str, List[str]]]:
        """
        Validate a batch of coins.
        
        Returns:
            tuple: (all_valid, dict_of_errors_by_coin_id)
        """
        all_errors = {}
        all_valid = True
        
        for coin in coins:
            coin_id = coin.get('coin_id', 'UNKNOWN')
            is_valid, errors = self.validate_coin(coin)
            
            if not is_valid:
                all_valid = False
                all_errors[coin_id] = errors
        
        return all_valid, all_errors
    
    def format_validation_report(self, errors_by_coin: Dict[str, List[str]]) -> str:
        """Format validation errors into a readable report."""
        if not errors_by_coin:
            return "✅ All coins passed validation"
        
        report = ["❌ VALIDATION ERRORS FOUND:\n"]
        
        for coin_id, errors in errors_by_coin.items():
            report.append(f"🪙 {coin_id}:")
            for error in errors:
                report.append(f"  - {error}")
            report.append("")
        
        return "\n".join(report)

def validate_coin_data(coin_data: Dict) -> tuple[bool, List[str]]:
    """Convenience function for validating a single coin."""
    validator = CoinEntryValidator()
    return validator.validate_coin(coin_data)

def validate_coin_batch(coins: List[Dict]) -> tuple[bool, Dict[str, List[str]]]:
    """Convenience function for validating multiple coins."""
    validator = CoinEntryValidator()
    return validator.validate_batch(coins)

if __name__ == "__main__":
    # Test the validator
    test_coin = {
        "coin_id": "US-TEST-2024-P",
        "series_id": "test_series",
        "series_name": "Test Series", 
        "year": 2024,
        "mint": "P",
        "denomination": "Test",
        "country": "US",
        "obverse_description": "Test obverse description with sufficient length",
        "reverse_description": "Test reverse description with sufficient length",
        "distinguishing_features": ["Feature 1", "Feature 2"],
        "identification_keywords": ["test", "coin", "example"],
        "common_names": ["Test Coin"]
    }
    
    is_valid, errors = validate_coin_data(test_coin)
    print(f"Test validation: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    if errors:
        for error in errors:
            print(f"  - {error}")