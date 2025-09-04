# Coin Taxonomy Release Notes

This directory contains detailed release notes for significant updates to the coin-taxonomy system. Each release note documents breaking changes, new features, migration instructions, and API changes.

## Release History

### 2025

- **[2025-09-04: Schema Alignment & Three-Cent Pieces (v2.1.0)](./2025-09-04-schema-alignment.md)** 🚨 **Breaking Changes**  
  Adds Three-Cent Pieces and fixes critical schema alignment issues. Updates export column mappings and improves pre-commit validation.

- **[2025-09-02: Category Standardization Update (v1.2.0)](./2025-09-02-category-standardization.md)**  
  Implements standardized `category` and `subcategory` fields for distinguishing coins, currency, tokens, and exonumia following professional numismatic standards.

## Release Note Format

Each release note follows this structure:

1. **Summary** - Brief overview of the changes
2. **Breaking Changes** - Any changes that require action
3. **New Features** - What's been added
4. **Migration Instructions** - Step-by-step upgrade guide
5. **Data Updates** - Statistics on data changes
6. **API Changes** - Schema and field updates
7. **Files Changed** - List of modified files
8. **Testing** - How to verify the changes
9. **Support** - Where to get help

## For Developers

When implementing updates from a release:

1. Always read the **Breaking Changes** section first
2. Follow the **Migration Instructions** step-by-step
3. Run the **Testing** commands to verify
4. Check your application for any custom code that might be affected

## Contributing

When creating a new release note:

1. Use the format: `YYYY-MM-DD-feature-name.md`
2. Follow the structure of existing release notes
3. Include concrete examples and commands
4. Link to the relevant GitHub issue
5. Update this README with the new release entry