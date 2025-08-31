# Integration Guide for Coin Taxonomy

## Overview

This guide is for engineers integrating the coin-taxonomy database into their e-commerce platforms, auction systems, or pricing engines. The taxonomy provides standardized `COUNTRY-TYPE-YEAR-MINT` identifiers for 3,125+ coins across US and Canada.

## Quick Start

### 1. Choose Your Integration Method

#### Method A: Universal JSON Format (Recommended)
Best for: Web applications, microservices, APIs

```javascript
// Fetch via CDN (cached, no rate limits)
const US_COINS = 'https://cdn.jsdelivr.net/gh/mattsilv/coin-taxonomy@main/data/universal/us_issues.json';
const CA_COINS = 'https://cdn.jsdelivr.net/gh/mattsilv/coin-taxonomy@main/data/universal/ca_issues.json';

async function loadTaxonomy() {
  const [usData, caData] = await Promise.all([
    fetch(US_COINS).then(r => r.json()),
    fetch(CA_COINS).then(r => r.json())
  ]);
  
  console.log(`Loaded ${usData.totalIssues} US coins`);
  console.log(`Loaded ${caData.totalIssues} CA coins`);
  return { us: usData, ca: caData };
}
```

#### Method B: SQLite Database
Best for: Desktop applications, data analysis, complex queries

```python
import sqlite3
import requests

# Download latest database
response = requests.get(
    'https://github.com/mattsilv/coin-taxonomy/raw/main/coins.db',
    headers={'Accept': 'application/vnd.github.v3.raw'}
)
with open('coins.db', 'wb') as f:
    f.write(response.content)

# Query the database
conn = sqlite3.connect('coins.db')
cursor = conn.cursor()

# Example: Find all Morgan Dollars
cursor.execute("""
    SELECT coin_id, year, mint, rarity 
    FROM coins 
    WHERE series LIKE '%Morgan%'
    ORDER BY year, mint
""")
morgans = cursor.fetchall()
```

#### Method C: AI-Optimized Format
Best for: LLM applications, token-limited contexts

```python
# Compact format with comma-delimited years
import requests

taxonomy = requests.get(
    'https://cdn.jsdelivr.net/gh/mattsilv/coin-taxonomy@main/data/ai-optimized/us_taxonomy.json'
).json()

# Each series contains comma-delimited coin IDs
for series in taxonomy['series']:
    coin_ids = series['coin_ids'].split(',')
    print(f"{series['name']}: {len(coin_ids)} coins")
```

## Data Structure

### Universal Format Schema

```typescript
interface Issue {
  issueId: string;        // "US-MORG-1921-D"
  country: string;        // "US" or "CA"
  denomination: string;   // "Dollars"
  year: number;          // 1921
  mint: string;          // "D"
  seriesName: string;    // "Morgan Dollar"
  rarity: string;        // "common", "scarce", "key"
  businessStrikes?: number;
  proofStrikes?: number;
  composition: {
    silver?: number;     // 0.9 = 90%
    copper?: number;
    gold?: number;
  };
  weightGrams: number;
  diameterMm: number;
  varieties?: Array<{
    name: string;
    premium: boolean;
  }>;
  obverseDescription: string;
  reverseDescription: string;
  commonNames?: string;
}
```

### Coin ID Format

All coins follow the pattern: `COUNTRY-TYPE-YEAR-MINT`

```
US-MORG-1921-D  → 1921-D Morgan Dollar
CA-LOON-1987-P  → 1987 Canadian Loonie
US-LWCT-1909-S  → 1909-S Lincoln Wheat Cent
CA-GMPL-2023-P  → 2023 Gold Maple Leaf
```

## Synchronization Strategies

### 1. Daily Sync via GitHub Actions

Create `.github/workflows/sync-taxonomy.yml`:

```yaml
name: Sync Coin Taxonomy
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Fetch Latest Data
        run: |
          mkdir -p data/taxonomy
          
          # Core data files
          for file in us_issues.json ca_issues.json taxonomy_summary.json; do
            curl -sL "https://raw.githubusercontent.com/mattsilv/coin-taxonomy/main/data/universal/$file" \
              > "data/taxonomy/$file"
          done
          
          # Registry files
          for file in series_registry.json composition_registry.json; do
            curl -sL "https://raw.githubusercontent.com/mattsilv/coin-taxonomy/main/data/universal/$file" \
              > "data/taxonomy/$file"
          done
      
      - name: Process Updates
        run: python scripts/import_taxonomy.py
      
      - name: Deploy
        run: |
          # Your deployment process here
          echo "Taxonomy updated"
```

### 2. Real-time Webhook Updates

```python
from flask import Flask, request
import hashlib
import hmac

app = Flask(__name__)
WEBHOOK_SECRET = 'your-github-webhook-secret'

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # Verify webhook signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return 'Unauthorized', 401
    
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    if event == 'push':
        # Check if taxonomy files were updated
        files_changed = set()
        for commit in payload.get('commits', []):
            files_changed.update(commit.get('modified', []))
            files_changed.update(commit.get('added', []))
        
        if any('data/universal/' in f for f in files_changed):
            # Trigger sync
            sync_taxonomy()
    
    return 'OK', 200

def verify_signature(payload, signature):
    if not signature:
        return False
    
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)

def sync_taxonomy():
    # Your sync implementation
    print("Syncing taxonomy updates...")
```

### 3. Incremental Updates

```python
import json
from datetime import datetime

class IncrementalSync:
    def __init__(self):
        self.state_file = '.taxonomy_state.json'
    
    def get_last_sync(self):
        try:
            with open(self.state_file) as f:
                return json.load(f)
        except:
            return {'version': '0.0', 'timestamp': None, 'total_issues': 0}
    
    def check_for_updates(self):
        # Fetch summary
        import requests
        summary = requests.get(
            'https://cdn.jsdelivr.net/gh/mattsilv/coin-taxonomy@main/data/universal/taxonomy_summary.json'
        ).json()
        
        last_sync = self.get_last_sync()
        
        # Check if update needed
        if (summary['taxonomy_version'] != last_sync['version'] or
            summary['total_issues'] != last_sync['total_issues']):
            return True, summary
        
        return False, None
    
    def sync_if_needed(self):
        needs_update, summary = self.check_for_updates()
        
        if needs_update:
            print(f"Updating from v{self.get_last_sync()['version']} to v{summary['taxonomy_version']}")
            
            # Perform sync
            self.perform_sync()
            
            # Save state
            with open(self.state_file, 'w') as f:
                json.dump({
                    'version': summary['taxonomy_version'],
                    'timestamp': datetime.now().isoformat(),
                    'total_issues': summary['total_issues']
                }, f)
            
            return True
        
        return False
```

## Mapping eBay/Heritage Listings

### Common Patterns

```python
LISTING_PATTERNS = {
    # Pattern: (regex, coin_id_template)
    r'(\d{4})\s*-?([PDSO])\s+Morgan\s+Dollar': 'US-MORG-{0}-{1}',
    r'(\d{4})\s+Mercury\s+Dime\s+([PDSO])': 'US-MERC-{0}-{1}',
    r'(\d{4})\s+Walking\s+Liberty\s+Half': 'US-WLHD-{0}-P',
    r'(\d{4})\s+Wheat\s+Penn[yi]': 'US-LWCT-{0}-P',
    r'Indian\s+Head\s+Penn[yi]\s+(\d{4})': 'US-INCH-{0}-P',
}

def map_listing_to_taxonomy(listing_title):
    import re
    
    for pattern, template in LISTING_PATTERNS.items():
        match = re.search(pattern, listing_title, re.I)
        if match:
            return template.format(*match.groups())
    
    return None

# Examples
print(map_listing_to_taxonomy("1921-D Morgan Dollar"))  # US-MORG-1921-D
print(map_listing_to_taxonomy("1916 Mercury Dime S"))   # US-MERC-1916-S
```

## Performance Optimization

### Caching Strategy

```python
import redis
import json
from functools import lru_cache

# Redis caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_coin_data(coin_id):
    # Check cache
    cached = redis_client.get(f'coin:{coin_id}')
    if cached:
        return json.loads(cached)
    
    # Fetch from taxonomy
    data = fetch_from_taxonomy(coin_id)
    
    # Cache for 24 hours
    redis_client.setex(
        f'coin:{coin_id}',
        86400,
        json.dumps(data)
    )
    
    return data

# Memory caching for frequently accessed data
@lru_cache(maxsize=1000)
def get_series_coins(series_name):
    # This will cache in memory
    return fetch_series_from_taxonomy(series_name)
```

### Bulk Operations

```python
def bulk_import_to_database(taxonomy_data):
    """Efficient bulk import using transactions"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('BEGIN TRANSACTION')
        
        # Prepare bulk insert
        cursor.executemany("""
            INSERT OR REPLACE INTO coins 
            (coin_id, country, year, mint, denomination, series, rarity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                issue['issueId'],
                issue['country'],
                issue['year'],
                issue['mint'],
                issue['denomination'],
                issue['seriesName'],
                issue.get('rarity', 'common')
            )
            for issue in taxonomy_data['issues']
        ])
        
        cursor.execute('COMMIT')
        print(f"Imported {len(taxonomy_data['issues'])} coins")
        
    except Exception as e:
        cursor.execute('ROLLBACK')
        raise e
    finally:
        conn.close()
```

## Error Handling

```python
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class TaxonomyClient:
    def __init__(self):
        self.session = requests.Session()
        
        # Configure retries
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def fetch_with_fallback(self, primary_url, fallback_url):
        """Try primary URL, fall back to secondary if needed"""
        try:
            response = self.session.get(primary_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Primary failed: {e}, trying fallback")
            
            try:
                response = self.session.get(fallback_url, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as fallback_error:
                print(f"Both sources failed: {fallback_error}")
                raise
    
    def get_taxonomy(self):
        return self.fetch_with_fallback(
            'https://cdn.jsdelivr.net/gh/mattsilv/coin-taxonomy@main/data/universal/us_issues.json',
            'https://raw.githubusercontent.com/mattsilv/coin-taxonomy/main/data/universal/us_issues.json'
        )
```

## Support

- **GitHub Issues**: https://github.com/mattsilv/coin-taxonomy/issues
- **Latest Updates**: Watch the repository for releases
- **Breaking Changes**: Check `taxonomy_version` in taxonomy_summary.json
- **Data Corrections**: Submit pull requests with validation

## License

MIT License - Free for commercial and non-commercial use.