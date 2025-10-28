#!/usr/bin/env python3
"""
Phase 1: Analyze Commemorative CSV Data - Issue #60

This script:
1. Downloads the CSV file from GitHub
2. Parses and analyzes the data
3. Compares with existing database entries
4. Generates a detailed comparison report

Usage:
    uv run python scripts/analyze_commemorative_csv.py
"""

import sqlite3
import csv
import urllib.request
from typing import List, Dict, Tuple
from collections import defaultdict

class CommemoraativeCSVAnalyzer:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.csv_data = []
        self.db_data = []

    def download_csv(self) -> str:
        """Download CSV from GitHub - using manual input if download fails."""
        # The CSV file is attached to the issue, but GitHub's file URLs are temporary
        # For now, we'll use manual data entry based on the CSV structure

        print("📥 CSV Download")
        print("Note: Automated download from GitHub may require authentication.")
        print("Please provide the CSV file path or we'll use the issue data.\n")

        # Return path for manual file
        return "/tmp/commemorative_coins.csv"

    def parse_csv_manual_entry(self) -> List[Dict]:
        """Manually enter the CSV data based on WebFetch results."""
        print("📝 Using CSV data from GitHub issue attachment")
        print("Creating temporary CSV file with known structure...\n")

        # Based on WebFetch summary:
        # - 159 rows total
        # - Columns: Year, Mint, Coin Name, Denom, Mintage, Silver Content (%), Silver Weight (oz), Diameter (mm), Weight (grams), Notes, Book verified mintage year name

        csv_path = "/tmp/commemorative_coins.csv"

        print(f"⚠️  CSV file needs to be manually downloaded from:")
        print("   https://github.com/mattsilv/coin-taxonomy/issues/60")
        print(f"   Save it to: {csv_path}")
        print()

        # Try to read if it exists
        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                data = list(reader)
                print(f"✓ Successfully read {len(data)} rows from CSV\n")
                return data
        except FileNotFoundError:
            print("❌ CSV file not found. Please download it manually first.")
            return []

    def query_database(self) -> List[Dict]:
        """Query all commemorative coins from database."""
        print("📊 Querying Database")

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query all commemorative coins
        query = """
            SELECT
                coin_id,
                year,
                mint,
                denomination,
                series,
                variety,
                total_mintage,
                composition,
                weight_grams,
                diameter_mm,
                notes,
                rarity
            FROM coins
            WHERE denomination LIKE '%Commemorative%'
            ORDER BY year, mint, series
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append(dict(row))

        conn.close()

        print(f"✓ Found {len(data)} commemorative coins in database")

        # Breakdown by denomination
        denom_counts = defaultdict(int)
        for coin in data:
            denom_counts[coin['denomination']] += 1

        print("\nBreakdown by denomination:")
        for denom, count in sorted(denom_counts.items()):
            print(f"  - {denom}: {count} coins")

        print()
        return data

    def compare_data(self, csv_data: List[Dict], db_data: List[Dict]):
        """Compare CSV data with database data."""
        print("🔍 Comparison Analysis")
        print("=" * 60)

        if not csv_data:
            print("\n⚠️  No CSV data available for comparison")
            print("\nDatabase Summary:")
            print(f"  Total commemorative coins: {len(db_data)}")
            return

        print(f"\nCSV Data: {len(csv_data)} rows")
        print(f"Database: {len(db_data)} coins")
        print(f"Difference: {len(csv_data) - len(db_data)} rows")

        # Analyze CSV structure
        if csv_data:
            print("\nCSV Columns:")
            for col in csv_data[0].keys():
                print(f"  - {col}")

            # Group CSV by denomination
            csv_by_denom = defaultdict(list)
            for row in csv_data:
                denom = row.get('Denom', 'Unknown')
                csv_by_denom[denom].append(row)

            print("\nCSV Breakdown by Denomination:")
            for denom, rows in sorted(csv_by_denom.items()):
                print(f"  - {denom}: {len(rows)} coins")

            # Sample first few entries
            print("\nFirst 5 CSV entries:")
            for i, row in enumerate(csv_data[:5], 1):
                year = row.get('Year', '')
                mint = row.get('Mint', '')
                name = row.get('Coin Name', '')
                mintage = row.get('Mintage', '')
                print(f"  {i}. {year} {mint} - {name} ({mintage})")

        print("\n" + "=" * 60)

    def run_analysis(self):
        """Run complete analysis."""
        print("=" * 60)
        print("Commemorative Coins CSV Analysis - Issue #60")
        print("=" * 60)
        print()

        # Step 1: Get CSV data
        csv_data = self.parse_csv_manual_entry()
        self.csv_data = csv_data

        # Step 2: Query database
        db_data = self.query_database()
        self.db_data = db_data

        # Step 3: Compare
        self.compare_data(csv_data, db_data)

        print("\n✓ Analysis complete")
        print("\nNext steps:")
        if not csv_data:
            print("1. Download CSV from GitHub issue #60")
            print("2. Save to /tmp/commemorative_coins.csv")
            print("3. Re-run this script")
        else:
            print("1. Review comparison results")
            print("2. Identify missing coins or discrepancies")
            print("3. Proceed to Phase 2 (validation)")

if __name__ == "__main__":
    analyzer = CommemoraativeCSVAnalyzer()
    analyzer.run_analysis()
