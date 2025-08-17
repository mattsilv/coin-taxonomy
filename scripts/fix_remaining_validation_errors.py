#!/usr/bin/env python3
"""
Fix remaining validation errors in the database.
"""

import sqlite3
import json
import os

def main():
    print("🔧 Fixing remaining validation errors...")
    
    db_path = "database/coins.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Fix 1: Remove coin with SMS mint mark
        print("🔧 Fixing SMS mint mark (should be removed)...")
        cursor.execute("DELETE FROM coins WHERE coin_id LIKE '%-SMS'")
        deleted_count = cursor.rowcount
        print(f"  ✅ Removed {deleted_count} coins with SMS mint mark")
        
        # Fix 2: Fix varieties field that contains strings instead of JSON
        print("🔧 Fixing varieties field format...")
        cursor.execute("""
            SELECT coin_id, varieties 
            FROM coins 
            WHERE varieties IS NOT NULL 
            AND varieties != '[]' 
            AND varieties != ''
        """)
        
        coins_with_varieties = cursor.fetchall()
        
        for coin_id, varieties in coins_with_varieties:
            # If varieties is a string, convert to proper JSON array
            if isinstance(varieties, str) and not varieties.startswith('['):
                # Create a proper variety object
                variety_obj = [{
                    "variety_id": f"{coin_id}-V1",
                    "name": varieties.strip(),
                    "description": varieties.strip()
                }]
                
                cursor.execute("""
                    UPDATE coins 
                    SET varieties = ?
                    WHERE coin_id = ?
                """, (json.dumps(variety_obj), coin_id))
                
                print(f"  ✅ Fixed varieties for {coin_id}")
        
        # Commit changes
        conn.commit()
        print("✅ Successfully fixed remaining validation errors")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()