# Bullion Integration Guide for Backend Engineers

**Last Updated:** November 7, 2025
**Version:** 1.0
**Status:** Production Ready

## Overview

This guide provides everything backend engineers need to integrate the coin-taxonomy bullion dataset into their applications. The taxonomy now supports both **numismatic coins** (specific years matter) and **bullion products** (random year, valued by metal content).

---

## What Changed (November 7, 2025)

### Random Year Pattern Support Added

The taxonomy now supports `XXXX` as a year placeholder for bullion products sold as "random year" or "dealer's choice."

**Why this matters:**
- Major dealers (eBay, APMEX, JM Bullion, SD Bullion) sell bullion as "random year" at lowest premium
- These are legitimate product listings that need canonical taxonomy IDs
- Enables uniform price tracking, inventory management, and marketplace comparison

**Schema changes:**
- Year field: Changed from `INTEGER` to `TEXT` with CHECK constraint
- Accepts either 4-digit year (1773-9999) OR literal string "XXXX"
- Coin ID pattern updated: `^[A-Z]{2,3}-[A-Z]{4}-(\\d{4}|XXXX)-[A-Z]{1,2}$`
- All 609 existing coins migrated with zero data loss

**Example IDs:**
```
US-AGEO-XXXX-X  → Gold Eagle 1 oz, random year, any mint
US-ASEA-XXXX-X  → Silver Eagle 1 oz, random year, any mint
US-AGBF-XXXX-W  → Gold Buffalo 1 oz, random year, West Point
CA-GMLO-XXXX-X  → Canadian Gold Maple Leaf 1 oz, random year
```

---

## Bullion vs Numismatic: Key Differences

### Numismatic Coins (Collectible Value)
- **Year matters**: 1909-S VDB Lincoln Cent vs 1943 Steel Cent = different values
- **Condition matters**: MS-65 vs AU-50 = significant price difference
- **Varieties matter**: 1955 Doubled Die vs regular = massive premium
- **Specific identifiers required**: `US-LWC-1909-S` (exact year, exact mint)

### Bullion Products (Metal Content Value)
- **Year doesn't matter**: 2010 Silver Eagle vs 2024 Silver Eagle = same melt value
- **Condition less important**: Circulated vs uncirculated = small premium difference
- **Generic product**: "1 oz Silver Eagle" sold at spot + premium
- **Random year acceptable**: `US-ASEA-XXXX-X` (year unspecified)

---

## Bullion Coverage Status

| Country | Metal | Series | Coins in DB | Status |
|---------|-------|--------|-------------|--------|
| 🇨🇦 Canada | Gold | Maple Leaf | 219 | ✅ Complete (1979-2024) |
| 🇨🇦 Canada | Silver | Maple Leaf | 43 | ✅ Complete (1988-2024) |
| 🇨🇦 Canada | Platinum | Maple Leaf | 30 | ✅ Complete (1988-2024) |
| 🇨🇦 Canada | Palladium | Maple Leaf | 14 | ✅ Complete (2005-2024) |
| 🇺🇸 USA | Gold | Eagles (4 sizes) | 0* | ⏳ Planned (#52) |
| 🇺🇸 USA | Gold | Buffalo | 0* | ⏳ Planned (#52) |
| 🇺🇸 USA | Silver | Silver Eagle | 0* | ⏳ Planned (#51) |

*Script exists with sample data, full implementation pending

---

## Integration Patterns

### Pattern 1: E-commerce Marketplace (eBay, Etsy)

**Use case:** Parse listings, map to taxonomy IDs, enable price comparison

```python
# Example: Parse eBay listing
listing_title = "American Silver Eagle 1 oz - Random Year"

# Map to taxonomy
if "random year" in listing_title.lower() or "varied year" in listing_title.lower():
    taxonomy_id = "US-ASEA-XXXX-X"  # Random year bullion
    product_type = "bullion"
    valuation_method = "spot_plus_premium"
else:
    # Extract specific year and mint
    taxonomy_id = "US-ASEA-2024-W"  # Specific year numismatic
    product_type = "numismatic"
    valuation_method = "market_value"

# Query taxonomy for product details
coin_data = taxonomy.get(taxonomy_id)
# → {
#     "series": "American Silver Eagle",
#     "composition": {"silver": 99.9},
#     "weight_grams": 31.103,
#     "denomination": "$1",
#     ...
# }
```

### Pattern 2: Inventory Management System

**Use case:** Track bullion inventory with mixed year coins

```python
# Inventory database schema
class BullionInventory:
    taxonomy_id: str       # US-AGEO-XXXX-X or US-AGEO-2024-W
    quantity: int
    acquisition_cost: float
    acquisition_date: date
    specific_years: list   # [2020, 2021, 2024] if tracking

# Example: Mixed year inventory
inventory = [
    {
        "taxonomy_id": "US-AGEO-XXXX-X",  # Random year Gold Eagle
        "quantity": 100,
        "specific_years": [2015, 2018, 2019, 2022, 2024],
        "valuation": "spot_plus_premium",
        "notes": "Mixed year inventory, dealer choice"
    },
    {
        "taxonomy_id": "US-AGEO-2024-W",  # Specific 2024 proof
        "quantity": 10,
        "valuation": "numismatic_premium",
        "notes": "2024 proof editions, sealed mint packaging"
    }
]

# Price calculation
def get_current_value(item):
    coin = taxonomy.get(item["taxonomy_id"])

    if "XXXX" in item["taxonomy_id"]:
        # Bullion: spot + premium
        spot_price = get_spot_price(coin["composition"]["metal"])
        premium = 0.05  # 5% dealer premium
        return item["quantity"] * coin["weight_troy_oz"] * spot_price * (1 + premium)
    else:
        # Numismatic: market value
        return item["quantity"] * get_market_price(item["taxonomy_id"])
```

### Pattern 3: Price Tracking API

**Use case:** Aggregate prices from multiple dealers

```python
# API endpoint: /api/v1/prices/<taxonomy_id>
GET /api/v1/prices/US-ASEA-XXXX-X

# Response
{
    "taxonomy_id": "US-ASEA-XXXX-X",
    "product_name": "American Silver Eagle 1 oz (Random Year)",
    "product_type": "bullion",
    "spot_price": 31.50,  # Current silver spot
    "dealer_prices": [
        {
            "dealer": "APMEX",
            "price": 34.99,
            "premium_pct": 11.1,
            "url": "https://..."
        },
        {
            "dealer": "JM Bullion",
            "price": 33.95,
            "premium_pct": 7.8,
            "url": "https://..."
        },
        {
            "dealer": "SD Bullion",
            "price": 33.49,
            "premium_pct": 6.3,
            "url": "https://..."
        }
    ],
    "best_price": {
        "dealer": "SD Bullion",
        "price": 33.49,
        "premium_pct": 6.3
    },
    "specifications": {
        "weight_troy_oz": 1.0,
        "purity": 0.999,
        "composition": {"silver": 99.9, "copper": 0.1}
    }
}
```

### Pattern 4: Collection Management

**Use case:** Track personal collection with graded and raw bullion

```python
# Collection database
class CollectionItem:
    taxonomy_id: str           # US-AGEO-2024-W or US-AGEO-XXXX-X
    quantity: int
    grade: Optional[str]       # "MS-69", "PR-70", null for bullion
    grading_service: Optional[str]  # "PCGS", "NGC", null
    cert_number: Optional[str]
    purchase_price: float
    purchase_date: date
    notes: str

# Example collection
collection = [
    {
        "taxonomy_id": "US-AGEO-2024-W",
        "quantity": 1,
        "grade": "PR-70",
        "grading_service": "PCGS",
        "cert_number": "12345678",
        "purchase_price": 2500.00,
        "notes": "2024 Proof Gold Eagle, perfect grade"
    },
    {
        "taxonomy_id": "US-AGEO-XXXX-X",
        "quantity": 10,
        "grade": null,  # Raw/ungraded bullion
        "grading_service": null,
        "cert_number": null,
        "purchase_price": 2100.00,
        "notes": "Mixed year bullion stack, purchased for melt value"
    }
]

# Valuation logic
def value_collection_item(item):
    if item["grade"]:
        # Numismatic: use market value for graded coin
        return get_graded_coin_value(item["taxonomy_id"], item["grade"])
    else:
        # Bullion: use spot + premium
        coin = taxonomy.get(item["taxonomy_id"])
        return calculate_melt_value(coin) * item["quantity"]
```

---

## Database Schema Recommendations

### Recommended Fields for Bullion Integration

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    taxonomy_id TEXT NOT NULL,           -- US-ASEA-XXXX-X or US-ASEA-2024-W
    product_type TEXT NOT NULL           -- 'bullion' or 'numismatic'
        CHECK(product_type IN ('bullion', 'numismatic')),

    -- If taxonomy_id contains XXXX:
    is_random_year BOOLEAN GENERATED ALWAYS AS
        (taxonomy_id LIKE '%-XXXX-%') STORED,

    -- Product details
    title TEXT,
    description TEXT,
    dealer_name TEXT,

    -- Pricing
    price_usd DECIMAL(10,2),
    spot_price_usd DECIMAL(10,2),       -- If bullion
    premium_pct DECIMAL(5,2),           -- If bullion

    -- Inventory
    quantity_available INT,
    last_updated TIMESTAMP DEFAULT NOW(),

    -- Numismatic-specific (nullable for bullion)
    grade TEXT,                          -- MS-65, PR-69, etc.
    grading_service TEXT,                -- PCGS, NGC, etc.
    condition TEXT,                      -- circulated, uncirculated

    -- Indexes
    INDEX idx_taxonomy (taxonomy_id),
    INDEX idx_product_type (product_type),
    INDEX idx_random_year (is_random_year)
);
```

### Query Examples

```sql
-- Find all random year bullion products
SELECT * FROM products
WHERE is_random_year = true
AND product_type = 'bullion';

-- Get cheapest Silver Eagles (any year)
SELECT taxonomy_id, title, price_usd, premium_pct
FROM products
WHERE taxonomy_id LIKE 'US-ASEA-%'
ORDER BY price_usd ASC
LIMIT 10;

-- Compare random year vs specific year pricing
SELECT
    CASE
        WHEN is_random_year THEN 'Random Year'
        ELSE 'Specific Year'
    END as category,
    AVG(premium_pct) as avg_premium,
    MIN(price_usd) as min_price,
    MAX(price_usd) as max_price,
    COUNT(*) as listing_count
FROM products
WHERE taxonomy_id LIKE 'US-AGEO-%'  -- Gold Eagles only
GROUP BY is_random_year;
```

---

## Validation and Error Handling

### Validate Taxonomy ID Format

```python
import re

def validate_taxonomy_id(taxonomy_id: str) -> dict:
    """
    Validate taxonomy ID format and extract components.

    Returns:
        {
            "valid": bool,
            "country": str,
            "series": str,
            "year": str,
            "mint": str,
            "is_random_year": bool,
            "error": str
        }
    """
    # Pattern: COUNTRY-TYPE-YEAR-MINT
    # Year can be 4 digits OR "XXXX"
    pattern = r'^([A-Z]{2,3})-([A-Z]{4})-(\\d{4}|XXXX)-([A-Z]{1,2})$'

    match = re.match(pattern, taxonomy_id)

    if not match:
        return {
            "valid": False,
            "error": "Invalid format. Expected: COUNTRY-TYPE-YEAR-MINT"
        }

    country, series, year, mint = match.groups()

    return {
        "valid": True,
        "country": country,
        "series": series,
        "year": year,
        "mint": mint,
        "is_random_year": (year == "XXXX"),
        "error": None
    }

# Usage
result = validate_taxonomy_id("US-AGEO-XXXX-X")
# → {"valid": True, "is_random_year": True, ...}

result = validate_taxonomy_id("US-AGEO-2024-W")
# → {"valid": True, "is_random_year": False, ...}

result = validate_taxonomy_id("INVALID-ID")
# → {"valid": False, "error": "..."}
```

### Handle Missing Taxonomy Entries

```python
def get_product_details(taxonomy_id: str):
    """Get product details with fallback for missing entries."""

    # Try exact match first
    product = taxonomy.get(taxonomy_id)

    if product:
        return product

    # If XXXX not found, suggest specific year alternatives
    if "XXXX" in taxonomy_id:
        # Extract series code
        country, series, _, mint = taxonomy_id.split("-")

        # Find any coins matching this series
        alternatives = taxonomy.search(
            country=country,
            series=series,
            mint=mint if mint != "X" else None
        )

        if alternatives:
            return {
                "error": "Random year entry not found",
                "taxonomy_id": taxonomy_id,
                "suggestion": "Use specific year alternative",
                "alternatives": alternatives[:5]  # Show first 5
            }

    # No match found
    return {
        "error": "Taxonomy ID not found",
        "taxonomy_id": taxonomy_id
    }
```

---

## Best Practices

### 1. Distinguish Product Types

Always check if a product is bullion or numismatic:

```python
def get_product_type(taxonomy_id: str) -> str:
    if "XXXX" in taxonomy_id:
        return "bullion"

    # Check series code
    bullion_series = ["AGEO", "AGET", "AGEF", "AGES", "AGBF",  # US Gold
                      "ASEA",                                    # US Silver
                      "GMLO", "GMLH", "GMLQ", "GMLT",           # CA Gold
                      "SMLO"]                                    # CA Silver

    series = taxonomy_id.split("-")[1]
    if series in bullion_series:
        # Could be either - check composition and mintage
        coin = taxonomy.get(taxonomy_id)
        if coin.get("mintage", 0) > 1000000:  # High mintage = likely bullion
            return "bullion"

    return "numismatic"
```

### 2. Price Appropriately

```python
def calculate_price(taxonomy_id: str, coin_data: dict) -> float:
    if "XXXX" in taxonomy_id:
        # Bullion: spot + premium
        metal = coin_data["composition"]["primary_metal"]
        spot_price = get_spot_price(metal)
        weight_oz = coin_data["weight_troy_oz"]
        premium = 0.05  # 5% typical dealer premium

        return spot_price * weight_oz * (1 + premium)
    else:
        # Numismatic: market value (check pricing databases)
        return get_market_value(taxonomy_id, coin_data.get("grade"))
```

### 3. Filter Intelligently

```python
# E-commerce filter example
def build_product_filters():
    return {
        "product_type": ["bullion", "numismatic"],
        "metal": ["gold", "silver", "platinum", "palladium"],
        "weight": ["1oz", "1/2oz", "1/4oz", "1/10oz"],
        "year": ["any", "2024", "2023", "2022", "2021", "older"],
        "condition": ["raw", "graded"]
    }

def apply_filters(filters: dict):
    query = "SELECT * FROM products WHERE 1=1"

    if filters.get("product_type") == "bullion":
        query += " AND (is_random_year = true OR product_type = 'bullion')"

    if filters.get("year") == "any":
        query += " AND is_random_year = true"
    elif filters.get("year") != "all":
        query += f" AND year = '{filters['year']}'"

    # ... additional filters

    return execute(query)
```

### 4. Document Clearly

```python
# API documentation example
"""
GET /api/v1/products?type=bullion&year=any

Returns bullion products with random year (XXXX pattern).

Query Parameters:
- type: "bullion" or "numismatic"
- year: "any" (XXXX pattern), specific year (2024), or "all"
- metal: "gold", "silver", "platinum", "palladium"
- series: "US-AGEO" (Gold Eagle 1oz), "US-ASEA" (Silver Eagle), etc.

Example Response:
{
    "products": [
        {
            "taxonomy_id": "US-AGEO-XXXX-X",
            "title": "American Gold Eagle 1 oz (Random Year)",
            "type": "bullion",
            "year": "random",
            "price_usd": 2150.00,
            "premium_pct": 5.2,
            ...
        }
    ]
}
"""
```

---

## Common Pitfalls to Avoid

### ❌ Don't: Treat random year as numismatic
```python
# BAD: This will fail or give wrong valuation
coin = get_coin("US-AGEO-XXXX-X")
grade = "MS-69"  # Doesn't make sense for random year
market_value = get_graded_value(coin, grade)  # Wrong approach!
```

### ✅ Do: Recognize bullion and use spot pricing
```python
# GOOD: Check year pattern and use appropriate valuation
coin = get_coin("US-AGEO-XXXX-X")
if "XXXX" in coin["taxonomy_id"]:
    value = calculate_melt_value(coin) * (1 + premium)
else:
    value = get_market_value(coin)
```

### ❌ Don't: Assume XXXX means "unknown"
```python
# BAD: XXXX is not the same as damaged/worn coins
if "XXXX" in taxonomy_id:
    condition = "unknown"  # Wrong!
```

### ✅ Do: Understand XXXX is for random year products
```python
# GOOD: XXXX specifically means "dealer's choice year"
if "XXXX" in taxonomy_id:
    product_type = "bullion"
    year_specificity = "random_year"
    notes = "Dealer will select year based on inventory"
```

### ❌ Don't: Mix year types in inventory tracking
```python
# BAD: Ambiguous inventory
inventory = {
    "US-AGEO-XXXX-X": 100,  # Random year
    "US-AGEO-2024-W": ???   # Is this included in the 100 above?
}
```

### ✅ Do: Separate specific year and random year inventory
```python
# GOOD: Clear separation
inventory = {
    "random_year": {
        "US-AGEO-XXXX-X": 100,
        "actual_years": [2015, 2018, 2019, 2022, 2024]
    },
    "specific_year": {
        "US-AGEO-2024-W": 10  # Separate count for 2024
    }
}
```

---

## Testing Your Integration

### Unit Tests

```python
import pytest

def test_random_year_validation():
    assert validate_taxonomy_id("US-AGEO-XXXX-X")["valid"] == True
    assert validate_taxonomy_id("US-AGEO-XXXX-X")["is_random_year"] == True
    assert validate_taxonomy_id("US-AGEO-2024-W")["is_random_year"] == False

def test_bullion_pricing():
    coin = {
        "taxonomy_id": "US-ASEA-XXXX-X",
        "weight_troy_oz": 1.0,
        "composition": {"silver": 99.9}
    }

    # Mock spot price = $30/oz
    price = calculate_price(coin, spot_silver=30.0, premium=0.05)

    assert price == 31.50  # $30 * 1.05

def test_product_type_detection():
    assert get_product_type("US-AGEO-XXXX-X") == "bullion"
    assert get_product_type("US-IHC-1877-P") == "numismatic"
```

### Integration Tests

```python
def test_end_to_end_bullion_flow():
    # 1. Parse dealer listing
    listing = "American Silver Eagle 1 oz - Random Year - $34.99"

    # 2. Map to taxonomy
    taxonomy_id = parse_listing(listing)
    assert taxonomy_id == "US-ASEA-XXXX-X"

    # 3. Get product details
    coin = taxonomy.get(taxonomy_id)
    assert coin["series"] == "American Silver Eagle"

    # 4. Calculate value
    value = calculate_price(taxonomy_id, coin)
    assert value < 50.0  # Reasonable bullion price

    # 5. Store in database
    product_id = save_product(taxonomy_id, listing, value)
    assert product_id > 0

    # 6. Query and verify
    retrieved = get_product(product_id)
    assert retrieved["is_random_year"] == True
```

---

## Support and Resources

### Taxonomy Access

- **Database:** `coins.db` (SQLite)
- **JSON Exports:** `data/us/coins/*.json`, `data/ca/coins/*.json`
- **API:** TBD (community contributions welcome)
- **GitHub:** https://github.com/mattsilv/coin-taxonomy

### Reference Documentation

- **Schema documentation:** `data/us/schema/coin.schema.json`
- **Project docs:** `docs/PROJECT_DOCS.md`
- **Grading standards:** `docs/external-metadata/COIN_GRADING.md`
- **Bullion integration:** `docs/BULLION_INTEGRATION_GUIDE.md` (this document)

### Series Code Reference

#### US Gold Bullion
- `AGES` - American Gold Eagle $5 (1/10 oz)
- `AGET` - American Gold Eagle $10 (1/4 oz)
- `AGEF` - American Gold Eagle $25 (1/2 oz)
- `AGEO` - American Gold Eagle $50 (1 oz)
- `AGBF` - American Gold Buffalo $50 (1 oz)

#### US Silver Bullion
- `ASEA` - American Silver Eagle $1 (1 oz)
- `ATBQ` - America the Beautiful 5 oz (2010-2021)

#### Canadian Gold Bullion
- `GMLT` - Gold Maple Leaf 1/20 oz
- `GMLE` - Gold Maple Leaf 1/10 oz
- `GMLQ` - Gold Maple Leaf 1/4 oz
- `GMLH` - Gold Maple Leaf 1/2 oz
- `GMLO` - Gold Maple Leaf 1 oz

#### Canadian Silver Bullion
- `SMLO` - Silver Maple Leaf 1 oz

### Community

- **GitHub Issues:** Report bugs, request features
- **Pull Requests:** Contribute improvements
- **Discussions:** Ask questions, share integration stories

---

## Changelog

### November 7, 2025 - v1.0

**Added:**
- Random year pattern support (XXXX placeholder)
- Schema migration from INTEGER to TEXT year field
- Documentation for bullion vs numismatic distinction
- Integration patterns for e-commerce, inventory, pricing APIs
- Database schema recommendations
- Validation helpers and error handling examples

**Changed:**
- Year field now accepts either 4-digit year OR "XXXX" string
- Coin ID pattern updated to accept XXXX in year position
- All validation scripts updated to handle both formats

**Migration:**
- All 609 existing coins migrated successfully
- Zero data loss
- Backward compatible (all existing IDs still valid)

---

## License

This taxonomy is open source. See main repository for license details.

---

## Contact

For integration support or questions:
- GitHub Issues: https://github.com/mattsilv/coin-taxonomy/issues
- Documentation: https://github.com/mattsilv/coin-taxonomy/tree/main/docs

---

**Happy integrating!** 🪙✨
