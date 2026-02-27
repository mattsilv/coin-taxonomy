---
title: Add missing bullion taxonomy codes for price comparison system
date: 2026-02-23
category: database-issues
tags:
  - bullion
  - taxonomy
  - migration
  - schema-validation
  - export-pipeline
severity: medium
component:
  - database
  - scripts
  - schema
issue: "#130"
status: resolved
---

# Missing Bullion Taxonomy Codes Migration

## Problem

The coin-taxonomy database lacked 11 bullion product taxonomy codes needed by the u2-server price comparison system (FindBullionPrices.com). Products missing: British Britannias (Gold 1oz, Gold 1/10oz, Silver 1oz), Generic Silver (Rounds 1oz, Bars 1/5/10/100oz), Junk Silver 90%, American Platinum Eagle 1oz, and Generic Gold Bar 1oz. Without these codes, dealer listings could not be classified for price matching.

## Root Cause

Simple data gap -- these products hadn't been added to the taxonomy yet. However, the implementation revealed several pipeline gotchas.

## Solution

Created migration script `scripts/add_missing_bullion_issue130.py` following the `add_international_bullion.py` template. Defined 11 products with full metadata and used `INSERT OR IGNORE` for idempotent inserts into both `series_registry` and `coins` tables.

### Products Added

| Code | Product | Country | Denomination |
|------|---------|---------|-------------|
| BGBO | British Gold Britannia 1 oz | GB | 100 Pounds |
| BGBT | British Gold Britannia 1/10 oz | GB | 10 Pounds |
| BSBO | British Silver Britannia 1 oz | GB | 2 Pounds |
| GNSR | Generic Silver Round 1 oz | XX | No Face Value |
| GSB1 | Generic Silver Bar 1 oz | XX | No Face Value |
| GSB5 | Generic Silver Bar 5 oz | XX | No Face Value |
| GS10 | Generic Silver Bar 10 oz | XX | No Face Value |
| G100 | Generic Silver Bar 100 oz | XX | No Face Value |
| JS90 | Junk Silver 90% $10 FV | US | $10 Face Value |
| APEO | American Platinum Eagle 1 oz | US | $100 |
| GNGB | Generic Gold Bar 1 oz | XX | No Face Value |

### Migration Script Pattern

```python
BULLION_SERIES = [
    {
        "country": "GB", "code": "BGBO",
        "name": "British Gold Britannia (1 oz)",
        "series_id": "british_gold_britannia_1oz",
        "denomination": "100 Pounds", "start_year": 1987,
        "weight_grams": 31.1035, "composition": ".9999 Au",
        "aliases": ["Gold Britannia", "Brit Gold"],
        "series_group": "Britannia", "mint": "RM", "type": "bullion",
    },
    # ... 10 more entries
]
```

### Key Design Decisions

- **Abbreviation convention**: Weight suffixes O=1oz, H=1/2oz, T=1/10oz matching existing Gold Eagle/Maple Leaf patterns
- **Country codes**: GB for British, XX for generic/private-mint (consistent with existing XX-WGLD)
- **Junk Silver**: Modeled as single entry with `$10 Face Value` denomination, ~715g weight, type=bullion. Pragmatic approach for price comparison, not numismatic cataloging.
- **All entries use XXXX random year pattern** with appropriate mint marks (RM=Royal Mint, W=West Point, X=unspecified)

## Gotchas Encountered

### 1. Export pipeline requires 3 separate scripts (not 1)

The main export script (`export_from_database.py`) does NOT call the universal export. The full pipeline is:

```bash
# Step 1: Main export (coins → JSON)
uv run python scripts/export_from_database.py

# Step 2: Populate issues table from coins (required before Step 3)
uv run python scripts/migrate_to_universal_v1_1.py

# Step 3: Universal format export (series_registry.json, country issues)
uv run python scripts/export_db_v1_1.py
```

Missing Step 2 or 3 means new entries appear in the database but NOT in the universal JSON exports that downstream consumers read.

### 2. Validation schema has hardcoded denomination enum

The pre-commit hook validates against `data/us/schema/coin.schema.json` which has a hardcoded list of allowed denominations. Adding `$100` (Platinum Eagle) and `$10 Face Value` (Junk Silver) required updating this enum. **Always check the schema when introducing new denomination types.**

### 3. Abbreviation collision checking is manual

Must query existing ~172+ codes before choosing new abbreviations:
```sql
SELECT series_abbreviation FROM series_registry ORDER BY series_abbreviation;
```

## Prevention Checklist

For future bullion/coin series additions:

- [ ] Check abbreviation uniqueness against all existing codes in series_registry
- [ ] Check if new denominations need adding to `data/us/schema/coin.schema.json` enum
- [ ] Run all 3 export scripts in order (export_from_database, migrate_to_universal, export_db_v1_1)
- [ ] Verify new entries appear in `data/universal/series_registry.json`
- [ ] Verify country-specific issue files created (e.g., `gb_issues.json`, `xx_issues.json`)
- [ ] Pre-commit hook passes all validation checks

## Follow-Up: Britannia/RCM Expansion (Issue #135)

Applied the same pattern to add weight suffix variants for existing Britannia series and new branded bar series:

| coin_id | Product |
|---------|---------|
| `GB-BSBO-XXXX-RM-2oz` | Silver Britannia 2 oz |
| `GB-BSBO-XXXX-RM-10oz` | Silver Britannia 10 oz |
| `GB-BGBO-XXXX-RM-14oz` | Gold Britannia 1/4 oz |
| `GB-BGBO-XXXX-RM-12oz` | Gold Britannia 1/2 oz |
| `CA-RCMB-XXXX-P-10oz` | RCM Silver Bar 10 oz |
| `GB-RMSB-XXXX-RM-10oz` | Royal Mint Silver Bar 10 oz |

### Key Learnings from #135

- **Weight suffix pattern extends to sizes > 1oz**: `2oz`, `10oz` work alongside existing fractional suffixes (`14oz`, `12oz`, `110oz`). No schema or constraint changes needed.
- **Branded bar products get their own series codes**: RCM Silver Bar (`RCMB`) and Royal Mint Silver Bar (`RMSB`) are distinct from generic silver bars (`GS10`) since branding affects dealer premiums.
- **`variety_suffixes` on existing series**: Updated `BSBO` and `BGBO` with their new weight suffixes to document valid suffix values for downstream consumers.
- **No denomination schema update needed**: Bar products use "Silver Bar" denomination (no face value), and Britannia sizes use existing GBP denominations (5, 10, 25, 50 Pounds).

## Cross-References

- **Issue**: [#130](https://github.com/mattsilv/coin-taxonomy/issues/130)
- **Related**: [#129 - Corrupted series abbreviations](https://github.com/mattsilv/coin-taxonomy/issues/129) (should be merged first)
- **Template script**: `scripts/add_international_bullion.py` (Issue #74)
- **Bullion guide**: `docs/BULLION_INTEGRATION_GUIDE.md`
- **ID format spec**: `docs/taxonomy-id-format.md`
- **Prior solution**: `docs/solutions/database-issues/corrupted-series-abbreviations-migration.md`
- **Downstream**: u2-server PR #452 (price comparison system)
