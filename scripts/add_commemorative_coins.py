#!/usr/bin/env python3
"""
Migration Script: Add US Classic Commemorative Coins (1892-1954)

This script adds the complete set of Classic US Commemorative coins including:
- Commemorative Half Dollars (1892-1954)
- Commemorative Silver Dollars (1900-1939)
- Commemorative Gold coins ($1, $2.50, $50) (1903-1926)

Following database-first workflow and Senior Engineer Task Execution Rule.

Usage:
    uv run python scripts/add_commemorative_coins.py
    uv run python scripts/add_commemorative_coins.py --dry-run
"""

import sqlite3
import os
import argparse
from datetime import datetime
from typing import List, Dict

class CommemorativeCoinMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_commemorative_backup_{timestamp}.db"

        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def get_commemorative_half_dollars(self) -> List[Dict]:
        """Classic Commemorative Half Dollars (1892-1954)

        Data source: Issue #53 comment with verified mintage figures
        All coins are 90% silver, 0.3617 oz silver weight, 30.6mm diameter, 12.5g weight
        """
        # Series abbreviation: COMM for Commemorative
        # Format: US-COMM-YEAR-MINT

        coins = []

        # Columbian Exposition (First US commemorative)
        coins.extend([
            {"year": 1892, "mint": "P", "name": "World's Columbian Exposition", "mintage": 950000,
             "notes": "First US commemorative coin"},
            {"year": 1893, "mint": "P", "name": "World's Columbian Exposition", "mintage": 1550405},
        ])

        # Panama-Pacific
        coins.append({"year": 1915, "mint": "S", "name": "Panama-Pacific International Exposition",
                     "mintage": 27134, "rarity": "key", "notes": "One of the rarer commemoratives"})

        # State and regional commemoratives 1918-1928
        coins.extend([
            {"year": 1918, "mint": "P", "name": "Illinois Centennial", "mintage": 100058,
             "notes": "Features Abraham Lincoln"},
            {"year": 1920, "mint": "P", "name": "Maine Centennial", "mintage": 50028},
            {"year": 1920, "mint": "P", "name": "Pilgrim Tercentenary", "mintage": 152112},
            {"year": 1921, "mint": "P", "name": "Alabama Centennial", "mintage": 59038, "variety": "Regular"},
            {"year": 1921, "mint": "P", "name": "Alabama Centennial 2X2", "mintage": 6006, "rarity": "key",
             "variety": "2X2", "notes": "With 2X2 mark (22nd state)"},
            {"year": 1921, "mint": "P", "name": "Missouri Centennial", "mintage": 15428, "variety": "Regular"},
            {"year": 1921, "mint": "P", "name": "Missouri Centennial 2★4", "mintage": 5000, "rarity": "key",
             "variety": "2★4", "notes": "With 2★4 mark (24th state)"},
        ])

        # Grant Memorial
        coins.extend([
            {"year": 1922, "mint": "P", "name": "Grant Memorial", "mintage": 67405, "variety": "Regular"},
            {"year": 1922, "mint": "P", "name": "Grant Memorial with Star", "mintage": 4256, "rarity": "key",
             "variety": "With Star", "notes": "With star in field"},
        ])

        # 1923-1928 commemoratives
        coins.extend([
            {"year": 1923, "mint": "S", "name": "Monroe Doctrine Centennial", "mintage": 274077},
            {"year": 1924, "mint": "P", "name": "Huguenot-Walloon Tercentenary", "mintage": 142080},
            {"year": 1925, "mint": "S", "name": "California Diamond Jubilee", "mintage": 86594},
            {"year": 1925, "mint": "P", "name": "Fort Vancouver Centennial", "mintage": 14994, "rarity": "scarce"},
            {"year": 1925, "mint": "P", "name": "Lexington-Concord Sesquicentennial", "mintage": 162013},
            {"year": 1925, "mint": "P", "name": "Stone Mountain Memorial", "mintage": 1314709,
             "notes": "Highest mintage of classic commemoratives"},
        ])

        # Oregon Trail Memorial (1926-1939, multiple years and mints)
        oregon_trail = [
            (1926, "P", 47955), (1926, "S", 83055), (1928, "P", 6028), (1933, "D", 5008),
            (1934, "D", 7006), (1936, "P", 10006), (1936, "D", 5006), (1936, "S", 5006),
            (1937, "D", 12008), (1938, "P", 6006), (1938, "D", 6005), (1938, "S", 6006),
            (1939, "P", 3004), (1939, "D", 3004), (1939, "S", 3005),
        ]
        for year, mint, mintage in oregon_trail:
            coins.append({"year": year, "mint": mint, "name": "Oregon Trail Memorial",
                         "mintage": mintage, "rarity": "scarce" if mintage < 10000 else "common"})

        # 1926-1928 commemoratives continued
        coins.extend([
            {"year": 1926, "mint": "P", "name": "Sesquicentennial of American Independence", "mintage": 141120,
             "notes": "Features Calvin Coolidge - only living president on US coin"},
            {"year": 1927, "mint": "P", "name": "Vermont Sesquicentennial", "mintage": 28162},
            {"year": 1928, "mint": "P", "name": "Hawaiian Sesquicentennial", "mintage": 10008, "rarity": "key",
             "notes": "One of the rarest commemoratives"},
        ])

        # Daniel Boone Bicentennial (1934-1938, multiple years and mints)
        daniel_boone = [
            (1934, "P", 10007), (1935, "P", 10010), (1935, "D", 5005), (1935, "S", 5005),
            (1936, "P", 12012), (1936, "D", 5005), (1936, "S", 5006), (1937, "P", 9810),
            (1937, "D", 2506), (1937, "S", 2506), (1938, "P", 2100), (1938, "D", 2100), (1938, "S", 2100),
        ]
        for year, mint, mintage in daniel_boone:
            coins.append({"year": year, "mint": mint, "name": "Daniel Boone Bicentennial",
                         "mintage": mintage, "rarity": "key" if mintage < 5000 else "scarce"})

        # Maryland
        coins.append({"year": 1934, "mint": "P", "name": "Maryland Tercentenary", "mintage": 25015})

        # Texas Centennial (1934-1938, multiple years and mints)
        texas = [
            (1934, "P", 61463), (1935, "P", 9996), (1935, "D", 10007), (1935, "S", 10008),
            (1936, "P", 8911), (1936, "D", 9039), (1936, "S", 9055), (1937, "P", 6571),
            (1937, "D", 6605), (1937, "S", 6637), (1938, "P", 3780), (1938, "D", 3775), (1938, "S", 3814),
        ]
        for year, mint, mintage in texas:
            coins.append({"year": year, "mint": mint, "name": "Texas Centennial",
                         "mintage": mintage, "rarity": "key" if mintage < 5000 else "scarce"})

        # Arkansas Centennial (1935-1939, multiple years and mints)
        arkansas = [
            (1935, "P", 13012), (1935, "D", 5505), (1935, "S", 5506), (1936, "P", 9660),
            (1936, "D", 9660), (1936, "S", 9662), (1937, "P", 5505), (1937, "D", 5505),
            (1937, "S", 5506), (1938, "P", 3156), (1938, "D", 3155), (1938, "S", 3156),
            (1939, "P", 2104), (1939, "D", 2104), (1939, "S", 2105),
        ]
        for year, mint, mintage in arkansas:
            coins.append({"year": year, "mint": mint, "name": "Arkansas Centennial",
                         "mintage": mintage, "rarity": "key" if mintage < 5000 else "scarce"})

        # California-Pacific Exposition
        coins.extend([
            {"year": 1935, "mint": "S", "name": "California-Pacific Exposition", "mintage": 70132},
            {"year": 1936, "mint": "D", "name": "California-Pacific Exposition", "mintage": 30092},
        ])

        # 1935 commemoratives
        coins.extend([
            {"year": 1935, "mint": "P", "name": "Connecticut Tercentenary", "mintage": 25018,
             "notes": "Features the Charter Oak"},
            {"year": 1935, "mint": "P", "name": "Hudson, New York, Sesquicentennial", "mintage": 10008,
             "rarity": "key", "notes": "One of the rarest commemoratives"},
            {"year": 1935, "mint": "P", "name": "Old Spanish Trail", "mintage": 10008, "rarity": "key",
             "notes": "One of the rarest commemoratives"},
        ])

        # 1936 commemoratives (the "Great Commemorative Boom")
        coins.extend([
            {"year": 1936, "mint": "P", "name": "Albany, New York, Charter", "mintage": 17671},
            {"year": 1936, "mint": "P", "name": "Arkansas-Robinson", "mintage": 25265,
             "notes": "Features Senator Joseph T. Robinson"},
            {"year": 1936, "mint": "P", "name": "Battle of Gettysburg", "mintage": 26928,
             "notes": "75th anniversary"},
            {"year": 1936, "mint": "P", "name": "Bridgeport, Connecticut, Centennial", "mintage": 25015,
             "notes": "Features P.T. Barnum"},
        ])

        # Cincinnati Music Center (3-coin set)
        coins.extend([
            {"year": 1936, "mint": "P", "name": "Cincinnati Music Center", "mintage": 5005, "rarity": "key",
             "notes": "Set sold as 3-coin set"},
            {"year": 1936, "mint": "D", "name": "Cincinnati Music Center", "mintage": 5005, "rarity": "key",
             "notes": "Set sold as 3-coin set"},
            {"year": 1936, "mint": "S", "name": "Cincinnati Music Center", "mintage": 5006, "rarity": "key",
             "notes": "Set sold as 3-coin set"},
        ])

        # More 1936 commemoratives
        coins.append({"year": 1936, "mint": "P", "name": "Cleveland Centennial", "mintage": 50030})

        # Columbia, South Carolina (3-coin set)
        coins.extend([
            {"year": 1936, "mint": "P", "name": "Columbia, South Carolina, Sesquicentennial", "mintage": 9007,
             "notes": "Set sold as 3-coin set"},
            {"year": 1936, "mint": "D", "name": "Columbia, South Carolina, Sesquicentennial", "mintage": 8009,
             "notes": "Set sold as 3-coin set"},
            {"year": 1936, "mint": "S", "name": "Columbia, South Carolina, Sesquicentennial", "mintage": 8007,
             "notes": "Set sold as 3-coin set"},
        ])

        # Final 1936 commemoratives
        coins.extend([
            {"year": 1936, "mint": "P", "name": "Delaware Tercentenary", "mintage": 20993},
            {"year": 1936, "mint": "P", "name": "Elgin, Illinois, Centennial", "mintage": 20015},
            {"year": 1936, "mint": "P", "name": "Long Island Tercentenary", "mintage": 81826},
            {"year": 1936, "mint": "P", "name": "Lynchburg, Virginia, Sesquicentennial", "mintage": 20013,
             "notes": "Features Senator Carter Glass"},
            {"year": 1936, "mint": "P", "name": "Norfolk, Virginia, Bicentennial", "mintage": 16936},
        ])

        # Providence, Rhode Island (3-coin set)
        coins.extend([
            {"year": 1936, "mint": "P", "name": "Providence, Rhode Island, Tercentenary", "mintage": 20013,
             "notes": "Set sold as 3-coin set"},
            {"year": 1936, "mint": "D", "name": "Providence, Rhode Island, Tercentenary", "mintage": 15010,
             "notes": "Set sold as 3-coin set"},
            {"year": 1936, "mint": "S", "name": "Providence, Rhode Island, Tercentenary", "mintage": 15011,
             "notes": "Set sold as 3-coin set"},
        ])

        # Final 1936 and 1937-1938 commemoratives
        coins.extend([
            {"year": 1936, "mint": "S", "name": "San Francisco-Oakland Bay Bridge", "mintage": 71424},
            {"year": 1936, "mint": "P", "name": "Wisconsin Territorial Centennial", "mintage": 25015},
            {"year": 1936, "mint": "P", "name": "York County, Maine, Tercentenary", "mintage": 25015},
            {"year": 1937, "mint": "P", "name": "Battle of Antietam", "mintage": 18028,
             "notes": "75th anniversary"},
            {"year": 1937, "mint": "P", "name": "Roanoke Island", "mintage": 29030,
             "notes": "350th anniversary"},
            {"year": 1938, "mint": "P", "name": "New Rochelle, New York, 250th Anniversary", "mintage": 15266,
             "notes": "Last US coin with denticles"},
        ])

        # Post-WWII commemoratives
        coins.append({"year": 1946, "mint": "P", "name": "Iowa Statehood Centennial", "mintage": 100057,
                     "notes": "First commemorative after WWII"})

        # Booker T. Washington (1946-1951, multiple years and mints)
        btw = [
            (1946, "P", 1000546), (1946, "D", 200113), (1946, "S", 500279),
            (1947, "P", 100017), (1947, "D", 100017), (1947, "S", 100017),
            (1948, "P", 8005), (1948, "D", 8005), (1948, "S", 8005),
            (1949, "P", 6004), (1949, "D", 6004), (1949, "S", 6004),
            (1950, "P", 6004), (1950, "D", 6004), (1950, "S", 6004),
            (1951, "P", 210082), (1951, "D", 7004), (1951, "S", 7004),
        ]
        first_btw = True
        for year, mint, mintage in btw:
            notes = "First African American on US coin" if first_btw else None
            coins.append({"year": year, "mint": mint, "name": "Booker T. Washington",
                         "mintage": mintage, "notes": notes})
            first_btw = False

        # Carver/Washington (1951-1954, final classic commemoratives)
        carver_wash = [
            (1951, "P", 10004), (1951, "D", 10004), (1951, "S", 10004),
            (1952, "P", 1106292), (1952, "D", 8006), (1952, "S", 8006),
            (1953, "P", 8003), (1953, "D", 8003), (1953, "S", 8003),
            (1954, "P", 12006), (1954, "D", 12006), (1954, "S", 42024),
        ]
        first_cw = True
        for year, mint, mintage in carver_wash:
            notes = "First dual portrait commemorative" if first_cw else None
            if year == 1954:
                notes = "Final classic commemorative"
            coins.append({"year": year, "mint": mint, "name": "Carver/Washington",
                         "mintage": mintage, "notes": notes})
            first_cw = False

        return coins

    def get_commemorative_dollars(self) -> List[Dict]:
        """Classic Commemorative Silver Dollars (1900-1939)

        All coins are 90% silver, 26.73mm diameter, 26.73g weight
        """
        # Note: Several commemorative silver dollars used same designs as half dollars
        # but in dollar denomination. Listing major distinct dollar designs.

        coins = [
            {"year": 1900, "mint": "P", "name": "Lafayette Dollar", "mintage": 36026, "rarity": "key",
             "notes": "First commemorative silver dollar", "weight_grams": 26.73, "diameter_mm": 38.1},
        ]

        return coins

    def get_commemorative_gold(self) -> List[Dict]:
        """Classic Commemorative Gold Coins (1903-1926)

        Includes Gold Dollars, Quarter Eagles ($2.50), and $50 pieces
        """
        coins = []

        # Gold Dollars ($1)
        coins.extend([
            {"year": 1903, "mint": "P", "name": "Louisiana Purchase - Jefferson", "mintage": 17500,
             "denomination": "Gold Dollars", "weight_grams": 1.672, "diameter_mm": 15,
             "composition": "90% Gold", "rarity": "key"},
            {"year": 1903, "mint": "P", "name": "Louisiana Purchase - McKinley", "mintage": 17500,
             "denomination": "Gold Dollars", "weight_grams": 1.672, "diameter_mm": 15,
             "composition": "90% Gold", "rarity": "key"},
            {"year": 1904, "mint": "P", "name": "Lewis & Clark Exposition", "mintage": 10025,
             "denomination": "Gold Dollars", "weight_grams": 1.672, "diameter_mm": 15,
             "composition": "90% Gold", "rarity": "key"},
            {"year": 1905, "mint": "P", "name": "Lewis & Clark Exposition", "mintage": 10041,
             "denomination": "Gold Dollars", "weight_grams": 1.672, "diameter_mm": 15,
             "composition": "90% Gold", "rarity": "key"},
            {"year": 1915, "mint": "S", "name": "Panama-Pacific Exposition", "mintage": 15000,
             "denomination": "Gold Dollars", "weight_grams": 1.672, "diameter_mm": 15,
             "composition": "90% Gold", "rarity": "key"},
            {"year": 1916, "mint": "P", "name": "McKinley Memorial", "mintage": 9977,
             "denomination": "Gold Dollars", "weight_grams": 1.672, "diameter_mm": 15,
             "composition": "90% Gold", "rarity": "key"},
            {"year": 1917, "mint": "P", "name": "McKinley Memorial", "mintage": 10000,
             "denomination": "Gold Dollars", "weight_grams": 1.672, "diameter_mm": 15,
             "composition": "90% Gold", "rarity": "key"},
            {"year": 1922, "mint": "P", "name": "Grant Memorial with Star", "mintage": 5016,
             "denomination": "Gold Dollars", "weight_grams": 1.672, "diameter_mm": 15,
             "composition": "90% Gold", "rarity": "key", "variety": "With Star"},
        ])

        # Quarter Eagles ($2.50)
        coins.extend([
            {"year": 1915, "mint": "S", "name": "Panama-Pacific Exposition", "mintage": 6749,
             "denomination": "Quarter Eagles", "weight_grams": 4.18, "diameter_mm": 18,
             "composition": "90% Gold", "rarity": "key"},
            {"year": 1926, "mint": "P", "name": "Sesquicentennial of American Independence", "mintage": 46019,
             "denomination": "Quarter Eagles", "weight_grams": 4.18, "diameter_mm": 18,
             "composition": "90% Gold", "rarity": "key"},
        ])

        # $50 Gold (Panama-Pacific)
        coins.extend([
            {"year": 1915, "mint": "S", "name": "Panama-Pacific Exposition Round", "mintage": 483,
             "denomination": "Fifty Dollars", "weight_grams": 83.59, "diameter_mm": 44,
             "composition": "90% Gold", "rarity": "key", "notes": "Extremely rare, round version"},
            {"year": 1915, "mint": "S", "name": "Panama-Pacific Exposition Octagonal", "mintage": 645,
             "denomination": "Fifty Dollars", "weight_grams": 83.59, "diameter_mm": 44,
             "composition": "90% Gold", "rarity": "key", "notes": "Extremely rare, octagonal version"},
        ])

        return coins

    def get_type_code(self, name: str, denomination: str) -> str:
        """Generate unique 4-character type code for commemorative."""
        # Map commemorative names to unique type codes
        type_codes = {
            # Half Dollars
            "World's Columbian Exposition": "WCOL",
            "Panama-Pacific International Exposition": "PPIE",
            "Illinois Centennial": "ILCN",
            "Maine Centennial": "MECN",
            "Pilgrim Tercentenary": "PILG",
            "Alabama Centennial": "ALCN",
            "Alabama Centennial 2X2": "ALXX",
            "Missouri Centennial": "MOCN",
            "Missouri Centennial 2★4": "MOSS",
            "Grant Memorial": "GRNT",
            "Grant Memorial with Star": "GRNS",
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
            "Iowa Statehood Centennial": "IASC",
            "Booker T. Washington": "BTWH",
            "Carver/Washington": "CARW",
            # Dollars
            "Lafayette Dollar": "LAFA",
            # Gold
            "Louisiana Purchase - Jefferson": "LPJF",
            "Louisiana Purchase - McKinley": "LPMK",
            "Lewis & Clark Exposition": "LEWC",
            "McKinley Memorial": "MCKI",
            "Panama-Pacific Exposition Round": "PPER",
            "Panama-Pacific Exposition Octagonal": "PPEO",
        }

        # For Panama-Pacific gold $1 and quarter eagle, use different codes
        if name == "Panama-Pacific Exposition":
            if "Gold Dollars" in denomination:
                return "PPGD"
            elif "Quarter Eagles" in denomination:
                return "PPQE"

        # For Sesquicentennial quarter eagle vs half dollar
        if name == "Sesquicentennial of American Independence" and "Quarter Eagles" in denomination:
            return "SAQE"

        # For Grant gold dollar with star
        if name == "Grant Memorial with Star" and "Gold Dollars" in denomination:
            return "GRGS"

        return type_codes.get(name, "COMM")

    def insert_coins_batch(self, coins: List[Dict], denomination: str, dry_run: bool = False):
        """Insert a batch of commemorative coins into the database."""
        if dry_run:
            print(f"\nDRY RUN: Would insert {len(coins)} {denomination}:")
            for coin in coins[:5]:  # Show first 5
                type_code = self.get_type_code(coin['name'], denomination)
                print(f"  - US-{type_code}-{coin['year']}-{coin['mint']}: {coin['name']}")
            if len(coins) > 5:
                print(f"  ... and {len(coins) - 5} more")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        inserted_count = 0
        skipped_count = 0

        try:
            for coin in coins:
                # Generate coin_id with unique type code per commemorative
                type_code = self.get_type_code(coin['name'], denomination)
                coin_id = f"US-{type_code}-{coin['year']}-{coin['mint']}"

                # Check if coin already exists
                cursor.execute('SELECT coin_id FROM coins WHERE coin_id = ?', (coin_id,))
                if cursor.fetchone():
                    print(f"  ⊘ Skipped (exists): {coin_id}")
                    skipped_count += 1
                    continue

                # Prepare coin data
                total_mintage = coin.get('mintage', 0)

                # Default composition and specs for half dollars unless overridden
                composition = coin.get('composition', '90% Silver, 10% Copper')
                weight_grams = coin.get('weight_grams', 12.5)
                diameter_mm = coin.get('diameter_mm', 30.6)

                # Insert coin
                cursor.execute('''
                    INSERT INTO coins (
                        coin_id, year, mint, denomination, series, variety,
                        composition, weight_grams, diameter_mm,
                        business_strikes, total_mintage, notes, rarity,
                        source_citation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    coin_id,
                    coin['year'],
                    coin['mint'],
                    denomination,
                    coin['name'],  # Series is the commemorative name
                    coin.get('variety'),
                    composition,
                    weight_grams,
                    diameter_mm,
                    total_mintage,  # business_strikes = total_mintage for commemoratives
                    total_mintage,
                    coin.get('notes'),
                    coin.get('rarity', 'common'),
                    'Issue #53 - Classic Commemoratives (1892-1954)'
                ))

                inserted_count += 1
                print(f"  ✓ {coin_id}: {coin['name']}")

            conn.commit()
            print(f"\n✓ Successfully inserted {inserted_count} coins")
            if skipped_count > 0:
                print(f"  ({skipped_count} already existed, skipped)")

        except sqlite3.Error as e:
            conn.rollback()
            print(f"\n✗ Database error: {e}")
            raise
        finally:
            conn.close()

    def run_migration(self, dry_run: bool = False):
        """Execute the complete commemorative coin migration."""
        print("=" * 60)
        print("US Classic Commemorative Coins Migration (1892-1954)")
        print("=" * 60)

        if not dry_run:
            self.create_backup()

        # Migrate commemorative half dollars
        print("\n--- Commemorative Half Dollars (1892-1954) ---")
        half_dollars = self.get_commemorative_half_dollars()
        self.insert_coins_batch(half_dollars, "Commemorative Half Dollars", dry_run)

        # Migrate commemorative dollars
        print("\n--- Commemorative Silver Dollars (1900-1939) ---")
        dollars = self.get_commemorative_dollars()
        self.insert_coins_batch(dollars, "Commemorative Dollars", dry_run)

        # Migrate commemorative gold (group by denomination)
        print("\n--- Commemorative Gold Coins (1903-1926) ---")
        gold_coins = self.get_commemorative_gold()

        # Group coins by denomination
        gold_by_denom = {}
        for coin in gold_coins:
            denom = coin.pop('denomination')
            if denom not in gold_by_denom:
                gold_by_denom[denom] = []
            gold_by_denom[denom].append(coin)

        # Insert each denomination group
        for denom, coins in gold_by_denom.items():
            self.insert_coins_batch(coins, denom, dry_run)

        if not dry_run:
            print(f"\n✓ Migration completed. Backup: {self.backup_path}")
            print("\nNext steps:")
            print("  1. Run: uv run python scripts/export_from_database.py")
            print("  2. Commit all changes with: git add . && git commit")

def main():
    parser = argparse.ArgumentParser(description='Add US Classic Commemorative Coins (1892-1954)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')

    args = parser.parse_args()

    migration = CommemorativeCoinMigration()

    try:
        migration.run_migration(dry_run=args.dry_run)

        if not args.dry_run:
            print("\n" + "=" * 60)
            print("✓ MIGRATION COMPLETE")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("DRY RUN COMPLETE - No changes made")
            print("Run without --dry-run to apply changes")
            print("=" * 60)

    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
