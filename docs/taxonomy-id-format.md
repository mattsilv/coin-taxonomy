# Taxonomy ID Format Specification

This document defines the canonical format for coin taxonomy IDs used across all repositories.

## Format

```
{COUNTRY}-{SERIES}-{YEAR}-{MINT}[-{VARIETY}]
```

### Components

| Component | Format | Required | Description |
|-----------|--------|----------|-------------|
| COUNTRY | 2-3 uppercase letters | Yes | ISO country code (US, CA, MX, GB) |
| SERIES | 4 uppercase letters | Yes | Series abbreviation code |
| YEAR | 4 digits or XXXX | Yes | Mint year (XXXX for random year bullion) |
| MINT | 1-2 uppercase letters | Yes | Mint mark |
| VARIETY | 1-4 alphanumeric | No | Variety suffix for significant variants |

### Examples

```
US-WCOL-1892-P      # World's Columbian Exposition, 1892, Philadelphia
US-MORG-1879-CC     # Morgan Dollar, 1879, Carson City
US-ASEA-2024-W      # American Silver Eagle, 2024, West Point
MX-MLSO-2023-M      # Mexican Libertad 1oz Silver, 2023, Mexico City
US-GRNT-1922-P-STAR # Grant Memorial with Star variety
US-AGEO-XXXX-X      # American Gold Eagle 1oz, random year (bullion)
```

## Validation Rules

### Database Constraint
```sql
CONSTRAINT valid_coin_id_format CHECK (
    coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
    coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
    coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-XXXX-[A-Z]*' OR
    coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-XXXX-[A-Z]*'
)
```

### Rules
1. **Exactly 4 parts** (or 5 with variety suffix) separated by dashes
2. **Country code**: 2-3 uppercase letters (ISO standard)
3. **Series code**: Exactly 4 uppercase letters
4. **Year**: 4-digit year (1773-9999) OR literal `XXXX` for bullion
5. **Mint mark**: 1-2 uppercase letters

## Year-Agnostic Queries

For searching across all years of a series, use SQL LIKE patterns:

```sql
-- Find all Morgan Dollars
SELECT * FROM coins WHERE coin_id LIKE 'US-MORG-%'

-- Find all Texas Centennial commemoratives
SELECT * FROM coins WHERE coin_id LIKE 'US-TXCN-%'

-- Find all Mexican Libertad 1oz silver
SELECT * FROM coins WHERE coin_id LIKE 'MX-MLSO-%'
```

### Pattern Format
```
{COUNTRY}-{SERIES}-%
```

## Mint Mark Normalization

| Raw Input | Normalized | Meaning |
|-----------|------------|---------|
| (blank) | P or X | Philadelphia (US) or unspecified |
| P | P | Philadelphia |
| D | D | Denver |
| S | S | San Francisco |
| W | W | West Point |
| CC | C | Carson City (single letter in ID) |
| O | O | New Orleans |
| Mo | M | Mexico City |

**Note**: For bullion with unspecified mint, use `X`.

## Variety Suffix Rules

Variety suffixes are **optional** and only used for significant design variants that affect collector value.

### When to Use
- Major die varieties (8TF, 7TF, VDB)
- Design type changes (T1, T2, T3)
- Commemorative variants (STAR, 2X2, 2S4)
- Weight variants for bullion (110oz, 14oz)

### Suffix Format
- 1-4 uppercase alphanumeric characters
- Appended with additional dash: `US-GRNT-1922-P-STAR`

### Examples

| Full ID | Series | Variety |
|---------|--------|---------|
| `US-GRNT-1922-P-STAR` | Grant Memorial | With Star |
| `US-ALCN-1921-P-2X2` | Alabama Centennial | 2X2 variety |
| `US-MOGD-1878-P-8TF` | Morgan Dollar | 8 Tail Feathers |
| `US-TCST-1851-P-T1` | Three-Cent Silver | Type I |

## Series Code Registry

See [series-codes/](./series-codes/) for complete code listings by coin type:

- [commemorative-half-dollars.md](./series-codes/commemorative-half-dollars.md)
- [morgan-dollars.md](./series-codes/morgan-dollars.md)
- [american-eagles.md](./series-codes/american-eagles.md)
- [libertads.md](./series-codes/libertads.md)

## Usage in Consumer Repos

### coindex-backend
```typescript
// Generate taxonomy ID
const taxonomyId = `US-${seriesCode}-${year}-${mint}`;

// Year-agnostic search
const pattern = `US-${seriesCode}-%`;
const coins = await db.query(`SELECT * FROM coins WHERE taxonomy_id LIKE ?`, [pattern]);
```

### silv-scraper
```python
# Detect taxonomy from listing
detected_taxonomy_id = f"US-{series_code}-{year}-{mint}"
```

## Validation Tests

```javascript
describe('Taxonomy ID Validation', () => {
  it('accepts valid format: US-WCOL-1892-P', () => {
    expect(isValidTaxonomyId('US-WCOL-1892-P')).toBe(true);
  });

  it('rejects missing country: WCOL-1892-P', () => {
    expect(isValidTaxonomyId('WCOL-1892-P')).toBe(false);
  });

  it('accepts XXXX year for bullion: US-AGEO-XXXX-X', () => {
    expect(isValidTaxonomyId('US-AGEO-XXXX-X')).toBe(true);
  });

  it('accepts variety suffix: US-GRNT-1922-P-STAR', () => {
    expect(isValidTaxonomyId('US-GRNT-1922-P-STAR')).toBe(true);
  });
});
```
