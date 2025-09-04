# Schema Alignment & Three-Cent Pieces Update (v2.1.0)

**Date:** 2025-09-04  
**Version:** 2.1.0  
**Issues:** #50, #57  
**Type:** Major Update with Breaking Changes

## Summary

This release adds Three-Cent Pieces to the taxonomy and fixes critical schema alignment issues between the database and export scripts. The pre-commit validation system has been redesigned to be less brittle and follow single source of truth principles.

## 🚨 Breaking Changes

### Export Column Mappings
The following column mappings have changed in export scripts:
- `series` → `series_id` in AI taxonomy export
- `variety` → `varieties` in all exports  
- `country_code` → `country` in universal export

### Test Structure Changes
- GitHub Pages tests now expect `coins` array, not `series`
- Tests check for `series_id` field, not `series`
- Universal export warnings are now non-blocking

### Removed Features
- Category/subcategory columns (not present in current schema)
- Hard-coded category validation
- Seller/marketplace functionality (out of scope)

## New Features

### Three-Cent Pieces (#50)
Added 51 Three-Cent Pieces to the database:

**Silver Three-Cent Pieces (26 coins)**
- Type I (1851-1853): 6 coins, 75% silver, no star outlines
- Type II (1854-1858): 5 coins, 90% silver, three star outlines
- Type III (1859-1873): 15 coins, 90% silver, two star outlines

**Nickel Three-Cent Pieces (25 coins)**
- Years: 1865-1889
- Composition: 75% copper, 25% nickel
- All Philadelphia mint

### Schema Alignment Fixes (#57)
- Fixed export scripts to use actual database columns
- Established database as single source of truth
- Removed assumptions about non-existent columns

### Improved Pre-commit Validation
- Less brittle, follows single source of truth (database → JSON)
- Better error messages with actionable guidance
- Non-critical checks show warnings instead of failing

## Migration Instructions

### For JSON File Consumers

Update your code to check both old and new field names:

```javascript
// Old way
const series = coin.series;

// New way - backward compatible
const series = coin.series_id || coin.series;
const varieties = coin.varieties || coin.variety;
```

### For Database Users

The core `coins` table schema remains unchanged. New Three-Cent coins use these IDs:
- Silver: `US-TCST-YYYY-M` (e.g., `US-TCST-1851-O`)
- Nickel: `US-TCNT-YYYY-M` (e.g., `US-TCNT-1865-P`)

### For CI/CD Pipelines

Update your tests and validation:
1. Check for `coins` array instead of `series` in us_coins_complete.json
2. Test for `series_id` field instead of `series`
3. Pre-commit hook warnings for universal export are now non-blocking

## Data Updates

- **Database:** 51 new Three-Cent Pieces added (609 total coins)
- **New JSON file:** `data/us/coins/three_cents.json`
- **Updated:** All export scripts to use correct schema

## API Changes

### Coin Object Structure
```json
{
  "coin_id": "US-TCST-1851-O",
  "year": 1851,
  "mint": "O",
  "denomination": "Three Cents",
  "series_id": "Silver Three-Cent Type I",  // was "series"
  "series_name": "Silver Three-Cent Type I",
  "varieties": [{"id": "type_i", "name": "Type I"}],  // was "variety"
  "composition": {"silver": 75.0, "copper": 25.0}
}
```

## Files Changed

### Modified Scripts
- `scripts/export_from_database.py` - Fixed column mappings
- `scripts/export_ai_taxonomy.py` - Updated for actual schema
- `scripts/export_db_v1_1.py` - Fixed universal export
- `scripts/data_integrity_check.py` - Removed hard-coded validation
- `scripts/test_github_pages.js` - Tests actual data structure
- `.git/hooks/pre-commit` - Redesigned for robustness

### New Scripts
- `scripts/add_three_cent_pieces.py` - Migration for Three-Cent Pieces

## Testing

Run these commands to verify the update:

```bash
# Check Three-Cent Pieces in database
sqlite3 database/coins.db "SELECT COUNT(*) FROM coins WHERE coin_id LIKE 'US-TC%'"
# Should return: 51

# Verify exports work
uv run python scripts/export_from_database.py

# Run pre-commit validation
bash .git/hooks/pre-commit
```

## Support

For questions or issues:
- GitHub Issues: https://github.com/mattsilv/coin-taxonomy/issues
- Schema questions: See Issue #57
- Three-Cent Pieces: See Issue #50

---

[Back to Release Notes](./README.md)