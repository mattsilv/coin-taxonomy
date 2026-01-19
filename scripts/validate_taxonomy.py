#!/usr/bin/env python3
"""
Taxonomy Validation Tests

Issue #85: Add taxonomy documentation and validation tests
Updated for Issue #113: Uses shared TaxonomyValidator module

Validates:
- All series codes are unique 4-letter uppercase
- No duplicate codes across coin types
- Coin IDs match expected format
- Series codes match coin_id patterns
"""

import json
import sqlite3
import sys
from pathlib import Path
from collections import defaultdict

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Use the shared canonical validator (Issue #113)
from scripts.utils.taxonomy_validator import TaxonomyValidator

# Module-level validator instance
_validator = TaxonomyValidator()


def validate_series_code_format(code: str) -> tuple[bool, str]:
    """Validate series code using shared TaxonomyValidator.

    Returns:
        tuple: (is_valid, error_message)
    """
    errors, _ = _validator.validate_series_code(code)
    if errors:
        return False, errors[0].message
    return True, ""


def validate_coin_id_format(coin_id: str) -> tuple[bool, str]:
    """Validate coin ID using shared TaxonomyValidator.

    Returns:
        tuple: (is_valid, error_message)
    """
    errors, _ = _validator.validate_coin_id(coin_id)
    if errors:
        return False, errors[0].message
    return True, ""


def check_unique_codes_in_file(filepath: Path) -> tuple[list[str], list[str]]:
    """Check for unique series codes in a JSON file."""
    errors = []
    codes_found = []

    try:
        with open(filepath) as f:
            data = json.load(f)

        if "series" not in data:
            return codes_found, []

        seen_codes = set()
        for series in data["series"]:
            code = series.get("series_code")
            if code:
                codes_found.append(code)
                if code in seen_codes:
                    errors.append(f"Duplicate code '{code}' in {filepath.name}")
                seen_codes.add(code)

                # Validate format
                valid, msg = validate_series_code_format(code)
                if not valid:
                    errors.append(f"{filepath.name}: {msg}")

    except json.JSONDecodeError as e:
        errors.append(f"JSON parse error in {filepath}: {e}")
    except Exception as e:
        errors.append(f"Error reading {filepath}: {e}")

    return codes_found, errors


def check_coin_ids_in_file(filepath: Path) -> list[str]:
    """Validate all coin_ids in a JSON file."""
    errors = []

    try:
        with open(filepath) as f:
            data = json.load(f)

        if "series" not in data:
            return errors

        for series in data["series"]:
            series_code = series.get("series_code", "UNKNOWN")
            for coin in series.get("coins", []):
                coin_id = coin.get("coin_id", "")
                valid, msg = validate_coin_id_format(coin_id)
                if not valid:
                    errors.append(f"{filepath.name}: {msg}")

                # Verify coin_id contains the series code
                if series_code != "UNKNOWN" and f"-{series_code}-" not in coin_id:
                    errors.append(
                        f"{filepath.name}: coin_id '{coin_id}' doesn't contain series_code '{series_code}'"
                    )

    except Exception as e:
        errors.append(f"Error reading {filepath}: {e}")

    return errors


def validate_database(db_path: str) -> list[str]:
    """Validate coin_ids in database."""
    errors = []

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check all coin_ids
        cursor.execute("SELECT coin_id FROM coins")
        for (coin_id,) in cursor.fetchall():
            valid, msg = validate_coin_id_format(coin_id)
            if not valid:
                errors.append(f"Database: {msg}")

        conn.close()
    except Exception as e:
        errors.append(f"Database error: {e}")

    return errors


def main():
    print("🔍 Validating Taxonomy...")
    print("=" * 60)

    all_errors = []
    all_codes = defaultdict(list)  # code -> [files containing it]

    # Find all JSON files with coin data
    data_dir = Path("data/us/coins")
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        return 1

    json_files = list(data_dir.glob("*.json"))
    print(f"\n📁 Checking {len(json_files)} JSON files...")

    for filepath in sorted(json_files):
        codes, errors = check_unique_codes_in_file(filepath)
        all_errors.extend(errors)

        for code in codes:
            all_codes[code].append(filepath.name)

        coin_errors = check_coin_ids_in_file(filepath)
        all_errors.extend(coin_errors)

        if not errors and not coin_errors:
            print(f"   ✅ {filepath.name}")
        else:
            print(f"   ❌ {filepath.name} ({len(errors) + len(coin_errors)} errors)")

    # Check for duplicate codes across files
    print("\n📊 Checking for cross-file duplicate codes...")
    duplicate_count = 0
    for code, files in sorted(all_codes.items()):
        if len(files) > 1:
            all_errors.append(
                f"Code '{code}' appears in multiple files: {', '.join(files)}"
            )
            duplicate_count += 1

    if duplicate_count == 0:
        print("   ✅ No cross-file duplicates found")
    else:
        print(f"   ⚠️  {duplicate_count} codes appear in multiple files")

    # Validate database (canonical path: database/coins.db)
    print("\n🗄️  Validating database...")
    db_path = "database/coins.db"  # Canonical DB path per SOURCE_OF_TRUTH.md
    if Path(db_path).exists():
        db_errors = validate_database(db_path)
        if not db_errors:
            print(f"   ✅ {db_path}")
        else:
            print(f"   ❌ {db_path} ({len(db_errors)} errors)")
            all_errors.extend(db_errors)
    else:
        print(f"   ⚠️  Database not found at {db_path}")

    # Summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print(f"   Total series codes: {len(all_codes)}")
    print(f"   Files checked: {len(json_files)}")

    if all_errors:
        print(f"\n❌ FAILED: {len(all_errors)} errors found")
        print("\nErrors:")
        for error in all_errors[:20]:  # Show first 20 errors
            print(f"   - {error}")
        if len(all_errors) > 20:
            print(f"   ... and {len(all_errors) - 20} more errors")
        return 1
    else:
        print("\n✅ PASSED: All validations successful")
        return 0


if __name__ == "__main__":
    sys.exit(main())
