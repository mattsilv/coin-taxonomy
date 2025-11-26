#!/usr/bin/env python3
"""
Migration script to add complete Morgan Dollar series (1878-1904, 1921)

This script implements the comprehensive mintage data from Issue #69,
adding ~98 Morgan Dollar entries covering the complete series with
accurate mintages from the user's spreadsheet.

Data source: docs/external-metadata/morgan-dollars.xlsx
"""

import sqlite3
import json
import os
from datetime import datetime


def main():
    print("Morgan Dollar Series Migration (1878-1904, 1921)")
    print("=" * 60)
    print("Data source: Issue #69 / morgan-dollars.xlsx")

    # Database connection
    db_path = "database/coins.db"
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check for existing Morgan dollars
        cursor.execute("SELECT COUNT(*) FROM coins WHERE series = 'morgan_dollar'")
        existing_count = cursor.fetchone()[0]
        if existing_count > 0:
            print(f"\nFound {existing_count} existing Morgan Dollar records")
            print("Removing existing records before fresh import...")
            cursor.execute("DELETE FROM coins WHERE series = 'morgan_dollar'")
            print(f"Removed {existing_count} records")

        # Morgan Dollar specifications
        composition = {
            "alloy_name": "90% Silver",
            "silver": 0.90,
            "copper": 0.10
        }
        weight_grams = 26.73
        diameter_mm = 38.1

        # Complete mintage data from spreadsheet
        # Format: (year, mint, variety_suffix): mintage
        mintage_data = {
            # 1878 - First year with tail feather varieties
            (1878, 'P', '8TF'): 749500,
            (1878, 'P', '7TF'): 9759300,
            (1878, 'CC', None): 2212000,
            (1878, 'S', None): 9774000,

            # 1879
            (1879, 'P', None): 14806000,
            (1879, 'CC', None): 756000,
            (1879, 'O', None): 2887000,
            (1879, 'S', None): 9110000,

            # 1880
            (1880, 'P', None): 12600000,
            (1880, 'CC', None): 591000,
            (1880, 'O', None): 5305000,
            (1880, 'S', None): 8900000,

            # 1881
            (1881, 'P', None): 9162991,
            (1881, 'CC', None): 296000,
            (1881, 'O', None): 5708000,
            (1881, 'S', None): 12760000,

            # 1882
            (1882, 'P', None): 11100000,
            (1882, 'CC', None): 1133000,
            (1882, 'O', None): 6090000,
            (1882, 'S', None): 9250000,

            # 1883
            (1883, 'P', None): 12290000,
            (1883, 'CC', None): 1204000,
            (1883, 'O', None): 8725000,
            (1883, 'S', None): 6250000,

            # 1884
            (1884, 'P', None): 14070000,
            (1884, 'CC', None): 1136000,
            (1884, 'O', None): 9730000,
            (1884, 'S', None): 3200000,

            # 1885
            (1885, 'P', None): 17787000,
            (1885, 'CC', None): 228000,
            (1885, 'O', None): 9185000,
            (1885, 'S', None): 1497000,

            # 1886 - No Carson City
            (1886, 'P', None): 19963000,
            (1886, 'O', None): 10710000,
            (1886, 'S', None): 750000,

            # 1887 - No Carson City
            (1887, 'P', None): 20290000,
            (1887, 'O', None): 11550000,
            (1887, 'S', None): 1771000,

            # 1888 - No Carson City
            (1888, 'P', None): 19183000,
            (1888, 'O', None): 12150000,
            (1888, 'S', None): 657000,

            # 1889 - Carson City returns
            (1889, 'P', None): 21726000,
            (1889, 'CC', None): 350000,
            (1889, 'O', None): 11875000,
            (1889, 'S', None): 700000,

            # 1890
            (1890, 'P', None): 16802000,
            (1890, 'CC', None): 2309041,
            (1890, 'O', None): 10701000,
            (1890, 'S', None): 8230373,

            # 1891
            (1891, 'P', None): 8693556,
            (1891, 'CC', None): 1618000,
            (1891, 'O', None): 7954529,
            (1891, 'S', None): 5296000,

            # 1892
            (1892, 'P', None): 1036000,
            (1892, 'CC', None): 1352000,
            (1892, 'O', None): 2744000,
            (1892, 'S', None): 1200000,

            # 1893 - Last Carson City year
            (1893, 'P', None): 378000,
            (1893, 'CC', None): 677000,
            (1893, 'O', None): 300000,
            (1893, 'S', None): 100000,  # KEY DATE - lowest circulation strike

            # 1894 - No Carson City
            (1894, 'P', None): 110000,
            (1894, 'O', None): 1723000,
            (1894, 'S', None): 1260000,

            # 1895 - Includes proof-only Philadelphia
            (1895, 'P', None): 12000,  # KEY DATE - proofs only, rarest Morgan
            (1895, 'O', None): 450000,
            (1895, 'S', None): 400000,

            # 1896
            (1896, 'P', None): 9976000,
            (1896, 'O', None): 4900000,
            (1896, 'S', None): 5000000,

            # 1897
            (1897, 'P', None): 2822000,
            (1897, 'O', None): 4004000,
            (1897, 'S', None): 5825000,

            # 1898
            (1898, 'P', None): 5884000,
            (1898, 'O', None): 4400000,
            (1898, 'S', None): 4102000,

            # 1899
            (1899, 'P', None): 330000,
            (1899, 'O', None): 2562000,
            (1899, 'S', None): 8830000,

            # 1900
            (1900, 'P', None): 12590000,
            (1900, 'O', None): 3540000,
            (1900, 'S', None): 6962000,

            # 1901
            (1901, 'P', None): 13320000,
            (1901, 'O', None): 2284000,
            (1901, 'S', None): 7994000,

            # 1902
            (1902, 'P', None): 8636000,
            (1902, 'O', None): 1530000,
            (1902, 'S', None): 4652000,

            # 1903
            (1903, 'P', None): 4450000,
            (1903, 'O', None): 1241000,
            (1903, 'S', None): 2788000,

            # 1904 - Last year before hiatus (no San Francisco)
            (1904, 'P', None): 3720000,
            (1904, 'O', None): 2304000,

            # 1921 - Post-Pittman Act revival (includes first Denver)
            (1921, 'P', None): 44690000,
            (1921, 'D', None): 20345000,
            (1921, 'S', None): 21695000,
        }

        # Key dates and semi-key dates for rarity classification
        key_dates = {
            # Key dates (very low mintage or high collector demand)
            (1893, 'S'): 'key',      # 100,000 - lowest circulation strike
            (1895, 'P'): 'key',      # 12,000 - proof-only, rarest Morgan
            (1895, 'O'): 'key',      # 450,000
            (1889, 'CC'): 'key',     # 350,000 - famous key date
            (1879, 'CC'): 'key',     # 756,000
            (1881, 'CC'): 'key',     # 296,000
            (1885, 'CC'): 'key',     # 228,000

            # Semi-key dates
            (1892, 'S'): 'semi-key',   # 1,200,000
            (1894, 'P'): 'semi-key',   # 110,000
            (1895, 'S'): 'semi-key',   # 400,000
            (1899, 'P'): 'semi-key',   # 330,000
            (1893, 'O'): 'semi-key',   # 300,000
            (1893, 'P'): 'semi-key',   # 378,000
            (1880, 'CC'): 'semi-key',  # 591,000
            (1884, 'CC'): 'semi-key',  # 1,136,000
        }

        # Notes for special coins
        special_notes = {
            (1878, 'P', '8TF'): "First Morgan Dollar design with 8 tail feathers on eagle",
            (1878, 'P', '7TF'): "Revised design with 7 tail feathers, standard for series",
            (1893, 'S'): "Lowest circulation strike Morgan - classic key date",
            (1895, 'P'): "Proof-only year - rarest of all Morgan dollars (12,000 proofs)",
            (1889, 'CC'): "Famous Carson City key date - few survivors outside GSA hoards",
            (1879, 'CC'): "Carson City key date",
            (1881, 'CC'): "Carson City key date - very low mintage",
            (1885, 'CC'): "Carson City key date - lowest CC mintage",
            (1921, 'P'): "Post-Pittman Act revival - last year of Morgan production",
            (1921, 'D'): "First and only Denver Morgan Dollar",
            (1921, 'S'): "Post-Pittman Act - final San Francisco Morgan",
        }

        # Obverse and reverse descriptions (same for all Morgans)
        obverse_desc = "Liberty head facing left wearing Phrygian cap with 'LIBERTY' headband, surrounded by cotton and wheat. 'E PLURIBUS UNUM' above, date below, 13 stars around border."
        reverse_desc = "Heraldic eagle with wings spread holding olive branch and arrows, 'UNITED STATES OF AMERICA' above, 'ONE DOLLAR' below, 'IN GOD WE TRUST' on ribbon."

        print(f"\nInserting {len(mintage_data)} Morgan Dollar records...")

        inserted_count = 0

        for (year, mint, variety_suffix), mintage in mintage_data.items():
            # Build coin_id with optional suffix
            if variety_suffix:
                coin_id = f"US-MOGD-{year}-{mint}-{variety_suffix}"
            else:
                coin_id = f"US-MOGD-{year}-{mint}"

            # Determine rarity
            rarity_key = (year, mint)
            rarity = key_dates.get(rarity_key, None)

            # Get special notes
            notes_key = (year, mint, variety_suffix) if variety_suffix else (year, mint)
            notes = special_notes.get(notes_key, "")
            if not notes and variety_suffix is None:
                notes_key = (year, mint)
                notes = special_notes.get(notes_key, "")

            # Build common names
            common_names = ["Morgan Dollar", "Morgan Silver Dollar"]
            if mint == 'CC':
                common_names.append("Carson City Morgan")
            if year == 1921:
                common_names.append("1921 Morgan")
            if variety_suffix == '8TF':
                common_names.append("8 Tail Feathers Morgan")
            elif variety_suffix == '7TF':
                common_names.append("7 Tail Feathers Morgan")

            # Build identification keywords
            keywords = ["morgan", "dollar", "silver", "liberty", "eagle"]
            if mint == 'CC':
                keywords.extend(["carson", "city"])
            if variety_suffix:
                keywords.extend(["tail", "feathers", variety_suffix.lower()])

            # Build distinguishing features
            features = [
                "Liberty head by George T. Morgan",
                "90% silver dollar",
                f"{mint} mint mark" if mint != 'P' else "No mint mark (Philadelphia)"
            ]
            if variety_suffix == '8TF':
                features.append("Eight tail feathers on eagle (first design)")
            elif variety_suffix == '7TF':
                features.append("Seven tail feathers on eagle (standard design)")
            if year == 1895 and mint == 'P':
                features.append("Proof-only issue - no business strikes")

            # Insert record - using actual database schema columns
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, year, mint, denomination, series,
                    variety, composition, weight_grams, diameter_mm,
                    business_strikes, notes, rarity,
                    obverse_description, reverse_description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin_id,
                str(year),  # year is TEXT in schema
                mint,
                "Dollars",
                "morgan_dollar",
                variety_suffix,  # variety column for suffix
                json.dumps(composition),
                weight_grams,
                diameter_mm,
                mintage,
                notes,
                rarity,
                obverse_desc,
                reverse_desc
            ))

            inserted_count += 1
            if inserted_count % 20 == 0:
                print(f"  Processed {inserted_count} records...")

        # Commit changes
        conn.commit()
        print(f"\nSuccessfully added {inserted_count} Morgan Dollar records")

        # Verification queries
        print("\n" + "=" * 60)
        print("VERIFICATION")
        print("=" * 60)

        # Total count
        cursor.execute("SELECT COUNT(*) FROM coins WHERE series = 'morgan_dollar'")
        final_count = cursor.fetchone()[0]
        print(f"\nTotal Morgan Dollars in database: {final_count}")

        # Mint breakdown
        cursor.execute("""
            SELECT mint, COUNT(*) as count
            FROM coins
            WHERE series = 'morgan_dollar'
            GROUP BY mint
            ORDER BY count DESC
        """)
        print("\nMint breakdown:")
        for mint, count in cursor.fetchall():
            print(f"  {mint}: {count} coins")

        # Rarity breakdown
        cursor.execute("""
            SELECT rarity, COUNT(*) as count
            FROM coins
            WHERE series = 'morgan_dollar'
            GROUP BY rarity
            ORDER BY
                CASE rarity
                    WHEN 'key' THEN 1
                    WHEN 'semi-key' THEN 2
                    ELSE 3
                END
        """)
        print("\nRarity breakdown:")
        for rarity, count in cursor.fetchall():
            rarity_display = rarity if rarity else "common"
            print(f"  {rarity_display}: {count} coins")

        # Key dates
        cursor.execute("""
            SELECT coin_id, business_strikes, rarity
            FROM coins
            WHERE series = 'morgan_dollar'
              AND rarity = 'key'
            ORDER BY business_strikes
        """)
        print("\nKey dates (by mintage):")
        for coin_id, mintage, rarity in cursor.fetchall():
            print(f"  {coin_id}: {mintage:,}")

        # Year range
        cursor.execute("""
            SELECT MIN(year), MAX(year)
            FROM coins
            WHERE series = 'morgan_dollar'
        """)
        min_year, max_year = cursor.fetchone()
        print(f"\nYear range: {min_year}-{max_year}")

        # Total mintage
        cursor.execute("""
            SELECT SUM(business_strikes)
            FROM coins
            WHERE series = 'morgan_dollar'
        """)
        total_mintage = cursor.fetchone()[0]
        print(f"Total mintage: {total_mintage:,}")

        # Database total
        cursor.execute("SELECT COUNT(*) FROM coins")
        total_coins = cursor.fetchone()[0]
        print(f"\nDatabase now contains {total_coins} total coins")

        print("\n" + "=" * 60)
        print("Morgan Dollar series (1878-1904, 1921) successfully added!")
        print("Run 'uv run python scripts/export_from_database.py' to export JSON")
        print("=" * 60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
