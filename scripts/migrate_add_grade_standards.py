#!/usr/bin/env python3
"""
Database Migration: Add Grade Standards Table

Creates a grade_standards table in the database to store canonical grade
hierarchy and parsing rules. This enables:
- Multi-grade parsing (e.g., "XF/AU" → take lower grade)
- Grade comparison and sorting
- RAW-{grade} classification for uncertified coins
- Alias normalization (EF ↔ XF)

Data Source: data/references/grades_unified.json

Export Target: data/universal/grade_standards.json (generated via export_from_database.py)

See: GitHub Issue #64

Usage:
    uv run python scripts/migrate_add_grade_standards.py
    uv run python scripts/migrate_add_grade_standards.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from pathlib import Path
import shutil

class GradeStandardsMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None
        self.grades_source = 'data/references/grades_unified.json'

    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_pre_grade_standards_{timestamp}.db"

        if os.path.exists(self.db_path):
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")

    def load_grades_data(self):
        """Load grade data from grades_unified.json."""
        with open(self.grades_source, 'r') as f:
            return json.load(f)

    def create_grade_standards_table(self, conn, dry_run=False):
        """Create the grade_standards table."""
        cursor = conn.cursor()

        if dry_run:
            print("\nDRY RUN: Would create grade_standards table with schema:")
            print("""
  - grade_id: Primary key (e.g., 'MS-65')
  - grade_name: Full name (e.g., 'Mint State (MS-65)')
  - abbreviation: Canonical format (e.g., 'MS-65')
  - numeric_value: Sheldon scale position (1-70)
  - category: Circulated, About Uncirculated, Uncirculated
  - subcategory: Specific classification
  - description: Grade description
  - sheldon_scale_position: Position on Sheldon 70-point scale
  - market_threshold: Boolean - significant price break point
  - market_relevance: low, moderate, high, very_high
  - common_in_practice: Boolean - commonly used in the market
  - strike_types: JSON array of applicable strike types
  - alternate_notations: JSON array of accepted formats
  - sheldon_range_min: Minimum Sheldon range
  - sheldon_range_max: Maximum Sheldon range
  - aliases: JSON object mapping alternate codes
  - modifiers_allowed: JSON array of valid modifiers (for proof grades)
            """)
            return

        print("\nCreating grade_standards table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grade_standards (
                grade_id TEXT PRIMARY KEY,
                grade_name TEXT NOT NULL,
                abbreviation TEXT NOT NULL UNIQUE,
                numeric_value INTEGER NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                description TEXT,
                sheldon_scale_position INTEGER NOT NULL,
                market_threshold BOOLEAN DEFAULT 0,
                market_relevance TEXT DEFAULT 'moderate',
                common_in_practice BOOLEAN DEFAULT 1,
                strike_types JSON,
                alternate_notations JSON,
                sheldon_range_min INTEGER,
                sheldon_range_max INTEGER,
                aliases JSON,
                modifiers_allowed JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CHECK (market_relevance IN ('low', 'moderate', 'high', 'very_high'))
            )
        ''')
        print("✓ Created grade_standards table")

        # Create indices for common lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_grade_numeric
            ON grade_standards(numeric_value)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_grade_category
            ON grade_standards(category)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_grade_market_threshold
            ON grade_standards(market_threshold)
        ''')
        print("✓ Created indices")

    def determine_market_relevance(self, grade_data):
        """Determine market relevance rating based on grade characteristics."""
        numeric = grade_data['numeric_value']
        market_threshold = grade_data.get('market_threshold', False)
        common = grade_data.get('common_in_practice', False)

        # Very high relevance: Market thresholds + commonly used
        if market_threshold and common:
            if numeric >= 65:  # MS-65+, PR-65+
                return 'very_high'
            elif numeric >= 58:  # AU-58+
                return 'high'

        # High relevance: Commonly used grades
        if common:
            if 40 <= numeric < 65:  # XF-40 through MS-64
                return 'high'
            elif 20 <= numeric < 40:  # VF-20 through XF-45
                return 'moderate'

        # Low relevance: Uncommon grades
        if not common:
            return 'low'

        # Default: moderate
        return 'moderate'

    def determine_sheldon_range(self, grade_data):
        """Determine Sheldon range for grade groupings."""
        abbr = grade_data['abbreviation']
        numeric = grade_data['numeric_value']

        # Define range mappings
        range_map = {
            'P-1': (1, 1),
            'FR-2': (2, 2),
            'AG-3': (3, 3),
            'G-4': (4, 6),
            'G-6': (4, 6),
            'VG-8': (8, 10),
            'VG-10': (8, 10),
            'F-12': (12, 15),
            'F-15': (12, 15),
            'VF-20': (20, 35),
            'VF-25': (20, 35),
            'VF-30': (20, 35),
            'VF-35': (20, 35),
            'XF-40': (40, 45),
            'XF-45': (40, 45),
            'AU-50': (50, 58),
            'AU-53': (50, 58),
            'AU-55': (50, 58),
            'AU-58': (50, 58),
        }

        # Check if we have a specific range mapping
        if abbr in range_map:
            return range_map[abbr]

        # For MS/PR/SP grades, range is just the numeric value
        if abbr.startswith(('MS-', 'PR-', 'SP-', 'PF-')):
            return (numeric, numeric)

        # Default: same as numeric value
        return (numeric, numeric)

    def build_alias_map(self, grade_data):
        """Build alias mappings for the grade."""
        aliases = {}
        abbr = grade_data['abbreviation']

        # XF/EF aliasing
        if abbr.startswith('XF-'):
            ef_variant = abbr.replace('XF-', 'EF-')
            aliases['EF'] = 'XF'
            aliases[ef_variant] = abbr
            aliases[ef_variant.replace('-', '')] = abbr
            aliases[ef_variant.replace('-', ' ')] = abbr

        # PR/PF aliasing for proof grades
        if abbr.startswith('PR-'):
            pf_variant = abbr.replace('PR-', 'PF-')
            aliases['PF'] = 'PR'
            aliases[pf_variant] = abbr
            aliases[pf_variant.replace('-', '')] = abbr
            aliases[pf_variant.replace('-', ' ')] = abbr

        return aliases if aliases else None

    def populate_grade_standards(self, conn, dry_run=False):
        """Populate grade_standards table from grades_unified.json."""
        cursor = conn.cursor()

        # Load source data
        print("\nLoading grade data from grades_unified.json...")
        grades_data = self.load_grades_data()
        grades = grades_data['grades']

        if dry_run:
            print(f"DRY RUN: Would insert {len(grades)} grade records")
            # Show a few examples
            for i, grade in enumerate(grades[:3]):
                print(f"\n  Example {i+1}:")
                print(f"    Grade: {grade['abbreviation']}")
                print(f"    Category: {grade['category']}")
                print(f"    Market Relevance: {self.determine_market_relevance(grade)}")
            return

        print(f"Populating grade_standards with {len(grades)} grades...")

        inserted_count = 0
        for grade in grades:
            # Prepare data
            grade_id = grade['abbreviation']
            sheldon_range = self.determine_sheldon_range(grade)
            market_relevance = self.determine_market_relevance(grade)
            aliases = self.build_alias_map(grade)

            # Insert grade record
            cursor.execute('''
                INSERT OR REPLACE INTO grade_standards (
                    grade_id,
                    grade_name,
                    abbreviation,
                    numeric_value,
                    category,
                    subcategory,
                    description,
                    sheldon_scale_position,
                    market_threshold,
                    market_relevance,
                    common_in_practice,
                    strike_types,
                    alternate_notations,
                    sheldon_range_min,
                    sheldon_range_max,
                    aliases,
                    modifiers_allowed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                grade_id,
                grade['grade'],
                grade['abbreviation'],
                grade['numeric_value'],
                grade['category'],
                grade['subcategory'],
                grade.get('description'),
                grade['sheldon_scale_position'],
                1 if grade.get('market_threshold', False) else 0,
                market_relevance,
                1 if grade.get('common_in_practice', True) else 0,
                json.dumps(grade.get('strike_types', [])),
                json.dumps(grade.get('alternate_notations', [])),
                sheldon_range[0],
                sheldon_range[1],
                json.dumps(aliases) if aliases else None,
                json.dumps(grade.get('modifiers_allowed')) if grade.get('modifiers_allowed') else None
            ))
            inserted_count += 1

        print(f"✓ Inserted {inserted_count} grade records")

        # Verify count
        cursor.execute('SELECT COUNT(*) FROM grade_standards')
        final_count = cursor.fetchone()[0]
        print(f"✓ Final grade_standards table: {final_count} rows")

        return final_count

    def create_parsing_rules_table(self, conn, dry_run=False):
        """Create table for grade parsing rules and patterns."""
        cursor = conn.cursor()

        if dry_run:
            print("\nDRY RUN: Would create grade_parsing_rules table")
            return

        print("\nCreating grade_parsing_rules table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grade_parsing_rules (
                rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_type TEXT NOT NULL,
                rule_name TEXT NOT NULL,
                rule_value JSON NOT NULL,
                description TEXT,
                priority INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CHECK (rule_type IN ('separator', 'strategy', 'pattern', 'alias'))
            )
        ''')
        print("✓ Created grade_parsing_rules table")

        # Insert default parsing rules
        rules = [
            ('separator', 'multi_grade_separators', ["/", "-", " - ", " to ", " or "],
             'Separators used to split multi-grade expressions like "XF/AU"', 1),
            ('strategy', 'multi_grade_strategy', 'conservative',
             'Strategy for multi-grade handling: take lower (conservative) grade', 1),
            ('pattern', 'raw_grade_prefix', 'RAW-',
             'Prefix pattern for uncertified coins (e.g., RAW-XF-45)', 1),
            ('pattern', 'grade_extraction_basic', r'^([A-Z]{1,2})-?(\d{1,2})$',
             'Basic grade pattern: MS-65, XF40, etc.', 2),
            ('pattern', 'grade_extraction_with_desc', r'((?:MS|PR|PF|SP|XF|EF|AU|VF|F|VG|G|AG|FR|P)-?\d{1,2})',
             'Extract grade from descriptive text', 2),
        ]

        for rule_type, rule_name, rule_value, description, priority in rules:
            cursor.execute('''
                INSERT INTO grade_parsing_rules
                (rule_type, rule_name, rule_value, description, priority)
                VALUES (?, ?, ?, ?, ?)
            ''', (rule_type, rule_name, json.dumps(rule_value), description, priority))

        print(f"✓ Inserted {len(rules)} parsing rules")

    def run(self, dry_run=False):
        """Execute the migration."""
        print("=== Grade Standards Database Migration ===\n")
        print("Purpose: Add canonical grade hierarchy and parsing rules to database")
        print("Source: data/references/grades_unified.json")
        print("Export: data/universal/grade_standards.json (via export_from_database.py)\n")

        if not dry_run:
            self.create_backup()

        # Verify source data exists
        if not os.path.exists(self.grades_source):
            print(f"✗ Source file not found: {self.grades_source}")
            return False

        conn = sqlite3.connect(self.db_path)

        try:
            # Create tables
            self.create_grade_standards_table(conn, dry_run)
            self.create_parsing_rules_table(conn, dry_run)

            # Populate data
            if not dry_run:
                grade_count = self.populate_grade_standards(conn, dry_run)
                conn.commit()

                print(f"\n✓ Migration completed successfully")
                print(f"✓ Backup: {self.backup_path}")
                print(f"✓ Grades loaded: {grade_count}")
                print("\nNext steps:")
                print("  1. Update export_from_database.py to export grade_standards.json")
                print("  2. Run: uv run python scripts/export_from_database.py")
                print("  3. Create data/schema/grade_standards.schema.json")
                print("  4. Update validate.py to validate grade_standards.json")
                print("  5. Commit changes - Issue #64")
            else:
                print("\n✓ Dry run completed (no changes made)")

        except Exception as e:
            if not dry_run:
                conn.rollback()
            print(f"\n✗ Migration failed: {e}")
            raise
        finally:
            conn.close()

def main():
    parser = argparse.ArgumentParser(
        description='Add grade standards table to database (Issue #64)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying'
    )

    args = parser.parse_args()

    migration = GradeStandardsMigration()

    try:
        migration.run(dry_run=args.dry_run)
        return 0
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
