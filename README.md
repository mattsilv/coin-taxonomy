# United States & Canada Coin Taxonomy Database

📚 **[Documentation Hub](./docs/PROJECT_DOCS.md)** | 📋 **[Release Notes](./docs/release-notes/README.md)** | 🌐 **[Live Demo](https://mattsilv.github.io/coin-taxonomy/)** | 📝 **[Changelog](./CHANGELOG.md)**

**The universal translator between different auction sites and marketplaces**

The coin taxonomy project becomes your universal translator between different auction sites, while providing standardized `COUNTRY-TYPE-YEAR-MINT` identifiers that create the foundation for comprehensive coin price intelligence systems.

With 2,567+ US coins, 558+ Canadian coins, and 82+ paper currency notes mapped to consistent IDs, this taxonomy enables seamless integration across eBay, Heritage, PCGS, NGC, and any coin marketplace or database.

**🌐 [Live Demo](https://mattsilv.github.io/coin-taxonomy/)** | **📊 [AI Formats](#ai-optimized-formats)** | **🔗 [Integration Guide](#integration-for-external-systems)** | **🔄 [Sync Instructions](#keeping-your-data-synchronized)**

## 🚀 NEW: Auction & Marketplace Integration (v1.3.0)

Parse auction listings and marketplace items with intelligent variant mapping:
- **Auction Parser**: Extract coin details from auction titles with 95%+ accuracy
- **Fuzzy Matching**: Handle typos, abbreviations, and non-standard formats
- **Variant Resolution**: Map special varieties to base coins automatically
- **Priority Scoring**: Resolve ambiguous cases (e.g., 1864 Two Cent → Large Motto)

```python
# Parse auction listing
from scripts.auction_catalog_parser import AuctionCatalogParser
parser = AuctionCatalogParser()
listing = parser.parse_listing("1918-D Buffalo Nickel 8/7 MS64 PCGS")
# Returns: Year=1918, Mint=D, Type=BUFFALO_NICKEL, Variant=8OVER7, Grade=MS-64

# Fuzzy match marketplace listing
from scripts.marketplace_listing_matcher import MarketplaceListingMatcher
matcher = MarketplaceListingMatcher()
result = matcher.match_listing("1918d buffallo nickle")  # With typos!
# Returns: US-BUFF-1918-D with confidence score
```

### 🎯 NEW: Unified Coin Grading Standard (External Metadata)

Standardize coin grades across all your marketplace integrations with canonical format validation:

**Grade Normalization** (Input → Output):
```python
from scripts.utils.grade_validator import GradeNormalizer
normalizer = GradeNormalizer()

# Accepts all variations, outputs canonical format
normalizer.normalize('MS65')    # → MS-65
normalizer.normalize('MS 65')   # → MS-65
normalizer.normalize('ms-65')   # → MS-65
normalizer.normalize('PR69')    # → PR-69
normalizer.normalize('AU58')    # → AU-58
```

**Real-World Examples**:
```python
# eBay listing: "1942 Mercury Dime MS67 Full Bands PCGS"
listing.grade = "MS-67"                    # Canonical format
listing.grading_service = "PCGS"          # Normalized service
listing.modifiers = ["FB"]                # Full Bands designation

# Heritage auction: "1909-S VDB Lincoln Cent PCGS MS64RB"
listing.grade = "MS-64"                    # Canonical format
listing.modifiers = ["RB"]                # Red-Brown color

# Raw (uncertified) coin: "1877 Indian Head Cent AU58"
listing.grade = "AU-58"                    # Canonical format
listing.grading_service = "raw"           # Not certified
```

**Complete Sheldon 70-Point Scale Supported**:
- Circulated: P-1, FR-2, AG-3, G-4, G-6, VG-8, VG-10, F-12, F-15, VF-20, VF-25, VF-30, VF-35, XF-40, XF-45, AU-50, AU-53, AU-55, AU-58
- Uncirculated: MS-60 through MS-70 (11 grades)
- Proof: PR-60 through PR-70 (11 grades)
- Specimen: SP-60 through SP-70

**Reference Files**:
- [`data/references/grades_unified.json`](data/references/grades_unified.json) - Complete grade scale
- [`data/references/grading_services.json`](data/references/grading_services.json) - PCGS & NGC details
- [`data/references/grade_modifiers.json`](data/references/grade_modifiers.json) - CAM, DCAM, FB, RD/RB/BN, etc.
- [`docs/external-metadata/COIN_GRADING.md`](docs/external-metadata/COIN_GRADING.md) - Complete developer guide

See [Issue #62](https://github.com/mattsilv/coin-taxonomy/issues/62) for full specification.

## What You Get

- **3,125+ coins across 2 countries** (US: 2,567, Canada: 558)
- **82+ paper currency notes** with standardized identifiers
- **Complete gold & silver bullion coverage** (Eagles, Maple Leafs, commemoratives)
- **Full pre-1933 gold coins** (1,123+ US coins across all denominations)
- **Modern bullion programs** (US & Canadian gold/silver/platinum/palladium)
- **SQLite database** as single source of truth (version controlled)
- **AI-optimized formats** for marketplace integration (10K-26K tokens)
- **Complete composition data** for melt value calculations
- **Pre-commit hooks** for automatic JSON generation

## Quick Start for Engineers

```bash
# Clone and setup
git clone https://github.com/mattsilv/coin-taxonomy.git
cd coin-taxonomy
uv venv && source .venv/bin/activate

# Generate database and exports
uv run python scripts/rebuild_and_export.py

# Map your listings to our taxonomy
uv run python scripts/import_listing.py
```

## Mapping Your Database

### Standard Coin ID Format: `COUNTRY-TYPE-YEAR-MINT`

**Real Examples from Our Database:**
```
US-LWCT-1909-S  → 1909-S Lincoln Wheat Cent (VDB variety available)
US-MERC-1916-D  → 1916-D Mercury Dime (Key date, only 264,000 minted)
US-WASH-1932-D  → 1932-D Washington Quarter (First year key date)
US-MORG-1921-D  → 1921-D Morgan Dollar (Last year of Morgans)
US-WLHD-1916-S  → 1916-S Walking Liberty Half (First year)
US-INCH-1877-P  → 1877 Indian Head Cent (Ultimate key date)
US-BUFF-1937-D  → 1937-D Buffalo Nickel (3-legged variety exists)
US-DESG-1907-P  → 1907 Saint-Gaudens Double Eagle (High Relief)
US-QEIH-1911-D  → 1911-D Indian Head Quarter Eagle (Key date)
US-GDLA-1849-P  → 1849 Gold Dollar Type I (First year)
```

**Commemorative Half Dollars** (139+ issues cataloged):
```
US-CHCO-1892-P  → 1892 World's Columbian Exposition
US-CHPP-1915-S  → 1915-S Panama-Pacific International Exposition
US-CHIL-1918-P  → 1918 Illinois Centennial
US-CHGR-1922-P  → 1922 Grant Memorial (with star variety)
US-CHOR-1926-P  → 1926 Oregon Trail Memorial (15 varieties 1926-1939)
US-CHDB-1934-P  → 1934 Daniel Boone Bicentennial (13 varieties)
US-CHTX-1934-P  → 1934 Texas Centennial (13 varieties 1934-1938)
US-CHAR-1935-P  → 1935 Arkansas Centennial (15 varieties 1935-1939)
US-CHCI-1936-P  → 1936 Cincinnati Music Center
US-CHGE-1936-P  → 1936 Battle of Gettysburg
US-CHBW-1946-P  → 1946 Booker T. Washington (18 varieties)
US-CHCW-1951-P  → 1951 Carver/Washington (12 varieties 1951-1954)
```
All commemorative halves include proper mint mark variations (P/D/S) and year ranges.

### Random Year Bullion Pattern

**NEW**: Bullion products sold as "random year" or "dealer's choice" at lowest premium over spot:

```
US-AGEO-XXXX-X  → American Gold Eagle 1 oz, random year, any mint
US-ASEA-XXXX-X  → American Silver Eagle 1 oz, random year, any mint
US-AGBF-XXXX-W  → American Gold Buffalo 1 oz, random year, West Point
CA-GMLO-XXXX-X  → Canadian Gold Maple Leaf 1 oz, random year
```

**Use Case**: Common dealer listings like "Gold Eagle 1 oz (Our Choice)" or "Silver Eagle - Varied Year" where specific year doesn't affect the bullion value. These are valued by metal content only, not numismatic value.

**Important**: XXXX pattern is **ONLY** for bullion products. Numismatic coins always need specific years.

### Handling Unknown Data

When mapping damaged or incomplete coins:
```
US-LWCT-YYYY-X  → Lincoln Wheat Cent, unknown year & mint
US-MERC-1942-X  → 1942 Mercury Dime, unknown mint (could be P, D, or S)
US-INCH-YYYY-P  → Indian Head Cent from Philadelphia, year unknown
US-BUFF-1936-X  → 1936 Buffalo Nickel, mint mark worn off
US-WASH-19XX-D  → Washington Quarter from Denver, decade visible (1940s, 1950s, etc)
```

### Common eBay Listings → Our Taxonomy IDs
```
"1943 Steel Penny"           → US-LWCT-1943-P (also -D, -S variants)
"1916 Mercury Dime Denver"   → US-MERC-1916-D
"Morgan Silver Dollar 1921"  → US-MORG-1921-P (also -D, -S variants)
"Walking Liberty Half 1942"  → US-WLHD-1942-P (also -D, -S variants)
"Indian Head Penny 1909"     → US-INCH-1909-P (last year)
"Buffalo Nickel no date"     → US-BUFF-YYYY-X
"Kennedy Half 1964 Silver"   → US-KHDO-1964-P (90% silver)
"Wheat Penny 1909 VDB"       → US-LWCT-1909-P (VDB variety)
```

### 📊 Numismatic Market Index (7-Coin Baseline) → Taxonomy Mapping

**Theoretical index tracking highly liquid, certified U.S. coins for market sentiment analysis.**

This demonstrates mapping investment-grade coins (PCGS/NGC certified) to standardized IDs with full grade metadata:

| Metal  | Coin Type                  | Marketplace Listing                           | Taxonomy ID    | Grade  | Modifiers |
|--------|----------------------------|-----------------------------------------------|----------------|--------|-----------|
| Copper | Lincoln Wheat Cent         | "1958 Lincoln Wheat Cent PCGS MS65 RD"        | US-LWCT-1958-P | MS-65  | RD        |
| Nickel | Buffalo Nickel             | "1937 Buffalo Nickel NGC MS66"                | US-BUFF-1937-P | MS-66  |           |
| Silver | Standing Liberty Quarter   | "1930 Standing Liberty Quarter PCGS MS64"     | US-SLIQ-1930-P | MS-64  |           |
| Silver | Morgan Silver Dollar       | "1921 Morgan Dollar NGC MS65"                 | US-MORG-1921-P | MS-65  |           |
| Silver | Peace Silver Dollar        | "1922 Peace Dollar PCGS MS63"                 | US-PEAC-1922-P | MS-63  |           |
| Gold   | Saint-Gaudens Double Eagle | "1924 Saint-Gaudens $20 NGC MS63"             | US-DESG-1924-P | MS-63  |           |
| Gold   | Indian Head Eagle          | "1925 Indian Head $10 PCGS MS63"              | US-QEIH-1925-P | MS-63  |           |

**Grade Normalization Applied:**
```python
# Input: "1921 Morgan Dollar NGC MS65"
{
  "coin_id": "US-MORG-1921-P",
  "grade": "MS-65",              # Canonical format
  "grading_service": "NGC",      # Normalized uppercase
  "certification_number": "1234567",
  "metal_content": "90% silver", # From composition registry
  "market_threshold": true       # MS-65 is key price tier
}

# Input: "1958 Lincoln Wheat Cent PCGS MS65RD"
{
  "coin_id": "US-LWCT-1958-P",
  "grade": "MS-65",              # Canonical format
  "grading_service": "PCGS",
  "modifiers": ["RD"],           # Red designation
  "certification_number": "87654321"
}
```

**Index Use Cases:**
- **Market tracking**: Monitor quarterly price changes across denominations
- **Portfolio management**: Track certified coin investments with consistent IDs
- **Price normalization**: Isolate numismatic premium from spot metal prices
- **Liquidity analysis**: High-population coins ensure reliable pricing data

**Rationale:**
- 10,000+ PCGS/NGC population for each coin ensures deep liquidity
- Balanced exposure: Copper (1), Nickel (1), Silver (3), Gold (2)
- Common dates with strong collector demand
- Standardized grades (MS63-MS66) represent mainstream market

### Type Code Reference

**Common Coin Types** (4-letter codes):
```python
# Cents
INCH = Indian Head Cent       LWCT = Lincoln Wheat Cent
LMCT = Lincoln Memorial Cent  LSCT = Lincoln Shield Cent

# Nickels  
JEFF = Jefferson Nickel       BUFF = Buffalo Nickel

# Dimes
MERC = Mercury Dime           ROOS = Roosevelt Dime

# Quarters
WASH = Washington Quarter     SLIQ = Standing Liberty Quarter

# Dollars
MORG = Morgan Dollar          PEAC = Peace Dollar
TRDO = Trade Dollar

# Gold Bullion (Modern)
AGEO = American Gold Eagle 1oz    AGEH = American Gold Eagle 1/2oz
AGEQ = American Gold Eagle 1/4oz  AGET = American Gold Eagle 1/10oz
AGBF = American Buffalo Gold

# Silver Bullion (Modern)
ASEA = American Silver Eagle      ATBQ = America the Beautiful 5oz
MSMC = Morgan Commemorative       PSMC = Peace Commemorative
```

**Paper Currency Examples:**
```python
# Federal Reserve Notes
US-FRN-1963-A-1    = $1 Federal Reserve Note Series 1963A
US-SC-1923-P-1     = $1 Silver Certificate Series 1923
US-LTN-1880-P-10   = $10 Legal Tender Note Series 1880
US-FRN-1934-A-100  = $100 Federal Reserve Note Series 1934A
```

[Full type code list](data/universal/series_registry.json)

## AI-Optimized Formats

Two formats optimized for different use cases:

### Year-List Format (10K tokens)
**File:** [`data/ai-optimized/us_taxonomy_year_list.json`](data/ai-optimized/us_taxonomy_year_list.json)
```json
{
  "series": "lincoln_wheat_cent",
  "t": "LWCT",
  "years": "1909,1910,1911,1912,1913...",
  "ob": "Abraham Lincoln bust facing right..."
}
```
**Use for:** Year-based classification, GPT-3.5 compatible

### Coin-ID Format (26K tokens)  
**File:** [`data/ai-optimized/us_taxonomy.json`](data/ai-optimized/us_taxonomy.json)
```json
{
  "series": "lincoln_wheat_cent",
  "t": "LWCT",
  "coin_ids": "US-LWCT-1909-P,US-LWCT-1909-D,US-LWCT-1909-S..."
}
```
**Use for:** Exact coin matching, marketplace integration

## Integration Scripts

### Marketplace Listing Matcher
**Script:** [`scripts/import_listing.py`](scripts/import_listing.py)
```python
# Match eBay/marketplace listings to taxonomy
uv run python scripts/import_listing.py
# Enter: "1909 S Lincoln Cent VDB"
# Returns: US-LWCT-1909-S (with VDB variety)
```

### Melt Value Calculator
**Script:** [`scripts/calculate_melt.py`](scripts/calculate_melt.py)
```python
# Calculate silver content value
uv run python scripts/calculate_melt.py
# Uses composition_registry.json for metal content
```

### Database Export Pipeline
**Script:** [`scripts/export_from_database.py`](scripts/export_from_database.py)
```bash
# Regenerate all JSON from SQLite
uv run python scripts/export_from_database.py
```

## Database Architecture

### SQLite Database (Source of Truth)
**Location:** `database/coins.db`

**Key tables:**
- `issues` - Universal flat structure for all coins
- `coins` - Legacy US coin data  
- `composition_registry` - Metal content definitions
- `series_registry` - Series metadata

### Export Formats

**Universal Format:** [`data/universal/us_issues.json`](data/universal/us_issues.json)
```json
{
  "issue_id": "US-LWCT-1909-S",
  "object_type": "coin",
  "denomination": {...},
  "specifications": {...}
}
```

**Legacy Format:** [`data/us/us_coins_complete.json`](data/us/us_coins_complete.json)
```json
{
  "series_name": "Lincoln Wheat Cent",
  "coins": [{"coin_id": "US-LWCT-1909-S", ...}]
}
```

## Sample Integration Code

### Python Example
```python
import sqlite3
import json

# Connect to taxonomy database
conn = sqlite3.connect('database/coins.db')
cursor = conn.cursor()

# Map your listing to taxonomy
listing = "1909 S Lincoln Cent VDB"
cursor.execute("""
    SELECT coin_id, year, mint 
    FROM coins 
    WHERE series_name LIKE '%Lincoln%' 
    AND year = 1909 
    AND mint = 'S'
""")
result = cursor.fetchone()
print(f"Taxonomy ID: {result[0]}")  # US-LWCT-1909-S
```

### JavaScript Example  
```javascript
// Load AI-optimized format
const taxonomy = require('./data/ai-optimized/us_taxonomy.json');

// Find series by type code
const lincolnWheat = taxonomy.series.find(s => s.t === 'LWCT');
console.log(lincolnWheat.coin_ids.split(','));
// ['US-LWCT-1909-P', 'US-LWCT-1909-D', 'US-LWCT-1909-S', ...]
```

## Advanced Features

### Variety Handling
Varieties stored separately from coin IDs:
```json
{
  "coin_id": "US-LWCT-1909-S",
  "varieties": [
    {"name": "VDB", "description": "Designer initials on reverse"}
  ]
}
```

### Composition Tracking
Precise metal content with transition dates:
- 90% silver dimes/quarters: 1796-1964
- Wartime silver nickels: 1942-1945 (35% silver)
- Clad coinage: 1965-present

### Key Date Identification  
39 verified key dates with market-based rarity:
- `US-MERC-1916-D` - King of Mercury dimes
- `US-LWCT-1909-S` - VDB variety
- `US-WASH-1932-D` - First year key date

## Resources

- **[Live Demo](https://mattsilv.github.io/coin-taxonomy/)** - Search interface
- **[Developer Guide](docs/CONTRIBUTING_DEVELOPERS.md)** - Schema docs
- **[Research Notes](docs/coin-research.md)** - Mintage analysis
- **[Series Registry](data/universal/series_registry.json)** - All type codes
- **[Composition Data](data/universal/composition_registry.json)** - Metal content

## Data Quality

- **Sources:** PCGS, NGC, Red Book, US Mint
- **Validation:** JSON Schema + automated tests
- **Coverage:** 1,539+ coins, 48+ series (1793-present)
- **Updates:** Git-tracked with full audit trail

## Integration for External Systems

### For E-commerce & Auction Platforms

If you're using this taxonomy as a source of truth for your coin auction platform, marketplace, or pricing engine, here's how to efficiently integrate and stay synchronized:

#### Recommended Integration Approach

1. **Use the Universal Format** (Most Efficient)
   ```bash
   # Fetch the complete universal taxonomy (includes all countries)
   curl -H "Accept: application/vnd.github.v3.raw" \
     https://api.github.com/repos/mattsilv/coin-taxonomy/contents/data/universal/us_issues.json \
     > us_issues.json
   
   curl -H "Accept: application/vnd.github.v3.raw" \
     https://api.github.com/repos/mattsilv/coin-taxonomy/contents/data/universal/ca_issues.json \
     > ca_issues.json
   ```

2. **Or Clone the SQLite Database** (Most Complete)
   ```bash
   # Download the latest database directly
   curl -H "Accept: application/vnd.github.v3.raw" \
     https://api.github.com/repos/mattsilv/coin-taxonomy/contents/coins.db \
     > coins.db
   ```

3. **Or Use CDN for JSON Files** (Fastest)
   ```javascript
   // Use jsDelivr CDN for automatic caching
   const US_TAXONOMY = 'https://cdn.jsdelivr.net/gh/mattsilv/coin-taxonomy@main/data/universal/us_issues.json';
   const CA_TAXONOMY = 'https://cdn.jsdelivr.net/gh/mattsilv/coin-taxonomy@main/data/universal/ca_issues.json';
   
   fetch(US_TAXONOMY)
     .then(res => res.json())
     .then(data => console.log(`Loaded ${data.totalIssues} US coins`));
   ```

## Keeping Your Data Synchronized

### Automated Sync Strategy

#### Option 1: GitHub Actions (Recommended)
Create `.github/workflows/sync-taxonomy.yml` in your repo:

```yaml
name: Sync Coin Taxonomy
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:      # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Fetch Latest Taxonomy
        run: |
          # Fetch universal format files
          curl -H "Accept: application/vnd.github.v3.raw" \
            https://api.github.com/repos/mattsilv/coin-taxonomy/contents/data/universal/us_issues.json \
            > data/us_issues.json
          
          curl -H "Accept: application/vnd.github.v3.raw" \
            https://api.github.com/repos/mattsilv/coin-taxonomy/contents/data/universal/ca_issues.json \
            > data/ca_issues.json
          
          # Fetch metadata files
          curl -H "Accept: application/vnd.github.v3.raw" \
            https://api.github.com/repos/mattsilv/coin-taxonomy/contents/data/universal/taxonomy_summary.json \
            > data/taxonomy_summary.json
      
      - name: Check for Updates
        id: check
        run: |
          git diff --exit-code data/ || echo "::set-output name=changed::true"
      
      - name: Commit Updates
        if: steps.check.outputs.changed == 'true'
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add data/
          git commit -m "Update coin taxonomy $(date +%Y-%m-%d)"
          git push
```

#### Option 2: Webhook Integration
Monitor repository changes via GitHub webhooks:

```python
# Flask webhook endpoint example
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.json
    
    # Check if commits affect data files
    if any('data/' in commit['modified'] for commit in payload['commits']):
        # Trigger your sync process
        subprocess.run(['python', 'sync_taxonomy.py'])
    
    return 'OK', 200
```

#### Option 3: Simple Cron Script
```bash
#!/bin/bash
# sync_taxonomy.sh - Run daily via cron

# Get latest commit hash
LATEST=$(curl -s https://api.github.com/repos/mattsilv/coin-taxonomy/commits/main | jq -r '.sha')
CURRENT=$(cat .taxonomy_version 2>/dev/null)

if [ "$LATEST" != "$CURRENT" ]; then
  echo "Updating taxonomy from $CURRENT to $LATEST"
  
  # Download latest files
  wget -q https://raw.githubusercontent.com/mattsilv/coin-taxonomy/main/data/universal/us_issues.json
  wget -q https://raw.githubusercontent.com/mattsilv/coin-taxonomy/main/data/universal/ca_issues.json
  wget -q https://raw.githubusercontent.com/mattsilv/coin-taxonomy/main/coins.db
  
  # Save version
  echo "$LATEST" > .taxonomy_version
  
  # Trigger your import process
  python import_taxonomy.py
fi
```

### Change Detection & Versioning

The taxonomy includes built-in versioning:

```json
// data/universal/taxonomy_summary.json
{
  "taxonomy_version": "1.1",
  "generated_at": "2025-08-31T17:42:40.588489+00:00",
  "total_issues": 329,
  "countries": 2
}
```

Monitor this file to detect updates:
- `taxonomy_version`: Major schema changes
- `generated_at`: Last update timestamp
- `total_issues`: Count changes indicate new coins

### API Rate Limits & Best Practices

1. **GitHub API Limits**: 60 requests/hour (unauthenticated), 5000/hour (authenticated)
2. **Use CDN for Production**: jsDelivr has no rate limits and caches files
3. **Cache Locally**: Store files with 24-hour TTL minimum
4. **Batch Requests**: Fetch all needed files in one sync operation

### Production Integration Example

```python
import requests
import json
import sqlite3
from datetime import datetime, timedelta

class TaxonomySync:
    def __init__(self, cache_hours=24):
        self.cache_hours = cache_hours
        self.base_url = "https://cdn.jsdelivr.net/gh/mattsilv/coin-taxonomy@main"
        
    def needs_update(self):
        """Check if local cache is stale"""
        try:
            with open('.last_sync', 'r') as f:
                last_sync = datetime.fromisoformat(f.read())
                return datetime.now() - last_sync > timedelta(hours=self.cache_hours)
        except:
            return True
    
    def sync_taxonomy(self):
        """Sync taxonomy data from GitHub"""
        if not self.needs_update():
            return False
        
        # Fetch summary first to check version
        summary = requests.get(f"{self.base_url}/data/universal/taxonomy_summary.json").json()
        
        # Fetch country-specific data
        us_data = requests.get(f"{self.base_url}/data/universal/us_issues.json").json()
        ca_data = requests.get(f"{self.base_url}/data/universal/ca_issues.json").json()
        
        # Store in your database
        self.import_to_database(us_data, ca_data)
        
        # Update sync timestamp
        with open('.last_sync', 'w') as f:
            f.write(datetime.now().isoformat())
        
        return True
    
    def import_to_database(self, us_data, ca_data):
        """Import taxonomy into your database"""
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        
        for issue in us_data['issues'] + ca_data['issues']:
            cursor.execute("""
                INSERT OR REPLACE INTO coin_taxonomy 
                (coin_id, country, denomination, year, mint, series_name, rarity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                issue['issueId'],
                issue['country'],
                issue['denomination'],
                issue['year'],
                issue['mint'],
                issue['seriesName'],
                issue.get('rarity', 'common')
            ))
        
        conn.commit()
        conn.close()

# Usage
syncer = TaxonomySync()
if syncer.sync_taxonomy():
    print("Taxonomy updated successfully")
```

### Support & Updates

- **Issues**: Report at [GitHub Issues](https://github.com/mattsilv/coin-taxonomy/issues)
- **Updates**: Watch the repo for release notifications
- **Breaking Changes**: Will increment `taxonomy_version` in summary file
- **Data Corrections**: Submitted via pull requests with validation

## License

MIT License - Open source for commercial and non-commercial use.

For numismatic tools and updates: **[silv.app](https://www.silv.app)**