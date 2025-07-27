#!/usr/bin/env python3
"""
Export complete coin taxonomy to a single comprehensive JSON file.
"""

import json
import sqlite3
import os
from datetime import datetime

def export_complete_taxonomy(db_path='database/coins.db', output_file='coin_taxonomy_complete.json'):
    """Export entire database to a single comprehensive JSON file"""
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Build complete taxonomy structure
    taxonomy = {
        "metadata": {
            "title": "United States Coin Taxonomy Database",
            "description": "Comprehensive database of US coin series, mintages, varieties, and key dates",
            "version": "1.0",
            "generated": datetime.now().isoformat(),
            "source": "Compiled from PCGS CoinFacts, NGC, Red Book, US Mint records"
        },
        "countries": {}
    }
    
    # Get all countries
    countries = conn.execute('SELECT DISTINCT country FROM coins ORDER BY country').fetchall()
    
    for country_row in countries:
        country_code = country_row['country']
        country_name = get_country_name(country_code)
        
        taxonomy['countries'][country_code] = {
            "name": country_name,
            "denominations": {}
        }
        
        # Get denominations for this country
        denominations = conn.execute('''
            SELECT DISTINCT denomination FROM coins 
            WHERE country = ? 
            ORDER BY denomination
        ''', (country_code,)).fetchall()
        
        for denom_row in denominations:
            denomination = denom_row['denomination']
            
            denom_data = {
                "face_value": get_face_value(denomination),
                "series": {}
            }
            
            # Get series for this denomination
            series_list = conn.execute('''
                SELECT series_id, series_name, MIN(year) as min_year FROM coins 
                WHERE country = ? AND denomination = ?
                GROUP BY series_id, series_name
                ORDER BY min_year
            ''', (country_code, denomination)).fetchall()
            
            for series_row in series_list:
                series_id = series_row[0]
                series_name = series_row[1]
                
                # Get complete series data
                series_data = build_complete_series_data(conn, country_code, denomination, series_id, series_name)
                denom_data['series'][series_id] = series_data
            
            taxonomy['countries'][country_code]['denominations'][denomination] = denom_data
    
    # Add summary statistics
    stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT country) as countries,
            COUNT(DISTINCT denomination) as denominations,
            COUNT(DISTINCT series_id) as series,
            COUNT(*) as total_coins,
            MIN(year) as earliest_year,
            MAX(year) as latest_year,
            COUNT(CASE WHEN rarity = 'key' THEN 1 END) as key_dates,
            COUNT(CASE WHEN varieties IS NOT NULL THEN 1 END) as varieties
        FROM coins
    ''').fetchone()
    
    taxonomy['statistics'] = {
        "countries": stats['countries'],
        "denominations": stats['denominations'],
        "series": stats['series'],
        "total_coins": stats['total_coins'],
        "year_range": f"{stats['earliest_year']}-{stats['latest_year']}",
        "key_dates": stats['key_dates'],
        "varieties": stats['varieties']
    }
    
    # Write to file
    with open(output_file, 'w') as f:
        json.dump(taxonomy, f, indent=2)
    
    conn.close()
    
    print(f"Complete taxonomy exported to {output_file}")
    print(f"Statistics: {stats['total_coins']} coins across {stats['series']} series")
    print(f"Key dates: {stats['key_dates']}, Varieties: {stats['varieties']}")
    
    return output_file

def get_country_name(country_code):
    """Get full country name from code"""
    names = {
        'US': 'United States',
        'CA': 'Canada',
        'UK': 'United Kingdom',
        'MX': 'Mexico'
    }
    return names.get(country_code, country_code)

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

def build_complete_series_data(conn, country, denomination, series_id, series_name):
    """Build complete series data from database"""
    
    # Get series overview
    overview = conn.execute('''
        SELECT 
            MIN(year) as start_year, 
            MAX(year) as end_year,
            COUNT(DISTINCT year) as years_minted,
            COUNT(DISTINCT mint) as mints_used,
            SUM(business_strikes) as total_mintage,
            SUM(proof_strikes) as total_proof_mintage,
            MIN(diameter_mm) as diameter,
            COUNT(CASE WHEN rarity = 'key' THEN 1 END) as key_dates,
            COUNT(CASE WHEN rarity = 'semi-key' THEN 1 END) as semi_key_dates,
            COUNT(CASE WHEN varieties IS NOT NULL THEN 1 END) as varieties
        FROM coins 
        WHERE country = ? AND denomination = ? AND series_id = ?
    ''', (country, denomination, series_id)).fetchone()
    
    series_data = {
        "overview": {
            "years": {
                "start": overview['start_year'],
                "end": overview['end_year'] if overview['end_year'] != overview['start_year'] else "present",
                "years_minted": overview['years_minted']
            },
            "mints_used": overview['mints_used'],
            "total_business_strikes": overview['total_mintage'] or 0,
            "total_proof_strikes": overview['total_proof_mintage'] or 0,
            "key_dates": overview['key_dates'],
            "semi_key_dates": overview['semi_key_dates'],
            "varieties": overview['varieties']
        },
        "specifications": {},
        "composition_periods": [],
        "coins": {}
    }
    
    # Add specifications
    if overview['diameter']:
        series_data['specifications'] = {
            "diameter_mm": overview['diameter'],
            "edge": "reeded"  # Default assumption for most US coins
        }
    
    # Get composition periods
    comp_periods = conn.execute('''
        SELECT DISTINCT composition, weight_grams, MIN(year) as start, MAX(year) as end
        FROM coins 
        WHERE country = ? AND denomination = ? AND series = ? AND composition IS NOT NULL
        GROUP BY composition, weight_grams
        ORDER BY start
    ''', (country, denomination, series_name)).fetchall()
    
    for period in comp_periods:
        try:
            comp = json.loads(period['composition'])
            period_data = {
                "date_range": {
                    "start": period['start'],
                    "end": period['end'] if period['end'] != period['start'] else "present"
                },
                "alloy": comp,
                "weight": {
                    "grams": period['weight_grams']
                }
            }
            series_data['composition_periods'].append(period_data)
        except (json.JSONDecodeError, TypeError):
            continue
    
    # Get all coins in series
    coins = conn.execute('''
        SELECT year, mint, mintage, proof_mintage, key_date_status, 
               varieties, source_citation, notes
        FROM coins 
        WHERE country = ? AND denomination = ? AND series = ?
        ORDER BY year, mint
    ''', (country, denomination, series_name)).fetchall()
    
    for coin in coins:
        coin_key = f"{coin['year']}-{coin['mint']}"
        
        coin_data = {
            "year": coin['year'],
            "mint": coin['mint'],
            "mintage": coin['mintage'],
            "proof_mintage": coin['proof_mintage']
        }
        
        # Add optional fields
        if coin['key_date_status']:
            coin_data['rarity'] = coin['key_date_status']
        if coin['varieties']:
            try:
                coin_data['varieties'] = json.loads(coin['varieties'])
            except json.JSONDecodeError:
                pass
        if coin['source_citation']:
            coin_data['source'] = coin['source_citation']
        if coin['notes']:
            coin_data['notes'] = coin['notes']
        
        series_data['coins'][coin_key] = coin_data
    
    return series_data

def main():
    print("Generating complete coin taxonomy file...")
    
    # First ensure we have a database
    if not os.path.exists('database/coins.db'):
        print("Database not found. Building database first...")
        import subprocess
        subprocess.run(['python', 'scripts/build_db.py'])
    
    output_file = export_complete_taxonomy()
    
    # Show file size and basic stats
    file_size = os.path.getsize(output_file) / 1024  # KB
    print(f"File size: {file_size:.1f} KB")

if __name__ == "__main__":
    main()