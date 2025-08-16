#!/usr/bin/env python3
"""
Fix Kennedy Half Dollar JSON fields to proper array format.
"""

import sqlite3
import json

DATABASE_PATH = 'database/coins.db'

def fix_kennedy_json_fields():
    """Fix JSON fields for Kennedy Half Dollars."""
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get all Kennedy Half Dollar entries
    cursor.execute("""
        SELECT coin_id, distinguishing_features, identification_keywords, common_names
        FROM coins 
        WHERE coin_id LIKE 'US-KHDO-%'
    """)
    
    kennedy_entries = cursor.fetchall()
    
    for coin_id, features, keywords, names in kennedy_entries:
        # Convert string fields to JSON arrays
        features_array = [f.strip() for f in features.split(',') if f.strip()] if features else []
        keywords_array = [k.strip() for k in keywords.split(',') if k.strip()] if keywords else []
        names_array = [n.strip() for n in names.split(',') if n.strip()] if names else []
        
        # Update the database
        cursor.execute("""
            UPDATE coins 
            SET distinguishing_features = ?,
                identification_keywords = ?,
                common_names = ?
            WHERE coin_id = ?
        """, (
            json.dumps(features_array),
            json.dumps(keywords_array), 
            json.dumps(names_array),
            coin_id
        ))
        
        print(f"✓ Fixed JSON fields for {coin_id}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Fixed JSON formatting for {len(kennedy_entries)} Kennedy Half Dollar entries")

if __name__ == '__main__':
    fix_kennedy_json_fields()