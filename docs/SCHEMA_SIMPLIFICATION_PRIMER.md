# Schema Simplification Engineering Primer
*For engineers new to the coin-taxonomy codebase*

## 🎯 Mission: Fix Architecture Bloat Blocking Development Velocity

**GitHub Issue:** [#59 - Schema Simplification: Remove Unused Tables and Fields](https://github.com/mattsilv/coin-taxonomy/issues/59)

## 📚 Quick Context

### What This Project Is
The **coin-taxonomy** is a comprehensive database of US coins used by collectors, auction houses, and marketplace integrations. Think of it as the "Rosetta Stone" for coin identification and pricing.

### Current Architecture Problem
Over time, the codebase evolved from a simple coin database into a complex multi-table system, but **most of the complexity is unused**:

- **609 coins** in the `coins` table ✅ (actively used)
- **0 records** in `issues`, `series_registry`, `composition_registry`, `subject_registry` tables ❌ (unused bloat)
- **GitHub Pages site shows "0 results"** ❌ (expects data that doesn't exist)

### Why This Matters
**Before Fix:** Adding new coins requires navigating complex, unused schema  
**After Fix:** Adding new coins becomes a simple database INSERT

## 🔍 Technical Deep Dive

### Current State Analysis

**Database Schema (database/coins.db):**
```sql
-- USED TABLE (609 records)
coins                    ✅ Active, contains all coin data

-- UNUSED TABLES (0 records each) 
issues                   ❌ Empty, complex schema
series_registry          ❌ Empty, planning artifact  
composition_registry     ❌ Empty, over-engineering
subject_registry         ❌ Empty, unused feature
```

**Data Pipeline Problem:**
```
SQLite Database (coins) → JSON Export → Universal Migration → Issues Format → GitHub Pages
     ↑                                                           ↑                    ↑
   Has Data                                                 Expects Different     Shows 0 Results  
                                                              Data Model
```

### Root Cause
The system was designed for an "issues-based" taxonomy (like stamp collecting), but the actual implementation uses an "individual coins" model. The GitHub Pages site expects issues data, but we only have coins data.

## 🛠️ Implementation Plan

### Phase 1: Database Schema Cleanup (2 hours)

**Step 1 - Backup Everything:**
```bash
cp database/coins.db database/coins_backup_schema_simplification_$(date +%Y%m%d_%H%M%S).db
```

**Step 2 - Identify Unused Fields in `coins` table:**
```bash
# Check which fields are actually populated
sqlite3 database/coins.db "SELECT 
    SUM(CASE WHEN grade IS NOT NULL THEN 1 ELSE 0 END) as grade_count,
    SUM(CASE WHEN edge IS NOT NULL THEN 1 ELSE 0 END) as edge_count,
    SUM(CASE WHEN thickness_mm IS NOT NULL THEN 1 ELSE 0 END) as thickness_count,
    SUM(CASE WHEN mint_state_strikes IS NOT NULL THEN 1 ELSE 0 END) as mint_state_count
FROM coins;"
```

**Step 3 - Create Simplified Schema:**
```sql
CREATE TABLE coins_new (
    coin_id TEXT PRIMARY KEY,
    year INTEGER NOT NULL,
    mint TEXT NOT NULL, 
    denomination TEXT NOT NULL,
    series_name TEXT NOT NULL,        -- Renamed from 'series' for clarity
    composition TEXT,                 -- Simple text like "90% Silver"
    weight_grams REAL,
    diameter_mm REAL,
    business_strikes INTEGER,
    proof_strikes INTEGER,
    total_mintage INTEGER,
    notes TEXT,
    rarity TEXT CHECK(rarity IN ('key', 'semi-key', 'common', 'scarce', NULL)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_coin_id_format CHECK (
        coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'
    )
);
```

**Step 4 - Migrate Data:**
```sql
INSERT INTO coins_new SELECT 
    coin_id,
    year,
    mint,
    denomination,
    series as series_name,
    composition,
    weight_grams,
    diameter_mm,
    business_strikes,
    proof_strikes,
    total_mintage,
    notes,
    rarity,
    created_at
FROM coins;
```

### Phase 2: Direct Export Pipeline (1 hour)

**Current Complex Pipeline:**
```bash
# Multiple scripts, multiple transformations
python scripts/export_from_database.py
python scripts/migrate_to_universal_v1_1.py  
python scripts/export_db_v1_1.py
```

**New Simple Pipeline:**
```python
# Single script: scripts/simple_export.py
def export_all():
    # Export 1: Developer format
    export_coins_complete()    # → data/us/us_coins_complete.json
    
    # Export 2: GitHub Pages format  
    export_for_site()         # → docs/data/universal/us_issues.json
```

### Phase 3: Fix GitHub Pages Site (30 minutes)

**Option A (Recommended):** Modify site to use coins data directly
**Option B:** Generate fake issues data from coins during export

## 🚀 Development Workflow (Post-Fix)

### Adding New Coins (SIMPLE!)
```bash
# 1. Add to database
sqlite3 database/coins.db "INSERT INTO coins VALUES ('US-MORG-1921-S', 1921, 'S', 'Dollar', 'Morgan Silver Dollar', '90% Silver', 26.73, 38.1, 21695000, 0, 21695000, 'Final year of Morgan production', 'common', datetime('now'));"

# 2. Export (single command)  
uv run python scripts/simple_export.py

# 3. Commit
git add . && git commit -m "Add 1921-S Morgan Silver Dollar"
```

### Testing Changes
```bash
# Local testing
python -m http.server 8000 -d docs
open http://localhost:8000

# Should now show coin data instead of "0 results"
```

## ⚠️ Common Gotchas

1. **Backup First**: Always backup database before schema changes
2. **Coin ID Format**: Must be exactly `COUNTRY-TYPE-YEAR-MINT` (4 parts, 3 dashes)
3. **Export After Changes**: Always run export script after database modifications
4. **Test Site Locally**: Verify GitHub Pages works before pushing

## 📊 Success Metrics

**Before Simplification:**
- Database: 5 tables (4 empty)
- Export: 3 complex scripts
- Site: Broken (0 results)
- Add Coin: ~10 minutes (complex schema navigation)

**After Simplification:**
- Database: 1 table (clean, focused)
- Export: 1 simple script  
- Site: Working (displays real data)
- Add Coin: ~2 minutes (simple INSERT + export)

## 🔗 Key Files to Modify

1. **Database**: `database/coins.db` - Schema simplification
2. **Export**: `scripts/simple_export.py` - New direct pipeline  
3. **Site**: `docs/app.js` - Handle coins format OR generate issues format
4. **Tests**: Update pre-commit hooks for new schema

## 📞 Getting Help

- **GitHub Issue**: [#59](https://github.com/mattsilv/coin-taxonomy/issues/59) - Primary discussion
- **Documentation**: See `docs/PROJECT_DOCS.md` for full documentation index
- **Database Schema**: Check current schema with `sqlite3 database/coins.db ".schema"`
- **Site Testing**: Use `python -m http.server 8000 -d docs` for local testing

## 🎯 Why This Matters

This isn't just code cleanup - it's **removing friction** from the core workflow. Every collector, auction house, and marketplace integration benefits when we can rapidly add new coins without fighting unnecessary complexity.

**Current Reality**: "I need to add a new coin... which tables do I update? What's this issues thing? Why is the site broken?"

**Post-Fix Reality**: "INSERT new coin, run export, done."

---

*Remember: Database first, validate always, keep it simple!*