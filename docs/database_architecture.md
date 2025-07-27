# Database Architecture & Migration Strategy

## Current Status: Structural Overhaul in Progress

We are implementing major structural changes to improve the taxonomy before public launch:

### Key Structural Changes
1. **Coins Object → Array**: Changed from `{"1916-D": {...}}` to `[{"coin_id": "IHC-1916-D", ...}]`
2. **Unique Identifiers**: Added `series_id` and `coin_id` fields for stable linking
3. **Mintage Separation**: Changed `mintage`/`proof_mintage` to `business_strikes`/`proof_strikes`
4. **Varieties Array**: Changed from object to array structure with `variety_id`
5. **Alloy Names**: Added human-readable `alloy_name` alongside detailed composition

### Database Management Best Practices

#### Migration Strategy
1. **Backup Before Changes**: Always create timestamped backups
2. **Schema Versioning**: Track schema changes with version numbers
3. **Migration Scripts**: Automated scripts for schema updates
4. **Validation**: Ensure data integrity after each migration

#### Current Approach vs ORM Evaluation

**Current Approach (SQLite + JSON)**
- ✅ Simple and working well
- ✅ Easy to understand and debug
- ✅ Perfect for read-heavy taxonomy data
- ✅ JSON validation provides structure
- ❌ Manual migration management
- ❌ No automatic relationship validation

**ORM Introduction (SQLAlchemy/Peewee)**
- ✅ Automated migrations with Alembic
- ✅ Better relationship modeling
- ✅ Type safety and validation
- ✅ Complex query capabilities
- ❌ Additional complexity before launch
- ❌ Potential over-engineering for our use case
- ❌ Learning curve and debugging complexity

#### Recommendation: Phased Approach

**Phase 1 (Pre-Launch): Current Approach**
- Complete structural changes with existing SQLite + JSON
- Implement manual migration scripts
- Focus on data accuracy and structure
- Get to market quickly

**Phase 2 (Post-Launch): ORM Evaluation**
- Gather real user feedback on query patterns
- Evaluate if ORM benefits outweigh complexity
- Consider SQLAlchemy for complex relationships
- Implement based on actual usage patterns

### Migration Scripts Architecture

```python
# migrations/
├── 001_initial_schema.sql
├── 002_add_coin_ids.sql
├── 003_restructure_varieties.sql
└── migrate.py  # Migration runner
```

#### Best Practices Implemented:
1. **Version Control**: All schema changes tracked in git
2. **Rollback Capability**: Each migration has rollback script
3. **Data Validation**: Post-migration validation checks
4. **Backup Strategy**: Automated backups before each migration

### Current Implementation Status

**Completed:**
- ✅ Structural changes to cents.json
- ✅ New schema with series_id, coin_id
- ✅ business_strikes/proof_strikes separation
- ✅ Varieties as arrays with variety_id
- ✅ Human-readable alloy_name fields

**In Progress:**
- 🔄 Update remaining denomination files
- 🔄 Update JSON schema validation
- 🔄 Update database build scripts
- 🔄 Update import/export scripts

**Pending:**
- ⏳ Comprehensive testing
- ⏳ Migration script creation
- ⏳ Documentation updates