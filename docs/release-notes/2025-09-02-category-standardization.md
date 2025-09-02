# Release Notes: Category Standardization Update
**Date:** September 2, 2025  
**Version:** 1.2.0  
**Issue:** [#47](https://github.com/mattsilv/coin-taxonomy/issues/47)

## Summary

This release implements standardized `category` and `subcategory` fields across the taxonomy system to properly distinguish between different types of numismatic items, following professional numismatic standards.

## Breaking Changes

⚠️ **Database Schema Changes:**
- Added `subcategory` column to `coins` table
- Changed `issues.object_type` from `"banknote"` to `"currency"` for consistency
- All `category` values now use lowercase (was `"COIN"`, now `"coin"`)

## New Features

### 1. Standardized Category Field
All coins now include a `category` field with standardized values:
- `"coin"` - Struck metal pieces
- `"currency"` - Paper money (banknotes)
- `"token"` - Trade or transportation tokens
- `"exonumia"` - Medals, badges, and other numismatic items

### 2. Subcategory Classification
New `subcategory` field for granular filtering:

**For Coins:**
- `"circulation"` - Business strikes (default)
- `"bullion"` - Investment grade (Gold/Silver Eagles, Maple Leafs)
- `"commemorative"` - Special commemorative issues
- `"proof"` - Proof strikes
- `"pattern"` - Trial strikes

**For Currency:**
- `"federal"` - Federal Reserve Notes
- `"certificate"` - Silver/Gold certificates
- `"national"` - National Bank Notes
- `"fractional"` - Fractional currency
- `"confederate"` - Confederate currency
- `"colonial"` - Colonial/Continental currency

### 3. JSON Export Updates
All exported JSON files now include:
```json
{
  "coin_id": "US-BARB-1894-O",
  "category": "coin",
  "subcategory": "circulation",
  // ... other fields
}
```

## Migration Instructions

### For Developers Using Previous Version

1. **Backup Your Database:**
   ```bash
   cp database/coins.db database/coins_backup.db
   ```

2. **Run Migration Script:**
   ```bash
   uv run python scripts/migrate_category_standardization.py
   ```

3. **Re-export JSON Files:**
   ```bash
   uv run python scripts/export_from_database.py
   ```

4. **Update Your Code:**
   - Change any references from `object_type = "banknote"` to `object_type = "currency"`
   - Update any category checks from `"COIN"` to `"coin"` (lowercase)
   - Add handling for the new `subcategory` field if needed

### Database Changes Applied

```sql
-- Add subcategory column
ALTER TABLE coins ADD COLUMN subcategory TEXT;

-- Update category values to lowercase
UPDATE coins SET category = 'coin' WHERE UPPER(category) = 'COIN';

-- Update issues table for consistency
UPDATE issues SET object_type = 'currency' WHERE object_type = 'banknote';
```

## Data Updates

- **2,567** US coins categorized
- **20** Canadian coins categorized
- **82** paper currency entries updated from "banknote" to "currency"
- Automatic subcategory classification based on series names

### Subcategory Distribution
- `circulation`: 2,564 items
- `bullion`: 21 items (Gold/Silver Eagles, Maple Leafs)
- `commemorative`: 2 items

## API Changes

### Coins Table
New fields in `coins` table:
- `category` (TEXT) - Primary classification
- `subcategory` (TEXT) - Secondary classification

### Issues Table
- `object_type` values: `"coin"`, `"currency"` (was `"coin"`, `"banknote"`)

## Benefits

1. **Industry Alignment** - Matches ANA, NGC/PCGS standards
2. **Better Filtering** - Easy to filter coins vs paper money
3. **Future-Proof** - Handles polymer notes, tokens, medals
4. **International** - Works for all countries (US, CA, etc.)

## Files Changed

- `scripts/migrate_category_standardization.py` - New migration script
- `scripts/export_from_database.py` - Updated to export category/subcategory
- `scripts/export_canada_from_database.py` - Updated for Canada coins
- All JSON exports in `data/us/coins/` - Now include category fields
- All JSON exports in `data/ca/` - Now include category fields

## Backward Compatibility

- Existing code reading JSON files will continue to work
- New fields are additive, not replacing existing fields
- Database maintains all existing data

## Testing

Run the following to verify the migration:
```bash
# Check category distribution
sqlite3 database/coins.db "SELECT category, subcategory, COUNT(*) FROM coins GROUP BY category, subcategory"

# Verify JSON includes new fields
jq '.series[0].coins[0] | {coin_id, category, subcategory}' data/us/coins/cents.json

# Check issues table
sqlite3 database/coins.db "SELECT object_type, COUNT(*) FROM issues GROUP BY object_type"
```

## Next Steps

Future enhancements may include:
- Additional subcategories as needed
- Token and exonumia support
- Pattern coin classification
- Proof set tracking

## Support

For questions or issues with this update:
- Open an issue: https://github.com/mattsilv/coin-taxonomy/issues
- Reference Issue #47 for context