# AI Research Guidelines for Coin Data Sourcing

## Overview

This document provides structured guidelines for AI agents to research and source coin data for the taxonomy system. Each research task should follow the format and sourcing requirements outlined below.

## Research Task Format

When researching coin data for new issues, use the following template:

```
TASK: Research [COIN_SERIES] for [COUNTRY]
YEARS: [START_YEAR] - [END_YEAR]
PRIORITY: [HIGH/MEDIUM/LOW]

REQUIRED DATA POINTS:
1. Year of issue
2. Mint marks (all locations that struck this coin)
3. Business strike mintages
4. Proof strike mintages
5. Composition (metal content, weight, diameter)
6. Design descriptions (obverse/reverse)
7. Key date identification
8. Major varieties

SOURCING REQUIREMENTS:
- Primary sources only (see approved list below)
- Must provide exact page/catalog numbers
- Include direct URLs when available
- Note conflicting data between sources
```

## Approved Primary Sources

### United States Coins

#### Official References
- **Red Book (A Guide Book of United States Coins)** by R.S. Yeoman
  - Current edition: 2025 (78th Edition)
  - ISBN: 978-0-7948-5204-8
  - Source URL: https://www.whitman.com/redbook
  - Citation format: `Red Book 2025, p. [PAGE]`

- **PCGS CoinFacts**
  - URL: https://www.pcgs.com/coinfacts
  - Citation format: `PCGS #[CERT_NUMBER]`
  - Example: https://www.pcgs.com/coinfacts/coin/1877-indian-cent/2127

- **NGC Coin Explorer**
  - URL: https://www.ngccoin.com/coin-explorer
  - Citation format: `NGC ID: [ID_NUMBER]`

- **US Mint Production Reports**
  - URL: https://www.usmint.gov/about/production-sales-figures
  - Historical reports: https://nnp.wustl.edu/library/mintreports

#### Variety References
- **Cherrypickers' Guide** by Bill Fivaz & J.T. Stanton
  - Volume I: Half Cents through Nickel Five-Cent Pieces
  - Volume II: Dimes through Gold Coins
  - Citation format: `CPG FS-[NUMBER]`

- **VAM World** (Morgan & Peace Dollars)
  - URL: http://www.vamworld.com
  - Citation format: `VAM-[NUMBER]`

### Canadian Coins

#### Official References  
- **Charlton Standard Catalogue of Canadian Coins**
  - Current edition: 2025 (79th Edition)
  - Citation format: `Charlton 2025, p. [PAGE]`

- **Royal Canadian Mint**
  - URL: https://www.mint.ca
  - Annual Reports: https://www.mint.ca/en/about-us/annual-reports

- **Coins of Canada (COINSCAN)**
  - URL: https://www.coinsandcanada.com
  - Citation format: `COINSCAN #[NUMBER]`

### Paper Currency

#### United States
- **Friedberg Paper Money of the United States**
  - Current edition: 22nd Edition (2023)
  - Citation format: `Friedberg #[NUMBER]`

- **Standard Guide to Small-Size U.S. Paper Money**
  - By Dean Oakes & John Schwartz
  - Citation format: `Oakes-Schwartz #[NUMBER]`

#### Canada
- **Charlton Standard Catalogue of Canadian Government Paper Money**
  - Current edition: 2025 (37th Edition)
  - Citation format: `Charlton Currency 2025, p. [PAGE]`

## Research Examples

### Example 1: American Silver Eagles (Issue #51)

```
TASK: Research American Silver Eagles for US
YEARS: 1986 - 2025
PRIORITY: HIGH

SOURCES CONSULTED:
1. Red Book 2025, pp. 376-380
2. PCGS CoinFacts: https://www.pcgs.com/coinfacts/category/silver-eagles/117
3. US Mint Production: https://www.usmint.gov/about/production-sales-figures/bullion

DATA EXTRACTED:
- 1986: 5,393,005 business strikes, no proofs
  Source: Red Book 2025, p. 377
- 1986-S: 1,446,778 proof strikes
  Source: PCGS #9801
- Composition: .999 fine silver, 31.103g (1 troy oz), 40.6mm
  Source: US Mint specifications

VARIETIES IDENTIFIED:
- 2008-W Reverse of 2007: CPG FS-901
- 2011-S/-W Burnished Set: Red Book 2025, p. 379
```

### Example 2: American Gold Eagles (Issue #52)

```
TASK: Research American Gold Eagles for US  
YEARS: 1986 - 2025
PRIORITY: HIGH

SOURCES CONSULTED:
1. Red Book 2025, pp. 381-390
2. NGC Coin Explorer: https://www.ngccoin.com/coin-explorer/gold-eagles
3. US Mint Annual Reports 1986-2024

DENOMINATIONS:
- $5 (1/10 oz): 16.5mm, 3.393g
- $10 (1/4 oz): 22.0mm, 8.483g
- $25 (1/2 oz): 27.0mm, 16.966g
- $50 (1 oz): 32.7mm, 33.931g
Source: US Mint specifications

KEY DATES IDENTIFIED:
- 1991 $25: 24,100 mintage (Red Book 2025, p. 386)
- 1993-P $10: 46,464 mintage (PCGS #9856)
```

## Data Validation Rules

1. **Cross-reference minimum 2 sources** for mintage data
2. **Flag discrepancies** between sources with notes
3. **Use most recent catalog** when sources conflict
4. **Prefer official mint reports** for production numbers
5. **Document variety discovery dates** when known

## Conflicting Data Protocol

When sources provide different information:

```
CONFLICT NOTED:
Field: [e.g., 1909-S VDB mintage]
Source A: Red Book 2025 - 484,000
Source B: PCGS CoinFacts - 484,000
Source C: Heritage Auctions - 420,000
RESOLUTION: Use Red Book/PCGS consensus of 484,000
NOTES: Heritage figure likely excludes damaged specimens
```

## AI Agent Instructions

When executing research tasks:

1. **Start with the Red Book** or equivalent national catalog
2. **Verify with grading services** (PCGS/NGC)
3. **Check mint records** for official production data
4. **Document varieties** from specialized references
5. **Include direct URLs** for online sources
6. **Note data gaps** that require manual verification
7. **Flag suspicious data** (e.g., round numbers, estimates)

## Quality Checklist

Before submitting researched data:

- [ ] All years in range covered
- [ ] All mint marks identified
- [ ] Business/Proof strikes separated
- [ ] Composition verified
- [ ] Weight/diameter confirmed
- [ ] Key dates marked
- [ ] Major varieties noted
- [ ] Sources properly cited
- [ ] Conflicts documented
- [ ] URLs tested and working

## Output Format

Research results should be formatted as migration scripts following the existing patterns in `/scripts/`. Example:

```python
def add_american_silver_eagles():
    """Add American Silver Eagle bullion coins (1986-2025)."""
    
    coins = [
        {
            'coin_id': 'US-ASE1-1986-P',
            'series_name': 'American Silver Eagle',
            'year': 1986,
            'mint': 'P',
            'business_strikes': 5393005,
            'proof_strikes': 0,
            'composition': {
                'silver': 99.9,
                'weight_grams': 31.103,
                'diameter_mm': 40.6
            },
            'source_citation': 'Red Book 2025, p. 377',
            # ... additional fields
        }
    ]
    
    return coins
```

## Periodic Updates

Research tasks should be re-run:
- **Annually** for ongoing series (bullion, commemoratives)
- **When new editions** of primary sources are released
- **When varieties** are discovered and authenticated
- **When mint reports** correct historical data

## Contact for Clarification

For questions about sourcing or data conflicts, create an issue with:
- Tag: `research-question`
- Title: `[Research] Question about [SERIES_NAME]`
- Include specific sources and page numbers in question