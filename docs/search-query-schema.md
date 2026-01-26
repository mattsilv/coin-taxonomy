# Search Query Schema Documentation

This document defines the JSON schema for search query configuration files used by coin data aggregation systems.

## Overview

Search query configuration files define how to search for specific coin series across auction platforms and marketplaces. They provide:

- **Search strategies** for finding relevant listings
- **Validation keywords** for filtering results
- **Exclusion patterns** to remove false positives
- **Filter thresholds** for seller quality and pricing

## File Location

Search query configurations are stored in:
```
data/search-queries/{series-category}.json
```

Example: `data/search-queries/commemorative-halves.json`

## Schema Structure

### Root Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Semantic version of the configuration |
| `last_updated` | string | Yes | ISO date of last update (YYYY-MM-DD) |
| `description` | string | Yes | Human-readable description |
| `filter_config` | object | Yes | Global filtering rules |
| `commemorative_halves` | array | Yes | Array of series configurations |

### Filter Configuration

The `filter_config` object defines global filtering rules applied to all results.

```json
{
  "filter_config": {
    "seller_min_feedback_score": 100,
    "seller_min_feedback_percentage": 98.0,
    "price_floor_graded_usd": 10,
    "accepted_grading_services": ["PCGS", "NGC", "CACG", "CAC"],
    "rejected_grading_services": ["ANACS", "ICG", "PCI", "SEGS", "NTC"],
    "global_exclusion_terms": ["copy", "replica", "plated", "tribute"]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `seller_min_feedback_score` | integer | Minimum seller feedback count |
| `seller_min_feedback_percentage` | float | Minimum positive feedback % (0-100) |
| `price_floor_graded_usd` | integer | Minimum price for graded coins (filters junk) |
| `accepted_grading_services` | array | Grading companies to accept |
| `rejected_grading_services` | array | Grading companies to exclude |
| `global_exclusion_terms` | array | Terms that indicate fakes/replicas |

### Series Configuration

Each entry in the series array defines search parameters for one coin series.

```json
{
  "series_code": "FTVA",
  "series_name": "Fort Vancouver Centennial",
  "taxonomy_id_pattern": "US-FTVA-{year}-P",
  "years": [1925],
  "search_strategy": "year_specific",
  "primary_search": "1925 fort vancouver MS",
  "broad_search": "fort vancouver half dollar",
  "validation_keywords": ["vancouver", "fort vancouver"],
  "exclusion_keywords": [],
  "min_results_threshold": 20,
  "notes": "Single year."
}
```

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `series_code` | string | 4-letter code matching taxonomy (e.g., "FTVA") |
| `series_name` | string | Full series name |
| `taxonomy_id_pattern` | string | Pattern for generating coin IDs |
| `years` | array | Years the series was minted |
| `search_strategy` | string | Either `"year_specific"` or `"keyword_only"` |
| `primary_search` | string | High-precision search query |
| `broad_search` | string | Lower-precision fallback query |
| `validation_keywords` | array | At least one must appear in listing |
| `exclusion_keywords` | array | Exclude listings containing these |
| `min_results_threshold` | integer | Minimum expected results (for alerts) |

#### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `mints` | array | Mint marks for multi-mint series |
| `notes` | string | Human-readable notes about the series |

## Search Strategies

### `year_specific`

Use for **single-year series** or when the year is a strong identifier.

**When to use:**
- Series minted in only one year
- Year + series name combination is unique
- Risk of matching other years is low

**Query generation:**
```
primary_search: "1925 fort vancouver MS"
  → Search includes year for precision
```

**Example series:**
- Fort Vancouver (1925 only)
- Illinois Centennial (1918 only)
- Maine Centennial (1920 only)

### `keyword_only`

Use for **multi-year series** or when including year would miss results.

**When to use:**
- Series spans multiple years
- Series has naming collision risk with other products
- Broader search yields better recall

**Query generation:**
```
primary_search: "oregon trail MS"
  → Search excludes year, relies on series name
```

**Example series:**
- Oregon Trail (1926-1939, multiple years)
- Daniel Boone (1934-1938, multiple mints)
- World's Columbian Exposition (1892-1893)

## Validation Keywords

Validation keywords filter search results to ensure relevance. At least one keyword must appear in the listing title or description.

**Best practices:**
- Include common names and abbreviations
- Include key design elements (e.g., "lincoln" for Illinois Centennial)
- Use lowercase (matching is case-insensitive)

```json
{
  "series_code": "ILCN",
  "validation_keywords": ["illinois", "lincoln"]
}
```

## Exclusion Keywords

Exclusion keywords filter out false positives and prevent matching wrong products.

**Common exclusion patterns:**

| Pattern | Reason |
|---------|--------|
| `"gold"`, `"$50"` | Exclude gold variants of the same event |
| `"quarter"`, `"state quarter"` | Exclude modern State Quarters |
| `"medal"`, `"token"` | Exclude non-coin collectibles |
| `"columbian"`, `"columbus"` | Avoid series name collisions |

**Example: Gettysburg (naming collision risk)**

```json
{
  "series_code": "GTYB",
  "series_name": "Battle of Gettysburg",
  "search_strategy": "keyword_only",
  "validation_keywords": ["gettysburg"],
  "exclusion_keywords": ["quarter", "medal", "token"],
  "notes": "Single year. Use keyword_only to avoid matching medals/tokens."
}
```

## Examples by Series Type

### Single-Year Series (Fort Vancouver)

```json
{
  "series_code": "FTVA",
  "series_name": "Fort Vancouver Centennial",
  "taxonomy_id_pattern": "US-FTVA-{year}-P",
  "years": [1925],
  "search_strategy": "year_specific",
  "primary_search": "1925 fort vancouver MS",
  "broad_search": "fort vancouver half dollar",
  "validation_keywords": ["vancouver", "fort vancouver"],
  "exclusion_keywords": [],
  "min_results_threshold": 20,
  "notes": "Single year."
}
```

**Characteristics:**
- Single year (1925), so `year_specific` strategy works well
- Year in primary search provides precision
- No exclusions needed (unique series name)

### Multi-Year Series (Oregon Trail)

```json
{
  "series_code": "ORTR",
  "series_name": "Oregon Trail Memorial",
  "taxonomy_id_pattern": "US-ORTR-{year}-{mint}",
  "years": [1926, 1928, 1933, 1934, 1936, 1937, 1938, 1939],
  "mints": ["P", "D", "S"],
  "search_strategy": "keyword_only",
  "primary_search": "oregon trail MS",
  "broad_search": "oregon trail half commemorative",
  "validation_keywords": ["oregon trail", "oregon"],
  "exclusion_keywords": ["quarter", "state quarter"],
  "min_results_threshold": 20,
  "notes": "Multi-year series (1926-1939). Exclude Oregon State Quarters."
}
```

**Characteristics:**
- Spans 8 years across 3 mints
- `keyword_only` captures all years in one search
- Excludes "state quarter" to avoid Oregon State Quarter matches
- `mints` field specifies mint variations

### Naming Collision Risk (Gettysburg)

```json
{
  "series_code": "GTYB",
  "series_name": "Battle of Gettysburg",
  "taxonomy_id_pattern": "US-GTYB-{year}-P",
  "years": [1936],
  "search_strategy": "keyword_only",
  "primary_search": "gettysburg half MS",
  "broad_search": "gettysburg commemorative half",
  "validation_keywords": ["gettysburg"],
  "exclusion_keywords": ["quarter", "medal", "token"],
  "min_results_threshold": 20,
  "notes": "Single year. Use keyword_only to avoid matching medals/tokens."
}
```

**Characteristics:**
- Single year BUT uses `keyword_only` strategy
- "Gettysburg" appears on many non-coin products (medals, tokens)
- Primary search includes "half" to specify denomination
- Exclusions filter out medals and tokens

## Consumer Integration

### TypeScript

```typescript
import { readFileSync } from 'fs';

interface FilterConfig {
  seller_min_feedback_score: number;
  seller_min_feedback_percentage: number;
  price_floor_graded_usd: number;
  accepted_grading_services: string[];
  rejected_grading_services: string[];
  global_exclusion_terms: string[];
}

interface SeriesConfig {
  series_code: string;
  series_name: string;
  taxonomy_id_pattern: string;
  years: number[];
  mints?: string[];
  search_strategy: 'year_specific' | 'keyword_only';
  primary_search: string;
  broad_search: string;
  validation_keywords: string[];
  exclusion_keywords: string[];
  min_results_threshold: number;
  notes?: string;
}

interface SearchQueryConfig {
  version: string;
  last_updated: string;
  description: string;
  filter_config: FilterConfig;
  commemorative_halves: SeriesConfig[];
}

// Load configuration
function loadSearchConfig(path: string): SearchQueryConfig {
  const content = readFileSync(path, 'utf-8');
  return JSON.parse(content) as SearchQueryConfig;
}

// Example: Generate search queries for a series
function generateSearchQueries(config: SeriesConfig): string[] {
  const queries: string[] = [config.primary_search];

  if (config.search_strategy === 'year_specific') {
    // Add year-specific variants for each year
    for (const year of config.years) {
      queries.push(`${year} ${config.series_name}`);
    }
  }

  queries.push(config.broad_search);
  return queries;
}

// Example: Validate a listing
function validateListing(
  title: string,
  config: SeriesConfig,
  filterConfig: FilterConfig
): boolean {
  const titleLower = title.toLowerCase();

  // Check global exclusions
  for (const term of filterConfig.global_exclusion_terms) {
    if (titleLower.includes(term.toLowerCase())) {
      return false;
    }
  }

  // Check series-specific exclusions
  for (const term of config.exclusion_keywords) {
    if (titleLower.includes(term.toLowerCase())) {
      return false;
    }
  }

  // Check validation keywords (at least one must match)
  const hasValidKeyword = config.validation_keywords.some(
    keyword => titleLower.includes(keyword.toLowerCase())
  );

  return hasValidKeyword;
}
```

### Python

```python
import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class FilterConfig:
    seller_min_feedback_score: int
    seller_min_feedback_percentage: float
    price_floor_graded_usd: int
    accepted_grading_services: list[str]
    rejected_grading_services: list[str]
    global_exclusion_terms: list[str]

@dataclass
class SeriesConfig:
    series_code: str
    series_name: str
    taxonomy_id_pattern: str
    years: list[int]
    search_strategy: str  # "year_specific" or "keyword_only"
    primary_search: str
    broad_search: str
    validation_keywords: list[str]
    exclusion_keywords: list[str]
    min_results_threshold: int
    mints: Optional[list[str]] = None
    notes: Optional[str] = None

class SearchQueryConfig:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            data = json.load(f)

        self.version = data['version']
        self.last_updated = data['last_updated']
        self.description = data['description']

        self.filter_config = FilterConfig(**data['filter_config'])

        self.series = [
            SeriesConfig(**series_data)
            for series_data in data['commemorative_halves']
        ]

    def get_series_by_code(self, code: str) -> Optional[SeriesConfig]:
        """Find a series by its 4-letter code."""
        for series in self.series:
            if series.series_code == code:
                return series
        return None

    def validate_listing(self, title: str, series: SeriesConfig) -> bool:
        """Check if a listing title matches the series criteria."""
        title_lower = title.lower()

        # Check global exclusions
        for term in self.filter_config.global_exclusion_terms:
            if term.lower() in title_lower:
                return False

        # Check series-specific exclusions
        for term in series.exclusion_keywords:
            if term.lower() in title_lower:
                return False

        # Check validation keywords (at least one must match)
        return any(
            keyword.lower() in title_lower
            for keyword in series.validation_keywords
        )

    def generate_taxonomy_id(self, series: SeriesConfig, year: int, mint: str) -> str:
        """Generate a taxonomy ID for a specific coin."""
        return series.taxonomy_id_pattern.format(year=year, mint=mint)


# Usage example
if __name__ == '__main__':
    config = SearchQueryConfig('data/search-queries/commemorative-halves.json')

    # Find a series
    oregon = config.get_series_by_code('ORTR')
    if oregon:
        print(f"Oregon Trail: {oregon.years}")
        print(f"Strategy: {oregon.search_strategy}")

        # Generate taxonomy ID
        coin_id = config.generate_taxonomy_id(oregon, 1926, 'P')
        print(f"Coin ID: {coin_id}")  # US-ORTR-1926-P

    # Validate a listing
    title = "1936 Oregon Trail Commemorative Half Dollar MS65 PCGS"
    is_valid = config.validate_listing(title, oregon)
    print(f"Valid: {is_valid}")  # True
```

## Related Documentation

- [Taxonomy ID Format](./taxonomy-id-format.md) - Coin ID structure
- [Commemorative Half Dollars](./series-codes/commemorative-half-dollars.md) - Series codes reference
- [Integration Guide](./INTEGRATION_GUIDE.md) - General integration patterns

## Related Issues

- coindex-monorepo PR #106 - Filter pipeline implementation
- silv-scraper #219 - Python integration
- u2-server #308 - Python integration
