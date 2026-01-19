#!/usr/bin/env python3
"""
Canonical Taxonomy Validation Module

Consolidates all validation rules for coin-taxonomy per Epic #116.
This is the SINGLE SOURCE OF TRUTH for validation logic.

Usage:
    from scripts.utils.taxonomy_validator import TaxonomyValidator

    validator = TaxonomyValidator()
    errors, warnings = validator.validate_coin_id("US-MORG-1879-CC")
"""

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# Canonical database path (per SOURCE_OF_TRUTH.md)
CANONICAL_DB_PATH = Path("database/coins.db")


@dataclass
class ValidationResult:
    """Result of a validation check."""
    valid: bool
    message: str = ""


@dataclass
class ValidationError:
    """An error that must be fixed (test failure)."""
    field: str
    message: str
    value: str = ""


@dataclass
class ValidationWarning:
    """A warning that should be reviewed but doesn't fail tests."""
    field: str
    message: str
    value: str = ""


class TaxonomyValidator:
    """
    Canonical validator for coin taxonomy data.

    Rules are categorized as:
    - Errors: MUST be fixed (cause test failures)
    - Warnings: SHOULD be reviewed (logged but tests pass)
    """

    # Regex patterns for validation
    COUNTRY_PATTERN = re.compile(r"^[A-Z]{2,3}$")
    SERIES_CODE_PATTERN = re.compile(r"^[A-Z0-9]{4}$")
    YEAR_PATTERN = re.compile(r"^(\d{4}|XXXX)$")
    MINT_PATTERN = re.compile(r"^[A-Z]{1,2}$")
    VARIETY_PATTERN = re.compile(r"^[A-Za-z0-9]{1,20}$")

    def validate_coin_id(self, coin_id: str) -> tuple[list[ValidationError], list[ValidationWarning]]:
        """
        Validate coin ID format: COUNTRY-CODE-YEAR-MINT[-VARIETY]

        Returns:
            tuple: (errors, warnings)
        """
        errors = []
        warnings = []

        if not coin_id:
            errors.append(ValidationError("coin_id", "Empty coin_id", ""))
            return errors, warnings

        parts = coin_id.split("-")

        if len(parts) < 4:
            errors.append(ValidationError(
                "coin_id",
                f"Must have at least 4 parts (COUNTRY-CODE-YEAR-MINT)",
                coin_id
            ))
            return errors, warnings

        if len(parts) > 5:
            errors.append(ValidationError(
                "coin_id",
                f"Must have at most 5 parts (COUNTRY-CODE-YEAR-MINT[-VARIETY])",
                coin_id
            ))
            return errors, warnings

        country, code, year, mint = parts[:4]
        variety = parts[4] if len(parts) == 5 else None

        # Validate country (ERROR)
        if not self.COUNTRY_PATTERN.match(country):
            errors.append(ValidationError(
                "country",
                f"Must be 2-3 uppercase letters",
                country
            ))

        # Validate series code (ERROR)
        if not self.SERIES_CODE_PATTERN.match(code):
            errors.append(ValidationError(
                "series_code",
                f"Must be 4 uppercase alphanumeric characters",
                code
            ))

        # Validate year (ERROR)
        if not self.YEAR_PATTERN.match(year):
            errors.append(ValidationError(
                "year",
                f"Must be 4 digits or 'XXXX'",
                year
            ))

        # Validate mint (ERROR)
        if not self.MINT_PATTERN.match(mint):
            errors.append(ValidationError(
                "mint",
                f"Must be 1-2 uppercase letters",
                mint
            ))

        # Validate variety if present
        if variety:
            if not self.VARIETY_PATTERN.match(variety):
                errors.append(ValidationError(
                    "variety",
                    f"Must be 1-20 alphanumeric characters",
                    variety
                ))

            # Warning for long or mixed-case variety (per plan)
            if len(variety) > 4:
                warnings.append(ValidationWarning(
                    "variety",
                    f"Variety suffix >4 chars - consider shorter code",
                    variety
                ))

            if variety != variety.upper() and variety != variety.lower():
                warnings.append(ValidationWarning(
                    "variety",
                    f"Mixed case variety suffix - prefer all uppercase",
                    variety
                ))

        return errors, warnings

    def validate_series_code(self, code: str) -> tuple[list[ValidationError], list[ValidationWarning]]:
        """
        Validate series code format.

        Returns:
            tuple: (errors, warnings)
        """
        errors = []
        warnings = []

        if not code:
            errors.append(ValidationError("series_code", "Empty series code", ""))
            return errors, warnings

        if len(code) != 4:
            errors.append(ValidationError(
                "series_code",
                f"Must be exactly 4 characters",
                code
            ))

        if not code.isalnum():
            errors.append(ValidationError(
                "series_code",
                f"Must be alphanumeric only",
                code
            ))

        if not all(c.isupper() or c.isdigit() for c in code):
            errors.append(ValidationError(
                "series_code",
                f"Must be uppercase letters and digits only",
                code
            ))

        return errors, warnings

    def validate_series_name(
        self,
        name: str,
        country: Optional[str] = None,
        denomination: Optional[str] = None
    ) -> tuple[list[ValidationError], list[ValidationWarning]]:
        """
        Validate series name format.

        Returns:
            tuple: (errors, warnings)
        """
        errors = []
        warnings = []

        if not name:
            errors.append(ValidationError("series_name", "Empty series name", ""))
            return errors, warnings

        # Check for double underscore (ERROR)
        if "__" in name:
            errors.append(ValidationError(
                "series_name",
                f"Must not contain double underscores",
                name
            ))

        return errors, warnings


class DatabaseValidator:
    """
    Validates taxonomy data directly from the SQLite database.

    This is the DB-only validation approach per Issue #114.
    """

    def __init__(self, db_path: Path = CANONICAL_DB_PATH):
        self.db_path = db_path
        self.validator = TaxonomyValidator()

    def validate_all_coin_ids(self) -> tuple[list[ValidationError], list[ValidationWarning]]:
        """
        Validate all coin_ids in the coins table.

        Returns:
            tuple: (errors, warnings)
        """
        all_errors = []
        all_warnings = []

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT coin_id FROM coins")
        for (coin_id,) in cursor.fetchall():
            errors, warnings = self.validator.validate_coin_id(coin_id)
            for e in errors:
                e.message = f"[{coin_id}] {e.message}"
            for w in warnings:
                w.message = f"[{coin_id}] {w.message}"
            all_errors.extend(errors)
            all_warnings.extend(warnings)

        conn.close()
        return all_errors, all_warnings

    def validate_all_series_codes(self) -> tuple[list[ValidationError], list[ValidationWarning]]:
        """
        Validate all series codes in series_registry.

        Returns:
            tuple: (errors, warnings)
        """
        all_errors = []
        all_warnings = []

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT series_abbreviation, series_name FROM series_registry")
        for (code, name) in cursor.fetchall():
            # Validate code format
            errors, warnings = self.validator.validate_series_code(code)
            for e in errors:
                e.message = f"[{code}] {e.message}"
            for w in warnings:
                w.message = f"[{code}] {w.message}"
            all_errors.extend(errors)
            all_warnings.extend(warnings)

            # Validate series name
            name_errors, name_warnings = self.validator.validate_series_name(name)
            for e in name_errors:
                e.message = f"[{code}] series_name: {e.message}"
            for w in name_warnings:
                w.message = f"[{code}] series_name: {w.message}"
            all_errors.extend(name_errors)
            all_warnings.extend(name_warnings)

        conn.close()
        return all_errors, all_warnings

    def check_series_code_uniqueness(self) -> list[ValidationError]:
        """
        Check that all series codes are unique.

        Returns:
            list: Errors for duplicate codes
        """
        errors = []

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT series_abbreviation, COUNT(*) as cnt
            FROM series_registry
            GROUP BY series_abbreviation
            HAVING cnt > 1
        """)

        for (code, count) in cursor.fetchall():
            errors.append(ValidationError(
                "series_code",
                f"Duplicate series code found {count} times",
                code
            ))

        conn.close()
        return errors

    def check_series_name_uniqueness(self) -> list[ValidationError]:
        """
        Check that series names are unique within (country, denomination) pairs.

        Returns:
            list: Errors for duplicate names
        """
        errors = []

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT series_name, country_code, denomination, COUNT(*) as cnt
            FROM series_registry
            GROUP BY series_name, country_code, denomination
            HAVING cnt > 1
        """)

        for (name, country, denom, count) in cursor.fetchall():
            errors.append(ValidationError(
                "series_name",
                f"Duplicate series name for {country}/{denom}: found {count} times",
                name
            ))

        conn.close()
        return errors


def validate_database(db_path: Path = CANONICAL_DB_PATH) -> tuple[list[ValidationError], list[ValidationWarning]]:
    """
    Convenience function to run all database validations.

    Returns:
        tuple: (all_errors, all_warnings)
    """
    db_validator = DatabaseValidator(db_path)

    all_errors = []
    all_warnings = []

    # Validate coin IDs
    errors, warnings = db_validator.validate_all_coin_ids()
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # Validate series codes
    errors, warnings = db_validator.validate_all_series_codes()
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # Check uniqueness constraints
    all_errors.extend(db_validator.check_series_code_uniqueness())
    all_errors.extend(db_validator.check_series_name_uniqueness())

    return all_errors, all_warnings


if __name__ == "__main__":
    # Quick test
    validator = TaxonomyValidator()

    test_cases = [
        "US-MORG-1879-CC",      # Valid
        "US-MORG-1879-CC-VAM",  # Valid with variety
        "US-MORG-1879-CC-VeryLongVarietyName",  # Warning: long variety
        "us-morg-1879-cc",      # Error: lowercase
        "US-MOR-1879-CC",       # Error: 3-char code
    ]

    print("Testing TaxonomyValidator:")
    for coin_id in test_cases:
        errors, warnings = validator.validate_coin_id(coin_id)
        status = "ERROR" if errors else ("WARNING" if warnings else "OK")
        print(f"  {coin_id}: {status}")
        for e in errors:
            print(f"    - Error: {e.message}")
        for w in warnings:
            print(f"    - Warning: {w.message}")
