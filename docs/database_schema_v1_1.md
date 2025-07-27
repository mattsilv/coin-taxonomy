# Universal Currency Taxonomy Database Schema v1.1

## Overview

The v1.1 schema introduces a universal flat structure that can accommodate coins and banknotes from any country and time period. The design uses JSON fields for complex data while maintaining relational integrity through registry tables.

## Core Tables

### `issues` Table
The primary table containing all currency items in a flat, normalized structure.

#### Column Structure

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `issue_id` | TEXT | No | Human-readable unique identifier (e.g., `US-LWC-1909-S-VDB`) |
| `object_type` | TEXT | Yes | Type of currency item: `coin`, `banknote` |
| `series_id` | TEXT | Yes | Foreign key to `series_registry` |
| `country_code` | TEXT | Yes | ISO-style country code |
| `authority_name` | TEXT | Yes | Full name of issuing authority |
| `monetary_system` | TEXT | Yes | System type: `decimal`, `pre-decimal`, etc. |
| `currency_unit` | TEXT | Yes | Base currency unit: `dollar`, `pound`, `franc`, etc. |
| `face_value` | REAL | Yes | Numeric face value in base currency unit |
| `unit_name` | TEXT | Yes | Denomination name: `cent`, `dime`, `quarter`, etc. |
| `common_names` | JSON | No | Array of common names: `["penny", "cent"]` |
| `system_fraction` | TEXT | No | Fraction description: `"1/100 dollar"` |
| `issue_year` | INTEGER | Yes | Year of issue |
| `mint_id` | TEXT | No | Mint mark or identifier |
| `date_range_start` | INTEGER | No | Start year for multi-year issues |
| `date_range_end` | INTEGER | No | End year for multi-year issues |
| `authority_period` | JSON | No | Authority context data |
| `specifications` | JSON | Yes | Physical specifications (see below) |
| `sides` | JSON | Yes | Design data for obverse/reverse (see below) |
| `mintage` | JSON | No | Production figures (see below) |
| `rarity` | TEXT | No | Rarity classification: `key`, `semi-key`, `scarce`, `common` |
| `varieties` | JSON | No | Array of variety data (see below) |
| `source_citation` | TEXT | No | Data source citation |
| `notes` | TEXT | No | Additional notes |
| `metadata` | JSON | No | Extensible metadata field |

#### JSON Field Specifications

##### `specifications` JSON Structure
Physical characteristics of the currency item:

```json
{
  "weight_grams": 3.11,
  "diameter_mm": 19.05,           // For coins
  "thickness_mm": 1.55,           // For coins  
  "height_mm": 66.3,              // For banknotes
  "width_mm": 156.0,              // For banknotes
  "edge": "plain",                // For coins: "plain", "reeded", "lettered"
  "substrate": "cotton_linen",    // For banknotes
  "color_scheme": ["green", "black"], // For banknotes
  "composition_key": "bronze_95_4_1"  // Reference to composition_registry
}
```

##### `sides` JSON Structure  
Design information for obverse and reverse:

```json
{
  "obverse": {
    "design_id": "lincoln_wheat_obverse_1909",
    "primary_element": {
      "type": "portrait",           // portrait, symbol, heraldic, architectural, etc.
      "subject_id": "abraham_lincoln", // Reference to subject_registry
      "subject_type": "historical_figure",
      "description": "Right-facing bust of Abraham Lincoln"
    },
    "inscriptions": [
      {"text": "IN GOD WE TRUST", "position": "top_arc"},
      {"text": "LIBERTY", "position": "left_field"},
      {"text": "1909", "position": "right_field"}
    ],
    "designer_id": "victor_brenner"  // Reference to subject_registry
  },
  "reverse": {
    "design_id": "wheat_ears_reverse_1909",
    "primary_element": {
      "type": "botanical",
      "subject_id": "wheat_ears",
      "subject_type": "flora", 
      "description": "Two ears of durum wheat flanking denomination"
    },
    "inscriptions": [
      {"text": "ONE CENT", "position": "center"},
      {"text": "UNITED STATES OF AMERICA", "position": "top_arc"}
    ],
    "designer_id": "victor_brenner"
  }
}
```

##### `mintage` JSON Structure
Production and distribution data:

```json
{
  "business_strikes": 484000,
  "proof_strikes": 0,
  "specimen_strikes": 0,          // Optional
  "pattern_strikes": 0,           // Optional
  "total_mintage": 484000,        // Calculated field
  "mint_distribution": {          // Optional breakdown
    "philadelphia": 300000,
    "denver": 184000
  }
}
```

##### `varieties` JSON Structure
Array of known varieties and errors:

```json
[
  {
    "variety_id": "LWC-1909-S-VDB-01",
    "name": "VDB", 
    "description": "With designer initials VDB on reverse",
    "type": "design_variant",      // design_variant, die_error, striking_error
    "estimated_mintage": 484000,
    "rarity": "key",
    "notes": "First year with designer initials"
  }
]
```

##### `common_names` JSON Structure
Array of alternative names:

```json
["penny", "cent", "copper"]
```

##### `authority_period` JSON Structure
Historical context about the issuing authority:

```json
{
  "entity_type": "federal_republic",
  "leader": {
    "id": "william_howard_taft",
    "role": "president", 
    "term": {"start": 1909, "end": 1913}
  },
  "regime_changes": [],           // Optional array of historical events
  "monetary_reforms": []          // Optional array of currency changes
}
```

### Registry Tables

#### `subject_registry`
Catalog of all people, symbols, and design elements:

| Column | Type | Description |
|--------|------|-------------|
| `subject_id` | TEXT | Unique identifier |
| `type` | TEXT | Category: `historical_figure`, `flora`, `fauna`, `symbol`, etc. |
| `name` | TEXT | Full name or description |
| `nationality` | TEXT | National origin |
| `roles` | JSON | Array of roles: `["president", "monarch"]` |
| `life_dates` | JSON | Birth/death: `{"birth": 1809, "death": 1865}` |
| `reign_dates` | JSON | Rule period: `{"start": 1952, "end": 2022}` |
| `significance` | TEXT | Historical importance |
| `symbolism` | JSON | Array of symbolic meanings |
| `scientific_name` | TEXT | For flora/fauna |
| `first_coin_appearance` | INTEGER | Year first used on currency |

#### `composition_registry`
Standardized alloy and material definitions:

| Column | Type | Description |
|--------|------|-------------|
| `composition_key` | TEXT | Unique identifier |
| `name` | TEXT | Common name |
| `alloy_composition` | JSON | Precise composition: `{"copper": 0.95, "tin": 0.04}` |
| `period_description` | TEXT | Usage period |
| `density_g_cm3` | REAL | Physical density |
| `magnetic_properties` | TEXT | Magnetic behavior |
| `color_description` | TEXT | Visual appearance |

#### `series_registry`  
Metadata for currency series:

| Column | Type | Description |
|--------|------|-------------|
| `series_id` | TEXT | Unique identifier |
| `series_name` | TEXT | Common series name |
| `country_code` | TEXT | Issuing country |
| `denomination` | TEXT | Denomination category |
| `start_year` | INTEGER | First year of issue |
| `end_year` | INTEGER | Last year of issue (NULL if ongoing) |
| `defining_characteristics` | TEXT | Key design features |
| `official_name` | TEXT | Official designation |
| `type` | TEXT | Currency type: `coin`, `banknote` |

## Issue ID Format

The universal system uses human-readable identifiers:

**Format**: `{COUNTRY}-{SERIES_ABBREV}-{YEAR}-{MINT}[-{VARIETY}]`

**Generation Rules**:
- Country: ISO-style country code (US, UK, CA, etc.)
- Series: First 3 uppercase characters of series_id
- Year: 4-digit issue year
- Mint: Mint mark or facility identifier
- Variety: Optional variety identifier

**Examples**:
- `US-LWC-1909-S-VDB` - 1909-S VDB Lincoln Wheat Cent
- `UK-VIC-1887-GOLD-JUB` - 1887 Victoria Golden Jubilee
- `CA-DOL-1935-SILVER` - 1935 Canadian Silver Dollar

## Data Migration Notes

### Known Issues from v1.0 Migration
During the initial migration from v1.0 to v1.1, some field mappings were incorrect:

1. **Specifications data** may be in wrong JSON fields
2. **Design data** needs enrichment from basic placeholders  
3. **Rarity classifications** need to be properly assigned

### Correction Scripts
- `fix_face_values.py` - Corrects denomination value mappings
- `data_integrity_check.py` - Validates data consistency
- Migration can be re-run with improved field mappings

## Usage Examples

### Query by Country and Year
```sql
SELECT issue_id, unit_name, mintage 
FROM issues 
WHERE country_code = 'US' AND issue_year = 1916;
```

### Find Key Dates
```sql
SELECT issue_id, JSON_EXTRACT(mintage, '$.business_strikes') as mintage
FROM issues 
WHERE rarity = 'key' 
ORDER BY JSON_EXTRACT(mintage, '$.business_strikes') ASC;
```

### Subject Registry Lookup
```sql
SELECT i.issue_id, s.name, s.significance
FROM issues i
JOIN subject_registry s ON JSON_EXTRACT(i.sides, '$.obverse.primary_element.subject_id') = s.subject_id
WHERE s.type = 'historical_figure';
```

This schema provides the foundation for truly universal numismatic cataloging while maintaining data integrity and performance.