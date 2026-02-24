---
title: "feat: Add missing bullion taxonomy codes for price comparison"
type: feat
status: completed
date: 2026-02-23
---

# Add Missing Bullion Taxonomy Codes for Price Comparison

## Overview

Add taxonomy codes for bullion products that are missing from the database but needed by the u2-server price comparison system (PR #452). Covers British Britannias, Generic Rounds/Bars, Junk Silver, American Platinum Eagles, and Generic Gold Bars — approximately 14 product types across all major dealers.

## Problem Statement

The price comparison system at FindBullionPrices.com covers 14 product types across major dealers. Several common bullion products found on dealer sites have no taxonomy codes, blocking price matching. Without these codes, dealer listings for Britannias, generic silver, junk silver, and platinum eagles cannot be classified.

## Proposed Solution

Create a single migration script (`scripts/add_missing_bullion_issue130.py`) that:
1. Backs up `database/coins.db`
2. INSERTs new entries into `series_registry` and `coins` tables
3. Verifies inserts
4. Reminds to run export

Follow the established pattern from `scripts/add_international_bullion.py` (Issue #74).

## Series Code Definitions

### Abbreviation Convention

Follow existing family patterns:
- **Weight suffixes**: `O` = 1oz, `H` = 1/2oz, `Q` = 1/4oz, `T` = 1/10oz, `S` = 1/20oz (matches Gold Eagle: AGEO/AGEF/AGET/AGES and Maple Leaf: GMLO/GMLH/GMLQ/GMLS/GMLT)
- **Country codes**: `GB` for British, `US` for American, `XX` for generic/private-mint
- **Mint marks**: `RM` for Royal Mint, `W` for West Point, `X` for unspecified

### High Priority

| Product | Abbrev | series_id | coin_id | Denomination | Start Year |
|---------|--------|-----------|---------|-------------|------------|
| British Gold Britannia 1 oz | `BGBO` | `british_gold_britannia_1oz` | `GB-BGBO-XXXX-RM` | 100 Pounds | 1987 |
| British Gold Britannia 1/10 oz | `BGBT` | `british_gold_britannia_110oz` | `GB-BGBT-XXXX-RM` | 10 Pounds | 1987 |
| British Silver Britannia 1 oz | `BSBO` | `british_silver_britannia_1oz` | `GB-BSBO-XXXX-RM` | 2 Pounds | 1997 |
| Generic Silver Round 1 oz | `GNSR` | `generic_silver_round_1oz` | `XX-GNSR-XXXX-X` | No Face Value | 1970 |
| Generic Silver Bar 1 oz | `GSB1` | `generic_silver_bar_1oz` | `XX-GSB1-XXXX-X` | No Face Value | 1970 |
| Generic Silver Bar 5 oz | `GSB5` | `generic_silver_bar_5oz` | `XX-GSB5-XXXX-X` | No Face Value | 1970 |
| Generic Silver Bar 10 oz | `GS10` | `generic_silver_bar_10oz` | `XX-GS10-XXXX-X` | No Face Value | 1970 |
| Generic Silver Bar 100 oz | `G100` | `generic_silver_bar_100oz` | `XX-G100-XXXX-X` | No Face Value | 1970 |
| Junk Silver 90% $10 FV | `JS90` | `junk_silver_90pct` | `US-JS90-XXXX-X` | $10 Face Value | 1892 |

### Medium Priority

| Product | Abbrev | series_id | coin_id | Denomination | Start Year |
|---------|--------|-----------|---------|-------------|------------|
| American Platinum Eagle 1 oz | `APEO` | `american_platinum_eagle_1oz` | `US-APEO-XXXX-W` | $100 | 1997 |
| Generic Gold Bar 1 oz | `GNGB` | `generic_gold_bar_1oz` | `XX-GNGB-XXXX-X` | No Face Value | 1970 |

### Verified: No Collisions

All proposed abbreviations (`BGBO`, `BGBT`, `BSBO`, `GNSR`, `GSB1`, `GSB5`, `GS10`, `G100`, `JS90`, `APEO`, `GNGB`) checked against all ~172 existing codes — zero collisions.

### Already Exists (No Action Needed)

- **Gold Buffalo 1 oz**: `AGBF` already in database

## Technical Considerations

### Junk Silver Data Model

Junk Silver is conceptually different — it is a **bag of mixed coins** (pre-1965 dimes, quarters, half dollars), not a single coin type. This stretches the data model, which assumes one record = one coin type.

**Proposed approach**: Model as a single series_registry + coins entry with:
- `denomination`: `"$10 Face Value"`
- `weight_grams`: `715.0` (approximate silver content: ~7.15 troy oz)
- `diameter_mm`: `NULL`
- `composition`: `.900 Ag (mixed denominations)`
- `notes`: `"Bag of pre-1965 US 90% silver coins (dimes, quarters, half dollars). Weight approximate based on $10 face value = ~7.15 troy oz silver content."`
- `type`: `"bullion"` (valued by metal content, not numismatics)

This follows the pragmatic approach — it exists for price comparison, not numismatic cataloging.

### Export Pipeline Compatibility

Verified: `scripts/export_db_v1_1.py` dynamically queries `SELECT DISTINCT country_code FROM issues` and exports per-country JSON files. No hardcoded US-only logic. Existing non-US entries (GB Queen's Beasts, AU Koala, CA Maple Leaf, ZA Krugerrand) confirm the pipeline handles `GB` and `XX` correctly.

### Generic Product Country Code `XX`

Using `XX` for generic/private-mint products is consistent with existing `XX-WGLD` (World Gold Sovereigns). ISO 3166-1 does not assign `XX`, so no country collision.

### Series Groups

Group related products for easier querying:
- `"Britannia"` for all GB Britannia products
- `"Generic Silver"` for all XX silver rounds/bars
- `"Generic Gold"` for XX gold bars
- `"American Eagle"` for Platinum Eagle (matches existing Gold/Silver Eagle grouping)

### Physical Specifications

| Product | Weight (g) | Diameter (mm) | Composition | Edge |
|---------|-----------|---------------|-------------|------|
| Gold Britannia 1 oz | 31.1035 | 32.69 | .9999 Au | Reeded |
| Gold Britannia 1/10 oz | 3.1103 | 16.50 | .9999 Au | Reeded |
| Silver Britannia 1 oz | 31.1035 | 38.61 | .999 Ag | Reeded |
| Generic Silver Round 1 oz | 31.1035 | ~39.0 | .999 Ag | Varies |
| Generic Silver Bar 1 oz | 31.1035 | N/A | .999 Ag | N/A |
| Generic Silver Bar 5 oz | 155.517 | N/A | .999 Ag | N/A |
| Generic Silver Bar 10 oz | 311.035 | N/A | .999 Ag | N/A |
| Generic Silver Bar 100 oz | 3110.35 | N/A | .999 Ag | N/A |
| Junk Silver 90% bag | ~715.0 | N/A | .900 Ag | N/A |
| Platinum Eagle 1 oz | 31.1035 | 32.70 | .9995 Pt | Reeded |
| Generic Gold Bar 1 oz | 31.1035 | N/A | .999 Au | N/A |

### Aliases for Downstream Matching

Each series should include `aliases` JSON for text matching in the price comparison system:

```json
{
  "BGBO": ["Gold Britannia", "Brit Gold", "Royal Mint Gold Britannia"],
  "BSBO": ["Silver Britannia", "Brit Silver", "Royal Mint Silver Britannia"],
  "GNSR": ["Silver Round", ".999 Silver Round", "Generic Silver Round"],
  "GSB1": ["1 oz Silver Bar", ".999 Silver Bar"],
  "JS90": ["Junk Silver", "90% Silver", "Constitutional Silver", "$10 FV Silver", "Pre-1965 Silver"],
  "APEO": ["Platinum Eagle", "American Platinum Eagle", "APE"],
  "GNGB": ["Gold Bar", "1 oz Gold Bar", ".999 Gold Bar"]
}
```

## Scope Boundary

**In scope (this issue):**
- The 11 products listed above (9 high + 2 medium priority)
- Including 1 oz generic silver bar (missing from issue but most common traded size)

**Explicitly out of scope (future issues):**
- Additional Britannia fractionals (1/2 oz, 1/4 oz, 1/20 oz)
- Additional Platinum Eagle fractionals (1/2, 1/4, 1/10 oz)
- Additional generic bar sizes (10 oz gold, kilo bars)
- Junk Silver other face values ($5 FV, $100 FV, $1 FV rolls)

## Acceptance Criteria

- [x] Migration script `scripts/add_missing_bullion_issue130.py` created following existing pattern
- [x] All 11 series added to `series_registry` table with correct metadata
- [x] All 11 `XXXX` year coin entries added to `coins` table
- [x] No abbreviation collisions with existing ~172 codes
- [x] `uv run python scripts/export_from_database.py` runs successfully
- [x] New entries appear in `data/universal/series_registry.json`
- [x] New coin entries appear in country-specific universal JSON exports
- [x] `scripts/validate.py` passes
- [ ] Pre-commit hook export completes without errors
- [ ] All changes committed together (database + generated JSON)

## Implementation Steps

1. **Create migration script** `scripts/add_missing_bullion_issue130.py`
   - Follow `add_international_bullion.py` template
   - Define all 11 products with full metadata
   - INSERT OR IGNORE into `series_registry` and `coins`
   - Backup before writes, verify after

2. **Run migration**: `uv run python scripts/add_missing_bullion_issue130.py`

3. **Run export**: `uv run python scripts/export_from_database.py`

4. **Verify exports** — spot-check JSON files for new entries

5. **Commit all files**: `git add . && git commit`

6. **Create PR** referencing Issue #130

## Dependencies & Risks

- **Issue #129** (corrupted abbreviations) should be merged first — it fixes the series_registry validation. Current branch `fix/corrupted-series-abbreviations-129` has this fix.
- **Low risk**: All INSERTs use `INSERT OR IGNORE` making the script idempotent
- **Junk Silver modeling** is the highest-risk item — may need revision if downstream consumers need different granularity (e.g., separate $5/$10/$100 FV products)

## Sources

- GitHub Issue: [#130](https://github.com/mattsilv/coin-taxonomy/issues/130)
- Related: u2-server PR #452, coin-taxonomy Issue #129
- Template script: `scripts/add_international_bullion.py`
- Bullion guide: `docs/BULLION_INTEGRATION_GUIDE.md`
- ID format spec: `docs/taxonomy-id-format.md`
