# 🪙 Coin Taxonomy Project - Engineering Handoff Document

## 📋 Executive Summary
This document provides a complete handoff for the coin-taxonomy project, a production-ready numismatic database and JSON export system serving as the single source of truth for U.S. and Canadian coin data. The system powers multiple downstream applications through a database-first pipeline with automated validation and export mechanisms.

## 🎯 Current Status & Immediate Actions

### ✅ Recently Completed Work
1. **Schema Alignment Fix** - Critical database schema issues resolved (Issues #57, #50)
   - Fixed `varieties` table foreign key constraints
   - Aligned JSON export with database schema
   - Implemented Three-Cent Pieces correctly
   - All exports now pass validation

2. **Documentation Consolidation** - Organized release notes and documentation
   - Created unified release notes structure
   - Updated PROJECT_DOCS.md index
   - Archived outdated documentation

3. **Schema Simplification Primer** - Created comprehensive engineering guide
   - **GitHub Issue**: [#59 - Schema Simplification](https://github.com/mattsilv/coin-taxonomy/issues/59)
   - **Technical Guide**: [SCHEMA_SIMPLIFICATION_PRIMER.md](./SCHEMA_SIMPLIFICATION_PRIMER.md)
   - Estimated: 3-4 hours of work to complete

### 🚨 Immediate Action Required
**Schema Simplification (Issue #59)** - The database has accumulated architecture bloat with 37 columns per coin record. The new engineer should:
1. Review the [Schema Simplification Primer](./SCHEMA_SIMPLIFICATION_PRIMER.md)
2. Follow the step-by-step migration plan
3. Test thoroughly with the validation suite
4. Deploy the simplified schema

## 🏗️ System Architecture

### Database-First Pipeline
```
SQLite Database (coins.db) → Export Scripts → JSON Files → GitHub Pages Site
       ↑                          ↓                ↓
   SOURCE OF TRUTH          Pre-commit      AI-Optimized Format
                            Validation
```

### Key Components
1. **Database**: `database/coins.db` - Single source of truth (version controlled)
2. **Export Pipeline**: Scripts in `scripts/` that generate all JSON artifacts
3. **Validation**: Pre-commit hooks ensure data integrity
4. **Distribution**: JSON exports for different consumers (standard, AI-optimized, universal)
5. **Web Interface**: GitHub Pages site at https://mattsilv.github.io/coin-taxonomy/

## 📁 Repository Structure

```
coin-taxonomy/
├── database/
│   └── coins.db                    # ⚠️ SINGLE SOURCE OF TRUTH
├── scripts/
│   ├── export_from_database.py     # Main export orchestrator
│   ├── export_db.py                # Database → JSON exporter
│   ├── export_db_v1_1.py           # Universal format exporter
│   ├── migrate_to_universal_v1_1.py # Universal format migrator
│   ├── validate.py                 # Data validation
│   ├── add_*.py                    # Migration scripts for new coins
│   └── test_*.py                   # Test suites
├── data/
│   ├── us/
│   │   ├── coins/                  # Per-denomination JSON files
│   │   └── us_coins_complete.json  # Complete US dataset
│   ├── ca/                         # Canadian coins
│   ├── ai-optimized/               # AI-friendly format
│   └── universal/                  # Universal interchange format
├── docs/
│   ├── release-notes/              # Version history
│   ├── index.html                  # GitHub Pages site
│   └── *.md                        # Technical documentation
└── tests/                          # pytest test suites
```

## 🔑 Critical Workflows

### Adding New Coins
```bash
# 1. Create migration script
uv run python scripts/add_new_coins.py

# 2. Export from database (generates all JSON)
uv run python scripts/export_from_database.py

# 3. Commit everything (database + generated files)
git add .
git commit -m "Add new coin series"
```

### Export Pipeline Process
The `export_from_database.py` script orchestrates:
1. 📊 Export coins from SQLite to JSON by denomination
2. 📄 Create complete taxonomy file
3. 🔄 Run universal format migration
4. 📁 Export universal format
5. 🧪 Validate all exports
6. 🌐 Copy to docs folder for GitHub Pages

### Pre-Commit Validation
- Automatically runs on every commit
- Validates JSON schema compliance
- Ensures ID format consistency
- Checks foreign key relationships
- **If validation fails**: Fix data issues OR update validation schemas

## ⚠️ Critical Rules & Constraints

### Database is Source of Truth
- **NEVER edit JSON files directly** - they are generated artifacts
- **Always modify database** then re-export
- **Version control the database** - commit `database/coins.db` to git

### Coin ID Format (STRICT)
Format: `COUNTRY-TYPE-YEAR-MINT`
- Example: `US-IHC-1877-P` (US Indian Head Cent, 1877, Philadelphia)
- Exactly 4 parts, 3 dashes
- All uppercase
- Varieties go in `varieties` array, NOT in coin_id

### Foreign Key Relationships
- `varieties` table references `issues` table (NOT `coins`)
- `issues.issue_id` must exist before adding varieties
- Cascade deletes are enabled

## 🐛 Known Issues & Tech Debt

### Schema Bloat (Issue #59)
- **Problem**: 37 columns per coin, most rarely used
- **Solution**: Implement Core + Extensions pattern
- **Guide**: [SCHEMA_SIMPLIFICATION_PRIMER.md](./SCHEMA_SIMPLIFICATION_PRIMER.md)

### Performance Considerations
- Large JSON exports (us_coins_complete.json > 5MB)
- Consider implementing pagination for web interface
- Database indexes could be optimized

### Data Quality
- Some historical coins missing mint marks
- Variety descriptions need standardization
- Grade distribution data incomplete for older series

## 🚀 Current Sprint: Red Book Classification
See [NEXT_SPRINT_PRIMER.md](../NEXT_SPRINT_PRIMER.md) for details on:
- PCGS number integration
- Red Book page references
- Population report data
- Grading service alignment

## 🧪 Testing & Validation

### Test Suite
```bash
# Run all tests
uv run pytest

# Validate exports
uv run python scripts/validate.py

# Test specific functionality
uv run python scripts/test_variety_export.py
```

### Validation Checks
- JSON schema compliance
- Foreign key integrity
- ID format validation
- Duplicate detection
- Export completeness

## 🔧 Development Setup

### Prerequisites
- Python 3.11+
- uv (Python package manager)
- Git with pre-commit hooks

### Quick Start
```bash
# Clone repository
git clone https://github.com/mattsilv/coin-taxonomy.git
cd coin-taxonomy

# Install dependencies
uv venv
uv pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run export pipeline
uv run python scripts/export_from_database.py

# Start local development
uv run python -m http.server 8000 --directory docs/
```

## 📊 Production Usage

### Current Integrations
- **GitHub Pages**: https://mattsilv.github.io/coin-taxonomy/
- **Unified Taxonomy System**: Daily sync via mattsilv/unified-taxonomy
- **AI Applications**: Using ai-optimized/ format
- **External APIs**: Via universal/ interchange format

### API Endpoints (GitHub Pages)
- Complete dataset: `/data/universal/coins_v1_1.json`
- US coins: `/data/us/us_coins_complete.json`
- By denomination: `/data/us/coins/{denomination}.json`

## 🔐 Security & Access

### Repository Permissions
- Main branch protected
- Requires PR reviews
- Pre-commit hooks mandatory
- Database changes require migration scripts

### Sensitive Data
- No PII or pricing data in repository
- Population/census data is public domain
- Images must have proper licensing

## 📝 Documentation Index

### Essential Reading
1. [README.md](../README.md) - Project overview
2. [PROJECT_DOCS.md](./PROJECT_DOCS.md) - Documentation index
3. [SCHEMA_SIMPLIFICATION_PRIMER.md](./SCHEMA_SIMPLIFICATION_PRIMER.md) - Current priority task
4. [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) - How to use the data

### Reference Documentation
- [HIERARCHICAL_VARIANT_RESOLUTION.md](./HIERARCHICAL_VARIANT_RESOLUTION.md) - Variant system
- [AI_RESEARCH_GUIDELINES.md](./AI_RESEARCH_GUIDELINES.md) - AI integration
- [Release Notes](./release-notes/) - Version history

## 🎯 Next Steps for New Engineer

### Week 1 Priorities
1. **Review this handoff document** thoroughly
2. **Complete Schema Simplification** (Issue #59) - 3-4 hours
3. **Run the test suite** and understand validation
4. **Make a small contribution** to get familiar with the workflow

### Week 2 Goals
- Review and close any other open GitHub issues
- Optimize database indexes
- Improve test coverage
- Document any undocumented scripts

### Long-term Opportunities
- Implement Canadian coin varieties
- Add world coin support
- Create REST API wrapper
- Build automated Red Book alignment
- Develop mobile-friendly interface

## 📞 Resources & Support

### GitHub
- **Repository**: https://github.com/mattsilv/coin-taxonomy
- **Issues**: https://github.com/mattsilv/coin-taxonomy/issues
- **Wiki**: (Consider creating for extended documentation)

### External References
- PCGS CoinFacts: https://www.pcgs.com/coinfacts
- NGC Coin Explorer: https://www.ngccoin.com/coin-explorer/
- Red Book (Whitman Publishing): Industry standard reference

### Project Philosophy
- **Database-first**: All data flows from the SQLite database
- **Validation-driven**: Pre-commit hooks ensure quality
- **Human-approved**: No automated data changes without review
- **Open source**: Freely available for numismatic community

## ✅ Handoff Checklist

Before considering this handoff complete, ensure:
- [ ] Schema Simplification Issue #59 is reviewed
- [ ] Test suite runs successfully
- [ ] Export pipeline completes without errors
- [ ] Pre-commit hooks are installed and working
- [ ] Documentation has been read and understood
- [ ] At least one small PR has been submitted

## 🏁 Final Notes

This project represents the industry's most comprehensive open-source coin taxonomy system. It serves as a critical foundation for AI applications, collector tools, and market analysis platforms. The database-first architecture ensures data integrity while the multi-format export system provides maximum compatibility.

The immediate priority is completing the Schema Simplification (Issue #59) to reduce technical debt and improve maintainability. This well-documented task provides an excellent introduction to the codebase while delivering immediate value.

Welcome to the coin-taxonomy project! Your contributions will help preserve numismatic knowledge and make it accessible to collectors, researchers, and applications worldwide.

---

*Last Updated: 2025-09-04*
*Document Version: 1.0*
*Primary Author: Previous Engineering Team*