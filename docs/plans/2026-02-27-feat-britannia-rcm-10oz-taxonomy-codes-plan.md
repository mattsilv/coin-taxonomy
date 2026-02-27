---
title: Add taxonomy codes for 10oz coins and expanded Britannia sizes
type: feat
status: completed
date: 2026-02-27
---

# Add taxonomy codes for 10oz coins and expanded Britannia sizes

Add new XXXX random-year bullion entries for Britannia fractionals (gold 1/4oz, 1/2oz; silver 2oz, 10oz) and RCM branded silver bars, using weight suffixes on existing series codes.

## New Coin Entries

### Britannia Silver (existing series: `BSBO`)

| coin_id | Weight | Denomination | Composition | Weight (g) |
|---------|--------|-------------|-------------|------------|
| `GB-BSBO-XXXX-RM-2oz` | 2 oz | 5 Pounds | .999 Ag | 62.207 |
| `GB-BSBO-XXXX-RM-10oz` | 10 oz | 10 Pounds | .999 Ag | 311.035 |

### Britannia Gold (existing series: `BGBO`)

| coin_id | Weight | Denomination | Composition | Weight (g) |
|---------|--------|-------------|-------------|------------|
| `GB-BGBO-XXXX-RM-14oz` | 1/4 oz | 25 Pounds | .9999 Au | 7.776 |
| `GB-BGBO-XXXX-RM-12oz` | 1/2 oz | 50 Pounds | .9999 Au | 15.552 |

### RCM Silver Bar (new series: `RCMB`)

| coin_id | Weight | Denomination | Composition | Weight (g) |
|---------|--------|-------------|-------------|------------|
| `CA-RCMB-XXXX-P-10oz` | 10 oz | Silver Bar | .9999 Ag | 311.035 |

### Royal Mint Silver Bar (new series: `RMSB`)

| coin_id | Weight | Denomination | Composition | Weight (g) |
|---------|--------|-------------|-------------|------------|
| `GB-RMSB-XXXX-RM-10oz` | 10 oz | Silver Bar | .999 Ag | 311.035 |

## Series Registry Changes

### Updates to existing series (add `variety_suffixes`)

```sql
-- BSBO: add 2oz and 10oz suffixes
UPDATE series_registry SET variety_suffixes = '["2oz", "10oz"]'
WHERE series_abbreviation = 'BSBO';

-- BGBO: add 14oz and 12oz suffixes
UPDATE series_registry SET variety_suffixes = '["14oz", "12oz"]'
WHERE series_abbreviation = 'BGBO';
```

### New series entries

| series_id | abbreviation | name | country | type | start_year |
|-----------|-------------|------|---------|------|------------|
| `rcm_silver_bar` | `RCMB` | RCM Silver Bar | CA | bullion | 2000 |
| `royal_mint_silver_bar` | `RMSB` | Royal Mint Silver Bar | GB | bullion | 2010 |

## Acceptance Criteria

- [x] 6 new coin entries inserted into `coins` table (4 Britannia + 1 RCM + 1 Royal Mint)
- [x] 2 new series_registry entries (`RCMB`, `RMSB`) with `variety_suffixes = '["10oz"]'`
- [x] `variety_suffixes` updated on existing `BSBO` and `BGBO` series
- [x] No abbreviation conflicts (verified: `RCMB` and `RMSB` are unused)
- [x] `export_from_database.py` runs successfully with all 7 steps passing
- [x] New entries appear in `data/universal/series_registry.json`
- [ ] Pre-commit hook passes

## Implementation

Single migration script: `scripts/add_britannia_rcm_expansion_issue135.py`

Follow established pattern from `scripts/add_missing_bullion_issue130.py`:
1. Backup database with `shutil.copy2()`
2. Insert new series_registry entries (`RCMB`, `RMSB`)
3. Update `variety_suffixes` on existing `BSBO`, `BGBO` series
4. Insert 6 new coin entries with XXXX year pattern
5. Verify insertions with count query
6. Run `export_from_database.py` to regenerate JSON

## Context

- Issue: #135
- User feedback requesting broader Britannia and 10oz coverage for [dealer prices page](https://coindex.app/tools/dealer-prices/)
- Weight suffix approach matches existing CA Maple Leaf pattern (`CA-GMPL-1982-P-14oz`)
- Downstream consumers: coindex-monorepo frontend, u2-server scraper taxonomy mapping

## Sources

- Template script: `scripts/add_missing_bullion_issue130.py`
- Learnings: `docs/solutions/database-issues/missing-bullion-taxonomy-migration.md`
- Existing GB entries: `GB-BGBO-XXXX-RM`, `GB-BGBT-XXXX-RM`, `GB-BSBO-XXXX-RM`
- Related issue: #135
