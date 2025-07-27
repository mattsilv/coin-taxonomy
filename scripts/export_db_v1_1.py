#!/usr/bin/env python3
"""
Universal Currency Taxonomy Export Script v1.1
Exports both legacy and universal taxonomy structures.

This script supports:
1. Legacy nested structure (for backward compatibility)
2. New universal flat structure (issues + registries)
3. Banknote support (when available)
"""

import json
import sqlite3
import os
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path


def safe_json_loads(data, default=None):
    """Safely parse JSON data, returning default on error."""
    if not data:
        return default
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default




def check_universal_tables(conn):
    """Check if universal taxonomy tables exist."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    
    universal_tables = {'issues', 'subject_registry', 'composition_registry', 'series_registry'}
    return universal_tables.issubset(tables)


def export_legacy_format(conn, output_dir='data'):
    """Export in legacy nested format for backward compatibility."""
    print("Exporting legacy format...")
    
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
            
            # Get series for this denomination
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
            
            print(f"✓ Exported {denomination} to {output_path}")


def export_universal_format(conn, output_dir='data'):
    """Export new universal flat format."""
    print("Exporting universal format...")
    
    # Create universal output directory
    universal_dir = f"{output_dir}/universal"
    os.makedirs(universal_dir, exist_ok=True)
    
    # Export registries
    export_registries(conn, universal_dir)
    
    # Export issues by country
    export_issues_by_country(conn, universal_dir)
    
    # Export complete dataset
    export_complete_universal_dataset(conn, universal_dir)


def export_registries(conn, output_dir):
    """Export registry tables."""
    cursor = conn.cursor()
    
    # Subject Registry
    cursor.execute('SELECT * FROM subject_registry ORDER BY subject_id')
    subjects = []
    for row in cursor.fetchall():
        subject = {
            'subject_id': row[0],
            'type': row[1],
            'name': row[2],
            'nationality': row[3],
            'roles': safe_json_loads(row[4], []),
            'life_dates': safe_json_loads(row[5], {}),
            'reign_dates': safe_json_loads(row[6], {}),
            'significance': row[7],
            'symbolism': safe_json_loads(row[8], []),
            'scientific_name': row[9],
            'first_coin_appearance': row[10],
            'metadata': safe_json_loads(row[11], {})
        }
        # Remove null values
        subjects.append({k: v for k, v in subject.items() if v is not None})
    
    with open(f"{output_dir}/subject_registry.json", 'w') as f:
        json.dump({"subjects": subjects}, f, indent=2)
    print(f"✓ Exported {len(subjects)} subjects")
    
    # Composition Registry
    cursor.execute('SELECT * FROM composition_registry ORDER BY composition_key')
    compositions = []
    for row in cursor.fetchall():
        comp = {
            'composition_key': row[0],
            'name': row[1],
            'alloy_composition': safe_json_loads(row[2], {}),
            'period_description': row[3],
            'density_g_cm3': row[4],
            'magnetic_properties': row[5],
            'color_description': row[6]
        }
        # Remove null values
        compositions.append({k: v for k, v in comp.items() if v is not None})
    
    with open(f"{output_dir}/composition_registry.json", 'w') as f:
        json.dump({"compositions": compositions}, f, indent=2)
    print(f"✓ Exported {len(compositions)} compositions")
    
    # Series Registry
    cursor.execute('SELECT * FROM series_registry ORDER BY country_code, start_year')
    series_list = []
    for row in cursor.fetchall():
        series = {
            'series_id': row[0],
            'series_name': row[1],
            'country_code': row[2],
            'denomination': row[3],
            'start_year': row[4],
            'end_year': row[5],
            'defining_characteristics': row[6],
            'official_name': row[7],
            'type': row[8]
        }
        # Remove null values
        series_list.append({k: v for k, v in series.items() if v is not None})
    
    with open(f"{output_dir}/series_registry.json", 'w') as f:
        json.dump({"series": series_list}, f, indent=2)
    print(f"✓ Exported {len(series_list)} series")


def export_issues_by_country(conn, output_dir):
    """Export issues grouped by country."""
    cursor = conn.cursor()
    
    # Get countries
    cursor.execute('SELECT DISTINCT country_code FROM issues ORDER BY country_code')
    countries = [row[0] for row in cursor.fetchall()]
    
    for country in countries:
        cursor.execute('''
            SELECT * FROM issues 
            WHERE country_code = ? 
            ORDER BY issue_year, face_value, mint_id
        ''', (country,))
        
        issues = []
        for row in cursor.fetchall():
            issue = {
                'issue_id': row[0],
                'object_type': row[1],
                'series_id': row[2],
                'issuing_entity': {
                    'country_code': row[3],
                    'authority_name': row[4],
                    'monetary_system': row[5],
                    'currency_unit': row[6]
                },
                'denomination': {
                    'face_value': row[7],
                    'unit_name': row[8],
                    'common_names': safe_json_loads(row[9], []),
                    'system_fraction': row[10]
                },
                'issue_year': row[11],
                'mint_id': row[12],
                'specifications': safe_json_loads(row[15], {}),
                'sides': safe_json_loads(row[16], {}),
                'mintage': safe_json_loads(row[17], {}),
                'rarity': row[18],
                'varieties': safe_json_loads(row[19], [])
            }
            
            # Add optional fields
            if row[13]:  # date_range_start
                issue['date_range_start'] = row[13]
            if row[14]:  # date_range_end
                issue['date_range_end'] = row[14]
            if row[20]:  # source_citation
                issue['source_citation'] = row[20]
            if row[21]:  # notes
                issue['notes'] = row[21]
            
            issues.append(issue)
        
        country_data = {
            'country_code': country,
            'total_issues': len(issues),
            'issues': issues
        }
        
        with open(f"{output_dir}/{country.lower()}_issues.json", 'w') as f:
            json.dump(country_data, f, indent=2)
        print(f"✓ Exported {len(issues)} {country} issues")


def export_complete_universal_dataset(conn, output_dir):
    """Export complete universal dataset."""
    cursor = conn.cursor()
    
    # Get summary statistics
    cursor.execute('SELECT COUNT(*) FROM issues')
    total_issues = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT country_code) FROM issues')
    total_countries = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT object_type) FROM issues')
    total_types = cursor.fetchone()[0]
    
    cursor.execute('SELECT MIN(issue_year), MAX(issue_year) FROM issues')
    year_range = cursor.fetchone()
    
    # Build summary
    summary = {
        'taxonomy_version': '1.1',
        'format': 'universal_flat_structure',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total_issues': total_issues,
        'countries': total_countries,
        'object_types': total_types,
        'year_range': {
            'earliest': year_range[0],
            'latest': year_range[1]
        },
        'registries': {
            'subjects': 'subject_registry.json',
            'compositions': 'composition_registry.json', 
            'series': 'series_registry.json'
        },
        'issue_files': []
    }
    
    # Add issue file references
    cursor.execute('SELECT DISTINCT country_code FROM issues ORDER BY country_code')
    for row in cursor.fetchall():
        country = row[0]
        summary['issue_files'].append(f"{country.lower()}_issues.json")
    
    with open(f"{output_dir}/taxonomy_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Exported universal taxonomy summary")


def get_face_value(denomination):
    """Get face value for denomination."""
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
    """Main export function."""
    print("Universal Currency Taxonomy Export v1.1")
    print("=" * 50)
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement
    
    # Check available table structures
    has_universal = check_universal_tables(conn)
    has_legacy = check_legacy_tables(conn)
    
    print(f"Universal tables available: {has_universal}")
    print(f"Legacy tables available: {has_legacy}")
    print()
    
    if has_universal:
        export_universal_format(conn)
    
    if has_legacy:
        export_legacy_format(conn)
    
    if not has_universal and not has_legacy:
        print("Error: No compatible table structure found.")
        return
    
    conn.close()
    print("\n✓ Export completed successfully")


def check_legacy_tables(conn):
    """Check if legacy tables exist."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    
    legacy_tables = {'coins', 'series_metadata', 'composition_periods'}
    return legacy_tables.issubset(tables)


if __name__ == "__main__":
    main()