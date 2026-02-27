#!/usr/bin/env python3
"""
Standardize bullion weight encoding to suffix-only convention.
Issue #137

Migrates from separate series-per-weight codes to base code + weight suffix:
- Phase 1: Libertad (MLSH→MLSO-12oz, MLSD→MLSO-110oz, etc.)
- Phase 2: US Eagles (AGEH→AGEO-12oz, AGEQ→AGEO-14oz, AGET→AGEO-110oz)
- Phase 3: Britannia (BGBT→BGBO-110oz)

Also fixes:
- Libertad type: coin → bullion
- Libertad denominations: product name → "No Face Value"
- Duplicate series: removes MLS1, MLG1
- Missing XXXX entries: adds MLSO, MLGO 1oz base entries
- Adds MLGO to series_registry (was missing)
- Updates variety_suffixes on base series
"""

import sqlite3
import json
import shutil
from datetime import datetime
from pathlib import Path

# === COIN_ID REMAPPING ===
# old_coin_id → new_coin_id
COIN_REMAPS = {
    # Phase 1: Libertad Silver
    "MX-MLSH-XXXX-MO": "MX-MLSO-XXXX-MO-12oz",
    "MX-MLSQ-XXXX-MO": "MX-MLSO-XXXX-MO-14oz",
    "MX-MLSD-XXXX-MO": "MX-MLSO-XXXX-MO-110oz",
    "MX-MLST-XXXX-MO": "MX-MLSO-XXXX-MO-120oz",
    "MX-MLSW-XXXX-MO": "MX-MLSO-XXXX-MO-2oz",
    "MX-MLSF-XXXX-MO": "MX-MLSO-XXXX-MO-5oz",
    "MX-MLSK-XXXX-MO": "MX-MLSO-XXXX-MO-1kg",
    # Phase 1: Libertad Gold
    "MX-MLGH-XXXX-MO": "MX-MLGO-XXXX-MO-12oz",
    "MX-MLGQ-XXXX-MO": "MX-MLGO-XXXX-MO-14oz",
    "MX-MLGD-XXXX-MO": "MX-MLGO-XXXX-MO-110oz",
    "MX-MLGT-XXXX-MO": "MX-MLGO-XXXX-MO-120oz",
    # Phase 2: US Gold Eagles
    "US-AGEH-XXXX-X": "US-AGEO-XXXX-X-12oz",
    "US-AGEQ-XXXX-X": "US-AGEO-XXXX-X-14oz",
    "US-AGET-XXXX-X": "US-AGEO-XXXX-X-110oz",
    # Phase 3: Britannia
    "GB-BGBT-XXXX-RM": "GB-BGBO-XXXX-RM-110oz",
}

# === SERIES TO DEPRECATE (delete from series_registry) ===
DEPRECATED_SERIES = [
    "AGEH", "AGEQ", "AGET",  # Eagle fractionals
    "BGBT",  # Britannia 1/10oz
    "MLSH", "MLSQ", "MLSD", "MLST", "MLSW", "MLSF", "MLSK",  # Libertad Silver
    "MLGH", "MLGQ", "MLGD", "MLGT",  # Libertad Gold
    "MLS1", "MLG1",  # Duplicates
]

# === VARIETY SUFFIXES UPDATES ===
VARIETY_SUFFIX_UPDATES = {
    "AGEO": ["12oz", "14oz", "110oz"],
    "MLSO": ["120oz", "110oz", "14oz", "12oz", "2oz", "5oz", "1kg"],
    "MLGO": ["120oz", "110oz", "14oz", "12oz"],
    "BGBO": ["110oz", "14oz", "12oz"],  # add 110oz to existing [14oz, 12oz]
}

# === TYPE FIXES (coin → bullion) ===
LIBERTAD_TYPE_FIX = ["MLSO", "MLPO"]  # Only series that will remain

# === DENOMINATION FIXES ===
DENOMINATION_FIXES = {
    "MLPO": "No Face Value",
    "MLSK": "No Face Value",  # Applied before deletion, to the coin entry
}

# === MISSING XXXX ENTRIES TO ADD ===
NEW_XXXX_ENTRIES = [
    {
        "coin_id": "MX-MLSO-XXXX-MO",
        "mint": "MO",
        "denomination": "No Face Value",
        "series": "Mexican Libertad Silver 1 oz",
        "composition": ".999 Ag",
        "weight_grams": 31.1035,
        "diameter_mm": 36.0,
        "edge": "Reeded",
        "designer": "Based on 1921 Centenario design",
        "obverse": "Winged Victory (Angel of Independence), Mexican coat of arms",
        "reverse": "National arms, eagle on cactus",
        "notes": "Random year bullion - 1 oz Silver Libertad. Valued by metal content.",
    },
    {
        "coin_id": "MX-MLGO-XXXX-MO",
        "mint": "MO",
        "denomination": "No Face Value",
        "series": "Mexican Libertad Gold 1 oz",
        "composition": ".999 Au",
        "weight_grams": 31.1035,
        "diameter_mm": 34.5,
        "edge": "Reeded",
        "designer": "Based on 1921 Centenario design",
        "obverse": "Winged Victory (Angel of Independence), Mexican coat of arms",
        "reverse": "National arms, eagle on cactus",
        "notes": "Random year bullion - 1 oz Gold Libertad. Valued by metal content.",
    },
]

# === NEW SERIES REGISTRY ENTRY ===
NEW_SERIES = [
    {
        "series_id": "mexican_libertad_gold_1oz",
        "series_name": "Mexican Libertad Gold (1 oz)",
        "series_abbreviation": "MLGO",
        "country_code": "MX",
        "denomination": "No Face Value",
        "start_year": 1981,
        "end_year": None,
        "defining_characteristics": "Bullion, .999 Au, Winged Victory design",
        "official_name": "Libertad de Oro",
        "type": "bullion",
        "aliases": json.dumps(["Gold Libertad", "Libertad Gold", "Mexican Gold Libertad", "Onza de Oro"]),
        "variety_suffixes": json.dumps(["120oz", "110oz", "14oz", "12oz"]),
        "series_group": "Libertad",
    },
]


def phase1_libertad(conn):
    """Fix Libertad: remap coins, fix types, fix denominations, add missing entries."""
    cursor = conn.cursor()
    print("=== PHASE 1: LIBERTAD ===")

    # 1a. Add MLGO to series_registry (missing)
    for s in NEW_SERIES:
        print(f"  Adding series: {s['series_abbreviation']}")
        cursor.execute("""
            INSERT OR IGNORE INTO series_registry (
                series_id, series_name, series_abbreviation, country_code,
                denomination, start_year, end_year, defining_characteristics,
                official_name, type, aliases, variety_suffixes, series_group
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["series_id"], s["series_name"], s["series_abbreviation"],
            s["country_code"], s["denomination"], s["start_year"], s["end_year"],
            s["defining_characteristics"], s["official_name"], s["type"],
            s["aliases"], s["variety_suffixes"], s["series_group"],
        ))

    # 1b. Fix MLSO type and update with variety_suffixes
    print("  Fixing MLSO: type → bullion, adding variety_suffixes")
    cursor.execute("""
        UPDATE series_registry SET
            type = 'bullion',
            series_name = 'Mexican Libertad Silver (1 oz)',
            official_name = 'Libertad de Plata',
            variety_suffixes = ?,
            series_group = 'Libertad'
        WHERE series_abbreviation = 'MLSO'
    """, (json.dumps(VARIETY_SUFFIX_UPDATES["MLSO"]),))

    # 1c. Fix MLPO type
    print("  Fixing MLPO: type → bullion")
    cursor.execute("""
        UPDATE series_registry SET
            type = 'bullion',
            denomination = 'No Face Value',
            series_name = 'Mexican Libertad Platinum (1 oz)',
            official_name = 'Libertad de Platino',
            series_group = 'Libertad'
        WHERE series_abbreviation = 'MLPO'
    """)

    # 1d. Add missing XXXX entries
    for entry in NEW_XXXX_ENTRIES:
        print(f"  Adding XXXX entry: {entry['coin_id']}")
        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description, notes, rarity,
                source_citation
            ) VALUES (?, 'XXXX', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'common', 'Official mint specifications')
        """, (
            entry["coin_id"], entry["mint"], entry["denomination"],
            entry["series"], entry["composition"], entry["weight_grams"],
            entry["diameter_mm"], entry["edge"], entry["designer"],
            entry["obverse"], entry["reverse"], entry["notes"],
        ))

    # 1e. Remap Libertad coin entries
    libertad_remaps = {k: v for k, v in COIN_REMAPS.items() if k.startswith("MX-")}
    for old_id, new_id in libertad_remaps.items():
        print(f"  Remapping: {old_id} → {new_id}")
        # Read the existing entry
        cursor.execute("SELECT * FROM coins WHERE coin_id = ?", (old_id,))
        row = cursor.fetchone()
        if not row:
            print(f"    WARNING: {old_id} not found, skipping")
            continue

        cols = [d[0] for d in cursor.description]
        data = dict(zip(cols, row))

        # Fix denomination if it's a product name
        if data["denomination"].startswith("Mexican Libertad"):
            data["denomination"] = "No Face Value"

        # Update series to base series name
        if "MLS" in old_id:
            data["series"] = "Mexican Libertad Silver (1 oz)"
        else:
            data["series"] = "Mexican Libertad Gold (1 oz)"

        # Insert new entry
        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description,
                business_strikes, proof_strikes, total_mintage,
                notes, rarity, source_citation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_id, data["year"], data["mint"], data["denomination"],
            data["series"], data["variety"], data["composition"],
            data["weight_grams"], data["diameter_mm"], data["edge"],
            data["designer"], data["obverse_description"],
            data["reverse_description"], data["business_strikes"],
            data["proof_strikes"], data["total_mintage"],
            data["notes"], data["rarity"], data["source_citation"],
        ))

        # Delete old entry
        cursor.execute("DELETE FROM coins WHERE coin_id = ?", (old_id,))

    conn.commit()
    print(f"  Phase 1 complete: {len(libertad_remaps)} Libertad entries remapped\n")


def phase2_eagles(conn):
    """Fix US Eagles: remap fractional XXXX entries to suffix format."""
    cursor = conn.cursor()
    print("=== PHASE 2: US EAGLES ===")

    eagle_remaps = {k: v for k, v in COIN_REMAPS.items() if k.startswith("US-")}
    for old_id, new_id in eagle_remaps.items():
        print(f"  Remapping: {old_id} → {new_id}")
        cursor.execute("SELECT * FROM coins WHERE coin_id = ?", (old_id,))
        row = cursor.fetchone()
        if not row:
            print(f"    WARNING: {old_id} not found, skipping")
            continue

        cols = [d[0] for d in cursor.description]
        data = dict(zip(cols, row))

        # Update series name to base
        data["series"] = "American Gold Eagle (1 oz)"

        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description,
                business_strikes, proof_strikes, total_mintage,
                notes, rarity, source_citation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_id, data["year"], data["mint"], data["denomination"],
            data["series"], data["variety"], data["composition"],
            data["weight_grams"], data["diameter_mm"], data["edge"],
            data["designer"], data["obverse_description"],
            data["reverse_description"], data["business_strikes"],
            data["proof_strikes"], data["total_mintage"],
            data["notes"], data["rarity"], data["source_citation"],
        ))

        cursor.execute("DELETE FROM coins WHERE coin_id = ?", (old_id,))

    # Update AGEO variety_suffixes
    print("  Updating AGEO variety_suffixes")
    cursor.execute("""
        UPDATE series_registry SET variety_suffixes = ?
        WHERE series_abbreviation = 'AGEO'
    """, (json.dumps(VARIETY_SUFFIX_UPDATES["AGEO"]),))

    conn.commit()
    print(f"  Phase 2 complete: {len(eagle_remaps)} Eagle entries remapped\n")


def phase3_britannia(conn):
    """Fix Britannia: remap BGBT to BGBO-110oz."""
    cursor = conn.cursor()
    print("=== PHASE 3: BRITANNIA ===")

    old_id = "GB-BGBT-XXXX-RM"
    new_id = "GB-BGBO-XXXX-RM-110oz"
    print(f"  Remapping: {old_id} → {new_id}")

    cursor.execute("SELECT * FROM coins WHERE coin_id = ?", (old_id,))
    row = cursor.fetchone()
    if row:
        cols = [d[0] for d in cursor.description]
        data = dict(zip(cols, row))
        data["series"] = "British Gold Britannia (1 oz)"

        cursor.execute("""
            INSERT OR IGNORE INTO coins (
                coin_id, year, mint, denomination, series, variety,
                composition, weight_grams, diameter_mm, edge, designer,
                obverse_description, reverse_description,
                business_strikes, proof_strikes, total_mintage,
                notes, rarity, source_citation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_id, data["year"], data["mint"], data["denomination"],
            data["series"], data["variety"], data["composition"],
            data["weight_grams"], data["diameter_mm"], data["edge"],
            data["designer"], data["obverse_description"],
            data["reverse_description"], data["business_strikes"],
            data["proof_strikes"], data["total_mintage"],
            data["notes"], data["rarity"], data["source_citation"],
        ))

        cursor.execute("DELETE FROM coins WHERE coin_id = ?", (old_id,))
    else:
        print(f"    WARNING: {old_id} not found")

    # Update BGBO variety_suffixes to include 110oz
    print("  Updating BGBO variety_suffixes (adding 110oz)")
    cursor.execute("""
        UPDATE series_registry SET variety_suffixes = ?
        WHERE series_abbreviation = 'BGBO'
    """, (json.dumps(VARIETY_SUFFIX_UPDATES["BGBO"]),))

    conn.commit()
    print("  Phase 3 complete\n")


def deprecate_old_series(conn):
    """Remove deprecated series codes from series_registry."""
    cursor = conn.cursor()
    print("=== DEPRECATING OLD SERIES ===")

    for code in DEPRECATED_SERIES:
        cursor.execute("SELECT series_abbreviation FROM series_registry WHERE series_abbreviation = ?", (code,))
        if cursor.fetchone():
            print(f"  Removing: {code}")
            cursor.execute("DELETE FROM series_registry WHERE series_abbreviation = ?", (code,))
        else:
            print(f"  Already gone: {code}")

    conn.commit()
    print(f"  Deprecated {len(DEPRECATED_SERIES)} series codes\n")


def verify(conn):
    """Verify migration results."""
    cursor = conn.cursor()
    print("=== VERIFICATION ===")

    # Check new coin entries exist
    new_ids = list(COIN_REMAPS.values()) + [e["coin_id"] for e in NEW_XXXX_ENTRIES]
    cursor.execute(
        f"SELECT coin_id FROM coins WHERE coin_id IN ({','.join('?' * len(new_ids))})",
        new_ids,
    )
    found = {row[0] for row in cursor.fetchall()}
    missing = set(new_ids) - found
    print(f"  New coin entries: {len(found)}/{len(new_ids)} found")
    if missing:
        print(f"  MISSING: {missing}")

    # Check old entries are gone
    old_ids = list(COIN_REMAPS.keys())
    cursor.execute(
        f"SELECT coin_id FROM coins WHERE coin_id IN ({','.join('?' * len(old_ids))})",
        old_ids,
    )
    leftover = {row[0] for row in cursor.fetchall()}
    print(f"  Old coin entries removed: {len(old_ids) - len(leftover)}/{len(old_ids)}")
    if leftover:
        print(f"  STILL PRESENT: {leftover}")

    # Check deprecated series are gone
    cursor.execute(
        f"SELECT series_abbreviation FROM series_registry WHERE series_abbreviation IN ({','.join('?' * len(DEPRECATED_SERIES))})",
        DEPRECATED_SERIES,
    )
    leftover_series = {row[0] for row in cursor.fetchall()}
    print(f"  Deprecated series removed: {len(DEPRECATED_SERIES) - len(leftover_series)}/{len(DEPRECATED_SERIES)}")
    if leftover_series:
        print(f"  STILL PRESENT: {leftover_series}")

    # Check base series have correct variety_suffixes
    for code, expected in VARIETY_SUFFIX_UPDATES.items():
        cursor.execute("SELECT variety_suffixes FROM series_registry WHERE series_abbreviation = ?", (code,))
        row = cursor.fetchone()
        if row and row[0]:
            actual = json.loads(row[0])
            status = "OK" if set(actual) == set(expected) else f"MISMATCH: {actual}"
            print(f"  {code} variety_suffixes: {status}")
        else:
            print(f"  {code} variety_suffixes: MISSING")

    # Check Libertad type fixed
    cursor.execute("SELECT series_abbreviation, type FROM series_registry WHERE series_abbreviation IN ('MLSO', 'MLGO', 'MLPO')")
    for row in cursor.fetchall():
        status = "OK" if row[1] == "bullion" else f"WRONG: {row[1]}"
        print(f"  {row[0]} type: {status}")

    return len(missing) == 0 and len(leftover) == 0 and len(leftover_series) == 0


def main():
    db_path = Path(__file__).parent.parent / "database" / "coins.db"

    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return 1

    # Backup
    backup_dir = Path(__file__).parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / f"coins_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}\n")

    conn = sqlite3.connect(db_path)
    try:
        phase1_libertad(conn)
        phase2_eagles(conn)
        phase3_britannia(conn)
        deprecate_old_series(conn)
        success = verify(conn)
        if not success:
            print("\nVerification FAILED!")
            return 1
        print("\nAll verifications passed!")
    finally:
        conn.close()

    print("\nNext step: python3 scripts/export_from_database.py")
    return 0


if __name__ == "__main__":
    exit(main())
