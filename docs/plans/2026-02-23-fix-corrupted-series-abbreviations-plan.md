---
title: "fix: Corrupted series abbreviations in coins.db"
type: fix
status: completed
date: 2026-02-23
---

# fix: Corrupted series abbreviations in coins.db

## Overview

Several `series_abbreviation` values in `series_registry` are corrupted — containing parentheses, dollar signs, spaces, trailing whitespace, or full series names instead of 2-4 character codes. This breaks automated mapping for downstream consumers (e.g., precious metals price comparison in mattsilv/u2-server#451). Additionally, some series have duplicate/overlapping entries from the original auto-migration.

## Problem Statement / Motivation

The `migrate_to_universal_v1_1.py` script auto-generated abbreviations using a strategy that didn't sanitize special characters. This produced:
- **Paren artifacts**: `ASE(`, `AGE(` (from series names containing "(1 oz)")
- **Dollar signs/spaces**: `$10`, `$5 `, `10 `, `25 `, `5 C`, `5 C1`, `50 ` (from Canadian coin names starting with numbers)
- **Full names as abbreviations**: `American Gold Buffalo (1 oz)`, `American Silver Eagle (1 oz)` stored in abbreviation field
- **Duplicate entries**: Gold Maple Leaf has 7 overlapping series_registry rows (`GML`, `GOL`, `GOL1`-`GOL4`, `GMLO`)

**120 issue_ids** in the `issues` table contain these corrupted abbreviations (e.g., `CA-5 C-1968-P`, `US-AGE(-XXXX-X`), violating the coin ID format standard.

## Proposed Solution

Create a migration script following the `fix_corrupted_varieties.py` pattern to:
1. Fix corrupted `series_abbreviation` values in `series_registry`
2. Update all affected `issue_id` values in `issues` table
3. Merge duplicate series entries where target abbreviation already exists
4. Remove dead entries (0-issue rows with full-name abbreviations)
5. Relax `TaxonomyValidator.SERIES_CODE_PATTERN` from `{4}` to `{2,4}` to match CLAUDE.md spec

## Technical Considerations

### Critical: AGEO/ASEA Already Exist — Merge Required

The database already has correctly-named series entries:
- `AGEO` (series_id: `american_gold_eagle_1oz`) — 0 issues
- `ASEA` (series_id: `american_silver_eagle_1oz`) — 0 issues
- `AGBF` (series_id: not yet created) — Gold Buffalo target

The corrupted entries (`AGE(`, `ASE(`) cannot be simply renamed — they must be **merged**:
1. Re-point the issue's `series_id` FK to the existing correct series_id
2. Rename the `issue_id` (e.g., `US-AGE(-XXXX-X` → `US-AGEO-XXXX-X`)
3. Delete the corrupted `series_registry` row

Similarly, `AME` (American Gold Buffalo) should merge into the `american_gold_buffalo_1oz` series and rename to `AGBF`.

### Canadian Abbreviation Assignments (Decision Required)

These need new 4-character abbreviations. Proposed values (must not collide with existing):

| Corrupted | Series Name | Proposed | Rationale |
|---|---|---|---|
| `$10` | $10 Gold (CA, 1912-1914) | `TGLD` | Ten-dollar Gold |
| `$5 ` | $5 Gold (CA, 1912-1914) | `FGLD` | Five-dollar Gold |
| `10 ` | 10 Cents Steel (CA, 2000-2024) | `DIMS` | Dime Steel |
| `25 ` | 25 Cents Steel (CA, 2000-2024) | `QRTS` | Quarter Steel |
| `5 C` | 5 Cents Nickel (CA, 1968-1999) | `NICK` | Nickel |
| `5 C1` | 5 Cents Steel (CA, 2000-2024) | `NICS` | Nickel Steel |
| `50 ` | 50 Cents Steel (CA, 2000-2020) | `HLFS` | Half-dollar Steel |

### Gold Maple Leaf: NOT Duplicates — Leave Separate

SpecFlow analysis revealed these are **distinct products**, not duplicates:
- `GML` = 1 oz Gold Maple Leaf (46 issues, 31.1g) — valid, keep
- `GOL` = 100kg Big Maple Leaf (1 issue, 100,000g) — unique product, keep but rename to `BGML`
- `GOL1`-`GOL4` = fractional sizes (1/10, 1/4, 1/2, 1/20 oz) — keep but rename to proper 4-char codes
- `GMLO` = dead entry (0 issues) — delete

Proposed GML renames:

| Current | Proposed | Product |
|---|---|---|
| `GML` | `GML` (keep) | 1 oz Gold Maple Leaf |
| `GOL` | `BGML` | Big Maple Leaf (100kg) |
| `GOL1` | `GMT` | Gold Maple Leaf 1/10 oz |
| `GOL2` | `GMH` | Gold Maple Leaf 1/2 oz |
| `GOL3` | `GMT2` | Gold Maple Leaf 1/20 oz |
| `GOL4` | `GMQ` | Gold Maple Leaf 1/4 oz |
| `GMLO` | (delete) | Dead entry, 0 issues |

### 99 FK Violations — Out of Scope

The 99 FK violations (Engelhard bars, Mexican Libertad variants, Silver Three-Cent types) are a **separate problem** requiring new `series_registry` entries to be authored. This should be a child issue, not part of this fix.

### Transaction Safety

The migration must:
1. Create a backup of `coins.db` before any changes
2. Run with `PRAGMA foreign_keys = OFF` during the migration
3. Execute all changes in a single transaction
4. Re-enable FK checks and run `PRAGMA foreign_key_check` after
5. Roll back on any error

### Validator Pattern Fix

`scripts/utils/taxonomy_validator.py` line 44 has `SERIES_CODE_PATTERN = re.compile(r"^[A-Z0-9]{4}$")`. This must change to `{2,4}` to match the CLAUDE.md spec ("2-4 uppercase letters"). Without this fix, wiring the validator into pre-commit would reject 476 valid 3-character issue_ids.

## System-Wide Impact

- **Interaction graph**: Migration script → SQLite DB → export_from_database.py → JSON files → docs folder. Pre-commit hook runs export automatically on commit.
- **Error propagation**: If migration fails mid-transaction, `conn.rollback()` restores DB. If export fails after migration, DB is already committed but JSON is stale (re-run export).
- **State lifecycle risks**: Partial migration could leave issue_ids renamed but series_abbreviation unchanged (or vice versa). Single transaction prevents this.
- **API surface parity**: Downstream consumers (`silv-scraper`, `coindex-backend`) read exported JSON. The `issue_id` field in `ca_issues.json` and `us_issues.json` will change for affected records. These consumers do a full resync from taxonomy, so renamed IDs will be picked up on next sync.
- **Integration test scenarios**: (1) Export after migration produces valid JSON with no corrupted IDs, (2) TaxonomyValidator accepts all post-migration abbreviations, (3) No new FK violations introduced.

## Acceptance Criteria

- [x] All `series_abbreviation` values match `^[A-Z0-9]{2,4}$` pattern
- [x] All `issue_id` values in `issues` table match `COUNTRY-TYPE-YEAR-MINT` format (TYPE = 2-4 uppercase alphanumeric)
- [x] No series_registry rows with full-name abbreviations or 0-issue dead entries remain
- [x] `AGEO`, `ASEA`, `AGBF` merges complete — corrupted source rows deleted
- [x] Gold Maple Leaf entries properly renamed (not merged — they are distinct products)
- [x] `export_from_database.py` runs successfully after migration
- [x] `TaxonomyValidator.SERIES_CODE_PATTERN` updated to `{2,4}`
- [x] Migration script creates backup before running
- [x] All changes in single transaction with rollback on error
- [x] Canadian abbreviation assignments confirmed (see table above)

## Success Metrics

- Zero corrupted abbreviations in `series_registry` (currently 9 corrupted + 2 full-name)
- Zero issue_ids with special characters or spaces (currently 120)
- `PRAGMA foreign_key_check` returns same or fewer violations than before (99 FK violations are out of scope but must not increase)

## Dependencies & Risks

**Dependencies:**
- Confirmation of Canadian abbreviation assignments (table above)
- No concurrent changes to `series_registry` or `issues` table

**Risks:**
- **Downstream orphaned references**: If `silv-scraper` or `coindex-backend` cache old issue_ids, they'll have stale references until next sync. Mitigated by full-resync behavior.
- **Abbreviation collisions**: Proposed new codes must not collide with existing. Migration script should check uniqueness before applying.
- **Pre-commit hook breakage**: If validator is wired in before pattern is relaxed, all commits will fail. Fix pattern first.

## Implementation Files

### New files
- `scripts/fix_corrupted_abbreviations.py` — migration script (follow `scripts/fix_corrupted_varieties.py` pattern)

### Modified files
- `database/coins.db` — source of truth, updated by migration
- `scripts/utils/taxonomy_validator.py:44` — relax `SERIES_CODE_PATTERN` to `{2,4}`
- `data/universal/series_registry.json` — regenerated by export
- `data/universal/ca_issues.json` — regenerated (renamed issue_ids)
- `data/universal/us_issues.json` — regenerated (renamed issue_ids)
- `docs/data/universal/*` — regenerated copies

### Reference files
- `scripts/fix_corrupted_varieties.py` — backup/query/fix/commit pattern
- `scripts/fix_coin_id_format.py` — PK rename pattern
- `scripts/add_silver_eagles_and_gold_buffalos.py` — correct ASEA/AGBF abbreviations
- `scripts/add_gold_eagle_series.py` — correct AGEO abbreviation

## Open Questions

1. **Canadian abbreviation assignments** — Are the proposed codes (`TGLD`, `FGLD`, `DIMS`, `QRTS`, `NICK`, `NICS`, `HLFS`) acceptable? Or should they follow a different convention?
2. **Gold Maple Leaf fractional codes** — Are `GMT`, `GMH`, `GMT2`, `GMQ` clear enough, or should they use a weight-suffix pattern like `GML1`, `GML2`, `GML4`, `GML5`?
3. **Should a child issue be opened for the 99 FK violations?** These are a distinct problem (missing series_registry entries for Engelhard, Libertad, etc.)

## Sources & References

- Related issue: [#129](https://github.com/mattsilv/coin-taxonomy/issues/129)
- Root cause: `scripts/migrate_to_universal_v1_1.py:340-368` (`generate_unique_series_abbreviation()`)
- Correct abbreviations: `scripts/add_silver_eagles_and_gold_buffalos.py`, `scripts/add_gold_eagle_series.py`
- Fix pattern: `scripts/fix_corrupted_varieties.py`, `scripts/fix_coin_id_format.py`
- Validator: `scripts/utils/taxonomy_validator.py:44`
- Coin ID format spec: `docs/taxonomy-id-format.md`
