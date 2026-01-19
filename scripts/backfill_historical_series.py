#!/usr/bin/env python3
"""
Backfill historical US coin series - Issues #98-103

This script adds missing historical coin series to the database:
- Issue #98: Standing Liberty Quarter (1916-1930)
- Issue #99: Barber Coinage (Dime, Quarter - Half exists)
- Issue #100: Seated Liberty (Dollar, Twenty Cent - others exist)
- Issue #101: Early US Coinage (Draped Bust, Capped Bust)
- Issue #102: Minor Coinage (Two Cent, Shield/V Nickel - Three Cents exist)
- Issue #103: Modern Series (Presidential Dollar, Native American Dollar, American Liberty Gold)

Usage:
    uv run python scripts/backfill_historical_series.py --dry-run
    uv run python scripts/backfill_historical_series.py
"""

import sqlite3
import argparse
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "coins.db"

# Mint operational periods
MINT_PERIODS = {
    "P": (1792, 2030),   # Philadelphia - always operational
    "D": (1906, 2030),   # Denver - opened 1906
    "S": (1854, 2030),   # San Francisco - opened 1854
    "O": (1838, 1909),   # New Orleans - 1838-1909
    "CC": (1870, 1893),  # Carson City - 1870-1893
    "C": (1838, 1861),   # Charlotte - gold only
    "D_gold": (1838, 1861),  # Dahlonega - gold only (we'll use 'D' but only for pre-1862)
    "W": (1984, 2030),   # West Point - modern era
}

# Early era - only Philadelphia
def early_mints():
    return ["P"]

# Pre-1838 - only Philadelphia
def pre_1838_mints():
    return ["P"]

# 1838-1861 - Philadelphia, New Orleans
def antebellum_mints():
    return ["P", "O"]

# 1861-1870 - Philadelphia, San Francisco (New Orleans closed during Civil War)
def civil_war_mints():
    return ["P", "S"]

# 1870-1893 - Philadelphia, San Francisco, Carson City
def carson_city_era_mints():
    return ["P", "S", "CC"]

# 1893-1906 - Philadelphia, San Francisco, New Orleans
def pre_denver_mints():
    return ["P", "S", "O"]

# 1906-1909 - Philadelphia, Denver, San Francisco, New Orleans
def all_early_mints():
    return ["P", "D", "S", "O"]

# 1909+ - Philadelphia, Denver, San Francisco
def modern_mints():
    return ["P", "D", "S"]

# Modern proof/collector - Philadelphia, San Francisco, West Point
def collector_mints():
    return ["P", "S", "W"]


def get_mints_for_year(year: int, series_type: str = "silver") -> list:
    """Get operational mints for a given year and coin type."""
    if year < 1838:
        return ["P"]
    elif year < 1854:
        return ["P", "O"]  # New Orleans opened 1838
    elif year < 1861:
        return ["P", "O", "S"]  # San Francisco opened 1854
    elif year < 1870:
        return ["P", "S"]  # Civil War era
    elif year < 1893:
        # Carson City era
        if year <= 1878 or (year >= 1870 and year <= 1893):
            return ["P", "S", "CC"]
        return ["P", "S"]
    elif year < 1906:
        return ["P", "S", "O"]  # Pre-Denver
    elif year <= 1909:
        return ["P", "D", "S", "O"]  # All mints
    else:
        return ["P", "D", "S"]  # Modern mints


HISTORICAL_SERIES = [
    # ============================================
    # ISSUE #98: Standing Liberty Quarter
    # ============================================
    {
        "series_code": "SLQT",  # Standing Liberty Quarter
        "series_name": "Standing Liberty Quarter",
        "denomination": "Quarters",
        "years": (1916, 1930),
        "mints": ["P", "D", "S"],
        "aliases": ["SLQ", "Standing Liberty"],
        "composition": "silver_90",
        "weight_grams": 6.25,
        "diameter_mm": 24.3,
        "edge": "Reeded",
        "designer": "Hermon A. MacNeil",
        "obverse_description": "Standing Liberty figure",
        "reverse_description": "Flying eagle",
        "variety_suffixes": ["T1", "T2", "FH"],
        "issue": 98,
    },

    # ============================================
    # ISSUE #99: Barber Coinage (Dime and Quarter)
    # ============================================
    {
        "series_code": "BRBR",
        "series_name": "Barber Dime",
        "denomination": "Dimes",
        "years": (1892, 1916),
        "mints": "auto",  # Will use get_mints_for_year
        "aliases": ["Liberty Head Dime", "Barber 10c"],
        "composition": "silver_90",
        "weight_grams": 2.5,
        "diameter_mm": 17.9,
        "edge": "Reeded",
        "designer": "Charles E. Barber",
        "obverse_description": "Liberty head with cap and laurel wreath",
        "reverse_description": "Wreath surrounding denomination",
        "issue": 99,
    },
    {
        "series_code": "BRBQ",
        "series_name": "Barber Quarter",
        "denomination": "Quarters",
        "years": (1892, 1916),
        "mints": "auto",
        "aliases": ["Liberty Head Quarter", "Barber 25c"],
        "composition": "silver_90",
        "weight_grams": 6.25,
        "diameter_mm": 24.3,
        "edge": "Reeded",
        "designer": "Charles E. Barber",
        "obverse_description": "Liberty head with cap and laurel wreath",
        "reverse_description": "Heraldic eagle",
        "issue": 99,
    },

    # ============================================
    # ISSUE #100: Seated Liberty (Dollar, Twenty Cent)
    # ============================================
    {
        "series_code": "SLDL",  # Seated Liberty Dollar
        "series_name": "Seated Liberty Dollar",
        "denomination": "Dollars",
        "years": (1840, 1873),
        "mints": "auto",
        "aliases": ["Liberty Seated Dollar", "Seated Dollar"],
        "composition": "silver_90",
        "weight_grams": 26.73,
        "diameter_mm": 38.1,
        "edge": "Reeded",
        "designer": "Christian Gobrecht",
        "obverse_description": "Seated Liberty with shield",
        "reverse_description": "Eagle with shield",
        "variety_suffixes": ["NM", "WM"],  # No Motto, With Motto
        "issue": 100,
    },
    {
        "series_code": "20CT",
        "series_name": "Twenty Cent Piece",
        "denomination": "Twenty Cents",
        "years": (1875, 1878),
        "mints": ["P", "S", "CC"],
        "aliases": ["Seated Liberty Twenty Cents", "20 Cent", "20c"],
        "composition": "silver_90",
        "weight_grams": 5.0,
        "diameter_mm": 22.0,
        "edge": "Plain",
        "designer": "William Barber",
        "obverse_description": "Seated Liberty",
        "reverse_description": "Eagle with shield",
        "issue": 100,
    },

    # ============================================
    # ISSUE #101: Early US Coinage
    # ============================================
    {
        "series_code": "DBHD",  # Draped Bust Half Dollar
        "series_name": "Draped Bust Half Dollar",
        "denomination": "Half Dollars",
        "years": (1796, 1807),
        "mints": ["P"],
        "aliases": ["Draped Bust Half", "Early Half Dollar"],
        "composition": "silver_89",
        "weight_grams": 13.48,
        "diameter_mm": 32.5,
        "edge": "Lettered",
        "designer": "Robert Scot",
        "obverse_description": "Draped bust of Liberty",
        "reverse_description": "Small eagle (early) or heraldic eagle",
        "variety_suffixes": ["SE", "HE"],  # Small Eagle, Heraldic Eagle
        "issue": 101,
    },
    {
        "series_code": "DBDL",  # Draped Bust Dollar
        "series_name": "Draped Bust Dollar",
        "denomination": "Dollars",
        "years": (1795, 1804),
        "mints": ["P"],
        "aliases": ["Draped Bust Silver Dollar", "Early Dollar"],
        "composition": "silver_89",
        "weight_grams": 26.96,
        "diameter_mm": 39.0,
        "edge": "Lettered",
        "designer": "Robert Scot",
        "obverse_description": "Draped bust of Liberty",
        "reverse_description": "Small eagle (early) or heraldic eagle",
        "variety_suffixes": ["SE", "HE"],
        "issue": 101,
    },
    {
        "series_code": "CBHD",  # Capped Bust Half Dollar
        "series_name": "Capped Bust Half Dollar",
        "denomination": "Half Dollars",
        "years": (1807, 1839),
        "mints": ["P", "O"],  # New Orleans from 1838
        "aliases": ["Capped Bust Half", "Lettered Edge Half"],
        "composition": "silver_89",
        "weight_grams": 13.48,
        "diameter_mm": 32.5,
        "edge": "Lettered (1807-1836), Reeded (1836-1839)",
        "designer": "John Reich",
        "obverse_description": "Capped bust of Liberty",
        "reverse_description": "Eagle with shield",
        "variety_suffixes": ["LE", "RE"],  # Lettered Edge, Reeded Edge
        "issue": 101,
    },
    {
        "series_code": "CBQT",  # Capped Bust Quarter
        "series_name": "Capped Bust Quarter",
        "denomination": "Quarters",
        "years": (1815, 1838),
        "mints": ["P"],
        "aliases": ["Capped Bust Quarter Dollar"],
        "composition": "silver_89",
        "weight_grams": 6.74,
        "diameter_mm": 27.0,
        "edge": "Reeded",
        "designer": "John Reich",
        "obverse_description": "Capped bust of Liberty",
        "reverse_description": "Eagle with shield",
        "issue": 101,
    },
    {
        "series_code": "CBDM",  # Capped Bust Dime
        "series_name": "Capped Bust Dime",
        "denomination": "Dimes",
        "years": (1809, 1837),
        "mints": ["P"],
        "aliases": ["Capped Bust Dime"],
        "composition": "silver_89",
        "weight_grams": 2.7,
        "diameter_mm": 18.8,
        "edge": "Reeded",
        "designer": "John Reich",
        "obverse_description": "Capped bust of Liberty",
        "reverse_description": "Eagle with shield",
        "issue": 101,
    },
    {
        "series_code": "CBH5",
        "series_name": "Capped Bust Half Dime",
        "denomination": "Half Dimes",
        "years": (1829, 1837),
        "mints": ["P"],
        "aliases": ["Capped Bust Half Dime", "Capped Bust 5c Silver"],
        "composition": "silver_89",
        "weight_grams": 1.35,
        "diameter_mm": 15.5,
        "edge": "Reeded",
        "designer": "William Kneass",
        "obverse_description": "Capped bust of Liberty",
        "reverse_description": "Eagle",
        "issue": 101,
    },
    {
        "series_code": "DBH5",
        "series_name": "Draped Bust Half Dime",
        "denomination": "Half Dimes",
        "years": (1796, 1805),
        "mints": ["P"],
        "aliases": ["Draped Bust Half Dime", "Early Half Dime"],
        "composition": "silver_89",
        "weight_grams": 1.35,
        "diameter_mm": 16.5,
        "edge": "Reeded",
        "designer": "Robert Scot",
        "obverse_description": "Draped bust of Liberty",
        "reverse_description": "Small eagle or heraldic eagle",
        "variety_suffixes": ["SE", "HE"],
        "issue": 101,
    },
    {
        "series_code": "SLH5",
        "series_name": "Seated Liberty Half Dime",
        "denomination": "Half Dimes",
        "years": (1837, 1873),
        "mints": "auto",
        "aliases": ["Liberty Seated Half Dime", "Seated Half Dime"],
        "composition": "silver_90",
        "weight_grams": 1.24,
        "diameter_mm": 15.5,
        "edge": "Reeded",
        "designer": "Christian Gobrecht",
        "obverse_description": "Seated Liberty",
        "reverse_description": "Wreath",
        "variety_suffixes": ["NS", "WS", "AR", "LG"],  # No Stars, With Stars, Arrows, Legend
        "issue": 101,
    },

    # ============================================
    # ISSUE #102: Minor Coinage
    # ============================================
    {
        "series_code": "2CNT",
        "series_name": "Two Cent Piece",
        "denomination": "Two Cents",
        "years": (1864, 1873),
        "mints": ["P"],
        "aliases": ["2 Cent", "Two Cent", "2c"],
        "composition": "bronze_95_4_1",
        "weight_grams": 6.22,
        "diameter_mm": 23.0,
        "edge": "Plain",
        "designer": "James B. Longacre",
        "obverse_description": "Shield with IN GOD WE TRUST",
        "reverse_description": "Wreath with 2 CENTS",
        "variety_suffixes": ["SM", "LM"],  # Small Motto, Large Motto
        "issue": 102,
    },
    {
        "series_code": "SHLD",
        "series_name": "Shield Nickel",
        "denomination": "Nickels",
        "years": (1866, 1883),
        "mints": ["P"],
        "aliases": ["Shield 5c", "Shield Five Cent"],
        "composition": "nickel_75_25",
        "weight_grams": 5.0,
        "diameter_mm": 20.5,
        "edge": "Plain",
        "designer": "James B. Longacre",
        "obverse_description": "Shield with cross and stars",
        "reverse_description": "Large numeral 5",
        "variety_suffixes": ["WR", "NR"],  # With Rays (1866-1867), No Rays
        "issue": 102,
    },
    {
        "series_code": "LHNK",
        "series_name": "Liberty Head Nickel",
        "denomination": "Nickels",
        "years": (1883, 1912),
        "mints": ["P", "D", "S"],
        "aliases": ["V Nickel", "Liberty Nickel", "Liberty Head V Nickel"],
        "composition": "nickel_75_25",
        "weight_grams": 5.0,
        "diameter_mm": 21.2,
        "edge": "Plain",
        "designer": "Charles E. Barber",
        "obverse_description": "Liberty head with coronet",
        "reverse_description": "Roman numeral V in wreath",
        "variety_suffixes": ["NC", "WC"],  # No CENTS (1883), With CENTS
        "issue": 102,
    },

    # ============================================
    # ISSUE #103: Modern Series
    # ============================================
    {
        "series_code": "PRSD",
        "series_name": "Presidential Dollar",
        "denomination": "Dollars",
        "years": (2007, 2020),
        "mints": ["P", "D", "S"],
        "aliases": ["Presidential $1", "President Dollar"],
        "composition": "manganese_brass_clad",
        "weight_grams": 8.1,
        "diameter_mm": 26.5,
        "edge": "Lettered",
        "designer": "Various",
        "obverse_description": "Portrait of US President",
        "reverse_description": "Statue of Liberty",
        "issue": 103,
    },
    {
        "series_code": "NATV",
        "series_name": "Native American Dollar",
        "denomination": "Dollars",
        "years": (2009, 2025),
        "mints": ["P", "D", "S"],
        "aliases": ["Sacagawea Dollar", "Native $1", "Native American $1"],
        "composition": "manganese_brass_clad",
        "weight_grams": 8.1,
        "diameter_mm": 26.5,
        "edge": "Lettered",
        "designer": "Glenna Goodacre (obverse), Various (reverse)",
        "obverse_description": "Sacagawea and child",
        "reverse_description": "Varies by year - Native American themes",
        "issue": 103,
    },
    {
        "series_code": "ALGD",
        "series_name": "American Liberty Gold",
        "denomination": "$100 Gold",
        "years": (2015, 2025),
        "mints": ["W"],  # West Point only
        "aliases": ["Liberty Gold $100", "High Relief Liberty", "American Liberty HR"],
        "composition": "gold_9999",
        "weight_grams": 31.108,  # 1 oz
        "diameter_mm": 30.61,
        "edge": "Reeded",
        "designer": "Justin Kunz / Various",
        "obverse_description": "Liberty (design varies)",
        "reverse_description": "Eagle",
        "variety_suffixes": ["HR"],  # High Relief
        "issue": 103,
    },
    {
        "series_code": "SBAD",  # Susan B. Anthony Dollar
        "series_name": "Susan B. Anthony Dollar",
        "denomination": "Dollars",
        "years": (1979, 1999),  # 1979-1981, then 1999
        "mints": ["P", "D", "S"],
        "aliases": ["SBA Dollar", "Anthony Dollar", "Susan B Anthony"],
        "composition": "cupronickel_clad",
        "weight_grams": 8.1,
        "diameter_mm": 26.5,
        "edge": "Reeded",
        "designer": "Frank Gasparro",
        "obverse_description": "Susan B. Anthony portrait",
        "reverse_description": "Apollo 11 moon landing eagle",
        "issue": 103,
    },
]


def coin_exists(cursor, coin_id: str) -> bool:
    """Check if a coin already exists in the database."""
    cursor.execute("SELECT 1 FROM coins WHERE coin_id = ?", (coin_id,))
    return cursor.fetchone() is not None


def generate_coin_id(series_code: str, year: int, mint: str) -> str:
    """Generate coin ID in format US-CODE-YEAR-MINT."""
    return f"US-{series_code}-{year}-{mint}"


def get_mints_for_series(series: dict, year: int) -> list:
    """Get mints for a specific series and year."""
    if series.get("mints") == "auto":
        return get_mints_for_year(year)
    return series["mints"]


def insert_coins(cursor, series: dict, dry_run: bool = False) -> int:
    """Insert coins for a series, returns count of inserted coins."""
    inserted = 0
    start_year, end_year = series["years"]

    for year in range(start_year, end_year + 1):
        mints = get_mints_for_series(series, year)

        for mint in mints:
            # Special handling for mint operational periods
            if mint == "D" and year < 1906 and series["denomination"] not in ["$5 Gold", "$10 Gold", "$20 Gold"]:
                continue  # Denver didn't exist yet for non-gold
            if mint == "O" and (year < 1838 or year > 1909):
                continue  # New Orleans operational period
            if mint == "O" and year >= 1861 and year <= 1878:
                continue  # New Orleans closed during/after Civil War for most of this period
            if mint == "CC" and (year < 1870 or year > 1893):
                continue  # Carson City operational period
            if mint == "S" and year < 1854:
                continue  # San Francisco didn't exist yet
            if mint == "W" and year < 1984:
                continue  # West Point didn't exist yet

            # SBA Dollar special handling - only 1979-1981 and 1999
            if series["series_code"] == "SBAD" and year not in [1979, 1980, 1981, 1999]:
                continue

            coin_id = generate_coin_id(series["series_code"], year, mint)

            if coin_exists(cursor, coin_id):
                continue

            if dry_run:
                print(f"  Would insert: {coin_id}")
                inserted += 1
                continue

            cursor.execute("""
                INSERT INTO coins (
                    coin_id, year, mint, denomination, series, variety,
                    composition, weight_grams, diameter_mm, edge,
                    designer, obverse_description, reverse_description,
                    notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin_id,
                str(year),
                mint,
                series["denomination"],
                series["series_name"],
                None,  # variety
                series.get("composition"),
                series.get("weight_grams"),
                series.get("diameter_mm"),
                series.get("edge"),
                series.get("designer"),
                series.get("obverse_description"),
                series.get("reverse_description"),
                f"Issue #{series['issue']}",
            ))
            inserted += 1

    return inserted


def main():
    parser = argparse.ArgumentParser(description="Backfill historical US coin series")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be inserted without making changes")
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"{'DRY RUN - ' if args.dry_run else ''}Backfilling historical US coin series...")
    print(f"Database: {DB_PATH}")
    print()

    total_inserted = 0
    issue_counts = {}

    for series in HISTORICAL_SERIES:
        issue_num = series["issue"]
        if issue_num not in issue_counts:
            issue_counts[issue_num] = 0

        print(f"Processing: {series['series_name']} ({series['years'][0]}-{series['years'][1]})")
        count = insert_coins(cursor, series, args.dry_run)
        issue_counts[issue_num] += count
        total_inserted += count
        print(f"  Inserted: {count} coins")
        print()

    if not args.dry_run:
        conn.commit()

    print("=" * 50)
    print("Summary by Issue:")
    for issue_num in sorted(issue_counts.keys()):
        print(f"  Issue #{issue_num}: {issue_counts[issue_num]} coins")
    print(f"\nTotal coins inserted: {total_inserted}")

    conn.close()


if __name__ == "__main__":
    main()
