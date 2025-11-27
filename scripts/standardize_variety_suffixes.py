#!/usr/bin/env python3
"""
Migration script to standardize variety suffix patterns (Issue #70)

Migrates coins to use the standard 5-part ID format:
  COUNTRY-TYPE-YEAR-MINT-SUFFIX

Migrations performed:
1. Grant Memorial: US-GRNS-1922-P -> US-GRNT-1922-P-STAR
2. Alabama Centennial: US-ALXX-1921-P -> US-ALCN-1921-P-2X2
3. Missouri Centennial: US-MOSS-1921-P -> US-MOCN-1921-P-2S4
4. Three-Cent Silver: Add -T1/-T2/-T3 suffix based on variety field
"""

import sqlite3
import os
from datetime import datetime


def create_backup(db_path: str) -> str:
    """Create a backup before migration."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/coins_variety_suffix_migration_{timestamp}.db"

    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def migrate_commemorative(cursor, old_id: str, new_id: str, new_series: str, new_variety: str):
    """Migrate a commemorative coin to new ID format."""
    # Check if old ID exists
    cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (old_id,))
    if not cursor.fetchone():
        print(f"  SKIP: {old_id} not found in database")
        return False

    # Check if new ID already exists
    cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (new_id,))
    if cursor.fetchone():
        print(f"  SKIP: {new_id} already exists")
        return False

    # Insert new record with new coin_id
    cursor.execute("""
        INSERT INTO coins (
            coin_id, year, mint, denomination, series, variety,
            composition, weight_grams, diameter_mm, edge, designer,
            obverse_description, reverse_description, business_strikes,
            proof_strikes, total_mintage, notes, rarity, source_citation
        )
        SELECT
            ?, year, mint, denomination, ?, ?,
            composition, weight_grams, diameter_mm, edge, designer,
            obverse_description, reverse_description, business_strikes,
            proof_strikes, total_mintage, notes, rarity, source_citation
        FROM coins WHERE coin_id = ?
    """, (new_id, new_series, new_variety, old_id))

    # Delete old record
    cursor.execute("DELETE FROM coins WHERE coin_id = ?", (old_id,))

    print(f"  MIGRATED: {old_id} -> {new_id}")
    return True


def migrate_three_cent_silver(cursor):
    """Add type suffixes to Three-Cent Silver coins."""
    # Get all Three-Cent Silver coins
    cursor.execute("""
        SELECT coin_id, variety FROM coins
        WHERE coin_id LIKE 'US-TCST-%'
        AND coin_id NOT LIKE '%-T1'
        AND coin_id NOT LIKE '%-T2'
        AND coin_id NOT LIKE '%-T3'
        ORDER BY coin_id
    """)
    coins = cursor.fetchall()

    if not coins:
        print("  No Three-Cent Silver coins need migration")
        return 0

    migrated = 0
    for coin_id, variety in coins:
        # Determine suffix based on variety field
        if variety == "Type I":
            suffix = "T1"
        elif variety == "Type II":
            suffix = "T2"
        elif variety == "Type III":
            suffix = "T3"
        else:
            print(f"  SKIP: {coin_id} has unknown variety '{variety}'")
            continue

        new_id = f"{coin_id}-{suffix}"

        # Check if new ID already exists
        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (new_id,))
        if cursor.fetchone():
            print(f"  SKIP: {new_id} already exists")
            continue

        # Insert new record
        cursor.execute("""
            INSERT INTO coins (
                coin_id, year, mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, business_strikes,
                proof_strikes, total_mintage, notes, rarity, source_citation
            )
            SELECT
                ?, year, mint, denomination, 'Silver Three-Cent', variety,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, business_strikes,
                proof_strikes, total_mintage, notes, rarity, source_citation
            FROM coins WHERE coin_id = ?
        """, (new_id, coin_id))

        # Delete old record
        cursor.execute("DELETE FROM coins WHERE coin_id = ?", (coin_id,))

        print(f"  MIGRATED: {coin_id} -> {new_id}")
        migrated += 1

    return migrated


def main():
    print("=" * 60)
    print("Variety Suffix Standardization Migration (Issue #70)")
    print("=" * 60)

    db_path = "database/coins.db"
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return

    # Create backup
    os.makedirs("backups", exist_ok=True)
    backup_path = create_backup(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Begin transaction
        cursor.execute("BEGIN TRANSACTION")

        # 1. Grant Memorial migration
        print("\n[1/4] Grant Memorial (GRNS -> GRNT-STAR)")
        migrate_commemorative(
            cursor,
            old_id="US-GRNS-1922-P",
            new_id="US-GRNT-1922-P-STAR",
            new_series="Grant Memorial",
            new_variety="With Star"
        )

        # 2. Alabama Centennial migration
        print("\n[2/4] Alabama Centennial (ALXX -> ALCN-2X2)")
        migrate_commemorative(
            cursor,
            old_id="US-ALXX-1921-P",
            new_id="US-ALCN-1921-P-2X2",
            new_series="Alabama Centennial",
            new_variety="2X2"
        )

        # 3. Missouri Centennial migration
        print("\n[3/4] Missouri Centennial (MOSS -> MOCN-2S4)")
        migrate_commemorative(
            cursor,
            old_id="US-MOSS-1921-P",
            new_id="US-MOCN-1921-P-2S4",
            new_series="Missouri Centennial",
            new_variety="2S4"
        )

        # 4. Three-Cent Silver migration
        print("\n[4/4] Three-Cent Silver (add -T1/-T2/-T3 suffixes)")
        three_cent_count = migrate_three_cent_silver(cursor)

        # Commit transaction
        conn.commit()

        # Verify results
        print("\n" + "=" * 60)
        print("VERIFICATION")
        print("=" * 60)

        # Check commemorative migrations
        print("\nCommemorative Half Dollars:")
        cursor.execute("""
            SELECT coin_id, series, variety FROM coins
            WHERE coin_id LIKE 'US-GRNT-1922%'
               OR coin_id LIKE 'US-ALCN-1921%'
               OR coin_id LIKE 'US-MOCN-1921%'
            ORDER BY coin_id
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]} | {row[1]} | {row[2]}")

        # Check Three-Cent Silver migrations
        print(f"\nThree-Cent Silver ({three_cent_count} migrated):")
        cursor.execute("""
            SELECT coin_id, series, variety FROM coins
            WHERE coin_id LIKE 'US-TCST-%'
            ORDER BY coin_id
            LIMIT 10
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]} | {row[1]} | {row[2]}")
        if three_cent_count > 10:
            print(f"  ... and {three_cent_count - 10} more")

        # Check no orphaned records
        print("\nOrphaned records check:")
        cursor.execute("""
            SELECT coin_id FROM coins
            WHERE coin_id IN ('US-GRNS-1922-P', 'US-ALXX-1921-P', 'US-MOSS-1921-P')
        """)
        orphans = cursor.fetchall()
        if orphans:
            print(f"  WARNING: Found {len(orphans)} orphaned records!")
            for row in orphans:
                print(f"    {row[0]}")
        else:
            print("  OK - No orphaned records found")

        print("\n" + "=" * 60)
        print("Migration complete!")
        print(f"Backup available at: {backup_path}")
        print("Run 'uv run python scripts/export_from_database.py' to export JSON files")
        print("=" * 60)

    except Exception as e:
        conn.rollback()
        print(f"\nERROR: {e}")
        print("Transaction rolled back")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
