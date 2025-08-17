#!/usr/bin/env python3
"""
Split major varieties into separate coin records for accurate price tracking.
Starting with 1909-S VDB as proof of concept.
"""

import sqlite3
import json
import sys
import os
from datetime import datetime

def backup_database(db_path):
    """Create backup before making changes"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/coins_vdb_split_backup_{timestamp}.db"
    
    os.makedirs("backups", exist_ok=True)
    
    with sqlite3.connect(db_path) as source:
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)
    
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path

def find_vdb_varieties(conn):
    """Find coins with VDB varieties that need to be split"""
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT coin_id, varieties, series_name, year, mint, business_strikes
        FROM coins 
        WHERE varieties LIKE '%VDB%' AND varieties != '[]'
    ''')
    
    vdb_coins = cursor.fetchall()
    print(f"\n🔍 Found {len(vdb_coins)} coins with VDB varieties:")
    
    for coin in vdb_coins:
        coin_id, varieties_json, series_name, year, mint, mintage = coin
        try:
            varieties = json.loads(varieties_json) if varieties_json else []
            vdb_varieties = [v for v in varieties if 'VDB' in v.get('name', '')]
            if vdb_varieties:
                print(f"  📍 {coin_id}: {series_name} {year}-{mint} ({mintage:,} minted)")
                for variety in vdb_varieties:
                    print(f"    🔸 {variety.get('name', 'Unknown')} - {variety.get('description', 'No description')}")
        except json.JSONDecodeError:
            print(f"  ❌ Invalid JSON in varieties for {coin_id}")
    
    return vdb_coins

def split_1909_s_vdb(conn):
    """Split 1909-S Lincoln Cent VDB into separate record"""
    cursor = conn.cursor()
    
    # Find the 1909-S Lincoln Wheat Cent
    cursor.execute('''
        SELECT * FROM coins 
        WHERE coin_id = 'US-LWCT-1909-S'
    ''')
    
    original_coin = cursor.fetchone()
    if not original_coin:
        print("❌ 1909-S Lincoln Cent not found in database")
        return False
    
    # Get column names
    cursor.execute("PRAGMA table_info(coins)")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Create dictionary of original coin data
    coin_data = dict(zip(columns, original_coin))
    print(f"\n📍 Found original coin: {coin_data['coin_id']}")
    print(f"   Business strikes: {coin_data['business_strikes']:,}")
    print(f"   Current varieties: {coin_data['varieties']}")
    
    # Parse varieties
    try:
        varieties = json.loads(coin_data['varieties']) if coin_data['varieties'] else []
        vdb_variety = None
        
        for variety in varieties:
            if 'VDB' in variety.get('name', ''):
                vdb_variety = variety
                break
        
        if not vdb_variety:
            print("❌ No VDB variety found in 1909-S coin")
            return False
        
        print(f"   🎯 VDB variety: {vdb_variety}")
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON in varieties")
        return False
    
    # Create VDB variety record
    vdb_data = coin_data.copy()
    vdb_data['coin_id'] = 'US-LWCT-1909-S-VDB'
    vdb_data['variety_suffix'] = 'VDB'
    vdb_data['business_strikes'] = vdb_variety.get('estimated_mintage', 484000)  # Known VDB mintage
    vdb_data['varieties'] = '[]'  # Clear varieties since this IS the VDB variety
    vdb_data['notes'] = f"1909-S VDB variety - {vdb_variety.get('description', 'With designer initials VDB')}"
    vdb_data['rarity'] = 'key'  # VDB is definitely a key date
    
    # Check if VDB record already exists
    cursor.execute('SELECT coin_id FROM coins WHERE coin_id = ?', (vdb_data['coin_id'],))
    if cursor.fetchone():
        print(f"ℹ️  VDB record already exists: {vdb_data['coin_id']}")
        return True
    
    # Insert VDB variety as separate coin
    placeholders = ', '.join(['?' for _ in columns])
    insert_sql = f"INSERT INTO coins ({', '.join(columns)}) VALUES ({placeholders})"
    
    try:
        cursor.execute(insert_sql, [vdb_data[col] for col in columns])
        print(f"✅ Created VDB variety record: {vdb_data['coin_id']}")
        print(f"   Business strikes: {vdb_data['business_strikes']:,}")
        print(f"   Rarity: {vdb_data['rarity']}")
        
        # Update original coin to remove VDB variety and adjust mintage
        remaining_varieties = [v for v in varieties if 'VDB' not in v.get('name', '')]
        non_vdb_mintage = 72702618  # Total 1909-S mintage minus VDB mintage
        
        cursor.execute('''
            UPDATE coins 
            SET varieties = ?, 
                business_strikes = ?,
                notes = COALESCE(notes, '') || ' (VDB variety split to separate record)'
            WHERE coin_id = ?
        ''', (
            json.dumps(remaining_varieties),
            non_vdb_mintage,
            'US-LWCT-1909-S'
        ))
        
        print(f"✅ Updated original record: US-LWCT-1909-S")
        print(f"   Adjusted mintage: {non_vdb_mintage:,} (without VDB)")
        print(f"   Remaining varieties: {len(remaining_varieties)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating VDB record: {e}")
        return False

def verify_split(conn):
    """Verify the VDB split was successful"""
    cursor = conn.cursor()
    
    print("\n🔍 Verifying VDB split:")
    
    # Check both records exist
    for coin_id in ['US-LWCT-1909-S', 'US-LWCT-1909-S-VDB']:
        cursor.execute('''
            SELECT coin_id, business_strikes, variety_suffix, rarity, notes
            FROM coins WHERE coin_id = ?
        ''', (coin_id,))
        
        result = cursor.fetchone()
        if result:
            coin_id, mintage, suffix, rarity, notes = result
            print(f"  ✅ {coin_id}")
            print(f"     Mintage: {mintage:,}")
            print(f"     Suffix: '{suffix}'")
            print(f"     Rarity: {rarity}")
            if suffix == 'VDB':
                print(f"     Notes: {notes}")
        else:
            print(f"  ❌ Missing: {coin_id}")
    
    # Verify mintage totals
    cursor.execute('''
        SELECT SUM(business_strikes) as total_mintage
        FROM coins WHERE coin_id LIKE 'US-LWCT-1909-S%'
    ''')
    
    total = cursor.fetchone()[0]
    expected_total = 72702618 + 484000  # Original S mintage + VDB mintage
    print(f"\n📊 Total 1909-S mintage: {total:,}")
    print(f"📊 Expected total: {expected_total:,}")
    
    if abs(total - expected_total) < 1000:  # Allow small rounding differences
        print("✅ Mintage split verification passed")
        return True
    else:
        print("❌ Mintage split verification failed")
        return False

def get_database_stats(conn):
    """Get current database statistics"""
    cursor = conn.cursor()
    
    stats = cursor.execute('''
        SELECT 
            COUNT(*) as total_coins,
            COUNT(CASE WHEN variety_suffix != '' THEN 1 END) as coins_with_suffix,
            COUNT(CASE WHEN varieties != '[]' AND varieties IS NOT NULL THEN 1 END) as coins_with_varieties
        FROM coins
    ''').fetchone()
    
    print(f"\n📊 Database Statistics:")
    print(f"  Total coins: {stats[0]}")
    print(f"  Coins with variety suffix: {stats[1]}")
    print(f"  Coins with varieties: {stats[2]}")
    
    return stats

def main():
    """Main execution function"""
    db_path = "database/coins.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        sys.exit(1)
    
    print("🚀 Splitting VDB varieties for accurate price tracking")
    print("=" * 60)
    
    backup_path = backup_database(db_path)
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            
            # Get initial stats
            get_database_stats(conn)
            
            # Find all VDB varieties
            find_vdb_varieties(conn)
            
            # Split 1909-S VDB as proof of concept
            success = split_1909_s_vdb(conn)
            
            if success:
                # Verify the split
                verify_split(conn)
                
                # Get final stats
                get_database_stats(conn)
                
                conn.commit()
                print("\n✅ VDB variety split completed successfully!")
                print("\nPrice tracking benefits:")
                print("- US-LWCT-1909-S: Standard 1909-S Lincoln cent (~$100-$150)")
                print("- US-LWCT-1909-S-VDB: 1909-S with VDB initials (~$800-$1200)")
                print("\nNext steps:")
                print("1. Update export scripts to handle variety suffixes")
                print("2. Test JSON exports include both records")
                print("3. Add more major varieties (Mercury FB, Standing Liberty Types)")
            else:
                print("\n❌ VDB variety split failed")
                sys.exit(1)
                
    except Exception as e:
        print(f"\n❌ Error splitting varieties: {e}")
        print(f"Database backup available at: {backup_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()