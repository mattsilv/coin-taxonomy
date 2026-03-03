#!/usr/bin/env python3
"""
Import vintage Engelhard and Johnson Matthey bullion into coin-taxonomy.

Reads ~1,265 products from the Nucleus47 coindex.db source database and inserts
them into database/coins.db with proper series_registry entries and coin IDs.

Usage:
    uv run python scripts/import_vintage_bullion.py
    uv run python scripts/import_vintage_bullion.py --dry-run
"""

import argparse
import json
import re
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

# Source database path
SOURCE_DB = Path.home() / "Desktop" / "Nucleus47 Master" / "Nucleus47 Entity" / "Ventures" / "Coindex" / "coindex_db" / "coindex.db"

# Target database path
TARGET_DB = Path(__file__).parent.parent / "database" / "coins.db"

# Brand+category -> series abbreviation mapping
SERIES_MAP = {
    ("engelhard", "AG-1oz"): "EA1S",
    ("engelhard", "AG-5oz"): "EA5S",
    ("engelhard", "AG-10oz"): "EATS",
    ("engelhard", "AG-20oz-25oz"): "EA2S",
    ("engelhard", "AG-50oz"): "EA5L",
    ("engelhard", "AG-100oz"): "EAHS",
    ("engelhard", "AG-Half-Kilo-Kilo"): "EAKS",
    ("engelhard", "AG-Odd-Size"): "EAOS",
    ("engelhard", "AG-Rounds"): "EARS",
    ("engelhard", "AU-Rounds"): "EARG",
    ("engelhard", "PD-All-Classes"): "EAPD",
    ("engelhard", "PT-All-Classes"): "EAPT",
    ("johnson_matthey", "AG-1oz"): "JM1S",
    ("johnson_matthey", "AG-5oz"): "JM5S",
    ("johnson_matthey", "AG-10oz"): "JMTS",
    ("johnson_matthey", "AG-20oz-25oz"): "JM2S",
    ("johnson_matthey", "AG-50oz"): "JM5L",
    ("johnson_matthey", "AG-100oz"): "JMHS",
    ("johnson_matthey", "AG-HalfKilo-Kilo"): "JMKS",
    ("johnson_matthey", "AG-Odd-Size"): "JMOS",
}

# Series registry metadata
SERIES_REGISTRY = {
    "EA1S": {"name": "Engelhard Silver Bar (1 oz)", "series_id": "engelhard_silver_1oz"},
    "EA5S": {"name": "Engelhard Silver Bar (5 oz)", "series_id": "engelhard_silver_5oz"},
    "EATS": {"name": "Engelhard Silver Bar (10 oz)", "series_id": "engelhard_silver_10oz"},
    "EA2S": {"name": "Engelhard Silver Bar (20-25 oz)", "series_id": "engelhard_silver_20oz"},
    "EA5L": {"name": "Engelhard Silver Bar (50 oz)", "series_id": "engelhard_silver_50oz"},
    "EAHS": {"name": "Engelhard Silver Bar (100 oz)", "series_id": "engelhard_silver_100oz"},
    "EAKS": {"name": "Engelhard Silver Bar (Half Kilo - Kilo)", "series_id": "engelhard_silver_kilo"},
    "EAOS": {"name": "Engelhard Silver Bar (Odd Size)", "series_id": "engelhard_silver_odd"},
    "EARS": {"name": "Engelhard Silver Round", "series_id": "engelhard_silver_rounds"},
    "EARG": {"name": "Engelhard Gold Round", "series_id": "engelhard_gold_rounds"},
    "EAPD": {"name": "Engelhard Palladium", "series_id": "engelhard_palladium"},
    "EAPT": {"name": "Engelhard Platinum", "series_id": "engelhard_platinum"},
    "JM1S": {"name": "Johnson Matthey Silver Bar (1 oz)", "series_id": "jm_silver_1oz"},
    "JM5S": {"name": "Johnson Matthey Silver Bar (5 oz)", "series_id": "jm_silver_5oz"},
    "JMTS": {"name": "Johnson Matthey Silver Bar (10 oz)", "series_id": "jm_silver_10oz"},
    "JM2S": {"name": "Johnson Matthey Silver Bar (20-25 oz)", "series_id": "jm_silver_20oz"},
    "JM5L": {"name": "Johnson Matthey Silver Bar (50 oz)", "series_id": "jm_silver_50oz"},
    "JMHS": {"name": "Johnson Matthey Silver Bar (100 oz)", "series_id": "jm_silver_100oz"},
    "JMKS": {"name": "Johnson Matthey Silver Bar (Half Kilo - Kilo)", "series_id": "jm_silver_kilo"},
    "JMOS": {"name": "Johnson Matthey Silver Bar (Odd Size)", "series_id": "jm_silver_odd"},
}

# Composition by category prefix
COMPOSITION_MAP = {
    "AG": json.dumps({"silver": 0.999}),
    "AU": json.dumps({"gold": 0.9999}),
    "PD": json.dumps({"palladium": 0.9995}),
    "PT": json.dumps({"platinum": 0.9995}),
}

# Weight in grams by category slug
WEIGHT_MAP = {
    "AG-1oz": 31.103,
    "AG-5oz": 155.517,
    "AG-10oz": 311.035,
    "AG-20oz-25oz": 622.069,
    "AG-50oz": 1555.174,
    "AG-100oz": 3110.348,
    "AG-Half-Kilo-Kilo": 500.0,
    "AG-HalfKilo-Kilo": 500.0,
    "AG-Odd-Size": None,
    "AG-Rounds": 31.103,
    "AU-Rounds": 31.103,
    "PD-All-Classes": None,
    "PT-All-Classes": None,
}

# Old series abbreviations to delete
OLD_SERIES = [
    "EN10", "ENG", "EBO", "EIC(", "ENG1", "ENG2", "ENG3", "ENG4", "ENG5",
    "ENG6", "ENG7", "ENG8", "ENG9", "ENG10", "EPO", "JOH",
]


def get_composition(category_slug):
    """Get composition JSON from category slug."""
    prefix = category_slug.split("-")[0]
    return COMPOSITION_MAP.get(prefix, COMPOSITION_MAP["AG"])


def get_weight(category_slug):
    """Get weight in grams from category slug."""
    return WEIGHT_MAP.get(category_slug)


def get_source_citation(brand_slug):
    """Get source citation based on brand."""
    if brand_slug == "engelhard":
        return "Engelhard Definitive Pages"
    return "Johnson Matthey Definitive Pages"


def parse_mintage(text):
    """Parse estimated mintage text to integer, return None if unparseable."""
    if not text or text.strip() in ("", "N/A", "Unknown", "?"):
        return None
    clean = text.strip().replace("<", "").replace(">", "").replace(",", "").replace("~", "")
    # Extract first number
    match = re.search(r"(\d+)", clean)
    if match:
        return int(match.group(1))
    return None


def derive_rarity(mintage_text):
    """Derive rarity from estimated mintage text."""
    mintage = parse_mintage(mintage_text)
    if mintage is None:
        return None
    if mintage < 100:
        return "key"
    if mintage < 1000:
        return "scarce"
    if mintage < 10000:
        return "semi-key"
    return "common"


def make_suffix(variety_id, seq_counter):
    """
    Generate variety suffix from variety_id.

    If variety_id starts with 'EI' -> clean to alphanumeric uppercase.
    Otherwise -> sequential V001, V002, etc.
    """
    if variety_id and variety_id not in ("N/A", ""):
        vid = variety_id.strip()
        if vid.upper().startswith("EI"):
            # Clean: remove dashes, spaces, keep alphanumeric, uppercase
            cleaned = re.sub(r"[^A-Za-z0-9]", "", vid).upper()
            if cleaned:
                return cleaned
    # Sequential fallback
    return f"V{seq_counter:03d}"


def build_notes(commentary, serial_numbers, mintage):
    """Build notes field from source columns."""
    parts = []
    if commentary and commentary.strip():
        parts.append(f"Commentary: {commentary.strip()}")
    if serial_numbers and serial_numbers.strip():
        parts.append(f"Sample Serials: {serial_numbers.strip()}")
    if mintage and mintage.strip():
        parts.append(f"Estimated Mintage: {mintage.strip()}")
    return "\n".join(parts) if parts else None


def read_source_products(source_db_path):
    """Read all products from source database, joined with brand and category."""
    conn = sqlite3.connect(source_db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            p.id,
            p.row_number,
            p.variety_id,
            p.variety_name,
            p.obverse_description,
            p.reverse_description,
            p.commentary,
            p.sample_serial_numbers,
            p.icr_estimated_mintage,
            b.slug AS brand_slug,
            c.slug AS category_slug
        FROM products p
        JOIN brands b ON p.brand_id = b.id
        JOIN categories c ON p.category_id = c.id
        ORDER BY b.slug, c.slug, p.row_number
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Import vintage Engelhard and Johnson Matthey bullion into coin-taxonomy"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing to database",
    )
    args = parser.parse_args()

    if not SOURCE_DB.exists():
        print(f"Source database not found: {SOURCE_DB}")
        return 1

    if not TARGET_DB.exists():
        print(f"Target database not found: {TARGET_DB}")
        return 1

    # Read source data
    products = read_source_products(SOURCE_DB)
    print(f"Read {len(products)} products from source database")

    if not args.dry_run:
        # Backup target database
        backup_dir = Path(__file__).parent.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / f"coins_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(TARGET_DB, backup_path)
        print(f"Backup created: {backup_path}")

    conn = sqlite3.connect(TARGET_DB)
    cursor = conn.cursor()

    try:
        # --- Step 1: Delete old entries ---
        old_coin_count = cursor.execute(
            "SELECT COUNT(*) FROM coins WHERE coin_id LIKE 'US-EN%' OR coin_id LIKE 'US-JMTB%'"
        ).fetchone()[0]
        print(f"\nDeleting {old_coin_count} old coin entries (US-EN*, US-JMTB*)...")

        if not args.dry_run:
            cursor.execute("DELETE FROM coins WHERE coin_id LIKE 'US-EN%' OR coin_id LIKE 'US-JMTB%'")

        placeholders = ",".join("?" * len(OLD_SERIES))
        old_series_count = cursor.execute(
            f"SELECT COUNT(*) FROM series_registry WHERE series_abbreviation IN ({placeholders})",
            OLD_SERIES,
        ).fetchone()[0]
        print(f"Deleting {old_series_count} old series_registry entries...")

        if not args.dry_run:
            cursor.execute(
                f"DELETE FROM series_registry WHERE series_abbreviation IN ({placeholders})",
                OLD_SERIES,
            )

        # --- Step 2: Insert new series_registry entries ---
        print(f"\nInserting {len(SERIES_REGISTRY)} series_registry entries...")
        for abbrev, meta in SERIES_REGISTRY.items():
            brand = "Engelhard" if abbrev.startswith("EA") else "Johnson Matthey"
            if not args.dry_run:
                cursor.execute("""
                    INSERT OR REPLACE INTO series_registry (
                        series_id, series_name, series_abbreviation, country_code,
                        denomination, start_year, type
                    ) VALUES (?, ?, ?, 'US', 'No Face Value', 1960, 'bullion')
                """, (
                    meta["series_id"],
                    meta["name"],
                    abbrev,
                ))
            print(f"  {abbrev}: {meta['name']}")

        # --- Step 3: Insert coin entries ---
        print(f"\nInserting coin entries...")
        # Track sequential counters and used suffixes per series
        seq_counters = {}
        used_suffixes = {}  # series_abbrev -> set of used suffixes
        inserted = 0
        skipped = 0

        for product in products:
            brand_slug = product["brand_slug"]
            category_slug = product["category_slug"]
            key = (brand_slug, category_slug)

            series_abbrev = SERIES_MAP.get(key)
            if series_abbrev is None:
                print(f"  WARNING: No series mapping for {key}, skipping product {product['id']}")
                skipped += 1
                continue

            # Track sequential counter per series
            if series_abbrev not in seq_counters:
                seq_counters[series_abbrev] = 0
                used_suffixes[series_abbrev] = set()
            seq_counters[series_abbrev] += 1

            suffix = make_suffix(product["variety_id"], seq_counters[series_abbrev])
            # Handle duplicate suffixes (e.g., two products with EI-1A in same series)
            if suffix in used_suffixes[series_abbrev]:
                base = suffix
                dedup = 2
                while suffix in used_suffixes[series_abbrev]:
                    suffix = f"{base}{dedup}"
                    dedup += 1
            used_suffixes[series_abbrev].add(suffix)
            coin_id = f"US-{series_abbrev}-XXXX-X-{suffix}"

            composition = get_composition(category_slug)
            weight = get_weight(category_slug)
            citation = get_source_citation(brand_slug)
            rarity = derive_rarity(product["icr_estimated_mintage"])
            notes = build_notes(
                product["commentary"],
                product["sample_serial_numbers"],
                product["icr_estimated_mintage"],
            )

            variety_name = product["variety_name"] or ""

            if not args.dry_run:
                try:
                    cursor.execute("""
                        INSERT INTO coins (
                            coin_id, year, mint, denomination, series, variety,
                            composition, weight_grams,
                            obverse_description, reverse_description,
                            notes, source_citation, rarity,
                            proof_strikes, business_strikes, total_mintage
                        ) VALUES (?, 'XXXX', 'X', 'No Face Value', ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL, NULL)
                    """, (
                        coin_id,
                        variety_name,
                        suffix,
                        composition,
                        weight,
                        product["obverse_description"],
                        product["reverse_description"],
                        notes,
                        citation,
                        rarity,
                    ))
                    inserted += 1
                except sqlite3.IntegrityError as e:
                    print(f"  ERROR inserting {coin_id}: {e}")
                    skipped += 1
                    continue
            else:
                inserted += 1

            if inserted <= 5 or inserted % 200 == 0:
                print(f"  [{inserted}] {coin_id} = {variety_name[:60]}")

        if not args.dry_run:
            conn.commit()

        # --- Step 4: Verification ---
        print(f"\n{'DRY RUN ' if args.dry_run else ''}Summary:")
        print(f"  Old entries deleted: {old_coin_count} coins, {old_series_count} series")
        print(f"  New series inserted: {len(SERIES_REGISTRY)}")
        print(f"  New coins inserted: {inserted}")
        print(f"  Skipped: {skipped}")

        if not args.dry_run:
            # Verify counts
            new_count = cursor.execute(
                "SELECT COUNT(*) FROM coins WHERE coin_id LIKE 'US-EA%' OR coin_id LIKE 'US-JM%'"
            ).fetchone()[0]
            new_series = cursor.execute(
                f"SELECT COUNT(*) FROM series_registry WHERE series_abbreviation IN ({','.join('?' * len(SERIES_REGISTRY))})",
                list(SERIES_REGISTRY.keys()),
            ).fetchone()[0]
            print(f"\nVerification:")
            print(f"  Coins in DB (US-EA*, US-JM*): {new_count}")
            print(f"  Series in registry: {new_series}/{len(SERIES_REGISTRY)}")

            # Show per-series breakdown
            print("\nPer-series breakdown:")
            for abbrev in sorted(SERIES_REGISTRY.keys()):
                count = cursor.execute(
                    "SELECT COUNT(*) FROM coins WHERE coin_id LIKE ?",
                    (f"US-{abbrev}-%",),
                ).fetchone()[0]
                print(f"  {abbrev}: {count} coins")

    finally:
        conn.close()

    if not args.dry_run:
        print("\nNext step: uv run python scripts/export_from_database.py")

    return 0


if __name__ == "__main__":
    exit(main())
