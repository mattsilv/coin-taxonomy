#!/usr/bin/env python3
"""
Database Migration: Add Coin Inventory Table

Creates a coin_inventory table to separate coin identity from graded instances.
This enables tracking specific graded coins with certification details.

Purpose:
- Link coin issues (coins table) with specific grades (grade_standards table)
- Store certification details (grading service, cert number, modifiers)
- Enable value determination: coin identity + grade = market value
- Support collection management and inventory tracking

Schema based on: data/schema/grade_external_metadata.schema.json

See: GitHub Issue #65 (Enhancement Recommendation #3)

Usage:
    uv run python scripts/migrate_add_coin_inventory.py
    uv run python scripts/migrate_add_coin_inventory.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from pathlib import Path
import shutil

class CoinInventoryMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_pre_inventory_{timestamp}.db"

        if os.path.exists(self.db_path):
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def create_coin_inventory_table(self, conn, dry_run=False):
        """Create the coin_inventory table."""
        cursor = conn.cursor()

        if dry_run:
            print("\nDRY RUN: Would create coin_inventory table with schema:")
            print("""
  Core Fields:
  - inventory_id: Auto-increment primary key
  - coin_id: Foreign key to coins table (coin identity)
  - grade_id: Foreign key to grade_standards table (grade)

  Certification Details:
  - grading_service: PCGS, NGC, ANACS, ICG, raw, self-graded
  - certification_number: Service certification number
  - is_certified: Boolean - third-party certified or raw
  - strike_type: business, proof, specimen

  Grade Modifiers:
  - modifiers: JSON array - CAM, DCAM, UCAM, FB, FBL, RD, RB, BN, etc.
  - full_grade_string: Complete grade as appears on holder

  Market Analysis:
  - market_threshold_grade: Boolean - significant price break point
  - purchase_price: Optional - acquisition cost
  - purchase_date: Optional - when acquired
  - current_value_estimate: Optional - estimated current value

  Collection Management:
  - collection_name: Optional - which collection this belongs to
  - storage_location: Optional - where physically stored
  - notes: Optional - condition notes, special characteristics
  - image_urls: JSON array - photos of the coin

  Metadata:
  - created_at: When record was created
  - updated_at: When record was last modified
            """)
            return

        print("\nCreating coin_inventory table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coin_inventory (
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Core References
                coin_id TEXT NOT NULL,
                grade_id TEXT NOT NULL,

                -- Certification Details
                grading_service TEXT NOT NULL DEFAULT 'raw',
                certification_number TEXT,
                is_certified BOOLEAN NOT NULL DEFAULT 0,
                strike_type TEXT,

                -- Grade Modifiers
                modifiers JSON,  -- Array of modifiers: ["CAM", "DCAM", "RD", etc.]
                full_grade_string TEXT,  -- Complete grade: "PCGS MS-65 RD"

                -- Market Analysis
                market_threshold_grade BOOLEAN DEFAULT 0,
                purchase_price REAL,
                purchase_date DATE,
                current_value_estimate REAL,

                -- Collection Management
                collection_name TEXT,
                storage_location TEXT,
                notes TEXT,
                image_urls JSON,  -- Array of image URLs

                -- Metadata
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Foreign Keys
                FOREIGN KEY (coin_id) REFERENCES coins(coin_id) ON DELETE CASCADE,
                FOREIGN KEY (grade_id) REFERENCES grade_standards(grade_id) ON DELETE RESTRICT,

                -- Constraints
                CHECK (grading_service IN ('PCGS', 'NGC', 'ANACS', 'ICG', 'raw', 'self-graded')),
                CHECK (strike_type IN ('business', 'proof', 'specimen', NULL)),
                CHECK (is_certified IN (0, 1)),
                CHECK (market_threshold_grade IN (0, 1))
            )
        ''')
        print("✓ Created coin_inventory table")

        # Create indices for common lookups
        print("\nCreating indices...")

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_inventory_coin_id
            ON coin_inventory(coin_id)
        ''')
        print("  ✓ Index on coin_id")

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_inventory_grade_id
            ON coin_inventory(grade_id)
        ''')
        print("  ✓ Index on grade_id")

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_inventory_grading_service
            ON coin_inventory(grading_service)
        ''')
        print("  ✓ Index on grading_service")

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_inventory_collection
            ON coin_inventory(collection_name)
        ''')
        print("  ✓ Index on collection_name")

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_inventory_certified
            ON coin_inventory(is_certified)
        ''')
        print("  ✓ Index on is_certified")

        print("✓ Created all indices")

    def create_inventory_views(self, conn, dry_run=False):
        """Create helpful views for querying inventory."""
        cursor = conn.cursor()

        if dry_run:
            print("\nDRY RUN: Would create helpful views:")
            print("  - vw_inventory_full: Complete coin details with grade info")
            print("  - vw_inventory_summary: Collection overview statistics")
            return

        print("\nCreating database views...")

        # Full inventory view with all details
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS vw_inventory_full AS
            SELECT
                i.inventory_id,
                i.coin_id,
                c.year,
                c.mint,
                c.denomination,
                c.series,
                c.variety,
                i.grade_id,
                g.grade_name,
                g.numeric_value as grade_numeric,
                g.category as grade_category,
                g.subcategory as grade_subcategory,
                i.grading_service,
                i.certification_number,
                i.is_certified,
                i.strike_type,
                i.modifiers,
                i.full_grade_string,
                i.market_threshold_grade,
                i.purchase_price,
                i.purchase_date,
                i.current_value_estimate,
                i.collection_name,
                i.storage_location,
                i.notes,
                i.created_at,
                i.updated_at
            FROM coin_inventory i
            JOIN coins c ON i.coin_id = c.coin_id
            JOIN grade_standards g ON i.grade_id = g.grade_id
        ''')
        print("  ✓ Created vw_inventory_full")

        # Summary view for collection statistics
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS vw_inventory_summary AS
            SELECT
                collection_name,
                COUNT(*) as total_coins,
                SUM(CASE WHEN is_certified = 1 THEN 1 ELSE 0 END) as certified_count,
                SUM(CASE WHEN is_certified = 0 THEN 1 ELSE 0 END) as raw_count,
                COUNT(DISTINCT grading_service) as grading_services_used,
                SUM(purchase_price) as total_purchase_cost,
                SUM(current_value_estimate) as total_estimated_value,
                MIN(purchase_date) as earliest_purchase,
                MAX(purchase_date) as latest_purchase
            FROM coin_inventory
            WHERE collection_name IS NOT NULL
            GROUP BY collection_name
        ''')
        print("  ✓ Created vw_inventory_summary")

        print("✓ Created all views")

    def add_sample_data(self, conn, dry_run=False):
        """Add sample inventory records for demonstration."""
        cursor = conn.cursor()

        if dry_run:
            print("\nDRY RUN: Would insert sample inventory records")
            return

        # Check if we have any coins in the database
        cursor.execute('SELECT coin_id FROM coins LIMIT 5')
        sample_coins = cursor.fetchall()

        if not sample_coins:
            print("\n⚠ No coins found in database - skipping sample data insertion")
            return

        print("\nInserting sample inventory records...")

        samples = [
            {
                'coin_id': sample_coins[0][0],
                'grade_id': 'MS-65',
                'grading_service': 'PCGS',
                'certification_number': '12345678',
                'is_certified': 1,
                'strike_type': 'business',
                'modifiers': json.dumps(['RD']),
                'full_grade_string': 'PCGS MS-65 RD',
                'market_threshold_grade': 1,
                'collection_name': 'Example Collection',
                'notes': 'Sample certified coin'
            },
            {
                'coin_id': sample_coins[0][0],
                'grade_id': 'AU-58',
                'grading_service': 'raw',
                'is_certified': 0,
                'strike_type': 'business',
                'full_grade_string': 'AU-58',
                'market_threshold_grade': 1,
                'collection_name': 'Example Collection',
                'notes': 'Sample raw coin - self-graded estimate'
            }
        ]

        inserted = 0
        for sample in samples:
            try:
                cursor.execute('''
                    INSERT INTO coin_inventory (
                        coin_id, grade_id, grading_service, certification_number,
                        is_certified, strike_type, modifiers, full_grade_string,
                        market_threshold_grade, collection_name, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sample['coin_id'],
                    sample['grade_id'],
                    sample['grading_service'],
                    sample.get('certification_number'),
                    sample['is_certified'],
                    sample.get('strike_type'),
                    sample.get('modifiers'),
                    sample['full_grade_string'],
                    sample['market_threshold_grade'],
                    sample.get('collection_name'),
                    sample.get('notes')
                ))
                inserted += 1
            except sqlite3.IntegrityError as e:
                print(f"  ⚠ Skipped sample: {e}")

        print(f"✓ Inserted {inserted} sample records")

    def verify_migration(self, conn):
        """Verify the migration was successful."""
        cursor = conn.cursor()

        print("\nVerifying migration...")

        # Check table exists
        cursor.execute('''
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='coin_inventory'
        ''')
        if not cursor.fetchone():
            raise Exception("coin_inventory table not created")
        print("  ✓ coin_inventory table exists")

        # Check views exist
        cursor.execute('''
            SELECT name FROM sqlite_master
            WHERE type='view' AND name IN ('vw_inventory_full', 'vw_inventory_summary')
        ''')
        views = cursor.fetchall()
        if len(views) != 2:
            raise Exception("Views not created")
        print("  ✓ Views created")

        # Check indices exist
        cursor.execute('''
            SELECT name FROM sqlite_master
            WHERE type='index' AND tbl_name='coin_inventory'
        ''')
        indices = cursor.fetchall()
        print(f"  ✓ {len(indices)} indices created")

        # Check sample data
        cursor.execute('SELECT COUNT(*) FROM coin_inventory')
        count = cursor.fetchone()[0]
        print(f"  ✓ {count} sample records in coin_inventory")

        print("✓ Migration verification passed")

    def run(self, dry_run=False, skip_samples=False):
        """Execute the migration."""
        print("=== Coin Inventory Database Migration ===\n")
        print("Purpose: Add coin_inventory table to separate coin identity from graded instances")
        print("Enhancement: GitHub Issue #65 - Recommendation #3\n")

        if not dry_run:
            self.create_backup()

        conn = sqlite3.connect(self.db_path)

        try:
            # Create table and indices
            self.create_coin_inventory_table(conn, dry_run)

            # Create views
            self.create_inventory_views(conn, dry_run)

            # Add sample data (unless skipped)
            if not skip_samples:
                self.add_sample_data(conn, dry_run)

            if not dry_run:
                conn.commit()

                # Verify migration
                self.verify_migration(conn)

                print(f"\n✓ Migration completed successfully")
                print(f"✓ Backup: {self.backup_path}")

                print("\nNext steps:")
                print("  1. Run: uv run python scripts/export_from_database.py")
                print("  2. Update documentation with coin_inventory usage examples")
                print("  3. Consider adding API endpoints for inventory management")
                print("  4. Update schema documentation")
                print("  5. Commit changes - Issue #65")
            else:
                print("\n✓ Dry run completed (no changes made)")

        except Exception as e:
            if not dry_run:
                conn.rollback()
            print(f"\n✗ Migration failed: {e}")
            raise
        finally:
            conn.close()

def main():
    parser = argparse.ArgumentParser(
        description='Add coin_inventory table to database (Issue #65 - Recommendation #3)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying'
    )
    parser.add_argument(
        '--skip-samples',
        action='store_true',
        help='Skip inserting sample inventory records'
    )

    args = parser.parse_args()

    migration = CoinInventoryMigration()

    try:
        migration.run(dry_run=args.dry_run, skip_samples=args.skip_samples)
        return 0
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
