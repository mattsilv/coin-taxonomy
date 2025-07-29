#!/usr/bin/env python3
"""
Update coin IDs to use 4-letter TYPE codes
This implements the standardization proposed in GitHub Issue #7
"""

import sqlite3
import sys
from datetime import datetime
import importlib.util
import sys
import os

# Add the scripts directory to the path
sys.path.append(os.path.dirname(__file__))

# Import the mapping
spec = importlib.util.spec_from_file_location("mapping", os.path.join(os.path.dirname(__file__), "4letter_mapping.py"))
mapping_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mapping_module)
TYPE_MAPPING = mapping_module.TYPE_MAPPING

def backup_database():
    """Create a backup before making changes"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/coins_backup_4letter_{timestamp}.db"
    
    import shutil
    shutil.copy2("database/coins.db", backup_path)
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path

def update_coin_ids():
    """Update all coin IDs to use 4-letter TYPE codes"""
    conn = sqlite3.connect("database/coins.db")
    cursor = conn.cursor()
    
    # Get all current coin IDs
    cursor.execute("SELECT coin_id FROM coins ORDER BY coin_id")
    all_coins = cursor.fetchall()
    
    print(f"Found {len(all_coins)} coins to update")
    
    updates_made = 0
    
    for (old_coin_id,) in all_coins:
        # Parse the coin ID: US-TYPE-YEAR-MINT
        parts = old_coin_id.split('-')
        if len(parts) != 4:
            print(f"⚠️  Skipping malformed coin_id: {old_coin_id}")
            continue
            
        country, old_type, year, mint = parts
        
        if old_type in TYPE_MAPPING:
            new_type = TYPE_MAPPING[old_type]
            new_coin_id = f"{country}-{new_type}-{year}-{mint}"
            
            # Update the coin_id
            cursor.execute(
                "UPDATE coins SET coin_id = ? WHERE coin_id = ?",
                (new_coin_id, old_coin_id)
            )
            
            print(f"  {old_coin_id} → {new_coin_id}")
            updates_made += 1
        else:
            print(f"⚠️  No mapping found for TYPE: {old_type} in {old_coin_id}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updates_made} coin IDs to 4-letter format")
    return updates_made

def verify_updates():
    """Verify all updates were applied correctly"""
    conn = sqlite3.connect("database/coins.db")
    cursor = conn.cursor()
    
    # Check TYPE code lengths
    cursor.execute("""
        SELECT 
            substr(coin_id, 4, instr(substr(coin_id, 4), '-') - 1) as type_code,
            COUNT(*) as count
        FROM coins 
        GROUP BY type_code 
        ORDER BY type_code
    """)
    
    type_codes = cursor.fetchall()
    
    print("\n=== VERIFICATION ===")
    print("TYPE codes after update:")
    
    all_4_letter = True
    for type_code, count in type_codes:
        length = len(type_code)
        status = "✅" if length == 4 else "❌"
        print(f"  {status} {type_code} ({length} chars): {count} coins")
        
        if length != 4:
            all_4_letter = False
    
    if all_4_letter:
        print("\n✅ All TYPE codes are now 4 letters!")
    else:
        print("\n❌ Some TYPE codes are not 4 letters!")
        
    conn.close()
    return all_4_letter

def main():
    print("=== 4-LETTER TYPE CODE STANDARDIZATION ===")
    print("This script will update all coin IDs to use 4-letter TYPE codes")
    print("Based on GitHub Issue #7 proposal\n")
    
    # Backup database
    backup_path = backup_database()
    
    try:
        # Apply updates
        updates_made = update_coin_ids()
        
        # Verify results
        success = verify_updates()
        
        if success and updates_made > 0:
            print(f"\n🎉 SUCCESS: All {updates_made} coin IDs updated to 4-letter format!")
            print(f"📁 Backup available at: {backup_path}")
            return 0
        else:
            print(f"\n❌ FAILURE: Update did not complete successfully")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERROR during update: {e}")
        print(f"💾 Database backup available at: {backup_path}")
        return 1

if __name__ == "__main__":
    sys.exit(main())