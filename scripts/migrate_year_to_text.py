#!/usr/bin/env python3
"""
Migrate year column from INTEGER to TEXT to support XXXX pattern for random year bullion.

This migration changes the year field to accept either:
- 4-digit numeric years (1773-9999)
- "XXXX" placeholder for random year bullion products

The coin_id CHECK constraint is also updated to accept XXXX in the year position.
"""

import sqlite3
import sys
from pathlib import Path

def migrate_year_column():
    """Migrate year from INTEGER to TEXT with validation."""

    db_path = Path(__file__).parent.parent / 'coins.db'

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        sys.exit(1)

    print(f"📊 Migrating database: {db_path}")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        # Check current row count
        cursor.execute("SELECT COUNT(*) FROM coins")
        row_count = cursor.fetchone()[0]
        print(f"📈 Current coins in database: {row_count}")

        # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
        print("🔨 Creating new table with TEXT year field...")

        conn.executescript('''
            -- Create temporary table with new schema
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
                grade TEXT,
                composition TEXT,
                weight_grams REAL,
                diameter_mm REAL,
                thickness_mm REAL,
                edge TEXT,
                designer TEXT,
                obverse_description TEXT,
                reverse_description TEXT,
                business_strikes INTEGER,
                proof_strikes INTEGER,
                uncirculated_strikes INTEGER,
                mint_state_strikes INTEGER,
                special_strikes INTEGER,
                total_mintage INTEGER,
                notes TEXT,
                rarity TEXT CHECK(rarity IN ('key', 'semi-key', 'common', 'scarce', NULL)),
                source_citation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Multi-country coin ID format: COUNTRY-TYPE-YEAR-MINT
                -- Now supports XXXX for random year bullion
                CONSTRAINT valid_coin_id_format CHECK (
                    coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-XXXX-[A-Z]*' OR
                    coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-XXXX-[A-Z]*'
                )
            );
        ''')

        print("📋 Copying data with year cast to TEXT...")
        cursor.execute('''
            INSERT INTO coins_new SELECT
                coin_id,
                CAST(year AS TEXT) as year,
                mint,
                denomination,
                series,
                variety,
                grade,
                composition,
                weight_grams,
                diameter_mm,
                thickness_mm,
                edge,
                designer,
                obverse_description,
                reverse_description,
                business_strikes,
                proof_strikes,
                uncirculated_strikes,
                mint_state_strikes,
                special_strikes,
                total_mintage,
                notes,
                rarity,
                source_citation,
                created_at
            FROM coins
        ''')

        # Verify data copied correctly
        cursor.execute("SELECT COUNT(*) FROM coins_new")
        new_row_count = cursor.fetchone()[0]

        if new_row_count != row_count:
            print(f"❌ Error: Row count mismatch! Original: {row_count}, New: {new_row_count}")
            conn.rollback()
            sys.exit(1)

        print(f"✅ Data copied successfully: {new_row_count} rows")

        # Drop old table and rename new table
        print("🔄 Swapping tables...")
        conn.executescript('''
            DROP TABLE coins;
            ALTER TABLE coins_new RENAME TO coins;
        ''')

        # Recreate indexes
        print("📇 Recreating indexes...")
        conn.executescript('''
            CREATE INDEX idx_coin_country ON coins(substr(coin_id, 1, 2));
            CREATE INDEX idx_coin_year ON coins(year);
            CREATE INDEX idx_coin_denomination ON coins(denomination);
            CREATE INDEX idx_coin_series ON coins(series);
            CREATE INDEX idx_coin_rarity ON coins(rarity);
        ''')

        # Commit all changes
        conn.commit()

        # Verify final state
        cursor.execute("SELECT COUNT(*) FROM coins")
        final_count = cursor.fetchone()[0]

        # Test the new constraint by attempting to insert a test XXXX coin
        print("🧪 Testing XXXX pattern support...")
        try:
            cursor.execute('''
                INSERT INTO coins (coin_id, year, mint, denomination)
                VALUES ('US-TEST-XXXX-X', 'XXXX', 'X', 'Test')
            ''')
            cursor.execute("DELETE FROM coins WHERE coin_id = 'US-TEST-XXXX-X'")
            conn.commit()
            print("✅ XXXX pattern validation: PASSED")
        except sqlite3.IntegrityError as e:
            print(f"❌ XXXX pattern validation: FAILED - {e}")
            conn.rollback()

        print(f"\n✅ Migration complete!")
        print(f"📊 Final coin count: {final_count}")
        print(f"✨ Database now supports both numeric years (1773-9999) and 'XXXX' for random year bullion")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 70)
    print("Database Migration: Year INTEGER → TEXT (with XXXX support)")
    print("=" * 70)
    print()

    response = input("⚠️  This will modify the database structure. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Migration cancelled")
        sys.exit(0)

    print()
    migrate_year_column()
