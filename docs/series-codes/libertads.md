# Mexican Libertad Series Codes

**SYNCED FROM**: coin-taxonomy database
**Last Updated**: 2025-01-10

## Code Pattern

Libertads use the pattern `ML{METAL}{SIZE}`:

- **ML** = Mexican Libertad prefix
- **METAL** = S (Silver), G (Gold), P (Platinum)
- **SIZE** = O (1oz), H (1/2oz), Q (1/4oz), T (1/10oz), F (1/20oz), W (2oz), V (5oz), K (1kg)

## Silver Libertads

| Code | Size | Weight |
|------|------|--------|
| MLSO | 1 oz | 31.1g |
| MLSH | 1/2 oz | 15.55g |
| MLSQ | 1/4 oz | 7.78g |
| MLST | 1/10 oz | 3.11g |
| MLSF | 1/20 oz | 1.56g |
| MLSW | 2 oz | 62.2g |
| MLSV | 5 oz | 155.5g |
| MLSK | 1 kg | 1000g |

## Gold Libertads

| Code | Size | Weight |
|------|------|--------|
| MLGO | 1 oz | 31.1g |
| MLGH | 1/2 oz | 15.55g |
| MLGQ | 1/4 oz | 7.78g |
| MLGT | 1/10 oz | 3.11g |
| MLGF | 1/20 oz | 1.56g |

## Taxonomy ID Format

```
MX-{CODE}-{YEAR}-{MINT}
```

### Examples
```
MX-MLSO-2024-M     # 2024 Silver Libertad 1oz, Mexico City
MX-MLGO-2023-M     # 2023 Gold Libertad 1oz
MX-MLSV-2024-M     # 2024 Silver Libertad 5oz
MX-MLSO-XXXX-X     # Random year Silver 1oz (bullion)
```

## Mint Marks

| Mint | Mark | Notes |
|------|------|-------|
| Mexico City | M | All Libertads minted here |
| Unspecified | X | Used for random year bullion |

## Type Designations

### Silver Types

| Year Range | Type | Design Notes |
|------------|------|--------------|
| 1982-1995 | Type 1 | Original design, no edge lettering |
| 1996-1999 | Type 2 | Edge lettering added |
| 2000-2018 | Type 3 | New reverse design |
| 2019-present | Type 4 | Updated security features |

### Gold Types

| Year Range | Type |
|------------|------|
| 1981-1999 | Type 1 |
| 2000-2018 | Type 2 |
| 2019-present | Type 3 |

## Query Patterns

```sql
-- All Mexican Libertads
SELECT * FROM coins WHERE coin_id LIKE 'MX-ML%'

-- All Silver Libertads
SELECT * FROM coins WHERE coin_id LIKE 'MX-MLS%'

-- All 1oz Silver Libertads
SELECT * FROM coins WHERE coin_id LIKE 'MX-MLSO-%'

-- All Gold Libertads
SELECT * FROM coins WHERE coin_id LIKE 'MX-MLG%'

-- All fractional silver (not 1oz)
SELECT * FROM coins
WHERE coin_id LIKE 'MX-MLS%'
  AND coin_id NOT LIKE 'MX-MLSO-%'
```

## Related Documentation

- [Taxonomy ID Format](../taxonomy-id-format.md)
- [American Eagles](./american-eagles.md) - Similar bullion pattern
