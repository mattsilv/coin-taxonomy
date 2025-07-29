#!/usr/bin/env python3
"""
Update issues table to use 4-letter TYPE codes
"""

import sqlite3
import sys
from datetime import datetime

# 4-letter TYPE mapping from our previous work
TYPE_MAPPING = {
    'IHC': 'INCH',  # Indian Head Cent
    'LWC': 'LWCT',  # Lincoln Wheat Cent
    'LMC': 'LMCT',  # Lincoln Memorial Cent
    'LBC': 'LBCT',  # Lincoln Bicentennial Cent
    'LSC': 'LSCT',  # Lincoln Shield Cent
    'SN': 'SHLD',   # Shield Nickel
    'LHN': 'LHNI',  # Liberty Head Nickel
    'BN': 'BUFF',   # Buffalo Nickel
    'JN': 'JEFF',   # Jefferson Nickel
    'BD': 'BARD',   # Barber Dime
    'WHD': 'MERC',  # Mercury Dime (Winged Liberty Head)
    'RD': 'ROOS',   # Roosevelt Dime
    'BQ': 'BARQ',   # Barber Quarter
    'SLQ': 'SLIQ',  # Standing Liberty Quarter
    'WQ': 'WASH',   # Washington Quarter
    'MD': 'MORG',   # Morgan Dollar
    'PD': 'PEAC',   # Peace Dollar
    'ED': 'EISE',   # Eisenhower Dollar
    'SBA': 'SANT',  # Susan B. Anthony Dollar
    'SAC': 'SACA'   # Sacagawea Dollar
}

def update_issues_table():
    """Update issues table issue_id to use 4-letter TYPE codes"""
    
    conn = sqlite3.connect('database/coins.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all current issue_ids
    cursor.execute('SELECT issue_id FROM issues WHERE issue_id LIKE "US-%-%-%" ORDER BY issue_id')
    issues = cursor.fetchall()
    
    print(f"Found {len(issues)} issues to potentially update")
    
    updates = []
    for issue in issues:
        old_id = issue['issue_id']
        
        # Parse the current format: US-TYPE-YEAR-MINT
        parts = old_id.split('-')
        if len(parts) != 4:
            print(f"⚠️  Skipping malformed ID: {old_id}")
            continue
            
        country, current_type, year, mint = parts
        
        # Check if we have a mapping for this type
        if current_type in TYPE_MAPPING:
            new_type = TYPE_MAPPING[current_type]
            new_id = f"{country}-{new_type}-{year}-{mint}"
            updates.append((new_id, old_id))
            print(f"  {old_id} → {new_id}")
        else:
            print(f"  No mapping for type '{current_type}' in ID: {old_id}")
    
    if not updates:
        print("No updates needed - all issue_ids already use 4-letter codes")
        return
    
    print(f"\nUpdating {len(updates)} issue IDs...")
    
    # Perform updates
    for new_id, old_id in updates:
        try:
            cursor.execute('''
                UPDATE issues 
                SET issue_id = ?, updated_at = ? 
                WHERE issue_id = ?
            ''', (new_id, datetime.now().isoformat(), old_id))
        except sqlite3.Error as e:
            print(f"❌ Error updating {old_id}: {e}")
            return False
    
    # Commit changes
    conn.commit()
    print(f"✅ Successfully updated {len(updates)} issue IDs")
    
    # Verify the changes
    cursor.execute('SELECT COUNT(*) as count FROM issues WHERE issue_id LIKE "US-%-%-%" AND LENGTH(SUBSTR(issue_id, 4, INSTR(SUBSTR(issue_id, 4), "-") - 1)) = 4')
    count_4letter = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM issues WHERE issue_id LIKE "US-%-%-%" AND LENGTH(SUBSTR(issue_id, 4, INSTR(SUBSTR(issue_id, 4), "-") - 1)) != 4')
    count_not_4letter = cursor.fetchone()['count']
    
    print(f"✅ Verification: {count_4letter} issues with 4-letter codes, {count_not_4letter} with other lengths")
    
    conn.close()
    return True

if __name__ == '__main__':
    success = update_issues_table()
    sys.exit(0 if success else 1)