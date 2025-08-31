#!/usr/bin/env python3
"""
Fix corrupted variety data in the database where nested objects were stored
instead of proper string values for name and description fields.
"""

import sqlite3
import json
import sys

def fix_corrupted_varieties(db_path='database/coins.db'):
    """Fix all corrupted variety entries in the database."""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Find all coins with corrupted varieties
    cursor.execute("""
        SELECT coin_id, varieties 
        FROM coins 
        WHERE varieties LIKE '%"name": {%' 
           OR varieties LIKE '%"description": {%'
    """)
    
    corrupted_coins = cursor.fetchall()
    print(f"Found {len(corrupted_coins)} coins with corrupted varieties")
    
    fixed_count = 0
    for coin_id, varieties_json in corrupted_coins:
        try:
            varieties = json.loads(varieties_json)
            fixed_varieties = []
            
            for variety in varieties:
                fixed_variety = {}
                
                # Fix variety_id
                if 'variety_id' in variety:
                    fixed_variety['variety_id'] = variety['variety_id']
                
                # Fix name field
                if 'name' in variety:
                    if isinstance(variety['name'], dict):
                        # Take the name from the nested dict
                        if 'name' in variety['name']:
                            fixed_variety['name'] = variety['name']['name']
                        else:
                            fixed_variety['name'] = str(variety['name'])
                    else:
                        fixed_variety['name'] = variety['name']
                
                # Fix description field  
                if 'description' in variety:
                    if isinstance(variety['description'], dict):
                        # Take the description from the nested dict
                        if 'description' in variety['description']:
                            fixed_variety['description'] = variety['description']['description']
                        else:
                            fixed_variety['description'] = str(variety['description'])
                    else:
                        fixed_variety['description'] = variety['description']
                
                # Add other fields if present
                if 'estimated_mintage' in variety:
                    fixed_variety['estimated_mintage'] = variety['estimated_mintage']
                
                # Only add if we have at least variety_id
                if 'variety_id' in fixed_variety:
                    fixed_varieties.append(fixed_variety)
            
            # Update the database
            if fixed_varieties:
                cursor.execute(
                    "UPDATE coins SET varieties = ? WHERE coin_id = ?",
                    (json.dumps(fixed_varieties), coin_id)
                )
                fixed_count += 1
                print(f"Fixed: {coin_id}")
            else:
                # If no valid varieties, set to empty array
                cursor.execute(
                    "UPDATE coins SET varieties = '[]' WHERE coin_id = ?",
                    (coin_id,)
                )
                fixed_count += 1
                print(f"Cleared invalid varieties: {coin_id}")
                
        except Exception as e:
            print(f"Error fixing {coin_id}: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Fixed {fixed_count} coins with corrupted varieties")
    return fixed_count

if __name__ == "__main__":
    fixed = fix_corrupted_varieties()
    if fixed > 0:
        print("\n✓ Database updated. Run export script to regenerate JSON files:")
        print("  uv run python scripts/export_from_database.py")
        sys.exit(0)
    else:
        print("\n✓ No corrupted varieties found")
        sys.exit(0)