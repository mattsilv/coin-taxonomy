#!/usr/bin/env python3
"""
Export Canada coins from database to JSON files.
"""

import sqlite3
import json
import os
from pathlib import Path

def export_canada_coins():
    """Export Canada coins to JSON files and universal format."""
    
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    # Create output directories
    os.makedirs('data/ca/coins', exist_ok=True)
    os.makedirs('data/universal', exist_ok=True)
    os.makedirs('docs/data/universal', exist_ok=True)
    
    print("📊 Exporting Canada coins from database...")
    
    # Get all Canada coins
    cursor.execute('''
        SELECT 
            coin_id, series_id, denomination, series_name, year, mint,
            business_strikes, proof_strikes, rarity, composition,
            weight_grams, diameter_mm, varieties, source_citation, notes,
            obverse_description, reverse_description, distinguishing_features,
            identification_keywords, common_names
        FROM coins
        WHERE country = 'CA'
        ORDER BY denomination, year, mint
    ''')
    
    rows = cursor.fetchall()
    print(f"Found {len(rows)} Canada coins")
    
    # Group by denomination
    denominations = {}
    face_values = {
        'Cents': 0.01,
        'Five Cents': 0.05,
        'Ten Cents': 0.10,
        'Twenty Cents': 0.20,
        'Twenty-Five Cents': 0.25,
        'Fifty Cents': 0.50,
        'Dollars': 1.00,
        'Two Dollars': 2.00,
        'Five Dollars': 5.00,
        'Gold Maple Leaf': 50.00,
        'Silver Maple Leaf': 5.00,
        'Platinum Maple Leaf': 50.00,
        'Palladium Maple Leaf': 50.00,
        'Sovereign': 1.00
    }
    
    for row in rows:
        denom = row[2]  # denomination
        if denom not in denominations:
            denominations[denom] = []
        
        coin = {
            'coin_id': row[0],
            'series_id': row[1],
            'denomination': row[2],
            'series_name': row[3],
            'year': row[4],
            'mint': row[5],
            'business_strikes': row[6],
            'proof_strikes': row[7],
            'rarity': row[8],
            'composition': json.loads(row[9]) if row[9] else {},
            'weight_grams': row[10],
            'diameter_mm': row[11],
            'varieties': json.loads(row[12]) if row[12] else [],
            'source_citation': row[13],
            'notes': row[14],
            'obverse_description': row[15],
            'reverse_description': row[16],
            'distinguishing_features': row[17],
            'identification_keywords': row[18],
            'common_names': row[19]
        }
        
        # Remove None values
        coin = {k: v for k, v in coin.items() if v is not None}
        denominations[denom].append(coin)
    
    # Write denomination files
    for denom, coins in denominations.items():
        filename = f"ca_{denom.lower().replace(' ', '_')}.json"
        filepath = Path('data/ca/coins') / filename
        
        data = {
            'country': 'CA',
            'denomination': denom,
            'face_value': face_values.get(denom, 1.00),
            'coins': coins
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Written {filepath}")
    
    # Create complete file
    all_coins = []
    for coins in denominations.values():
        all_coins.extend(coins)
    
    complete_data = {
        'country': 'CA',
        'total_coins': len(all_coins),
        'denominations': list(denominations.keys()),
        'coins': all_coins
    }
    
    with open('data/ca/ca_coins_complete.json', 'w') as f:
        json.dump(complete_data, f, indent=2)
    print("✅ Written data/ca/ca_coins_complete.json")
    
    # Create universal format for frontend
    issues = []
    for coin in all_coins:
        issue = {
            'issueId': coin['coin_id'],
            'country': 'CA',
            'denomination': coin['denomination'],
            'year': coin['year'],
            'mint': coin['mint'],
            'seriesName': coin['series_name'],
            'rarity': coin.get('rarity', 'common'),
            'businessStrikes': coin.get('business_strikes'),
            'proofStrikes': coin.get('proof_strikes'),
            'composition': coin.get('composition', {}),
            'weightGrams': coin.get('weight_grams'),
            'diameterMm': coin.get('diameter_mm'),
            'varieties': coin.get('varieties', []),
            'obverseDescription': coin.get('obverse_description', ''),
            'reverseDescription': coin.get('reverse_description', ''),
            'commonNames': coin.get('common_names', '')
        }
        issues.append(issue)
    
    # Write universal format
    universal_data = {
        'country': 'CA',
        'countryName': 'Canada',
        'totalIssues': len(issues),
        'issues': issues
    }
    
    # Write to both locations for frontend access
    for path in ['data/universal/ca_issues.json', 'docs/data/universal/ca_issues.json']:
        with open(path, 'w') as f:
            json.dump(universal_data, f, indent=2)
        print(f"✅ Written {path}")
    
    # Update taxonomy summary to include Canada
    summary_path = 'data/universal/taxonomy_summary.json'
    if os.path.exists(summary_path):
        with open(summary_path, 'r') as f:
            summary = json.load(f)
    else:
        summary = {}
    
    # Update summary to include Canada
    if 'issue_files' not in summary:
        summary['issue_files'] = []
    
    if 'ca_issues.json' not in summary['issue_files']:
        summary['issue_files'].append('ca_issues.json')
    
    # Update country count
    summary['countries'] = len(summary.get('issue_files', []))
    
    # Write updated summary
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✅ Updated {summary_path}")
    
    # Copy to docs
    docs_summary = 'docs/data/universal/taxonomy_summary.json'
    if os.path.exists('docs/data/universal'):
        with open(docs_summary, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Updated {docs_summary}")
    
    conn.close()
    print(f"\n✅ Export complete: {len(all_coins)} Canada coins exported")

if __name__ == '__main__':
    export_canada_coins()