# Gold Eagle Weight Variations - Backend Engineer Handoff

**Date:** November 7, 2025
**Status:** ✅ Implemented & Deployed
**Commit:** `8e10fa2` - [View on GitHub](https://github.com/mattsilv/coin-taxonomy/commit/8e10fa2)

---

## What We Built

Added 4 American Gold Eagle weight variations to the coin taxonomy with random year (XXXX) support for bullion products.

### New Series Codes

| Series Code | Weight | Denomination | Coin ID | Example Use Case |
|-------------|--------|--------------|---------|-----------------|
| **AGEO** | 1 oz | $50 | `US-AGEO-XXXX-X` | "1 oz Gold Eagle - Random Year" |
| **AGEF** | 1/2 oz | $25 | `US-AGEF-XXXX-X` | "1/2 oz Gold Eagle - Dealer's Choice" |
| **AGET** | 1/4 oz | $10 | `US-AGET-XXXX-X` | "1/4 oz Gold Eagle - Any Year" |
| **AGES** | 1/10 oz | $5 | `US-AGES-XXXX-X` | "1/10 oz Gold Eagle - Mixed Years" |

---

## Why This Matters for Backend

### Problem Solved
Major bullion dealers (eBay, APMEX, JM Bullion) sell Gold Eagles as "random year" at the lowest premium over spot. These are legitimate products that need canonical taxonomy IDs for:
- Price tracking across dealers
- Inventory management (mixed year stock)
- Marketplace comparison
- Uniform product categorization

### Key Distinction

**Numismatic Coins** (year matters):
```javascript
// 1909-S VDB vs 1943 Steel = different values
taxonomy_id: "US-LWC-1909-S"  // Specific year required
valuation: "market_value"      // Condition & year dependent
```

**Bullion Products** (year doesn't matter):
```javascript
// 2010 vs 2024 Gold Eagle = same melt value
taxonomy_id: "US-AGEO-XXXX-X"  // Random year acceptable
valuation: "spot_plus_premium"  // Metal content only
```

---

## Database Schema Changes

### Year Field Migration
```sql
-- BEFORE:
year INTEGER NOT NULL

-- AFTER:
year TEXT NOT NULL CHECK(
    year GLOB '[0-9][0-9][0-9][0-9]' OR
    year = 'XXXX'
)
```

### Coin ID Pattern
```sql
-- BEFORE:
coin_id GLOB '[A-Z][A-Z]-[A-Z]{4}-[0-9]{4}-[A-Z]{1,2}'

-- AFTER (accepts both):
coin_id GLOB '[A-Z][A-Z]-[A-Z]{4}-[0-9]{4}-[A-Z]{1,2}' OR
coin_id GLOB '[A-Z][A-Z]-[A-Z]{4}-XXXX-[A-Z]{1,2}'
```

**Migration:** All 762 existing coins preserved with zero data loss. Numeric years converted from INTEGER to TEXT ("1909" instead of 1909 in database, but exported as integer 1909 in JSON).

---

## Integration Examples

### 1. Parse eBay Listings
```python
def map_to_taxonomy(listing_title: str) -> dict:
    """Map eBay listing to taxonomy ID."""

    # Detect random year patterns
    if any(x in listing_title.lower() for x in
           ['random year', 'varied year', 'our choice', "dealer's choice"]):

        # Extract weight
        if '1 oz' in listing_title:
            return {
                'taxonomy_id': 'US-AGEO-XXXX-X',
                'product_type': 'bullion',
                'weight_oz': 1.0
            }
        elif '1/2 oz' in listing_title:
            return {
                'taxonomy_id': 'US-AGEF-XXXX-X',
                'product_type': 'bullion',
                'weight_oz': 0.5
            }
        # ... etc

    else:
        # Extract specific year and map to numismatic
        year = extract_year(listing_title)  # Your regex
        mint = extract_mint(listing_title)  # P, D, S, W

        return {
            'taxonomy_id': f'US-AGEO-{year}-{mint}',
            'product_type': 'numismatic',
            'weight_oz': 1.0
        }
```

### 2. Price Comparison API
```python
# Query for cheapest Gold Eagles (any year)
SELECT
    dealer_name,
    price,
    premium_pct,
    in_stock
FROM products
WHERE taxonomy_id LIKE 'US-AGEO-%'  -- All 1 oz Gold Eagles
ORDER BY price ASC
LIMIT 10;

# Filter only random year (lowest premiums)
WHERE taxonomy_id = 'US-AGEO-XXXX-X'

# Filter specific year (numismatic premium)
WHERE taxonomy_id = 'US-AGEO-2024-W'
```

### 3. Inventory Management
```python
class BullionInventory:
    """Track mixed year bullion inventory."""

    def __init__(self):
        self.stock = {
            'US-AGEO-XXXX-X': {
                'quantity': 100,
                'actual_years': [2015, 2018, 2019, 2022, 2024],
                'avg_cost': 2050.00,
                'valuation_method': 'spot_plus_premium'
            },
            'US-AGEO-2024-W': {
                'quantity': 10,
                'actual_years': [2024],
                'avg_cost': 2500.00,
                'valuation_method': 'numismatic_premium'
            }
        }

    def get_current_value(self, taxonomy_id: str) -> float:
        """Calculate current value based on type."""
        item = self.stock[taxonomy_id]

        if 'XXXX' in taxonomy_id:
            # Bullion: spot + premium
            spot_price = get_gold_spot()  # $2300/oz
            premium = 0.05  # 5% over spot
            return item['quantity'] * spot_price * (1 + premium)
        else:
            # Numismatic: market value
            return item['quantity'] * get_market_price(taxonomy_id)
```

---

## Validation

### Coin ID Format
```python
import re

pattern = r'^([A-Z]{2,3})-([A-Z]{4})-(\d{4}|XXXX)-([A-Z]{1,2})$'

# Valid IDs:
re.match(pattern, 'US-AGEO-XXXX-X')  # ✅ Random year bullion
re.match(pattern, 'US-AGEO-2024-W')  # ✅ Specific year
re.match(pattern, 'US-LWC-1909-S')   # ✅ Numismatic

# Invalid IDs:
re.match(pattern, 'US-AGEO-XXXX-W-PR')  # ❌ Too many parts (variety goes in varieties array)
re.match(pattern, 'us-ageo-xxxx-x')     # ❌ Lowercase not allowed
```

### Year Field Type
```python
def convert_year(year_value):
    """Convert year from database to JSON type."""
    if year_value == 'XXXX':
        return 'XXXX'  # String
    try:
        return int(year_value)  # Integer for numeric years
    except (ValueError, TypeError):
        return year_value
```

---

## Database Access

### Query Examples
```sql
-- Get all Gold Eagle series
SELECT
    series_abbreviation,
    series_name,
    denomination,
    defining_characteristics
FROM series_registry
WHERE series_abbreviation LIKE 'AG%';

-- Get all random year bullion coins
SELECT coin_id, series, year, weight_grams
FROM coins
WHERE year = 'XXXX';

-- Results:
-- US-AGEO-XXXX-X | American Gold Eagle (1 oz)    | XXXX | 31.103
-- US-AGEF-XXXX-X | American Gold Eagle (1/2 oz)  | XXXX | 16.966
-- US-AGET-XXXX-X | American Gold Eagle (1/4 oz)  | XXXX | 8.483
-- US-AGES-XXXX-X | American Gold Eagle (1/10 oz) | XXXX | 3.393
```

### JSON Export Files
```bash
# Per-denomination exports
data/us/coins/$50.json   # AGEO (1 oz)
data/us/coins/$25.json   # AGEF (1/2 oz)
data/us/coins/$10.json   # AGET (1/4 oz)
data/us/coins/$5.json    # AGES (1/10 oz)

# Complete taxonomy
data/us/us_coins_complete.json

# Series registry
data/universal/series_registry.json
```

---

## Recommended Database Schema

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    taxonomy_id TEXT NOT NULL,

    -- Auto-detect bullion vs numismatic
    is_random_year BOOLEAN GENERATED ALWAYS AS
        (taxonomy_id LIKE '%-XXXX-%') STORED,

    product_type TEXT CHECK(product_type IN ('bullion', 'numismatic')),

    -- Pricing
    price_usd DECIMAL(10,2),
    spot_price_usd DECIMAL(10,2),  -- For bullion
    premium_pct DECIMAL(5,2),      -- Over spot

    -- Product info
    dealer_name TEXT,
    title TEXT,
    url TEXT,
    in_stock BOOLEAN,

    -- Indexes
    INDEX idx_taxonomy (taxonomy_id),
    INDEX idx_random_year (is_random_year),
    INDEX idx_dealer (dealer_name)
);

-- Example queries:
-- Cheapest random year Gold Eagles
SELECT * FROM products
WHERE is_random_year = true
  AND taxonomy_id LIKE 'US-AGEO-%'
ORDER BY price_usd ASC;

-- Compare random year vs specific year pricing
SELECT
    CASE WHEN is_random_year THEN 'Random' ELSE 'Specific' END,
    AVG(premium_pct),
    MIN(price_usd),
    COUNT(*)
FROM products
WHERE taxonomy_id LIKE 'US-AGEO-%'
GROUP BY is_random_year;
```

---

## Common Pitfalls to Avoid

### ❌ Don't: Mix year types in inventory
```python
# BAD: Ambiguous
inventory = {
    'US-AGEO-XXXX-X': 100,  # Does this include the 2024 coins below?
    'US-AGEO-2024-W': 10    # Unclear relationship
}
```

### ✅ Do: Separate random year and specific year inventory
```python
# GOOD: Clear separation
inventory = {
    'random_year': {
        'US-AGEO-XXXX-X': {
            'quantity': 100,
            'actual_years': [2015, 2018, 2022, 2024]
        }
    },
    'specific_year': {
        'US-AGEO-2024-W': {
            'quantity': 10,
            'notes': '2024 proof editions'
        }
    }
}
```

### ❌ Don't: Treat XXXX as "unknown year"
```python
# BAD: XXXX doesn't mean damaged or worn
if year == 'XXXX':
    condition = 'unknown'  # Wrong!
```

### ✅ Do: Understand XXXX means random year bullion
```python
# GOOD: XXXX is intentional for bullion products
if year == 'XXXX':
    product_type = 'bullion'
    notes = "Dealer will select year from available inventory"
    pricing_method = 'spot_plus_premium'
```

---

## Quick Reference

### Series Codes Cheat Sheet
```
AGEO → 1 oz Gold Eagle
AGEF → 1/2 oz Gold Eagle (F = Fractional/Half)
AGET → 1/4 oz Gold Eagle (T = Twenty-five/Quarter)
AGES → 1/10 oz Gold Eagle (S = Small/Tenth)
```

### Valuation Logic
```python
if 'XXXX' in taxonomy_id:
    # Bullion: Spot + Premium
    value = gold_spot * weight_oz * (1 + premium)
else:
    # Numismatic: Market Value
    value = get_market_value(taxonomy_id, grade)
```

### File Locations
```
Database:  database/coins.db
Exports:   data/us/coins/*.json
Schema:    data/us/schema/coin.schema.json
Guide:     docs/BULLION_INTEGRATION_GUIDE.md
```

---

## Testing Your Integration

```python
# Unit test example
def test_gold_eagle_taxonomy():
    # Test random year detection
    assert is_random_year('US-AGEO-XXXX-X') == True
    assert is_random_year('US-AGEO-2024-W') == False

    # Test pricing
    coin_data = taxonomy.get('US-AGEO-XXXX-X')
    assert coin_data['weight_grams'] == 31.103
    assert coin_data['composition']['gold'] == 91.67

    # Test valuation
    price = calculate_price('US-AGEO-XXXX-X', spot=2300, premium=0.05)
    assert price == 2415.00  # $2300 * 1.05
```

---

## Migration Scripts

All migration scripts are version controlled and reusable:

```bash
# Schema migration (already run, safe to re-run)
uv run python scripts/migrate_schema_for_xxxx_support.py --dry-run

# Add Gold Eagle series (already run)
uv run python scripts/add_gold_eagle_series.py --dry-run

# Export database to JSON
uv run python scripts/export_from_database.py
```

---

## Documentation

- **Complete Integration Guide:** `docs/BULLION_INTEGRATION_GUIDE.md`
- **Schema Documentation:** `data/us/schema/coin.schema.json`
- **Project Docs:** `docs/PROJECT_DOCS.md`
- **GitHub Issue:** [#52](https://github.com/mattsilv/coin-taxonomy/issues/52)

---

## Support

If you have questions or need help integrating:
1. Check `docs/BULLION_INTEGRATION_GUIDE.md` (comprehensive examples)
2. Review this commit: `8e10fa2`
3. Open a GitHub issue with `@mattsilv` mention

---

**Status:** ✅ Ready for backend integration
**Next Steps:** Use these taxonomy IDs in your price tracking, inventory, or marketplace integration
