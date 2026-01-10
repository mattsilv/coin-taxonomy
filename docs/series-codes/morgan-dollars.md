# Morgan Dollar Series Codes

**SYNCED FROM**: coin-taxonomy database
**Last Updated**: 2025-01-10

## Series Code

| Code | Official Name | Years |
|------|---------------|-------|
| MORG | Morgan Dollar | 1878-1921, 2021-present |

## Taxonomy ID Format

```
US-MORG-{YEAR}-{MINT}[-{VARIETY}]
```

### Examples
```
US-MORG-1879-CC    # 1879 Carson City
US-MORG-1893-S     # 1893 San Francisco (key date)
US-MORG-1921-P     # 1921 Philadelphia
US-MORG-2021-P     # 2021 Centennial reissue
```

## Mint Marks

| Mint | Mark | Years Active |
|------|------|--------------|
| Philadelphia | P | 1878-1904, 1921, 2021-present |
| San Francisco | S | 1878-1904, 1921, 2021-present |
| Carson City | C | 1878-1893 |
| New Orleans | O | 1879-1904 |
| Denver | D | 1921, 2021-present |

**Note**: In taxonomy IDs, Carson City uses single letter `C` (normalized from `CC`).

## Variety Suffixes

| Suffix | Description | Example |
|--------|-------------|---------|
| 8TF | 8 Tail Feathers | US-MORG-1878-P-8TF |
| 7TF | 7 Tail Feathers | US-MORG-1878-P-7TF |
| 7O8 | 7 over 8 Tail Feathers | US-MORG-1878-P-7O8 |
| VAM | Specific VAM variety | US-MORG-1878-P-VAM1 |

## Key Dates

| Coin ID | Rarity | Notes |
|---------|--------|-------|
| US-MORG-1893-S | key | Lowest mintage (100,000) |
| US-MORG-1889-C | key | Low CC mintage |
| US-MORG-1879-C | semi-key | Popular CC date |
| US-MORG-1895-P | key | Proof only |

## Query Patterns

```sql
-- All Morgan Dollars
SELECT * FROM coins WHERE coin_id LIKE 'US-MORG-%'

-- All Carson City Morgans
SELECT * FROM coins WHERE coin_id LIKE 'US-MORG-%-C'

-- All 8 Tail Feather varieties
SELECT * FROM coins WHERE coin_id LIKE 'US-MORG-%-8TF'
```

## Related Documentation

- [Taxonomy ID Format](../taxonomy-id-format.md)
- [Source of Truth](../SOURCE_OF_TRUTH.md)
