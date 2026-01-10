# American Eagle Series Codes

**SYNCED FROM**: coin-taxonomy database
**Last Updated**: 2025-01-10

## Series Codes

### Gold Eagles

| Code | Official Name | Metal | Size |
|------|---------------|-------|------|
| AGEO | American Gold Eagle 1 oz | Gold | 1 oz |
| AGEH | American Gold Eagle 1/2 oz | Gold | 1/2 oz |
| AGEQ | American Gold Eagle 1/4 oz | Gold | 1/4 oz |
| AGET | American Gold Eagle 1/10 oz | Gold | 1/10 oz |

### Silver Eagles

| Code | Official Name | Metal | Size |
|------|---------------|-------|------|
| ASEA | American Silver Eagle 1 oz | Silver | 1 oz |

### Platinum Eagles

| Code | Official Name | Metal | Size |
|------|---------------|-------|------|
| APEA | American Platinum Eagle 1 oz | Platinum | 1 oz |
| APEH | American Platinum Eagle 1/2 oz | Platinum | 1/2 oz |
| APEQ | American Platinum Eagle 1/4 oz | Platinum | 1/4 oz |
| APET | American Platinum Eagle 1/10 oz | Platinum | 1/10 oz |

## Taxonomy ID Format

```
US-{CODE}-{YEAR}-{MINT}
```

### Examples
```
US-AGEO-2024-W     # 2024 Gold Eagle 1oz, West Point
US-ASEA-2024-P     # 2024 Silver Eagle 1oz, Philadelphia
US-AGEO-XXXX-X     # Random year Gold Eagle (bullion)
```

## Mint Marks

| Mint | Mark | Notes |
|------|------|-------|
| Philadelphia | P | Uncirculated/Burnished |
| West Point | W | Proofs and special editions |
| San Francisco | S | Proofs |

## Random Year Pattern

For bullion sold as "random year" or "dealer's choice":

```
US-AGEO-XXXX-X     # Random year, unspecified mint
US-ASEA-XXXX-X     # Random year Silver Eagle
```

**Use Case**: Bullion products valued by metal content only, where specific year doesn't affect premium.

## Query Patterns

```sql
-- All American Gold Eagles
SELECT * FROM coins WHERE coin_id LIKE 'US-AGE%'

-- All American Silver Eagles
SELECT * FROM coins WHERE coin_id LIKE 'US-ASEA-%'

-- All 1oz Gold Eagles
SELECT * FROM coins WHERE coin_id LIKE 'US-AGEO-%'

-- All random year bullion
SELECT * FROM coins WHERE coin_id LIKE '%-XXXX-%'
```

## Type Designations

| Year Range | Type | Notes |
|------------|------|-------|
| 1986-2021 | Type I | Original design |
| 2021-present | Type II | Reverse redesign |

For type-specific queries:
```sql
-- Type I Silver Eagles (original design)
SELECT * FROM coins
WHERE coin_id LIKE 'US-ASEA-%'
  AND year BETWEEN 1986 AND 2020

-- Type II Silver Eagles
SELECT * FROM coins
WHERE coin_id LIKE 'US-ASEA-%'
  AND year >= 2021
```

## Related Documentation

- [Taxonomy ID Format](../taxonomy-id-format.md)
- [Libertads](./libertads.md) - Similar bullion pattern
