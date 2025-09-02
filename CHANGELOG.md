# Changelog

All notable changes to the US Coin Taxonomy project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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