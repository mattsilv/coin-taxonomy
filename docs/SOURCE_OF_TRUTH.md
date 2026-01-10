# coin-taxonomy: Canonical Source of Truth

This document establishes `coin-taxonomy` as the canonical source of truth for all taxonomy definitions across the coin ecosystem.

## What This Repo Owns

### Taxonomy ID Format Specification
- **Format**: `{COUNTRY}-{SERIES}-{YEAR}-{MINT}[-{VARIETY}]`
- **Examples**: `US-WCOL-1892-P`, `US-MORG-1879-CC`, `MX-MLSO-2024-X`
- See [taxonomy-id-format.md](./taxonomy-id-format.md) for complete specification

### Series Codes
All 4-letter series codes are defined here:
- [Commemorative Half Dollars](./series-codes/commemorative-half-dollars.md) - 48 codes
- [Morgan Dollars](./series-codes/morgan-dollars.md) - MORG code + varieties
- [American Eagles](./series-codes/american-eagles.md) - AGE/ASE patterns
- [Libertads](./series-codes/libertads.md) - ML{metal}{size} pattern

### Valid Enum Values
- **Grading Services**: PCGS, NGC, ANACS, ICG, CAC
- **Mint Marks**: P, D, S, W, CC, O, C (US); Mo (Mexico)
- **Rarity Classifications**: key, semi-key, common, scarce

### Validation Rules
- Coin ID format constraints (CHECK constraint in database)
- 4-letter uppercase series codes
- Year format (4 digits or 'XXXX' for bullion)

## Consumer Repositories

### coindex-backend
- **Syncs**: Series codes to `commemorative-master-list.ts`
- **Uses**: Taxonomy IDs for coin identification
- **Pattern**: `LIKE 'US-{CODE}-%'` for year-agnostic queries

### silv-scraper
- **Uses**: Series codes for `detected_taxonomy_id` field
- **Syncs**: Codes at Bronze tier for raw scraped data

### u2-server
- **References**: Taxonomy for scraper integration
- **Uses**: Codes for priority scoring

### coindex-frontend
- **Consumes**: Backend API (indirect consumer)
- **Uses**: Taxonomy IDs for tracker queries

## How to Update Taxonomy

### Adding New Series
1. Create migration script in `scripts/` (e.g., `add_new_series.py`)
2. Add to SQLite database (source of truth)
3. Run `uv run python scripts/export_from_database.py`
4. Update series-codes documentation
5. Create PR with updated JSON exports

### Syncing to Consumer Repos
After merging taxonomy changes:
1. Create linked issues in consumer repos
2. Update with `SYNCED FROM` comments:
```typescript
/**
 * SYNCED FROM: https://github.com/mattsilv/coin-taxonomy/blob/main/...
 * DO NOT manually edit. Update coin-taxonomy first.
 * Last synced: YYYY-MM-DD
 */
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        coin-taxonomy                            │
│              CANONICAL SOURCE OF TRUTH FOR DEFINITIONS          │
│  - Series codes (WCOL, TXCN, MORG, MLSO...)                    │
│  - Taxonomy ID format specification                             │
│  - Valid enum values (grading services, mints)                  │
└─────────────────────────────────────────────────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
  │ silv-scraper  │    │coindex-backend│    │   u2-server   │
  │               │    │               │    │               │
  │ OWNS:         │    │ OWNS:         │    │ OWNS:         │
  │ - Bronze tier │───▶│ - Parsing     │    │ - Crawling    │
  │ - Raw storage │    │ - ORM/D1      │    │ - Approval    │
  │ - detected_   │    │ - API         │    │ - Priority    │
  │   taxonomy_id │    │ - Discovery   │    │   scoring     │
  └───────────────┘    └───────────────┘    └───────────────┘
                                │
                                ▼
                      ┌───────────────┐
                      │coindex-frontend│
                      │               │
                      │ OWNS:         │
                      │ - UI/UX       │
                      │ - Client state│
                      └───────────────┘
```

## Related Issues

- [#84](https://github.com/mattsilv/coin-taxonomy/issues/84) - Add 51 series codes
- [#85](https://github.com/mattsilv/coin-taxonomy/issues/85) - Taxonomy docs + tests
- [#86](https://github.com/mattsilv/coin-taxonomy/issues/86) - Source of truth docs (this document)
