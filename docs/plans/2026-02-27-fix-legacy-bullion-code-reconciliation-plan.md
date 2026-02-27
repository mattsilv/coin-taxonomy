---
title: "Fix Legacy Bullion Code Reconciliation"
type: fix
status: active
date: 2026-02-27
issue: "#133"
---

# Fix Legacy Bullion Code Reconciliation

## Overview

The dealer prices pipeline (u2-server) and coindex frontend use bullion series codes that predate the coin-taxonomy weight suffix convention. Two urgent collisions were already fixed (GMLS->GMLE, MLST->MLSF). This plan addresses the remaining misaligned codes using Option C (Hybrid): grandfather harmless legacy codes, fix the three misleading American Gold Eagle codes whose suffixes actively conflict with convention meaning.

## Problem Statement

Three American Gold Eagle abbreviations use suffix letters that mean something **different** in the weight convention:

| Current | Should Be | Product | Problem |
|---------|-----------|---------|---------|
| AGEF | AGEH | Gold Eagle 1/2 oz | F = 1/20oz in convention |
| AGES | AGET | Gold Eagle 1/10 oz | S has no convention meaning |
| AGET | AGEQ | Gold Eagle 1/4 oz | T = 1/10oz in convention |

These create active confusion — a developer reading `AGEF` would reasonably assume it's the 1/20oz, not the 1/2oz.

## Scope

### In Scope

1. **Rename three Eagle codes**: AGET->AGEQ, AGES->AGET, AGEF->AGEH (in that order)
2. **Clean up corrupted duplicates**: Delete AGE(, AME1, AME2, AME3 entries (leftover from Issue #129)
3. **Populate `aliases` field**: Add old codes as aliases on renamed series for downstream lookup
4. **Update documentation**: Gold Eagle docs, Handoff Primer, Bullion Integration Guide
5. **Coordinate downstream**: Provide alias mappings for u2-server and coindex frontend

### Out of Scope (tracked separately)

- **GML/SML namespace confusion**: GML is actually the Big Maple Leaf (100kg), not the 1oz. GOL2 (the real 1oz) has 45 issue_ids prefixed `CA-GML-`. This is a larger cleanup requiring ~90 issue_id renames — separate issue.
- **MLSD inconsistency**: Libertad Silver 1/10oz uses `D` instead of convention `T`, but `MLST` is already taken by the 1/20oz. No collision, accept as-is.
- **GOL2-GOL7 renaming**: Gold Maple Leaf fractional codes need full reconciliation — separate issue.
- **SIL/SML reconciliation**: Similar namespace confusion to GML — separate issue.

## Technical Approach

### Critical: Circular Rename Problem

AGES cannot be renamed to AGET while AGET already exists (UNIQUE constraint on `series_abbreviation`). **Required order**:

```
Step 1: AGET -> AGEQ  (frees the AGET slot)
Step 2: AGES -> AGET  (takes the freed slot)
Step 3: AGEF -> AGEH  (independent, no conflict)
```

### Tables Affected

The migration must update **three tables** (not just two):

1. **`series_registry`** — `series_abbreviation` column (the rename itself)
2. **`coins`** — `coin_id` primary key embeds the abbreviation (e.g., `US-AGET-XXXX-X`)
3. **`issues`** — `issue_id` primary key embeds the abbreviation; `series_id` foreign key

Additionally: `coin_inventory` has FK to `coins(coin_id)` with ON DELETE CASCADE. Current data shows **no** inventory entries for AGEF/AGES/AGET coin_ids, so no inventory changes needed — but the migration script should verify this.

### Migration Script Design

Following the proven pattern from `scripts/fix_corrupted_abbreviations.py` (Issue #129):

```python
# scripts/reconcile_eagle_codes.py

# 1. Backup database
# 2. PRAGMA foreign_keys = OFF
# 3. BEGIN TRANSACTION
# 4. Pre-flight: verify expected state (current codes exist, targets don't)
# 5. Pre-flight: verify no coin_inventory entries for affected coin_ids
# 6. For each rename (AGET->AGEQ, AGES->AGET, AGEF->AGEH):
#    a. UPDATE series_registry SET series_abbreviation = NEW WHERE series_abbreviation = OLD
#    b. UPDATE coins SET coin_id = REPLACE(coin_id, '-OLD-', '-NEW-') WHERE coin_id LIKE '%-OLD-%'
#    c. UPDATE issues SET issue_id = REPLACE(issue_id, '-OLD-', '-NEW-') WHERE issue_id LIKE '%-OLD-%'
#    d. UPDATE series_registry SET aliases = json_array(OLD) WHERE series_abbreviation = NEW
# 7. Delete corrupted duplicates: AGE(, AME1, AME2, AME3
#    a. Delete from issues WHERE issue_id matches these codes
#    b. Delete from coins WHERE coin_id matches these codes
#    c. Delete from series_registry WHERE series_abbreviation IN ('AGE(', 'AME1', 'AME2', 'AME3')
# 8. COMMIT
# 9. PRAGMA foreign_keys = ON
# 10. Verify: query all three tables to confirm renames
```

### Validation Steps

After migration:
1. Run `uv run python scripts/export_from_database.py` (handles full 3-step pipeline)
2. Verify `data/universal/series_registry.json` contains AGEH, AGET (1/10oz), AGEQ
3. Verify no JSON files reference old AGEF/AGES codes
4. Pre-commit hooks must pass (export + validate + integrity check)

## Acceptance Criteria

- [x] `series_registry` has AGEH (1/2oz), AGET (1/10oz), AGEQ (1/4oz) — no AGEF, AGES, old-AGET
- [x] `coins` table coin_ids updated: `US-AGEH-XXXX-X`, `US-AGET-XXXX-X`, `US-AGEQ-XXXX-X`
- [x] `aliases` field populated: AGEH has `["AGEF"]`, AGET has `["AGES"]`, AGEQ has `["AGET"]`
- [x] Corrupted entries deleted: AGE(, AME1, AME2, AME3 removed from all tables
- [x] `export_from_database.py` succeeds with no errors
- [ ] Pre-commit hooks pass
- [x] `docs/series-codes/american-eagles.md` updated with new codes
- [x] `docs/BULLION_INTEGRATION_GUIDE.md` updated with new codes
- [x] `docs/handoffs/GOLD_EAGLE_HANDOFF_PRIMER.md` updated or deprecated
- [x] Migration script is idempotent (safe to run twice)

## Implementation Phases

### Phase 1: Migration Script (`scripts/reconcile_eagle_codes.py`)

1. Write migration script following the pattern above
2. Include dry-run mode (`--dry-run` flag) that prints changes without committing
3. Include pre-flight checks that abort if unexpected state is found
4. Include post-flight verification queries

### Phase 2: Run Migration + Export

1. Run migration script: `uv run python scripts/reconcile_eagle_codes.py`
2. Run export: `uv run python scripts/export_from_database.py`
3. Verify all JSON exports
4. Run pre-commit validation manually

### Phase 3: Documentation Updates

Update these files with new codes:
- `docs/series-codes/american-eagles.md` — code table and examples
- `docs/BULLION_INTEGRATION_GUIDE.md` — any Eagle code references
- `docs/handoffs/GOLD_EAGLE_HANDOFF_PRIMER.md` — SQL examples, code references

### Phase 4: Commit + PR

1. Create branch: `git checkout -b fix/legacy-eagle-code-reconciliation-133`
2. Commit database + generated files + docs + migration script
3. Create PR referencing Issue #133

### Phase 5: Downstream Coordination (post-merge)

Provide alias mappings for downstream repos:

**coindex frontend** (TAXONOMY_META aliases):
```
AGEF -> AGEH  (Gold Eagle 1/2 oz)
AGES -> AGET  (Gold Eagle 1/10 oz)
AGET -> AGEQ  (Gold Eagle 1/4 oz)
```

**u2-server** (`bullion_taxonomy.py` / `taxonomy_map.py`):
- Update emitted codes from AGEF/AGES/AGET to AGEH/AGET/AGEQ

Rollout order:
1. Merge this PR (coin-taxonomy)
2. Add aliases in coindex frontend
3. Update u2-server to emit new codes
4. Remove old aliases from frontend (cleanup)

## Dependencies & Risks

| Risk | Mitigation |
|------|------------|
| Circular rename fails mid-transaction | Single transaction with rollback; backup created first |
| Downstream breaks during transition | Frontend alias support allows both old and new codes |
| coin_inventory FK cascade | Pre-flight query confirms no affected inventory rows |
| Pre-commit hook runs export twice | Export is idempotent — double-run is safe, just slow |
| UNIQUE constraint violation | Ordered renames (AGET->AGEQ first) prevent conflicts |

## Follow-Up Issues to File

After this PR merges, file separate issues for:
1. **GML/GOL2 namespace reconciliation** — 45 issue_ids use `CA-GML-` prefix but belong to GOL2 series
2. **GOL2-GOL7 fractional Maple Leaf code standardization** — rename to GMLO/GMLH/GMLQ/GMLE/GMLF
3. **SIL/SML Silver Maple Leaf reconciliation** — similar namespace confusion
4. **Remaining corrupted abbreviations** — AGB(, APE(, ASE( still in database

## Sources

- Related issue: #133
- Previous migration pattern: `scripts/fix_corrupted_abbreviations.py` (Issue #129)
- Institutional learnings: `docs/solutions/database-issues/corrupted-series-abbreviations-migration.md`
- Bullion integration guide: `docs/BULLION_INTEGRATION_GUIDE.md`
- Eagle code definitions: `docs/series-codes/american-eagles.md`
- Handoff primer: `docs/handoffs/GOLD_EAGLE_HANDOFF_PRIMER.md`
