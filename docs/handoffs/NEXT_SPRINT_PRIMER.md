# Next Sprint Primer - Red Book Classification Sprint

## Sprint Goal
Complete the Red Book Classification foundation by adding the remaining high-priority US coin series that are essential for collector applications.

## Context from v1.3.0
- ✅ **Issue #47 COMPLETE**: Standardized category/subcategory fields implemented
  - All 2,592 coins now properly categorized (coin/circulation, coin/bullion, etc.)
  - Pre-commit validation ensures data integrity
  - Foundation laid for currency, tokens, and exonumia

## How This Codebase Works

### Database-First Workflow (CRITICAL)
```
SQLite Database (source of truth) → Export Scripts → JSON Files (generated)
        ↑                                                     ↓
   Migration Scripts                               GitHub Pages Site
```

**NEVER edit JSON files directly!** They're regenerated on every commit.

### Development Cycle
1. Write migration script in `/scripts/`
2. Run migration: `uv run python scripts/your_migration.py`
3. Export to JSON: `uv run python scripts/export_from_database.py`
4. Commit everything: `git add . && git commit -m "Your message"`
5. Pre-commit hooks validate and regenerate all files

## Priority Issues for This Sprint

### Priority 1: Issue #51 - American Silver Eagles (1986-2025)
**Why Critical**: Most popular modern US bullion series, essential for collectors
**Direct Link**: https://github.com/mattsilv/coin-taxonomy/issues/51

```python
# Migration template for scripts/add_american_silver_eagles.py
def add_silver_eagles():
    """Add American Silver Eagle bullion coins."""
    coins = []
    
    # Regular bullion strikes
    for year in range(1986, 2026):
        coins.append({
            'coin_id': f'US-ASE1-{year}-P',
            'series_name': 'American Silver Eagle',
            'denomination': 'dollars',
            'year': year,
            'mint': 'P',
            'category': 'coin',
            'subcategory': 'bullion',
            'composition': {'silver': 99.9},
            'weight_grams': 31.103,
            'diameter_mm': 40.6,
            # Add mintages from Red Book 2025
        })
    
    # Don't forget W mint proofs, burnished, reverse proofs!
    return coins
```

### Priority 2: Issue #52 - American Gold Eagles & Buffalos (1986-2025)
**Why Critical**: Essential gold bullion series for serious collectors
**Direct Link**: https://github.com/mattsilv/coin-taxonomy/issues/52

```python
# Four denominations to handle:
denominations = {
    '$5': {'weight': 3.393, 'diameter': 16.5},   # 1/10 oz
    '$10': {'weight': 8.483, 'diameter': 22.0},  # 1/4 oz
    '$25': {'weight': 16.966, 'diameter': 27.0}, # 1/2 oz
    '$50': {'weight': 33.931, 'diameter': 32.7}  # 1 oz
}

# Remember Gold Buffalos are separate series starting 2006!
```

### Priority 3: Issue #50 - Three-Cent Pieces (Silver & Nickel)
**Why Critical**: Unique denomination, key dates highly sought after
**Direct Link**: https://github.com/mattsilv/coin-taxonomy/issues/50

```python
# Two distinct series:
# 1. Silver Three-Cent (1851-1873) - 75% silver Type I, 90% silver Type II/III
# 2. Nickel Three-Cent (1865-1889) - 75% copper, 25% nickel
```

## Implementation Guidance

### 1. Research Data Using AI Guidelines
Check `docs/AI_RESEARCH_GUIDELINES.md` for approved sources:
- Red Book 2025 (primary source)
- PCGS CoinFacts for verification
- US Mint production reports

### 2. Database Schema
Current coins table has all needed fields:
```sql
-- Key fields for new coins:
category TEXT CHECK (category IN ('coin', 'currency', 'token', 'exonumia'))
subcategory TEXT CHECK (subcategory IN ('circulation', 'bullion', 'commemorative', ...))
```

### 3. Coin ID Format
**MUST follow**: `COUNTRY-TYPE-YEAR-MINT`
- `US-ASE1-2021-W` ✅ (American Silver Eagle, 2021, West Point)
- `US-AGE5-1986-P` ✅ (American Gold Eagle $5, 1986, Philadelphia)
- `US-3CS-1851-O` ✅ (Three Cent Silver, 1851, New Orleans)

### 4. Required Fields
```python
{
    'coin_id': 'US-ASE1-2021-W',  # Follows format exactly
    'series_id': 'us-american-silver-eagle',
    'country': 'US',
    'denomination': 'dollars',
    'series_name': 'American Silver Eagle',
    'year': 2021,
    'mint': 'W',
    'category': 'coin',  # Always lowercase
    'subcategory': 'bullion',  # or 'proof' for proof strikes
    'business_strikes': 0,  # From Red Book
    'proof_strikes': 299998,  # From Red Book
    'composition': {
        'silver': 99.9,
        'weight_grams': 31.103,
        'diameter_mm': 40.6
    },
    'obverse_description': 'Walking Liberty by Adolph A. Weinman',
    'reverse_description': 'Heraldic eagle with shield',
    'distinguishing_features': 'Type 2 reverse with enhanced details',
    'identification_keywords': 'ASE, Silver Eagle, bullion, Walking Liberty',
    'common_names': 'Silver Eagle, ASE',
    'source_citation': 'Red Book 2025, p. 379'
}
```

### 5. Varieties Handling
Major varieties go in the `varieties` JSON array:
```python
'varieties': [
    {
        'name': '2008-W Reverse of 2007',
        'description': 'Early 2008 strikes used 2007 reverse die',
        'premium': 'significant'
    }
]
```

## Testing Your Implementation

```bash
# 1. Run your migration
uv run python scripts/add_american_silver_eagles.py

# 2. Export to JSON
uv run python scripts/export_from_database.py

# 3. Check data integrity
uv run python scripts/data_integrity_check.py

# 4. Test pre-commit (this will run automatically on commit)
git add . && git commit -m "Add American Silver Eagles (Issue #51)"
```

## Common Gotchas

1. **JSON files out of sync**: Run export_from_database.py before committing
2. **Category must be lowercase**: 'coin' not 'COIN'
3. **Subcategory required for bullion**: Use 'bullion' or 'proof'
4. **Mint marks**: W=West Point, S=San Francisco, P=Philadelphia (or blank)
5. **Include all strikes**: Business, Proof, Burnished, Enhanced, Reverse Proof

## Success Criteria

- [ ] All years 1986-2025 covered for Eagles
- [ ] All denominations included ($5, $10, $25, $50)
- [ ] Proper categorization (bullion vs proof)
- [ ] Mintages match Red Book 2025
- [ ] Pre-commit hooks pass
- [ ] Data integrity check shows valid categories
- [ ] JSON exports include new coins

## Stretch Goals (if time permits)
- Issue #53: Modern commemoratives
- Issue #54: Pattern coins
- Issue #48: Enhanced variety support

## Questions/Help
- Check existing migrations: `/scripts/backfill_*.py`
- Database schema: `/scripts/implement_universal_taxonomy.py`
- Export process: `/scripts/export_from_database.py`
- Create GitHub issue with tag `question`

## Validation System
This codebase uses **pre-commit hooks only** for validation and data export. No GitHub Actions workflows are needed.

## Why This Matters
These modern bullion series are actively collected and traded. Having accurate, structured data for them enables:
- Price guide integration
- Portfolio tracking
- Variety identification
- Submission to grading services
- Insurance documentation

Good luck! The foundation is solid - just follow the patterns and the pre-commit hooks will catch any issues.