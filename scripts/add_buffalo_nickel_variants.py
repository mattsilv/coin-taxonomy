#!/usr/bin/env python3
"""
Migration script to add Buffalo Nickel variants to coin_variants table.
Issue #55: Add Buffalo Nickel variants to tracking system

Buffalo Nickels have two major types:
- Type 1 (1913 only): 5 CENTS on raised ground
- Type 2 (1913-1938): 5 CENTS in recess

Plus special varieties like overdates and the famous three-legged buffalo.
"""

import sqlite3
from datetime import datetime

def add_buffalo_variants(conn):
    """Add Buffalo Nickel variants to the database"""
    
    buffalo_variants = []
    
    # 1913 Type 1 (Raised Ground) - Major variants
    for mint in ['P', 'D', 'S']:
        mint_suffix = '' if mint == 'P' else f'-{mint}'
        buffalo_variants.append({
            'variant_id': f'US-BUFF-1913-{mint}-T1',
            'base_type': 'BUFFALO_NICKEL',
            'denomination': '5 cents',
            'series_name': 'Buffalo Nickel',
            'year': 1913,
            'mint_mark': mint,
            'variant_type': 'Type 1 - Raised Ground',
            'variant_description': f'1913{mint_suffix} Buffalo Nickel Type 1 - FIVE CENTS on raised ground',
            'sort_order': 10 if mint == 'P' else (20 if mint == 'D' else 30),
            'is_major_variant': 1,
            'notes': 'First year of issue, Type 1 design with denomination on raised mound'
        })
    
    # 1913 Type 2 (Recessed) - Major variants for transition year
    for mint in ['P', 'D', 'S']:
        mint_suffix = '' if mint == 'P' else f'-{mint}'
        buffalo_variants.append({
            'variant_id': f'US-BUFF-1913-{mint}-T2',
            'base_type': 'BUFFALO_NICKEL',
            'denomination': '5 cents',
            'series_name': 'Buffalo Nickel',
            'year': 1913,
            'mint_mark': mint,
            'variant_type': 'Type 2 - Recessed',
            'variant_description': f'1913{mint_suffix} Buffalo Nickel Type 2 - FIVE CENTS in recess',
            'sort_order': 40 if mint == 'P' else (50 if mint == 'D' else 60),
            'is_major_variant': 1,
            'notes': 'Mid-year design change, Type 2 with recessed denomination'
        })
    
    # Special overdate varieties (Major variants)
    special_varieties = [
        {
            'variant_id': 'US-BUFF-1914-P-4OVER3',
            'year': 1914,
            'mint_mark': 'P',
            'variant_type': '1914/3 Overdate',
            'variant_description': '1914 Buffalo Nickel with 4 over 3 overdate variety',
            'sort_order': 15,
            'is_major_variant': 1,
            'notes': 'Scarce overdate variety where 4 is punched over 3'
        },
        {
            'variant_id': 'US-BUFF-1918-D-8OVER7',
            'year': 1918,
            'mint_mark': 'D',
            'variant_type': '1918/7-D Overdate',
            'variant_description': '1918-D Buffalo Nickel with 8 over 7 overdate variety',
            'sort_order': 25,
            'is_major_variant': 1,
            'notes': 'Popular overdate variety where 8 is punched over 7'
        },
        {
            'variant_id': 'US-BUFF-1937-D-3LEG',
            'year': 1937,
            'mint_mark': 'D',
            'variant_type': 'Three-Legged Buffalo',
            'variant_description': '1937-D Buffalo Nickel Three-Legged variety - missing front leg',
            'sort_order': 25,
            'is_major_variant': 1,
            'notes': 'Famous error variety caused by over-polishing of die removing buffalo\'s front leg'
        }
    ]
    
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
            'notes': variety['notes']
        })
    
    # Regular Type 2 business strikes for selected years (1914-1938)
    # Adding a representative sample - full implementation would include all years
    sample_years = [
        (1914, ['P', 'D', 'S']),
        (1915, ['P', 'D', 'S']),
        (1916, ['P', 'D', 'S']),
        (1917, ['P', 'D', 'S']),
        (1918, ['P', 'D', 'S']),
        (1919, ['P', 'D', 'S']),
        (1920, ['P', 'D', 'S']),
        (1921, ['P', 'S']),  # No Denver mint this year
        (1925, ['P', 'D', 'S']),
        (1926, ['P', 'D', 'S']),
        (1930, ['P', 'S']),  # No Denver mint this year
        (1935, ['P', 'D', 'S']),
        (1936, ['P', 'D', 'S']),
        (1937, ['P', 'D', 'S']),
        (1938, ['D'])  # Final year, Denver only
    ]
    
    for year, mints in sample_years:
        for i, mint in enumerate(mints):
            mint_suffix = '' if mint == 'P' else f'-{mint}'
            
            # Skip if this is a special variety we already added
            if (year == 1914 and mint == 'P') or (year == 1918 and mint == 'D') or (year == 1937 and mint == 'D'):
                # Still add regular strike alongside the overdate/error
                buffalo_variants.append({
                    'variant_id': f'US-BUFF-{year}-{mint}',
                    'base_type': 'BUFFALO_NICKEL',
                    'denomination': '5 cents',
                    'series_name': 'Buffalo Nickel',
                    'year': year,
                    'mint_mark': mint,
                    'variant_type': 'Type 2 - Business Strike',
                    'variant_description': f'{year}{mint_suffix} Buffalo Nickel Type 2 regular business strike',
                    'sort_order': 10 + (i * 10),
                    'is_major_variant': 0,
                    'notes': None
                })
            else:
                buffalo_variants.append({
                    'variant_id': f'US-BUFF-{year}-{mint}',
                    'base_type': 'BUFFALO_NICKEL',
                    'denomination': '5 cents',
                    'series_name': 'Buffalo Nickel',
                    'year': year,
                    'mint_mark': mint,
                    'variant_type': 'Type 2 - Business Strike',
                    'variant_description': f'{year}{mint_suffix} Buffalo Nickel Type 2 regular business strike',
                    'sort_order': 10 + (i * 10),
                    'is_major_variant': 0,
                    'notes': None
                })
    
    # Insert all variants
    for variant in buffalo_variants:
        conn.execute('''
            INSERT OR REPLACE INTO coin_variants (
                variant_id, base_type, denomination, series_name, year, mint_mark,
                variant_type, variant_description, sort_order, is_major_variant, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            variant['notes']
        ))

def verify_buffalo_variants(conn):
    """Verify Buffalo Nickel variants were added correctly"""
    cursor = conn.cursor()
    
    # Count total variants
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL"')
    total_count = cursor.fetchone()[0]
    
    # Count major variants
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL" AND is_major_variant = 1')
    major_count = cursor.fetchone()[0]
    
    # Count Type 1 vs Type 2
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL" AND variant_type LIKE "%Type 1%"')
    type1_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "BUFFALO_NICKEL" AND variant_type LIKE "%Type 2%"')
    type2_count = cursor.fetchone()[0]
    
    print(f"✅ Added {total_count} total Buffalo Nickel variants")
    print(f"   - {major_count} major variants")
    print(f"   - {type1_count} Type 1 (Raised Ground) variants")
    print(f"   - {type2_count} Type 2 (Recessed) variants")
    
    # Show 1913 variants (both types)
    print("\n📊 1913 Buffalo Nickel variants (Type 1 & Type 2):")
    cursor.execute('''
        SELECT variant_id, variant_type, mint_mark
        FROM coin_variants
        WHERE base_type = "BUFFALO_NICKEL" AND year = 1913
        ORDER BY sort_order
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]} (Mint: {row[2]})")
    
    # Show special varieties
    print("\n🌟 Special varieties:")
    cursor.execute('''
        SELECT variant_id, variant_type, year
        FROM coin_variants
        WHERE base_type = "BUFFALO_NICKEL" 
        AND (variant_type LIKE "%Overdate%" OR variant_type LIKE "%Three-Legged%")
        ORDER BY year
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]} ({row[2]})")

def main():
    """Run migration"""
    print("🔄 Running migration: Adding Buffalo Nickel variants...")
    
    # Connect to database (using database/coins.db where coin_variants table exists)
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    try:
        # Add Buffalo Nickel variants
        add_buffalo_variants(conn)
        print("✅ Populated Buffalo Nickel variants")
        
        # Verify the data
        verify_buffalo_variants(conn)
        
        # Commit changes
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()