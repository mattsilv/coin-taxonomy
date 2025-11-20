#!/usr/bin/env python3
"""
Fix Canadian Maple Leaf Issues (Issue #68)

Corrections based on expert research report:
1. Gold Maple Leaf: Remove incorrect 1/2 oz (1982-1985), should start 1986
2. Gold Maple Leaf: Remove incorrect 1/20 oz (1982-1992), should start 1993
3. Gold Maple Leaf: Add missing 1 gram size (2014-2024)
4. Platinum Maple Leaf: Add fractional sizes (1988-2002)
5. Platinum Maple Leaf: Add 2010 (check if exists)
6. Update specifications to match research data
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import shutil


def backup_database():
    """Create backup before migration."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)

    source = Path('database/coins.db')
    backup = backup_dir / f'coins_backup_maple_fix_{timestamp}.db'

    shutil.copy(source, backup)
    print(f"✅ Database backed up to {backup}")
    return backup


def remove_incorrect_gold_fractionals(conn):
    """Remove Gold Maple Leaf fractionals that started too early."""
    cursor = conn.cursor()

    print("\n🔧 Fixing Gold Maple Leaf fractional start dates...")

    # Remove 1/2 oz from 1982-1985 (should start 1986)
    cursor.execute("""
        DELETE FROM coins
        WHERE series = 'Gold Maple Leaf'
          AND denomination = 'Gold Maple Leaf 1/2 oz'
          AND CAST(year AS INTEGER) BETWEEN 1982 AND 1985
    """)
    removed_half = cursor.rowcount
    print(f"  ✅ Removed {removed_half} incorrect 1/2 oz entries (1982-1985)")

    # Remove 1/20 oz from 1982-1992 (should start 1993)
    cursor.execute("""
        DELETE FROM coins
        WHERE series = 'Gold Maple Leaf'
          AND denomination = 'Gold Maple Leaf 1/20 oz'
          AND CAST(year AS INTEGER) BETWEEN 1982 AND 1992
    """)
    removed_twentieth = cursor.rowcount
    print(f"  ✅ Removed {removed_twentieth} incorrect 1/20 oz entries (1982-1992)")

    return removed_half + removed_twentieth


def add_gold_1gram_size(conn):
    """Add missing Gold Maple Leaf 1 gram size (2014-2024)."""
    cursor = conn.cursor()

    print("\n➕ Adding Gold Maple Leaf 1 gram size (2014-2024)...")

    added = 0
    for year in range(2014, 2025):
        coin_id = f"CA-GMPL-{year}-P-1g"

        # Check if already exists
        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
        if cursor.fetchone():
            continue

        cursor.execute("""
            INSERT INTO coins (
                coin_id, year, mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description,
                business_strikes, proof_strikes, total_mintage,
                notes, rarity, source_citation, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin_id,
            str(year),
            'P',
            'Gold Maple Leaf 1 gram',
            'Gold Maple Leaf',
            None,
            '.9999 Au',
            1.0,
            None,  # Diameter not specified in research
            'Reeded',
            'Walter Ott (reverse maple leaf)',
            'Queen Elizabeth II (Susanna Blunt 2003-2023) / King Charles III (Steven Rosati 2024+)',
            'Sugar maple leaf',
            None,
            None,
            None,
            f'Fractional 1 gram. Introduced 2014. Security features: Radial lines, micro-engraving (2013+)',
            'common',
            'RCM specifications, Issue #68 research',
            datetime.now().isoformat()
        ))
        added += 1

    print(f"  ✅ Added {added} 1 gram Gold Maple Leaf entries")
    return added


def add_platinum_fractionals(conn):
    """Add missing Platinum Maple Leaf fractional sizes (1988-2002)."""
    cursor = conn.cursor()

    print("\n➕ Adding Platinum Maple Leaf fractional sizes (1988-2002)...")

    # Fractional specifications from research
    fractionals = [
        {'size': '1/2 oz', 'weight': 15.59, 'diameter': 25.0, 'face_value': 150, 'code': '12oz'},
        {'size': '1/4 oz', 'weight': 7.8, 'diameter': 20.0, 'face_value': 75, 'code': '14oz'},
        {'size': '1/10 oz', 'weight': 3.13, 'diameter': 16.0, 'face_value': 30, 'code': '110oz'},
        {'size': '1/20 oz', 'weight': 1.555, 'diameter': 13.9, 'face_value': None, 'code': '120oz'},
    ]

    # Special 1/15 oz only in 1994
    fractionals_1994 = [
        {'size': '1/15 oz', 'weight': 2.07, 'diameter': None, 'face_value': None, 'code': '115oz'},
    ]

    added = 0

    # Add standard fractionals 1988-2002
    for year in range(1988, 2003):
        for frac in fractionals:
            coin_id = f"CA-PMPL-{year}-P-{frac['code']}"

            # Check if already exists
            cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
            if cursor.fetchone():
                continue

            notes = f"Fractional {frac['size']}. Discontinued 2002. Purity: .9995 Pt (1988-2002)"

            cursor.execute("""
                INSERT INTO coins (
                    coin_id, year, mint, denomination, series, variety,
                    composition, weight_grams, diameter_mm, edge, designer,
                    obverse_description, reverse_description,
                    business_strikes, proof_strikes, total_mintage,
                    notes, rarity, source_citation, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin_id,
                str(year),
                'P',
                f'Platinum Maple Leaf {frac["size"]}',
                'Platinum Maple Leaf',
                None,
                '.9995 Pt',
                frac['weight'],
                frac['diameter'],
                'Serrated',
                'Walter Ott (reverse maple leaf)',
                'Queen Elizabeth II',
                'Sugar maple leaf',
                None,
                None,
                None,
                notes,
                'scarce',
                'RCM specifications, Issue #68 research',
                datetime.now().isoformat()
            ))
            added += 1

    # Add special 1/15 oz for 1994
    for frac in fractionals_1994:
        coin_id = f"CA-PMPL-1994-P-{frac['code']}"

        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, year, mint, denomination, series, variety,
                    composition, weight_grams, diameter_mm, edge, designer,
                    obverse_description, reverse_description,
                    business_strikes, proof_strikes, total_mintage,
                    notes, rarity, source_citation, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin_id,
                '1994',
                'P',
                f'Platinum Maple Leaf {frac["size"]}',
                'Platinum Maple Leaf',
                None,
                '.9995 Pt',
                frac['weight'],
                frac['diameter'],
                'Serrated',
                'Walter Ott (reverse maple leaf)',
                'Queen Elizabeth II',
                'Sugar maple leaf',
                None,
                None,
                None,
                f'Fractional {frac["size"]}. Only minted in 1994. Purity: .9995 Pt',
                'key',
                'RCM specifications, Issue #68 research',
                datetime.now().isoformat()
            ))
            added += 1

    print(f"  ✅ Added {added} fractional Platinum Maple Leaf entries")
    return added


def add_platinum_2010(conn):
    """Add Platinum Maple Leaf 2010 if missing."""
    cursor = conn.cursor()

    print("\n➕ Checking Platinum Maple Leaf 2010...")

    coin_id = "CA-PMPL-2010-P"
    cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))

    if cursor.fetchone():
        print("  ℹ️  2010 Platinum Maple Leaf already exists")
        return 0

    # Research suggests production resumed in 2009, so 2010 should exist
    cursor.execute("""
        INSERT INTO coins (
            coin_id, year, mint, denomination, series, variety,
            composition, weight_grams, diameter_mm, edge, designer,
            obverse_description, reverse_description,
            business_strikes, proof_strikes, total_mintage,
            notes, rarity, source_citation, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        coin_id,
        '2010',
        'P',
        'Platinum Maple Leaf',
        'Platinum Maple Leaf',
        None,
        '.9999 Pt',
        31.103,
        30.0,
        'Serrated',
        'Walter Ott (reverse maple leaf)',
        'Queen Elizabeth II (Susanna Blunt)',
        'Sugar maple leaf',
        None,
        None,
        None,
        'Modern era production (2009+). Purity: .9999 Pt. Only 1 oz size',
        'common',
        'RCM specifications, Issue #68 research',
        datetime.now().isoformat()
    ))

    print("  ✅ Added 2010 Platinum Maple Leaf")
    return 1


def update_specifications(conn):
    """Update specifications to match research data."""
    cursor = conn.cursor()

    print("\n🔧 Updating specifications to match research...")

    # Update 1 oz Gold Maple Leaf weights to exact specs
    cursor.execute("""
        UPDATE coins
        SET weight_grams = 31.1030,
            diameter_mm = 30.0,
            notes = CASE
                WHEN CAST(year AS INTEGER) < 1982 THEN '.999 fine (1979-Oct 1982)'
                WHEN CAST(year AS INTEGER) >= 1982 THEN '.9999 fine (Nov 1982+). Security features: Radial lines, micro-engraving (2013+)'
            END
        WHERE series = 'Gold Maple Leaf'
          AND denomination = 'Gold Maple Leaf'
          AND year NOT LIKE 'XXXX'
    """)
    print(f"  ✅ Updated {cursor.rowcount} Gold Maple Leaf 1 oz specs")

    # Update 1 oz Silver Maple Leaf specs
    cursor.execute("""
        UPDATE coins
        SET weight_grams = 31.11,
            diameter_mm = 38.0,
            notes = CASE
                WHEN CAST(year AS INTEGER) >= 2018 THEN '.9999 fine. Security features: Radial lines (2014+), micro-engraving (2015+), MINTSHIELD™ (2018+)'
                WHEN CAST(year AS INTEGER) >= 2014 THEN '.9999 fine. Security features: Radial lines (2014+), micro-engraving (2015+)'
                ELSE '.9999 fine silver'
            END
        WHERE series = 'Silver Maple Leaf'
          AND denomination = 'Silver Maple Leaf'
          AND year NOT LIKE 'XXXX'
    """)
    print(f"  ✅ Updated {cursor.rowcount} Silver Maple Leaf specs")

    # Update 1 oz Platinum Maple Leaf specs
    cursor.execute("""
        UPDATE coins
        SET weight_grams = 31.110,
            diameter_mm = 30.0,
            composition = CASE
                WHEN CAST(year AS INTEGER) <= 2002 THEN '.9995 Pt'
                WHEN CAST(year AS INTEGER) >= 2009 THEN '.9999 Pt'
            END,
            notes = CASE
                WHEN CAST(year AS INTEGER) <= 2002 THEN 'Purity: .9995 Pt (1988-2002). Fractional sizes available'
                WHEN CAST(year AS INTEGER) >= 2009 THEN 'Purity: .9999 Pt (2009+). Only 1 oz size. Security features: Radial lines, micro-engraving'
            END
        WHERE series = 'Platinum Maple Leaf'
          AND denomination = 'Platinum Maple Leaf'
          AND year NOT LIKE 'XXXX'
    """)
    print(f"  ✅ Updated {cursor.rowcount} Platinum Maple Leaf specs")

    # Update 1 oz Palladium Maple Leaf specs
    cursor.execute("""
        UPDATE coins
        SET weight_grams = 31.103,
            diameter_mm = 33.0,
            composition = '.9995 Pd',
            notes = CASE
                WHEN year = '2005' THEN 'Inaugural issue. Mintage: 62,919. Highly collectible. Purity: .9995 Pd'
                WHEN CAST(year AS INTEGER) BETWEEN 2006 AND 2007 THEN 'Limited production era (2005-2007). Purity: .9995 Pd'
                WHEN year = '2009' THEN 'Brief production resumption. Purity: .9995 Pd'
                WHEN CAST(year AS INTEGER) >= 2015 THEN 'Modern continuous production (2015+). Purity: .9995 Pd. Security features: Radial lines, micro-engraving'
            END
        WHERE series = 'Palladium Maple Leaf'
          AND denomination = 'Palladium Maple Leaf'
          AND year NOT LIKE 'XXXX'
    """)
    print(f"  ✅ Updated {cursor.rowcount} Palladium Maple Leaf specs")

    return True


def verify_corrections(conn):
    """Verify all corrections were applied."""
    cursor = conn.cursor()

    print("\n📊 Verification Summary:")

    # Check Gold 1/2 oz start date
    cursor.execute("""
        SELECT MIN(CAST(year AS INTEGER)) as min_year, COUNT(*) as count
        FROM coins
        WHERE series = 'Gold Maple Leaf'
          AND denomination = 'Gold Maple Leaf 1/2 oz'
    """)
    result = cursor.fetchone()
    print(f"  Gold 1/2 oz: Starts {result[0]} (should be 1986), {result[1]} entries")

    # Check Gold 1/20 oz start date
    cursor.execute("""
        SELECT MIN(CAST(year AS INTEGER)) as min_year, COUNT(*) as count
        FROM coins
        WHERE series = 'Gold Maple Leaf'
          AND denomination = 'Gold Maple Leaf 1/20 oz'
    """)
    result = cursor.fetchone()
    print(f"  Gold 1/20 oz: Starts {result[0]} (should be 1993), {result[1]} entries")

    # Check Gold 1 gram
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM coins
        WHERE series = 'Gold Maple Leaf'
          AND denomination = 'Gold Maple Leaf 1 gram'
    """)
    result = cursor.fetchone()
    print(f"  Gold 1 gram: {result[0]} entries (should be 11 for 2014-2024)")

    # Check Platinum fractionals
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM coins
        WHERE series = 'Platinum Maple Leaf'
          AND denomination LIKE '%oz'
          AND CAST(year AS INTEGER) BETWEEN 1988 AND 2002
    """)
    result = cursor.fetchone()
    print(f"  Platinum fractionals (1988-2002): {result[0]} entries")

    # Check Platinum 2010
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM coins
        WHERE series = 'Platinum Maple Leaf'
          AND year = '2010'
    """)
    result = cursor.fetchone()
    print(f"  Platinum 2010: {result[0]} entry (should be 1)")

    # Total Canadian Maple Leaf count
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM coins
        WHERE series LIKE '%Maple Leaf%'
          AND coin_id LIKE 'CA-%'
    """)
    result = cursor.fetchone()
    print(f"\n  Total Canadian Maple Leaf entries: {result[0]}")


def main():
    """Execute Canadian Maple Leaf corrections."""
    print("🚀 Fixing Canadian Maple Leaf Issues (Issue #68)")
    print("=" * 60)

    # Backup database
    backup_path = backup_database()

    try:
        # Connect to database
        conn = sqlite3.connect('database/coins.db')

        # Run corrections
        removed = remove_incorrect_gold_fractionals(conn)
        added_1g = add_gold_1gram_size(conn)
        added_pt_frac = add_platinum_fractionals(conn)
        added_pt_2010 = add_platinum_2010(conn)
        update_specifications(conn)

        # Commit changes
        conn.commit()

        # Verify results
        verify_corrections(conn)

        conn.close()

        print("\n✨ Corrections Complete!")
        print(f"  Removed: {removed} incorrect entries")
        print(f"  Added: {added_1g + added_pt_frac + added_pt_2010} new entries")
        print("\nNext steps:")
        print("  1. Run export: uv run python scripts/export_from_database.py")
        print("  2. Test validation: uv run python scripts/validate.py")
        print("  3. Review changes and commit")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print(f"Restore from backup: {backup_path}")
        raise


if __name__ == "__main__":
    main()
