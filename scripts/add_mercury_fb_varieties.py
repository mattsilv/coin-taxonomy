#!/usr/bin/env python3
"""
Add Mercury Dime Full Bands (FB) varieties for accurate price tracking.
Based on research from GitHub issue #24 and #25.

FB Criteria (from research):
- Full separation with recessed area on center bands
- Top and bottom bands separated  
- No bridging/interruptions/marks
- PCGS allows AU50 FB for 1916-D and 1942/1, 1942/1-D exceptions
- Otherwise MS60+ for FB designation

Priority dates: 1916-D, 1921, 1926-S, 1931-D, 1942/1 overdates, 1945-P
"""

import sqlite3
import json
import sys
import os
from datetime import datetime

def backup_database(db_path):
    """Create backup before making changes"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/coins_mercury_fb_backup_{timestamp}.db"
    
    os.makedirs("backups", exist_ok=True)
    
    with sqlite3.connect(db_path) as source:
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)
    
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path

def get_mercury_inventory(conn):
    """Get current Mercury dime inventory"""
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT coin_id, year, mint, business_strikes, varieties, notes
        FROM coins 
        WHERE series_name LIKE '%Mercury%'
        ORDER BY year, mint
    ''')
    
    mercury_coins = cursor.fetchall()
    print(f"\n🔍 Mercury Dime inventory ({len(mercury_coins)} coins):")
    
    priority_dates = ['1916-D', '1921', '1926-S', '1931-D', '1942', '1945-P']
    
    for coin in mercury_coins:
        coin_id, year, mint, mintage, varieties, notes = coin
        date_mint = f"{year}-{mint}"
        is_priority = any(priority in date_mint for priority in priority_dates)
        priority_mark = "🎯" if is_priority else "📍"
        
        print(f"  {priority_mark} {coin_id}: {year}-{mint} ({mintage:,} minted)")
        if notes:
            print(f"    📝 {notes}")
        
        # Check for existing varieties
        if varieties and varieties != '[]':
            try:
                varieties_data = json.loads(varieties)
                for variety in varieties_data:
                    print(f"    🔸 {variety.get('name', 'Unknown')} - {variety.get('description', 'No description')}")
            except json.JSONDecodeError:
                print(f"    ❌ Invalid JSON in varieties")
    
    return mercury_coins

def create_fb_variety_record(conn, original_coin_data, columns):
    """Create FB variety record for a Mercury dime"""
    cursor = conn.cursor()
    
    # Create FB variety data
    fb_data = original_coin_data.copy()
    fb_data['coin_id'] = original_coin_data['coin_id'] + '-FB'
    fb_data['variety_suffix'] = 'FB'
    fb_data['varieties'] = '[]'  # Clear varieties since this IS the FB variety
    
    # Update notes with FB description
    original_notes = fb_data.get('notes', '')
    fb_data['notes'] = f"Full Bands variety - {original_notes}" if original_notes else "Full Bands variety"
    
    # Add FB identification criteria
    fb_criteria = [
        "Full separation with recessed area on center bands",
        "Top and bottom bands separated", 
        "No bridging, interruptions, or contact marks",
        "Requires MS60+ (AU50+ for 1916-D and 1942/1 exceptions)"
    ]
    fb_data['distinguishing_features'] = json.dumps(fb_criteria)
    
    # Check if FB record already exists
    cursor.execute('SELECT coin_id FROM coins WHERE coin_id = ?', (fb_data['coin_id'],))
    if cursor.fetchone():
        print(f"ℹ️  FB record already exists: {fb_data['coin_id']}")
        return True
    
    # Insert FB variety record
    placeholders = ', '.join(['?' for _ in columns])
    insert_sql = f"INSERT INTO coins ({', '.join(columns)}) VALUES ({placeholders})"
    
    try:
        cursor.execute(insert_sql, [fb_data[col] for col in columns])
        print(f"✅ Created FB variety: {fb_data['coin_id']}")
        return True
    except Exception as e:
        print(f"❌ Error creating FB record for {fb_data['coin_id']}: {e}")
        return False

def add_fb_varieties_priority_dates(conn):
    """Add FB varieties for priority Mercury dime dates"""
    cursor = conn.cursor()
    
    # Get column names
    cursor.execute("PRAGMA table_info(coins)")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Priority dates based on research
    priority_conditions = [
        "coin_id = 'US-MERC-1916-D'",  # King of Mercury dimes
        "coin_id LIKE 'US-MERC-1921%'",  # Both P and D are semi-keys
        "coin_id = 'US-MERC-1926-S'",  # Notorious for weak strikes
        "coin_id LIKE 'US-MERC-1931%'",  # Depression era keys
        "coin_id LIKE 'US-MERC-1942%' AND varieties LIKE '%Overdate%'",  # 1942/1 overdates
        "coin_id = 'US-MERC-1945-P'"   # Extreme FB rarity per research
    ]
    
    print("\n🔄 Adding FB varieties for priority dates...")
    success_count = 0
    
    for condition in priority_conditions:
        cursor.execute(f'''
            SELECT * FROM coins 
            WHERE series_name LIKE '%Mercury%' AND ({condition})
        ''')
        
        matching_coins = cursor.fetchall()
        
        for coin_record in matching_coins:
            # Create dictionary of coin data
            coin_data = dict(zip(columns, coin_record))
            coin_id = coin_data['coin_id']
            
            print(f"\n📍 Processing: {coin_id}")
            print(f"   Mintage: {coin_data['business_strikes']:,}")
            print(f"   Notes: {coin_data.get('notes', 'None')}")
            
            # Create FB variety
            if create_fb_variety_record(conn, coin_data, columns):
                success_count += 1
    
    print(f"\n✅ Created {success_count} FB variety records")
    return success_count > 0

def add_fb_varieties_remaining_dates(conn):
    """Add FB varieties for remaining Mercury dime dates"""
    cursor = conn.cursor()
    
    # Get column names
    cursor.execute("PRAGMA table_info(coins)")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Get all Mercury dimes that don't have FB varieties yet
    cursor.execute('''
        SELECT * FROM coins 
        WHERE series_name LIKE '%Mercury%' 
        AND coin_id NOT IN (
            SELECT REPLACE(coin_id, '-FB', '') 
            FROM coins 
            WHERE coin_id LIKE '%-FB'
        )
    ''')
    
    remaining_coins = cursor.fetchall()
    
    print(f"\n🔄 Adding FB varieties for remaining {len(remaining_coins)} dates...")
    success_count = 0
    
    for coin_record in remaining_coins:
        # Create dictionary of coin data
        coin_data = dict(zip(columns, coin_record))
        coin_id = coin_data['coin_id']
        
        print(f"\n📍 Processing: {coin_id}")
        
        # Create FB variety
        if create_fb_variety_record(conn, coin_data, columns):
            success_count += 1
    
    print(f"\n✅ Created {success_count} additional FB variety records")
    return success_count > 0

def verify_mercury_fb_implementation(conn):
    """Verify Mercury FB varieties were created successfully"""
    cursor = conn.cursor()
    
    print("\n🔍 Verifying Mercury FB implementation:")
    
    # Get all Mercury dimes including FB varieties
    cursor.execute('''
        SELECT coin_id, year, mint, business_strikes, variety_suffix, notes
        FROM coins 
        WHERE series_name LIKE '%Mercury%'
        ORDER BY year, mint, variety_suffix
    ''')
    
    results = cursor.fetchall()
    regular_count = 0
    fb_count = 0
    
    print(f"\n📊 Mercury Dime varieties ({len(results)} total):")
    
    current_date = None
    for coin_id, year, mint, mintage, suffix, notes in results:
        date_mint = f"{year}-{mint}"
        
        if date_mint != current_date:
            if current_date:
                print()  # Blank line between dates
            current_date = date_mint
            print(f"  📅 {date_mint}:")
        
        if suffix == 'FB':
            fb_count += 1
            print(f"    🔸 {coin_id} (FB variety)")
            print(f"      Notes: {notes[:60]}...")
        else:
            regular_count += 1
            print(f"    📍 {coin_id} (Regular)")
            if mintage:
                print(f"      Mintage: {mintage:,}")
    
    print(f"\n📊 Summary:")
    print(f"  Regular Mercury dimes: {regular_count}")
    print(f"  FB varieties: {fb_count}")
    print(f"  Total Mercury records: {len(results)}")
    
    # Check for FB coverage
    cursor.execute('''
        SELECT 
            COUNT(CASE WHEN variety_suffix = '' OR variety_suffix IS NULL THEN 1 END) as regular,
            COUNT(CASE WHEN variety_suffix = 'FB' THEN 1 END) as fb
        FROM coins 
        WHERE series_name LIKE '%Mercury%'
    ''')
    
    regular_final, fb_final = cursor.fetchone()
    coverage_percent = (fb_final / regular_final * 100) if regular_final > 0 else 0
    
    print(f"\n📈 FB Coverage:")
    print(f"  Regular dates: {regular_final}")
    print(f"  FB varieties: {fb_final}")
    print(f"  Coverage: {coverage_percent:.1f}%")
    
    return len(results) > 0 and fb_count > 0

def get_database_stats(conn):
    """Get current database statistics"""
    cursor = conn.cursor()
    
    stats = cursor.execute('''
        SELECT 
            COUNT(*) as total_coins,
            COUNT(CASE WHEN variety_suffix != '' AND variety_suffix IS NOT NULL THEN 1 END) as coins_with_suffix,
            COUNT(CASE WHEN series_name LIKE '%Mercury%' THEN 1 END) as mercury_coins,
            COUNT(CASE WHEN variety_suffix = 'FB' THEN 1 END) as fb_varieties
        FROM coins
    ''').fetchone()
    
    print(f"\n📊 Database Statistics:")
    print(f"  Total coins: {stats[0]}")
    print(f"  Coins with variety suffix: {stats[1]}")
    print(f"  Mercury dimes: {stats[2]}")
    print(f"  FB varieties: {stats[3]}")
    
    return stats

def main():
    """Main execution function"""
    db_path = "database/coins.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        sys.exit(1)
    
    print("🚀 Adding Mercury Dime Full Bands (FB) varieties")
    print("📚 Research source: https://github.com/mattsilv/coin-taxonomy/issues/24")
    print("🎯 Target dates: 1916-D, 1921, 1926-S, 1931-D, 1942/1, 1945-P")
    print("=" * 70)
    
    backup_path = backup_database(db_path)
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            
            # Get initial stats and inventory
            get_database_stats(conn)
            get_mercury_inventory(conn)
            
            # Add FB varieties for priority dates first
            success1 = add_fb_varieties_priority_dates(conn)
            
            if success1:
                # Add FB varieties for remaining dates
                success2 = add_fb_varieties_remaining_dates(conn)
                
                if success2:
                    # Verify implementation
                    verify_mercury_fb_implementation(conn)
                    
                    # Get final stats
                    get_database_stats(conn)
                    
                    conn.commit()
                    print("\n✅ Mercury Dime FB varieties added successfully!")
                    print("\nPrice tracking benefits:")
                    print("- US-MERC-1916-D vs US-MERC-1916-D-FB (4-8x premium)")
                    print("- US-MERC-1921-P vs US-MERC-1921-P-FB (significant premium)")
                    print("- US-MERC-1945-P vs US-MERC-1945-P-FB (extreme rarity)")
                    print("\nNext steps:")
                    print("1. Test JSON exports include FB suffixes")
                    print("2. Collect specific FB price premium data (Issue #25)")
                    print("3. Implement Jefferson nickel Full Steps varieties")
                else:
                    print("\n❌ Failed to add FB varieties for remaining dates")
                    sys.exit(1)
            else:
                print("\n❌ Failed to add FB varieties for priority dates")
                sys.exit(1)
                
    except Exception as e:
        print(f"\n❌ Error adding Mercury FB varieties: {e}")
        print(f"Database backup available at: {backup_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()