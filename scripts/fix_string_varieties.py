#!/usr/bin/env python3
"""
Fix string varieties that should be JSON objects
"""

import sqlite3
import json

def fix_string_varieties():
    """Fix varieties that are stored as strings instead of JSON objects"""
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    # Find coins with varieties that are JSON arrays of strings (not objects)
    cursor.execute("""
        SELECT coin_id, varieties 
        FROM coins 
        WHERE varieties IS NOT NULL 
        AND varieties != '[]'
        AND json_valid(varieties) = 1
    """)
    
    string_varieties = cursor.fetchall()
    
    print(f"Found {len(string_varieties)} coins with string varieties")
    
    for coin_id, varieties_json in string_varieties:
        try:
            varieties_list = json.loads(varieties_json)
            # Check if this is an array of strings (not objects)
            if isinstance(varieties_list, list) and varieties_list and isinstance(varieties_list[0], str):
                print(f"Fixing {coin_id}: {varieties_list}")
                
                # Convert strings to proper JSON objects
                variety_objects = []
                for i, variety_str in enumerate(varieties_list):
                    variety_objects.append({
                        "variety_id": f"{coin_id}-V{i+1}",
                        "name": variety_str,
                        "description": variety_str
                    })
                
                # Update the database
                cursor.execute("""
                    UPDATE coins 
                    SET varieties = ? 
                    WHERE coin_id = ?
                """, (json.dumps(variety_objects), coin_id))
        except json.JSONDecodeError:
            print(f"Invalid JSON for {coin_id}: {varieties_json}")
    
    conn.commit()
    conn.close()
    
    print(f"Fixed {len(string_varieties)} string varieties")

if __name__ == "__main__":
    fix_string_varieties()