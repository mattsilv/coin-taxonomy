#!/usr/bin/env python3
"""
Migration Script: Implement Standardized Category Field for Coin vs Currency Classification

This migration implements Issue #47 by:
1. Adding subcategory field to coins table
2. Updating category values to lowercase standard format
3. Auto-classifying subcategories based on series names
4. Synchronizing issues.object_type with standardized values

Usage:
    python scripts/migrate_category_standardization.py
    python scripts/migrate_category_standardization.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Tuple

class CategoryStandardizationMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None
        
        # Define subcategory mappings based on series names
        self.coin_subcategory_mappings = {
            'bullion': ['eagle', 'maple leaf', 'buffalo', 'libertad', 'britannia', 'gold bullion', 'silver bullion', 'platinum', 'palladium'],
            'commemorative': ['commemorative', 'anniversary', 'olympic', 'bicentennial'],
            'pattern': ['pattern', 'trial', 'experimental'],
            'proof': ['proof'],
            'circulation': []  # Default for regular coins
        }
        
        self.currency_subcategory_mappings = {
            'federal': ['federal reserve', 'frn'],
            'certificate': ['silver certificate', 'gold certificate'],
            'national': ['national bank', 'nbn'],
            'fractional': ['fractional'],
            'confederate': ['confederate'],
            'colonial': ['colonial', 'continental'],
            'obsolete': ['obsolete']
        }
        
    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_category_migration_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")
            return True
        return False
        
    def add_subcategory_column(self, conn):
        """Add subcategory column to coins table if it doesn't exist."""
        cursor = conn.cursor()
        
        # Check if subcategory column exists
        cursor.execute("PRAGMA table_info(coins)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'subcategory' not in columns:
            print("📝 Adding subcategory column to coins table...")
            cursor.execute("ALTER TABLE coins ADD COLUMN subcategory TEXT")
            conn.commit()
            print("✓ Subcategory column added")
        else:
            print("✓ Subcategory column already exists")
            
    def update_category_values(self, conn, dry_run=False):
        """Update category values to lowercase standard format."""
        cursor = conn.cursor()
        
        print("\n📊 Updating category values to standard format...")
        
        # Get current category distribution
        cursor.execute("SELECT category, COUNT(*) FROM coins WHERE category IS NOT NULL GROUP BY category")
        current_categories = cursor.fetchall()
        
        print("Current category distribution:")
        for cat, count in current_categories:
            print(f"  {cat}: {count} coins")
        
        if not dry_run:
            # Update COIN to coin
            cursor.execute("UPDATE coins SET category = 'coin' WHERE UPPER(category) = 'COIN'")
            coin_updates = cursor.rowcount
            print(f"✓ Updated {coin_updates} coins from 'COIN' to 'coin'")
            
            # Check for any paper currency entries based on series names
            paper_currency_keywords = ['certificate', 'note', 'bill', 'currency', 'frn', 'nbn']
            
            for keyword in paper_currency_keywords:
                cursor.execute("""
                    UPDATE coins 
                    SET category = 'currency' 
                    WHERE LOWER(series_name) LIKE ? 
                    AND (category IS NULL OR category = 'coin')
                """, (f'%{keyword}%',))
                
                if cursor.rowcount > 0:
                    print(f"✓ Updated {cursor.rowcount} entries to 'currency' based on '{keyword}' in series name")
            
            conn.commit()
        else:
            print("DRY RUN: Would update category values")
            
    def classify_subcategories(self, conn, dry_run=False):
        """Auto-classify subcategories based on series names."""
        cursor = conn.cursor()
        
        print("\n🏷️ Classifying subcategories...")
        
        # Classify coin subcategories
        cursor.execute("SELECT coin_id, series_name, category FROM coins WHERE category = 'coin'")
        coins = cursor.fetchall()
        
        subcategory_counts = {}
        
        for coin_id, series_name, category in coins:
            series_lower = series_name.lower() if series_name else ''
            subcategory = 'circulation'  # Default
            
            # Check for special subcategories
            for subcat, keywords in self.coin_subcategory_mappings.items():
                if subcat == 'circulation':
                    continue
                if any(keyword in series_lower for keyword in keywords):
                    subcategory = subcat
                    break
            
            # Check for proof strikes
            cursor.execute("SELECT proof_strikes FROM coins WHERE coin_id = ?", (coin_id,))
            proof_strikes = cursor.fetchone()[0]
            if proof_strikes and proof_strikes > 0 and 'proof' in series_lower:
                subcategory = 'proof'
            
            subcategory_counts[subcategory] = subcategory_counts.get(subcategory, 0) + 1
            
            if not dry_run:
                cursor.execute("UPDATE coins SET subcategory = ? WHERE coin_id = ?", 
                             (subcategory, coin_id))
        
        # Classify currency subcategories
        cursor.execute("SELECT coin_id, series_name FROM coins WHERE category = 'currency'")
        currencies = cursor.fetchall()
        
        for coin_id, series_name in currencies:
            series_lower = series_name.lower() if series_name else ''
            subcategory = 'federal'  # Default for currency
            
            for subcat, keywords in self.currency_subcategory_mappings.items():
                if any(keyword in series_lower for keyword in keywords):
                    subcategory = subcat
                    break
            
            subcategory_counts[subcategory] = subcategory_counts.get(subcategory, 0) + 1
            
            if not dry_run:
                cursor.execute("UPDATE coins SET subcategory = ? WHERE coin_id = ?", 
                             (subcategory, coin_id))
        
        if not dry_run:
            conn.commit()
            
        print("\nSubcategory distribution:")
        for subcat, count in sorted(subcategory_counts.items()):
            print(f"  {subcat}: {count} items")
            
    def synchronize_issues_table(self, conn, dry_run=False):
        """Synchronize issues.object_type with standardized values."""
        cursor = conn.cursor()
        
        print("\n🔄 Synchronizing issues table...")
        
        # Get current object_type distribution
        cursor.execute("SELECT object_type, COUNT(*) FROM issues GROUP BY object_type")
        current_types = cursor.fetchall()
        
        print("Current object_type distribution:")
        for obj_type, count in current_types:
            print(f"  {obj_type}: {count} issues")
        
        if not dry_run:
            # Update banknote to currency for consistency
            cursor.execute("UPDATE issues SET object_type = 'currency' WHERE object_type = 'banknote'")
            updates = cursor.rowcount
            
            if updates > 0:
                print(f"✓ Updated {updates} issues from 'banknote' to 'currency'")
            
            conn.commit()
        else:
            print("DRY RUN: Would update object_type values")
            
    def verify_migration(self, conn):
        """Verify the migration was successful."""
        cursor = conn.cursor()
        
        print("\n✅ Verification:")
        
        # Check coins table
        cursor.execute("""
            SELECT category, subcategory, COUNT(*) 
            FROM coins 
            GROUP BY category, subcategory 
            ORDER BY category, subcategory
        """)
        
        print("\nCoins table - Category/Subcategory distribution:")
        for cat, subcat, count in cursor.fetchall():
            print(f"  {cat}/{subcat}: {count} coins")
        
        # Check issues table
        cursor.execute("SELECT object_type, COUNT(*) FROM issues GROUP BY object_type")
        
        print("\nIssues table - Object type distribution:")
        for obj_type, count in cursor.fetchall():
            print(f"  {obj_type}: {count} issues")
        
        # Check for any NULL categories
        cursor.execute("SELECT COUNT(*) FROM coins WHERE category IS NULL")
        null_count = cursor.fetchone()[0]
        if null_count > 0:
            print(f"\n⚠️ Warning: {null_count} coins have NULL category")
        
        # Sample some categorizations
        print("\nSample categorizations:")
        cursor.execute("""
            SELECT coin_id, series_name, category, subcategory 
            FROM coins 
            WHERE subcategory IS NOT NULL 
            LIMIT 10
        """)
        
        for coin_id, series, cat, subcat in cursor.fetchall():
            print(f"  {coin_id}: {series} → {cat}/{subcat}")
            
    def run_migration(self, dry_run=False):
        """Run the complete migration."""
        print("🚀 Starting Category Standardization Migration")
        print(f"Database: {self.db_path}")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        
        if not dry_run:
            if not self.create_backup():
                print("❌ Failed to create backup")
                return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Run migration steps
            self.add_subcategory_column(conn)
            self.update_category_values(conn, dry_run)
            self.classify_subcategories(conn, dry_run)
            self.synchronize_issues_table(conn, dry_run)
            
            if not dry_run:
                self.verify_migration(conn)
            
            conn.close()
            
            print("\n✨ Migration completed successfully!")
            
            if not dry_run:
                print(f"\nBackup saved to: {self.backup_path}")
                print("\nNext steps:")
                print("1. Run: python scripts/export_from_database.py")
                print("2. Commit all changes: git add . && git commit -m 'Implement standardized category field (Issue #47)'")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            if not dry_run and self.backup_path:
                print(f"Restore from backup: {self.backup_path}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Migrate to standardized category field')
    parser.add_argument('--dry-run', action='store_true', 
                      help='Run migration in dry-run mode (no changes)')
    
    args = parser.parse_args()
    
    migration = CategoryStandardizationMigration()
    success = migration.run_migration(dry_run=args.dry_run)
    
    exit(0 if success else 1)

if __name__ == '__main__':
    main()