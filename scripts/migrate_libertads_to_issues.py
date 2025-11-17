#!/usr/bin/env python3
"""
Migrate Mexican Libertads from coins table to issues table (Universal Schema)

This script migrates the 105 Mexican Libertad bullion coins from the legacy
coins table to the new universal issues table, making them accessible via
the front-end GitHub Pages site.

Usage:
    python scripts/migrate_libertads_to_issues.py
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import shutil


def backup_database():
    """Create backup before migration."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)

    source = Path('database/coins.db')
    backup = backup_dir / f'coins_backup_libertad_issues_{timestamp}.db'

    shutil.copy(source, backup)
    print(f"✅ Database backed up to {backup}")
    return backup


def transform_libertad_to_issue(coin):
    """Transform a Libertad coin record to universal issues format."""

    # Parse composition JSON
    composition = json.loads(coin['composition'])

    # Determine metal and series
    is_gold = 'gold' in composition
    metal = 'Gold' if is_gold else 'Silver'

    # Determine fineness for notes
    if is_gold:
        if 'copper' in composition:
            fineness = '.900'
        else:
            fineness = '.999'
    else:
        fineness = '.999'

    # Build series ID (e.g., mexican_libertad_gold_1oz)
    series_id = f"mexican_libertad_{metal.lower()}_1oz"

    # Build common names
    common_names = [
        f"Mexican {metal} Libertad",
        f"Libertad 1 oz {metal}",
        f"Onza Libertad {metal}"
    ]

    if coin['variety']:
        common_names.append(f"Libertad {coin['variety']}")

    # Build specifications
    specifications = {
        "weight_grams": coin['weight_grams'],
        "diameter_mm": coin['diameter_mm'],
        "edge": coin['edge'] or 'Reeded',
        "thickness_mm": 3.0 if not is_gold else 2.5,
        "composition": composition,
        "fineness": fineness
    }

    # Build sides (obverse/reverse descriptions)
    sides = {
        "obverse": {
            "design": coin['obverse_description'] or 'Mexican coat of arms',
            "designer": coin['designer'] or "Based on 1921 Centenario design",
            "elements": ["Mexican coat of arms", "historical versions"]
        },
        "reverse": {
            "design": coin['reverse_description'] or 'Winged Victoria',
            "designer": coin['designer'] or "Based on 1921 Centenario design",
            "elements": ["Angel of Independence", "Volcanoes Popocatépetl and Iztaccihuatl"]
        }
    }

    # Build mintage info
    mintage = {}
    if coin['business_strikes'] and coin['business_strikes'] > 0:
        mintage['business_strikes'] = coin['business_strikes']
    if coin['proof_strikes'] and coin['proof_strikes'] > 0:
        mintage['proof_strikes'] = coin['proof_strikes']
    if coin['total_mintage'] and coin['total_mintage'] > 0:
        mintage['total_mintage'] = coin['total_mintage']

    # Build varieties array
    varieties = []
    if coin['variety']:
        varieties.append({
            "variety_id": coin['coin_id'],
            "name": coin['variety'],
            "description": f"{coin['variety']} finish",
            "estimated_mintage": coin['total_mintage'] or 0
        })

    # Build distinguishing features
    distinguishing_features = [
        f"{fineness} fine {metal.lower()}",
        f"1 ounce {metal.lower()} content",
        "MO mint mark (Mexico City)",
        "No face value (valued by metal content)"
    ]

    if coin['variety']:
        distinguishing_features.append(f"{coin['variety']} finish")

    # Build keywords
    keywords = [
        "mexican",
        "libertad",
        metal.lower(),
        "bullion",
        "onza",
        f"{coin['year']}",
        "angel",
        "victoria"
    ]

    if coin['variety']:
        keywords.append(coin['variety'].lower())

    # Create issue record (matching issues table schema)
    issue = {
        'issue_id': coin['coin_id'],
        'object_type': 'coin',
        'series_id': series_id,
        'series_group': f"Mexican Libertad {metal} 1 oz",
        'series_group_years': '1981-present' if is_gold else '1982-present',
        'country_code': 'MX',
        'authority_name': 'La Casa de Moneda de México',
        'monetary_system': 'decimal',
        'currency_unit': 'peso',
        'face_value': 0.0,  # No face value
        'unit_name': 'No Face Value',
        'common_names': json.dumps(common_names),
        'system_fraction': 'Bullion coin',
        'issue_year': int(coin['year']),
        'mint_id': coin['mint'],
        'date_range_start': int(coin['year']),
        'date_range_end': int(coin['year']),
        'authority_period': json.dumps({
            "entity_type": "federal_republic",
            "guarantor": "Banco de México"
        }),
        'specifications': json.dumps(specifications),
        'sides': json.dumps(sides),
        'mintage': json.dumps(mintage),
        'rarity': coin['rarity'] or 'common',
        'varieties': json.dumps(varieties),
        'source_citation': coin['source_citation'],
        'notes': coin['notes'],
        'metadata': json.dumps({
            "collection_significance": "Modern bullion program",
            "historical_context": "Mexico's official bullion coin since early 1980s",
            "distinguishing_features": distinguishing_features,
            "identification_keywords": keywords,
            "fineness": fineness,
            "variety_type": coin['variety']
        })
    }

    return issue


def migrate_libertads_to_issues(conn):
    """Migrate all Libertads from coins table to issues table."""
    cursor = conn.cursor()

    # Fetch all Mexican Libertads from coins table
    cursor.execute("""
        SELECT * FROM coins
        WHERE coin_id LIKE 'MX-%'
        ORDER BY year, coin_id
    """)

    columns = [description[0] for description in cursor.description]
    libertads = []
    for row in cursor.fetchall():
        coin = dict(zip(columns, row))
        libertads.append(coin)

    print(f"📊 Found {len(libertads)} Libertads in coins table")

    # Transform and insert into issues table
    issues_added = 0
    for coin in libertads:
        try:
            issue = transform_libertad_to_issue(coin)

            # Insert into issues table
            cursor.execute("""
                INSERT OR REPLACE INTO issues (
                    issue_id, object_type, series_id, series_group, series_group_years,
                    country_code, authority_name, monetary_system, currency_unit,
                    face_value, unit_name, common_names, system_fraction,
                    issue_year, mint_id, date_range_start, date_range_end,
                    authority_period, specifications, sides, mintage, rarity,
                    varieties, source_citation, notes, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                issue['issue_id'], issue['object_type'], issue['series_id'],
                issue['series_group'], issue['series_group_years'],
                issue['country_code'], issue['authority_name'], issue['monetary_system'],
                issue['currency_unit'], issue['face_value'], issue['unit_name'],
                issue['common_names'], issue['system_fraction'], issue['issue_year'],
                issue['mint_id'], issue['date_range_start'], issue['date_range_end'],
                issue['authority_period'], issue['specifications'], issue['sides'],
                issue['mintage'], issue['rarity'], issue['varieties'],
                issue['source_citation'], issue['notes'], issue['metadata']
            ))

            issues_added += 1
            print(f"  ✅ Added {issue['issue_id']}")

        except Exception as e:
            print(f"  ❌ Failed to add {coin['coin_id']}: {e}")
            raise

    return issues_added


def verify_migration(conn):
    """Verify Libertads were added to issues table."""
    cursor = conn.cursor()

    print("\n📊 Verification Summary:")

    # Check total count
    cursor.execute("""
        SELECT COUNT(*) FROM issues
        WHERE country_code = 'MX'
    """)
    total_count = cursor.fetchone()[0]
    print(f"  Total MX issues: {total_count}")

    # Check by series
    cursor.execute("""
        SELECT series_id, COUNT(*) as count
        FROM issues
        WHERE country_code = 'MX'
        GROUP BY series_id
        ORDER BY series_id
    """)

    print("  By series:")
    for row in cursor.fetchall():
        series_id, count = row
        print(f"    {series_id}: {count}")

    # Check year range
    cursor.execute("""
        SELECT MIN(issue_year), MAX(issue_year)
        FROM issues
        WHERE country_code = 'MX'
    """)

    min_year, max_year = cursor.fetchone()
    print(f"  Year range: {min_year}-{max_year}")


def main():
    """Execute Libertads to issues migration."""
    print("🚀 Migrating Mexican Libertads to Universal Issues Table")
    print("=" * 70)

    # Backup database
    backup_path = backup_database()

    try:
        # Connect to database
        conn = sqlite3.connect('database/coins.db')

        # Migrate Libertads
        issues_added = migrate_libertads_to_issues(conn)

        # Commit changes
        conn.commit()

        # Verify results
        verify_migration(conn)

        conn.close()

        print(f"\n✨ Migration Complete! Added {issues_added} issues to universal table")
        print("Next steps:")
        print("  1. Run export: uv run python scripts/export_db_v1_1.py")
        print("  2. Update front-end to include Mexico")
        print("  3. Test GitHub Pages site")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print(f"Restore from backup: {backup_path}")
        raise


if __name__ == "__main__":
    main()
