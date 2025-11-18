#!/usr/bin/env python3
"""
Migrate Engelhard Bullion from coins table to issues table (Universal Schema)

This script migrates the 72 Engelhard bullion bars from the legacy
coins table to the new universal issues table, making them accessible via
the front-end GitHub Pages site.

Usage:
    python scripts/migrate_engelhard_to_issues.py
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
    backup = backup_dir / f'coins_backup_engelhard_issues_{timestamp}.db'

    shutil.copy(source, backup)
    print(f"✅ Database backed up to {backup}")
    return backup


def transform_engelhard_to_issue(coin):
    """Transform an Engelhard coin record to universal issues format."""

    # Parse composition JSON
    composition = json.loads(coin['composition'])

    # Build series ID from the coin series name
    series_id = f"engelhard_{coin['series'].lower().replace(' ', '_').replace('(', '').replace(')', '').replace('.', '')}"

    # Build common names
    common_names = [
        f"Engelhard 1 oz Silver Bar",
        coin['series'],
        "Engelhard Bullion"
    ]

    # Build specifications
    specifications = {
        "weight_grams": coin['weight_grams'],
        "diameter_mm": coin['diameter_mm'],
        "edge": "plain",
        "composition": composition,
        "fineness": ".999"
    }

    # Build sides (obverse/reverse descriptions)
    sides = {
        "obverse": {
            "design": coin['obverse_description'] or 'Engelhard hallmark and specifications',
            "designer": "Engelhard Corporation",
            "elements": ["Engelhard hallmark", "Weight marking", "Fineness marking"]
        },
        "reverse": {
            "design": coin['reverse_description'] or 'Varies by variety',
            "designer": "Engelhard Corporation",
            "elements": ["Varies by type"]
        }
    }

    # Build mintage info (mostly unknown for Engelhard)
    mintage = {}
    if coin['business_strikes'] and coin['business_strikes'] > 0:
        mintage['business_strikes'] = coin['business_strikes']

    # Build varieties array (empty for now, specifics are in notes)
    varieties = []

    # Build distinguishing features
    distinguishing_features = [
        ".999 fine silver",
        "1 ounce silver content",
        "Engelhard Corporation production",
        "Collectible variety",
        coin['series']
    ]

    # Build keywords
    keywords = [
        "engelhard",
        "silver",
        "bullion",
        "bar",
        "1oz",
        ".999"
    ]

    # Build authority period (Engelhard era)
    authority_period = {
        "entity_type": "private_mint",
        "company": {
            "name": "Engelhard Corporation",
            "period": "1902-2006"
        }
    }

    # Create issue record (matching issues table schema)
    issue = {
        'issue_id': coin['coin_id'],
        'object_type': 'coin',
        'series_id': series_id,
        'series_group': "Engelhard Silver Bullion Bars",
        'series_group_years': '1960s-1980s',
        'country_code': 'US',
        'authority_name': 'Engelhard Corporation',
        'monetary_system': 'bullion',
        'currency_unit': 'none',
        'face_value': 0.0,  # No face value
        'unit_name': 'No Face Value',
        'common_names': json.dumps(common_names),
        'system_fraction': 'Bullion bar',
        'issue_year': 'XXXX',  # Random year bullion
        'mint_id': 'X',  # Unspecified
        'date_range_start': None,
        'date_range_end': None,
        'authority_period': json.dumps(authority_period),
        'specifications': json.dumps(specifications),
        'sides': json.dumps(sides),
        'mintage': json.dumps(mintage) if mintage else None,
        'rarity': coin['rarity'],
        'varieties': json.dumps(varieties),
        'source_citation': coin['source_citation'],
        'notes': coin['notes'],
        'metadata': json.dumps({
            "distinguishing_features": distinguishing_features,
            "keywords": keywords,
            "variety_name": coin['series']
        })
    }

    return issue


def migrate_engelhard():
    """Migrate all Engelhard bullion to issues table."""
    print("\n🚀 Migrating Engelhard Bullion to Issues Table")
    print("=" * 50)

    # Backup database first
    backup_database()

    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Get all Engelhard coins (new format: US-EN01 through US-EN72)
        cursor.execute("""
            SELECT *
            FROM coins
            WHERE coin_id LIKE 'US-EN__-XXXX-X'
            ORDER BY coin_id
        """)

        engelhards = cursor.fetchall()
        print(f"\n📊 Found {len(engelhards)} Engelhard bullion bars to migrate")

        if len(engelhards) == 0:
            print("⚠️  No Engelhard bars found. Exiting.")
            return

        # Transform and insert each Engelhard
        inserted = 0
        skipped = 0

        for coin in engelhards:
            # Check if already exists in issues
            cursor.execute("SELECT issue_id FROM issues WHERE issue_id = ?", (coin['coin_id'],))
            if cursor.fetchone():
                print(f"   ⏭  Skipped {coin['coin_id']} (already exists)")
                skipped += 1
                continue

            # Transform to issue format
            issue = transform_engelhard_to_issue(coin)

            # Insert into issues table
            cursor.execute("""
                INSERT INTO issues (
                    issue_id, object_type, series_id, series_group, series_group_years,
                    country_code, authority_name, monetary_system, currency_unit,
                    face_value, unit_name, common_names, system_fraction,
                    issue_year, mint_id, date_range_start, date_range_end,
                    authority_period, specifications, sides, mintage, rarity,
                    varieties, source_citation, notes, metadata
                ) VALUES (
                    :issue_id, :object_type, :series_id, :series_group, :series_group_years,
                    :country_code, :authority_name, :monetary_system, :currency_unit,
                    :face_value, :unit_name, :common_names, :system_fraction,
                    :issue_year, :mint_id, :date_range_start, :date_range_end,
                    :authority_period, :specifications, :sides, :mintage, :rarity,
                    :varieties, :source_citation, :notes, :metadata
                )
            """, issue)

            print(f"   ✅ Migrated {issue['issue_id']} - {json.loads(issue['common_names'])[1]}")
            inserted += 1

        # Commit changes
        conn.commit()

        print(f"\n✅ Migration Complete!")
        print(f"   📝 Inserted: {inserted} Engelhard bars")
        print(f"   ⏭  Skipped: {skipped} (already existed)")

    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()

    return True


if __name__ == "__main__":
    success = migrate_engelhard()
    exit(0 if success else 1)
