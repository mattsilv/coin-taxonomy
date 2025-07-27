# United States Coin Taxonomy Database

A comprehensive, structured database of US coin series, mintages, varieties, and key dates from 1859 to present.

## Project Goals

The goal of this project is to create a **unified taxonomy structure** that enables AI systems to accurately classify coins and better connect buyers and sellers in the age of artificial intelligence. By providing standardized, machine-readable coin data with consistent identifiers and comprehensive metadata, this database serves as a foundation for:

- **AI-powered coin identification** and classification systems
- **Automated marketplace matching** between buyer needs and seller inventory
- **Price analysis and market research** with reliable historical data
- **Numismatic education** through structured, validated information

## Overview

This project provides a machine-readable taxonomy of United States coins with:

- **Complete series coverage**: All major US coin denominations from cents to dollars
- **Detailed mintage data**: Business strikes and proof mintages from authoritative sources
- **Key date identification**: Coins marked by rarity status (key, semi-key, scarce, common)
- **Variety tracking**: Major overdates, doubled dies, and mint errors
- **Composition periods**: Accurate metal content through time
- **Source attribution**: Citations from PCGS CoinFacts, NGC, Red Book, US Mint records

## Project Structure

```
coin-taxonomy/
   data/                    # JSON source files organized by country
      us/
          schema/          # JSON Schema validation
          coins/           # Coin series data files
          references/      # Supporting reference data
          us_coins_complete.json  # Complete taxonomy (convenience file)
   scripts/                 # Database and utility scripts
   docs/                    # Documentation and research
   examples/                # Sample usage files
   database/               # Generated SQLite database (gitignored)
```

## Key Features

### Comprehensive Data Coverage

- **20 major series** across 5 denominations
- **105 individual coin entries** with full attribution
- **39 key dates** identified with rarity status
- **33 major varieties** documented with descriptions

### Database-First Architecture

The SQLite database serves as the source of truth, with JSON files for version control:

1. **JSON files**: Human-readable, version-controlled source data
2. **SQLite database**: Optimized for queries and analysis
3. **Export scripts**: Generate comprehensive datasets for testing

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

3. **Verify installation:**
   ```bash
   # Test that validation works
   uv run python scripts/validate.py
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
```

## Data Structure

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
  "coin_id": "MD-1916-D",
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
- **`export_db.py`**: Exports database back to JSON files
- **`export_us_complete.py`**: Generates single comprehensive US taxonomy file

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

### Expanding Beyond US Coins

We welcome contributions to expand this taxonomy beyond United States coins. If you have expertise in coins from other countries and are interested in contributing to create a truly global numismatic taxonomy, please feel free to reach out.

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