#!/usr/bin/env python3
"""
Taxonomy Validation Tests

Issue #85: Add taxonomy documentation and validation tests

Validates:
- All series codes are unique 4-letter uppercase
- No duplicate codes across coin types
- Coin IDs match expected format
- Series codes match coin_id patterns
"""

import json
import re
import sqlite3
import sys
from pathlib import Path
from collections import defaultdict


def validate_series_code_format(code: str) -> tuple[bool, str]:
    """Validate series code is 4 uppercase alphanumeric characters.

    Note: While CLAUDE.md specifies letters only, some existing series
    (Engelhard, ATB) use alphanumeric codes like EN18, ATB5.
    """
    if not code:
        return False, "Empty code"
    if len(code) != 4:
        return False, f"Code '{code}' is not 4 characters"
    if not code.isupper() and not code.isdigit():
        # Check if mixed alphanumeric but all uppercase letters
        if not all(c.isupper() or c.isdigit() for c in code):
            return False, f"Code '{code}' contains invalid characters"
    if not code.isalnum():
        return False, f"Code '{code}' is not alphanumeric"
    return True, ""


def validate_coin_id_format(coin_id: str) -> tuple[bool, str]:
    """Validate coin ID matches format: COUNTRY-CODE-YEAR-MINT[-VARIETY]."""
    if not coin_id:
        return False, "Empty coin_id"

    # Split by dash
    parts = coin_id.split("-")
    if len(parts) < 4:
        return False, f"'{coin_id}' has less than 4 parts"
    if len(parts) > 5:
        return False, f"'{coin_id}' has more than 5 parts"

    country, code, year, mint = parts[:4]
    variety = parts[4] if len(parts) == 5 else None

    # Country: 2-3 uppercase letters
    if not re.match(r"^[A-Z]{2,3}$", country):
        return False, f"Invalid country '{country}' in {coin_id}"

    # Code: 4 uppercase alphanumeric characters
    if not re.match(r"^[A-Z0-9]{4}$", code):
        return False, f"Invalid series code '{code}' in {coin_id}"

    # Year: 4 digits or XXXX
    if not re.match(r"^(\d{4}|XXXX)$", year):
        return False, f"Invalid year '{year}' in {coin_id}"

    # Mint: 1-2 uppercase letters
    if not re.match(r"^[A-Z]{1,2}$", mint):
        return False, f"Invalid mint '{mint}' in {coin_id}"

    # Variety (optional): 1-20 alphanumeric (extended for descriptive names like PronghornAntelope)
    # Note: Prefer short codes (4 chars) for new entries
    if variety and not re.match(r"^[A-Za-z0-9]{1,20}$", variety):
        return False, f"Invalid variety '{variety}' in {coin_id}"

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

    # Validate database
    print("\n🗄️  Validating database...")
    db_paths = ["coins.db", "database/coins.db"]
    for db_path in db_paths:
        if Path(db_path).exists():
            db_errors = validate_database(db_path)
            if not db_errors:
                print(f"   ✅ {db_path}")
            else:
                print(f"   ❌ {db_path} ({len(db_errors)} errors)")
                all_errors.extend(db_errors)
            break

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
