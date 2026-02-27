---
date: 2026-02-27
topic: bullion-weight-suffix-standard
---

# Bullion Weight Suffix Standard

## What We're Building

A single, universal convention for encoding bullion weights in taxonomy IDs. Today we have three competing patterns. We need one standard that works for every sovereign mint coin and private bar worldwide.

## Current State: Three Competing Conventions

### Convention A: Separate series per weight (US Eagles, Libertad)

Each weight gets its own 4-letter series abbreviation with the last letter encoding weight:

| Code | Product | Weight Letter |
|------|---------|---------------|
| `AGEO` | Gold Eagle 1oz | O=1oz |
| `AGEH` | Gold Eagle 1/2oz | H=1/2oz |
| `AGEQ` | Gold Eagle 1/4oz | Q=1/4oz |
| `AGET` | Gold Eagle 1/10oz | T=1/10oz |
| `MLSO` | Libertad Silver 1oz | O=1oz |
| `MLSH` | Libertad Silver 1/2oz | H=1/2oz |
| `MLSD` | Libertad Silver 1/10oz | D=1/10oz |
| `MLST` | Libertad Silver 1/20oz | T=1/20oz |

**Problem**: T=1/10oz (Eagle) vs T=1/20oz (Libertad). Letters run out for sizes >1oz. Already have duplicates (MLS1 vs MLSD).

### Convention B: Weight suffix on coin_id (Maple Leaf, Krugerrand, Britannia #135)

One base series code, weight as 5th part of coin_id:

```
CA-GMPL-1982-P-14oz    → Maple Leaf 1/4oz
ZA-KRGR-XXXX-X-12oz    → Krugerrand 1/2oz
GB-BGBO-XXXX-RM-14oz   → Britannia Gold 1/4oz
GB-BSBO-XXXX-RM-10oz   → Britannia Silver 10oz
```

**Already working** for Maple Leaf (214 year-specific entries with suffixes), Krugerrand, and Britannia.

### Convention C: Hybrid (Britannia legacy)

BGBO=1oz (O suffix) AND BGBT=1/10oz (separate code), but BGBO also has `-14oz` and `-12oz` suffixes. Inconsistent.

## Chosen Approach: Weight Suffixes Only

**Decision: Convention B is the standard going forward.**

### The Standard

1. **One series code per product line + metal** — the base code represents the product line, NOT a specific weight
2. **No suffix = 1oz** (the default/most traded size)
3. **Weight suffix = 5th part of coin_id** for all other sizes
4. **`variety_suffixes`** on series_registry documents valid suffixes

### Weight Suffix Reference

| Suffix | Weight | Example |
|--------|--------|---------|
| *(none)* | 1 oz | `US-AGEO-XXXX-X` |
| `120oz` | 1/20 oz | `MX-MLSO-XXXX-MO-120oz` |
| `110oz` | 1/10 oz | `US-AGEO-XXXX-X-110oz` |
| `14oz` | 1/4 oz | `US-AGEO-XXXX-X-14oz` |
| `12oz` | 1/2 oz | `US-AGEO-XXXX-X-12oz` |
| `2oz` | 2 oz | `GB-BSBO-XXXX-RM-2oz` |
| `5oz` | 5 oz | `MX-MLSO-XXXX-MO-5oz` |
| `10oz` | 10 oz | `GB-BSBO-XXXX-RM-10oz` |
| `100oz` | 100 oz | `XX-G100-XXXX-X` *(stays as-is, single product)* |
| `1kg` | 1 kilogram | `MX-MLSO-XXXX-MO-1kg` |

### Validation Against World Bullion

| Product Line | Base Code | Country | Suffixes Needed | Status |
|-------------|-----------|---------|-----------------|--------|
| **American Gold Eagle** | `AGEO` | US | 12oz, 14oz, 110oz | Migrate: deprecate AGEH/AGEQ/AGET |
| **American Silver Eagle** | `ASEA` | US | *(1oz only)* | Already correct |
| **American Gold Buffalo** | `AGBF` | US | *(1oz only)* | Already correct |
| **American Platinum Eagle** | `APEO` | US | 12oz, 14oz, 110oz *(if added)* | Already correct for 1oz |
| **Gold Maple Leaf** | `GMPL` | CA | 110oz, 14oz, 12oz | Already uses suffixes (214 entries) |
| **Silver Maple Leaf** | `SMLO` | CA | *(1oz only currently)* | Already correct |
| **Libertad Silver** | `MLSO` | MX | 120oz, 110oz, 14oz, 12oz, 2oz, 5oz, 1kg | Migrate: deprecate MLSH/MLSQ/MLSD/MLST/MLSW/MLSF/MLSK |
| **Libertad Gold** | `MLGO` | MX | 120oz, 110oz, 14oz, 12oz | Migrate: deprecate MLGH/MLGQ/MLGD/MLGT |
| **Libertad Platinum** | `MLPO` | MX | *(1oz only)* | Already correct |
| **Britannia Gold** | `BGBO` | GB | 110oz, 14oz, 12oz | Partially done (14oz, 12oz). Deprecate BGBT |
| **Britannia Silver** | `BSBO` | GB | 2oz, 10oz | Already done (#135) |
| **Krugerrand Gold** | `KRGR` | ZA | 1oz, 12oz, 14oz, 110oz | Already uses variety_suffixes |
| **Krugerrand Silver** | `KRGS` | ZA | *(1oz only)* | Already correct |
| **Austrian Philharmonic Gold** | `PHGO`* | AT | 110oz, 14oz, 12oz | Not yet in DB |
| **Austrian Philharmonic Silver** | `PHSO`* | AT | *(1oz, 1.5 EUR planned)* | Not yet in DB |
| **Chinese Panda Gold** | `PNDG`* | CN | 1g, 3g, 8g, 15g, 30g | Not yet in DB — gram weights: `1g`, `3g`, `8g`, `15g`, `30g` |
| **Chinese Panda Silver** | `PAND` | CN | 30g *(base)* | Already in DB (30g base) |
| **Perth Kangaroo Gold** | `KANG`* | AU | 110oz, 14oz, 12oz | Not yet in DB |
| **Perth Kangaroo Silver** | `ROOS` | AU | *(1oz)* | Already in DB |
| **Perth Lunar Series** | `LUNR` | AU | 12oz, 2oz, 5oz, 10oz, 1kg | Already in DB (1oz base) |

*\* = proposed codes for future series*

### Edge Cases Resolved

1. **Gram-denominated products** (Chinese Panda): Use `1g`, `3g`, `8g`, `15g`, `30g` as suffixes. Same pattern, different unit.

2. **Products that only exist in one weight** (Silver Eagle, Gold Buffalo): No suffix needed. The base code IS the product.

3. **Generic bars/rounds**: Keep current codes (GSB1, GSB5, GS10, G100) — each is a distinct product, not a size variant of one series.

4. **Queen's Beasts 2oz** (`QBST`): This is a 2oz-only product line. No suffix needed — base weight IS 2oz. Document in series_registry.

5. **America the Beautiful 5oz** (`ATB5`): Same — 5oz-only product line. No suffix.

## Migration Scope

### Phase 1: Fix Libertad (highest inconsistency)

- **12 XXXX entries to remap** (MLSD→MLSO-110oz, MLST→MLSO-120oz, etc.)
- **54 year-specific MLSO entries**: already correct (base code)
- **51 year-specific MLGO entries**: already correct (base code)
- **0 year-specific fractional entries**: only XXXX exists for fractionals
- **Fix type**: `coin` → `bullion` on all Libertad series
- **Fix denominations**: replace product name with real denomination
- **Remove duplicates**: delete MLS1, MLG1 (dupes of MLSD, MLGD)
- **Add missing XXXX**: `MX-MLSO-XXXX-MO` (Silver 1oz), `MX-MLGO-XXXX-MO` (Gold 1oz)

### Phase 2: Fix US Eagles

- **4 XXXX entries to remap**: AGEH→AGEO-12oz, AGEQ→AGEO-14oz, AGET→AGEO-110oz
- **0 year-specific entries** for fractionals — only XXXX exists
- Deprecate AGEH, AGEQ, AGET series codes

### Phase 3: Fix Britannia legacy

- **1 XXXX entry to remap**: BGBT→BGBO-110oz
- Deprecate BGBT series code
- Update BGBO variety_suffixes to include 110oz

### Downstream Impact

Consumer repos that map taxonomy codes need backfill migrations:

- **u2-server**: price comparison scraper maps dealer listings to taxonomy codes. Old codes (AGEH, MLSH, etc.) stored in listings DB need remapping to new suffix format.
- **coindex-monorepo**: frontend displays bullion products by taxonomy code. Cached/stored codes need updating.

## Key Decisions

- **Base code = 1oz, no suffix**: The most common weight gets the clean ID
- **Weight suffixes are alphanumeric, no dots**: `14oz` not `0.25oz` (already established)
- **Gram suffixes**: `1g`, `3g`, `30g` for products denominated in grams
- **Generic bars keep separate codes**: GSB1/GSB5/GS10/G100 are not weight variants of one series — they're distinct products by size
- **Existing base codes preserved**: AGEO, MLSO, MLGO, BGBO stay as-is. Only the per-weight codes get deprecated.

## Open Questions

- Should we create a formal mapping table (`deprecated_code → new_code_with_suffix`) in the database for downstream consumers to query?
- Timeline for deprecation: hard cutoff or soft transition with both codes valid?

## Next Steps

→ `/workflows:plan` for the migration implementation (Phase 1: Libertad first)
→ Create GitHub issues in u2-server and coindex-monorepo for backfill migrations
