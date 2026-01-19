#!/usr/bin/env python3
"""
Complete Buffalo Nickel variant implementation with all years, mintages, and varieties.
Solves Issue #55: Add Buffalo Nickel variants to tracking system
"""

import sqlite3
from datetime import datetime

def clear_existing_buffalo_variants(conn):
    """Clear existing Buffalo variants for fresh import"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coin_variants WHERE base_type = 'BUFFALO_NICKEL'")
    print(f"🧹 Cleared existing Buffalo Nickel variants")

def add_complete_buffalo_variants(conn):
    """Add all Buffalo Nickel variants with mintage data"""
    
    buffalo_variants = []
    
    # 1913 Type 1 (Raised Ground) with mintages
    type1_data = [
        ('P', 30992000, 10),
        ('D', 5337000, 20),
        ('S', 2105000, 30)
    ]
    
    for mint, mintage, sort in type1_data:
        buffalo_variants.append({
            'variant_id': f'US-BUFF-1913-{mint}-T1',
            'base_type': 'BUFFALO_NICKEL',
            'denomination': '5 cents',
            'series_name': 'Buffalo Nickel',
            'year': 1913,
            'mint_mark': mint,
            'variant_type': 'Type 1 - Raised Ground',
            'variant_description': f'1913{"-" + mint if mint != "P" else ""} Type 1 - FIVE CENTS on raised ground',
            'sort_order': sort,
            'is_major_variant': 1,
            'mintage': mintage,
            'key_date_status': 'scarce' if mint == 'S' else 'common',
            'notes': 'First year, Type 1 design'
        })
    
    # 1913 Type 2 (Recessed) with mintages
    type2_1913_data = [
        ('P', 29857186, 40),
        ('D', 4156000, 50),
        ('S', 1209000, 60, 'semi-key')  # Lowest mintage Type 2
    ]
    
    for data in type2_1913_data:
        mint, mintage, sort = data[0], data[1], data[2]
        key_status = data[3] if len(data) > 3 else 'common'
        
        buffalo_variants.append({
            'variant_id': f'US-BUFF-1913-{mint}-T2',
            'base_type': 'BUFFALO_NICKEL',
            'denomination': '5 cents',
            'series_name': 'Buffalo Nickel',
            'year': 1913,
            'mint_mark': mint,
            'variant_type': 'Type 2 - Recessed',
            'variant_description': f'1913{"-" + mint if mint != "P" else ""} Type 2 - FIVE CENTS in recess',
            'sort_order': sort,
            'is_major_variant': 1,
            'mintage': mintage,
            'key_date_status': key_status,
            'notes': 'Mid-year design change to Type 2'
        })
    
    # Regular Type 2 mintages (1914-1938)
    mintage_data = {
        1914: [('P', 20664463), ('D', 3912000, 'semi-key'), ('S', 3470000)],
        1915: [('P', 20986220), ('D', 7569000), ('S', 1505000, 'semi-key')],
        1916: [('P', 63497466), ('D', 16860000), ('S', 11800000)],
        1917: [('P', 51424029), ('D', 9652000), ('S', 4193000)],
        1918: [('P', 32866000), ('D', 8362000), ('S', 4882000)],
        1919: [('P', 60868000), ('D', 8006000), ('S', 7524000)],
        1920: [('P', 63093000), ('D', 9418000), ('S', 9689000)],
        1921: [('P', 10663000), ('S', 1557000, 'semi-key')],
        # 1922: No nickels minted
        1923: [('P', 35715000), ('S', 6142000)],
        1924: [('P', 21620000), ('D', 5258000), ('S', 1437000, 'semi-key')],
        1925: [('P', 35565100), ('D', 4450000), ('S', 6256000)],
        1926: [('P', 44693000), ('D', 5638000), ('S', 970000, 'key')],  # 1926-S is major key
        1927: [('P', 37981000), ('D', 5730000), ('S', 3430000)],
        1928: [('P', 23411000), ('D', 6436000), ('S', 6936000)],
        1929: [('P', 36446000), ('D', 8370000), ('S', 7754000)],
        1930: [('P', 22849000), ('S', 5435000)],
        1931: [('S', 1200000, 'key')],  # Only S mint, key date
        # 1932-1933: No nickels minted
        1934: [('P', 20213000), ('D', 7480000)],
        1935: [('P', 58264000), ('D', 12092000), ('S', 10300000)],
        1936: [('P', 119001420), ('D', 24814000), ('S', 14930000)],
        1937: [('P', 79480000), ('D', 17826000), ('S', 5635000)],
        1938: [('D', 7020000)]  # Final year, Denver only
    }
    
    # Add regular business strikes
    for year, mint_data in mintage_data.items():
        for i, data in enumerate(mint_data):
            mint = data[0]
            mintage = data[1]
            key_status = data[2] if len(data) > 2 else 'common'
            
            buffalo_variants.append({
                'variant_id': f'US-BUFF-{year}-{mint}',
                'base_type': 'BUFFALO_NICKEL',
                'denomination': '5 cents',
                'series_name': 'Buffalo Nickel',
                'year': year,
                'mint_mark': mint,
                'variant_type': 'Type 2 - Business Strike',
                'variant_description': f'{year}{"-" + mint if mint != "P" else ""} Buffalo Nickel Type 2',
                'sort_order': 10 + (i * 10),
                'is_major_variant': 0,
                'mintage': mintage,
                'key_date_status': key_status,
                'notes': 'Final year' if year == 1938 else None
            })
    
    # Special varieties (overdates, errors, doubled dies)
    special_varieties = [
        {
            'variant_id': 'US-BUFF-1914-P-4OVER3',
            'year': 1914,
            'mint_mark': 'P',
            'variant_type': '1914/3 Overdate',
            'variant_description': '1914 4 over 3 overdate variety',
            'sort_order': 15,
            'is_major_variant': 1,
            'mintage': None,  # Included in regular 1914 mintage
            'key_date_status': 'scarce',
            'notes': 'Scarce overdate variety'
        },
        {
            'variant_id': 'US-BUFF-1916-P-DDO',
            'year': 1916,
            'mint_mark': 'P',
            'variant_type': 'Doubled Die Obverse',
            'variant_description': '1916 Doubled Die Obverse variety',
            'sort_order': 15,
            'is_major_variant': 1,
            'mintage': None,
            'key_date_status': 'scarce',
            'notes': 'Doubled Die on obverse'
        },
        {
            'variant_id': 'US-BUFF-1918-D-8OVER7',
            'year': 1918,
            'mint_mark': 'D',
            'variant_type': '1918/7-D Overdate',
            'variant_description': '1918-D 8 over 7 overdate variety',
            'sort_order': 25,
            'is_major_variant': 1,
            'mintage': None,
            'key_date_status': 'scarce',
            'notes': 'Popular overdate variety'
        },
        {
            'variant_id': 'US-BUFF-1935-P-DDR',
            'year': 1935,
            'mint_mark': 'P',
            'variant_type': 'Doubled Die Reverse',
            'variant_description': '1935 Doubled Die Reverse variety',
            'sort_order': 15,
            'is_major_variant': 1,
            'mintage': None,
            'key_date_status': 'scarce',
            'notes': 'Doubled Die on reverse'
        },
        {
            'variant_id': 'US-BUFF-1936-D-3HALFLEG',
            'year': 1936,
            'mint_mark': 'D',
            'variant_type': '3-1/2 Legged Buffalo',
            'variant_description': '1936-D 3-1/2 Legged Buffalo variety',
            'sort_order': 25,
            'is_major_variant': 1,
            'mintage': None,
            'key_date_status': 'scarce',
            'notes': 'Die polishing error, est. 10-15k survive'
        },
        {
            'variant_id': 'US-BUFF-1937-D-3LEG',
            'year': 1937,
            'mint_mark': 'D',
            'variant_type': 'Three-Legged Buffalo',
            'variant_description': '1937-D Three-Legged Buffalo variety',
            'sort_order': 25,
            'is_major_variant': 1,
            'mintage': None,
            'key_date_status': 'scarce',
            'notes': 'Most famous Buffalo Nickel error, est. 10-20k survive'
        }
    ]
    
    # Add special varieties
    for variety in special_varieties:
        buffalo_variants.append({
            'variant_id': variety['variant_id'],
            'base_type': 'BUFFALO_NICKEL',
            'denomination': '5 cents',
            'series_name': 'Buffalo Nickel',
            'year': variety['year'],
            'mint_mark': variety['mint_mark'],
            'variant_type': variety['variant_type'],
            'variant_description': variety['variant_description'],
            'sort_order': variety['sort_order'],
            'is_major_variant': variety['is_major_variant'],
            'mintage': variety['mintage'],
            'key_date_status': variety['key_date_status'],
            'notes': variety['notes']
        })
    
    # Add Proof variants for select years
    proof_years = [
        (1913, 'P', 'Matte Proof'),
        (1914, 'P', 'Matte Proof'),
        (1915, 'P', 'Matte Proof'),
        (1916, 'P', 'Matte Proof'),
        (1936, 'P', 'Brilliant Proof'),
        (1937, 'P', 'Brilliant Proof')
    ]
    
    for year, mint, proof_type in proof_years:
        buffalo_variants.append({
            'variant_id': f'US-BUFF-{year}-{mint}-PROOF',
            'base_type': 'BUFFALO_NICKEL',
            'denomination': '5 cents',
            'series_name': 'Buffalo Nickel',
            'year': year,
            'mint_mark': mint,
            'variant_type': proof_type,
            'variant_description': f'{year} Buffalo Nickel {proof_type}',
            'sort_order': 100,
            'is_major_variant': 0,
            'mintage': None,
            'key_date_status': 'scarce',
            'notes': f'{proof_type} finish for collectors'
        })
    
    # Insert all variants
    for variant in buffalo_variants:
        conn.execute('''
            INSERT OR REPLACE INTO coin_variants (
                variant_id, base_type, denomination, series_name, year, mint_mark,
                variant_type, variant_description, sort_order, is_major_variant, 
                mintage, key_date_status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            variant['variant_id'],
            variant['base_type'],
            variant['denomination'],
            variant['series_name'],
            variant['year'],
            variant['mint_mark'],
            variant['variant_type'],
            variant['variant_description'],
            variant['sort_order'],
            variant['is_major_variant'],
            variant['mintage'],
            variant['key_date_status'],
            variant['notes']
        ))
    
    return len(buffalo_variants)

def verify_complete_implementation(conn):
    """Verify the complete Buffalo Nickel implementation"""
    cursor = conn.cursor()
    
    print("\n📊 Complete Buffalo Nickel Implementation Summary")
    print("=" * 60)
    
    # Total counts
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL"')
    total = cursor.fetchone()[0]
    print(f"Total variants: {total}")
    
    # Major variants
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL" AND is_major_variant = 1')
    major = cursor.fetchone()[0]
    print(f"Major variants: {major}")
    
    # Key dates
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL" AND key_date_status = "key"')
    keys = cursor.fetchone()[0]
    print(f"Key dates: {keys}")
    
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL" AND key_date_status = "semi-key"')
    semi_keys = cursor.fetchone()[0]
    print(f"Semi-key dates: {semi_keys}")
    
    # Years covered
    cursor.execute('SELECT COUNT(DISTINCT year) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL"')
    years = cursor.fetchone()[0]
    print(f"Years covered: {years}")
    
    # Show key dates
    print("\n🔑 Key Dates:")
    cursor.execute('''
        SELECT variant_id, year, mint_mark, mintage, key_date_status
        FROM coin_variants 
        WHERE base_type = "BUFFALO_NICKEL" 
        AND key_date_status IN ("key", "semi-key")
        AND variant_type NOT LIKE "%Proof%"
        ORDER BY year, mint_mark
    ''')
    for row in cursor.fetchall():
        mintage_str = f"{row[3]:,}" if row[3] else "N/A"
        print(f"  {row[0]}: {mintage_str} ({row[4]})")
    
    # Show special varieties
    print("\n🌟 Special Varieties:")
    cursor.execute('''
        SELECT variant_id, variant_type, year
        FROM coin_variants 
        WHERE base_type = "BUFFALO_NICKEL" 
        AND (variant_type LIKE "%Overdate%" 
             OR variant_type LIKE "%Doubled Die%" 
             OR variant_type LIKE "%Legged%")
        ORDER BY year
    ''')
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} ({row[2]})")
    
    # Sample mintage data
    print("\n📈 Sample Mintage Data (1926 - Key Date Year):")
    cursor.execute('''
        SELECT variant_id, mintage, key_date_status
        FROM coin_variants 
        WHERE base_type = "BUFFALO_NICKEL" 
        AND year = 1926
        ORDER BY mint_mark
    ''')
    for row in cursor.fetchall():
        mintage_str = f"{row[1]:,}" if row[1] else "N/A"
        status = f" ({row[2]})" if row[2] != 'common' else ""
        print(f"  {row[0]}: {mintage_str}{status}")

def main():
    """Complete Buffalo Nickel implementation"""
    print("🦬 Implementing complete Buffalo Nickel variant system...")
    
    conn = sqlite3.connect('database/coins.db')
    
    try:
        # Clear existing and add complete set
        clear_existing_buffalo_variants(conn)
        count = add_complete_buffalo_variants(conn)
        print(f"✅ Added {count} Buffalo Nickel variants")
        
        # Verify implementation
        verify_complete_implementation(conn)
        
        # Commit changes
        conn.commit()
        print("\n✅ Complete Buffalo Nickel implementation successful!")
        print("   Issue #55 resolved with full production data and variants")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()