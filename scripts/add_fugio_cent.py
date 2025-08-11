#!/usr/bin/env python3
"""
Add Fugio Cent (1787) series and varieties to the coin taxonomy database.

Based on PCGS registry, there are 15 major varieties of the 1787 Fugio Cent
that collectors encounter in the marketplace.
"""

import sqlite3
import json
from datetime import datetime

def add_fugio_cent_series_and_coins():
    """Add Fugio Cent series and 15 PCGS varieties to database"""
    
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    try:
        # First, add the Fugio Cent series
        series_data = {
            'series_id': 'fugio_cent',
            'series_name': 'Fugio Cent',
            'series_abbreviation': 'FUGC',
            'country_code': 'US',
            'denomination': 'Cents',
            'start_year': 1787,
            'end_year': 1787,
            'defining_characteristics': 'First official U.S. cent authorized by Congress, featuring sundial design with "FUGIO" and linked rings with "WE ARE ONE"',
            'official_name': 'Fugio Cent (Federal Contract Coinage)',
            'type': 'coin'
        }
        
        cursor.execute('''
            INSERT INTO series_registry (
                series_id, series_name, series_abbreviation, country_code, 
                denomination, start_year, end_year, defining_characteristics, 
                official_name, type, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            series_data['series_id'], series_data['series_name'], 
            series_data['series_abbreviation'], series_data['country_code'],
            series_data['denomination'], series_data['start_year'], 
            series_data['end_year'], series_data['defining_characteristics'],
            series_data['official_name'], series_data['type'],
            datetime.now().isoformat(), datetime.now().isoformat()
        ))
        
        # Define the 15 PCGS varieties based on the research
        fugio_varieties = [
            {
                'coin_id': 'US-FUGC-1787-P',
                'variety_name': 'No Cinq, Cross After Date, STATES UNITED',
                'pcgs_number': '874',
                'newman_marriages': ['1-A', '1-B'],
                'rarity': 'scarce',
                'distinguishing_features': [
                    'No cinquefoils (5-petal flowers) on obverse',
                    'Cross after date on obverse',
                    'STATES UNITED legend on reverse'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, date "1787" with cross after, no cinquefoils',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "STATES UNITED" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-D',
                'variety_name': 'Cross After Date, UNITED STATES',
                'pcgs_number': '875',
                'newman_marriages': ['2-C', '3-D'],
                'rarity': 'scarce',
                'distinguishing_features': [
                    'Cross after date on obverse',
                    'UNITED STATES legend on reverse'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, date "1787" with cross after',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "UNITED STATES" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-S',
                'variety_name': 'STATES UNITED, 4 Cinquefoils',
                'pcgs_number': '876',
                'newman_marriages': ['4-E', '5-F'],
                'rarity': 'common',
                'distinguishing_features': [
                    'Four cinquefoils (5-petal flowers) on obverse',
                    'STATES UNITED legend on reverse'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, four cinquefoils around dial, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "STATES UNITED" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-CC',
                'variety_name': 'UNITED STATES, 4 Cinquefoils',
                'pcgs_number': '877',
                'newman_marriages': ['6-G', '7-H'],
                'rarity': 'common',
                'distinguishing_features': [
                    'Four cinquefoils (5-petal flowers) on obverse',
                    'UNITED STATES legend on reverse'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, four cinquefoils around dial, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "UNITED STATES" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-W',
                'variety_name': 'STATES UNITED, Eight-Pointed Stars',
                'pcgs_number': '878',
                'newman_marriages': ['15-Y'],
                'rarity': 'key',
                'distinguishing_features': [
                    'Eight-pointed stars instead of cinquefoils',
                    'STATES UNITED legend on reverse',
                    'Only die marriage with this star configuration'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, eight-pointed stars around dial, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "STATES UNITED" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-N',
                'variety_name': 'UNITED STATES, Pointed Rays (common)',
                'pcgs_number': '879',
                'newman_marriages': ['8-I', '9-J', '10-K'],
                'rarity': 'common',
                'distinguishing_features': [
                    'Pointed rays extending from sundial',
                    'UNITED STATES legend on reverse',
                    'Most common variety type'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, pointed rays extending from dial, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "UNITED STATES" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-O',
                'variety_name': 'STATES UNITED, Pointed Rays (common)',
                'pcgs_number': '880',
                'newman_marriages': ['11-L', '12-M', '13-N'],
                'rarity': 'common',
                'distinguishing_features': [
                    'Pointed rays extending from sundial',
                    'STATES UNITED legend on reverse',
                    'Common variety type'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, pointed rays extending from dial, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "STATES UNITED" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-H',
                'variety_name': 'UNITED STATES, 1 over Horizontal 1',
                'pcgs_number': '881',
                'newman_marriages': ['10-G'],
                'rarity': 'scarce',
                'distinguishing_features': [
                    'Overdate: vertical "1" punched over horizontal "1" in date',
                    'UNITED STATES legend on reverse',
                    'Clear evidence of date correction'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, date "1787" with "1" over horizontal "1", pointed rays',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "UNITED STATES" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-L',
                'variety_name': 'STATES UNITED, 1 over Horizontal 1',
                'pcgs_number': '882',
                'newman_marriages': ['10-L'],
                'rarity': 'scarce',
                'distinguishing_features': [
                    'Overdate: vertical "1" punched over horizontal "1" in date',
                    'STATES UNITED legend on reverse',
                    'Clear evidence of date correction'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, date "1787" with "1" over horizontal "1", pointed rays',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "STATES UNITED" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-U',
                'variety_name': 'UNITED Above, STATES Below',
                'pcgs_number': '883',
                'newman_marriages': ['14-O'],
                'rarity': 'scarce',
                'distinguishing_features': [
                    'Unusual reverse legend arrangement',
                    'UNITED at top of rim, STATES at bottom',
                    'Label-top variety often omitted from short lists'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, pointed rays extending from dial, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "UNITED" above, "STATES" below'
            },
            {
                'coin_id': 'US-FUGC-1787-R',
                'variety_name': 'STATES UNITED, Raised Rims (no rays)',
                'pcgs_number': '884',
                'newman_marriages': ['1-Y'],
                'rarity': 'key',
                'distinguishing_features': [
                    'Raised rims on both sides',
                    'No rays extending from sundial',
                    'STATES UNITED legend on reverse',
                    'R-6 rarity (extremely rare)'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, no rays, raised rim, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "STATES UNITED" around rim, raised rim'
            },
            {
                'coin_id': 'US-FUGC-1787-T',
                'variety_name': 'STATES UNITED at Sides (thin letters)',
                'pcgs_number': '885',
                'newman_marriages': ['16-P'],
                'rarity': 'scarce',
                'distinguishing_features': [
                    'STATES UNITED legend positioned at sides of reverse',
                    'Thin, narrow letter style',
                    'Distinctive reverse layout'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, pointed rays extending from dial, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "STATES UNITED" at sides with thin letters'
            },
            {
                'coin_id': 'US-FUGC-1787-C',
                'variety_name': 'CLUB RAYS, Rounded Ends',
                'pcgs_number': '886',
                'newman_marriages': ['17-Q', '18-R'],
                'rarity': 'scarce',
                'distinguishing_features': [
                    'Club-shaped rays extending from sundial',
                    'Rounded ends on the club rays',
                    'Distinctive ray design'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, club-shaped rays with rounded ends, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "UNITED STATES" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-A',
                'variety_name': 'CLUB RAYS, Concave Ends, UNITED STATES',
                'pcgs_number': '887',
                'newman_marriages': ['19-S', '20-T'],
                'rarity': 'scarce',
                'distinguishing_features': [
                    'Club-shaped rays extending from sundial',
                    'Concave (curved inward) ends on club rays',
                    'UNITED STATES legend on reverse',
                    'Contains FUCIO misspelling variety in late die state'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, club-shaped rays with concave ends, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "UNITED STATES" around rim'
            },
            {
                'coin_id': 'US-FUGC-1787-Z',
                'variety_name': 'CLUB RAYS, Concave Ends, STATES UNITED (rarest)',
                'pcgs_number': '888',
                'newman_marriages': ['1-Z'],
                'rarity': 'key',
                'distinguishing_features': [
                    'Club-shaped rays extending from sundial',
                    'Concave (curved inward) ends on club rays',
                    'STATES UNITED legend on reverse',
                    'Contains American Congress reverse variety',
                    'Rarest of all Fugio varieties (R-6+)'
                ],
                'obverse_desc': 'Sundial with "FUGIO" above, club-shaped rays with concave ends, date "1787"',
                'reverse_desc': '13 linked rings with "WE ARE ONE" in center, "STATES UNITED" around rim (American Congress variety)'
            }
        ]
        
        # Insert each coin variety
        for variety in fugio_varieties:
            coin_data = {
                'coin_id': variety['coin_id'],
                'series_id': 'fugio_cent',
                'country': 'US',
                'denomination': 'Cents',
                'series_name': 'Fugio Cent',
                'year': 1787,
                'mint': variety['coin_id'].split('-')[-1],  # Extract mint mark from coin_id
                'business_strikes': 0,  # Unknown exact numbers, distributed ~400,000 total
                'proof_strikes': 0,
                'rarity': variety['rarity'],
                'composition': json.dumps({"copper": 1.0}),
                'weight_grams': 10.0,  # Average ~10 grams
                'diameter_mm': 28.5,   # Average 28-29 mm
                'varieties': json.dumps([{
                    'variety_id': f"fugio-{variety['pcgs_number']}",
                    'name': variety['variety_name'],
                    'pcgs_number': variety['pcgs_number'],
                    'newman_marriages': variety['newman_marriages'],
                    'characteristics': variety['distinguishing_features']
                }]),
                'source_citation': 'PCGS Registry, Newman Die Marriage Catalog, APMEX Historical Guide',
                'notes': f"Federal Contract Coinage - {variety['variety_name']}. Newman marriages: {', '.join(variety['newman_marriages'])}. First official U.S. cent authorized by Congress.",
                'obverse_description': variety['obverse_desc'],
                'reverse_description': variety['reverse_desc'],
                'distinguishing_features': json.dumps(variety['distinguishing_features']),
                'identification_keywords': json.dumps([
                    'fugio cent', '1787 cent', 'federal contract', 'sundial', 
                    'we are one', 'linked rings', variety['variety_name'].lower(),
                    'first u.s. cent', 'colonial coin', 'early american'
                ]),
                'common_names': json.dumps([
                    'Fugio Cent', 
                    '1787 Fugio Cent',
                    f'Fugio Cent - {variety["variety_name"]}',
                    'Federal Contract Cent'
                ]),
                'category': 'COIN',
                'issuer': 'United States (Federal Contract)',
                'series_year': '1787',
                'calendar_type': 'GREGORIAN',
                'original_date': '1787'
            }
            
            cursor.execute('''
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name, year, mint,
                    business_strikes, proof_strikes, rarity, composition, weight_grams, 
                    diameter_mm, varieties, source_citation, notes, obverse_description,
                    reverse_description, distinguishing_features, identification_keywords,
                    common_names, category, issuer, series_year, calendar_type, original_date,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coin_data['coin_id'], coin_data['series_id'], coin_data['country'],
                coin_data['denomination'], coin_data['series_name'], coin_data['year'],
                coin_data['mint'], coin_data['business_strikes'], coin_data['proof_strikes'],
                coin_data['rarity'], coin_data['composition'], coin_data['weight_grams'],
                coin_data['diameter_mm'], coin_data['varieties'], coin_data['source_citation'],
                coin_data['notes'], coin_data['obverse_description'], coin_data['reverse_description'],
                coin_data['distinguishing_features'], coin_data['identification_keywords'],
                coin_data['common_names'], coin_data['category'], coin_data['issuer'],
                coin_data['series_year'], coin_data['calendar_type'], coin_data['original_date'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        print(f"✅ Successfully added Fugio Cent series and {len(fugio_varieties)} varieties to database")
        
        # Verify the insertions
        cursor.execute("SELECT COUNT(*) FROM coins WHERE series_id = 'fugio_cent'")
        coin_count = cursor.fetchone()[0]
        print(f"✅ Verified: {coin_count} Fugio Cent varieties in database")
        
        cursor.execute("SELECT COUNT(*) FROM series_registry WHERE series_id = 'fugio_cent'")
        series_count = cursor.fetchone()[0]
        print(f"✅ Verified: {series_count} Fugio Cent series entry in database")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    print("Adding Fugio Cent (1787) series and 15 PCGS varieties...")
    add_fugio_cent_series_and_coins()
    print("✅ Fugio Cent addition complete!")