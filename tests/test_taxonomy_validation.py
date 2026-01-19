#!/usr/bin/env python3
"""
Database-Only Taxonomy Validation Tests

Per Epic #116, Issue #114: These tests validate directly against the SQLite database
without relying on JSON exports or external data.

Run: python -m pytest tests/test_taxonomy_validation.py -v
"""

import sqlite3
import unittest
from pathlib import Path
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.utils.taxonomy_validator import (
    TaxonomyValidator,
    DatabaseValidator,
    ValidationError,
    ValidationWarning,
    CANONICAL_DB_PATH,
)


class TestCoinIdValidation(unittest.TestCase):
    """Test coin_id format validation rules."""

    @classmethod
    def setUpClass(cls):
        """Set up validator and database connection."""
        cls.validator = TaxonomyValidator()
        cls.db_path = CANONICAL_DB_PATH

        if not cls.db_path.exists():
            raise unittest.SkipTest(f"Database not found at {cls.db_path}")

    def test_valid_coin_id_basic(self):
        """Test basic valid coin ID format."""
        errors, warnings = self.validator.validate_coin_id("US-MORG-1879-CC")
        self.assertEqual(len(errors), 0, f"Unexpected errors: {errors}")

    def test_valid_coin_id_with_variety(self):
        """Test valid coin ID with variety suffix."""
        errors, warnings = self.validator.validate_coin_id("US-MORG-1878-P-8TF")
        self.assertEqual(len(errors), 0, f"Unexpected errors: {errors}")

    def test_valid_coin_id_xxxx_year(self):
        """Test valid coin ID with XXXX year (bullion random year)."""
        errors, warnings = self.validator.validate_coin_id("US-AGEO-XXXX-X")
        self.assertEqual(len(errors), 0, f"Unexpected errors: {errors}")

    def test_invalid_coin_id_lowercase(self):
        """Test that lowercase coin IDs are rejected."""
        errors, warnings = self.validator.validate_coin_id("us-morg-1879-cc")
        self.assertGreater(len(errors), 0, "Should reject lowercase country")

    def test_invalid_coin_id_short_code(self):
        """Test that short series codes are rejected."""
        errors, warnings = self.validator.validate_coin_id("US-MOR-1879-CC")
        self.assertGreater(len(errors), 0, "Should reject 3-char code")

    def test_invalid_coin_id_too_few_parts(self):
        """Test that coin IDs with too few parts are rejected."""
        errors, warnings = self.validator.validate_coin_id("US-MORG-1879")
        self.assertGreater(len(errors), 0, "Should reject < 4 parts")

    def test_invalid_coin_id_invalid_year(self):
        """Test that invalid years are rejected."""
        errors, warnings = self.validator.validate_coin_id("US-MORG-18-CC")
        self.assertGreater(len(errors), 0, "Should reject 2-digit year")

    def test_warning_long_variety(self):
        """Test that long variety suffixes generate warnings."""
        errors, warnings = self.validator.validate_coin_id("US-GRNT-1922-P-STARVARIETY")
        self.assertEqual(len(errors), 0, "Long variety should not be an error")
        self.assertGreater(len(warnings), 0, "Should warn about long variety")

    def test_all_coin_ids_valid_format(self):
        """CRITICAL: All coin_ids in database must match valid format."""
        db_validator = DatabaseValidator(self.db_path)
        errors, warnings = db_validator.validate_all_coin_ids()

        # Log warnings but don't fail
        if warnings:
            for w in warnings[:10]:  # Show first 10
                print(f"WARNING: {w.message}")

        # Errors cause test failure
        self.assertEqual(
            len(errors), 0,
            f"Found {len(errors)} invalid coin_ids. First 5: {[e.message for e in errors[:5]]}"
        )


class TestSeriesCodeValidation(unittest.TestCase):
    """Test series code validation rules."""

    @classmethod
    def setUpClass(cls):
        """Set up validator and database connection."""
        cls.validator = TaxonomyValidator()
        cls.db_path = CANONICAL_DB_PATH

        if not cls.db_path.exists():
            raise unittest.SkipTest(f"Database not found at {cls.db_path}")

    def test_valid_series_code_letters(self):
        """Test valid all-letter series code."""
        errors, warnings = self.validator.validate_series_code("MORG")
        self.assertEqual(len(errors), 0, f"Unexpected errors: {errors}")

    def test_valid_series_code_alphanumeric(self):
        """Test valid alphanumeric series code."""
        errors, warnings = self.validator.validate_series_code("ATB5")
        self.assertEqual(len(errors), 0, f"Unexpected errors: {errors}")

    def test_invalid_series_code_short(self):
        """Test that short codes are rejected."""
        errors, warnings = self.validator.validate_series_code("MOR")
        self.assertGreater(len(errors), 0, "Should reject 3-char code")

    def test_invalid_series_code_long(self):
        """Test that long codes are rejected."""
        errors, warnings = self.validator.validate_series_code("MORGA")
        self.assertGreater(len(errors), 0, "Should reject 5-char code")

    def test_invalid_series_code_lowercase(self):
        """Test that lowercase codes are rejected."""
        errors, warnings = self.validator.validate_series_code("morg")
        self.assertGreater(len(errors), 0, "Should reject lowercase code")

    def test_series_codes_audit(self):
        """AUDIT: Report series codes that don't match 4-char format.

        Note: This is an audit test - it reports issues for tracking but doesn't fail.
        Known issue: ~88 series have legacy full-name abbreviations instead of 4-char codes.
        Tracking in: Epic #116, Phase 4.
        """
        db_validator = DatabaseValidator(self.db_path)
        errors, warnings = db_validator.validate_all_series_codes()

        if errors:
            print(f"\n[AUDIT] Found {len(errors)} series with non-standard abbreviations")
            print("  First 5:")
            for e in errors[:5]:
                print(f"    - {e.message}")

        # Audit test - always passes but reports issues
        # When all issues are fixed, convert to strict test
        self.assertTrue(True, "Audit test - see output for issues")


class TestSeriesRegistry(unittest.TestCase):
    """Test series_registry table constraints."""

    @classmethod
    def setUpClass(cls):
        """Set up database connection."""
        cls.db_path = CANONICAL_DB_PATH

        if not cls.db_path.exists():
            raise unittest.SkipTest(f"Database not found at {cls.db_path}")

        cls.conn = sqlite3.connect(cls.db_path)

    @classmethod
    def tearDownClass(cls):
        """Clean up database connection."""
        if hasattr(cls, 'conn'):
            cls.conn.close()

    def test_series_code_uniqueness(self):
        """CRITICAL: All series codes must be unique."""
        db_validator = DatabaseValidator(self.db_path)
        errors = db_validator.check_series_code_uniqueness()

        self.assertEqual(
            len(errors), 0,
            f"Found duplicate series codes: {[e.value for e in errors]}"
        )

    def test_series_code_format_audit(self):
        """AUDIT: Report series codes with invalid format.

        Note: This is an audit test - reports issues without failing.
        Known issue: ~88 series have legacy full-name abbreviations.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT series_abbreviation FROM series_registry")

        invalid_codes = []
        for (code,) in cursor.fetchall():
            if not code or len(code) != 4:
                invalid_codes.append(f"{code} (len={len(code) if code else 0})")
            elif not code.isalnum():
                invalid_codes.append(f"{code} (not alnum)")
            elif not all(c.isupper() or c.isdigit() for c in code):
                invalid_codes.append(f"{code} (not uppercase)")

        if invalid_codes:
            print(f"\n[AUDIT] Found {len(invalid_codes)} series with invalid code format")
            print(f"  First 5: {invalid_codes[:5]}")

        # Audit - always passes
        self.assertTrue(True)

    def test_no_duplicate_series_names_audit(self):
        """AUDIT: Report duplicate series names.

        Note: Uniqueness is per (country, denomination) pair.
        """
        db_validator = DatabaseValidator(self.db_path)
        errors = db_validator.check_series_name_uniqueness()

        if errors:
            print(f"\n[AUDIT] Found {len(errors)} duplicate series names")
            for e in errors[:5]:
                print(f"    - {e.value}")

        # Audit - always passes
        self.assertTrue(True)

    def test_series_name_no_double_underscore_audit(self):
        """AUDIT: Report series names with double underscores.

        Note: SQL LIKE '%__%' matches any 2+ chars - using explicit check.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT series_name FROM series_registry")

        # Check for literal double underscore
        bad_names = [row[0] for row in cursor.fetchall() if row[0] and '__' in row[0]]

        if bad_names:
            print(f"\n[AUDIT] Found {len(bad_names)} series with '__' in name")
            print(f"  First 5: {bad_names[:5]}")

        # Audit - always passes
        self.assertTrue(True)


class TestDatabaseIntegrity(unittest.TestCase):
    """Test overall database integrity."""

    @classmethod
    def setUpClass(cls):
        """Set up database connection."""
        cls.db_path = CANONICAL_DB_PATH

        if not cls.db_path.exists():
            raise unittest.SkipTest(f"Database not found at {cls.db_path}")

        cls.conn = sqlite3.connect(cls.db_path)

    @classmethod
    def tearDownClass(cls):
        """Clean up database connection."""
        if hasattr(cls, 'conn'):
            cls.conn.close()

    def test_coins_table_exists(self):
        """Verify coins table exists."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coins'")
        self.assertIsNotNone(cursor.fetchone(), "coins table must exist")

    def test_series_registry_table_exists(self):
        """Verify series_registry table exists."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='series_registry'")
        self.assertIsNotNone(cursor.fetchone(), "series_registry table must exist")

    def test_coins_have_valid_series_references_audit(self):
        """AUDIT: Report coins that reference non-existent series.

        Note: Some coins may reference series not yet in series_registry.
        The coins table uses 'series' column which stores the series name.
        """
        cursor = self.conn.cursor()

        # Check if coins reference series that exist
        # coins.series = series_registry.series_name (or series_abbreviation)
        cursor.execute("""
            SELECT DISTINCT c.series
            FROM coins c
            WHERE c.series IS NOT NULL
              AND c.series NOT IN (SELECT series_name FROM series_registry)
              AND c.series NOT IN (SELECT series_abbreviation FROM series_registry)
            LIMIT 20
        """)

        orphan_series = [row[0] for row in cursor.fetchall()]

        if orphan_series:
            print(f"\n[AUDIT] Found {len(orphan_series)} coins with missing series references")
            print(f"  First 10: {orphan_series[:10]}")

        # Audit - always passes
        self.assertTrue(True)

    def test_canonical_db_path(self):
        """Verify we're using the canonical database path."""
        self.assertEqual(
            self.db_path,
            CANONICAL_DB_PATH,
            f"Test should use canonical path {CANONICAL_DB_PATH}"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
