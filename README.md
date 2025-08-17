# United States Coin Taxonomy Database

**A Professional-Grade Numismatic Database for the Digital Age**

This is a comprehensive, structured database containing 426+ US coins from 1793 to present, with complete mintage data, composition tracking, and variety documentation. Built specifically for coin professionals, researchers, and AI applications.

**🌐 [View Live Demo](https://mattsilv.github.io/coin-taxonomy/)** - Interactive search and filtering interface

## Why This Database Exists

The numismatic world needs **standardized, machine-readable coin data**. This project solves three critical problems:

1. **Inconsistent coin identification** across marketplaces and databases
2. **Scattered composition data** making silver content verification difficult  
3. **Lack of parseable identifiers** for AI and automated systems

**The Solution: Standardized Coin IDs** - Every coin gets a consistent `COUNTRY-TYPE-YEAR-MINT` identifier (like `US-LWCT-1909-S`) that both humans and machines can reliably parse and understand.

## Applications

- **AI-powered coin identification** from photos using computer vision
- **Marketplace automation** connecting buyers and sellers with precise matching
- **Academic research** with reliable, structured numismatic data
- **Professional attribution** using consistent terminology and standards

## What This Project Provides

This is a **machine-readable numismatic database** designed for the age of AI and digital marketplaces. For coin experts and taxonomy professionals, this project offers:

### Core Numismatic Data
- **Complete US coin coverage**: All major series from 1793-present (cents through dollars)
- **Authoritative mintage figures**: Business strikes and proof mintages from PCGS, NGC, Red Book, US Mint
- **Verified key dates**: 39 confirmed key dates with rarity classifications based on market data
- **Major varieties documented**: 33 varieties including overdates, doubled dies, design changes
- **Precise composition data**: Accurate metal content with exact transition dates (e.g., 1965 silver-to-clad)

### Technology Innovation for Numismatics
- **Standardized coin IDs**: Every coin has a consistent `COUNTRY-TYPE-YEAR-MINT` identifier that software can parse reliably
- **AI-optimized formats**: Token-efficient exports for machine learning and computer vision applications
- **Database architecture**: SQLite backend enables complex queries and analysis of numismatic patterns
- **Version-controlled taxonomy**: Git tracking of all changes with full audit trail

### Quality Standards
- **Source attribution**: Every data point cites authoritative numismatic sources
- **Schema validation**: JSON Schema ensures structural consistency across all data
- **Composition accuracy**: Metal content matches official US Mint specifications
- **Professional verification**: Data cross-referenced against multiple expert sources

## Project Structure

```
coin-taxonomy/
   data/                    # JSON source files organized by country
      us/
          schema/          # JSON Schema validation
          coins/           # Coin series data files
          references/      # Supporting reference data
          us_coins_complete.json  # Complete taxonomy (convenience file)
      ai-optimized/        # Token-optimized format for AI/ML systems
          us_taxonomy.json # Enhanced format with visual descriptions (85KB)
   scripts/                 # Database and utility scripts
   docs/                    # Documentation and research
   examples/                # Sample usage files
   database/               # Generated SQLite database (gitignored)
```

## Key Features

### Current Database Statistics

- **426+ coins** across all major US denominations
- **20+ coin series** from Large Cents (1793) to modern issues
- **Comprehensive silver periods**: War nickels (1942-1945), dimes (1946-1964), quarters, half dollars
- **Complete composition tracking**: Every metal change from 1793 copper to modern clad
- **Key date coverage**: All major rarities including 1909-S VDB, 1916-D Mercury, 1932-D Washington

### Database-First Architecture

⚠️ **CRITICAL**: SQLite database is the SINGLE SOURCE OF TRUTH for all coin data.

⚠️ **NEVER EDIT JSON FILES DIRECTLY** - They are generated artifacts!

### Data Flow (READ THIS CAREFULLY):
```
SQLite Database → JSON Export Files  
      ↑                    ↑
SOURCE OF TRUTH      GENERATED FILES
(version controlled)  (version controlled)
```

### Pre-Commit Hook Integration:
- **All commits trigger automatic export** from SQLite database
- **JSON files regenerated** automatically via pre-commit hooks
- **Database is version controlled** and committed to git
- **Add new coins directly to database** using migration scripts

### Workflow Rules:
1. **SQLite database is the source of truth** - version controlled and committed to git
2. **JSON files are generated artifacts** - exported from database via pre-commit hooks
3. **Add new coins using migration scripts** - modify database directly
4. **NEVER edit JSON files manually** - they will be overwritten on next commit
5. **Export JSON files from database**: `uv run python scripts/export_from_database.py`

### Validation and Quality Control

- JSON Schema validation ensures data consistency
- Automated testing of all coin data files
- Source citation tracking for data verification

## Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) for dependency management

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mattsilv/coin-taxonomy.git
   cd coin-taxonomy
   ```

2. **Set up the development environment:**
   ```bash
   # Create virtual environment
   uv venv
   
   # Activate virtual environment
   source .venv/bin/activate  # Linux/macOS
   # or on Windows: .venv\Scripts\activate
   
   # Install dependencies
   uv add jsonschema
   ```

3. **Generate the database:**
   ```bash
   # Complete rebuild pipeline (runs all migration scripts)
   uv run python scripts/rebuild_and_export.py
   ```

4. **Verify installation:**
   ```bash
   # Test that validation works
   uv run python scripts/validate.py
   
   # Verify database structure
   uv run python scripts/check_db_structure.py
   ```

### Basic Usage

```bash
# Validate all coin data
uv run python scripts/validate.py

# Build SQLite database from JSON sources
uv run python scripts/build_db.py

# Test marketplace listing matcher
uv run python scripts/import_listing.py

# Calculate metal melt values
uv run python scripts/calculate_melt.py

# Export complete US taxonomy to single file
uv run python scripts/export_us_complete.py

# Generate both legacy and universal format exports
uv run python scripts/export_db_v1_1.py

# Run comprehensive data integrity check
uv run python scripts/data_integrity_check.py
```

## Development Workflow

⚠️ **CRITICAL**: Never edit JSON files directly! They are generated artifacts.



### Database Export Process (DATABASE-FIRST)

The canonical way to export JSON files from the SQLite database:

```bash
# Export JSON files from database (DATABASE-FIRST PIPELINE)
uv run python scripts/export_from_database.py
```

This script performs the database-first export:
1. 📊 Reads coins from SQLite database (source of truth)
2. 📁 Generates JSON files by denomination (`data/us/coins/*.json`)
3. 📄 Creates complete taxonomy file (`data/us/us_coins_complete.json`)
4. 🔄 Runs universal migration (`scripts/migrate_to_universal_v1_1.py`)
5. 📁 Exports universal format (`scripts/export_db_v1_1.py`)
6. 🧪 Validates exports (`scripts/validate.py`)
7. 🌐 Copies universal data to docs folder

⚠️ **IMPORTANT**: After adding coins to database, run export and commit ALL generated files with `git add . && git commit`. The export process updates JSON files, universal data, and docs folder - ALL must be committed together.

### Safe Change Process (DATABASE-FIRST)
1. **Add coins to database** using migration scripts (e.g., `scripts/backfill_historical_coins.py`)
2. **Run database export**: `uv run python scripts/export_from_database.py`
3. **Verify export succeeded** - check that all steps pass
4. **Commit ALL changes**: `git add . && git commit` (includes database and generated JSON files)
5. **Database is now version controlled** - commit database changes to git

### Emergency Restore:
- JSON backups: `backups/json_files_*/`
- Database backups: `backups/coins_backup_*.db`
- **Regenerate from migration scripts** if database is lost (best practice)

### Coin ID Format: The Foundation of Everything

The **coin ID** is the most critical identifier in this database. It serves as the primary key that connects all data across systems and makes AI-powered coin identification possible.

#### Why Coin IDs Matter

In the age of AI and automated marketplaces, **consistent, parseable identifiers** are essential for:

- **AI coin identification**: Computer vision systems need reliable IDs to match photos to database entries
- **Marketplace integration**: E-commerce platforms require predictable formats to connect buyers and sellers
- **Price analysis**: Historical tracking and valuation requires stable, unique identifiers across time
- **Database reliability**: SQL queries and joins depend on consistent ID structures

#### Standard Format: `COUNTRY-TYPE-YEAR-MINT`

**Component Definitions:**

1. **COUNTRY** (2-3 letters): ISO-style country code
   - `US` = United States
   - `CA` = Canada  
   - `GB` = Great Britain
   - Future: `FR`, `DE`, `JP`, etc.

2. **TYPE** (4 letters): Standardized 4-letter series abbreviation identifying the coin design/series
   
   **Cents:**
   - `INCH` = Indian Head Cent
   - `LWCT` = Lincoln Wheat Cent  
   - `LMCT` = Lincoln Memorial Cent
   - `LBCT` = Lincoln Bicentennial Cent
   - `LSCT` = Lincoln Shield Cent
   
   **Nickels:**
   - `SHLD` = Shield Nickel
   - `LHNI` = Liberty Head Nickel
   - `BUFF` = Buffalo Nickel
   - `JEFF` = Jefferson Nickel
   
   **Dimes:**
   - `BARD` = Barber Dime
   - `MERC` = Mercury Dime (Winged Liberty Head)
   - `ROOS` = Roosevelt Dime
   
   **Quarters:**
   - `BARQ` = Barber Quarter
   - `SLIQ` = Standing Liberty Quarter
   - `WASH` = Washington Quarter
   
   **Dollars:**
   - `MORG` = Morgan Dollar
   - `PEAC` = Peace Dollar
   - `EISE` = Eisenhower Dollar
   - `SANT` = Susan B. Anthony Dollar
   - `SACA` = Sacagawea Dollar

3. **YEAR** (4 digits): The year the coin was minted
   - `1877`, `1909`, `1942`, `2024`

4. **MINT** (1-2 letters): US Mint facility where coin was produced
   - `P` = Philadelphia
   - `D` = Denver
   - `S` = San Francisco
   - `CC` = Carson City (historical)
   - `W` = West Point
   - `O` = New Orleans (historical)
   - `X` = Unknown mint mark (when uncertain or not visible)

#### Mapping Conventions for Unknown Data

When exact information is unknown or uncertain:

- **Unknown Year**: Use `YYYY` as placeholder (e.g., `US-LWCT-YYYY-P`)
- **Unknown Mint Mark**: Use `X` as placeholder (e.g., `US-LWCT-1909-X`)
- **Both Unknown**: Use both placeholders (e.g., `US-LWCT-YYYY-X`)

This enables consistent mapping of incomplete coin data while maintaining the standardized format.

**Examples:**
- `US-INCH-1877-P` = US Indian Head Cent, 1877, Philadelphia mint  
- `US-LWCT-1909-S` = US Lincoln Wheat Cent, 1909, San Francisco mint (famous VDB variety)
- `US-MERC-1942-D` = US Mercury Dime (Winged Liberty Head), 1942, Denver mint
- `US-LWCT-YYYY-X` = Lincoln Wheat Cent with unknown year and mint (for damaged coins)

## For Coin Experts: Why This Matters

This database solves real problems facing the numismatic community:

### **Marketplace Identification Crisis**
- eBay listings often misidentify coins due to inconsistent naming
- This database provides **standardized identifiers** that sellers and buyers can rely on
- AI-powered classification can automatically match photos to correct entries

### **Research and Analysis**
- **Composition tracking**: Instantly identify silver content periods for any denomination
- **Mintage analysis**: Compare production figures across series and years
- **Key date verification**: Authoritative rarity classifications based on market data

### **Educational Applications**
- **Systematic learning**: Structured progression through coin series
- **Visual identification**: Detailed descriptions help distinguish similar coins
- **Historical context**: Design periods and composition changes in chronological order

### **Professional Tools**
- **Database queries**: Find all coins from specific years, mints, or composition periods
- **Variety tracking**: Separate major varieties from base coin types
- **Attribution standards**: Consistent terminology across the entire hobby

**Validation Rules:**
- **Exactly 4 parts** separated by **exactly 3 dashes**
- **All uppercase letters** (no lowercase allowed)
- **No variety information** in the coin_id (goes in `varieties` array instead)
- **Consistent abbreviations** across all series

#### What This Enables

With standardized coin IDs, developers can:
- **Parse components**: `coin_id.split('-')` reliably returns `[country, type, year, mint]`
- **Query predictably**: `WHERE coin_id LIKE 'US-INCH-%'` finds all US Indian Head Cents
- **Filter by country**: `WHERE coin_id LIKE 'US-%'` finds all US coins
- **Join tables safely**: Foreign key relationships work consistently across systems
- **Build integrations**: APIs and services can depend on the format

#### Common Mistakes (Now Prevented)

❌ **Invalid formats** that break parsing:
- `INCH-1864-P-L` (missing country prefix, variety in main ID)
- `US-LWCT-1909-S-VDB` (5 parts - VDB goes in `varieties`)
- `US-MERC-1942-P-21` (5 parts - overdate info goes in `varieties`)

✅ **Correct format** with variety data properly separated:
```json
{
  "coin_id": "US-INCH-1864-P",
  "varieties": [
    {
      "variety_id": "INCH-1864-P-L-01", 
      "name": "L on Ribbon",
      "description": "Designer's initial L on ribbon"
    }
  ]
}
```

## Data Structure

### Universal Currency Taxonomy (v1.1)

As of v1.1, this project supports a **Universal Currency Taxonomy** that can accommodate coins and banknotes from any country and time period. The system uses a flat, normalized structure that replaces the previous nested format while maintaining full backward compatibility.

#### Database-First Architecture

The SQLite database (`database/coins.db`) serves as the **single source of truth**. All JSON exports are generated from the database:

```
database/coins.db (source of truth)
    ↓ (export via scripts)
data/us/coins/*.json (legacy format - backward compatibility)
data/universal/*.json (new universal format)
data/ai-optimized/us_taxonomy.json (AI-optimized format)
```

#### Universal Tables

The new v1.1 schema includes these core tables:

**`issues` table**: Flat structure for all currency items
- Universal issue IDs (e.g., `US-LWCT-1909-S`)
- Country-agnostic denomination and authority data
- JSON fields for specifications, design details, mintage data

**Registry Tables**: Normalized reference data
- `subject_registry`: People, symbols, design elements (8 entries)
- `composition_registry`: Alloy definitions (8 standard compositions)  
- `series_registry`: Series metadata across all countries

#### Export Formats

**Legacy Format** (`data/us/coins/*.json`): Preserves existing nested structure
```json
{
  "country": "United States",
  "denomination": "Cents",
  "series": [
    {
      "series_name": "Lincoln Wheat Cent",
      "coins": [...]
    }
  ]
}
```

**Universal Format** (`data/universal/*.json`): New flat structure
```json
{
  "country_code": "US", 
  "total_issues": 97,
  "issues": [
    {
      "issue_id": "US-LWCT-1909-S",
      "object_type": "coin",
      "issuing_entity": {...},
      "denomination": {...},
      "specifications": {...}
    }
  ]
}
```

**AI-Optimized Format**: Two specialized formats optimized for AI/ML systems with different efficiency profiles:

**Year-List Format** (`data/ai-optimized/us_taxonomy_year_list.json`): Most efficient (10K tokens, 33KB)
```json
{
  "format": "ai-taxonomy-v2-years",
  "approach": "comma-delimited year lists",
  "series": [
    {
      "series": "lincoln_wheat_cent",
      "s": "Lincoln Wheat Cent",
      "t": "LWCT",
      "years": "1909,1910,1911,1912,1913,1914,1915,1916,1917,1918,1919,1920",
      "year_range": "1909-1958",
      "ob": "Abraham Lincoln bust facing right...",
      "rv": "Two wheat stalks flanking 'ONE CENT'..."
    }
  ]
}
```

**Coin-ID Format** (`data/ai-optimized/us_taxonomy.json`): Comprehensive (26K tokens, 61KB)
```json
{
  "format": "ai-taxonomy-v2-coinids", 
  "approach": "complete coin ID lists",
  "series": [
    {
      "series": "lincoln_wheat_cent",
      "s": "Lincoln Wheat Cent", 
      "t": "LWCT",
      "coin_ids": "US-LWCT-1909-P,US-LWCT-1909-D,US-LWCT-1909-S,US-LWCT-1910-P,US-LWCT-1910-D,US-LWCT-1910-S",
      "year_range": "1909-1958"
    }
  ]
}
```

**Format Comparison**:
| Format | File Size | Tokens | GPT-4 Context | Use Case |
|--------|-----------|--------|---------------|----------|
| Year-List | 33KB | 10,150 | 7.9% | Year-based classification, GPT-3.5 compatible |
| Coin-ID | 61KB | 26,054 | 20.4% | Exact coin matching, marketplace applications |

Both formats provide:
- **Series-based grouping** to reduce redundancy
- **Complete year coverage** for all production periods  
- **Visual descriptions** for accurate coin identification
- **Abbreviated field names** to minimize token usage
- **Token-optimized structure** for AI/ML applications

#### Issue ID Generation

The universal system uses human-readable, standardized issue IDs:

**Format**: `{COUNTRY}-{SERIES_ABBREV}-{YEAR}-{MINT}[-{VARIETY}]`

**Examples**:
- `US-LWCT-1909-S` - 1909-S Lincoln Wheat Cent
- `US-MERC-1916-D` - 1916-D Mercury Dime  
- `US-WASH-1932-D` - 1932-D Washington Quarter

**Generation Logic**: 
- Country code (ISO-style)
- Series abbreviation (first 3 chars of series_id, uppercase)
- Year, mint mark, optional variety identifier

### Complete Taxonomy File

For convenience, a complete US coin taxonomy is available in a single file:
- **Location**: `data/us/us_coins_complete.json`
- **Content**: All denominations, series, and coins in one unified structure
- **References**: Includes resolved composition data and all reference files
- **Generation**: Updated via `scripts/export_us_complete.py`

This file combines all individual denomination files with resolved composition references, making it easy to access the entire taxonomy without loading multiple files.

### Series Information

Each coin series includes:

- **Basic metadata**: Official name, years of production, designers
- **Physical specifications**: Diameter, thickness, edge details
- **Composition periods**: Metal content with date ranges
- **Complete mintages**: Business strikes and proof production with unique identifiers

### Individual Coins

Each coin entry contains:

- **Unique identifiers**: Stable coin_id fields for programmatic access
- **Mintage figures**: Separate business_strikes and proof_strikes quantities
- **Rarity classification**: Key date status (key/semi-key/scarce/common)
- **Variety arrays**: Structured variety information with variety_id fields
- **Source attribution**: Citation to authoritative numismatic sources
- **Additional notes**: Context about significance or special characteristics

### Example Entry

```json
{
  "coin_id": "US-MERC-1916-D",
  "year": 1916,
  "mint": "D",
  "business_strikes": 264000,
  "proof_strikes": null,
  "rarity": "key",
  "source_citation": "PCGS CoinFacts",
  "notes": "King of Mercury dimes"
}
```

## Scripts and Tools

### Core Scripts

- **`validate.py`**: Validates all JSON files against schema
- **`build_db.py`**: Builds SQLite database from JSON sources
- **`migrate_db.py`**: Safely updates database schema
- **`export_db.py`**: Exports database back to JSON files (legacy format)
- **`export_db_v1_1.py`**: Enhanced export with both legacy and universal formats
- **`export_us_complete.py`**: Generates single comprehensive US taxonomy file

### Migration Scripts (v1.1)

- **`migrate_to_universal_v1_1.py`**: Complete migration to universal taxonomy
- **`fix_face_values.py`**: Data correction utilities
- **`data_integrity_check.py`**: Comprehensive validation and integrity checking

### Analysis Tools

- **`import_listing.py`**: Matches marketplace listings to canonical data
- **`calculate_melt.py`**: Calculates metal melt values based on composition

## Data Sources

All data compiled from authoritative numismatic sources:

- **PCGS CoinFacts** (pcgs.com/coinfacts)
- **NGC Coin Explorer** (ngccoin.com)
- **The Red Book** (Official Guide Book of United States Coins)
- **US Mint Records** (usmint.gov historical data)
- **Specialized references**: Expert sites for specific series

## Contributing

This project follows strict data quality standards:

1. **Source attribution required**: All data must cite authoritative sources
2. **Schema validation**: All changes must pass JSON Schema validation
3. **Key date verification**: Rarity classifications must be supported by market data
4. **Composition accuracy**: Metal content must match official mint specifications

### For Developers

See the **[Developer Contribution Guide](docs/CONTRIBUTING_DEVELOPERS.md)** for detailed information on:
- Universal schema architecture and design patterns
- Adding new currency data (coins and banknotes)
- Database operations and safety procedures
- Testing and validation processes
- Code standards and best practices

### For Numismatists  

We welcome contributions to expand this taxonomy beyond United States coins. If you have expertise in coins from other countries and are interested in contributing to create a truly global numismatic taxonomy, please feel free to reach out.

The v1.1 universal structure makes it straightforward to add:
- **International currencies** from any country or time period
- **Historical monetary systems** (pre-decimal, non-standard)
- **Banknotes and paper currency** with minimal schema changes
- **Complex authority relationships** (regime changes, successions)

For project updates and related numismatic tools, visit: **[silv.app](https://www.silv.app)**

## Research Methodology

The research document (`docs/coin-research.md`) provides detailed analysis of:

- Complete mintage figures for all series
- Key date identification and market significance
- Major variety documentation with estimated populations
- Composition changes with exact transition dates
- Authoritative source verification

## Open Source Release

**Project Status**: Ready for open source release

- Complete data coverage of major US coin series
- Validated against authoritative sources
- Comprehensive testing and quality control
- Well-documented codebase and data structure
- Database architecture supporting future expansion

## License

MIT License - see repository settings for full license text.

## Acknowledgments

Special thanks to the numismatic community and organizations that maintain the authoritative sources this project relies upon, including PCGS, NGC, and the publishers of the Red Book.