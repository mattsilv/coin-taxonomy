---
title: Fix corrupted series_abbreviation values in SQLite database
date: 2026-02-23
category: database-issues
tags: [series-abbreviations, data-corruption, migration, validation, merge-pattern]
module: database/coins.db, scripts/migrate_to_universal_v1_1.py, TaxonomyValidator
severity: high
symptom: 11 corrupted series_abbreviation entries containing invalid characters (parens, dollar signs, spaces, full names) affecting 295 issue_ids
root_cause: migrate_to_universal_v1_1.py auto-generated abbreviations from series names without sanitization
resolution_type: migration-script
---

# Corrupted Series Abbreviations Migration

## Problem

Several `series_abbreviation` values in `series_registry` were corrupted — containing parentheses (`AGE(`), dollar signs (`$10`), spaces (`5 C`), trailing whitespace (`$5 `), or full series names (`American Gold Buffalo (1 oz)`). This broke automated mapping for downstream consumers.

**Affected**: 11 corrupted abbreviations, 295 issue_ids renamed, 2 dead entries deleted, 5 Gold Maple Leaf entries renamed.

## Solution

### Root Cause

The `generate_unique_series_abbreviation()` function in `scripts/migrate_to_universal_v1_1.py` (lines 340-368) failed to sanitize special characters:
- **Strategy 2 (word initials)** extracted first letters including parentheses: "American Gold Eagle (1 oz)" produced `A+G+E+(` = `AGE(`
- **Strategy 1 (first N chars)** preserved leading special characters: "$10 Gold" produced `$10`
- Whitespace and trailing characters were not stripped

### Investigation

1. Discovered while building price comparison system that maps dealer products to taxonomy codes
2. Queried series_registry for non-alphanumeric abbreviations — found 11 corrupted entries
3. Traced corruption to `generate_unique_series_abbreviation()` logic
4. Found that `AGEO`/`ASEA` already existed as correct entries with 0 issues — requiring **merge**, not simple rename
5. SpecFlow analysis revealed Gold Maple Leaf `GOL` entries are NOT duplicates (`GOL` = 100kg Big Maple Leaf, a completely different product)
6. Identified 99 pre-existing FK violations as out-of-scope (Engelhard bars, Mexican Libertads)

### Solution Steps

Migration script: `scripts/fix_corrupted_abbreviations.py`

1. **Backup** — `shutil.copy2()` before any changes
2. **Disable FK checks** — `PRAGMA foreign_keys = OFF` during migration
3. **Fix full-name abbreviations on targets first** (Step 1 ordering is critical — must happen before merges)
4. **Merge corrupted entries** — Re-point FK, rename issue_id, delete old row
5. **Simple renames** — Canadian and GML entries with collision checking
6. **Delete dead entries** — 0-issue rows (GMLO, E100)
7. **Single transaction** with rollback on error
8. **Relax validator** — `SERIES_CODE_PATTERN` from `{4}` to `{2,4}`

### Key Code Pattern: Merge vs Rename

When the target abbreviation already exists in a UNIQUE column, you cannot simply UPDATE — you must **merge**:

```python
# Step 1: Fix target series' full-name abbreviation FIRST
# (target row exists but has corrupted abbreviation too)
FIX_FULL_NAME_ABBREVS = {
    "American Silver Eagle (1 oz)": "ASEA",  # series_id: american_silver_eagle_1oz
    "American Gold Buffalo (1 oz)": "AGBF",  # series_id: american_gold_buffalo_1oz
}

# Step 2: Merge corrupted entries into correct targets
# (target abbreviation must exist before merge can reference it)
MERGE_MAP = {
    "AGE(": ("american_gold_eagle_1oz", "AGEO"),
    "ASE(": ("american_silver_eagle_1oz", "ASEA"),
    "AME": ("american_gold_buffalo_1oz", "AGBF"),
}

# Merge logic per entry:
# 1. Re-point all issues: UPDATE issues SET series_id = target WHERE series_id = source
# 2. Rename issue_ids: replace old abbreviation in ID string
# 3. Delete source row: DELETE FROM series_registry WHERE series_id = source
```

**Why ordering matters**: If you try to rename `ASE(` → `ASEA` directly, it fails because `ASEA` already exists (UNIQUE constraint). You must first fix the target's own corrupted abbreviation (full name → proper code), then merge the source into it.

## Prevention

### High Priority

1. **Wire TaxonomyValidator into pre-commit** — Add series_abbreviation format validation to `scripts/data_integrity_check.py`. Fail the hook if any abbreviation doesn't match `^[A-Z0-9]{2,4}$`.

2. **Add database CHECK constraint**:
   ```sql
   CHECK(series_abbreviation GLOB '[A-Z0-9][A-Z0-9]*'
     AND length(series_abbreviation) BETWEEN 2 AND 4)
   ```

### Medium Priority

3. **Fix the generation function** — Sanitize `generate_unique_series_abbreviation()` to strip non-alphanumeric characters before generating abbreviations.

4. **Make audit test actually fail** — `test_taxonomy_validation.py` has a `test_series_code_format_audit` that explicitly always passes (`self.assertTrue(True)`). Make it assert on violations.

### Low Priority

5. **Create `sanitize_abbreviation()` utility** — Centralized function for all migration scripts to use.

6. **Add dry-run mode** to migration scripts that shows generated abbreviations before committing.

## Cross-References

- **Issue**: [#129](https://github.com/mattsilv/coin-taxonomy/issues/129)
- **PR**: [#131](https://github.com/mattsilv/coin-taxonomy/pull/131)
- **Root cause script**: `scripts/migrate_to_universal_v1_1.py:340-368`
- **Fix script**: `scripts/fix_corrupted_abbreviations.py`
- **Similar fix**: `scripts/fix_corrupted_varieties.py` (nested object corruption)
- **Similar fix**: `scripts/fix_coin_id_format.py` (PK rename pattern)
- **Correct abbreviations source**: `scripts/add_silver_eagles_and_gold_buffalos.py`, `scripts/add_gold_eagle_series.py`
- **Validator**: `scripts/utils/taxonomy_validator.py:60`
- **ID format spec**: `docs/taxonomy-id-format.md`
- **Source of truth**: `docs/SOURCE_OF_TRUTH.md`
