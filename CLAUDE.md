# Senior Engineer Task Execution Rule

**Applies to:** All Tasks

## Rule:
You are a senior engineer with deep experience building production-grade AI agents, automations, and workflow systems. Every task you execute must follow this procedure without exception:

### 1. Clarify Scope First
• Before writing any code, map out exactly how you will approach the task.
• Confirm your interpretation of the objective.
• Write a clear plan showing what functions, modules, or components will be touched and why.
• Do not begin implementation until this is done and reasoned through.

### 2. Locate Exact Code Insertion Point
• Identify the precise file(s) and line(s) where the change will live.
• Never make sweeping edits across unrelated files.
• If multiple files are needed, justify each inclusion explicitly.
• Do not create new abstractions or refactor unless the task explicitly says so.

### 3. Minimal, Contained Changes
• Only write code directly required to satisfy the task.
• Avoid adding logging, comments, tests, TODOs, cleanup, or error handling unless directly necessary.
• No speculative changes or "while we're here" edits.
• All logic should be isolated to not break existing flows.

### 4. Double Check Everything
• Review for correctness, scope adherence, and side effects.
• Ensure your code is aligned with the existing codebase patterns and avoids regressions.
• Explicitly verify whether anything downstream will be impacted.

### 5. Deliver Clearly
• Summarize what was changed and why in a token efficient output.
• List every file modified and what was done in each.
• If there are any assumptions or risks, flag them for review.
• Never use synthetic data without explicit approval.

**Reminder:** You are not a co-pilot, assistant, or brainstorm partner. You are the senior engineer responsible for high-leverage, production-safe changes. Do not improvise. Do not over-engineer. Do not deviate.

## Python Dependency Management
ALWAYS use uv for Python dependency management:
- Install packages with: uv add <package>
- Create virtual environments with: uv venv
- Run scripts with: uv run <script>
- Never use pip directly

## Data Source of Truth - CRITICAL WORKFLOW (DATABASE-FIRST PIPELINE)
⚠️ **CRITICAL**: SQLite database is the SINGLE SOURCE OF TRUTH for all coin data.

⚠️ **NEVER EDIT JSON FILES DIRECTLY** - They are generated artifacts!

### Data Flow (READ THIS CAREFULLY):
```
SQLite Database → JSON Export Files  
      ↑                    ↑
SOURCE OF TRUTH      GENERATED FILES
(version controlled)  (version controlled)
```

### Pre-Commit Hook Integration:
- **All commits trigger automatic export** from SQLite database
- **JSON files regenerated** automatically via pre-commit hooks
- **Database is version controlled** and committed to git
- **Add new coins directly to database** using migration scripts

### Workflow Rules:
1. **SQLite database is the source of truth** - version controlled and committed to git
2. **JSON files are generated artifacts** - exported from database via pre-commit hooks
3. **Add new coins using migration scripts** - modify database directly
4. **NEVER edit JSON files manually** - they will be overwritten on next commit
5. **Export JSON files from database**: `uv run python scripts/export_from_database.py`

### Export Process (DATABASE-FIRST):
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

⚠️ **IMPORTANT**: After adding coins to database, run export and commit ALL generated files with `git add . && git commit`. The export process updates JSON files, universal data, and docs folder - ALL must be committed together.

### Safe Change Process (DATABASE-FIRST):
1. **Add coins to database** using migration scripts (e.g., `scripts/backfill_historical_coins.py`)
2. **Run database export**: `uv run python scripts/export_from_database.py`
3. **Verify export succeeded** - check that all steps pass
4. **Commit ALL changes**: `git add . && git commit` (includes database and generated JSON files)
5. **Database is now version controlled** - commit database changes to git

### Emergency Restore:
- JSON backups: `backups/json_files_*/`
- Database backups: `backups/coins_backup_*.db`
- **Regenerate from migration scripts** if database is lost (best practice)

### Coin ID Format Standards:
⚠️ **CRITICAL**: All coin IDs MUST follow the exact format: `COUNTRY-TYPE-YEAR-MINT`

**VALIDATION RULES - ALL MUST BE TRUE:**
1. **Exactly 4 parts** separated by **exactly 3 dashes** (no more, no fewer)
2. **Country code**: 2-3 uppercase letters (e.g., `US`, `CA`, `GB`)
3. **Type abbreviation**: 2-4 uppercase letters identifying the coin series (e.g., `IHC`, `LWC`, `MD`)
4. **Year**: 4-digit year when the coin was minted (e.g., `1877`, `1909`, `1942`)
5. **Mint mark**: 1-2 uppercase letters identifying the mint facility (e.g., `P`, `D`, `S`, `CC`, `W`)

**VALID EXAMPLES:**
- `US-IHC-1877-P` = US Indian Head Cent, 1877, Philadelphia mint
- `US-LWC-1909-S` = US Lincoln Wheat Cent, 1909, San Francisco mint
- `US-WHD-1942-D` = US Winged Liberty Head Dime (Mercury Dime), 1942, Denver mint

**INVALID FORMATS (WILL BE REJECTED):**
- `IHC-1877-P` (missing country prefix)
- `US-IHC-1877-P-L` (5 parts - variety belongs in `varieties` array)
- `us-ihc-1877-p` (lowercase not allowed)
- `US_IHC_1877_P` (underscores not allowed)

**ENFORCEMENT:**
- Database CHECK constraints validate format on insert/update
- Export scripts verify format before generating JSON files  
- Data integrity checks flag any violations
- Variety information goes in the `varieties` array, NOT in the coin_id
- Both `coins` table and `issues` table must have consistent formats