#!/usr/bin/env python3
"""
Add Large Mexican Libertad Type Codes - Issue #83

Adds type codes for larger Mexican Libertad sizes and platinum:
  Silver: MLSW (2oz), MLSF (5oz), MLSK (1kg)
  Platinum: MLPO (1oz)

Uses XXXX year pattern for random-year bullion entries (AI classification).
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import shutil


# Database path
DB_PATH = Path(__file__).parent.parent / "database" / "coins.db"

# Large Silver Libertads (.999 fine silver)
SILVER_LARGE = {
    "MLSW": {
        "denomination": "Mexican Libertad Silver 2 oz",
        "series": "Mexican Libertad Silver 2 oz",
        "weight_grams": 62.206,
        "diameter_mm": 48.0,
        "weight_oz": 2.0,
        "composition": ".999 Ag",
    },
    "MLSF": {
        "denomination": "Mexican Libertad Silver 5 oz",
        "series": "Mexican Libertad Silver 5 oz",
        "weight_grams": 155.515,
        "diameter_mm": 65.0,
        "weight_oz": 5.0,
        "composition": ".999 Ag",
    },
    "MLSK": {
        "denomination": "Mexican Libertad Silver 1 kg",
        "series": "Mexican Libertad Silver 1 kg",
        "weight_grams": 1000.0,
        "diameter_mm": 110.0,
        "weight_oz": 32.15,  # ~32.15 troy oz in 1 kg
        "composition": ".999 Ag",
    },
}

# Platinum Libertad (.9995 fine platinum)
PLATINUM = {
    "MLPO": {
        "denomination": "Mexican Libertad Platinum 1 oz",
        "series": "Mexican Libertad Platinum 1 oz",
        "weight_grams": 31.103,
        "diameter_mm": 32.0,
        "weight_oz": 1.0,
        "composition": ".9995 Pt",
    },
}

# Combine all for easier iteration
ALL_LIBERTADS = {**SILVER_LARGE, **PLATINUM}


def backup_database():
    """Create backup before migration."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)

    backup = backup_dir / f'coins_backup_large_libertads_{timestamp}.db'
    shutil.copy(DB_PATH, backup)
    print(f"Database backed up to {backup}")
    return backup


def add_to_coins_table(conn: sqlite3.Connection, type_code: str, specs: dict) -> bool:
    """Add entry to the coins table."""
    cursor = conn.cursor()
    coin_id = f"MX-{type_code}-XXXX-MO"

    # Check if already exists
    cursor.execute("SELECT coin_id FROM coins WHERE coin_id = ?", (coin_id,))
    if cursor.fetchone():
        print(f"  [coins] Skipping {coin_id} - already exists")
        return False

    metal = "silver" if specs["composition"].endswith("Ag") else "platinum"
    rarity = "common" if metal == "silver" else "scarce"

    cursor.execute("""
        INSERT INTO coins (
            coin_id, year, mint, denomination, series,
            composition, weight_grams, diameter_mm, edge,
            obverse_description, reverse_description,
            notes, rarity, source_citation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        coin_id,
        "XXXX",
        "MO",
        specs["denomination"],
        specs["series"],
        specs["composition"],
        specs["weight_grams"],
        specs["diameter_mm"],
        "Reeded",
        "Winged Victory (Angel of Independence)",
        "Mexican coat of arms with eagle on cactus",
        f"Random year bullion ({specs['weight_oz']} oz {metal})",
        rarity,
        "Casa de Moneda de Mexico; findbullionprices.com"
    ))
    print(f"  [coins] Added {coin_id}")
    return True


def add_to_issues_table(conn: sqlite3.Connection, type_code: str, specs: dict) -> bool:
    """Add entry to the issues table for universal export."""
    cursor = conn.cursor()
    issue_id = f"MX-{type_code}-XXXX-MO"

    # Check if already exists
    cursor.execute("SELECT issue_id FROM issues WHERE issue_id = ?", (issue_id,))
    if cursor.fetchone():
        print(f"  [issues] Skipping {issue_id} - already exists")
        return False

    metal = "silver" if specs["composition"].endswith("Ag") else "platinum"
    series_id = f"{specs['series']}__No_Face_Value"

    # Build JSON fields matching existing entries
    specifications = json.dumps({
        "weight_grams": specs["weight_grams"],
        "diameter_mm": specs["diameter_mm"],
        "edge": "reeded",
        "composition": specs["composition"]
    })

    sides = json.dumps({
        "obverse": {"description": "Winged Victory"},
        "reverse": {"description": "Mexican coat of arms"}
    })

    cursor.execute("""
        INSERT INTO issues (
            issue_id, object_type, series_id,
            country_code, authority_name, monetary_system, currency_unit,
            face_value, unit_name, issue_year,
            specifications, sides,
            source_citation, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        issue_id,
        "coin",
        series_id,
        "MX",
        "Casa de Moneda de Mexico",
        "decimal",
        "peso",
        0.01,  # No face value
        "No Face Value",
        "XXXX",
        specifications,
        sides,
        "Casa de Moneda de Mexico",
        f"Random year {specs['weight_oz']} oz {metal} bullion"
    ))
    print(f"  [issues] Added {issue_id}")
    return True


def add_large_libertads(conn: sqlite3.Connection):
    """Add large Libertad coins to both coins and issues tables."""
    coins_added = 0
    issues_added = 0

    for type_code, specs in ALL_LIBERTADS.items():
        if add_to_coins_table(conn, type_code, specs):
            coins_added += 1
        if add_to_issues_table(conn, type_code, specs):
            issues_added += 1

    conn.commit()
    return coins_added, issues_added


def main():
    print("=" * 60)
    print("Adding Large Mexican Libertad Type Codes - Issue #83")
    print("=" * 60)

    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        return 1

    # Backup first
    backup_database()

    conn = sqlite3.connect(DB_PATH)

    try:
        print("\nAdding large Silver Libertad sizes...")
        print("  Type codes: MLSW (2oz), MLSF (5oz), MLSK (1kg)")

        print("\nAdding Platinum Libertad...")
        print("  Type code: MLPO (1oz)")

        print("\nProcessing...")
        coins_added, issues_added = add_large_libertads(conn)

        print(f"\nCoins table: {coins_added} added")
        print(f"Issues table: {issues_added} added")

        # Show summary of all Libertad entries
        cursor = conn.cursor()
        cursor.execute("""
            SELECT coin_id, denomination
            FROM coins
            WHERE coin_id LIKE 'MX-MLS%' OR coin_id LIKE 'MX-MLG%' OR coin_id LIKE 'MX-MLP%'
            ORDER BY coin_id
        """)

        print("\nAll Mexican Libertad type codes in database (coins table):")
        print("-" * 60)
        type_codes = set()
        for row in cursor.fetchall():
            parts = row[0].split('-')
            if len(parts) >= 2:
                type_codes.add(parts[1])

        for tc in sorted(type_codes):
            print(f"  {tc}")

        # Also show issues table count
        cursor.execute("""
            SELECT COUNT(*) FROM issues
            WHERE issue_id LIKE 'MX-MLS%' OR issue_id LIKE 'MX-MLG%' OR issue_id LIKE 'MX-MLP%'
        """)
        issues_count = cursor.fetchone()[0]
        print(f"\nTotal MX Libertad entries in issues table: {issues_count}")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
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
