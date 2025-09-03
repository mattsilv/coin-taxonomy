# Release Notes

## v1.3.0 - Auction & Marketplace Integration (2025-09-03)

### Features
- **Auction Catalog Parser** (#54)
  - Parse auction listings extracting year, mint mark, coin type, and grades
  - Detect special varieties (overdates, proofs, errors)
  - Map listings to coin variants with confidence scoring
  - Support batch processing with statistics

- **Marketplace Listing Matcher** (#56)
  - Fuzzy matching for typos and abbreviations
  - Hierarchical variant resolution (special → base)
  - Priority-based ambiguous resolution
  - Confidence scoring for match quality

### Database Enhancements
- Added priority scoring system for base variants
- Created `variant_priority_rules` documentation table
- Updated existing variants with proper priority scores

### Testing
- Comprehensive test suite for auction/marketplace features
- All 23 tests passing

### Files Added
- `scripts/auction_catalog_parser.py` - Parse auction catalog listings
- `scripts/marketplace_listing_matcher.py` - Fuzzy match marketplace listings  
- `scripts/update_variant_priority_scores.py` - Set variant priority scores
- `tests/test_auction_marketplace_integration.py` - Integration tests

---

## Previous Releases

### v1.2.0 - Canada Phase 3 Complete
- Added modern Canadian coins and bullion series
- Maple Leaf bullion programs (Gold, Silver, Platinum, Palladium)
- Canadian Sovereign gold coins

### v1.1.0 - Universal Taxonomy Migration
- Migrated to universal v1.1 format
- Added category/subcategory classification
- Standardized coin vs currency fields

### v1.0.0 - Initial Release
- US coin taxonomy with 2,572 coins
- SQLite database as source of truth
- JSON export pipeline
- GitHub Pages browser interface