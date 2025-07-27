# Developer Contribution Guide

## Overview

The Universal Currency Taxonomy v1.1 provides a robust foundation for cataloging coins and banknotes from any country and time period. This guide helps developers understand the architecture and contribute effectively.

## Quick Start for Developers

### Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Basic understanding of SQLite and JSON

### Setup
```bash
git clone https://github.com/mattsilv/coin-taxonomy.git
cd coin-taxonomy
uv venv && source .venv/bin/activate
uv add jsonschema
```

### Key Files to Understand
```
coin-taxonomy/
├── database/coins.db              # Source of truth (SQLite)
├── data/universal/               # Universal export format
├── data/us/coins/               # Legacy export format  
├── scripts/export_db_v1_1.py   # Dual-format export
├── scripts/migrate_to_universal_v1_1.py  # Migration logic
├── docs/database_schema_v1_1.md # Complete schema reference
├── examples/universal_issue_sample.json  # Format examples
└── README.md                    # Project overview
```

## Architecture Overview

### Database-First Design
The SQLite database serves as the **single source of truth**:

```
SQLite Database (source of truth)
    ↓ 
JSON Exports (generated)
    ↓
Applications & APIs
```

**Why this approach?**
- Ensures data consistency and integrity
- Enables complex queries and relationships
- Supports atomic transactions for data updates
- JSON exports provide version control and distribution

### Universal Schema Design

#### Core Philosophy
1. **Flat Structure**: Replaces nested hierarchies with normalized tables
2. **Registry Pattern**: Centralized catalogs for subjects, compositions, series
3. **JSON Fields**: Complex data stored as structured JSON within relational framework
4. **Human-Readable IDs**: Issue IDs like `US-LWC-1909-S-VDB` are self-documenting

#### Table Relationships
```
issues (main table)
├── series_id → series_registry
├── specifications.composition_key → composition_registry  
└── sides.*.subject_id → subject_registry
```

## Adding New Currency Data

### Step 1: Understand the Issue ID Format
Every currency item gets a unique, human-readable ID:

**Format**: `{COUNTRY}-{SERIES_ABBREV}-{YEAR}-{MINT}[-{VARIETY}]`

Examples:
- `US-LWC-1909-S-VDB` - US Lincoln Wheat Cent, 1909, San Francisco, VDB variety
- `UK-SOV-1887-GOLD` - UK Sovereign, 1887, Gold
- `CA-DOL-1935-SILVER` - Canada Dollar, 1935, Silver

### Step 2: Registry First Approach

Before adding issues, populate the registries:

#### Subject Registry
Add any new people, symbols, or design elements:

```python
# Example: Adding a new historical figure
subject = {
    "subject_id": "queen_elizabeth_ii",
    "type": "historical_figure", 
    "name": "Queen Elizabeth II",
    "nationality": "British",
    "roles": ["monarch", "head_of_state"],
    "life_dates": {"birth": 1926, "death": 2022},
    "reign_dates": {"start": 1952, "end": 2022},
    "significance": "Longest-reigning British monarch"
}
```

#### Composition Registry  
Add any new alloys or materials:

```python
# Example: Adding a new composition
composition = {
    "composition_key": "sterling_silver_925",
    "name": "Sterling Silver",
    "alloy_composition": {"silver": 0.925, "copper": 0.075},
    "period_description": "Traditional silver standard",
    "density_g_cm3": 10.49,
    "color_description": "Bright silver"
}
```

#### Series Registry
Define the currency series:

```python
# Example: Adding a new series
series = {
    "series_id": "canadian_silver_dollar",
    "series_name": "Canadian Silver Dollar",
    "country_code": "CA",
    "denomination": "dollar", 
    "start_year": 1935,
    "end_year": 1967,
    "defining_characteristics": "Large silver dollar with voyageur design",
    "type": "coin"
}
```

### Step 3: Create Issue Records

Build the complete issue record with all required fields:

```python
issue = {
    "issue_id": generate_issue_id("CA", "CSD", 1935, "SILVER"),
    "object_type": "coin",
    "series_id": "canadian_silver_dollar",
    "issuing_entity": {
        "country_code": "CA",
        "authority_name": "Dominion of Canada",
        "monetary_system": "decimal", 
        "currency_unit": "dollar"
    },
    "denomination": {
        "face_value": 1.00,
        "unit_name": "dollar",
        "common_names": ["silver dollar"],
        "system_fraction": "1 dollar"
    },
    "issue_year": 1935,
    "specifications": {
        "weight_grams": 23.33,
        "diameter_mm": 36.07,
        "edge": "reeded",
        "composition_key": "sterling_silver_925"
    },
    "sides": {
        "obverse": {
            "design_id": "george_v_obverse_1935",
            "primary_element": {
                "type": "portrait",
                "subject_id": "george_v",
                "description": "Left-facing bust of King George V"
            }
        },
        "reverse": {
            "design_id": "voyageur_reverse_1935", 
            "primary_element": {
                "type": "historical_scene",
                "subject_id": "voyageur_canoe",
                "description": "Voyageur and Indigenous guide in canoe"
            }
        }
    },
    "mintage": {
        "business_strikes": 428707,
        "proof_strikes": 0
    }
}
```

## Database Operations

### Safe Data Modification Process

**Always follow this sequence**:

1. **Backup first**:
   ```bash
   cp database/coins.db backups/coins_backup_$(date +%Y%m%d_%H%M%S).db
   ```

2. **Make changes via scripts** (never edit JSON directly):
   ```python
   # Use database operations
   conn = sqlite3.connect('database/coins.db')
   # ... make changes
   conn.commit()
   ```

3. **Validate integrity**:
   ```bash
   uv run python scripts/data_integrity_check.py
   ```

4. **Export to JSON**:
   ```bash
   uv run python scripts/export_db_v1_1.py
   ```

5. **Commit both database and JSON**:
   ```bash
   git add database/coins.db data/
   git commit -m "Add Canadian silver dollars"
   ```

### Common Database Operations

#### Adding New Issues
```python
import sqlite3
import json

conn = sqlite3.connect('database/coins.db')
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO issues (
        issue_id, object_type, series_id, country_code, authority_name,
        monetary_system, currency_unit, face_value, unit_name, common_names,
        issue_year, specifications, sides, mintage
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    issue["issue_id"],
    issue["object_type"], 
    # ... all other fields
))

conn.commit()
conn.close()
```

#### Querying Data
```python
# Find all issues from a specific year
cursor.execute("SELECT * FROM issues WHERE issue_year = ?", (1935,))

# Complex queries with JSON
cursor.execute("""
    SELECT issue_id, JSON_EXTRACT(mintage, '$.business_strikes') as mintage
    FROM issues 
    WHERE JSON_EXTRACT(specifications, '$.composition_key') = ?
""", ("sterling_silver_925",))
```

## Adding Banknote Support

The schema is designed to handle banknotes with minimal changes:

### Banknote-Specific Fields

```python
banknote_specifications = {
    "height_mm": 66.3,
    "width_mm": 156.0,
    "substrate": "cotton_linen_blend",
    "color_scheme": ["green", "black"],
    "security_features": [
        {"feature": "watermark", "subject": "george_washington"},
        {"feature": "security_thread", "inscription": "USA ONE"}
    ]
}

banknote_sides = {
    "obverse": {
        "primary_element": {
            "type": "portrait",
            "subject_id": "george_washington"
        },
        "signatories": [
            {"role": "treasurer", "signature_id": "jovita_carranza"},
            {"role": "secretary", "signature_id": "steven_mnuchin"}
        ]
    }
}
```

## Code Style and Standards

### Python Code
- Use type hints where possible
- Follow PEP 8 style guidelines
- Include docstrings for functions
- Use f-strings for formatting

### Database Scripts
- Always use parameterized queries (never string concatenation)
- Include error handling and rollback logic
- Add comprehensive logging
- Test with small datasets first

### Data Validation
- Validate all foreign key references
- Check required fields are present
- Verify JSON field structure
- Test edge cases (missing mints, varieties, etc.)

## Testing Your Changes

### Manual Testing Checklist
```bash
# 1. Validate database integrity
uv run python scripts/data_integrity_check.py

# 2. Test both export formats
uv run python scripts/export_db_v1_1.py

# 3. Verify JSON structure
python -m json.tool data/universal/us_issues.json > /dev/null

# 4. Check registry consistency  
uv run python -c "
import sqlite3
conn = sqlite3.connect('database/coins.db')
# Add validation queries here
"

# 5. Test sample queries
uv run python scripts/check_db_structure.py
```

### Automated Testing
Consider adding unit tests for:
- Issue ID generation logic
- JSON field validation
- Registry relationship integrity
- Export format consistency

## Common Pitfalls

1. **Don't edit JSON files directly** - they're generated from the database
2. **Always backup before migration** - database changes can be complex
3. **Validate foreign keys** - ensure subject_id references exist in subject_registry
4. **Test with edge cases** - handle missing mints, unknown varieties, etc.
5. **Check export consistency** - both legacy and universal formats should validate

## Getting Help

- **Schema Reference**: `docs/database_schema_v1_1.md`
- **Example Data**: `examples/universal_issue_sample.json`
- **Architecture**: `docs/database_architecture.md`
- **Issues**: Create GitHub issues with clear examples

## Future Enhancements

Areas where contributors can help:

### International Expansion
- Add European currencies (UK, France, Germany)
- Implement non-decimal monetary systems
- Create country-specific validation rules

### Design Data Enrichment
- Expand subject registry with more historical figures
- Add detailed inscription positioning data
- Link to external numismatic references (PCGS, NGC)

### Banknote Implementation
- Create complete banknote examples
- Implement signature tracking
- Add security feature cataloging

### Performance Optimization
- Index optimization for common queries
- Bulk import utilities
- Export format optimization

This foundation makes it straightforward to expand the taxonomy globally while maintaining data quality and consistency.