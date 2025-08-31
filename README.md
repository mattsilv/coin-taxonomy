# United States & Canada Coin Taxonomy Database

**The universal translator between different auction sites and marketplaces**

The coin taxonomy project becomes your universal translator between different auction sites, while providing standardized `COUNTRY-TYPE-YEAR-MINT` identifiers that create the foundation for comprehensive coin price intelligence systems.

With 2,567+ US coins, 558+ Canadian coins, and 82+ paper currency notes mapped to consistent IDs, this taxonomy enables seamless integration across eBay, Heritage, PCGS, NGC, and any coin marketplace or database.

**🌐 [Live Demo](https://mattsilv.github.io/coin-taxonomy/)** | **📊 [AI Formats](#ai-optimized-formats)** | **🔗 [Integration Guide](#integration-for-external-systems)** | **🔄 [Sync Instructions](#keeping-your-data-synchronized)**

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