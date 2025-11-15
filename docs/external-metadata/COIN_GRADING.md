# Coin Grading Standards - External Metadata Guide

**Version:** 1.0.0
**Last Updated:** 2025-01-28
**Status:** Official Standard

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Canonical Format Specification](#canonical-format-specification)
- [Reference Data Files](#reference-data-files)
- [Grade Validation](#grade-validation)
- [Use Cases](#use-cases)
- [Integration Patterns](#integration-patterns)
- [Common Pitfalls](#common-pitfalls)
- [API Reference](#api-reference)

---

## Overview

This document provides comprehensive guidance for external developers who want to standardize coin grade representation in their systems. The coin-taxonomy project provides **external metadata standards** that enable consistent grade formatting across collection management systems, market data APIs, and auction parsers.

### Scope

**✅ IN SCOPE:**
- Standardized grade schemas and reference data
- Grade validation and normalization utilities
- Integration with PCGS and NGC certification standards
- Support for collection management, market data, and auction parsing

**❌ OUT OF SCOPE:**
- Storing grades in the canonical taxonomy database
- Grading individual coins in the taxonomy itself
- This remains a taxonomy/catalog system, not a collection manager

### Key Principles

1. **One Canonical Format:** `MS-65` (uppercase + dash + number)
2. **Accept Variations:** Parse `MS65`, `MS 65`, `ms-65` but normalize to `MS-65`
3. **Industry Alignment:** Follow PCGS/NGC standards
4. **Validation Support:** Provide tools to verify grade strings

---

## Quick Start

### 1. Load Grade Reference Data

```python
import json

# Load unified grades
with open('data/references/grades_unified.json') as f:
    grades = json.load(f)

# Find a specific grade
ms65 = next(g for g in grades['grades'] if g['abbreviation'] == 'MS-65')
print(ms65)
# {
#   "grade": "Mint State (MS-65)",
#   "abbreviation": "MS-65",
#   "numeric_value": 65,
#   "category": "Uncirculated",
#   "market_threshold": true,
#   ...
# }
```

### 2. Validate a Grade String

```python
import re

def is_valid_grade(grade_str):
    """Validate grade against canonical format."""
    pattern = r'^[A-Z]{1,2}-\d{1,2}$'
    return bool(re.match(pattern, grade_str))

print(is_valid_grade('MS-65'))  # True
print(is_valid_grade('MS65'))   # False (not canonical, but acceptable for parsing)
```

### 3. Normalize to Canonical Format

```python
def normalize_grade(input_grade):
    """Normalize any grade format to canonical MS-65 format."""
    match = re.match(r'^([A-Z]{1,2})[\s-]?(\d{1,2})$', input_grade.upper())
    if not match:
        raise ValueError(f"Invalid grade format: {input_grade}")

    abbr, num = match.groups()
    return f"{abbr}-{num}"

print(normalize_grade('MS65'))   # MS-65
print(normalize_grade('MS 65'))  # MS-65
print(normalize_grade('ms-65'))  # MS-65
```

---

## Canonical Format Specification

### Grade Format: `{ABBR}-{NUM}`

**Pattern:** `^[A-Z]{1,2}-\d{1,2}$`

**Components:**
- **Abbreviation:** 1-2 uppercase letters (MS, PR, PF, AU, VF, XF, etc.)
- **Separator:** Single dash `-`
- **Number:** 1-2 digit numeric value (1-70 on Sheldon scale)

**Valid Examples:**
```
MS-65    ✅ Mint State 65
PR-69    ✅ Proof 69
AU-58    ✅ About Uncirculated 58
VF-30    ✅ Very Fine 30
XF-45    ✅ Extremely Fine 45
G-4      ✅ Good 4
```

**Invalid Examples:**
```
MS65     ❌ Missing dash (acceptable for parsing, not for storage)
MS 65    ❌ Space instead of dash (acceptable for parsing, not for storage)
ms-65    ❌ Lowercase (acceptable for parsing, not for storage)
MS-65RD  ❌ Modifier attached (use modifiers array instead)
```

### Full Grade String Format: `{SERVICE} {GRADE} {MODIFIERS}`

**Pattern:** `^([A-Z]+\s+)?[A-Z]{1,2}-\d{1,2}(\s+[A-Z+*]+)*$`

**Components:**
- **Service:** Optional UPPERCASE service code (PCGS, NGC)
- **Space Separator**
- **Grade:** Canonical format (MS-65)
- **Space Separator**
- **Modifiers:** Optional UPPERCASE modifiers, space-separated

**Valid Examples:**
```
PCGS MS-65          ✅ PCGS certified Gem Uncirculated
NGC PR-69 DCAM      ✅ NGC certified Proof with Deep Cameo
PCGS MS-67 FB RD    ✅ PCGS Superb Gem with Full Bands and Red
MS-63               ✅ Raw (uncertified) coin
NGC AU-58           ✅ NGC certified About Uncirculated
```

---

## Reference Data Files

### 1. Unified Grades (`data/references/grades_unified.json`)

Complete Sheldon 70-point scale with all grades from P-1 through MS-70, PR-60 through PR-70, and SP-60 through SP-70.

**Structure:**
```json
{
  "version": "1.0.0",
  "standard": "Sheldon 70-Point Scale",
  "canonical_format": "MS-65",
  "grades": [
    {
      "grade": "Mint State (MS-65)",
      "abbreviation": "MS-65",
      "numeric_value": 65,
      "category": "Uncirculated",
      "subcategory": "Gem Uncirculated",
      "market_threshold": true,
      "alternate_notations": ["MS65", "MS 65", "Gem BU"]
    }
  ]
}
```

**Use Cases:**
- Populate grade dropdown menus
- Convert numeric to descriptive formats
- Identify market threshold grades
- Validate grade abbreviations

### 2. Grade Standards (`data/universal/grade_standards.json`) ⭐ NEW

**Database-First:** This file is generated from the SQLite database (source of truth). See: [GitHub Issue #64](https://github.com/mattsilv/coin-taxonomy/issues/64)

Complete grading hierarchy with parsing rules for multi-grade expressions and RAW-{grade} classification.

**Structure:**
```json
{
  "version": "1.0.0",
  "standard": "Sheldon 70-Point Scale",
  "grade_hierarchy": [
    {
      "grade": "MS-65",
      "grade_name": "Mint State (MS-65)",
      "grade_numeric": 65,
      "grade_category": "Uncirculated",
      "grade_subcategory": "Gem Uncirculated",
      "market_threshold": true,
      "market_relevance": "very_high",
      "sheldon_range": {"min": 65, "max": 65},
      "abbreviations": ["MS65", "MS 65", "Gem"],
      "aliases": null
    }
  ],
  "parsing_rules": {
    "multi_grade_separator_patterns": ["/", "-", " to "],
    "multi_grade_strategy": "conservative",
    "grade_extraction_patterns": [
      {
        "name": "basic_pattern",
        "pattern": "^([A-Z]{1,2})-(\\d{1,2})$"
      }
    ]
  },
  "comparison_utilities": {
    "getLowestGrade": "Find the lowest grade from an array",
    "normalizeGrade": "Convert aliases to canonical format",
    "compareGrades": "Compare two grades (-1, 0, 1)"
  }
}
```

**Use Cases:**

**A. Multi-Grade Parsing (eBay, Marketplace Listings)**
```python
# Parse "XF/AU" → take lower grade (conservative strategy)
def parse_multi_grade(grade_str, grade_standards):
    separators = grade_standards['parsing_rules']['multi_grade_separator_patterns']

    for sep in separators:
        if sep in grade_str:
            grades = grade_str.split(sep)
            # Strategy: conservative = take lowest grade
            return get_lowest_grade(grades, grade_standards)

    return normalize_grade(grade_str)

# Example: "XF/AU" → "XF-40" (lower grade)
# Example: "MS-63 to MS-65" → "MS-63" (lower grade)
```

**B. RAW-{grade} Classification for Uncertified Coins**
```python
# Classify uncertified coins by grade range
def classify_raw_coin(listing_text, grade_standards):
    grade = extract_grade(listing_text, grade_standards)
    return f"RAW-{grade}"

# Example: "1892 COLUMBIAN EXPOSITION XF/AU" → "RAW-XF"
# Used for: Price intelligence buckets (RAW-VF, RAW-XF, RAW-AU)
```

**C. Grade Comparison and Sorting**
```python
def compare_grades(grade1, grade2, grade_standards):
    """Compare two grades. Returns -1, 0, or 1."""
    hierarchy = grade_standards['grade_hierarchy']

    g1 = next((g for g in hierarchy if g['grade'] == grade1), None)
    g2 = next((g for g in hierarchy if g['grade'] == grade2), None)

    if g1['grade_numeric'] < g2['grade_numeric']:
        return -1
    elif g1['grade_numeric'] > g2['grade_numeric']:
        return 1
    return 0

# Example: compare_grades("MS-63", "MS-65") → -1 (MS-63 is lower)
```

**D. Market Relevance Filtering**
```python
# Get only high-relevance grades for UI dropdowns
def get_common_grades(grade_standards):
    return [
        g for g in grade_standards['grade_hierarchy']
        if g['market_relevance'] in ['high', 'very_high']
    ]

# Returns: MS-65, MS-67, PR-69, AU-58, XF-45, etc.
# Omits: MS-61, PR-61 (low market relevance)
```

**Database Integration:**
```bash
# Regenerate grade_standards.json from database
uv run python scripts/export_from_database.py

# The migration that populates the database
uv run python scripts/migrate_add_grade_standards.py
```

### 3. Grading Services (`data/references/grading_services.json`)

Registry of PCGS and NGC certification details.

**Structure:**
```json
{
  "services": [
    {
      "code": "PCGS",
      "name": "Professional Coin Grading Service",
      "cert_number_format": {
        "pattern": "\\d{8}",
        "example": "12345678"
      },
      "grade_format": "PCGS {GRADE}",
      "grade_format_examples": ["PCGS MS-65", "PCGS PR-69 DCAM"]
    }
  ]
}
```

**Use Cases:**
- Validate certification numbers
- Parse certified grade strings
- Verify service-specific format conventions

### 3. Grade Modifiers (`data/references/grade_modifiers.json`)

Registry of common grade modifiers and special designations.

**Structure:**
```json
{
  "modifiers": [
    {
      "code": "DCAM",
      "name": "Deep Cameo",
      "applies_to_strike_types": ["proof", "specimen"],
      "market_premium": "high",
      "grading_services": ["PCGS", "NGC"]
    }
  ]
}
```

**Use Cases:**
- Validate modifier compatibility
- Parse auction listings
- Estimate market premiums
- Normalize service-specific codes (DCAM vs UC)

### 4. JSON Schema (`data/schema/grade_external_metadata.schema.json`)

Validation schema for external metadata systems.

**Use Cases:**
- Validate JSON data structures
- Generate TypeScript/OpenAPI types
- Enforce data consistency
- Document API contracts

---

## Grade Validation

### Basic Validation

```python
import re
import json

class GradeValidator:
    def __init__(self, grades_file='data/references/grades_unified.json'):
        with open(grades_file) as f:
            data = json.load(f)
            self.valid_grades = {g['abbreviation']: g for g in data['grades']}
            self.canonical_pattern = re.compile(data['canonical_format_pattern'])

    def validate_canonical(self, grade_str):
        """Validate grade string matches canonical format."""
        if not self.canonical_pattern.match(grade_str):
            return False, "Does not match canonical format"

        if grade_str not in self.valid_grades:
            return False, f"Unknown grade: {grade_str}"

        return True, "Valid"

    def validate_numeric(self, numeric_value):
        """Validate numeric grade value (1-70)."""
        if not isinstance(numeric_value, int):
            return False, "Numeric value must be integer"

        if numeric_value < 1 or numeric_value > 70:
            return False, "Numeric value must be 1-70"

        return True, "Valid"

# Usage
validator = GradeValidator()
print(validator.validate_canonical('MS-65'))  # (True, 'Valid')
print(validator.validate_numeric(65))         # (True, 'Valid')
```

### Normalization

```python
class GradeNormalizer:
    @staticmethod
    def normalize(input_grade):
        """
        Normalize any grade format to canonical format.

        Accepts:
          - MS65, MS 65, ms-65 → MS-65
          - PR69, PR 69, pr-69 → PR-69
        """
        input_clean = input_grade.strip().upper()

        # Extract abbreviation and number
        match = re.match(r'^([A-Z]{1,2})[\s-]?(\d{1,2})$', input_clean)
        if not match:
            raise ValueError(f"Invalid grade format: {input_grade}")

        abbr, num = match.groups()

        # Return canonical format
        return f"{abbr}-{num}"

    @staticmethod
    def normalize_full_string(input_str):
        """
        Normalize full grade string with service and modifiers.

        Accepts:
          - "PCGS MS65 RD" → "PCGS MS-65 RD"
          - "pcgs ms-65rd" → "PCGS MS-65 RD"
        """
        parts = input_str.strip().upper().replace('  ', ' ').split()

        normalized = []
        for part in parts:
            # Check if this looks like a grade (contains digit)
            if re.search(r'\d', part):
                # Extract grade and any attached modifiers
                grade_match = re.match(r'^([A-Z]{1,2})[\s-]?(\d{1,2})([A-Z]+)?$', part)
                if grade_match:
                    abbr, num, modifier = grade_match.groups()
                    normalized.append(f"{abbr}-{num}")
                    if modifier:
                        normalized.append(modifier)
                else:
                    normalized.append(part)
            else:
                normalized.append(part)

        return ' '.join(normalized)

# Usage
normalizer = GradeNormalizer()
print(normalizer.normalize('MS65'))                    # MS-65
print(normalizer.normalize_full_string('PCGS MS65 RD'))  # PCGS MS-65 RD
```

### Full Validation with Schema

```python
from jsonschema import validate, ValidationError

def validate_grade_metadata(grade_data, schema_file='data/schema/grade_external_metadata.schema.json'):
    """Validate grade metadata against JSON schema."""
    with open(schema_file) as f:
        schema = json.load(f)

    try:
        validate(instance=grade_data, schema=schema)
        return True, "Valid"
    except ValidationError as e:
        return False, str(e)

# Usage
grade_metadata = {
    "grade": "MS-65",
    "grade_numeric": 65,
    "grading_service": "PCGS",
    "certification_number": "12345678",
    "modifiers": ["RD"],
    "full_grade_string": "PCGS MS-65 RD"
}

is_valid, message = validate_grade_metadata(grade_metadata)
print(f"Valid: {is_valid}, Message: {message}")
```

---

## Use Cases

### 1. Collection Management System

**Scenario:** User tracking personal coin collection with grades.

```python
# Collection entry with grade metadata
collection_entry = {
    "coin_id": "US-LWC-1909-S",  # From coin-taxonomy
    "quantity": 1,
    "grade": "MS-64",
    "grade_numeric": 64,
    "grading_service": "PCGS",
    "certification_number": "12345678",
    "modifiers": ["RB"],
    "full_grade_string": "PCGS MS-64 RB",
    "purchase_price": 450.00,
    "purchase_date": "2024-03-15",
    "notes": "Nice original surfaces, key date"
}

# Validate before storing
validator = GradeValidator()
is_valid, msg = validator.validate_canonical(collection_entry['grade'])
if is_valid:
    # Store in database
    print(f"Storing coin: {collection_entry['full_grade_string']}")
```

### 2. Market Data / Pricing API

**Scenario:** Connecting grades to market pricing data.

```python
# Price guide with grade-specific values
price_guide = {
    "coin_id": "US-IHC-1877-P",
    "prices_by_grade": [
        {
            "grade": "G-4",
            "grade_numeric": 4,
            "market_value": 750,
            "market_threshold": False
        },
        {
            "grade": "VF-20",
            "grade_numeric": 20,
            "market_value": 1800,
            "market_threshold": False
        },
        {
            "grade": "MS-63",
            "grade_numeric": 63,
            "market_value": 6000,
            "market_threshold": True  # Key price break
        },
        {
            "grade": "MS-65",
            "grade_numeric": 65,
            "market_value": 15000,
            "market_threshold": True  # Major premium tier
        }
    ]
}

# Identify market threshold grades
threshold_grades = [
    p for p in price_guide['prices_by_grade']
    if p['market_threshold']
]
print(f"Key price breaks: {[g['grade'] for g in threshold_grades]}")
```

### 3. Auction Listing Parser

**Scenario:** Parsing eBay/Heritage/GreatCollections listings.

```python
def parse_auction_title(title):
    """
    Extract grade information from auction title.

    Examples:
      "1909-S VDB Lincoln Cent PCGS MS-65 RD Gem"
      "1877 Indian Head Cent NGC AU-58"
      "Mercury Dime 1916-D MS67 FB Full Bands"
    """
    normalizer = GradeNormalizer()

    # Look for grading service
    service = None
    for svc in ['PCGS', 'NGC', 'ANACS', 'ICG']:
        if svc in title.upper():
            service = svc
            break

    # Extract grade pattern
    grade_pattern = r'\b([A-Z]{1,2})[\s-]?(\d{1,2})\b'
    grade_match = re.search(grade_pattern, title.upper())

    if not grade_match:
        return None

    # Normalize grade
    abbr, num = grade_match.groups()
    canonical_grade = f"{abbr}-{num}"

    # Look for modifiers
    modifiers = []
    for mod in ['DCAM', 'CAM', 'FB', 'RD', 'RB', 'BN']:
        if mod in title.upper():
            modifiers.append(mod)

    return {
        "grade": canonical_grade,
        "grade_numeric": int(num),
        "grading_service": service or "raw",
        "modifiers": modifiers,
        "full_grade_string": ' '.join(filter(None, [service, canonical_grade] + modifiers))
    }

# Test
title = "1909-S VDB Lincoln Cent PCGS MS-65 RD Gem"
parsed = parse_auction_title(title)
print(parsed)
# {
#   'grade': 'MS-65',
#   'grade_numeric': 65,
#   'grading_service': 'PCGS',
#   'modifiers': ['RD'],
#   'full_grade_string': 'PCGS MS-65 RD'
# }
```

---

## Integration Patterns

### Pattern 1: Input → Normalize → Validate → Store

```python
def process_grade_input(user_input):
    """
    Accept user input in any format, normalize, validate, and store.
    """
    normalizer = GradeNormalizer()
    validator = GradeValidator()

    # Step 1: Normalize to canonical format
    try:
        canonical = normalizer.normalize(user_input)
    except ValueError as e:
        return {"error": str(e)}

    # Step 2: Validate canonical format
    is_valid, message = validator.validate_canonical(canonical)
    if not is_valid:
        return {"error": message}

    # Step 3: Store in canonical format
    return {
        "grade": canonical,
        "grade_numeric": int(canonical.split('-')[1]),
        "status": "stored"
    }

# Usage
print(process_grade_input('MS65'))   # Accepts and normalizes
print(process_grade_input('MS 65'))  # Accepts and normalizes
print(process_grade_input('MS-65'))  # Already canonical
print(process_grade_input('ZZ-99'))  # Rejects invalid grade
```

### Pattern 2: Database Query with Grade Range

```python
def query_by_grade_range(min_grade, max_grade):
    """
    Query collection by numeric grade range.
    """
    query = """
    SELECT * FROM collection
    WHERE grade_numeric BETWEEN ? AND ?
    ORDER BY grade_numeric DESC
    """
    # Execute query with min_grade, max_grade
    return results

# Find all Gem Uncirculated coins (MS-65 to MS-70)
gems = query_by_grade_range(65, 70)
```

### Pattern 3: API Response with Canonical Format

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/collection/<coin_id>')
def get_collection_item(coin_id):
    """
    Return collection item with grade in canonical format.
    """
    item = db.get_collection_item(coin_id)

    # Ensure grade is in canonical format before returning
    if item and 'grade' in item:
        normalizer = GradeNormalizer()
        item['grade'] = normalizer.normalize(item['grade'])

    return jsonify(item)
```

---

## Common Pitfalls

### 1. Storing Non-Canonical Formats

**❌ Wrong:**
```python
# Storing user input directly
coin['grade'] = 'MS65'  # Not canonical!
```

**✅ Correct:**
```python
# Always normalize before storing
normalizer = GradeNormalizer()
coin['grade'] = normalizer.normalize('MS65')  # MS-65
```

### 2. Case-Sensitive Comparisons

**❌ Wrong:**
```python
if grade == 'ms-65':  # Won't match 'MS-65'
    ...
```

**✅ Correct:**
```python
if grade.upper() == 'MS-65':  # Case-insensitive comparison
    ...
```

### 3. Ignoring Modifier Compatibility

**❌ Wrong:**
```python
# Accepting invalid modifier combinations
grade = {
    "grade": "MS-65",      # Business strike
    "modifiers": ["DCAM"]  # DCAM only for proofs!
}
```

**✅ Correct:**
```python
# Validate modifier compatibility
def validate_modifiers(grade, modifiers):
    if 'DCAM' in modifiers and not grade.startswith('PR-'):
        raise ValueError("DCAM only applies to proof coins")
```

### 4. Not Validating Certification Numbers

**❌ Wrong:**
```python
# Accepting any cert number format
cert_number = '123'  # Too short for PCGS!
```

**✅ Correct:**
```python
# Validate cert number format by service
if service == 'PCGS':
    if not re.match(r'^\d{8}$', cert_number):
        raise ValueError("PCGS cert numbers must be 8 digits")
```

---

## API Reference

### GradeValidator Class

```python
class GradeValidator:
    """
    Validates coin grades against unified standard.
    """

    def __init__(self, grades_file):
        """Initialize with grades reference file."""
        pass

    def validate_canonical(self, grade_str):
        """
        Validate grade matches canonical format.

        Returns:
            (bool, str): (is_valid, message)
        """
        pass

    def validate_numeric(self, numeric_value):
        """
        Validate numeric grade value (1-70).

        Returns:
            (bool, str): (is_valid, message)
        """
        pass

    def is_market_threshold(self, grade_str):
        """
        Check if grade represents market threshold.

        Returns:
            bool: True if market threshold grade
        """
        pass
```

### GradeNormalizer Class

```python
class GradeNormalizer:
    """
    Normalizes grade strings to canonical format.
    """

    @staticmethod
    def normalize(input_grade):
        """
        Normalize grade to canonical format (MS-65).

        Args:
            input_grade (str): Grade in any format

        Returns:
            str: Canonical format grade

        Raises:
            ValueError: If input is invalid
        """
        pass

    @staticmethod
    def normalize_full_string(input_str):
        """
        Normalize full grade string with service and modifiers.

        Args:
            input_str (str): Full grade string

        Returns:
            str: Normalized full grade string
        """
        pass
```

---

## Additional Resources

- **GitHub Issue:** [#62 - Unified Coin Grading Standard](https://github.com/mattsilv/coin-taxonomy/issues/62)
- **Reference Files:**
  - `data/references/grades_unified.json`
  - `data/references/grading_services.json`
  - `data/references/grade_modifiers.json`
- **Schema:** `data/schema/grade_external_metadata.schema.json`
- **Industry Standards:**
  - [PCGS Grading Guide](https://www.pcgs.com/grades)
  - [NGC Grading Scale](https://www.ngccoin.com/grading/)
  - ANA Official Grading Standards (ISBN: 978-0-7948-4268-1)

---

## Support

For questions or issues with the grading standard:

1. Check the [GitHub Issues](https://github.com/mattsilv/coin-taxonomy/issues)
2. Review the reference files in `data/references/`
3. Consult industry resources (PCGS, NGC)
4. Open a new issue with the `external-metadata` label

---

**Version History:**
- v1.0.0 (2025-01-28): Initial release with complete Sheldon 70-point scale, PCGS/NGC support, and comprehensive documentation
