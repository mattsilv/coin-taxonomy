# Next Sprint Engineering Primer: Red Book Classification & Modern Bullion
*For engineers new to the coin-taxonomy codebase*

## 🎯 Sprint Goal
Complete the Red Book Classification foundation by adding critical modern bullion series and fixing the schema gap for coin vs currency classification. This directly addresses collector needs and marketplace integration requirements.

## 📚 Quick Context for New Engineers

### What We Just Shipped (v1.3.0)
- **Auction Catalog Parser** ([Issue #54](https://github.com/mattsilv/coin-taxonomy/issues/54)): Parse auction listings → coin variants
- **Marketplace Fuzzy Matching** ([Issue #56](https://github.com/mattsilv/coin-taxonomy/issues/56)): Handle typos, resolve variants
- Both issues were blocking auction/marketplace integration - now resolved ✅

### How This Codebase Works
```
SQLite Database (source of truth) → JSON Exports → Universal Format → GitHub Pages
         ↑                             ↑                              ↑
    All changes               Pre-commit hooks            Live browser at
     start here               auto-generate              mattsilv.github.io
```

**Key Principles:**
1. **Database-First**: NEVER edit JSON files directly - they're generated
2. **Pre-Commit Validation**: Hooks auto-export and validate all changes  
3. **Universal Format v1.1**: Standardized taxonomy for all countries/currencies
4. **Coin ID Format**: `COUNTRY-TYPE-YEAR-MINT` (e.g., `US-AEAG-2024-W`)

## 🔥 Priority 1: Fix Schema Foundation (BLOCKER)

### [Issue #47](https://github.com/mattsilv/coin-taxonomy/issues/47): Implement Category Field
**Why First:** This blocks ALL other data additions. Without it, we can't properly classify coins vs currency.

**Implementation Steps:**
```python
# 1. Add to database schema
ALTER TABLE coins ADD COLUMN category TEXT DEFAULT 'coin';
ALTER TABLE coins ADD COLUMN subcategory TEXT;

# 2. Update for existing records
UPDATE coins SET category = 'coin', subcategory = 'circulating' 
WHERE series_name NOT LIKE '%Proof%';

UPDATE coins SET category = 'coin', subcategory = 'proof' 
WHERE series_name LIKE '%Proof%';

# 3. Update export scripts
scripts/export_from_database.py  # Add category to JSON export
scripts/validate.py              # Validate category field
```

**Testing:**
```bash
# After implementation
uv run python scripts/export_from_database.py
git add . && git commit  # Pre-commit hooks will validate
```

## 🥇 Priority 2: American Silver Eagles (Highest ROI)

### [Issue #51](https://github.com/mattsilv/coin-taxonomy/issues/51): Add Silver Eagles Dataset
**Why:** Most popular modern US coin, massive collector base, straightforward implementation

**Data Structure:**
```python
# Coin IDs follow pattern: US-AEAG-YYYY-M
US-AEAG-1986-S  # First year, San Francisco
US-AEAG-1986-P  # Proof version
US-AEAG-2024-W  # Current year, West Point

# Special variants to include:
- Burnished (W mint, matte finish)
- Proof (W or S mint)
- Reverse Proof 
- Enhanced Reverse Proof
- Emergency Production (P mint, 2021)
```

**Implementation:**
```python
# Create migration script: scripts/add_american_silver_eagles.py
def add_silver_eagles():
    years = range(1986, 2025)
    for year in years:
        # Business strikes (mostly W, some S, P in 2021)
        add_coin(f"US-AEAG-{year}-W", "American Silver Eagle", year, "W")
        
        # Proof versions
        if year >= 1986:
            add_coin(f"US-AEAG-{year}-P", "American Silver Eagle Proof", year, "W")
```

**Key Data Points:**
- Weight: 31.103g (1 troy oz silver)
- Composition: .999 fine silver
- Diameter: 40.6mm
- All are bullion except proofs

## 🥇 Priority 3: American Gold Eagles & Buffalos

### [Issue #52](https://github.com/mattsilv/coin-taxonomy/issues/52): Add Gold Bullion Dataset
**Why:** Major modern bullion series, strong investor demand, complements silver eagles

**Data Structure:**
```python
# American Gold Eagles (4 denominations)
US-AGE5-2024-W   # 1/10 oz ($5)
US-AGE10-2024-W  # 1/4 oz ($10)  
US-AGE25-2024-W  # 1/2 oz ($25)
US-AGE50-2024-W  # 1 oz ($50)

# American Gold Buffalos
US-BUFF50-2024-W # 1 oz ($50) - .9999 fine
```

**Implementation:**
```python
# scripts/add_american_gold_bullion.py
eagles = [
    {"denom": 5, "weight": 3.393, "code": "AGE5"},
    {"denom": 10, "weight": 8.483, "code": "AGE10"},
    {"denom": 25, "weight": 16.966, "code": "AGE25"},
    {"denom": 50, "weight": 33.931, "code": "AGE50"},
]

# Eagles: 1986-present, Buffalos: 2006-present
```

## 🪙 Priority 4: Three-Cent Pieces

### [Issue #50](https://github.com/mattsilv/coin-taxonomy/issues/50): Add Three-Cent Dataset
**Why:** Smaller dataset, important for type collectors, good momentum builder

**Data Structure:**
```python
# Silver Three-Cent (1851-1873)
US-3CS-1851-P  # Type 1 (no lines)
US-3CS-1854-P  # Type 2 (three lines)
US-3CS-1859-P  # Type 3 (two lines)

# Nickel Three-Cent (1865-1889)
US-3CN-1865-P  # All Philadelphia mint
```

## 🛠️ Development Workflow

### 1. Setup Environment
```bash
git clone https://github.com/mattsilv/coin-taxonomy.git
cd coin-taxonomy
uv venv && source .venv/bin/activate
uv add pytest --dev  # If running tests
```

### 2. Database-First Development
```bash
# Always start with database changes
sqlite3 database/coins.db

# Create migration script
vim scripts/add_[feature].py

# Run migration
uv run python scripts/add_[feature].py

# Export and validate
uv run python scripts/export_from_database.py
```

### 3. Testing Your Changes
```bash
# Run specific test
uv run python tests/test_auction_marketplace_integration.py

# Validate exports
uv run python scripts/validate.py

# Check pre-commit (this runs automatically)
git add . && git commit -m "test"
```

### 4. Pre-Commit Hook Pipeline
When you commit, these run automatically:
1. `export_from_database.py` - Generate JSON from DB
2. `migrate_to_universal_v1_1.py` - Convert to universal format
3. `validate.py` - Validate all JSON files
4. `test_github_pages.py` - Test browser interface

## ⚠️ Common Gotchas

1. **NEVER edit JSON files directly** - They're overwritten on export
2. **Coin IDs must be EXACTLY 4 parts**: `COUNTRY-TYPE-YEAR-MINT`
3. **Run exports before committing**: `uv run python scripts/export_from_database.py`
4. **Category field is required**: After #47, all coins need category/subcategory
5. **Varieties go in array**: Don't add to coin_id (e.g., NOT `US-AEAG-2021-W-TYPE2`)

## 📊 Success Criteria

- [ ] Issue #47: Category field working across all exports
- [ ] Issue #51: 39+ years of Silver Eagles (1986-2024)
- [ ] Issue #52: Gold Eagles (4 denominations) + Buffalos
- [ ] Issue #50: Three-Cent pieces complete (1851-1889)
- [ ] All pre-commit validations passing
- [ ] Universal taxonomy includes new data
- [ ] No regressions in auction parser tests

## 🚀 Stretch Goals (If Time Permits)

- Start scoping Issue #53 (Commemoratives) into manageable chunks
- Add variety information for key dates (e.g., 2021-P emergency Silver Eagles)
- Create bullion-specific validation rules
- Add melt value calculation helpers

## 📞 Getting Help

- **GitHub Issues**: Comment on the issue you're working on
- **Previous PRs**: Check commits `49106f0` and `3282a5e` for auction parser examples
- **Database Schema**: See `database/coins.db` for current structure
- **Test Examples**: `tests/test_auction_marketplace_integration.py` shows patterns

## 🎯 Why This Matters

The Red Book is the authoritative reference for US coin collectors. By aligning our taxonomy with Red Book classifications and adding these modern bullion series, we're:

1. **Closing critical gaps** that prevent marketplace integration
2. **Adding the most traded modern coins** (Silver/Gold Eagles)
3. **Enabling melt value calculations** with proper bullion data
4. **Setting foundation** for the massive commemorative dataset

This sprint directly impacts thousands of collectors and dealers who need accurate, comprehensive coin data for pricing and inventory management.

---

*Remember: Database first, validate always, and when in doubt - check the pre-commit hooks!*