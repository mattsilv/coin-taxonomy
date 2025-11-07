#!/usr/bin/env python3
"""
Schema Migration: Add XXXX Year Support for Bullion Products

Updates the database schema to support random year pattern (XXXX) for bullion:
1. Change year column from INTEGER to TEXT
2. Update coin_id CHECK constraint to accept XXXX in year position
3. Preserve all existing data (609 coins)

This migration enables:
- US-AGEO-XXXX-X (Gold Eagle, random year)
- US-ASEA-XXXX-X (Silver Eagle, random year)
- Other bullion products sold as "dealer's choice" year

See: docs/BULLION_INTEGRATION_GUIDE.md

Usage:
    uv run python scripts/migrate_schema_for_xxxx_support.py
    uv run python scripts/migrate_schema_for_xxxx_support.py --dry-run
"""

import sqlite3
import os
import argparse
from datetime import datetime
import shutil

class XXXXSchemaMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_pre_xxxx_migration_{timestamp}.db"

        if os.path.exists(self.db_path):
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def get_row_count(self, conn, table='coins'):
        """Get current row count for verification."""
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return cursor.fetchone()[0]

    def migrate_coins_table(self, conn, dry_run=False):
        """Migrate coins table to support XXXX year pattern."""
        cursor = conn.cursor()

        # Get current count
        original_count = self.get_row_count(conn, 'coins')
        print(f"Original coins table: {original_count} rows")

        if dry_run:
            print("\nDRY RUN: Would create new table with updated schema")
            print("  - year: INTEGER → TEXT (accepts YYYY or XXXX)")
            print("  - coin_id CHECK: Updated to accept XXXX pattern")
            return

        # Create new table with updated schema
        print("\nCreating new coins table with XXXX support...")
        cursor.execute('''
            CREATE TABLE coins_new (
                coin_id TEXT PRIMARY KEY,
                year TEXT NOT NULL CHECK(
                    year GLOB '[0-9][0-9][0-9][0-9]' OR
                    year = 'XXXX'
                ),
                mint TEXT NOT NULL,
                denomination TEXT NOT NULL,
                series TEXT,
                variety TEXT,
                composition TEXT,
                weight_grams REAL,
                diameter_mm REAL,
                edge TEXT,
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

                -- Updated: Accept both numeric years and XXXX
                CONSTRAINT valid_coin_id_format CHECK (
                    coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-XXXX-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-XXXX-[A-Z]*'
                )
            )
        ''')
        print("✓ Created coins_new table")

        # Copy all existing data (year will be converted from INTEGER to TEXT)
        print("\nCopying existing data...")
        cursor.execute('''
            INSERT INTO coins_new (
                coin_id, year, mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description,
                business_strikes, proof_strikes, total_mintage,
                notes, rarity, source_citation, created_at
            )
            SELECT
                coin_id,
                CAST(year AS TEXT),  -- Convert INTEGER to TEXT
                mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description,
                business_strikes, proof_strikes, total_mintage,
                notes, rarity, source_citation, created_at
            FROM coins
        ''')

        new_count = self.get_row_count(conn, 'coins_new')
        print(f"✓ Copied {new_count} rows to new table")

        # Verify counts match
        if original_count != new_count:
            raise ValueError(f"Row count mismatch! Original: {original_count}, New: {new_count}")

        # Drop old table and rename new one
        print("\nSwapping tables...")
        cursor.execute('DROP TABLE coins')
        cursor.execute('ALTER TABLE coins_new RENAME TO coins')
        print("✓ Schema migration completed")

        # Verify final count
        final_count = self.get_row_count(conn, 'coins')
        print(f"✓ Final coins table: {final_count} rows")

        return final_count

    def run(self, dry_run=False):
        """Execute the schema migration."""
        print("=== XXXX Year Support Schema Migration ===\n")

        if not dry_run:
            self.create_backup()

        conn = sqlite3.connect(self.db_path)

        try:
            final_count = self.migrate_coins_table(conn, dry_run)

            if not dry_run:
                conn.commit()
                print(f"\n✓ Migration completed successfully")
                print(f"✓ Backup: {self.backup_path}")
                print(f"✓ All {final_count} coins preserved")
                print("\nSchema changes:")
                print("  - year: INTEGER → TEXT (accepts YYYY or XXXX)")
                print("  - coin_id: Now accepts XXXX in year position")
                print("\nNext steps:")
                print("  1. Run: uv run python scripts/add_gold_eagle_series.py")
                print("  2. Run: uv run python scripts/export_from_database.py")
                print("  3. Commit changes")
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
        description='Migrate schema to support XXXX year pattern for bullion'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying'
    )

    args = parser.parse_args()

    migration = XXXXSchemaMigration()

    try:
        migration.run(dry_run=args.dry_run)
        return 0
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
