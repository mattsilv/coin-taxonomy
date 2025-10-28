# Coin Taxonomy Project Rules

## Pre-Commit Hook Validation ⚠️
**CRITICAL**: Always check for pre-commit hook errors and fix them before committing. If validation fails, either fix the data issues OR update the validation schemas to accommodate our growing taxonomy system.

## Python Dependency Management
ALWAYS use uv for Python dependency management:
- Install packages: `uv add <package>`
- Create virtual environments: `uv venv`
- Run scripts: `uv run <script>`
- Never use pip directly

## Data Source of Truth - Database-First Pipeline ⚠️
**CRITICAL**: SQLite database is the SINGLE SOURCE OF TRUTH for all coin data.

**NEVER EDIT JSON FILES DIRECTLY** - They are generated artifacts!

### Data Flow
```
SQLite Database → JSON Export Files
      ↑                    ↑
SOURCE OF TRUTH      GENERATED FILES
(version controlled)  (version controlled)
```

### Pre-Commit Hook Integration
- **All commits trigger automatic export** from SQLite database
- **JSON files regenerated** automatically via pre-commit hooks
- **Database is version controlled** and committed to git
- **Add new coins directly to database** using migration scripts

### Workflow Rules
1. **SQLite database is the source of truth** - version controlled and committed to git
2. **JSON files are generated artifacts** - exported from database via pre-commit hooks
3. **Add new coins using migration scripts** - modify database directly
4. **NEVER edit JSON files manually** - they will be overwritten on next commit
5. **Export JSON files from database**: `uv run python scripts/export_from_database.py`

### Export Process
```bash
# Export JSON files from database (DATABASE-FIRST PIPELINE)
uv run python scripts/export_from_database.py
```

This script performs the database-first export:
1. 📊 Reads coins from SQLite database (source of truth)
2. 📁 Generates JSON files by denomination (`data/us/coins/*.json`)
3. 📄 Creates complete taxonomy file (`data/us/us_coins_complete.json`)
4. 🔄 Runs universal migration (`scripts/migrate_to_universal_v1_1.py`)
5. 📁 Exports universal format (`scripts/export_db_v1_1.py`)
6. 🧪 Validates exports (`scripts/validate.py`)
7. 🌐 Copies universal data to docs folder

**IMPORTANT**: After adding coins to database, run export and commit ALL generated files with `git add . && git commit`. The export process updates JSON files, universal data, and docs folder - ALL must be committed together.

### Safe Change Process
1. **Add coins to database** using migration scripts (e.g., `scripts/backfill_historical_coins.py`)
2. **Run database export**: `uv run python scripts/export_from_database.py`
3. **Verify export succeeded** - check that all steps pass
4. **Commit ALL changes**: `git add . && git commit` (includes database and generated JSON files)

### Emergency Restore
- JSON backups: `backups/json_files_*/`
- Database backups: `backups/coins_backup_*.db`
- **Regenerate from migration scripts** if database is lost (best practice)

## Coin ID Format Standards ⚠️
**CRITICAL**: All coin IDs MUST follow the exact format: `COUNTRY-TYPE-YEAR-MINT`

### Validation Rules
1. **Exactly 4 parts** separated by **exactly 3 dashes** (no more, no fewer)
2. **Country code**: 2-3 uppercase letters (e.g., `US`, `CA`, `GB`)
3. **Type abbreviation**: 2-4 uppercase letters identifying the coin series (e.g., `IHC`, `LWC`, `MD`)
4. **Year**: 4-digit year when the coin was minted (e.g., `1877`, `1909`, `1942`)
5. **Mint mark**: 1-2 uppercase letters identifying the mint facility (e.g., `P`, `D`, `S`, `CC`, `W`)

### Valid Examples
- `US-IHC-1877-P` = US Indian Head Cent, 1877, Philadelphia mint
- `US-LWC-1909-S` = US Lincoln Wheat Cent, 1909, San Francisco mint
- `US-WHD-1942-D` = US Winged Liberty Head Dime (Mercury Dime), 1942, Denver mint

### Invalid Formats (Will Be Rejected)
- `IHC-1877-P` (missing country prefix)
- `US-IHC-1877-P-L` (5 parts - variety belongs in `varieties` array)
- `us-ihc-1877-p` (lowercase not allowed)
- `US_IHC_1877_P` (underscores not allowed)

### Enforcement
- Database CHECK constraints validate format on insert/update
- Export scripts verify format before generating JSON files
- Data integrity checks flag any violations
- Variety information goes in the `varieties` array, NOT in the coin_id
- Both `coins` table and `issues` table must have consistent formats

## GitHub Issue Workflow
- All feature work tracked in GitHub issues
- Reference issue numbers in commits: `"Add X - Issue #NN"`
- Check open issues before starting: `gh issue list`
- Link related documentation in issue descriptions
- Run success validation before closing issues

## Documentation Structure
- Main index: `docs/PROJECT_DOCS.md`
- README.md has comprehensive TOC
- Release notes: `docs/release-notes/`
- Never create orphaned .md files - link from PROJECT_DOCS.md

## Task Execution Principles
When executing tasks:
- **Clarify first**: Map out approach before coding
- **Database-first**: All data changes via migration scripts, never edit JSON directly
- **Minimal changes**: Only code directly required for task
- **Validate**: Run `export_from_database.py` after database changes
- **Document**: Update relevant docs in `/docs/` if schema changes
