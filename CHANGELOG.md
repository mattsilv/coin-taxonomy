# Changelog

All notable changes to the US Coin Taxonomy project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0] - 2025-09-04

### Added
- **Three-Cent Pieces** (#50)
  - Added 51 Three-Cent Pieces to the database
  - Silver Three-Cent Type I (1851-1853): 6 coins, 75% silver
  - Silver Three-Cent Type II (1854-1858): 5 coins, 90% silver
  - Silver Three-Cent Type III (1859-1873): 15 coins, 90% silver
  - Nickel Three-Cent (1865-1889): 25 coins, 75% copper/25% nickel
  - Complete composition, variety, and mintage data included

### Fixed
- **Critical Schema Alignment Issues** (#57)
  - Fixed export scripts expecting non-existent database columns
  - Corrected column mappings: `series` → `series_id`, `variety` → `varieties`
  - Fixed universal export using wrong column names (`country_code` → `country`)
  - Removed hard-coded category validation - categories should come from database
  - Updated all export scripts to use actual database schema

### Changed
- **Pre-commit Hook Improvements**
  - Redesigned to follow single source of truth principle (database → JSON)
  - Made validation less brittle and more forgiving
  - Non-critical checks (universal export, data integrity) now show warnings instead of failing
  - Improved error messages with actionable guidance
  - Tests now check actual data structure instead of theoretical schemas

### Removed
- Hard-coded category/subcategory validation (columns don't exist in current schema)
- Seller/marketplace functionality (out of scope for taxonomy project)

## [2.0.1] - 2025-09-03

### Added
- **Hierarchical Variant Resolution System** (#56)
  - Implemented parent-child relationships between coin variants for intelligent auction mapping
  - Added 4-level hierarchy: Base Variant → Major Variety → Special Variety → Strike Type
  - Database schema enhancements:
    - `parent_variant_id` column for variant relationships
    - `resolution_level` column for hierarchy depth (1-4)
    - `is_base_variant` boolean flag for base identification
    - `priority_score` integer for ambiguous case resolution
  - Created `auction_mapping` view for simplified variant queries
  - Implemented `VariantResolver` class with Python API and CLI interface
  - Added comprehensive test suite with 16 tests, all passing
  - Performance: < 10ms average resolution time (typically ~0.4ms)
  
### Enhanced
- Variant resolution with priority rules:
  - 1864 Two Cent: Defaults to Large Motto (priority 100) over Small Motto (priority 50)
  - 1913 Buffalo Nickel: Defaults to Type 2 (priority 100) over Type 1 (priority 50)
- Parent-child relationships established:
  - 75 base variants identified and marked
  - 11 parent-child relationships created (e.g., 1918-D 8/7 → 1918-D base)
  - Special varieties properly linked to their base variants

### Documentation
- Added `docs/HIERARCHICAL_VARIANT_RESOLUTION.md` - Complete system documentation
- Created `scripts/variant_resolver.py` - Resolution functions with CLI
- Added `tests/test_hierarchical_variant_resolution.py` - Comprehensive test coverage
- Migration script: `scripts/migrate_hierarchical_variant_resolution.py`

## [2.0.0] - 2025-01-02

### Added
- **Red Book Classification System Alignment** (#48)
  - Implemented industry-standard Red Book (A Guide Book of United States Coins) classification hierarchy
  - Added `red_book_categories` table with 36-category hierarchical structure
  - Created three-level classification: Major Categories → Type Categories → Series
  - Mapped all 2,217 existing US coins to appropriate Red Book categories
  - Generated comprehensive alignment analysis documentation
  - Identified 15 missing dataset categories with priority rankings

### Enhanced
- Database schema with `red_book_category_id` foreign keys in coins and series_registry tables
- Data organization to support hierarchical browsing by Red Book categories
- Export capabilities to include Red Book categorization metadata

### Documentation
- Added `docs/red_book_alignment_analysis.md` - Complete alignment analysis
- Added `data/red_book_missing_data_report.json` - Missing datasets report
- Created GitHub issues #49-#53 for high-priority missing datasets

### Data Coverage
- 60% of Red Book categories populated with existing data
- Fully covered: Small Cents, Nickels, Gold Dollars, Quarter Eagles, Half Eagles, Eagles, Double Eagles
- Substantial coverage: Large Cents, Dimes, Quarters, Half Dollars, Silver Dollars
- Identified gaps: Two-Cent Pieces, Three-Cent Pieces, Commemoratives, Bullion coins

## [1.5.0] - 2025-01-02

### Added
- Category and subcategory fields for coin classification (#47)
  - Added `category` field: coin vs currency distinction
  - Added `subcategory` field: circulation, bullion, commemorative classifications
  - Implemented validation in pre-commit hooks
  - Updated all 2,217 US coins with appropriate categorizations

### Fixed
- Pre-commit hook validation for category/subcategory fields
- Data integrity checks for new classification fields

## [1.4.0] - 2025-01-01

### Added
- Canada Phase 3: Modern coins and bullion series (#42)
  - 350 modern Canadian coins (1965-2024)
  - Complete bullion series: Gold, Silver, Platinum, Palladium Maple Leafs
  - Special commemoratives and collector coins
  - Updated taxonomy summary to reflect 2 countries

### Enhanced
- Integration guide for external systems
- API documentation for taxonomy access
- Webhook examples for real-time updates

## [1.3.0] - 2024-12-31

### Added
- Canada Phase 2: Confederation era coins (#41)
  - 450 coins from 1858-1964
  - George V and George VI series
  - Elizabeth II early reign
  - Complete denomination coverage

## [1.2.0] - 2024-12-30

### Added
- Canada Phase 1: Pre-Confederation coinage (#40)
  - Historical provincial coins (1858-1867)
  - Bank tokens and merchant tokens
  - Early colonial issues

## [1.1.0] - 2024-12-15

### Added
- Universal taxonomy format v1.1
- Cross-country compatibility layer
- Enhanced metadata fields
- Variety tracking improvements

## [1.0.0] - 2024-12-01

### Initial Release
- Complete US coin taxonomy (1792-2024)
- 2,217 individual coin entries
- 69 distinct series
- Database-first architecture
- JSON export pipeline
- Pre-commit validation hooks
- GitHub Pages browser interface