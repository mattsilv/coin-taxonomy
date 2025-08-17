#!/usr/bin/env python3
"""
Split Standing Liberty Quarter Type I and Type II varieties for precise taxonomic identification.
Based on comprehensive research from GitHub issue #24.

Type Timeline:
- 1916: Type I only (52,000 minted)
- 1917: Both Type I (early) and Type II (mid-year redesign)
- 1918-1930: Type II only

Research source: https://github.com/mattsilv/coin-taxonomy/issues/24
"""

import sqlite3
import json
import sys
import os
from datetime import datetime

def backup_database(db_path):
    """Create backup before making changes"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/coins_slq_split_backup_{timestamp}.db"
    
    os.makedirs("backups", exist_ok=True)
    
    with sqlite3.connect(db_path) as source:
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)
    
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path

def get_slq_inventory(conn):
    """Get current Standing Liberty Quarter inventory"""
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT coin_id, year, mint, business_strikes, varieties, notes
        FROM coins 
        WHERE series_name LIKE '%Standing Liberty%'
        ORDER BY year, mint
    ''')
    
    slq_coins = cursor.fetchall()
    print(f"\n🔍 Current Standing Liberty Quarter inventory ({len(slq_coins)} coins):")
    
    for coin in slq_coins:
        coin_id, year, mint, mintage, varieties, notes = coin
        print(f"  📍 {coin_id}: {year}-{mint} ({mintage:,} minted)")
        if varieties and varieties != '[]':
            try:
                varieties_data = json.loads(varieties)
                for variety in varieties_data:
                    print(f"    🔸 {variety.get('name', 'Unknown')} - {variety.get('description', 'No description')}")
            except json.JSONDecodeError:
                print(f"    ❌ Invalid JSON in varieties")
    
    return slq_coins

def split_1917_types(conn):
    """Split 1917 Standing Liberty Quarters into Type I and Type II"""
    cursor = conn.cursor()
    
    # Find 1917 coins that need splitting
    cursor.execute('''
        SELECT * FROM coins 
        WHERE coin_id = 'US-SLIQ-1917-P'
    ''')
    
    original_coin = cursor.fetchone()
    if not original_coin:
        print("❌ 1917-P Standing Liberty Quarter not found in database")
        return False
    
    # Get column names
    cursor.execute("PRAGMA table_info(coins)")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Create dictionary of original coin data
    coin_data = dict(zip(columns, original_coin))
    print(f"\n📍 Found original coin: {coin_data['coin_id']}")
    print(f"   Business strikes: {coin_data['business_strikes']:,}")
    print(f"   Current varieties: {coin_data['varieties']}")
    
    # Parse existing varieties to extract Type information
    try:
        varieties = json.loads(coin_data['varieties']) if coin_data['varieties'] else []
        type1_variety = None
        type2_variety = None
        
        for variety in varieties:
            variety_name = variety.get('name', '')
            if variety_name == 'Type I':
                type1_variety = variety
            elif variety_name == 'Type II':
                type2_variety = variety
        
        if not type1_variety:
            print("❌ Type I variety not found in 1917-P coin")
            return False
        if not type2_variety:
            print("❌ Type II variety not found in 1917-P coin")
            return False
        
        print(f"   🎯 Type I variety: {type1_variety}")
        print(f"   🎯 Type II variety: {type2_variety}")
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON in varieties")
        return False
    
    # Create Type I record (early 1917)
    type1_data = coin_data.copy()
    type1_data['coin_id'] = 'US-SLIQ-1917-P-TYPE1'
    type1_data['variety_suffix'] = 'TYPE1'
    type1_data['business_strikes'] = type1_variety.get('estimated_mintage', 8792000)  # Full mintage for now
    type1_data['varieties'] = '[]'  # Clear varieties since this IS the Type I
    type1_data['notes'] = f"1917 Type I - {type1_variety.get('description', 'Bare-breasted Liberty design')}"
    type1_data['distinguishing_features'] = json.dumps([
        "Liberty's right breast exposed",
        "Eagle positioned lower on reverse", 
        "Original 13 stars under eagle"
    ])
    
    # Create Type II record (mid-1917 redesign)
    type2_data = coin_data.copy()
    type2_data['coin_id'] = 'US-SLIQ-1917-P-TYPE2'
    type2_data['variety_suffix'] = 'TYPE2'
    type2_data['business_strikes'] = 0  # Will need research for actual split
    type2_data['varieties'] = '[]'  # Clear varieties since this IS the Type II
    type2_data['notes'] = f"1917 Type II - {type2_variety.get('description', 'Chain mail covering added')}"
    type2_data['distinguishing_features'] = json.dumps([
        "Liberty covered with chain mail",
        "Eagle repositioned higher on reverse",
        "Three additional stars under eagle (16 total)"
    ])
    
    # Check if records already exist
    for new_coin_id in ['US-SLIQ-1917-P-TYPE1', 'US-SLIQ-1917-P-TYPE2']:
        cursor.execute('SELECT coin_id FROM coins WHERE coin_id = ?', (new_coin_id,))
        if cursor.fetchone():
            print(f"ℹ️  Type record already exists: {new_coin_id}")
            continue
        
        # Insert new type record
        placeholders = ', '.join(['?' for _ in columns])
        insert_sql = f"INSERT INTO coins ({', '.join(columns)}) VALUES ({placeholders})"
        
        try:
            if 'TYPE1' in new_coin_id:
                cursor.execute(insert_sql, [type1_data[col] for col in columns])
                print(f"✅ Created Type I record: {type1_data['coin_id']}")
                print(f"   Features: Bare-breasted Liberty, eagle lower, 13 stars")
            else:
                cursor.execute(insert_sql, [type2_data[col] for col in columns])
                print(f"✅ Created Type II record: {type2_data['coin_id']}")
                print(f"   Features: Chain mail covering, eagle higher, 16 stars")
                
        except Exception as e:
            print(f"❌ Error creating {new_coin_id}: {e}")
            return False
    
    # Remove original 1917-P record (now split into types)
    cursor.execute('DELETE FROM coins WHERE coin_id = ?', ('US-SLIQ-1917-P',))
    print(f"✅ Removed original 1917-P record (split into Type I/II)")
    
    return True

def add_type_suffixes_other_years(conn):
    """Add type suffixes to other Standing Liberty Quarters"""
    cursor = conn.cursor()
    
    # 1916: Type I only
    cursor.execute('''
        UPDATE coins 
        SET variety_suffix = 'TYPE1',
            notes = COALESCE(notes, '') || ' (Type I - bare-breasted Liberty)',
            distinguishing_features = ?
        WHERE coin_id = 'US-SLIQ-1916-P'
    ''', (json.dumps([
        "Liberty's right breast exposed", 
        "Eagle positioned lower", 
        "13 stars under eagle"
    ]),))
    
    if cursor.rowcount > 0:
        print("✅ Updated 1916-P to Type I")
    
    # 1918-1930: Type II only (update existing coins)
    cursor.execute('''
        SELECT coin_id, year FROM coins 
        WHERE series_name LIKE '%Standing Liberty%' 
        AND year BETWEEN 1918 AND 1930
    ''')
    
    type2_coins = cursor.fetchall()
    for coin_id, year in type2_coins:
        cursor.execute('''
            UPDATE coins 
            SET variety_suffix = 'TYPE2',
                notes = COALESCE(notes, '') || ' (Type II - chain mail covering)',
                distinguishing_features = ?
            WHERE coin_id = ?
        ''', (json.dumps([
            "Liberty covered with chain mail", 
            "Eagle repositioned higher", 
            "16 stars under eagle"
        ]), coin_id))
        
        if cursor.rowcount > 0:
            print(f"✅ Updated {coin_id} to Type II")
    
    return True

def verify_slq_split(conn):
    """Verify the Standing Liberty Quarter type split was successful"""
    cursor = conn.cursor()
    
    print("\n🔍 Verifying SLQ type split:")
    
    # Check all SLQ records now have type suffixes
    cursor.execute('''
        SELECT coin_id, year, mint, business_strikes, variety_suffix, notes
        FROM coins 
        WHERE series_name LIKE '%Standing Liberty%'
        ORDER BY year, coin_id
    ''')
    
    results = cursor.fetchall()
    type1_count = 0
    type2_count = 0
    
    for coin_id, year, mint, mintage, suffix, notes in results:
        print(f"  ✅ {coin_id}")
        print(f"     Year: {year}, Mint: {mint}")
        print(f"     Mintage: {mintage:,}")
        print(f"     Type: {suffix}")
        print(f"     Notes: {notes[:80]}..." if len(notes) > 80 else f"     Notes: {notes}")
        
        if suffix == 'TYPE1':
            type1_count += 1
        elif suffix == 'TYPE2':
            type2_count += 1
        print()
    
    print(f"📊 Summary:")
    print(f"  Type I coins: {type1_count}")
    print(f"  Type II coins: {type2_count}")
    print(f"  Total SLQ coins: {len(results)}")
    
    # Verify year distribution
    expected_type1_years = [1916, 1917]  # 1916 only, 1917 Type I
    expected_type2_years = list(range(1917, 1931))  # 1917 Type II through 1930
    
    cursor.execute('''
        SELECT DISTINCT year FROM coins 
        WHERE series_name LIKE '%Standing Liberty%' AND variety_suffix = 'TYPE1'
        ORDER BY year
    ''')
    actual_type1_years = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('''
        SELECT DISTINCT year FROM coins 
        WHERE series_name LIKE '%Standing Liberty%' AND variety_suffix = 'TYPE2'  
        ORDER BY year
    ''')
    actual_type2_years = [row[0] for row in cursor.fetchall()]
    
    print(f"\n📅 Year Distribution Verification:")
    print(f"  Type I years: {actual_type1_years} (expected: 1916, 1917)")
    print(f"  Type II years: {actual_type2_years} (expected: 1917-1930)")
    
    # Check for 1917 dual types
    cursor.execute('''
        SELECT COUNT(*) FROM coins 
        WHERE coin_id LIKE 'US-SLIQ-1917-%TYPE%'
    ''')
    dual_1917_count = cursor.fetchone()[0]
    print(f"  1917 dual types: {dual_1917_count} (expected: 2 - TYPE1 and TYPE2)")
    
    return len(results) > 0 and type1_count > 0 and type2_count > 0

def get_database_stats(conn):
    """Get current database statistics"""
    cursor = conn.cursor()
    
    stats = cursor.execute('''
        SELECT 
            COUNT(*) as total_coins,
            COUNT(CASE WHEN variety_suffix != '' THEN 1 END) as coins_with_suffix,
            COUNT(CASE WHEN series_name LIKE '%Standing Liberty%' THEN 1 END) as slq_coins,
            COUNT(CASE WHEN series_name LIKE '%Standing Liberty%' AND variety_suffix != '' THEN 1 END) as slq_with_suffix
        FROM coins
    ''').fetchone()
    
    print(f"\n📊 Database Statistics:")
    print(f"  Total coins: {stats[0]}")
    print(f"  Coins with variety suffix: {stats[1]}")
    print(f"  Standing Liberty Quarters: {stats[2]}")
    print(f"  SLQ with type suffix: {stats[3]}")
    
    return stats

def main():
    """Main execution function"""
    db_path = "database/coins.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        sys.exit(1)
    
    print("🚀 Splitting Standing Liberty Quarter Type I/II varieties")
    print("📚 Research source: https://github.com/mattsilv/coin-taxonomy/issues/24")
    print("=" * 70)
    
    backup_path = backup_database(db_path)
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            
            # Get initial stats and inventory
            get_database_stats(conn)
            get_slq_inventory(conn)
            
            # Split 1917 into Type I and Type II
            print("\n🔄 Splitting 1917 varieties...")
            success = split_1917_types(conn)
            
            if success:
                # Add type suffixes to other years
                print("\n🏷️  Adding type suffixes to other years...")
                add_type_suffixes_other_years(conn)
                
                # Verify the split
                verify_slq_split(conn)
                
                # Get final stats
                get_database_stats(conn)
                
                conn.commit()
                print("\n✅ Standing Liberty Quarter type split completed successfully!")
                print("\nTaxonomic identification benefits:")
                print("- 1916-P TYPE1: Rare bare-breasted design (52,000 minted)")
                print("- 1917-P TYPE1: Early 1917 bare-breasted design")
                print("- 1917-P TYPE2: Mid-1917 chain mail redesign")
                print("- 1918+ TYPE2: All post-redesign quarters")
                print("\nNext steps:")
                print("1. Test JSON exports include type suffixes")
                print("2. Research 1917 mintage split between Type I/II")
                print("3. Proceed with Mercury dime Full Bands implementation")
            else:
                print("\n❌ Standing Liberty Quarter type split failed")
                sys.exit(1)
                
    except Exception as e:
        print(f"\n❌ Error splitting SLQ types: {e}")
        print(f"Database backup available at: {backup_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()