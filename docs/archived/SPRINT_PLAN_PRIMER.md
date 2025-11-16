# Coin Taxonomy Sprint Plan & Engineering Primer

## Executive Summary
This document provides a prioritized sprint plan for critical coin-taxonomy improvements, focusing on data integrity and system architecture first, then dataset completeness. Issues are grouped by dependency and impact on system stability.

---

## 🔴 SPRINT 1: Critical Foundation (2-3 weeks)
**Focus: Variant Tracking System Architecture**

### Issue #54: Add Explicit Coin Variant Tracking System
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/54  
**Priority**: CRITICAL - Blocks auction integration  
**Complexity**: Medium

#### What Needs to Be Done:
1. Create new `coin_variants` table in SQLite database
2. Link variants to parent coins via foreign key
3. Add variant-specific fields (die varieties, errors, special strikes)
4. Update export scripts to include variant relationships

#### Key Files to Modify:
- `database/coins.db` - Add new table
- `scripts/export_from_database.py` - Include variant exports
- Create new migration: `scripts/migrate_add_variant_tracking.py`

#### Context for New Engineer:
The current system tracks varieties as a JSON array within each coin record. This doesn't scale for auction mapping where we need hierarchical relationships (e.g., "1909-S VDB" is a variant of "1909-S Lincoln Cent"). Auction sites list these differently and we need to resolve them all to the same base coin.

---

### Issue #56: Implement Hierarchical Variant Resolution
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/56  
**Priority**: CRITICAL - Required for marketplace integration  
**Complexity**: High  
**Depends on**: #54 must be completed first

#### What Needs to Be Done:
1. Build variant resolution engine that matches auction listings to taxonomy
2. Create hierarchy: Base Coin → Major Variety → Minor Variety → Die State
3. Implement fuzzy matching for auction title parsing
4. Add confidence scoring for matches

#### Key Components:
```python
# Example hierarchy structure needed:
{
  "base_coin": "US-LWCT-1909-S",
  "major_variants": [
    {
      "variant_id": "US-LWCT-1909-S-VDB",
      "variant_type": "designer_initials",
      "premium_factor": 2.5
    }
  ],
  "minor_variants": [
    {
      "variant_id": "US-LWCT-1909-S-VDB-RPM",
      "parent": "US-LWCT-1909-S-VDB",
      "variant_type": "repunched_mintmark"
    }
  ]
}
```

#### Implementation Path:
1. Design variant hierarchy schema
2. Build resolution algorithm
3. Create test suite with real auction titles
4. Integrate with export pipeline

---

## 🟡 SPRINT 2: Data Quality Infrastructure (2 weeks)
**Focus: Human-in-the-loop approval system**

### Issue #45: Human Approval Workflow for External Data
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/45  
**Priority**: HIGH - Prevents data corruption  
**Complexity**: High

#### What Needs to Be Done:
1. Create approval queue table in database
2. Build CLI tool for reviewing proposed changes
3. Implement diff visualization for data changes
4. Add rollback capability for rejected changes

#### Key Features Required:
- Queue proposed changes from external sources
- Show before/after comparison
- Track approver and timestamp
- Batch approval for similar changes
- Automatic validation before queue entry

#### Implementation Files:
- Create: `scripts/approval_queue.py`
- Create: `scripts/review_changes_cli.py`
- Modify: `database/coins.db` - Add approval tables

---

### Issue #50: Add Three-Cent Pieces Dataset
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/50  
**Priority**: MEDIUM - Completes Red Book coverage  
**Complexity**: Low

#### Dataset Requirements:
- Silver Three-Cent Pieces (1851-1873)
- Nickel Three-Cent Pieces (1865-1889)
- All major varieties per Red Book listings

#### Implementation:
1. Create migration script: `scripts/add_three_cent_pieces.py`
2. Use existing patterns from other denominations
3. Include composition changes (silver → nickel transition)

---

## 🟢 SPRINT 3: Dataset Completion (2-3 weeks)
**Focus: Complete Red Book alignment**

### Issue #51: Silver Bullion Dataset (American Silver Eagles)
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/51  
**Dates**: 1986-Date  
**Special Considerations**: Include proof, burnished, and reverse proof variants

### Issue #52: Gold Bullion Dataset  
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/52  
**Series**: American Gold Eagles, Gold Buffalos  
**Dates**: 1986-Date

### Issue #53: Commemoratives Dataset
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/53  
**Dates**: 1892-Date  
**Complexity**: High - Many unique designs

### Issue #48: Red Book Classification Verification
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/48  
**Status**: 60% complete - needs above datasets for 100%

---

## 🔵 FUTURE: Sprint 4 (3-4 weeks)

### Issue #46: International Mint Data Integration
**GitHub**: https://github.com/mattsilv/coin-taxonomy/issues/46  
**Requires**: Issue #45 completed first  
**Complexity**: Very High - PDF parsing, multiple data formats

---

## Quick Start for New Engineer

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/mattsilv/coin-taxonomy.git
cd coin-taxonomy

# Install Python dependencies
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Verify database
sqlite3 database/coins.db ".tables"
```

### 2. Understanding the Codebase

#### Core Concepts:
- **Database First**: SQLite is the source of truth, JSON files are generated
- **Pre-commit Hooks**: Auto-exports JSON on every commit
- **Coin ID Format**: `COUNTRY-TYPE-YEAR-MINT` (e.g., `US-LWCT-1909-S`)

#### Key Directories:
```
coin-taxonomy/
├── database/coins.db       # Source of truth
├── scripts/                 # All migrations and tools
│   ├── export_from_database.py
│   └── migrate_*.py        # Migration scripts
├── data/                   # Generated JSON exports
│   ├── us/coins/          # US coin data
│   └── universal/         # Cross-country format
└── docs/                  # Documentation
```

### 3. Development Workflow

1. **Always create migrations** - Never edit database directly
2. **Run exports after changes**: `uv run python scripts/export_from_database.py`
3. **Commit database + JSON together** - They must stay in sync
4. **Check pre-commit hooks**: Ensure they pass before pushing

### 4. Testing Changes

```bash
# Run data integrity check
uv run python scripts/data_integrity_check.py

# Validate JSON exports
uv run python scripts/validate.py

# Test specific migration
uv run python scripts/your_migration.py --dry-run
```

### 5. Priority Order

**Week 1-2**: Focus on #54 (variant tracking foundation)
**Week 2-3**: Complete #56 (hierarchical resolution) 
**Week 4**: Implement #45 (approval workflow)
**Week 5-6**: Add datasets #50-53

### 6. Key Principles

1. **Data Integrity First**: Never compromise data quality for speed
2. **Database is Truth**: JSON files are always generated, never hand-edited
3. **Test Everything**: Use --dry-run flags, check backups
4. **Version Control**: Database is in git - commit it with changes
5. **Document Changes**: Update release notes in `docs/release-notes/`

### 7. Contact & Resources

- **Repository**: https://github.com/mattsilv/coin-taxonomy
- **Issues**: Check issue comments for additional context
- **Database Schema**: Run `.schema` in sqlite3 for current structure
- **Example Migrations**: Review existing `scripts/migrate_*.py` files

---

## Success Metrics

- **Sprint 1**: Variant tracking operational, auction mapping 80% accurate
- **Sprint 2**: Zero data corruption incidents, approval queue < 24hr turnaround  
- **Sprint 3**: 100% Red Book coverage for US coins
- **Sprint 4**: Successful integration with 1+ international mint

## Risk Mitigation

1. **Always backup before migrations**: Scripts create automatic backups
2. **Use dry-run mode**: Test migrations before applying
3. **Review approval queue daily**: Prevent backlog
4. **Monitor data integrity**: Run checks after each migration

---

*Last Updated: September 2, 2025*  
*Document Version: 1.0*