#!/usr/bin/env python3
"""
Enhancement Migration Script: Add VCD Guide Details to Commemorative Coins

This script enriches existing Classic Commemorative coins (1892-1954) with detailed
information from the Vegas Coin Dealer Complete Guide, including:
- Designer names
- Obverse descriptions
- Reverse descriptions
- Historical significance
- Commemorative purposes

Source: VCD Blog - "The Complete Guide to U.S. Classic Commemorative Coins (1892-1954)"
Database-First Pipeline: Updates coins table, then export to JSON

Usage:
    uv run python scripts/enhance_commemorative_coins.py
    uv run python scripts/enhance_commemorative_coins.py --dry-run
"""

import sqlite3
import argparse
from datetime import datetime
import os

class CommemorativeEnhancer:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_backup_commemorative_enhance_{timestamp}.db"

        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def get_commemorative_enhancements(self):
        """
        Return enhancement data for Classic Commemoratives from VCD guide.
        Each entry includes: coin_id, designer, obverse, reverse, notes, historical_significance
        """
        return [
            {
                "coin_id": "US-WCOL-1892-P",
                "designer": "Charles E. Barber (obverse), George T. Morgan (reverse)",
                "obverse": "Portrait bust of Columbus facing right",
                "reverse": "The flagship Santa Maria sailing west",
                "notes": "First U.S. commemorative coin. To celebrate Columbus' 400th anniversary journey and raise funds for the 1893 World's Fair. Sold for $1 at the fair.",
                "historical_significance": "First commemorative coin in U.S. history"
            },
            {
                "coin_id": "US-WCOL-1893-P",
                "designer": "Charles E. Barber (obverse), George T. Morgan (reverse)",
                "obverse": "Portrait bust of Columbus facing right",
                "reverse": "The flagship Santa Maria sailing west",
                "notes": "Part of World's Columbian Exposition series. To celebrate Columbus' 400th anniversary journey and raise funds for the 1893 World's Fair.",
                "historical_significance": "Second year of first commemorative series"
            },
            {
                "coin_id": "US-ISAB-1893-P",
                "designer": "Charles E. Barber",
                "obverse": "Crowned bust of Queen Isabella of Spain",
                "reverse": "A kneeling woman holding a distaff and spindle",
                "notes": "To raise funds for the Board of Lady Managers at the Columbian Exposition.",
                "historical_significance": "First U.S. coin to portray an actual woman (not Liberty)"
            },
            {
                "coin_id": "US-LAFA-1900-P",
                "designer": None,  # Not specified in guide
                "obverse": "Heads of Washington and Lafayette",
                "reverse": "Statue of Lafayette on horseback",
                "notes": "To fund an equestrian statue of Lafayette in Paris.",
                "historical_significance": "First commemorative silver dollar; first coin with Washington; first person (Lafayette) to appear on both sides"
            },
            {
                "coin_id": "US-PPIE-1915-S",
                "designer": None,
                "obverse": "Columbia with extended arms and a child holding cornucopia",
                "reverse": "Eagle with extended wings on a shield",
                "notes": "To celebrate the completion of the Panama Canal.",
                "historical_significance": None
            },
            {
                "coin_id": "US-ILCN-1918-P",
                "designer": None,
                "obverse": "Bust of Abraham Lincoln",
                "reverse": "Eagle with shield and state seal",
                "notes": "To commemorate 100 years of Illinois statehood.",
                "historical_significance": None
            },
            {
                "coin_id": "US-MECN-1920-P",
                "designer": None,
                "obverse": "Arms of the state of Maine with figures representing Commerce and Agriculture",
                "reverse": "Wreath of pine needles and cones",
                "notes": "To commemorate 100 years of Maine statehood.",
                "historical_significance": None
            },
            {
                "coin_id": "US-PILG-1920-P",
                "designer": None,
                "obverse": "Governor William Bradford carrying a Bible",
                "reverse": "The Mayflower sailing west",
                "notes": "To commemorate 300th anniversary of the Pilgrim landing.",
                "historical_significance": None
            },
            {
                "coin_id": "US-ALCN-1921-P",
                "designer": "Laura Gardin Fraser",
                "obverse": "Portraits of governors William Bibb and Thomas Kilby",
                "reverse": "Alabama state seal",
                "notes": "To commemorate 100 years of Alabama statehood.",
                "historical_significance": "First U.S. coin designed by a woman"
            },
            {
                "coin_id": "US-MOCN-1921-P",
                "designer": None,
                "obverse": "Bust of Daniel Boone wearing coonskin cap",
                "reverse": "Daniel Boone with Native American figure",
                "notes": "To commemorate 100 years of Missouri statehood.",
                "historical_significance": None
            },
            {
                "coin_id": "US-GRNT-1922-P",
                "designer": None,
                "obverse": "Bust of Ulysses S. Grant in military uniform",
                "reverse": "Grant's birthplace in Point Pleasant, Ohio",
                "notes": "To commemorate the centenary of Grant's birth.",
                "historical_significance": None
            },
            {
                "coin_id": "US-MNDO-1923-S",
                "designer": None,
                "obverse": "Busts of James Monroe and John Quincy Adams",
                "reverse": "Female figures representing North and South America",
                "notes": "To commemorate 100 years of the Monroe Doctrine.",
                "historical_significance": None
            },
            {
                "coin_id": "US-HUGE-1924-P",
                "designer": None,
                "obverse": "Busts of Admiral Gaspard de Coligny and William the Silent",
                "reverse": "The ship Nieu Nederlandt sailing",
                "notes": "To commemorate 300 years of New Netherland founding.",
                "historical_significance": None
            },
            {
                "coin_id": "US-CADJ-1925-S",
                "designer": None,
                "obverse": "A kneeling prospector with miner's pan",
                "reverse": "A grizzly bear walking",
                "notes": "To commemorate 75 years of California's statehood.",
                "historical_significance": None
            },
            {
                "coin_id": "US-FTVA-1925-P",
                "designer": None,
                "obverse": "Bust of Dr. John McLoughlin",
                "reverse": "A frontier trapper with Fort Vancouver and Mount Hood",
                "notes": "To commemorate 100 years of Fort Vancouver's founding.",
                "historical_significance": None
            },
            {
                "coin_id": "US-LEXC-1925-P",
                "designer": None,
                "obverse": "The Minute Man statue in Concord, Massachusetts",
                "reverse": "The Old Belfry in Lexington",
                "notes": "To commemorate 150 years since the Revolutionary War battles.",
                "historical_significance": None
            },
            {
                "coin_id": "US-STMN-1925-P",
                "designer": None,
                "obverse": "Generals Robert E. Lee and 'Stonewall' Jackson on horseback",
                "reverse": "Eagle perched on mountain precipice",
                "notes": "To fund the Stone Mountain Memorial.",
                "historical_significance": None
            },
            # Oregon Trail Memorial (multi-year series 1926-1939)
            {
                "series_pattern": "US-ORTR-%",  # Matches all Oregon Trail coins
                "designer": None,
                "obverse": "Conestoga wagon drawn by oxen heading west",
                "reverse": "Native American with outstretched arm and United States map",
                "notes": "To commemorate frontier families on the Oregon Trail.",
                "historical_significance": None
            },
            {
                "coin_id": "US-SEAI-1926-P",
                "designer": None,
                "obverse": "Heads of Washington and Calvin Coolidge",
                "reverse": "The Liberty Bell",
                "notes": "To commemorate 150 years of American independence.",
                "historical_significance": "Only living president (Coolidge) to appear on a U.S. coin"
            },
            {
                "coin_id": "US-VTSQ-1927-P",
                "designer": None,
                "obverse": "Head of Ira Allen, 'Founder of Vermont'",
                "reverse": "A catamount (mountain lion) with battle dates",
                "notes": "To commemorate 150 years of the Battle of Bennington.",
                "historical_significance": None
            },
            {
                "coin_id": "US-HISQ-1928-P",
                "designer": None,
                "obverse": "Head of Captain James Cook with compass needle",
                "reverse": "Native Hawaiian chief with Diamond Head in background",
                "notes": "To commemorate 150 years since Captain Cook's landing.",
                "historical_significance": None
            },
            # Daniel Boone Bicentennial (multi-year series 1934-1938)
            {
                "series_pattern": "US-DNBO-%",
                "designer": None,
                "obverse": "Bust of Daniel Boone",
                "reverse": "Boone with Native American chief holding peace treaty",
                "notes": "To commemorate 200 years since Boone's birth.",
                "historical_significance": None
            },
            {
                "coin_id": "US-MDTC-1934-P",
                "designer": None,
                "obverse": "Bust of Cecil Calvert (Lord Baltimore)",
                "reverse": "The coat of arms of Maryland",
                "notes": "To commemorate 300 years of Maryland's founding.",
                "historical_significance": None
            },
            # Texas Centennial (multi-year series 1934-1938)
            {
                "series_pattern": "US-TXCN-%",
                "designer": None,
                "obverse": "Eagle over a five-pointed star",
                "reverse": "Victory figure with the Alamo and portraits of Sam Houston and Stephen F. Austin",
                "notes": "To commemorate 100 years of Texas independence.",
                "historical_significance": None
            },
            # Arkansas Centennial (multi-year series 1935-1939)
            {
                "series_pattern": "US-ARCN-%",
                "designer": None,
                "obverse": "Native American chief and Lady Liberty",
                "reverse": "Eagle with Arkansas outline and diamond",
                "notes": "To commemorate 100 years of Arkansas statehood.",
                "historical_significance": None
            },
            # California-Pacific Exposition (1935-1936)
            {
                "series_pattern": "US-CAPE-%",
                "designer": None,
                "obverse": "Minerva from the California State Seal",
                "reverse": "Buildings from the 1915 Panama-California Exposition",
                "notes": "To commemorate the California-Pacific Exposition in San Diego.",
                "historical_significance": None
            },
            {
                "coin_id": "US-CTTC-1935-P",
                "designer": None,
                "obverse": "The Charter Oak tree",
                "reverse": "Eagle standing on rocky mound",
                "notes": "To commemorate 300 years of Connecticut's founding.",
                "historical_significance": None
            },
            {
                "coin_id": "US-HUNY-1935-P",
                "designer": None,
                "obverse": "The ship Half Moon sailing",
                "reverse": "Neptune riding backwards on a whale",
                "notes": "To commemorate 150 years of Hudson's founding.",
                "historical_significance": None
            },
            {
                "coin_id": "US-OSPT-1935-P",
                "designer": None,
                "obverse": "Head of a cow (referencing 'Cabeza de Vaca' meaning 'head of cow')",
                "reverse": "Yucca tree over a map of Gulf States with expedition route",
                "notes": "To commemorate Cabeza de Vaca's expedition.",
                "historical_significance": None
            },
            {
                "coin_id": "US-ALNY-1936-P",
                "designer": None,
                "obverse": "Beaver gnawing on maple branch",
                "reverse": "Governor Dongan, Robert Livingston, and the first mayor of Albany",
                "notes": "To commemorate 250 years of Albany's charter.",
                "historical_significance": None
            },
            {
                "coin_id": "US-ARRB-1936-P",
                "designer": None,
                "obverse": "Bust of Senator Joseph T. Robinson",
                "reverse": "Same as regular Arkansas Centennial design",
                "notes": "To raise funds for the Arkansas Centennial Commission.",
                "historical_significance": None
            },
            {
                "coin_id": "US-GTYB-1936-P",
                "designer": None,
                "obverse": "Confederate and Union veterans in uniform",
                "reverse": "Shields of Union and Confederate armies",
                "notes": "To commemorate 75 years since the battle.",
                "historical_significance": None
            },
            {
                "coin_id": "US-BDPT-1936-P",
                "designer": None,
                "obverse": "Bust of P.T. Barnum",
                "reverse": "Art Deco stylized eagle",
                "notes": "To commemorate P.T. Barnum and Bridgeport's centennial.",
                "historical_significance": None
            },
            # Cincinnati Music Center (1936 P/D/S)
            {
                "series_pattern": "US-CNMC-%",
                "designer": None,
                "obverse": "Stephen Foster, 'America's Troubadour'",
                "reverse": "Kneeling figure representing the goddess of music",
                "notes": "To commemorate 50 years of Cincinnati as a music center.",
                "historical_significance": None
            },
            {
                "coin_id": "US-CLVC-1936-P",
                "designer": None,
                "obverse": "Bust of Moses Cleaveland",
                "reverse": "Map of Great Lakes region with compass",
                "notes": "To commemorate 100 years of Cleveland's incorporation.",
                "historical_significance": None
            },
            # Columbia, South Carolina Sesquicentennial (1936 P/D/S)
            {
                "series_pattern": "US-COSC-%",
                "designer": None,
                "obverse": "Justice between the Old and New State Houses",
                "reverse": "Palmetto tree with crossed arrows",
                "notes": "To commemorate 150 years of Columbia's founding.",
                "historical_significance": None
            },
            {
                "coin_id": "US-DETC-1936-P",
                "designer": None,
                "obverse": "Old Swedes Church",
                "reverse": "Ship Kalmar Nyckel with three diamonds representing Delaware counties",
                "notes": "To commemorate 300 years of Delaware settlement.",
                "historical_significance": None
            },
            {
                "coin_id": "US-ELIL-1936-P",
                "designer": None,
                "obverse": "Bearded pioneer wearing fur cap",
                "reverse": "Four adult pioneers and baby",
                "notes": "To commemorate 100 years of Elgin's founding.",
                "historical_significance": None
            },
            {
                "coin_id": "US-LITC-1936-P",
                "designer": None,
                "obverse": "Heads of Dutch settler and Algonquin Native American",
                "reverse": "Dutch three-masted ship sailing",
                "notes": "To commemorate 300 years of Long Island settlement.",
                "historical_significance": None
            },
            {
                "coin_id": "US-LYVA-1936-P",
                "designer": None,
                "obverse": "Senator Carter Glass",
                "reverse": "Goddess Liberty with Monument Terrace and courthouse",
                "notes": "To commemorate 150 years of Lynchburg's incorporation.",
                "historical_significance": "Third living person on a U.S. coin"
            },
            {
                "coin_id": "US-NFVA-1936-P",
                "designer": None,
                "obverse": "Seal of Norfolk with three-masted ship",
                "reverse": "Royal Mace with British crown",
                "notes": "To commemorate Norfolk land grant and borough establishment.",
                "historical_significance": None
            },
            # Providence, Rhode Island Tercentenary (1936 P/D/S)
            {
                "series_pattern": "US-PVRI-%",
                "designer": None,
                "obverse": "Roger Williams in canoe greeting Native American",
                "reverse": "Anchor of Hope from Rhode Island state seal",
                "notes": "To commemorate 300 years of Providence's founding.",
                "historical_significance": None
            },
            {
                "coin_id": "US-SFBB-1936-S",
                "designer": None,
                "obverse": "California grizzly bear",
                "reverse": "The Bay Bridge with San Francisco Ferry Building",
                "notes": "To commemorate the opening of the Bay Bridge.",
                "historical_significance": None
            },
            {
                "coin_id": "US-WITC-1936-P",
                "designer": None,
                "obverse": "Badger standing on log with arrows and olive branch",
                "reverse": "Miner's arm with pickaxe and lead ore",
                "notes": "To commemorate 100 years of Wisconsin Territory.",
                "historical_significance": None
            },
            {
                "coin_id": "US-YCME-1936-P",
                "designer": None,
                "obverse": "Brown's Garrison stockade with sentries",
                "reverse": "Seal of York County, Maine",
                "notes": "To commemorate 300 years of York County's founding.",
                "historical_significance": None
            },
            {
                "coin_id": "US-ANTM-1937-P",
                "designer": None,
                "obverse": "Profiles of Generals McClellan and Lee",
                "reverse": "Burnside Bridge over Antietam Creek",
                "notes": "To commemorate 75 years since the battle.",
                "historical_significance": None
            },
            {
                "coin_id": "US-ROAN-1937-P",
                "designer": None,
                "obverse": "Sir Walter Raleigh",
                "reverse": "Eleanor Dare holding Virginia Dare with sailing ships",
                "notes": "To commemorate 350 years of Roanoke colony.",
                "historical_significance": None
            },
            {
                "coin_id": "US-NWRC-1938-P",
                "designer": None,
                "obverse": "John Pell holding fatted calf",
                "reverse": "Fleur-de-lis",
                "notes": "To commemorate 250 years of New Rochelle's founding.",
                "historical_significance": "Last U.S. coin with denticles along the rim"
            },
            {
                "coin_id": "US-IASC-1946-P",
                "designer": None,
                "obverse": "Old Stone Capitol in Iowa City",
                "reverse": "Eagle with Iowa state motto and 29 stars",
                "notes": "To commemorate 100 years of Iowa statehood.",
                "historical_significance": None
            },
            # Booker T. Washington (multi-year series 1946-1951)
            {
                "series_pattern": "US-BTWH-%",
                "designer": None,
                "obverse": "Three-quarter bust of Washington",
                "reverse": "Hall of Fame for Great Americans and Washington's birth cabin",
                "notes": "To honor Booker T. Washington and fund memorials.",
                "historical_significance": "First African American to appear on a U.S. coin"
            },
            # Carver/Washington (multi-year series 1951-1954)
            {
                "series_pattern": "US-CARW-%",
                "designer": None,
                "obverse": "Busts of both Booker T. Washington and George Washington Carver",
                "reverse": "Map of United States with 'Freedom and Opportunity for All'",
                "notes": "To honor both Booker T. Washington and George Washington Carver.",
                "historical_significance": "Final issue in the Classic Commemorative series"
            },
        ]

    def enhance_coins(self, conn, dry_run=False):
        """Update existing commemorative coins with enhanced data."""
        cursor = conn.cursor()
        enhancements = self.get_commemorative_enhancements()

        updated_count = 0
        skipped_count = 0

        for coin_data in enhancements:
            # Handle both specific coin_id and series_pattern (for multi-year issues)
            if 'series_pattern' in coin_data:
                # Match multiple coins with pattern (e.g., US-ORTR-% for all Oregon Trail)
                pattern = coin_data['series_pattern']
                cursor.execute("SELECT coin_id FROM coins WHERE coin_id LIKE ?", (pattern,))
                matching_coins = cursor.fetchall()

                if not matching_coins:
                    print(f"⚠ No coins matching pattern {pattern} - skipping")
                    skipped_count += 1
                    continue

                # Process each matching coin
                for (coin_id,) in matching_coins:
                    result = self._update_single_coin(conn, cursor, coin_id, coin_data, dry_run)
                    if result:
                        updated_count += 1
                    else:
                        skipped_count += 1
                continue

            # Handle specific coin_id
            coin_id = coin_data['coin_id']

            # Check if coin exists
            cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
            if not cursor.fetchone():
                print(f"⚠ Coin {coin_id} not found in database - skipping")
                skipped_count += 1
                continue

            result = self._update_single_coin(conn, cursor, coin_id, coin_data, dry_run)
            if result:
                updated_count += 1
            else:
                skipped_count += 1

        if not dry_run:
            conn.commit()

        return updated_count, skipped_count

    def _update_single_coin(self, conn, cursor, coin_id, coin_data, dry_run):
        """Update a single coin with enhancement data. Returns True if updated, False if skipped."""
        # Build update query dynamically based on non-None values
        updates = []
        params = []

        if coin_data.get('designer'):
            updates.append("designer = ?")
            params.append(coin_data['designer'])

        if coin_data.get('obverse'):
            updates.append("obverse_description = ?")
            params.append(coin_data['obverse'])

        if coin_data.get('reverse'):
            updates.append("reverse_description = ?")
            params.append(coin_data['reverse'])

        # Combine notes with historical significance if both exist
        notes_parts = []
        if coin_data.get('notes'):
            notes_parts.append(coin_data['notes'])
        if coin_data.get('historical_significance'):
            notes_parts.append(f"Historical Significance: {coin_data['historical_significance']}")

        if notes_parts:
            updates.append("notes = ?")
            params.append(" ".join(notes_parts))

        if not updates:
            print(f"⚠ No updates for {coin_id} - skipping")
            return False

        # Add coin_id to params for WHERE clause
        params.append(coin_id)

        update_query = f"UPDATE coins SET {', '.join(updates)} WHERE coin_id = ?"

        if dry_run:
            print(f"[DRY RUN] Would update {coin_id}:")
            print(f"  Designer: {coin_data.get('designer', 'N/A')}")
            print(f"  Obverse: {coin_data.get('obverse', 'N/A')[:50]}..." if coin_data.get('obverse') else "  Obverse: N/A")
            print(f"  Reverse: {coin_data.get('reverse', 'N/A')[:50]}..." if coin_data.get('reverse') else "  Reverse: N/A")
        else:
            cursor.execute(update_query, params)
            print(f"✓ Enhanced {coin_id}")

        return True

    def run(self, dry_run=False):
        """Execute the enhancement migration."""
        print("=" * 60)
        print("Commemorative Coin Enhancement Migration")
        print("=" * 60)
        print(f"Database: {self.db_path}")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print()

        if not dry_run:
            self.create_backup()

        conn = sqlite3.connect(self.db_path)

        try:
            updated, skipped = self.enhance_coins(conn, dry_run)

            print()
            print("=" * 60)
            print("Migration Summary")
            print("=" * 60)
            print(f"Coins enhanced: {updated}")
            print(f"Coins skipped: {skipped}")

            if not dry_run and updated > 0:
                print()
                print("Next steps:")
                print("1. Run: uv run python scripts/export_from_database.py")
                print("2. Commit changes: git add . && git commit")

        finally:
            conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Enhance commemorative coins with VCD guide details'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )

    args = parser.parse_args()

    enhancer = CommemorativeEnhancer()
    enhancer.run(dry_run=args.dry_run)
