#!/usr/bin/env python3
"""
Add International Bullion type codes to the coin taxonomy database.
Issue #74

Adds:
- CA-SMLO: Canadian Silver Maple Leaf 1 oz (1988-present)
- CA-GMLO: Canadian Gold Maple Leaf 1 oz (1979-present)
- CA-SMLI: Canadian Incuse Silver Maple Leaf (2018-present)
- CN-PAND: Chinese Silver Panda (1983-present)
- AU-WTED: Australian Wedge-Tailed Eagle (2014-present)

Each includes a XXXX-X entry for random year bullion purchases.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# International bullion series definitions
INTL_BULLION_SERIES = [
    {
        "country": "CA",
        "code": "SMLO",
        "name": "Silver Maple Leaf 1 oz",
        "denomination": "Five Dollars",
        "start_year": 1988,
        "end_year": None,  # Ongoing
        "weight_oz": 1.0,
        "composition": {"silver": 99.99},
        "weight_grams": 31.1035,
        "diameter_mm": 38.0,
        "edge": "Reeded",
        "designer": "Royal Canadian Mint",
        "obverse": "Queen Elizabeth II (various portraits), 'ELIZABETH II', 'CANADA', '5 DOLLARS', date",
        "reverse": "Maple leaf, 'FINE SILVER 1 OZ ARGENT PUR', '9999'",
        "aliases": ["Canadian Silver Maple Leaf", "Silver Maple Leaf", "SML"],
    },
    {
        "country": "CA",
        "code": "GMLO",
        "name": "Gold Maple Leaf 1 oz",
        "denomination": "$50",
        "start_year": 1979,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"gold": 99.99},
        "weight_grams": 31.1035,
        "diameter_mm": 30.0,
        "edge": "Reeded",
        "designer": "Royal Canadian Mint",
        "obverse": "Queen Elizabeth II (various portraits), 'ELIZABETH II', 'CANADA', '50 DOLLARS', date",
        "reverse": "Maple leaf, 'FINE GOLD 1 OZ OR PUR', '9999'",
        "aliases": ["Canadian Gold Maple Leaf", "Gold Maple Leaf", "GML"],
    },
    {
        "country": "CA",
        "code": "SMLI",
        "name": "Incuse Silver Maple Leaf",
        "denomination": "Five Dollars",
        "start_year": 2018,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"silver": 99.99},
        "weight_grams": 31.1035,
        "diameter_mm": 38.0,
        "edge": "Reeded",
        "designer": "Royal Canadian Mint",
        "obverse": "Queen Elizabeth II incuse portrait, 'ELIZABETH II', 'CANADA', '5 DOLLARS', date",
        "reverse": "Incuse maple leaf design, 'FINE SILVER 1 OZ ARGENT PUR', security features",
        "aliases": ["Incuse Maple Leaf", "Incuse SML"],
        "notes": "Features incuse design with Bullion DNA anti-counterfeiting technology",
    },
    {
        "country": "CN",
        "code": "PAND",
        "name": "Silver Panda",
        "denomination": "Ten Yuan",
        "start_year": 1983,
        "end_year": None,
        "weight_oz": 1.0,  # Note: varied 1oz/30g over time
        "composition": {"silver": 99.9},
        "weight_grams": 30.0,  # 30g since 2016 (was 1oz before)
        "diameter_mm": 40.0,
        "edge": "Reeded",
        "designer": "China Gold Coin Incorporation",
        "obverse": "Temple of Heaven, 'ZHONGHUA RENMIN GONGHEGUO' (People's Republic of China), date",
        "reverse": "Giant panda design (changes annually), 'Ag.999', weight denomination",
        "aliases": ["Chinese Silver Panda", "China Panda", "Panda"],
        "notes": "Panda design changes each year, highly collectible. Weight changed from 1oz to 30g in 2016.",
    },
    {
        "country": "AU",
        "code": "WTED",
        "name": "Wedge-Tailed Eagle 1 oz Silver",
        "denomination": "One Dollar",
        "start_year": 2014,
        "end_year": None,
        "weight_oz": 1.0,
        "composition": {"silver": 99.99},
        "weight_grams": 31.1035,
        "diameter_mm": 40.6,
        "edge": "Reeded",
        "designer": "John Mercanti (designer), Perth Mint",
        "obverse": "Queen Elizabeth II (Ian Rank-Broadley portrait), 'ELIZABETH II', 'AUSTRALIA', '1 DOLLAR', date",
        "reverse": "Wedge-tailed eagle in flight, designed by John Mercanti, 'AUSTRALIAN WEDGE-TAILED EAGLE', '1oz 9999 SILVER'",
        "aliases": ["Australian Wedge-Tailed Eagle", "Wedge-Tailed Eagle", "WTE"],
        "notes": "Designed by John Mercanti (former US Mint Chief Engraver). Perth Mint product.",
    },
]


def add_international_bullion(conn):
    """Add international bullion series to database"""
    cursor = conn.cursor()

    for series in INTL_BULLION_SERIES:
        country = series["country"]
        code = series["code"]
        name = series["name"]
        full_code = f"{country}-{code}"
        print(f"Adding {name} ({full_code})...")

        # Add to series_registry
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'coin', ?)
        """, (
            f"{name}__{series['denomination'].replace(' ', '_')}",
            name,
            code,
            country,
            series["denomination"],
            series["start_year"],
            series["end_year"],
            f"Bullion coin, {series['weight_oz']} oz {list(series['composition'].keys())[0]}",
            name,
            json.dumps(series.get("aliases", [])),
        ))

        # Add XXXX-X entry for random year bullion
        xxxx_coin_id = f"{country}-{code}-XXXX-X"
        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, notes, rarity,
                source_citation
            ) VALUES (?, 'XXXX', 'X', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', 'Official mint specifications')
        """, (
            xxxx_coin_id,
            series["denomination"],
            name,
            json.dumps(series["composition"]),
            series["weight_grams"],
            series["diameter_mm"],
            series["edge"],
            series["designer"],
            series["obverse"],
            series["reverse"],
            f"Random year bullion - valued by metal content. {series.get('notes', '')}".strip(),
        ))

        print(f"  ✓ Added series_registry entry and bullion entry {xxxx_coin_id}")

    conn.commit()
    print(f"\n✅ Added {len(INTL_BULLION_SERIES)} international bullion series")


def main():
    db_path = Path(__file__).parent.parent / "database" / "coins.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return 1

    conn = sqlite3.connect(db_path)
    try:
        add_international_bullion(conn)
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    exit(main())
