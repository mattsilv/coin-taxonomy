#!/usr/bin/env python3
"""
Add series_code column to series_registry and populate for all series.
Issue #84: Add series_code to all 51 commemorative half dollar entries

Database-first approach:
1. Add series_code column to series_registry if not exists
2. Populate series_code for all coins by extracting from coin_id pattern
3. Export script will then include series_code in JSON output
"""

import sqlite3
import os
from pathlib import Path

# Series code mappings for commemorative half dollars
# Extracted from coin_id format: COUNTRY-CODE-YEAR-MINT
COMMEMORATIVE_SERIES_CODES = {
    "World's Columbian Exposition": "WCOL",
    "Panama-Pacific International Exposition": "PPIE",
    "Illinois Centennial": "ILCN",
    "Maine Centennial": "MECN",
    "Pilgrim Tercentenary": "PILG",
    "Alabama Centennial": "ALCN",
    "Missouri Centennial": "MOCN",
    "Grant Memorial": "GRNT",
    "Monroe Doctrine Centennial": "MNDO",
    "Huguenot-Walloon Tercentenary": "HUGE",
    "California Diamond Jubilee": "CADJ",
    "Fort Vancouver Centennial": "FTVA",
    "Lexington-Concord Sesquicentennial": "LEXC",
    "Stone Mountain Memorial": "STMN",
    "Oregon Trail Memorial": "ORTR",
    "Sesquicentennial of American Independence": "SEAI",
    "Vermont Sesquicentennial": "VTSQ",
    "Hawaiian Sesquicentennial": "HISQ",
    "Daniel Boone Bicentennial": "DNBO",
    "Maryland Tercentenary": "MDTC",
    "Texas Centennial": "TXCN",
    "Arkansas Centennial": "ARCN",
    "California-Pacific Exposition": "CAPE",
    "Connecticut Tercentenary": "CTTC",
    "Hudson, New York, Sesquicentennial": "HUNY",
    "Old Spanish Trail": "OSPT",
    "Albany, New York, Charter": "ALNY",
    "Arkansas-Robinson": "ARRB",
    "Battle of Gettysburg": "GTYB",
    "Bridgeport, Connecticut, Centennial": "BDPT",
    "Cincinnati Music Center": "CNMC",
    "Cleveland Centennial": "CLVC",
    "Columbia, South Carolina, Sesquicentennial": "COSC",
    "Delaware Tercentenary": "DETC",
    "Elgin, Illinois, Centennial": "ELIL",
    "Long Island Tercentenary": "LITC",
    "Lynchburg, Virginia, Sesquicentennial": "LYVA",
    "Norfolk, Virginia, Bicentennial": "NFVA",
    "Providence, Rhode Island, Tercentenary": "PVRI",
    "San Francisco-Oakland Bay Bridge": "SFBB",
    "Wisconsin Territorial Centennial": "WITC",
    "York County, Maine, Tercentenary": "YCME",
    "Battle of Antietam": "ANTM",
    "Roanoke Island": "ROAN",
    "New Rochelle, New York, 250th Anniversary": "NWRC",
    "Booker T. Washington": "BTWH",
    "Iowa Statehood Centennial": "IASC",
    "Carver/Washington": "CARW",
}


def add_series_code_column(db_path: str) -> bool:
    """Add series_code column to series_registry if not exists."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(series_registry)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'series_code' not in columns:
            print("📊 Adding series_code column to series_registry...")
            cursor.execute('''
                ALTER TABLE series_registry
                ADD COLUMN series_code TEXT
            ''')
            conn.commit()
            print("   ✅ Column added")
        else:
            print("   ℹ️  series_code column already exists")

        return True

    except sqlite3.Error as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        conn.close()


def populate_commemorative_codes(db_path: str) -> int:
    """Populate series_code for commemorative half dollars."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    updated = 0
    inserted = 0

    try:
        print("📊 Populating series_code for commemorative half dollars...")

        # Get unique series from coins table
        cursor.execute('''
            SELECT DISTINCT series, MIN(coin_id) as sample_coin
            FROM coins
            WHERE denomination = 'Commemorative Half Dollars'
            GROUP BY series
        ''')

        coin_series = cursor.fetchall()

        for series_name, sample_coin_id in coin_series:
            # Extract series_code from coin_id (format: US-CODE-YEAR-MINT)
            if sample_coin_id and '-' in sample_coin_id:
                parts = sample_coin_id.split('-')
                if len(parts) >= 2:
                    series_code = parts[1]  # The 4-letter code

                    # Check if series exists in registry
                    cursor.execute('''
                        SELECT series_id FROM series_registry
                        WHERE series_name = ? AND denomination = 'Commemorative Half Dollars'
                    ''', (series_name,))

                    existing = cursor.fetchone()

                    if existing:
                        # Update existing entry
                        cursor.execute('''
                            UPDATE series_registry
                            SET series_code = ?
                            WHERE series_name = ? AND denomination = 'Commemorative Half Dollars'
                        ''', (series_code, series_name))
                        updated += 1
                    else:
                        # Insert new entry
                        series_id = f"{series_name}__Commemorative_Half_Dollars"
                        cursor.execute('''
                            INSERT INTO series_registry
                            (series_id, country, series_name, series_code, denomination)
                            VALUES (?, 'US', ?, ?, 'Commemorative Half Dollars')
                        ''', (series_id, series_name, series_code))
                        inserted += 1

                    print(f"   {series_code}: {series_name}")

        conn.commit()
        print(f"\n   ✅ Updated: {updated}, Inserted: {inserted}")
        return updated + inserted

    except sqlite3.Error as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        return 0
    finally:
        conn.close()


def populate_all_series_codes(db_path: str) -> int:
    """Populate series_code for all series by extracting from coin_ids."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    updated = 0
    inserted = 0

    try:
        print("📊 Populating series_code for all coin series...")

        # Get unique series from coins table with sample coin_id
        cursor.execute('''
            SELECT DISTINCT
                series,
                denomination,
                MIN(coin_id) as sample_coin
            FROM coins
            WHERE coin_id LIKE 'US-%'
            GROUP BY series, denomination
            ORDER BY denomination, series
        ''')

        coin_series = cursor.fetchall()

        for series_name, denomination, sample_coin_id in coin_series:
            if not series_name or not sample_coin_id:
                continue

            # Extract series_code from coin_id (format: US-CODE-YEAR-MINT)
            if '-' in sample_coin_id:
                parts = sample_coin_id.split('-')
                if len(parts) >= 2:
                    series_code = parts[1]  # The 4-letter code

                    # Check if series exists in registry
                    cursor.execute('''
                        SELECT series_id, series_code FROM series_registry
                        WHERE series_name = ? AND denomination = ?
                    ''', (series_name, denomination))

                    existing = cursor.fetchone()

                    if existing:
                        if existing[1] != series_code:
                            # Update existing entry
                            cursor.execute('''
                                UPDATE series_registry
                                SET series_code = ?
                                WHERE series_name = ? AND denomination = ?
                            ''', (series_code, series_name, denomination))
                            updated += 1
                    else:
                        # Insert new entry
                        series_id = f"{series_name}__{denomination.replace(' ', '_')}"
                        cursor.execute('''
                            INSERT INTO series_registry
                            (series_id, country, series_name, series_code, denomination)
                            VALUES (?, 'US', ?, ?, ?)
                        ''', (series_id, series_name, series_code, denomination))
                        inserted += 1

        conn.commit()
        print(f"\n   ✅ Updated: {updated}, Inserted: {inserted}")
        return updated + inserted

    except sqlite3.Error as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        return 0
    finally:
        conn.close()


def verify_series_codes(db_path: str):
    """Verify all commemorative half dollar series have codes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("\n📊 Verifying series codes...")

        # Get all commemorative series
        cursor.execute('''
            SELECT series_name, series_code
            FROM series_registry
            WHERE denomination = 'Commemorative Half Dollars'
            ORDER BY series_name
        ''')

        rows = cursor.fetchall()

        missing = []
        for series_name, series_code in rows:
            if not series_code:
                missing.append(series_name)

        if missing:
            print(f"   ⚠️  Missing codes for: {', '.join(missing)}")
        else:
            print(f"   ✅ All {len(rows)} commemorative series have codes")

        # Check total count matches expected (48 base series from coins)
        cursor.execute('''
            SELECT COUNT(DISTINCT series)
            FROM coins
            WHERE denomination = 'Commemorative Half Dollars'
        ''')
        coin_series_count = cursor.fetchone()[0]

        print(f"   📈 Coins table has {coin_series_count} unique series")
        print(f"   📈 Registry has {len(rows)} series with codes")

    finally:
        conn.close()


def main():
    # Find database path
    db_path = 'coins.db'
    if not os.path.exists(db_path):
        db_path = 'database/coins.db'
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return 1

    print(f"🗄️  Using database: {db_path}")

    # Add column if needed
    if not add_series_code_column(db_path):
        return 1

    # Populate all series codes
    count = populate_all_series_codes(db_path)

    # Verify
    verify_series_codes(db_path)

    print(f"\n✅ Done! {count} series processed")
    return 0


if __name__ == "__main__":
    exit(main())
