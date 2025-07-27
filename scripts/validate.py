#!/usr/bin/env python3
"""
Validates all JSON files against their schemas.
Works for any country's data files.
"""

import json
import glob
from jsonschema import validate, ValidationError
import os
import sys

def validate_country_data(country_code):
    """Validate all data files for a specific country"""
    coin_schema_path = f'data/{country_code}/schema/coin.schema.json'
    
    if not os.path.exists(coin_schema_path):
        print(f"No coin schema found for country: {country_code}")
        return 0
    
    errors = 0
    
    # Validate coin files
    with open(coin_schema_path) as f:
        coin_schema = json.load(f)
    
    coin_files = glob.glob(f'data/{country_code}/coins/*.json')
    
    for filepath in coin_files:
        try:
            with open(filepath) as f:
                data = json.load(f)
            validate(data, coin_schema)
            print(f"✓ {filepath}")
        except json.JSONDecodeError as e:
            print(f"✗ {filepath}: Invalid JSON - {e}")
            errors += 1
        except ValidationError as e:
            print(f"✗ {filepath}: Validation failed - {e.message}")
            errors += 1
    
    # Validate reference files
    reference_schemas = {
        'compositions.json': 'compositions.schema.json',
        'mints.json': 'mints.schema.json', 
        'grades.json': 'grades.schema.json'
    }
    
    for ref_file, schema_file in reference_schemas.items():
        ref_path = f'data/{country_code}/references/{ref_file}'
        schema_path = f'data/{country_code}/schema/{schema_file}'
        
        if os.path.exists(ref_path) and os.path.exists(schema_path):
            try:
                with open(schema_path) as f:
                    schema = json.load(f)
                with open(ref_path) as f:
                    data = json.load(f)
                validate(data, schema)
                print(f"✓ {ref_path}")
            except json.JSONDecodeError as e:
                print(f"✗ {ref_path}: Invalid JSON - {e}")
                errors += 1
            except ValidationError as e:
                print(f"✗ {ref_path}: Validation failed - {e.message}")
                errors += 1
    
    return errors

def main():
    # Find all country directories
    countries = [d for d in os.listdir('data') 
                 if os.path.isdir(f'data/{d}') and len(d) == 2]
    
    total_errors = 0
    for country in countries:
        print(f"\nValidating {country.upper()} data...")
        total_errors += validate_country_data(country)
    
    if total_errors:
        print(f"\n{total_errors} validation error(s) found")
        sys.exit(1)
    else:
        print("\n✓ All files valid")

if __name__ == "__main__":
    main()