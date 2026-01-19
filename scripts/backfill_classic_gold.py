#!/usr/bin/env python3
"""
Backfill Migration Script: Add Classic US Gold Series (Issue #97)

This script adds the 10 missing classic US gold coin series:

1. Gold Dollar Type 1 (1849-1854) - Liberty Head, small
2. Gold Dollar Type 2 (1854-1856) - Indian Princess, small head
3. Gold Dollar Type 3 (1856-1889) - Indian Princess, large head
4. $3 Gold (1854-1889) - Indian Princess
5. Liberty Head Half Eagle $5 (1839-1908)
6. Indian Head Half Eagle $5 (1908-1929)
7. Liberty Head Eagle $10 (1838-1907)
8. Indian Head Eagle $10 (1907-1933)
9. Liberty Head Double Eagle $20 (1850-1907)
10. St. Gaudens Double Eagle $20 (1907-1933)

Usage:
    python scripts/backfill_classic_gold.py
    python scripts/backfill_classic_gold.py --dry-run
"""

import sqlite3
import os
import argparse
from datetime import datetime
from typing import Dict, List

# Database path
DB_PATH = 'database/coins.db'

# Series definitions following the issue #97 specifications
CLASSIC_GOLD_SERIES = [
    # ==========================================================================
    # GOLD DOLLARS ($1)
    # ==========================================================================
    {
        "series_code": "GD1T",  # Gold Dollar Type 1
        "series_name": "Gold Dollar Type 1",
        "denomination": "$1 Gold",
        "years": (1849, 1854),
        "mints": ["P", "C", "D", "O", "S"],
        "notes": "Liberty Head design, smallest US gold coin",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 13.0,
        "weight_grams": 1.672,
        "aliases": ["Type 1 Gold Dollar", "Liberty Head Gold Dollar", "Small Liberty Gold Dollar"],
        "obverse_description": "Liberty head facing left wearing coronet inscribed 'LIBERTY', 13 stars around, date below",
        "reverse_description": "Wreath encircling '1 DOLLAR', 'UNITED STATES OF AMERICA' around",
    },
    {
        "series_code": "GD2T",  # Gold Dollar Type 2
        "series_name": "Gold Dollar Type 2",
        "denomination": "$1 Gold",
        "years": (1854, 1856),
        "mints": ["P", "C", "D", "O", "S"],
        "notes": "Indian Princess design with small head, thin planchet",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 15.0,
        "weight_grams": 1.672,
        "aliases": ["Type 2 Gold Dollar", "Small Indian Head Gold Dollar", "Indian Princess Type 2"],
        "obverse_description": "Indian Princess head facing left with feathered headdress, 'UNITED STATES OF AMERICA' around, date below",
        "reverse_description": "Wreath encircling '1 DOLLAR'",
    },
    {
        "series_code": "GD3T",  # Gold Dollar Type 3
        "series_name": "Gold Dollar Type 3",
        "denomination": "$1 Gold",
        "years": (1856, 1889),
        "mints": ["P", "C", "D", "O", "S"],
        "notes": "Indian Princess design with large head, thicker planchet",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 15.0,
        "weight_grams": 1.672,
        "aliases": ["Type 3 Gold Dollar", "Large Indian Head Gold Dollar", "Indian Princess Type 3"],
        "obverse_description": "Indian Princess head facing left with larger feathered headdress, 'UNITED STATES OF AMERICA' around, date below",
        "reverse_description": "Wreath encircling '1 DOLLAR'",
    },

    # ==========================================================================
    # $3 GOLD
    # ==========================================================================
    {
        "series_code": "3DGD",  # $3 Gold Dollar
        "series_name": "Three Dollar Gold",
        "denomination": "$3 Gold",
        "years": (1854, 1889),
        "mints": ["P", "D", "O", "S"],
        "notes": "Indian Princess design, unusual denomination intended to purchase 3-cent stamps",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 20.5,
        "weight_grams": 5.015,
        "aliases": ["$3 Gold", "Indian Princess $3", "Three Dollar Piece"],
        "obverse_description": "Indian Princess head facing left with feathered headdress, 'UNITED STATES OF AMERICA' around, date below",
        "reverse_description": "Agricultural wreath encircling '3 DOLLARS'",
    },

    # ==========================================================================
    # HALF EAGLES ($5)
    # ==========================================================================
    {
        "series_code": "LHHE",  # Liberty Head Half Eagle
        "series_name": "Liberty Head Half Eagle",
        "denomination": "$5 Gold",
        "years": (1839, 1908),
        "mints": ["P", "C", "CC", "D", "O", "S"],
        "notes": "Coronet/Liberty Head design, major US gold circulation coin",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 21.6,
        "weight_grams": 8.359,
        "aliases": ["Liberty $5", "Coronet Half Eagle", "Liberty Gold $5", "Coronet $5"],
        "obverse_description": "Liberty head facing left wearing coronet inscribed 'LIBERTY', 13 stars around, date below",
        "reverse_description": "Eagle with spread wings holding arrows and olive branch, 'UNITED STATES OF AMERICA' above, 'FIVE D.' below",
    },
    {
        "series_code": "IHHE",  # Indian Head Half Eagle
        "series_name": "Indian Head Half Eagle",
        "denomination": "$5 Gold",
        "years": (1908, 1929),
        "mints": ["P", "D", "O", "S"],
        "notes": "Unique incuse (recessed) design by Bela Lyon Pratt",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 21.6,
        "weight_grams": 8.359,
        "aliases": ["Indian $5", "Incuse $5", "Pratt $5", "Incuse Half Eagle"],
        "obverse_description": "Native American chief head facing left with feathered headdress, 13 stars around, date below",
        "reverse_description": "Standing eagle on bundle of arrows, 'E PLURIBUS UNUM' above, 'UNITED STATES OF AMERICA' and 'FIVE DOLLARS' below",
    },

    # ==========================================================================
    # EAGLES ($10)
    # ==========================================================================
    {
        "series_code": "LHEG",  # Liberty Head Eagle
        "series_name": "Liberty Head Eagle",
        "denomination": "$10 Gold",
        "years": (1838, 1907),
        "mints": ["P", "CC", "D", "O", "S"],
        "notes": "Coronet/Liberty Head design, major US gold circulation coin",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 27.0,
        "weight_grams": 16.718,
        "aliases": ["Liberty $10", "Coronet Eagle", "Liberty Gold $10", "Coronet $10"],
        "obverse_description": "Liberty head facing left wearing coronet inscribed 'LIBERTY', 13 stars around, date below",
        "reverse_description": "Eagle with spread wings holding arrows and olive branch, 'UNITED STATES OF AMERICA' above, 'TEN D.' below",
    },
    {
        "series_code": "IHEG",  # Indian Head Eagle
        "series_name": "Indian Head Eagle",
        "denomination": "$10 Gold",
        "years": (1907, 1933),
        "mints": ["P", "D", "S"],
        "notes": "Augustus Saint-Gaudens design, one of the most beautiful US coins",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 27.0,
        "weight_grams": 16.718,
        "aliases": ["Indian $10", "Saint-Gaudens $10", "Indian Eagle"],
        "obverse_description": "Liberty head facing left wearing Native American feathered headdress, 13 stars around, date below",
        "reverse_description": "Standing eagle on bundle of arrows, 'E PLURIBUS UNUM' above, 'UNITED STATES OF AMERICA' and 'TEN DOLLARS' below",
    },

    # ==========================================================================
    # DOUBLE EAGLES ($20)
    # ==========================================================================
    {
        "series_code": "LHDE",  # Liberty Head Double Eagle
        "series_name": "Liberty Head Double Eagle",
        "denomination": "$20 Gold",
        "years": (1850, 1907),
        "mints": ["P", "CC", "D", "O", "S"],
        "notes": "Coronet/Liberty Head design, largest regular-issue US gold coin",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 34.0,
        "weight_grams": 33.436,
        "aliases": ["Liberty $20", "Coronet Double Eagle", "Liberty Gold $20", "Coronet $20"],
        "obverse_description": "Liberty head facing left wearing coronet inscribed 'LIBERTY', 13 stars around, date below",
        "reverse_description": "Eagle with spread wings, shield on breast, 'UNITED STATES OF AMERICA' above, 'TWENTY D.' below",
    },
    {
        "series_code": "STGD",  # St. Gaudens Double Eagle
        "series_name": "St. Gaudens Double Eagle",
        "denomination": "$20 Gold",
        "years": (1907, 1933),
        "mints": ["P", "D", "S"],
        "notes": "Augustus Saint-Gaudens design, considered the most beautiful US coin",
        "composition": {"gold": 90.0, "copper": 10.0},
        "diameter_mm": 34.0,
        "weight_grams": 33.436,
        "aliases": ["Saint Gaudens $20", "St. Gaudens", "Saint-Gaudens Double Eagle", "Standing Liberty $20"],
        "obverse_description": "Full-length Liberty striding forward holding torch and olive branch, Capitol building in background, rays of sun behind",
        "reverse_description": "Flying eagle above rising sun, 'UNITED STATES OF AMERICA' and 'TWENTY DOLLARS' around",
        "variety_suffixes": ["HR"],  # High Relief variety for 1907
    },
]


def create_backup():
    """Create database backup before migration."""
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{backup_dir}/coins_classic_gold_backup_{timestamp}.db"

    if os.path.exists(DB_PATH):
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        print(f"✓ Backup created: {backup_path}")
    return backup_path


def get_mint_years(start_year: int, end_year: int, mint: str, denomination: str) -> List[int]:
    """Get years when a specific mint was active for a denomination."""
    # Define mint operational periods for gold coins
    mint_periods = {
        "P": (1793, 2030),    # Philadelphia - always active
        "C": (1838, 1861),    # Charlotte - gold only
        "CC": (1870, 1893),   # Carson City
        "D": (1838, 1861),    # Dahlonega - gold only (D = Denver after 1906)
        "O": (1838, 1909),    # New Orleans
        "S": (1854, 2030),    # San Francisco
    }

    # Special case: D mint in Denver era (after 1906)
    if mint == "D" and start_year >= 1906:
        mint_periods["D"] = (1906, 2030)

    if mint not in mint_periods:
        return []

    mint_start, mint_end = mint_periods[mint]

    # Intersect series years with mint operational period
    actual_start = max(start_year, mint_start)
    actual_end = min(end_year, mint_end)

    if actual_start > actual_end:
        return []

    return list(range(actual_start, actual_end + 1))


def generate_coin_records(series: Dict) -> List[Dict]:
    """Generate individual coin records for all years and mints of a series."""
    coins = []
    series_code = series["series_code"]
    start_year, end_year = series["years"]

    for mint in series["mints"]:
        years = get_mint_years(start_year, end_year, mint, series["denomination"])

        for year in years:
            coin_id = f"US-{series_code}-{year}-{mint}"

            coin = {
                "coin_id": coin_id,
                "year": str(year),
                "mint": mint,
                "denomination": series["denomination"],
                "series": series["series_name"],
                "composition": str(series.get("composition", {})),
                "weight_grams": series.get("weight_grams"),
                "diameter_mm": series.get("diameter_mm"),
                "edge": "reeded",
                "obverse_description": series.get("obverse_description", ""),
                "reverse_description": series.get("reverse_description", ""),
                "notes": series.get("notes", ""),
                "source_citation": "Issue #97 - Classic US Gold Series",
            }
            coins.append(coin)

    return coins


def insert_coins(conn: sqlite3.Connection, coins: List[Dict], dry_run: bool = False) -> int:
    """Insert coin records into database."""
    cursor = conn.cursor()
    inserted = 0
    skipped = 0

    for coin in coins:
        # Check if coin already exists
        cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin["coin_id"],))
        if cursor.fetchone():
            skipped += 1
            continue

        if dry_run:
            print(f"  Would insert: {coin['coin_id']}")
            inserted += 1
            continue

        try:
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, year, mint, denomination, series,
                    composition, weight_grams, diameter_mm, edge,
                    obverse_description, reverse_description, notes, source_citation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin["coin_id"],
                coin["year"],
                coin["mint"],
                coin["denomination"],
                coin["series"],
                coin["composition"],
                coin["weight_grams"],
                coin["diameter_mm"],
                coin["edge"],
                coin["obverse_description"],
                coin["reverse_description"],
                coin["notes"],
                coin["source_citation"],
            ))
            inserted += 1
        except sqlite3.IntegrityError as e:
            print(f"  Error inserting {coin['coin_id']}: {e}")
            skipped += 1

    if not dry_run:
        conn.commit()

    return inserted, skipped


def main():
    parser = argparse.ArgumentParser(description='Backfill classic US gold coin series')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be inserted without making changes')
    args = parser.parse_args()

    print("=" * 70)
    print("Classic US Gold Series Backfill - Issue #97")
    print("=" * 70)

    if args.dry_run:
        print("\n*** DRY RUN MODE - No changes will be made ***\n")
    else:
        # Create backup first
        create_backup()

    # Connect to database
    conn = sqlite3.connect(DB_PATH)

    total_inserted = 0
    total_skipped = 0

    for series in CLASSIC_GOLD_SERIES:
        print(f"\n{series['series_name']} ({series['denomination']})")
        print(f"  Years: {series['years'][0]}-{series['years'][1]}")
        print(f"  Mints: {', '.join(series['mints'])}")

        coins = generate_coin_records(series)
        inserted, skipped = insert_coins(conn, coins, args.dry_run)

        print(f"  Generated: {len(coins)} coin records")
        print(f"  Inserted: {inserted}, Skipped (existing): {skipped}")

        total_inserted += inserted
        total_skipped += skipped

    conn.close()

    print("\n" + "=" * 70)
    print(f"SUMMARY: Inserted {total_inserted} coins, Skipped {total_skipped} existing")
    print("=" * 70)

    if not args.dry_run:
        print("\nNext steps:")
        print("  1. Run: uv run python scripts/export_from_database.py")
        print("  2. Verify JSON exports")
        print("  3. Commit changes: git add . && git commit -m 'Add classic US gold series - Issue #97'")


if __name__ == "__main__":
    main()
