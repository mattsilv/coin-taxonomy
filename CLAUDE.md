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
**CRITICAL**: SQLite database at `database/coins.db` is the SINGLE SOURCE OF TRUTH for all coin data.

**Canonical DB Path**: `database/coins.db` (NOT `coins.db` at root - that's deprecated)

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
- `us-ihc-1877-p` (lowercase not allowed)
- `US_IHC_1877_P` (underscores not allowed)

### Enforcement
- Database CHECK constraints validate format on insert/update
- Export scripts verify format before generating JSON files
- Data integrity checks flag any violations
- Both `coins` table and `issues` table must have consistent formats

### Variety Suffix Pattern (Optional 5th Part)
For coins with significant design varieties that affect collector value, an optional suffix can be added:

**Format**: `COUNTRY-TYPE-YEAR-MINT-SUFFIX`

**Examples**:
- `US-GRNT-1922-P-STAR` = Grant Memorial with Star variety
- `US-ALCN-1921-P-2X2` = Alabama Centennial 2X2 variety
- `US-MOCN-1921-P-2S4` = Missouri Centennial 2 Star 4 variety
- `US-TCST-1851-P-T1` = Silver Three-Cent Type I
- `US-MOGD-1878-P-8TF` = Morgan Dollar 8 Tail Feathers
- `CA-GMPL-1982-P-14oz` = Gold Maple Leaf 1/4 oz

**Suffix Rules**:
1. **Uppercase alphanumeric only** - letters A-Z and digits 0-9 (1-4 characters)
2. **Suffix must match variety column** - if coin_id has suffix, variety column should contain matching value
3. **Weight suffixes for fractional bullion** - e.g., `110oz`, `12oz`, `14oz`, `120oz`, `1g` (no variety column needed)
4. **Base record (no suffix) = "regular" variety** - only add suffix for variations

**When to Use Suffix**:
- Major die varieties (8TF, 7TF, VDB)
- Design type changes within a series (T1, T2, T3)
- Commemorative design variants (STAR, 2X2, 2S4)
- Weight variants for bullion (110oz, 14oz)

**series_registry.json**: Use `variety_suffixes` field to document valid suffixes per series.

### Random Year Pattern (Bullion Only) ⚠️
**NEW**: Bullion products sold as "random year" or "dealer's choice" use the `XXXX` placeholder:

**Format**: `COUNTRY-TYPE-XXXX-MINT`

**Examples**:
- `US-AGEO-XXXX-X` = American Gold Eagle 1 oz, random year, unspecified mint
- `US-ASEA-XXXX-X` = American Silver Eagle 1 oz, random year, unspecified mint

**Use Case**: These entries represent bullion products sold at the lowest premium over spot where the specific year doesn't affect value (valued by metal content only).

**Important Rules**:
- XXXX pattern is **ONLY** used for bullion products
- **NOT** for numismatic coins (year always matters for collectible value)
- Use `X` for unspecified mint when applicable
- Document as "Random year bullion" in `notes` field
- Year field accepts either 4-digit numeric year (1773-9999) OR literal string "XXXX"

## GitHub Issue Workflow
- All feature work tracked in GitHub issues
- Reference issue numbers in commits: `"Add X - Issue #NN"`
- Check open issues before starting: `gh issue list`
- Link related documentation in issue descriptions
- Run success validation before closing issues

## Pull Request Workflow ⚠️
**CRITICAL**: NEVER push directly to main. Always create a PR.

### Required Steps
1. **Create feature branch**: `git checkout -b feature/issue-NN-description`
2. **Make changes and commit** to feature branch
3. **Push feature branch**: `git push -u origin feature/issue-NN-description`
4. **Create PR**: `gh pr create --title "..." --body "..."`
5. **Wait for review/approval** before merging

### PR Title Format
```
Add [feature] - Issue #NN
```

### PR Body Template
```markdown
## Summary
- Brief description of changes

## Test plan
- [ ] Ran export_from_database.py
- [ ] Validated JSON exports
- [ ] Tested affected functionality

Closes #NN
```

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
