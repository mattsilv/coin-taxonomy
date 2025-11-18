#!/usr/bin/env python3
"""
Update database schema to allow alphanumeric TYPE codes in coin_id format.

This allows IDs like US-ENG1-XXXX-X instead of requiring exactly 4 letters.
"""

import sqlite3

def update_schema():
    """Update the coins table CHECK constraint to allow alphanumeric TYPE codes."""
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()

    print("📊 Updating schema to allow alphanumeric TYPE codes...")

    # Store view definitions
    view_sql = cursor.execute("""
        SELECT name, sql FROM sqlite_master WHERE type='view'
    """).fetchall()

    # Drop dependent views
    for view_name, _ in view_sql:
        print(f"   Dropping view: {view_name}")
        cursor.execute(f"DROP VIEW IF EXISTS {view_name}")

    # Create new table with updated constraint
    cursor.execute("""
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

            -- Updated: Allow alphanumeric TYPE codes (2-4 characters, letters or numbers)
            CONSTRAINT valid_coin_id_format CHECK (
                coin_id GLOB '[A-Z][A-Z]-[A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                coin_id GLOB '[A-Z][A-Z]-[A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9]-XXXX-[A-Z]*' OR
                coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9]-XXXX-[A-Z]*'
            )
        )
    """)

    # Copy all data from old table to new table
    cursor.execute("""
        INSERT INTO coins_new
        SELECT * FROM coins
    """)

    # Drop old table
    cursor.execute("DROP TABLE coins")

    # Rename new table to old name
    cursor.execute("ALTER TABLE coins_new RENAME TO coins")

    # Recreate views
    for view_name, view_definition in view_sql:
        if view_definition:  # Skip if SQL is None
            print(f"   Recreating view: {view_name}")
            cursor.execute(view_definition)

    conn.commit()
    conn.close()

    print("✅ Schema updated successfully!")
    print("   TYPE codes can now be alphanumeric (e.g., ENG1, ENG2, AGE1, etc.)")
    print(f"   Recreated {len(view_sql)} views")

if __name__ == "__main__":
    update_schema()
