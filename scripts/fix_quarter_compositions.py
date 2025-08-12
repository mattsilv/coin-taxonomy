#!/usr/bin/env python3
"""
Fix US Quarter composition periods with precise specifications.

Based on user requirements:
- Washington Quarters (1932-1964): 90% silver, 10% copper - 6.25g
- Washington Quarters (1965+): Copper-nickel clad - 5.67g
- Fix missing composition data for earlier quarter series
- Update composition periods for each series
"""

import sqlite3
import json
import sys
from datetime import datetime

def create_backup():
    """Create database backup before modifications"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backups/coins_quarter_fix_backup_{timestamp}.db"
    
    # Create backup
    import shutil
    shutil.copy("database/coins.db", backup_name)
    print(f"✅ Created backup: {backup_name}")
    return backup_name

def update_quarter_compositions():
    """Update quarter compositions with correct specifications"""
    
    backup_file = create_backup()
    print("🚀 Starting quarter composition fixes...")
    
    conn = sqlite3.connect("database/coins.db")
    cursor = conn.cursor()
    
    # Define compositions
    silver_composition = {
        "alloy_name": "Silver",
        "alloy": {"silver": 0.9, "copper": 0.1}
    }
    
    clad_composition = {
        "alloy_name": "Copper-Nickel Clad", 
        "alloy": {"copper_core": 0.917, "cupronickel_cladding": 0.083}
    }
    
    historical_silver_composition = {
        "alloy_name": "Silver",
        "alloy": {"silver": 0.9, "copper": 0.1}
    }
    
    print("📋 Updating individual quarter compositions...")
    
    # 1. Fix 1838 Seated Liberty Quarter (missing composition)
    cursor.execute("""
        UPDATE coins 
        SET composition = ?, weight_grams = 6.25
        WHERE coin_id = 'US-SLQU-1838-P'
    """, (json.dumps(historical_silver_composition),))
    print("   ✅ Fixed 1838 Seated Liberty Quarter composition")
    
    # 2. Ensure all Barber Quarters have correct silver composition (1892-1913)
    cursor.execute("""
        UPDATE coins 
        SET composition = ?, weight_grams = 6.25
        WHERE denomination = 'Quarters' 
        AND series_id = 'barber_quarter'
        AND year BETWEEN 1892 AND 1913
    """, (json.dumps(silver_composition),))
    print("   ✅ Updated Barber Quarter compositions (1892-1913)")
    
    # 3. Ensure all Standing Liberty Quarters have correct silver composition (1916-1930)
    cursor.execute("""
        UPDATE coins 
        SET composition = ?, weight_grams = 6.25
        WHERE denomination = 'Quarters' 
        AND series_id = 'standing_liberty_quarter'
        AND year BETWEEN 1916 AND 1930
    """, (json.dumps(silver_composition),))
    print("   ✅ Updated Standing Liberty Quarter compositions (1916-1930)")
    
    # 4. Washington Quarters - Silver period (1932-1964)
    cursor.execute("""
        UPDATE coins 
        SET composition = ?, weight_grams = 6.25
        WHERE denomination = 'Quarters' 
        AND series_id = 'washington_quarter'
        AND year BETWEEN 1932 AND 1964
    """, (json.dumps(silver_composition),))
    print("   ✅ Updated Washington Quarter silver compositions (1932-1964)")
    
    # 5. Washington Quarters - Clad period (1965+)
    cursor.execute("""
        UPDATE coins 
        SET composition = ?, weight_grams = 5.67
        WHERE denomination = 'Quarters' 
        AND series_id = 'washington_quarter'
        AND year >= 1965
    """, (json.dumps(clad_composition),))
    print("   ✅ Updated Washington Quarter clad compositions (1965+)")
    
    # Add missing 1965 transition year coin if not exists
    cursor.execute("SELECT COUNT(*) FROM coins WHERE coin_id = 'US-WASH-1965-P'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO coins (
                coin_id, series_id, country, denomination, series_name, year, mint,
                business_strikes, composition, weight_grams, diameter_mm,
                common_names, distinguishing_features, identification_keywords,
                obverse_description, reverse_description, source_citation
            ) VALUES (
                'US-WASH-1965-P', 'washington_quarter', 'US', 'Quarters', 
                'Washington Quarter', 1965, 'P', 1817717540,
                ?, 5.67, 24.3,
                ?, ?, ?,
                'George Washington profile facing left, ''LIBERTY'' above, ''IN GOD WE TRUST'' to left, date below',
                'Heraldic eagle with spread wings standing on bundle of arrows with olive branches, ''UNITED STATES OF AMERICA'' above, ''QUARTER DOLLAR'' below',
                'US Mint records'
            )
        """, (
            json.dumps(clad_composition),
            json.dumps(["Washington Quarter", "Washington Twenty-Five Cent", "George Washington Quarter"]),
            json.dumps(["90% silver (1932-1964) then copper-nickel clad", "24.3mm diameter", "First president on regular issue coin", "Eagle with arrows and olive branches", "John Flanagan design"]),
            json.dumps(["washington quarter", "george washington quarter", "silver quarter", "clad quarter", "eagle quarter", "presidential quarter", "john flanagan", "25 cents"])
        ))
        print("   ✅ Added missing 1965 Washington Quarter (transition year)")
    
    conn.commit()
    print("📊 Verifying composition updates...")
    
    # Verify the changes
    cursor.execute("""
        SELECT series_id, COUNT(*) as count, 
               JSON_EXTRACT(composition, '$.alloy_name') as alloy_name,
               MIN(year) as first_year, MAX(year) as last_year
        FROM coins 
        WHERE denomination = 'Quarters' 
        AND composition IS NOT NULL
        AND composition != '{}'
        GROUP BY series_id, JSON_EXTRACT(composition, '$.alloy_name')
        ORDER BY series_id, first_year
    """)
    
    results = cursor.fetchall()
    print("\n📋 Quarter Composition Summary:")
    for result in results:
        series, count, alloy, first_year, last_year = result
        print(f"   • {series}: {count} coins, {alloy} ({first_year}-{last_year})")
    
    conn.close()
    print(f"\n✅ Quarter composition fixes completed!")
    print(f"💾 Backup saved as: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        success = update_quarter_compositions()
        if success:
            print("\n🎉 All quarter composition fixes applied successfully!")
            print("📝 Next: Run export script to update JSON files")
        else:
            print("\n❌ Quarter composition fix failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during quarter composition fix: {e}")
        sys.exit(1)