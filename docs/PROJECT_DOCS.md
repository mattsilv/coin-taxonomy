# Coin Taxonomy Documentation Index

## 📚 Documentation Structure

### Core Documentation
- **[README.md](../README.md)** - Project overview and quick start
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to contribute to the project
- **[CHANGELOG.md](../CHANGELOG.md)** - All changes by version
- **[LOCAL_TESTING.md](../LOCAL_TESTING.md)** - Local development setup

### 📋 Release Notes
- **[Release Notes Index](./release-notes/README.md)** - All release notes
- **[Latest: v2.1.0 - Schema Alignment](./release-notes/2025-09-04-schema-alignment.md)** 🚨 Breaking Changes

### 🔧 Integration & Development
- **[Integration Guide](./INTEGRATION_GUIDE.md)** - How to integrate the taxonomy into your application
- **[AI Research Guidelines](./AI_RESEARCH_GUIDELINES.md)** - Using AI for coin research
- **[Hierarchical Variant Resolution](./HIERARCHICAL_VARIANT_RESOLUTION.md)** - Variant mapping system

### 📊 Analysis & Research
- **[Red Book Alignment Analysis](./red_book_alignment_analysis.md)** - Industry standard alignment
- **[AI Coin Description Task](./ai-coin-description-task.md)** - Visual description standards

### 🚀 Sprint Planning
- **[PROJECT HANDOFF](./PROJECT_HANDOFF.md)** - 📌 Complete engineering handoff document
- **[Schema Simplification Primer](./SCHEMA_SIMPLIFICATION_PRIMER.md)** - Fix architecture bloat ([Issue #59](https://github.com/mattsilv/coin-taxonomy/issues/59))
- **[Current Sprint Primer](../NEXT_SPRINT_PRIMER.md)** - Red Book Classification Sprint
- **[Sprint Plan Primer](./SPRINT_PLAN_PRIMER.md)** - Sprint planning guidelines

### 🌐 GitHub Pages Site
- **[Live Site](https://mattsilv.github.io/coin-taxonomy/)** - Interactive coin browser
- **[Site Documentation](./index.html)** - GitHub Pages implementation

## 📁 Repository Layout

```
coin-taxonomy/
├── database/
│   └── coins.db            # Single source of truth
├── scripts/
│   ├── export_*.py         # Export scripts (database → JSON)
│   ├── add_*.py           # Migration scripts
│   └── test_*.py          # Test scripts
├── data/
│   ├── us/                # US coin JSON exports
│   ├── ca/                # Canadian coin JSON exports
│   ├── ai-optimized/      # AI taxonomy format
│   └── universal/         # Universal format (experimental)
├── docs/
│   ├── release-notes/     # Version release notes
│   ├── archived/          # Old documentation
│   └── *.md              # Technical documentation
└── tests/                 # Test suites
```

## 🔑 Key Principles

1. **Database First**: SQLite database is the single source of truth
2. **JSON as Artifacts**: All JSON files are generated from database
3. **Never Edit JSON**: Always modify database and re-export
4. **Version Control**: Database is version controlled
5. **Pre-commit Validation**: Ensures data integrity

## 🆘 Getting Help

- **GitHub Issues**: [Report issues](https://github.com/mattsilv/coin-taxonomy/issues)
- **Documentation**: You're reading it!
- **Live Demo**: [Browse the taxonomy](https://mattsilv.github.io/coin-taxonomy/)

## 📝 Documentation Standards

When creating documentation:
1. Use clear, descriptive titles
2. Include concrete examples
3. Link to related documents
4. Date your documents (for release notes)
5. Update this index when adding new docs