#!/usr/bin/env python3
"""
Update issues table to use proper 4-letter TYPE codes based on series_id
"""

import sqlite3
import sys
from datetime import datetime

# Map series_id to 4-letter TYPE code
SERIES_TO_TYPE = {
    # Cents
    'indian_head_cent': 'INCH',
    'lincoln_wheat_cent': 'LWCT',
    'lincoln_memorial_cent': 'LMCT',
    'lincoln_bicentennial_cent': 'LBCT',
    'lincoln_shield_cent': 'LSCT',
    
    # Nickels
    'shield_nickel': 'SHLD',
    'liberty_head_nickel': 'LHNI',
    'buffalo_nickel': 'BUFF',
    'jefferson_nickel': 'JEFF',
    
    # Dimes
    'barber_dime': 'BARD',
    'mercury_dime': 'MERC',
    'roosevelt_dime': 'ROOS',
    
    # Quarters
    'barber_quarter': 'BARQ',
    'standing_liberty_quarter': 'SLIQ',
    'washington_quarter': 'WASH',
    
    # Dollars
    'morgan_dollar': 'MORG',
    'peace_dollar': 'PEAC',
    'eisenhower_dollar': 'EISE',
    'susan_b_anthony_dollar': 'SANT',
    'sacagawea_dollar': 'SACA'
}

def update_issues_table():
    """Update issues table issue_id to use proper 4-letter TYPE codes based on series_id"""
    
    conn = sqlite3.connect('database/coins.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all current issues that need updating
    cursor.execute('''
        SELECT issue_id, series_id, issue_year, mint_id 
        FROM issues 
        WHERE issue_id LIKE "US-UNK-%-%" 
        ORDER BY issue_id
    ''')
    issues = cursor.fetchall()
    
    print(f"Found {len(issues)} issues with 'UNK' type to update")
    
    updates = []
    for issue in issues:
        old_id = issue['issue_id']
        series_id = issue['series_id']
        year = issue['issue_year']
        mint = issue['mint_id']
        
        # Get the proper type code for this series
        if series_id in SERIES_TO_TYPE:
            type_code = SERIES_TO_TYPE[series_id]
            new_id = f"US-{type_code}-{year}-{mint}"
            updates.append((new_id, old_id))
            print(f"  {old_id} → {new_id} (series: {series_id})")
        else:
            print(f"  ⚠️  No mapping for series '{series_id}' in ID: {old_id}")
    
    if not updates:
        print("No updates needed")
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
    cursor.execute('SELECT COUNT(*) as count FROM issues WHERE issue_id LIKE "US-%-%-%" AND issue_id NOT LIKE "US-UNK-%--%"')
    count_updated = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM issues WHERE issue_id LIKE "US-UNK-%--%"')
    count_remaining = cursor.fetchone()['count']
    
    print(f"✅ Verification: {count_updated} issues with proper codes, {count_remaining} still with UNK")
    
    conn.close()
    return True

if __name__ == '__main__':
    success = update_issues_table()
    sys.exit(0 if success else 1)