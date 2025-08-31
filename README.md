# United States Coin Taxonomy Database

**The standardized taxonomy for mapping coin databases to universal identifiers**

A comprehensive database of 1,539+ US coins (1793-present) with standardized `COUNTRY-TYPE-YEAR-MINT` identifiers for marketplace integration and AI applications.

**🌐 [Live Demo](https://mattsilv.github.io/coin-taxonomy/)** | **📊 [AI Formats](#ai-optimized-formats)** | **🔗 [Integration Guide](#mapping-your-database)**

## What You Get

- **1,539+ coins** with standardized `US-TYPE-YEAR-MINT` identifiers
- **SQLite database** as single source of truth (version controlled)
- **AI-optimized formats** for marketplace integration (10K-26K tokens)
- **Complete composition data** for melt value calculations
- **Pre-commit hooks** for automatic JSON generation

## Quick Start for Engineers

```bash
# Clone and setup
git clone https://github.com/mattsilv/coin-taxonomy.git
cd coin-taxonomy
uv venv && source .venv/bin/activate

# Generate database and exports
uv run python scripts/rebuild_and_export.py

# Map your listings to our taxonomy
uv run python scripts/import_listing.py
```

## Mapping Your Database

### Standard Coin ID Format: `COUNTRY-TYPE-YEAR-MINT`

**Examples:**
```
US-LWCT-1909-S  → 1909-S Lincoln Wheat Cent
US-MERC-1916-D  → 1916-D Mercury Dime  
US-WASH-1932-D  → 1932-D Washington Quarter
```

### Handling Unknown Data

When mapping damaged or incomplete coins:
```
US-LWCT-YYYY-X  → Lincoln Wheat Cent, unknown year & mint
US-MERC-1942-X  → 1942 Mercury Dime, unknown mint
US-INCH-YYYY-P  → Indian Head Cent from Philadelphia, year unknown
```

### Type Code Reference

**Common types** (4-letter codes):
```python
# Cents
INCH = Indian Head Cent       LWCT = Lincoln Wheat Cent
LMCT = Lincoln Memorial Cent  LSCT = Lincoln Shield Cent

# Nickels  
JEFF = Jefferson Nickel       BUFF = Buffalo Nickel

# Dimes
MERC = Mercury Dime           ROOS = Roosevelt Dime

# Quarters
WASH = Washington Quarter     SLIQ = Standing Liberty Quarter

# Dollars
MORG = Morgan Dollar          PEAC = Peace Dollar
```

[Full type code list](data/universal/series_registry.json)

## AI-Optimized Formats

Two formats optimized for different use cases:

### Year-List Format (10K tokens)
**File:** [`data/ai-optimized/us_taxonomy_year_list.json`](data/ai-optimized/us_taxonomy_year_list.json)
```json
{
  "series": "lincoln_wheat_cent",
  "t": "LWCT",
  "years": "1909,1910,1911,1912,1913...",
  "ob": "Abraham Lincoln bust facing right..."
}
```
**Use for:** Year-based classification, GPT-3.5 compatible

### Coin-ID Format (26K tokens)  
**File:** [`data/ai-optimized/us_taxonomy.json`](data/ai-optimized/us_taxonomy.json)
```json
{
  "series": "lincoln_wheat_cent",
  "t": "LWCT",
  "coin_ids": "US-LWCT-1909-P,US-LWCT-1909-D,US-LWCT-1909-S..."
}
```
**Use for:** Exact coin matching, marketplace integration

## Integration Scripts

### Marketplace Listing Matcher
**Script:** [`scripts/import_listing.py`](scripts/import_listing.py)
```python
# Match eBay/marketplace listings to taxonomy
uv run python scripts/import_listing.py
# Enter: "1909 S Lincoln Cent VDB"
# Returns: US-LWCT-1909-S (with VDB variety)
```

### Melt Value Calculator
**Script:** [`scripts/calculate_melt.py`](scripts/calculate_melt.py)
```python
# Calculate silver content value
uv run python scripts/calculate_melt.py
# Uses composition_registry.json for metal content
```

### Database Export Pipeline
**Script:** [`scripts/export_from_database.py`](scripts/export_from_database.py)
```bash
# Regenerate all JSON from SQLite
uv run python scripts/export_from_database.py
```

## Database Architecture

### SQLite Database (Source of Truth)
**Location:** `database/coins.db`

**Key tables:**
- `issues` - Universal flat structure for all coins
- `coins` - Legacy US coin data  
- `composition_registry` - Metal content definitions
- `series_registry` - Series metadata

### Export Formats

**Universal Format:** [`data/universal/us_issues.json`](data/universal/us_issues.json)
```json
{
  "issue_id": "US-LWCT-1909-S",
  "object_type": "coin",
  "denomination": {...},
  "specifications": {...}
}
```

**Legacy Format:** [`data/us/us_coins_complete.json`](data/us/us_coins_complete.json)
```json
{
  "series_name": "Lincoln Wheat Cent",
  "coins": [{"coin_id": "US-LWCT-1909-S", ...}]
}
```

## Sample Integration Code

### Python Example
```python
import sqlite3
import json

# Connect to taxonomy database
conn = sqlite3.connect('database/coins.db')
cursor = conn.cursor()

# Map your listing to taxonomy
listing = "1909 S Lincoln Cent VDB"
cursor.execute("""
    SELECT coin_id, year, mint 
    FROM coins 
    WHERE series_name LIKE '%Lincoln%' 
    AND year = 1909 
    AND mint = 'S'
""")
result = cursor.fetchone()
print(f"Taxonomy ID: {result[0]}")  # US-LWCT-1909-S
```

### JavaScript Example  
```javascript
// Load AI-optimized format
const taxonomy = require('./data/ai-optimized/us_taxonomy.json');

// Find series by type code
const lincolnWheat = taxonomy.series.find(s => s.t === 'LWCT');
console.log(lincolnWheat.coin_ids.split(','));
// ['US-LWCT-1909-P', 'US-LWCT-1909-D', 'US-LWCT-1909-S', ...]
```

## Advanced Features

### Variety Handling
Varieties stored separately from coin IDs:
```json
{
  "coin_id": "US-LWCT-1909-S",
  "varieties": [
    {"name": "VDB", "description": "Designer initials on reverse"}
  ]
}
```

### Composition Tracking
Precise metal content with transition dates:
- 90% silver dimes/quarters: 1796-1964
- Wartime silver nickels: 1942-1945 (35% silver)
- Clad coinage: 1965-present

### Key Date Identification  
39 verified key dates with market-based rarity:
- `US-MERC-1916-D` - King of Mercury dimes
- `US-LWCT-1909-S` - VDB variety
- `US-WASH-1932-D` - First year key date

## Resources

- **[Live Demo](https://mattsilv.github.io/coin-taxonomy/)** - Search interface
- **[Developer Guide](docs/CONTRIBUTING_DEVELOPERS.md)** - Schema docs
- **[Research Notes](docs/coin-research.md)** - Mintage analysis
- **[Series Registry](data/universal/series_registry.json)** - All type codes
- **[Composition Data](data/universal/composition_registry.json)** - Metal content

## Data Quality

- **Sources:** PCGS, NGC, Red Book, US Mint
- **Validation:** JSON Schema + automated tests
- **Coverage:** 1,539+ coins, 48+ series (1793-present)
- **Updates:** Git-tracked with full audit trail

## License

MIT License - Open source for commercial and non-commercial use.

For numismatic tools and updates: **[silv.app](https://www.silv.app)**