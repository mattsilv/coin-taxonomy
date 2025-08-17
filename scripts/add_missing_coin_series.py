#!/usr/bin/env python3
"""
Add missing US coin series to the coin taxonomy database.
This script adds major missing series identified from the analysis.
"""

import sqlite3
import json
from datetime import datetime

def add_barber_half_dollars(cursor):
    """Add Barber Half Dollar series (1892-1915)"""
    print("Adding Barber Half Dollar series...")
    
    current_time = datetime.now().isoformat()
    
    # Barber Half Dollar series (1892-1915)
    # Key representative years and varieties
    barber_half_dollars = [
        # First year 1892 - all mints
        {
            'coin_id': 'US-BARH-1892-P',
            'series': 'Barber Half Dollar',
            'denomination': 'Half Dollar', 
            'year': 1892,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head right wearing Phrygian cap with LIBERTY on headband',
            'reverse_design': 'Heraldic eagle with shield, arrows and olive branch',
            'designer': 'Charles E. Barber',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'First year of issue. Mint mark on reverse below eagle tail feathers.',
            'identification_keywords': 'barber half dollar 1892 philadelphia',
            'common_names': 'Barber Half',
            'rarity': 'common',
            'notes': 'First year of series, moderately scarce. Common in lower grades, scarce in AU+.',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'coin_id': 'US-BARH-1892-O',
            'series': 'Barber Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1892,
            'mint_mark': 'O',
            'country': 'United States',
            'obverse_design': 'Liberty head right wearing Phrygian cap with LIBERTY on headband',
            'reverse_design': 'Heraldic eagle with shield, arrows and olive branch',
            'designer': 'Charles E. Barber',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Normal O mint mark on reverse below eagle tail feathers.',
            'identification_keywords': 'barber half dollar 1892 new orleans key date',
            'common_names': 'Barber Half',
            'rarity': 'key',
            'notes': 'Key date of series, very scarce in all grades. Scarce in all grades, rare in XF+.',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'coin_id': 'US-BARH-1892-S',
            'series': 'Barber Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1892,
            'mint_mark': 'S',
            'country': 'United States',
            'obverse_design': 'Liberty head right wearing Phrygian cap with LIBERTY on headband',
            'reverse_design': 'Heraldic eagle with shield, arrows and olive branch',
            'designer': 'Charles E. Barber',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Mint mark on reverse below eagle tail feathers.',
            'identification_keywords': 'barber half dollar 1892 san francisco key date',
            'common_names': 'Barber Half',
            'rarity': 'key',
            'notes': 'Key date of series, very scarce in all grades. Scarce in all grades, rare in XF+.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1893-S - another key date
        {
            'coin_id': 'US-BARH-1893-S',
            'series': 'Barber Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1893,
            'mint_mark': 'S',
            'country': 'United States',
            'obverse_design': 'Liberty head right wearing Phrygian cap with LIBERTY on headband',
            'reverse_design': 'Heraldic eagle with shield, arrows and olive branch',
            'designer': 'Charles E. Barber',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Mint mark on reverse below eagle tail feathers.',
            'identification_keywords': 'barber half dollar 1893 san francisco key date',
            'common_names': 'Barber Half',
            'rarity': 'key',
            'notes': 'Key date of series, very scarce in all grades. Scarce in all grades, extremely rare in AU+.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1896-O - key date
        {
            'coin_id': 'US-BARH-1896-O',
            'series': 'Barber Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1896,
            'mint_mark': 'O',
            'country': 'United States',
            'obverse_design': 'Liberty head right wearing Phrygian cap with LIBERTY on headband',
            'reverse_design': 'Heraldic eagle with shield, arrows and olive branch',
            'designer': 'Charles E. Barber',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Mint mark on reverse below eagle tail feathers.',
            'identification_keywords': 'barber half dollar 1896 new orleans key date',
            'common_names': 'Barber Half',
            'rarity': 'key',
            'notes': 'Key date of series, very scarce in all grades. Scarce in all grades, rare in XF+.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1913 - key date from late period
        {
            'coin_id': 'US-BARH-1913-P',
            'series': 'Barber Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1913,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head right wearing Phrygian cap with LIBERTY on headband',
            'reverse_design': 'Heraldic eagle with shield, arrows and olive branch',
            'designer': 'Charles E. Barber',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date from late period. Low mintage.',
            'identification_keywords': 'barber half dollar 1913 philadelphia key date',
            'common_names': 'Barber Half',
            'rarity': 'key',
            'notes': 'Key date from late period, low mintage of 188,627. Scarce in all grades due to low mintage.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1915 - final year
        {
            'coin_id': 'US-BARH-1915-P',
            'series': 'Barber Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1915,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head right wearing Phrygian cap with LIBERTY on headband',
            'reverse_design': 'Heraldic eagle with shield, arrows and olive branch',
            'designer': 'Charles E. Barber',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Final year of Barber Half Dollar series.',
            'identification_keywords': 'barber half dollar 1915 philadelphia final year',
            'common_names': 'Barber Half',
            'rarity': 'key',
            'notes': 'Key date - final year of series. Popular as final year type, scarce in high grades.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Common date example - 1906
        {
            'coin_id': 'US-BARH-1906-P',
            'series': 'Barber Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1906,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head right wearing Phrygian cap with LIBERTY on headband',
            'reverse_design': 'Heraldic eagle with shield, arrows and olive branch',
            'designer': 'Charles E. Barber',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Representative common date from middle period.',
            'identification_keywords': 'barber half dollar 1906 philadelphia common date',
            'common_names': 'Barber Half',
            'rarity': 'common',
            'notes': 'Common date, readily available in lower grades. Common in G-VF, scarce in AU+.',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    for coin in barber_half_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series_id, series_name, country, denomination, year, mint,
                obverse_description, reverse_description, composition,
                weight_grams, diameter_mm, distinguishing_features, 
                identification_keywords, common_names, rarity, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['coin_id'][:7], coin['series'], coin['country'], 
            coin['denomination'], coin['year'], coin['mint_mark'], 
            coin['obverse_design'], coin['reverse_design'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'], coin['rarity'],
            coin['notes'], coin['created_at']
        ))

def add_walking_liberty_half_dollars(cursor):
    """Add Walking Liberty Half Dollar series (1916-1947)"""
    print("Adding Walking Liberty Half Dollar series...")
    
    current_time = datetime.now().isoformat()
    
    # Walking Liberty Half Dollar series (1916-1947)
    # Key dates and representative years
    walking_liberty_half_dollars = [
        # 1916 - first year and key date
        {
            'coin_id': 'US-WLHD-1916-P',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1916,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'First year. Mint mark on obverse below "IN GOD WE TRUST".',
            'identification_keywords': 'walking liberty half dollar 1916 first year key date',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'key',
            'notes': 'Key date - first year of series. Mint mark location on obverse. Very popular design.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1916-D
        {
            'coin_id': 'US-WLHD-1916-D',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1916,
            'mint_mark': 'D',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'First year. Mint mark on obverse below "IN GOD WE TRUST".',
            'identification_keywords': 'walking liberty half dollar 1916 denver first year',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'scarce',
            'notes': 'First year issue from Denver. Mint mark on obverse. Scarcer than Philadelphia.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1916-S
        {
            'coin_id': 'US-WLHD-1916-S',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1916,
            'mint_mark': 'S',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'First year. Mint mark on obverse below "IN GOD WE TRUST".',
            'identification_keywords': 'walking liberty half dollar 1916 san francisco first year',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'scarce',
            'notes': 'First year issue from San Francisco. Mint mark on obverse. Lower mintage.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1917-P - transition year for mint mark location
        {
            'coin_id': 'US-WLHD-1917-P',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1917,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Transition year. Early 1917 mint mark on obverse, later on reverse.',
            'identification_keywords': 'walking liberty half dollar 1917 philadelphia transition',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'common',
            'notes': 'Transition year for mint mark location. Mid-1917 change from obverse to reverse.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1921-P - key date
        {
            'coin_id': 'US-WLHD-1921-P',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1921,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Mint mark on reverse below olive branch.',
            'identification_keywords': 'walking liberty half dollar 1921 philadelphia key date',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'key',
            'notes': 'Key date of series. Low mintage and heavy melting during silver run-up.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1921-D - key date
        {
            'coin_id': 'US-WLHD-1921-D',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1921,
            'mint_mark': 'D',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Mint mark on reverse below olive branch.',
            'identification_keywords': 'walking liberty half dollar 1921 denver key date',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'key',
            'notes': 'Key date of series. Very low mintage, extremely scarce in high grades.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1921-S - key date
        {
            'coin_id': 'US-WLHD-1921-S',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1921,
            'mint_mark': 'S',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Mint mark on reverse below olive branch.',
            'identification_keywords': 'walking liberty half dollar 1921 san francisco key date',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'key',
            'notes': 'Key date of series. Very low mintage, extremely scarce and valuable.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1938-D - key date
        {
            'coin_id': 'US-WLHD-1938-D',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1938,
            'mint_mark': 'D',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date from late period. Mint mark on reverse below olive branch.',
            'identification_keywords': 'walking liberty half dollar 1938 denver key date',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'key',
            'notes': 'Key date from later period. Low mintage of 491,600.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1947 - final year
        {
            'coin_id': 'US-WLHD-1947-P',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1947,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Final year of series. Mint mark on reverse below olive branch.',
            'identification_keywords': 'walking liberty half dollar 1947 philadelphia final year',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'common',
            'notes': 'Final year of beloved series. Design later used on American Silver Eagle.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Common date example - 1943
        {
            'coin_id': 'US-WLHD-1943-P',
            'series': 'Walking Liberty Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1943,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty walking left draped in American flag with rising sun behind',
            'reverse_design': 'Eagle perched on mountain crag with wings partially spread',
            'designer': 'Adolph A. Weinman',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Wartime issue. Mint mark on reverse below olive branch.',
            'identification_keywords': 'walking liberty half dollar 1943 philadelphia common wartime',
            'common_names': 'Walking Liberty Half, Walker',
            'rarity': 'common',
            'notes': 'Representative common date from wartime period. High mintage.',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    for coin in walking_liberty_half_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series_id, series_name, country, denomination, year, mint,
                obverse_description, reverse_description, composition,
                weight_grams, diameter_mm, distinguishing_features, 
                identification_keywords, common_names, rarity, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['coin_id'][:7], coin['series'], coin['country'], 
            coin['denomination'], coin['year'], coin['mint_mark'], 
            coin['obverse_design'], coin['reverse_design'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'], coin['rarity'],
            coin['notes'], coin['created_at']
        ))

def add_franklin_half_dollars(cursor):
    """Add Franklin Half Dollar series (1948-1963)"""
    print("Adding Franklin Half Dollar series...")
    
    current_time = datetime.now().isoformat()
    
    # Franklin Half Dollar series (1948-1963)
    # Key dates and representative years
    franklin_half_dollars = [
        # 1948 - first year and key date
        {
            'coin_id': 'US-FRHD-1948-P',
            'series': 'Franklin Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1948,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Benjamin Franklin portrait facing right with LIBERTY around',
            'reverse_design': 'Liberty Bell with small eagle to right',
            'designer': 'John R. Sinnock',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'First year of issue. Mint mark above Liberty Bell on reverse.',
            'identification_keywords': 'franklin half dollar 1948 first year key date bell',
            'common_names': 'Franklin Half, Frankie',
            'rarity': 'key',
            'notes': 'Key date - first year of series. Look for FBL (Full Bell Lines) designation.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1949-S - key date
        {
            'coin_id': 'US-FRHD-1949-S',
            'series': 'Franklin Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1949,
            'mint_mark': 'S',
            'country': 'United States',
            'obverse_design': 'Benjamin Franklin portrait facing right with LIBERTY around',
            'reverse_design': 'Liberty Bell with small eagle to right',
            'designer': 'John R. Sinnock',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Mint mark above Liberty Bell on reverse.',
            'identification_keywords': 'franklin half dollar 1949 san francisco key date bell',
            'common_names': 'Franklin Half, Frankie',
            'rarity': 'key',
            'notes': 'Key date of series. Low mintage, scarce in all grades.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1953 - key date
        {
            'coin_id': 'US-FRHD-1953-P',
            'series': 'Franklin Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1953,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Benjamin Franklin portrait facing right with LIBERTY around',
            'reverse_design': 'Liberty Bell with small eagle to right',
            'designer': 'John R. Sinnock',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. No mint mark (Philadelphia).',
            'identification_keywords': 'franklin half dollar 1953 philadelphia key date bell',
            'common_names': 'Franklin Half, Frankie',
            'rarity': 'key',
            'notes': 'Key date of series. Low mintage of 2,796,920.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1953-S - key date
        {
            'coin_id': 'US-FRHD-1953-S',
            'series': 'Franklin Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1953,
            'mint_mark': 'S',
            'country': 'United States',
            'obverse_design': 'Benjamin Franklin portrait facing right with LIBERTY around',
            'reverse_design': 'Liberty Bell with small eagle to right',
            'designer': 'John R. Sinnock',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. Mint mark above Liberty Bell on reverse.',
            'identification_keywords': 'franklin half dollar 1953 san francisco key date bell',
            'common_names': 'Franklin Half, Frankie',
            'rarity': 'key',
            'notes': 'Key date of series. Very low mintage of 4,148,000.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1955 - key date and variety
        {
            'coin_id': 'US-FRHD-1955-P',
            'series': 'Franklin Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1955,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Benjamin Franklin portrait facing right with LIBERTY around',
            'reverse_design': 'Liberty Bell with small eagle to right',
            'designer': 'John R. Sinnock',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Key date. "Bugs Bunny" die clash variety exists.',
            'identification_keywords': 'franklin half dollar 1955 philadelphia key date bugs bunny variety',
            'common_names': 'Franklin Half, Frankie',
            'rarity': 'key',
            'notes': 'Key date with lowest mintage of series (2,498,181). Famous "Bugs Bunny" die clash variety.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1963 - final year
        {
            'coin_id': 'US-FRHD-1963-P',
            'series': 'Franklin Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1963,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Benjamin Franklin portrait facing right with LIBERTY around',
            'reverse_design': 'Liberty Bell with small eagle to right',
            'designer': 'John R. Sinnock',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Final year of Franklin Half Dollar series.',
            'identification_keywords': 'franklin half dollar 1963 philadelphia final year bell',
            'common_names': 'Franklin Half, Frankie',
            'rarity': 'common',
            'notes': 'Final year of series. Replaced by Kennedy Half Dollar in 1964.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1963-D - final year Denver
        {
            'coin_id': 'US-FRHD-1963-D',
            'series': 'Franklin Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1963,
            'mint_mark': 'D',
            'country': 'United States',
            'obverse_design': 'Benjamin Franklin portrait facing right with LIBERTY around',
            'reverse_design': 'Liberty Bell with small eagle to right',
            'designer': 'John R. Sinnock',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Final year Denver mint. Mint mark above Liberty Bell.',
            'identification_keywords': 'franklin half dollar 1963 denver final year bell',
            'common_names': 'Franklin Half, Frankie',
            'rarity': 'common',
            'notes': 'Final year Denver issue. High mintage of 67,069,292.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Common date example - 1961
        {
            'coin_id': 'US-FRHD-1961-P',
            'series': 'Franklin Half Dollar',
            'denomination': 'Half Dollar',
            'year': 1961,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Benjamin Franklin portrait facing right with LIBERTY around',
            'reverse_design': 'Liberty Bell with small eagle to right',
            'designer': 'John R. Sinnock',
            'composition': '90% silver, 10% copper',
            'weight_grams': 12.50,
            'diameter_mm': 30.6,
            'thickness_mm': None,
            'edge_type': 'Reeded',
            'distinguishing_features': 'Common date. Doubled-die reverse proof variety exists.',
            'identification_keywords': 'franklin half dollar 1961 philadelphia common bell doubled die',
            'common_names': 'Franklin Half, Frankie',
            'rarity': 'common',
            'notes': 'Representative common date. High mintage. 1961 proof has doubled-die reverse variety.',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    for coin in franklin_half_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series_id, series_name, country, denomination, year, mint,
                obverse_description, reverse_description, composition,
                weight_grams, diameter_mm, distinguishing_features, 
                identification_keywords, common_names, rarity, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['coin_id'][:7], coin['series'], coin['country'], 
            coin['denomination'], coin['year'], coin['mint_mark'], 
            coin['obverse_design'], coin['reverse_design'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'], coin['rarity'],
            coin['notes'], coin['created_at']
        ))

def add_three_cent_pieces(cursor):
    """Add Three-Cent Piece series (Silver 1851-1873, Nickel 1865-1889)"""
    print("Adding Three-Cent Piece series...")
    
    current_time = datetime.now().isoformat()
    
    # Silver Three-Cent Pieces (1851-1873)
    silver_three_cents = [
        # 1851 - first year Type I
        {
            'coin_id': 'US-SLTC-1851-P',
            'series': 'Silver Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1851,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with single-outline six-pointed star, UNITED STATES OF AMERICA around',
            'reverse_design': 'Roman numeral III inside C with ornaments',
            'designer': 'James B. Longacre',
            'composition': '75% silver, 25% copper',
            'weight_grams': 0.80,
            'diameter_mm': 14.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Type I - single outline star. First year of issue.',
            'identification_keywords': 'silver three cent 1851 trime type 1 first year',
            'common_names': 'Trime, Silver Trey',
            'rarity': 'common',
            'notes': 'First year of issue. Type I composition (75% silver).',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1851-O - only New Orleans mint three-cent
        {
            'coin_id': 'US-SLTC-1851-O',
            'series': 'Silver Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1851,
            'mint_mark': 'O',
            'country': 'United States',
            'obverse_design': 'Shield with single-outline six-pointed star, UNITED STATES OF AMERICA around',
            'reverse_design': 'Roman numeral III inside C with ornaments',
            'designer': 'James B. Longacre',
            'composition': '75% silver, 25% copper',
            'weight_grams': 0.80,
            'diameter_mm': 14.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Only New Orleans mint three-cent piece ever made. Type I.',
            'identification_keywords': 'silver three cent 1851 new orleans trime key date only',
            'common_names': 'Trime, Silver Trey',
            'rarity': 'key',
            'notes': 'Only three-cent piece ever made at New Orleans mint. Very scarce.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1854 - first Type II
        {
            'coin_id': 'US-SLTC-1854-P',
            'series': 'Silver Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1854,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with triple-outline six-pointed star, olive sprig and arrows',
            'reverse_design': 'Roman numeral III inside C with ornaments',
            'designer': 'James B. Longacre',
            'composition': '90% silver, 10% copper',
            'weight_grams': 0.75,
            'diameter_mm': 14.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Type II - triple outline star with olive sprig and arrows.',
            'identification_keywords': 'silver three cent 1854 trime type 2 triple outline',
            'common_names': 'Trime, Silver Trey',
            'rarity': 'common',
            'notes': 'First Type II issue. Changed to 90% silver composition.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1859 - first Type III
        {
            'coin_id': 'US-SLTC-1859-P',
            'series': 'Silver Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1859,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with double-outline six-pointed star',
            'reverse_design': 'Roman numeral III inside C with ornaments',
            'designer': 'James B. Longacre',
            'composition': '90% silver, 10% copper',
            'weight_grams': 0.75,
            'diameter_mm': 14.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Type III - double outline star, no olive sprig/arrows.',
            'identification_keywords': 'silver three cent 1859 trime type 3 double outline',
            'common_names': 'Trime, Silver Trey',
            'rarity': 'common',
            'notes': 'First Type III issue. Simplified design without olive sprig and arrows.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1873 - final year (proof only)
        {
            'coin_id': 'US-SLTC-1873-P',
            'series': 'Silver Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1873,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with double-outline six-pointed star',
            'reverse_design': 'Roman numeral III inside C with ornaments',
            'designer': 'James B. Longacre',
            'composition': '90% silver, 10% copper',
            'weight_grams': 0.75,
            'diameter_mm': 14.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Final year - proof only. Type III design.',
            'identification_keywords': 'silver three cent 1873 trime final year proof only',
            'common_names': 'Trime, Silver Trey',
            'rarity': 'key',
            'notes': 'Final year of series. Proof only - no business strikes.',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    # Nickel Three-Cent Pieces (1865-1889)
    nickel_three_cents = [
        # 1865 - first year
        {
            'coin_id': 'US-NLTC-1865-P',
            'series': 'Nickel Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1865,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head left with coronet inscribed LIBERTY',
            'reverse_design': 'Roman numeral III surrounded by wreath',
            'designer': 'James B. Longacre',
            'composition': '75% copper, 25% nickel',
            'weight_grams': 1.94,
            'diameter_mm': 17.9,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'First year of nickel three-cent series. Larger than silver.',
            'identification_keywords': 'nickel three cent 1865 first year copper nickel',
            'common_names': 'Nickel Three-Cent',
            'rarity': 'common',
            'notes': 'First year of nickel three-cent series. Larger and heavier than silver.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1877 - proof only key date
        {
            'coin_id': 'US-NLTC-1877-P',
            'series': 'Nickel Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1877,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head left with coronet inscribed LIBERTY',
            'reverse_design': 'Roman numeral III surrounded by wreath',
            'designer': 'James B. Longacre',
            'composition': '75% copper, 25% nickel',
            'weight_grams': 1.94,
            'diameter_mm': 17.9,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Proof only year - no business strikes made.',
            'identification_keywords': 'nickel three cent 1877 proof only key date',
            'common_names': 'Nickel Three-Cent',
            'rarity': 'key',
            'notes': 'Key date - proof only year. No business strikes produced.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1878 - proof only key date
        {
            'coin_id': 'US-NLTC-1878-P',
            'series': 'Nickel Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1878,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head left with coronet inscribed LIBERTY',
            'reverse_design': 'Roman numeral III surrounded by wreath',
            'designer': 'James B. Longacre',
            'composition': '75% copper, 25% nickel',
            'weight_grams': 1.94,
            'diameter_mm': 17.9,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Proof only year - no business strikes made.',
            'identification_keywords': 'nickel three cent 1878 proof only key date',
            'common_names': 'Nickel Three-Cent',
            'rarity': 'key',
            'notes': 'Key date - proof only year. No business strikes produced.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1885 - very low business strike mintage
        {
            'coin_id': 'US-NLTC-1885-P',
            'series': 'Nickel Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1885,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head left with coronet inscribed LIBERTY',
            'reverse_design': 'Roman numeral III surrounded by wreath',
            'designer': 'James B. Longacre',
            'composition': '75% copper, 25% nickel',
            'weight_grams': 1.94,
            'diameter_mm': 17.9,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Extremely low business strike mintage of only 1,000.',
            'identification_keywords': 'nickel three cent 1885 key date low mintage',
            'common_names': 'Nickel Three-Cent',
            'rarity': 'key',
            'notes': 'Key date - only 1,000 business strikes made. Extremely rare.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1889 - final year
        {
            'coin_id': 'US-NLTC-1889-P',
            'series': 'Nickel Three-Cent Piece',
            'denomination': 'Three Cents',
            'year': 1889,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Liberty head left with coronet inscribed LIBERTY',
            'reverse_design': 'Roman numeral III surrounded by wreath',
            'designer': 'James B. Longacre',
            'composition': '75% copper, 25% nickel',
            'weight_grams': 1.94,
            'diameter_mm': 17.9,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Final year of three-cent denomination.',
            'identification_keywords': 'nickel three cent 1889 final year last',
            'common_names': 'Nickel Three-Cent',
            'rarity': 'scarce',
            'notes': 'Final year of three-cent denomination. End of era.',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    all_three_cents = silver_three_cents + nickel_three_cents
    
    for coin in all_three_cents:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series_id, series_name, country, denomination, year, mint,
                obverse_description, reverse_description, composition,
                weight_grams, diameter_mm, distinguishing_features, 
                identification_keywords, common_names, rarity, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['coin_id'][:7], coin['series'], coin['country'], 
            coin['denomination'], coin['year'], coin['mint_mark'], 
            coin['obverse_design'], coin['reverse_design'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'], coin['rarity'],
            coin['notes'], coin['created_at']
        ))

def add_two_cent_pieces(cursor):
    """Add Two-Cent Piece series (1864-1873)"""
    print("Adding Two-Cent Piece series...")
    
    current_time = datetime.now().isoformat()
    
    # Two-Cent Piece series (1864-1873)
    two_cent_pieces = [
        # 1864 Large Motto - first year (common variety)
        {
            'coin_id': 'US-TWCT-1864-P',
            'series': 'Two-Cent Piece',
            'denomination': 'Two Cents',
            'year': 1864,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with ribbons, "IN GOD WE TRUST" on banner above',
            'reverse_design': 'Wreath with "2 CENTS" in center',
            'designer': 'James B. Longacre',
            'composition': '95% copper, 5% tin and zinc',
            'weight_grams': 6.22,
            'diameter_mm': 23.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'First US coin with "IN GOD WE TRUST". Large Motto variety.',
            'identification_keywords': 'two cent 1864 first year in god we trust large motto',
            'common_names': 'Two-Cent Piece',
            'rarity': 'common',
            'notes': 'First year. Large Motto is common variety. Historic first use of "IN GOD WE TRUST".',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1865/4 - overdate variety
        {
            'coin_id': 'US-TWCT-1865-P',
            'series': 'Two-Cent Piece',
            'denomination': 'Two Cents',
            'year': 1865,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with ribbons, "IN GOD WE TRUST" on banner above',
            'reverse_design': 'Wreath with "2 CENTS" in center',
            'designer': 'James B. Longacre',
            'composition': '95% copper, 5% tin and zinc',
            'weight_grams': 6.22,
            'diameter_mm': 23.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Overdate variety 1865/4 exists. High mintage year.',
            'identification_keywords': 'two cent 1865 overdate variety 1865/4',
            'common_names': 'Two-Cent Piece',
            'rarity': 'common',
            'notes': 'High mintage year. 1865/4 overdate variety is scarce and valuable.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1872 - key date low mintage
        {
            'coin_id': 'US-TWCT-1872-P',
            'series': 'Two-Cent Piece',
            'denomination': 'Two Cents',
            'year': 1872,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with ribbons, "IN GOD WE TRUST" on banner above',
            'reverse_design': 'Wreath with "2 CENTS" in center',
            'designer': 'James B. Longacre',
            'composition': '95% copper, 5% tin and zinc',
            'weight_grams': 6.22,
            'diameter_mm': 23.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Key date with very low mintage of 65,000.',
            'identification_keywords': 'two cent 1872 key date low mintage',
            'common_names': 'Two-Cent Piece',
            'rarity': 'key',
            'notes': 'Key date with lowest business strike mintage of 65,000.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 1873 - final year (proof only)
        {
            'coin_id': 'US-TWCT-1873-P',
            'series': 'Two-Cent Piece',
            'denomination': 'Two Cents',
            'year': 1873,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with ribbons, "IN GOD WE TRUST" on banner above',
            'reverse_design': 'Wreath with "2 CENTS" in center',
            'designer': 'James B. Longacre',
            'composition': '95% copper, 5% tin and zinc',
            'weight_grams': 6.22,
            'diameter_mm': 23.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Final year - proof only. Open 3 vs Closed 3 varieties.',
            'identification_keywords': 'two cent 1873 final year proof only open closed 3',
            'common_names': 'Two-Cent Piece',
            'rarity': 'key',
            'notes': 'Final year - proof only. Open 3 and Closed 3 varieties exist.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Common date example - 1865
        {
            'coin_id': 'US-TWCT-1869-P',
            'series': 'Two-Cent Piece',
            'denomination': 'Two Cents',
            'year': 1869,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Shield with ribbons, "IN GOD WE TRUST" on banner above',
            'reverse_design': 'Wreath with "2 CENTS" in center',
            'designer': 'James B. Longacre',
            'composition': '95% copper, 5% tin and zinc',
            'weight_grams': 6.22,
            'diameter_mm': 23.0,
            'thickness_mm': None,
            'edge_type': 'Plain',
            'distinguishing_features': 'Representative mid-period common date.',
            'identification_keywords': 'two cent 1869 common date',
            'common_names': 'Two-Cent Piece',
            'rarity': 'common',
            'notes': 'Representative common date from middle of series run.',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    for coin in two_cent_pieces:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series_id, series_name, country, denomination, year, mint,
                obverse_description, reverse_description, composition,
                weight_grams, diameter_mm, distinguishing_features, 
                identification_keywords, common_names, rarity, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['coin_id'][:7], coin['series'], coin['country'], 
            coin['denomination'], coin['year'], coin['mint_mark'], 
            coin['obverse_design'], coin['reverse_design'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'], coin['rarity'],
            coin['notes'], coin['created_at']
        ))

def add_presidential_dollars(cursor):
    """Add Presidential Dollar series (2007-2020)"""
    print("Adding Presidential Dollar series...")
    
    current_time = datetime.now().isoformat()
    
    # Presidential Dollar series (2007-2020)
    presidential_dollars = [
        # 2007 Washington - first president, first year
        {
            'coin_id': 'US-PRDO-2007-P',
            'series': 'Presidential Dollar',
            'denomination': 'Dollar',
            'year': 2007,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'George Washington portrait facing right',
            'reverse_design': 'Statue of Liberty with "$1" denomination',
            'designer': 'Don Everhart',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, mint mark, E PLURIBUS UNUM',
            'distinguishing_features': 'First presidential dollar. Edge lettering. "Godless Dollar" error exists.',
            'identification_keywords': 'presidential dollar 2007 washington first godless error',
            'common_names': 'Presidential Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'First presidential dollar. Famous "Godless Dollar" error missing edge lettering.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 2007 Adams - second president
        {
            'coin_id': 'US-PRDO-2007-D',
            'series': 'Presidential Dollar',
            'denomination': 'Dollar',
            'year': 2007,
            'mint_mark': 'D',
            'country': 'United States',
            'obverse_design': 'John Adams portrait facing right',
            'reverse_design': 'Statue of Liberty with "$1" denomination',
            'designer': 'Don Everhart',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, mint mark, E PLURIBUS UNUM',
            'distinguishing_features': 'Second president dollar. Edge lettering. Doubled edge lettering error exists.',
            'identification_keywords': 'presidential dollar 2007 adams second doubled edge error',
            'common_names': 'Presidential Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'Second president issued. Doubled edge lettering error is valuable.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 2009 Harrison - transition to obverse mint mark
        {
            'coin_id': 'US-PRDO-2009-P',
            'series': 'Presidential Dollar',
            'denomination': 'Dollar',
            'year': 2009,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'William Henry Harrison portrait facing right',
            'reverse_design': 'Statue of Liberty with "$1" denomination',
            'designer': 'Don Everhart',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, E PLURIBUS UNUM',
            'distinguishing_features': 'Mint mark moved to obverse in 2009. Edge still lettered.',
            'identification_keywords': 'presidential dollar 2009 harrison mint mark obverse',
            'common_names': 'Presidential Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'First year with mint mark on obverse instead of edge.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 2016 Reagan - final regular circulation year
        {
            'coin_id': 'US-PRDO-2016-P',
            'series': 'Presidential Dollar',
            'denomination': 'Dollar',
            'year': 2016,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Ronald Reagan portrait facing right',
            'reverse_design': 'Statue of Liberty with "$1" denomination',
            'designer': 'Don Everhart',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, E PLURIBUS UNUM',
            'distinguishing_features': 'Final year of original presidential dollar program.',
            'identification_keywords': 'presidential dollar 2016 reagan final year program',
            'common_names': 'Presidential Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'Final year of original presidential dollar program before hiatus.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 2020 Bush - return of series
        {
            'coin_id': 'US-PRDO-2020-P',
            'series': 'Presidential Dollar',
            'denomination': 'Dollar',
            'year': 2020,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'George H.W. Bush portrait facing right',
            'reverse_design': 'Statue of Liberty with "$1" denomination',
            'designer': 'Don Everhart',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, E PLURIBUS UNUM',
            'distinguishing_features': 'Return of series after hiatus. George H.W. Bush.',
            'identification_keywords': 'presidential dollar 2020 bush return series',
            'common_names': 'Presidential Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'Return of series in 2020 for George H.W. Bush after 3-year hiatus.',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    for coin in presidential_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series_id, series_name, country, denomination, year, mint,
                obverse_description, reverse_description, composition,
                weight_grams, diameter_mm, distinguishing_features, 
                identification_keywords, common_names, rarity, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['coin_id'][:7], coin['series'], coin['country'], 
            coin['denomination'], coin['year'], coin['mint_mark'], 
            coin['obverse_design'], coin['reverse_design'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'], coin['rarity'],
            coin['notes'], coin['created_at']
        ))

def add_native_american_dollars(cursor):
    """Add Native American Dollar series (2009-present)"""
    print("Adding Native American Dollar series...")
    
    current_time = datetime.now().isoformat()
    
    # Native American Dollar series (2009-present)
    native_american_dollars = [
        # 2009 - first year with Three Sisters agriculture theme
        {
            'coin_id': 'US-NADO-2009-P',
            'series': 'Native American Dollar',
            'denomination': 'Dollar',
            'year': 2009,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Sacagawea with baby Jean Baptiste',
            'reverse_design': 'Three Sisters agriculture - corn, beans, and squash',
            'designer': 'Glenna Goodacre (obverse), Norman E. Nemeth (reverse)',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, mint mark, E PLURIBUS UNUM',
            'distinguishing_features': 'First Native American Dollar. Three Sisters agriculture theme.',
            'identification_keywords': 'native american dollar 2009 sacagawea three sisters agriculture',
            'common_names': 'Native American Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'First year of series. Features Three Sisters agricultural practice.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 2010 - Great Law of Peace theme
        {
            'coin_id': 'US-NADO-2010-P',
            'series': 'Native American Dollar',
            'denomination': 'Dollar',
            'year': 2010,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Sacagawea with baby Jean Baptiste',
            'reverse_design': 'Hiawatha belt symbolizing Great Law of Peace',
            'designer': 'Glenna Goodacre (obverse), Thomas Cleveland (reverse)',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, mint mark, E PLURIBUS UNUM',
            'distinguishing_features': 'Great Law of Peace theme. Hiawatha belt design.',
            'identification_keywords': 'native american dollar 2010 great law peace hiawatha belt',
            'common_names': 'Native American Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'Second year. Honors Great Law of Peace and Iroquois Confederacy.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 2015 - Mohawk Ironworkers theme
        {
            'coin_id': 'US-NADO-2015-P',
            'series': 'Native American Dollar',
            'denomination': 'Dollar',
            'year': 2015,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Sacagawea with baby Jean Baptiste',
            'reverse_design': 'Mohawk ironworkers building New York skyline',
            'designer': 'Glenna Goodacre (obverse), Ronald D. Sanders (reverse)',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, mint mark, E PLURIBUS UNUM',
            'distinguishing_features': 'Mohawk ironworkers theme. New York skyline construction.',
            'identification_keywords': 'native american dollar 2015 mohawk ironworkers skyline construction',
            'common_names': 'Native American Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'Honors Mohawk ironworkers who built American skyscrapers.',
            'created_at': current_time,
            'updated_at': current_time
        },
        # 2020 - Elizabeth Peratrovich and Anti-Discrimination theme
        {
            'coin_id': 'US-NADO-2020-P',
            'series': 'Native American Dollar',
            'denomination': 'Dollar',
            'year': 2020,
            'mint_mark': 'P',
            'country': 'United States',
            'obverse_design': 'Sacagawea with baby Jean Baptiste',
            'reverse_design': 'Elizabeth Peratrovich and Alaska Anti-Discrimination Act',
            'designer': 'Glenna Goodacre (obverse), Chris Costello (reverse)',
            'composition': '88.5% copper, 6% zinc, 3.5% manganese, 2% nickel',
            'weight_grams': 8.1,
            'diameter_mm': 26.5,
            'thickness_mm': None,
            'edge_type': 'Lettered with date, mint mark, E PLURIBUS UNUM',
            'distinguishing_features': 'Elizabeth Peratrovich civil rights theme.',
            'identification_keywords': 'native american dollar 2020 elizabeth peratrovich civil rights alaska',
            'common_names': 'Native American Dollar, Golden Dollar',
            'rarity': 'common',
            'notes': 'Honors Elizabeth Peratrovich and Alaska Anti-Discrimination Act of 1945.',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    for coin in native_american_dollars:
        cursor.execute("""
            INSERT OR REPLACE INTO coins (
                coin_id, series_id, series_name, country, denomination, year, mint,
                obverse_description, reverse_description, composition,
                weight_grams, diameter_mm, distinguishing_features, 
                identification_keywords, common_names, rarity, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin['coin_id'], coin['coin_id'][:7], coin['series'], coin['country'], 
            coin['denomination'], coin['year'], coin['mint_mark'], 
            coin['obverse_design'], coin['reverse_design'], coin['composition'],
            coin['weight_grams'], coin['diameter_mm'], coin['distinguishing_features'],
            coin['identification_keywords'], coin['common_names'], coin['rarity'],
            coin['notes'], coin['created_at']
        ))

def main():
    """Main function to add all missing coin series"""
    print("Adding missing US coin series to database...")
    print("=" * 50)
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    try:
        # Add each series
        add_barber_half_dollars(cursor)
        add_walking_liberty_half_dollars(cursor)
        add_franklin_half_dollars(cursor)
        add_three_cent_pieces(cursor)
        add_two_cent_pieces(cursor)
        add_presidential_dollars(cursor)
        add_native_american_dollars(cursor)
        
        # Commit changes
        conn.commit()
        print("\n" + "=" * 50)
        print("✅ Successfully added missing coin series to database!")
        print("Run 'uv run python scripts/export_from_database.py' to regenerate JSON files")
        
    except Exception as e:
        print(f"❌ Error adding coins: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()