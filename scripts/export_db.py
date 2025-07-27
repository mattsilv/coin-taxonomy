#!/usr/bin/env python3
"""
Export database with series_metadata and composition_periods tables to JSON files.
This maintains the database as the source of truth while keeping JSON files for version control.
"""

import json
import sqlite3
import os
from collections import defaultdict

def export_to_json(db_path='database/coins.db', output_dir='data'):
    """Export database contents to JSON files"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement
    conn.row_factory = sqlite3.Row
    
    # Get all countries
    countries = conn.execute('SELECT DISTINCT country FROM coins ORDER BY country').fetchall()
    
    for country_row in countries:
        country = country_row['country'].lower()
        country_dir = f"{output_dir}/{country}/coins"
        os.makedirs(country_dir, exist_ok=True)
        
        # Get denominations for this country
        denominations = conn.execute('''
            SELECT DISTINCT denomination FROM coins 
            WHERE country = ? 
            ORDER BY denomination
        ''', (country_row['country'],)).fetchall()
        
        for denom_row in denominations:
            denomination = denom_row['denomination']
            
            # Build the JSON structure
            coin_data = {
                "country": country_row['country'],
                "denomination": denomination,
                "face_value": get_face_value(denomination),
                "series": []
            }
            
            # Get series for this denomination using the series_metadata table
            series_list = conn.execute('''
                SELECT DISTINCT sm.series_id, sm.series_name, sm.official_name,
                       sm.start_year, sm.end_year, sm.obverse_designer, sm.reverse_designer,
                       sm.diameter_mm, sm.thickness_mm, sm.edge_type
                FROM series_metadata sm
                JOIN coins c ON sm.series_id = c.series_id
                WHERE c.country = ? AND c.denomination = ?
                ORDER BY sm.start_year
            ''', (country_row['country'], denomination)).fetchall()
            
            for series_row in series_list:
                series_id = series_row['series_id']
                
                # Build series structure with metadata
                series_data = {
                    "series_id": series_id,
                    "series_name": series_row['series_name'],
                    "official_name": series_row['official_name'],
                    "years": {
                        "start": series_row['start_year'],
                        "end": series_row['end_year']
                    },
                    "specifications": {
                        "diameter_mm": series_row['diameter_mm'],
                        "thickness_mm": series_row['thickness_mm'],
                        "edge": series_row['edge_type']
                    },
                    "composition_periods": [],
                    "coins": [],
                    "designers": {
                        "obverse": series_row['obverse_designer'],
                        "reverse": series_row['reverse_designer']
                    }
                }
                
                # Get composition periods for this series
                comp_periods = conn.execute('''
                    SELECT start_year, end_year, alloy_name, alloy_composition, weight_grams
                    FROM composition_periods
                    WHERE series_id = ?
                    ORDER BY start_year
                ''', (series_id,)).fetchall()
                
                for period in comp_periods:
                    period_data = {
                        "date_range": {
                            "start": period['start_year'],
                            "end": period['end_year']
                        },
                        "alloy_name": period['alloy_name'],
                        "alloy": json.loads(period['alloy_composition']),
                        "weight": {
                            "grams": period['weight_grams']
                        }
                    }
                    series_data['composition_periods'].append(period_data)
                
                # Get coins for this series
                coins = conn.execute('''
                    SELECT coin_id, year, mint, business_strikes, proof_strikes, 
                           rarity, varieties, source_citation, notes
                    FROM coins 
                    WHERE country = ? AND denomination = ? AND series_id = ?
                    ORDER BY year, mint
                ''', (country_row['country'], denomination, series_id)).fetchall()
                
                for coin in coins:
                    coin_data_item = {
                        "coin_id": coin['coin_id'],
                        "year": coin['year'],
                        "mint": coin['mint'],
                        "business_strikes": coin['business_strikes'],
                        "proof_strikes": coin['proof_strikes']
                    }
                    
                    # Add optional fields
                    if coin['rarity']:
                        coin_data_item['rarity'] = coin['rarity']
                    if coin['source_citation']:
                        coin_data_item['source_citation'] = coin['source_citation']
                    if coin['notes']:
                        coin_data_item['notes'] = coin['notes']
                    if coin['varieties']:
                        try:
                            coin_data_item['varieties'] = json.loads(coin['varieties'])
                        except (json.JSONDecodeError, TypeError):
                            pass
                    
                    series_data['coins'].append(coin_data_item)
                
                coin_data['series'].append(series_data)
            
            # Write to file
            filename = denomination.lower().replace(' ', '_') + '.json'
            output_path = os.path.join(country_dir, filename)
            
            with open(output_path, 'w') as f:
                json.dump(coin_data, f, indent=2)
            
            print(f"Exported {denomination} to {output_path}")
    
    conn.close()

def get_face_value(denomination):
    """Get face value for denomination"""
    values = {
        'Cents': 0.01,
        'Nickels': 0.05,
        'Dimes': 0.10,
        'Quarters': 0.25,
        'Half Dollars': 0.50,
        'Dollars': 1.00
    }
    return values.get(denomination, 0.0)

def main():
    """Main export function"""
    print("Exporting database to JSON files...")
    
    # Check if we have the required tables
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    
    if 'series_metadata' not in table_names:
        print("Error: series_metadata table not found.")
        return
    
    if 'composition_periods' not in table_names:
        print("Error: composition_periods table not found.")
        return
    
    conn.close()
    
    export_to_json()
    print("✓ Database export completed successfully")

if __name__ == "__main__":
    main()