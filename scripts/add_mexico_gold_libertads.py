#!/usr/bin/env python3
"""
Migration script to add Mexico Gold Libertad data to the coin taxonomy database.

Data source: mexicannumismatics.com and findbullionprices.com

Gold Libertad specifications:
- Fineness: .900 Au (1981-1990), .999 Au (1991-present)
- Mint: Mexico City (Mo)
- Denominations: 1 oz, 1/2 oz, 1/4 oz, 1/10 oz, 1/20 oz

Coin ID format:
- 1 oz: MX-GLIB-YEAR-M
- 1/2 oz: MX-GLIB-YEAR-M-12oz
- 1/4 oz: MX-GLIB-YEAR-M-14oz
- 1/10 oz: MX-GLIB-YEAR-M-110oz
- 1/20 oz: MX-GLIB-YEAR-M-120oz
"""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "coins.db"

# Gold Libertad specifications by denomination
DENOMINATIONS = {
    "1 oz": {
        "suffix": "",
        "weight_grams": 31.103,
        "diameter_mm": 34.5,
        "denomination": "Gold Libertad 1 oz",
    },
    "1/2 oz": {
        "suffix": "-12oz",
        "weight_grams": 15.552,
        "diameter_mm": 29.0,
        "denomination": "Gold Libertad 1/2 oz",
    },
    "1/4 oz": {
        "suffix": "-14oz",
        "weight_grams": 7.776,
        "diameter_mm": 23.0,
        "denomination": "Gold Libertad 1/4 oz",
    },
    "1/10 oz": {
        "suffix": "-110oz",
        "weight_grams": 3.11,
        "diameter_mm": 16.0,
        "denomination": "Gold Libertad 1/10 oz",
    },
    "1/20 oz": {
        "suffix": "-120oz",
        "weight_grams": 1.555,
        "diameter_mm": 13.0,
        "denomination": "Gold Libertad 1/20 oz",
    },
}

# Uncirculated mintage data (1981-2023)
# Format: {year: {denom: mintage}}
UNCIRCULATED_MINTAGES = {
    1981: {"1/4 oz": 313000, "1/2 oz": 193000, "1 oz": 596000},
    1991: {"1/20 oz": 10000, "1/10 oz": 10000, "1/4 oz": 10000, "1/2 oz": 10000, "1 oz": 109193},
    1992: {"1/20 oz": 63858, "1/10 oz": 50592, "1/4 oz": 27321, "1/2 oz": 24343, "1 oz": 46281},
    1993: {"1/20 oz": 10000, "1/10 oz": 10000, "1/4 oz": 2500, "1/2 oz": 2500, "1 oz": 73881},
    1994: {"1/20 oz": 10000, "1/10 oz": 10000, "1/4 oz": 2500, "1/2 oz": 2500, "1 oz": 1000},
    2000: {"1/20 oz": 5300, "1/10 oz": 3500, "1/4 oz": 2500, "1/2 oz": 1500, "1 oz": 2370},
    2002: {"1/20 oz": 5000, "1/10 oz": 5000, "1/4 oz": 5000, "1/2 oz": 5000, "1 oz": 15000},
    2003: {"1/20 oz": 800, "1/10 oz": 300, "1/4 oz": 300, "1/2 oz": 300, "1 oz": 500},
    2004: {"1/20 oz": 4000, "1/10 oz": 2000, "1/4 oz": 1500, "1/2 oz": 500, "1 oz": 3000},
    2005: {"1/20 oz": 3200, "1/10 oz": 500, "1/4 oz": 500, "1/2 oz": 500, "1 oz": 3000},
    2006: {"1/20 oz": 3000, "1/10 oz": 4000, "1/4 oz": 1500, "1/2 oz": 500, "1 oz": 4000},
    2007: {"1/20 oz": 1200, "1/10 oz": 1200, "1/4 oz": 500, "1/2 oz": 500, "1 oz": 2500},
    2008: {"1/20 oz": 800, "1/10 oz": 2500, "1/4 oz": 800, "1/2 oz": 300, "1 oz": 800},
    2009: {"1/20 oz": 2000, "1/10 oz": 9000, "1/4 oz": 3000, "1/2 oz": 3000, "1 oz": 6200},
    2010: {"1/20 oz": 1500, "1/10 oz": 4500, "1/4 oz": 1500, "1/2 oz": 1500, "1 oz": 4000},
    2011: {"1/20 oz": 2500, "1/10 oz": 6500, "1/4 oz": 1500, "1/2 oz": 1500, "1 oz": 3000},
    2012: {"1 oz": 3000},  # Only 1 oz available
    2013: {"1/20 oz": 650, "1/10 oz": 2150, "1/4 oz": 750, "1/2 oz": 500, "1 oz": 2350},
    2014: {"1/20 oz": 1050, "1/10 oz": 2450, "1/4 oz": 1000, "1/2 oz": 1000, "1 oz": 4050},
    2015: {"1/20 oz": 1300, "1/10 oz": 4100, "1/4 oz": 1300, "1/2 oz": 1100, "1 oz": 4800},
    2016: {"1/20 oz": 2900, "1/10 oz": 3800, "1/4 oz": 1000, "1/2 oz": 1200, "1 oz": 4100},
    2017: {"1/20 oz": 1000, "1/10 oz": 300, "1/4 oz": 500, "1/2 oz": 700, "1 oz": 900},
    2018: {"1/20 oz": 2500, "1/10 oz": 1500, "1/4 oz": 1250, "1/2 oz": 1250, "1 oz": 2050},
    2019: {"1/20 oz": 1500, "1/10 oz": 1250, "1/4 oz": 1500, "1/2 oz": 1500, "1 oz": 2000},
    2020: {"1/20 oz": 700, "1/10 oz": 700, "1/4 oz": 700, "1/2 oz": 700, "1 oz": 1100},
    2021: {"1/20 oz": 1000, "1/10 oz": 850, "1/4 oz": 500, "1/2 oz": 500, "1 oz": 1050},
    2022: {"1/20 oz": 1100, "1/10 oz": 1400, "1/4 oz": 1300, "1/2 oz": 1000, "1 oz": 1900},
    2023: {"1/20 oz": 2000, "1/10 oz": 1750, "1/4 oz": 1000, "1/2 oz": 1000, "1 oz": 1500},
}

# Proof mintage data (includes regular proof; reverse proof noted separately)
# Format: {year: {denom: (proof, reverse_proof) or just proof}}
PROOF_MINTAGES = {
    1989: {"1 oz": 704},
    2004: {"1 oz": 1000},
    2005: {"1/20 oz": 400, "1/10 oz": 400, "1/4 oz": 2600, "1/2 oz": 400, "1 oz": 250},
    2006: {"1/20 oz": 520, "1/10 oz": 520, "1/4 oz": 2120, "1/2 oz": 520, "1 oz": 520},
    2007: {"1/20 oz": 500, "1/10 oz": 500, "1/4 oz": 1500, "1/2 oz": 500, "1 oz": 500},
    2008: {"1/20 oz": 500, "1/10 oz": 500, "1/4 oz": 800, "1/2 oz": 500, "1 oz": 500},
    2009: {"1/20 oz": 600, "1/10 oz": 600, "1/4 oz": 1700, "1/2 oz": 600, "1 oz": 600},
    2010: {"1/20 oz": 600, "1/10 oz": 600, "1/4 oz": 1000, "1/2 oz": 600, "1 oz": 600},
    2011: {"1/20 oz": 1100, "1/10 oz": 1100, "1/4 oz": 2000, "1/2 oz": 1100, "1 oz": 1100},
    2013: {"1/20 oz": 300, "1/10 oz": 300, "1/4 oz": 600, "1/2 oz": 300, "1 oz": 400},
    2014: {"1/20 oz": 250, "1/10 oz": 250, "1/4 oz": 250, "1/2 oz": 250, "1 oz": 250},
    2015: {"1/20 oz": 500, "1/10 oz": 500, "1/4 oz": 500, "1/2 oz": 500, "1 oz": 500},
    2016: {"1/20 oz": 2100, "1/10 oz": 2100, "1/4 oz": 2100, "1/2 oz": 2100, "1 oz": 2100},
    2017: {"1/20 oz": 600, "1/10 oz": 1500, "1/4 oz": 1500, "1/2 oz": 700, "1 oz": 600},
    # 2018+ have both proof and reverse proof for 1/2 oz and 1 oz
    2018: {"1/20 oz": 1000, "1/10 oz": 1500, "1/4 oz": 1000, "1/2 oz": (1000, 1000), "1 oz": (1000, 1000)},
    2019: {"1/20 oz": 1000, "1/10 oz": 1000, "1/4 oz": 800, "1/2 oz": (650, 500), "1 oz": (750, 500)},
    2020: {"1/20 oz": 250, "1/10 oz": 250, "1/4 oz": 250, "1/2 oz": (250, 250), "1 oz": (250, 250)},
    2021: {"1/20 oz": 350, "1/10 oz": 450, "1/4 oz": 450, "1/2 oz": (450, 500), "1 oz": (500, 500)},
    2022: {"1/20 oz": 1200, "1/10 oz": 1100, "1/4 oz": 1400, "1/2 oz": (1000, 500), "1 oz": (1300, 500)},
    2023: {"1/20 oz": 1000, "1/10 oz": 1000, "1/4 oz": 1000, "1/2 oz": (1000, 1000), "1 oz": (1000, 1000)},
}


def get_composition(year: int) -> str:
    """Return gold composition based on year."""
    return ".900 Au" if year <= 1990 else ".999 Au"


def get_rarity(mintage: int) -> str:
    """Determine rarity based on mintage."""
    if mintage <= 500:
        return "key"
    elif mintage <= 2000:
        return "semi-key"
    elif mintage <= 10000:
        return "scarce"
    return "common"


def add_gold_libertads(conn: sqlite3.Connection):
    """Add all Gold Libertad coins to the database."""
    cursor = conn.cursor()

    coins_added = 0
    coins_updated = 0

    # Process each year's uncirculated data
    for year, denoms in UNCIRCULATED_MINTAGES.items():
        for denom_name, mintage in denoms.items():
            denom_spec = DENOMINATIONS[denom_name]
            coin_id = f"MX-GLIB-{year}-M{denom_spec['suffix']}"

            # Get proof mintage if exists
            proof_mintage = None
            reverse_proof = None
            if year in PROOF_MINTAGES and denom_name in PROOF_MINTAGES[year]:
                proof_data = PROOF_MINTAGES[year][denom_name]
                if isinstance(proof_data, tuple):
                    proof_mintage, reverse_proof = proof_data
                else:
                    proof_mintage = proof_data

            # Build notes
            notes_parts = []
            if reverse_proof:
                notes_parts.append(f"Reverse proof mintage: {reverse_proof:,}")
            if year in [1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990]:
                if mintage is None:
                    notes_parts.append("Production gap year")

            notes = "; ".join(notes_parts) if notes_parts else None

            # Check if coin exists
            cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
            existing = cursor.fetchone()

            if existing:
                # Update existing record
                cursor.execute("""
                    UPDATE coins SET
                        business_strikes = ?,
                        proof_strikes = ?,
                        total_mintage = ?,
                        notes = COALESCE(notes || '; ' || ?, notes, ?),
                        rarity = ?
                    WHERE coin_id = ?
                """, (
                    mintage,
                    proof_mintage,
                    mintage + (proof_mintage or 0) + (reverse_proof or 0),
                    notes, notes,
                    get_rarity(mintage),
                    coin_id
                ))
                coins_updated += 1
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO coins (
                        coin_id, year, mint, denomination, series,
                        composition, weight_grams, diameter_mm, edge,
                        obverse_description, reverse_description,
                        business_strikes, proof_strikes, total_mintage,
                        notes, rarity, source_citation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    coin_id,
                    str(year),
                    "M",  # Mexico City mint
                    denom_spec["denomination"],
                    "Gold Libertad",
                    get_composition(year),
                    denom_spec["weight_grams"],
                    denom_spec["diameter_mm"],
                    "Reeded",
                    "Winged Victoria (Angel of Independence)",
                    "Mexican coat of arms with eagle on cactus",
                    mintage,
                    proof_mintage,
                    mintage + (proof_mintage or 0) + (reverse_proof or 0),
                    notes,
                    get_rarity(mintage),
                    "mexicannumismatics.com; findbullionprices.com"
                ))
                coins_added += 1

    # Add proof-only years (where no uncirculated version exists)
    for year, denoms in PROOF_MINTAGES.items():
        for denom_name, proof_data in denoms.items():
            if year in UNCIRCULATED_MINTAGES and denom_name in UNCIRCULATED_MINTAGES[year]:
                continue  # Already handled above

            denom_spec = DENOMINATIONS[denom_name]
            coin_id = f"MX-GLIB-{year}-M{denom_spec['suffix']}"

            if isinstance(proof_data, tuple):
                proof_mintage, reverse_proof = proof_data
            else:
                proof_mintage = proof_data
                reverse_proof = None

            notes = None
            if reverse_proof:
                notes = f"Reverse proof mintage: {reverse_proof:,}; Proof-only issue (no uncirculated version)"
            else:
                notes = "Proof-only issue (no uncirculated version)"

            # Check if exists
            cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
            if cursor.fetchone():
                continue

            cursor.execute("""
                INSERT INTO coins (
                    coin_id, year, mint, denomination, series,
                    composition, weight_grams, diameter_mm, edge,
                    obverse_description, reverse_description,
                    business_strikes, proof_strikes, total_mintage,
                    notes, rarity, source_citation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin_id,
                str(year),
                "M",
                denom_spec["denomination"],
                "Gold Libertad",
                get_composition(year),
                denom_spec["weight_grams"],
                denom_spec["diameter_mm"],
                "Reeded",
                "Winged Victoria (Angel of Independence)",
                "Mexican coat of arms with eagle on cactus",
                None,  # No business strikes
                proof_mintage,
                proof_mintage + (reverse_proof or 0),
                notes,
                get_rarity(proof_mintage),
                "mexicannumismatics.com; findbullionprices.com"
            ))
            coins_added += 1

    conn.commit()
    print(f"Added {coins_added} new Gold Libertad coins")
    print(f"Updated {coins_updated} existing Gold Libertad coins")

    return coins_added + coins_updated


def main():
    print("=" * 60)
    print("Adding Mexico Gold Libertad data to coin taxonomy database")
    print("=" * 60)

    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        return 1

    conn = sqlite3.connect(DB_PATH)

    try:
        total = add_gold_libertads(conn)
        print(f"\nTotal Gold Libertad entries: {total}")

        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT denomination, COUNT(*), MIN(year), MAX(year)
            FROM coins
            WHERE series = 'Gold Libertad'
            GROUP BY denomination
            ORDER BY weight_grams DESC
        """)

        print("\nGold Libertad summary by denomination:")
        print("-" * 50)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} coins ({row[2]}-{row[3]})")

        # Show key dates
        cursor.execute("""
            SELECT coin_id, business_strikes, rarity
            FROM coins
            WHERE series = 'Gold Libertad' AND rarity = 'key'
            ORDER BY business_strikes ASC
            LIMIT 10
        """)

        print("\nKey dates (lowest mintages):")
        print("-" * 50)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]:,} mintage")

    except Exception as e:
        print(f"ERROR: {e}")
        conn.rollback()
        return 1
    finally:
        conn.close()

    print("\n" + "=" * 60)
    print("Migration complete! Run 'uv run python scripts/export_from_database.py'")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit(main())
