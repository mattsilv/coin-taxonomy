#!/usr/bin/env python3
"""
Export complete US coin taxonomy to a single comprehensive JSON file.
Combines all individual denomination files into one unified structure.
"""

import json
import glob
import os
from datetime import datetime

def load_composition_data():
    """Load and resolve composition references"""
    with open('data/us/references/compositions.json') as f:
        compositions_data = json.load(f)
    return compositions_data['common_alloys']

def resolve_composition(period, compositions):
    """Resolve composition_key to full composition details"""
    if 'composition_key' in period:
        key = period['composition_key']
        if key in compositions:
            return {
                "date_range": period['date_range'],
                "alloy_name": compositions[key]['name'],
                "alloy": compositions[key]['composition'],
                "weight": period['weight']
            }
    # Return as-is if already has full composition or no key
    return period

def export_complete_us_taxonomy(output_file='data/us/us_coins_complete.json'):
    """Export complete US coin taxonomy to a single JSON file"""
    
    # Load composition data for reference resolution
    compositions = load_composition_data()
    
    # Build complete taxonomy structure
    complete_taxonomy = {
        "metadata": {
            "title": "United States Coin Taxonomy Database - Complete Edition",
            "description": "Comprehensive database of US coin series, mintages, varieties, and key dates",
            "version": "1.0",
            "generated": datetime.now().isoformat(),
            "source": "Compiled from PCGS CoinFacts, NGC, Red Book, US Mint records",
            "note": "This file combines all individual denomination files for convenience"
        },
        "country": "US",
        "denominations": {},
        "references": {}
    }
    
    # Load all coin denomination files
    coin_files = glob.glob('data/us/coins/*.json')
    
    total_series = 0
    total_coins = 0
    
    for filepath in sorted(coin_files):
        print(f"Processing {filepath}...")
        
        with open(filepath) as f:
            data = json.load(f)
        
        denomination = data['denomination']
        
        # Process each series in the denomination
        processed_series = []
        for series in data['series']:
            # Resolve composition references to full details
            resolved_periods = []
            for period in series.get('composition_periods', []):
                resolved_period = resolve_composition(period, compositions)
                resolved_periods.append(resolved_period)
            
            # Update series with resolved compositions
            series_copy = series.copy()
            series_copy['composition_periods'] = resolved_periods
            processed_series.append(series_copy)
            
            total_series += 1
            total_coins += len(series.get('coins', []))
        
        # Add denomination data
        complete_taxonomy['denominations'][denomination] = {
            "face_value": data['face_value'],
            "series": processed_series
        }
    
    # Load reference data
    reference_files = {
        'compositions': 'data/us/references/compositions.json',
        'mints': 'data/us/references/mints.json', 
        'grades': 'data/us/references/grades.json'
    }
    
    for ref_name, ref_path in reference_files.items():
        if os.path.exists(ref_path):
            with open(ref_path) as f:
                complete_taxonomy['references'][ref_name] = json.load(f)
    
    # Add statistics
    complete_taxonomy['statistics'] = {
        "denominations": len(complete_taxonomy['denominations']),
        "total_series": total_series,
        "total_coins": total_coins,
        "generation_date": datetime.now().isoformat(),
        "file_sources": [os.path.basename(f) for f in sorted(coin_files)]
    }
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write to file
    with open(output_file, 'w') as f:
        json.dump(complete_taxonomy, f, indent=2)
    
    # Calculate file size
    file_size_kb = os.path.getsize(output_file) / 1024
    
    print(f"\n✓ Complete US taxonomy exported to {output_file}")
    print(f"📊 Statistics:")
    print(f"  - {len(complete_taxonomy['denominations'])} denominations")
    print(f"  - {total_series} series")
    print(f"  - {total_coins} individual coins")
    print(f"  - File size: {file_size_kb:.1f} KB")
    print(f"  - Compositions resolved: {len(compositions)} reference keys")
    
    return output_file

def main():
    """Main export function"""
    print("🪙 Generating complete US coin taxonomy file...")
    
    # Check if source files exist
    coin_files = glob.glob('data/us/coins/*.json')
    if not coin_files:
        print("❌ No coin data files found in data/us/coins/")
        return
    
    print(f"📁 Found {len(coin_files)} denomination files")
    
    # Export the complete taxonomy
    output_file = export_complete_us_taxonomy()
    
    print(f"\n🎉 Complete! File available at: {output_file}")

if __name__ == "__main__":
    main()