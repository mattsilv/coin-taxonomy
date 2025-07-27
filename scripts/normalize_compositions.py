#!/usr/bin/env python3
"""
Normalize composition data by converting full composition details to references.
"""

import json
import glob
import os

def get_composition_mapping():
    """Create mapping from composition details to keys"""
    with open('data/us/references/compositions.json') as f:
        compositions = json.load(f)
    
    # Create mapping from composition to key
    comp_to_key = {}
    for key, details in compositions['common_alloys'].items():
        comp_str = json.dumps(details['composition'], sort_keys=True)
        comp_to_key[comp_str] = key
    
    return comp_to_key

def normalize_coin_file(filepath, comp_mapping):
    """Normalize a single coin file"""
    print(f"Normalizing {filepath}...")
    
    with open(filepath) as f:
        data = json.load(f)
    
    changes_made = 0
    
    for series in data['series']:
        for period in series.get('composition_periods', []):
            if 'alloy' in period and 'alloy_name' in period:
                # This is the old format - convert to key reference
                comp_str = json.dumps(period['alloy'], sort_keys=True)
                
                if comp_str in comp_mapping:
                    composition_key = comp_mapping[comp_str]
                    
                    # Replace full composition with key reference
                    del period['alloy']
                    del period['alloy_name'] 
                    period['composition_key'] = composition_key
                    changes_made += 1
                    
                    print(f"  Converted '{period.get('alloy_name', 'unknown')}' to key '{composition_key}'")
                else:
                    print(f"  WARNING: No key found for composition: {period.get('alloy_name')}")
    
    if changes_made > 0:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  ✓ Made {changes_made} changes to {filepath}")
    else:
        print(f"  No changes needed for {filepath}")
    
    return changes_made

def main():
    """Normalize all coin files"""
    print("Starting composition normalization...\n")
    
    # Get composition mapping
    comp_mapping = get_composition_mapping()
    print(f"Loaded {len(comp_mapping)} composition mappings\n")
    
    # Find all coin files
    coin_files = glob.glob('data/us/coins/*.json')
    
    total_changes = 0
    for filepath in coin_files:
        changes = normalize_coin_file(filepath, comp_mapping)
        total_changes += changes
        print()
    
    print(f"Normalization complete! Made {total_changes} total changes.")
    
    if total_changes > 0:
        print("\nRecommended next steps:")
        print("1. Run validation: uv run python scripts/validate.py")
        print("2. Test database export: uv run python scripts/export_db.py")
        print("3. Verify compositions resolve correctly")

if __name__ == "__main__":
    main()