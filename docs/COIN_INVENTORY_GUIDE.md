# Coin Inventory System

**Status**: ✅ Implemented (Issue #65)
**Version**: 1.0.0
**Last Updated**: 2025-11-16

## Overview

The coin inventory system separates **coin identity** from **graded instances**, enabling you to track specific coins with their grades and certification details.

**Key Principle**: `coin + grade = market value`

## Architecture

### Three-Table Design

```
coins table          →  Coin identity (series, year, mint, etc.)
                         ↓
coin_inventory table →  Specific graded instances
                         ↓
grade_standards table → Grade definitions (Sheldon scale)
```

### Database Tables

1. **`coins`** - Coin issue identity (what the coin is)
2. **`grade_standards`** - Universal grading standard (how good it is)
3. **`coin_inventory`** - Specific graded coins (your collection)

## Quick Start

### Add a Coin to Inventory

```sql
INSERT INTO coin_inventory (
    coin_id,
    grade_id,
    grading_service,
    certification_number,
    is_certified,
    full_grade_string,
    collection_name,
    notes
) VALUES (
    'US-LWC-1909-S',    -- Coin identity
    'MS-65',             -- Grade
    'PCGS',              -- Grading service
    '12345678',          -- Cert number
    1,                   -- Is certified
    'PCGS MS-65 RD',     -- Full grade string
    'My Collection',     -- Collection name
    'Key date Lincoln cent'
);
```

### Query Your Collection

Use the helpful views:

```sql
-- Full details of all coins
SELECT * FROM vw_inventory_full;

-- Collection statistics
SELECT * FROM vw_inventory_summary;

-- Find all MS-65 coins
SELECT * FROM vw_inventory_full WHERE grade_id = 'MS-65';

-- Find all PCGS certified coins
SELECT * FROM vw_inventory_full WHERE grading_service = 'PCGS';
```

## Fields Reference

### Core Fields
- `inventory_id` - Auto-increment primary key
- `coin_id` - Links to coins table (e.g., `US-LWC-1909-S`)
- `grade_id` - Links to grade_standards (e.g., `MS-65`)

### Certification Details
- `grading_service` - `PCGS`, `NGC`, `ANACS`, `ICG`, `raw`, `self-graded`
- `certification_number` - Service cert number (e.g., `12345678`)
- `is_certified` - Boolean (third-party or raw)
- `strike_type` - `business`, `proof`, `specimen`

### Grade Modifiers
- `modifiers` - JSON array: `["CAM", "DCAM", "RD", "FB", etc.]`
- `full_grade_string` - Complete: `"PCGS MS-65 RD"`
- `market_threshold_grade` - Boolean (significant price break)

### Market Analysis
- `purchase_price` - Acquisition cost
- `purchase_date` - When acquired
- `current_value_estimate` - Estimated current value

### Collection Management
- `collection_name` - Which collection
- `storage_location` - Physical location
- `notes` - Condition notes, special characteristics
- `image_urls` - JSON array of photo URLs

## Usage Examples

### Example 1: Raw Coin (Self-Graded)

```sql
INSERT INTO coin_inventory (
    coin_id, grade_id, grading_service,
    is_certified, full_grade_string,
    notes
) VALUES (
    'US-IHC-1877-P',
    'AU-58',
    'raw',
    0,
    'AU-58',
    'Self-graded estimate - attractive toning'
);
```

### Example 2: Certified Proof Coin

```sql
INSERT INTO coin_inventory (
    coin_id, grade_id, grading_service,
    certification_number, is_certified,
    strike_type, modifiers,
    full_grade_string, market_threshold_grade,
    purchase_price, purchase_date
) VALUES (
    'US-LWC-1936-P',
    'PR-69',
    'NGC',
    '1234567',
    1,
    'proof',
    '["DCAM"]',
    'NGC PR-69 DCAM',
    1,
    450.00,
    '2025-01-15'
);
```

### Example 3: Query Collection Value

```sql
SELECT
    collection_name,
    COUNT(*) as total_coins,
    SUM(purchase_price) as total_cost,
    SUM(current_value_estimate) as estimated_value,
    SUM(current_value_estimate) - SUM(purchase_price) as gain_loss
FROM coin_inventory
GROUP BY collection_name;
```

## Database Views

### `vw_inventory_full`
Complete coin details with grade information joined.

Fields include: coin identity (year, mint, series), grade details (name, numeric value, category), certification info, and all inventory fields.

### `vw_inventory_summary`
Collection statistics grouped by collection_name.

Provides: total coins, certified/raw counts, grading services used, total cost, estimated value, date ranges.

## Migration Script

To add the coin_inventory table to an existing database:

```bash
uv run python scripts/migrate_add_coin_inventory.py
```

Options:
- `--dry-run` - Preview changes without applying
- `--skip-samples` - Don't insert sample records

## Export

Inventory data is exported to `data/inventory/coin_inventory.json` via:

```bash
uv run python scripts/export_from_database.py
```

## Integration with External Systems

The coin inventory system integrates with the grade external metadata schema (`data/schema/grade_external_metadata.schema.json`) for standardized grade representation across:

- Collection management systems
- Market data APIs
- Auction parsing systems
- Price guide integrations

## See Also

- **Issue #65**: Enhancement recommendation for inventory system
- **Issue #64**: Universal grading standard implementation
- `data/schema/grade_external_metadata.schema.json` - Grade metadata schema
- `data/universal/grade_standards.json` - Complete grade hierarchy
