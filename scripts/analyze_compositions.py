#!/usr/bin/env python3
"""
Analyze composition usage across all coin files to design normalization.
"""

import json
import glob
from collections import defaultdict

def extract_compositions():
    """Extract all unique compositions from coin files"""
    compositions = {}
    composition_usage = defaultdict(list)
    
    coin_files = glob.glob('data/us/coins/*.json')
    
    for filepath in coin_files:
        with open(filepath) as f:
            data = json.load(f)
        
        denomination = data['denomination']
        
        for series in data['series']:
            series_name = series['series_name']
            
            for period in series.get('composition_periods', []):
                alloy_name = period['alloy_name']
                alloy_composition = period['alloy']
                weight = period['weight']['grams']
                
                # Create a consistent key for this composition
                alloy_key = json.dumps(alloy_composition, sort_keys=True)
                
                if alloy_key not in compositions:
                    compositions[alloy_key] = {
                        'name': alloy_name,
                        'composition': alloy_composition,
                        'weights': set(),
                        'periods': set(),
                        'usage': []
                    }
                
                compositions[alloy_key]['weights'].add(weight)
                compositions[alloy_key]['usage'].append(f"{denomination} - {series_name}")
                
                # Extract period info
                start = period['date_range']['start']
                end = period['date_range']['end'] 
                period_str = f"{start}-{end}"
                compositions[alloy_key]['periods'].add(period_str)
    
    return compositions

def propose_composition_keys():
    """Propose standardized keys for compositions"""
    compositions = extract_compositions()
    
    print("=== COMPOSITION ANALYSIS ===\n")
    
    proposed_keys = {}
    
    for i, (alloy_key, details) in enumerate(compositions.items()):
        # Convert sets to sorted lists for display
        details['weights'] = sorted(list(details['weights']))
        details['periods'] = sorted(list(details['periods']))
        
        print(f"Composition {i+1}:")
        print(f"  Name: {details['name']}")
        print(f"  Composition: {details['composition']}")
        print(f"  Weights used: {details['weights']} grams")
        print(f"  Periods: {details['periods']}")
        print(f"  Used in: {len(details['usage'])} series")
        for usage in sorted(set(details['usage'])):
            print(f"    - {usage}")
        
        # Propose a normalized key
        composition = details['composition']
        if 'silver' in composition and composition['silver'] == 0.9:
            key = 'silver_90'
        elif 'silver' in composition and composition['silver'] == 0.4:
            key = 'silver_40'
        elif 'silver' in composition and composition['silver'] == 0.35:
            key = 'silver_wartime'
        elif composition.get('copper') == 0.75 and composition.get('nickel') == 0.25:
            key = 'copper_nickel'
        elif composition.get('copper') == 0.88 and composition.get('nickel') == 0.12:
            key = 'copper_nickel_indian'
        elif composition.get('zinc') == 0.975 and composition.get('copper') == 0.025:
            key = 'zinc_copper_plated'
        elif composition.get('copper') == 0.95 and composition.get('zinc') == 0.05:
            key = 'brass_95_5'
        elif composition.get('copper') == 0.95 and composition.get('tin') == 0.04:
            key = 'bronze_95_4_1'
        elif composition.get('steel') == 0.99:
            key = 'steel_zinc_coated'
        elif 'copper_core' in composition:
            key = 'clad_cupronickel'
        elif 'manganese' in composition and len(composition) == 4:
            key = 'manganese_brass'
        else:
            # Fallback to first metal + percentage
            main_metal = max(composition.items(), key=lambda x: x[1])
            key = f"{main_metal[0]}_{int(main_metal[1]*100)}"
        
        proposed_keys[alloy_key] = key
        print(f"  Proposed key: {key}")
        print()
    
    return proposed_keys, compositions

if __name__ == "__main__":
    keys, comps = propose_composition_keys()
    
    print(f"\n=== SUMMARY ===")
    print(f"Found {len(comps)} unique compositions")
    print(f"Total composition usage instances: {sum(len(c['usage']) for c in comps.values())}")
    print("\nProposed normalization keys:")
    for alloy_key, proposed_key in keys.items():
        comp = comps[alloy_key]
        print(f"  {proposed_key}: {comp['name']} ({len(comp['usage'])} uses)")