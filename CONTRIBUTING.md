# Contributing to US Coin Taxonomy Database

Thank you for your interest in contributing to this project! This guide will help you understand our development workflow and data quality standards.

## Development Environment Setup

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Git

### Setup Steps

1. **Fork and clone the repository:**
   ```bash
   git fork <repository-url>
   git clone <your-fork-url>
   cd coin-taxonomy
   ```

2. **Set up development environment:**
   ```bash
   # Create virtual environment
   uv venv
   
   # Activate virtual environment
   source .venv/bin/activate  # Linux/macOS
   # or on Windows: .venv\Scripts\activate
   
   # Install dependencies
   uv add jsonschema
   ```

3. **Verify your setup:**
   ```bash
   # Run validation to ensure everything works
   uv run python scripts/validate.py
   ```

## Making Changes

### Before You Start

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Understand the database-first architecture:**
   - The SQLite database (`database/coins.db`) is the source of truth
   - JSON files are generated from the database for version control
   - Never edit JSON files directly - always work through the database

### Development Workflow

1. **Make database changes** using appropriate scripts
2. **Regenerate JSON files** from the database:
   ```bash
   uv run python scripts/export_db.py
   ```
3. **Run validation** to ensure data integrity:
   ```bash
   uv run python scripts/validate.py
   ```
4. **Commit both database and JSON changes** together

### Testing Your Changes

Always run these checks before submitting:

```bash
# Validate all data files
uv run python scripts/validate.py

# Test database integrity
uv run python scripts/data_integrity_check.py

# Build database from JSON (reverse test)
uv run python scripts/build_db.py
```

All tests must pass before submission.

## Data Quality Standards

### Source Attribution Requirements

All data must include proper source attribution:

- **Primary sources**: PCGS CoinFacts, NGC Coin Explorer, Red Book, US Mint records
- **Citation format**: Include source name in `source_citation` field
- **Verification**: Cross-reference multiple sources when possible

### Schema Compliance

All data must validate against our JSON schemas:

- **Coin data**: Must conform to `data/us/schema/coin.schema.json`
- **Reference data**: Must conform to respective schema files
- **Field requirements**: All required fields must be present and correctly formatted

### Data Accuracy Standards

#### Mintage Figures
- Use official US Mint records when available
- Cross-reference with PCGS/NGC for accuracy
- Mark estimates clearly in notes when exact figures unavailable

#### Rarity Classifications
- **Key dates**: Must have both low mintage AND market premium
- **Semi-key**: Moderate scarcity with some collector premium
- **Scarce**: Lower mintage but minimal premium
- **Common**: Regular production coins

#### Physical Specifications
- Use official US Mint specifications
- Verify measurements across multiple sources
- Include composition change dates accurately

#### Designer Attribution
- Use full designer names (never "Various")
- Verify designer credits through official sources
- Include both obverse and reverse designers when different

## Submission Guidelines

### Pull Request Process

1. **Ensure all tests pass:**
   ```bash
   uv run python scripts/validate.py
   ```

2. **Write clear commit messages:**
   ```
   Fix Lincoln cent composition periods (1909-1982)
   
   - Correct bronze period end date to 1962
   - Add brass period 1962-1982
   - Update thickness specification to 1.55mm
   - Source: US Mint technical specifications
   ```

3. **Submit pull request with:**
   - Clear description of changes made
   - Justification for any data corrections
   - Source citations for new data
   - Screenshots of validation output

### Review Process

All contributions will be reviewed for:

- **Data accuracy**: Verification against authoritative sources
- **Schema compliance**: All JSON files must validate
- **Code quality**: Scripts must follow project conventions
- **Documentation**: Changes must be properly documented

## Types of Contributions

### High Priority
- **Data corrections**: Fix factual errors in existing data
- **Missing key dates**: Add documented key date coins
- **Variety documentation**: Add major varieties with proper attribution
- **Source verification**: Cross-check and improve citations

### Medium Priority
- **Series expansion**: Add new coin series or denominations
- **Enhanced tooling**: Improve validation and analysis scripts
- **Documentation**: Improve guides and examples

### Low Priority
- **Convenience features**: Additional export formats
- **Performance optimization**: Database query improvements

## Code Style

### Python Scripts
- Follow PEP 8 style guidelines
- Include docstrings for all functions
- Use type hints where appropriate
- Handle errors gracefully with clear messages

### JSON Data
- Use consistent indentation (2 spaces)
- Sort objects by logical order (chronological for dates)
- Include all required schema fields
- Use null for unknown values (never empty strings)

## Getting Help

### Questions and Discussion
- Open an issue for questions about data accuracy
- Use discussions for general development questions
- Review existing issues before creating new ones

### Reporting Problems
- **Data errors**: Include source citations in your report
- **Schema violations**: Include validation output
- **Script bugs**: Include full error messages and steps to reproduce

## Recognition

Contributors will be acknowledged in:
- Project documentation
- Release notes for significant contributions
- Special recognition for major data corrections or enhancements

## License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.