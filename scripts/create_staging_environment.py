#!/usr/bin/env python3
"""
Create staging environment within existing SQLite database for safe migration testing.

This script creates staging tables (coins_staging, issues_staging) and copies
production data for testing the historical coin backfill migration.

Usage:
    python scripts/create_staging_environment.py --setup      # Create staging tables
    python scripts/create_staging_environment.py --cleanup    # Remove staging tables
    python scripts/create_staging_environment.py --status     # Check staging status
"""

import sqlite3
import argparse
from datetime import datetime

class StagingEnvironment:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        
    def create_staging_tables(self):
        """Create staging tables with same schema as production."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("🔧 Creating staging tables...")
            
            # Create coins_staging table with same schema as coins
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS coins_staging (
                    coin_id TEXT PRIMARY KEY,
                    series_id TEXT NOT NULL,
                    country TEXT NOT NULL,
                    denomination TEXT NOT NULL,
                    series_name TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    mint TEXT NOT NULL,
                    business_strikes INTEGER,
                    proof_strikes INTEGER,
                    rarity TEXT CHECK(rarity IN ("key", "semi-key", "common", "scarce")),
                    composition JSON,
                    weight_grams REAL,
                    diameter_mm REAL,
                    varieties JSON,
                    source_citation TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    CONSTRAINT valid_coin_id_format_staging CHECK (
                        coin_id GLOB 'US-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'
                    )
                )
            ''')
            
            # Create indexes for staging table
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_coins_staging_series ON coins_staging(series_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_coins_staging_year ON coins_staging(year)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_coins_staging_denomination ON coins_staging(denomination)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_coins_staging_rarity ON coins_staging(rarity)')
            
            # Create issues_staging table with exact same schema as issues
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS issues_staging (
                    issue_id TEXT PRIMARY KEY,
                    object_type TEXT NOT NULL,
                    series_id TEXT NOT NULL,
                    
                    -- Issuing Entity
                    country_code TEXT NOT NULL,
                    authority_name TEXT NOT NULL,
                    monetary_system TEXT NOT NULL,
                    currency_unit TEXT NOT NULL,
                    
                    -- Denomination
                    face_value REAL NOT NULL,
                    unit_name TEXT NOT NULL,
                    common_names JSON,
                    system_fraction TEXT,
                    
                    -- Issue Details
                    issue_year INTEGER NOT NULL,
                    mint_id TEXT,
                    date_range_start INTEGER,
                    date_range_end INTEGER,
                    
                    -- Authority Context
                    authority_period JSON,
                    
                    -- Physical Specifications
                    specifications JSON NOT NULL,
                    
                    -- Design Elements
                    sides JSON NOT NULL,
                    
                    -- Production Data
                    mintage JSON,
                    rarity TEXT,
                    varieties JSON,
                    
                    -- Metadata
                    source_citation TEXT,
                    notes TEXT,
                    metadata JSON,
                    
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    CONSTRAINT valid_issue_id_format_staging CHECK (
                        issue_id GLOB 'US-[A-Z]*-[0-9][0-9][0-9][0-9]-[A-Z]*'
                    )
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_issues_staging_series ON issues_staging(series_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_issues_staging_year ON issues_staging(issue_year)')
            
            conn.commit()
            print("✅ Staging tables created successfully")
            
        except sqlite3.Error as e:
            print(f"❌ Error creating staging tables: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def copy_production_data(self):
        """Copy current production data to staging tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("📋 Copying production data to staging...")
            
            # Copy coins data
            cursor.execute('DELETE FROM coins_staging')  # Clear existing staging data
            cursor.execute('''
                INSERT INTO coins_staging 
                SELECT * FROM coins
            ''')
            
            coins_copied = cursor.rowcount
            print(f"✅ Copied {coins_copied} coins to staging")
            
            # Copy issues data if table exists
            cursor.execute('''
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='issues'
            ''')
            
            if cursor.fetchone():
                cursor.execute('DELETE FROM issues_staging')
                cursor.execute('''
                    INSERT INTO issues_staging 
                    SELECT * FROM issues
                ''')
                
                issues_copied = cursor.rowcount
                print(f"✅ Copied {issues_copied} issues to staging")
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"❌ Error copying production data: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_staging_status(self):
        """Get current staging environment status."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if staging tables exist
            cursor.execute('''
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%_staging'
                ORDER BY name
            ''')
            
            staging_tables = [row[0] for row in cursor.fetchall()]
            
            if not staging_tables:
                print("❌ No staging tables found")
                return
                
            print("🔍 Staging Environment Status:")
            print(f"📊 Staging tables: {', '.join(staging_tables)}")
            
            # Get record counts
            for table in staging_tables:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                print(f"   {table}: {count} records")
            
            # Compare with production
            if 'coins_staging' in staging_tables:
                cursor.execute('SELECT COUNT(*) FROM coins')
                prod_coins = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM coins_staging')
                staging_coins = cursor.fetchone()[0]
                
                print(f"\n📈 Production vs Staging:")
                print(f"   coins: {prod_coins} (prod) vs {staging_coins} (staging)")
                
                if staging_coins > prod_coins:
                    diff = staging_coins - prod_coins
                    print(f"   🆕 {diff} new coins in staging (+{diff/prod_coins*100:.1f}%)")
                
        except sqlite3.Error as e:
            print(f"❌ Error checking staging status: {e}")
        finally:
            conn.close()
    
    def cleanup_staging(self):
        """Remove staging tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("🧹 Cleaning up staging environment...")
            
            # Get all staging tables
            cursor.execute('''
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%_staging'
            ''')
            
            staging_tables = [row[0] for row in cursor.fetchall()]
            
            for table in staging_tables:
                cursor.execute(f'DROP TABLE IF EXISTS {table}')
                print(f"✅ Dropped table: {table}")
            
            conn.commit()
            print("✅ Staging cleanup completed")
            
        except sqlite3.Error as e:
            print(f"❌ Error cleaning up staging: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='Manage staging environment for coin taxonomy')
    parser.add_argument('--setup', action='store_true', help='Create staging tables and copy production data')
    parser.add_argument('--cleanup', action='store_true', help='Remove staging tables')
    parser.add_argument('--status', action='store_true', help='Show staging environment status')
    parser.add_argument('--copy-data', action='store_true', help='Copy production data to existing staging tables')
    
    args = parser.parse_args()
    
    staging = StagingEnvironment()
    
    try:
        if args.setup:
            staging.create_staging_tables()
            staging.copy_production_data()
            staging.get_staging_status()
            
        elif args.cleanup:
            staging.cleanup_staging()
            
        elif args.status:
            staging.get_staging_status()
            
        elif args.copy_data:
            staging.copy_production_data()
            staging.get_staging_status()
            
        else:
            print("Please specify an action: --setup, --cleanup, --status, or --copy-data")
            return 1
            
    except Exception as e:
        print(f"❌ Operation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())