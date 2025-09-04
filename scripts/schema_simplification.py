#!/usr/bin/env python3
"""
Schema Simplification Migration - Issue #59

This script simplifies the database schema by:
1. Creating a new simplified coins table with only essential fields
2. Migrating all data from the old coins table
3. Dropping unused tables (issues, series_registry, composition_registry, subject_registry)
4. Renaming the simplified table to replace the original

The simplified schema removes:
- grade (always null)
- thickness_mm (rarely used)
- mint_state_strikes, uncirculated_strikes, special_strikes (confusing overlaps)
- edge (we'll preserve this since it has data)

And drops entire unused tables:
- issues (0 records)
- series_registry (0 records)
- composition_registry (0 records)
- subject_registry (0 records)
"""

import sqlite3
import os
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "database" / "coins.db"

def simplify_schema():
    """Execute the schema simplification migration."""
    print("🚀 Starting Schema Simplification (Issue #59)")
    print(f"📁 Database: {DB_PATH}")
    
    if not DB_PATH.exists():
        print("❌ Database not found!")
        sys.exit(1)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")
        
        # Step 1: Create the simplified coins table
        print("\n📊 Creating simplified coins table...")
        cursor.execute("""
            CREATE TABLE coins_simplified (
                coin_id TEXT PRIMARY KEY,
                year INTEGER NOT NULL,
                mint TEXT NOT NULL,
                denomination TEXT NOT NULL,
                series TEXT,
                variety TEXT,
                composition TEXT,
                weight_grams REAL,
                diameter_mm REAL,
                edge TEXT,  -- Keeping edge since it has data
                designer TEXT,
                obverse_description TEXT,
                reverse_description TEXT,
                business_strikes INTEGER,
                proof_strikes INTEGER,
                total_mintage INTEGER,
                notes TEXT,
                rarity TEXT CHECK(rarity IN ('key', 'semi-key', 'common', 'scarce', NULL)),
                source_citation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Multi-country coin ID format: COUNTRY-TYPE-YEAR-MINT
                CONSTRAINT valid_coin_id_format CHECK (
                    coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'
                )
            )
        """)
        print("✅ Simplified table structure created")
        
        # Step 2: Count records before migration
        cursor.execute("SELECT COUNT(*) FROM coins")
        original_count = cursor.fetchone()[0]
        print(f"\n📈 Migrating {original_count} coins...")
        
        # Step 3: Migrate data to simplified table
        cursor.execute("""
            INSERT INTO coins_simplified (
                coin_id, year, mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge,
                designer, obverse_description, reverse_description,
                business_strikes, proof_strikes, total_mintage,
                notes, rarity, source_citation, created_at
            )
            SELECT 
                coin_id, year, mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge,
                designer, obverse_description, reverse_description,
                business_strikes, proof_strikes, total_mintage,
                notes, rarity, source_citation, created_at
            FROM coins
        """)
        
        # Step 4: Verify migration
        cursor.execute("SELECT COUNT(*) FROM coins_simplified")
        new_count = cursor.fetchone()[0]
        
        if new_count != original_count:
            raise Exception(f"Migration failed! Original: {original_count}, New: {new_count}")
        
        print(f"✅ Successfully migrated {new_count} coins")
        
        # Step 5: Drop the old coins table and rename the new one
        print("\n🔄 Replacing old table with simplified version...")
        cursor.execute("DROP TABLE coins")
        cursor.execute("ALTER TABLE coins_simplified RENAME TO coins")
        
        # Step 6: Recreate indexes on the new table
        print("\n📑 Recreating indexes...")
        cursor.execute("CREATE INDEX idx_coin_country ON coins(substr(coin_id, 1, 2))")
        cursor.execute("CREATE INDEX idx_coin_year ON coins(year)")
        cursor.execute("CREATE INDEX idx_coin_denomination ON coins(denomination)")
        cursor.execute("CREATE INDEX idx_coin_series ON coins(series)")
        cursor.execute("CREATE INDEX idx_coin_rarity ON coins(rarity)")
        print("✅ Indexes recreated")
        
        # Step 7: Drop unused tables
        print("\n🗑️  Dropping unused tables...")
        tables_to_drop = ['issues', 'series_registry', 'composition_registry', 'subject_registry']
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"  ✅ Dropped {table}")
            except Exception as e:
                print(f"  ⚠️  Could not drop {table}: {e}")
        
        # Step 8: VACUUM to reclaim space
        print("\n🧹 Optimizing database...")
        conn.execute("COMMIT")
        conn.execute("VACUUM")
        
        # Final verification
        print("\n✨ Schema Simplification Complete!")
        print("\n📊 Final Statistics:")
        
        # Show removed fields
        removed_fields = ['grade', 'thickness_mm', 'mint_state_strikes', 'uncirculated_strikes', 'special_strikes']
        print(f"  🗑️  Removed fields: {', '.join(removed_fields)}")
        
        # Show table structure
        cursor.execute("PRAGMA table_info(coins)")
        columns = cursor.fetchall()
        print(f"  📋 New table has {len(columns)} columns (down from 25)")
        print(f"  💾 Total coins: {new_count}")
        
        # Show database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        db_size = cursor.fetchone()[0]
        print(f"  📦 Database size: {db_size / 1024:.1f} KB")
        
        print("\n✅ Issue #59 Schema Simplification successfully completed!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during migration: {e}")
        print("🔄 Transaction rolled back - database unchanged")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    simplify_schema()