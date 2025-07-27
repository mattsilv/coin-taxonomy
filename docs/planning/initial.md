# Coin Taxonomy Project

A comprehensive, open-source taxonomy system for coins, starting with United States coins.

## Project Structure

```
coin-taxonomy/
├── README.md                    # This file
├── LICENSE                      # MIT or similar
├── .gitignore                   # Excludes database and local files
├── CONTRIBUTING.md              # Contribution guidelines
├── data/
│   ├── us/                      # United States coins
│   │   ├── schema/
│   │   │   └── coin.schema.json
│   │   ├── coins/
│   │   │   ├── cents.json       # ALL cent series in one file
│   │   │   ├── nickels.json     # ALL nickel series in one file
│   │   │   ├── dimes.json       # ALL dime series in one file
│   │   │   ├── quarters.json    # ALL quarter series in one file
│   │   │   ├── half_dollars.json
│   │   │   └── dollars.json
│   │   ├── references/
│   │   │   ├── mints.json       # US mint locations and years
│   │   │   ├── grades.json      # Grade definitions
│   │   │   └── compositions.json # Common alloy definitions
│   │   └── README.md            # US-specific documentation
│   ├── ca/                      # Future: Canadian coins
│   ├── uk/                      # Future: British coins
│   └── mx/                      # Future: Mexican coins
├── scripts/
│   ├── validate.py              # Validate JSON against schemas
│   ├── build_db.py              # Generate SQLite from JSON
│   ├── import_listing.py        # Match eBay/Etsy listings
│   └── calculate_melt.py        # Calculate metal values
├── database/                    # Generated, not committed
│   └── coins.db                 # SQLite database
└── examples/
    └── sample_collection.csv    # Example personal collection
```

## Key Design Decisions

### File Organization
- **One file per denomination type** (cents.json contains ALL cent series: Indian Head, Lincoln Wheat, Lincoln Memorial, etc.)
- **Country folders** for future expansion (us/, ca/, uk/, etc.)
- **No database in git** - SQLite is generated locally from JSON source files

### Why This Structure?
- Easier to find data (look in dimes.json for ANY dime)
- Simpler to maintain (fewer files to validate)
- Natural for expansion (add new countries as needed)
- Clear separation between countries

## .gitignore Configuration

```gitignore
# Database files
database/
*.db
*.sqlite
*.sqlite3

# Local configuration
config.local.json
.env

# OS files
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
venv/
env/

# Editor
.vscode/
.idea/

# Build artifacts
dist/
build/
```

## Data Schema

### Example: dimes.json Structure

```json
{
  "country": "US",
  "denomination": "Dimes",
  "face_value": 0.10,
  "series": [
    {
      "series_name": "Mercury Dime",
      "official_name": "Winged Liberty Head Dime",
      "years": {
        "start": 1916,
        "end": 1945
      },
      "designers": {
        "obverse": "Adolph A. Weinman",
        "reverse": "Adolph A. Weinman"
      },
      "specifications": {
        "diameter_mm": 17.91,
        "thickness_mm": 1.35,
        "edge": "reeded",
        "edge_reeds": 118
      },
      "composition_periods": [
        {
          "date_range": {
            "start": 1916,
            "end": 1945
          },
          "alloy": {
            "silver": 0.900,
            "copper": 0.100
          },
          "weight": {
            "grams": 2.500,
            "troy_oz": 0.08038
          }
        }
      ],
      "mintages": {
        "1916": {
          "P": {
            "mintage": 22180080,
            "proof_mintage": null,
            "notes": null
          },
          "D": {
            "mintage": 264000,
            "proof_mintage": null,
            "notes": "Key date - lowest mintage"
          },
          "S": {
            "mintage": 10450000,
            "proof_mintage": null,
            "notes": null
          }
        }
      }
    },
    {
      "series_name": "Roosevelt Dime",
      "official_name": "Roosevelt Dime",
      "years": {
        "start": 1946,
        "end": "present"
      },
      "composition_periods": [
        {
          "date_range": {
            "start": 1946,
            "end": 1964
          },
          "alloy": {
            "silver": 0.900,
            "copper": 0.100
          },
          "weight": {
            "grams": 2.500
          }
        },
        {
          "date_range": {
            "start": 1965,
            "end": "present"
          },
          "alloy": {
            "copper_core": 0.917,
            "cupronickel_cladding": 0.083
          },
          "weight": {
            "grams": 2.268
          }
        }
      ],
      "mintages": {}
    }
  ]
}
```

### Mintage Structure (Simplified)

```json
{
  "1916": {
    "P": {
      "mintage": 22180080,
      "proof_mintage": null,
      "varieties": {
        "DDO": {
          "description": "Doubled Die Obverse",
          "estimated_mintage": null
        }
      },
      "notes": null
    }
  }
}
```

## Grade Definitions (Common Terms)

### Word Grades Reference (grades.json)

```json
{
  "grades": {
    "Poor": {
      "abbreviation": "P",
      "description": "Barely identifiable, most details worn smooth",
      "numeric_equivalent": "1"
    },
    "Fair": {
      "abbreviation": "FR",
      "description": "Some details visible but heavily worn",
      "numeric_equivalent": "2"
    },
    "Good": {
      "abbreviation": "G",
      "description": "Major design visible but faint, rims worn",
      "numeric_equivalent": "4-6"
    },
    "Very Good": {
      "abbreviation": "VG",
      "description": "Design clear but flat, some detail visible",
      "numeric_equivalent": "8-10"
    },
    "Fine": {
      "abbreviation": "F",
      "description": "Moderate even wear, all major details visible",
      "numeric_equivalent": "12-15"
    },
    "Very Fine": {
      "abbreviation": "VF",
      "description": "Light even wear on high points, sharp details",
      "numeric_equivalent": "20-35"
    },
    "Extremely Fine": {
      "abbreviation": "XF/EF",
      "description": "Slight wear on highest points only",
      "numeric_equivalent": "40-45"
    },
    "About Uncirculated": {
      "abbreviation": "AU",
      "description": "Traces of wear on highest points",
      "numeric_equivalent": "50-58"
    },
    "Uncirculated": {
      "abbreviation": "UNC/MS",
      "description": "No wear, but may have bag marks",
      "numeric_equivalent": "60-70"
    },
    "Proof": {
      "abbreviation": "PR/PF",
      "description": "Special striking for collectors",
      "numeric_equivalent": "60-70"
    }
  }
}
```

## Implementation Scripts

### Milestone 1: Data Validation (validate.py)

```python
#!/usr/bin/env python3
"""
Validates all JSON files against their schemas.
Works for any country's data files.
"""

import json
import glob
from jsonschema import validate, ValidationError
import os
import sys

def validate_country_data(country_code):
    """Validate all data files for a specific country"""
    schema_path = f'data/{country_code}/schema/coin.schema.json'
    
    if not os.path.exists(schema_path):
        print(f"No schema found for country: {country_code}")
        return 0
    
    with open(schema_path) as f:
        schema = json.load(f)
    
    errors = 0
    coin_files = glob.glob(f'data/{country_code}/coins/*.json')
    
    for filepath in coin_files:
        try:
            with open(filepath) as f:
                data = json.load(f)
            validate(data, schema)
            print(f"✓ {filepath}")
        except json.JSONDecodeError as e:
            print(f"✗ {filepath}: Invalid JSON - {e}")
            errors += 1
        except ValidationError as e:
            print(f"✗ {filepath}: Validation failed - {e.message}")
            errors += 1
    
    return errors

def main():
    # Find all country directories
    countries = [d for d in os.listdir('data') 
                 if os.path.isdir(f'data/{d}') and len(d) == 2]
    
    total_errors = 0
    for country in countries:
        print(f"\nValidating {country.upper()} data...")
        total_errors += validate_country_data(country)
    
    if total_errors:
        print(f"\n{total_errors} validation error(s) found")
        sys.exit(1)
    else:
        print("\n✓ All files valid")

if __name__ == "__main__":
    main()
```

### Milestone 2: Database Builder (build_db.py)

```python
#!/usr/bin/env python3
"""
Builds SQLite database from JSON source files.
Handles multiple countries seamlessly.
"""

import json
import sqlite3
import glob
import os

def create_tables(conn):
    conn.executescript('''
        -- Main coin reference table
        CREATE TABLE IF NOT EXISTS coins (
            id TEXT PRIMARY KEY,
            country TEXT NOT NULL,
            denomination TEXT NOT NULL,
            series TEXT NOT NULL,
            year INTEGER NOT NULL,
            mint TEXT NOT NULL,
            
            -- Composition and specifications
            composition JSON,
            weight_grams REAL,
            diameter_mm REAL,
            
            -- Mintage data
            mintage INTEGER,
            proof_mintage INTEGER,
            
            -- Metadata
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Full-text search
        CREATE VIRTUAL TABLE IF NOT EXISTS coin_search 
        USING fts5(
            canonical_name, 
            search_terms,
            content=coins
        );
        
        -- Grade reference table
        CREATE TABLE IF NOT EXISTS grades (
            grade_word TEXT PRIMARY KEY,
            abbreviation TEXT,
            description TEXT,
            numeric_range TEXT,
            country TEXT
        );
        
        CREATE INDEX idx_coins_country ON coins(country);
        CREATE INDEX idx_coins_year_mint ON coins(year, mint);
        CREATE INDEX idx_coins_series ON coins(series);
    ''')

def import_country_data(conn, country_code):
    """Import all coin data for a specific country"""
    coin_files = glob.glob(f'data/{country_code}/coins/*.json')
    
    for filepath in coin_files:
        with open(filepath) as f:
            data = json.load(f)
        
        # Import each series in the file
        for series_data in data.get('series', []):
            import_series(conn, country_code, data['denomination'], series_data)
    
    # Import grade definitions if they exist
    grades_file = f'data/{country_code}/references/grades.json'
    if os.path.exists(grades_file):
        with open(grades_file) as f:
            grades_data = json.load(f)
        
        for grade, info in grades_data.get('grades', {}).items():
            conn.execute('''
                INSERT OR REPLACE INTO grades 
                (grade_word, abbreviation, description, numeric_range, country)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                grade,
                info.get('abbreviation'),
                info.get('description'),
                info.get('numeric_equivalent'),
                country_code.upper()
            ))

def import_series(conn, country, denomination, series_data):
    """Import a single series worth of coins"""
    series_name = series_data['series_name']
    
    # Get composition for different periods
    comp_periods = series_data.get('composition_periods', [])
    
    # Process mintages
    for year_str, mint_data in series_data.get('mintages', {}).items():
        year = int(year_str)
        
        # Find applicable composition
        composition = None
        weight = None
        for period in comp_periods:
            start = period['date_range']['start']
            end = period['date_range']['end']
            if end == 'present':
                end = 9999
            if start <= year <= end:
                composition = period['alloy']
                weight = period['weight'].get('grams')
                break
        
        # Insert coin for each mint
        for mint, details in mint_data.items():
            if details is None:
                continue
                
            coin_id = f"{country}-{year}-{mint}-{series_name.replace(' ', '_')}"
            
            conn.execute('''
                INSERT OR REPLACE INTO coins 
                (id, country, denomination, series, year, mint, 
                 composition, weight_grams, diameter_mm, mintage, 
                 proof_mintage, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coin_id,
                country.upper(),
                denomination,
                series_name,
                year,
                mint,
                json.dumps(composition) if composition else None,
                weight,
                series_data.get('specifications', {}).get('diameter_mm'),
                details.get('mintage'),
                details.get('proof_mintage'),
                details.get('notes')
            ))

def build_search_index(conn):
    """Build search index for all countries"""
    conn.execute('''
        INSERT INTO coin_search (canonical_name, search_terms)
        SELECT 
            printf('%s %d-%s %s', country, year, mint, series) as canonical_name,
            printf('%s %d %s %s %s', country, year, mint, series, denomination) as search_terms
        FROM coins
    ''')

def main():
    print("Building database...")
    
    # Ensure database directory exists
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect('database/coins.db')
    create_tables(conn)
    
    # Import data for each country
    countries = [d for d in os.listdir('data') 
                 if os.path.isdir(f'data/{d}') and len(d) == 2]
    
    for country in countries:
        print(f"Importing {country.upper()} data...")
        import_country_data(conn, country)
    
    print("Building search index...")
    build_search_index(conn)
    
    conn.commit()
    
    # Print statistics
    stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT country) as countries,
            COUNT(DISTINCT series) as series,
            COUNT(*) as total_coins,
            MIN(year) as earliest,
            MAX(year) as latest
        FROM coins
    ''').fetchone()
    
    print(f"\nDatabase built successfully!")
    print(f"Countries: {stats[0]}")
    print(f"Series: {stats[1]}")
    print(f"Total coins: {stats[2]}")
    print(f"Year range: {stats[3]}-{stats[4]}")
    
    conn.close()

if __name__ == "__main__":
    main()
```

### Milestone 3: Listing Matcher (import_listing.py)

```python
#!/usr/bin/env python3
"""
Match marketplace listings to canonical coin taxonomy.
Automatically detects country when possible.
"""

import re
import sqlite3
import json

class ListingMatcher:
    def __init__(self, db_path='database/coins.db'):
        self.conn = sqlite3.connect(db_path)
        self.load_grade_mappings()
    
    def load_grade_mappings(self):
        """Load grade word mappings from database"""
        self.grade_map = {}
        cursor = self.conn.execute('SELECT grade_word, abbreviation FROM grades')
        for row in cursor:
            self.grade_map[row[0].lower()] = row[0]
            if row[1]:
                self.grade_map[row[1].lower()] = row[0]
        
        # Add common variations
        self.grade_map.update({
            'unc': 'Uncirculated',
            'bu': 'Uncirculated',
            'brilliant uncirculated': 'Uncirculated',
            'xf': 'Extremely Fine',
            'ef': 'Extremely Fine',
            'vf': 'Very Fine',
            'f': 'Fine',
            'vg': 'Very Good',
            'g': 'Good',
            'ag': 'About Good',
            'au': 'About Uncirculated'
        })
    
    def detect_country(self, text):
        """Try to detect country from listing text"""
        # Country indicators
        indicators = {
            'US': ['united states', 'usa', 'us ', 'american', 'liberty', 'cent', 
                   'nickel', 'dime', 'quarter', 'half dollar', 'dollar'],
            'CA': ['canada', 'canadian', 'maple leaf', 'loonie', 'toonie'],
            'UK': ['british', 'britain', 'england', 'pound', 'pence', 'shilling'],
            'MX': ['mexico', 'mexican', 'peso', 'aztec']
        }
        
        text_lower = text.lower()
        for country, keywords in indicators.items():
            if any(kw in text_lower for kw in keywords):
                return country
        
        # Default to US if unclear
        return 'US'
    
    def extract_year(self, text):
        """Extract year from listing text"""
        years = re.findall(r'\b(17|18|19|20)\d{2}\b', text)
        if years:
            return int(years[0])
        return None
    
    def extract_mint_mark(self, text):
        """Extract mint mark from listing text"""
        # Patterns for different countries
        us_mints = r'[PDSOCC]'
        ca_mints = r'[HWC]'  # Historical Canadian mints
        
        patterns = [
            r'(\d{4})\s*[-/]?\s*([' + us_mints + ca_mints + ']+)\b',
            r'\b([' + us_mints + ca_mints + '])\s+mint\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(match.lastindex).upper()
        
        return 'P'  # Default to Philadelphia for US
    
    def extract_grade(self, text):
        """Extract grade from listing text"""
        text_lower = text.lower()
        
        # Check each grade mapping
        for key, grade in sorted(self.grade_map.items(), 
                                key=lambda x: len(x[0]), reverse=True):
            if key in text_lower:
                return grade
        
        return None
    
    def match_listing(self, listing_text):
        """
        Match a listing to canonical coin data.
        Returns dict with matched coin info and confidence score.
        """
        result = {
            'input': listing_text,
            'country': self.detect_country(listing_text),
            'year': self.extract_year(listing_text),
            'mint': self.extract_mint_mark(listing_text),
            'grade': self.extract_grade(listing_text),
            'matches': [],
            'confidence': 0
        }
        
        if not result['year']:
            return result
        
        # Search database
        query = '''
            SELECT DISTINCT country, denomination, series, year, mint, mintage
            FROM coins
            WHERE year = ? AND country = ?
        '''
        params = [result['year'], result['country']]
        
        if result['mint']:
            query += ' AND mint = ?'
            params.append(result['mint'])
        
        matches = self.conn.execute(query, params).fetchall()
        
        # Try to identify series from listing text
        text_lower = listing_text.lower()
        
        # Common series keywords
        series_keywords = {
            'mercury': 'Mercury Dime',
            'winged liberty': 'Mercury Dime',
            'roosevelt': 'Roosevelt Dime',
            'barber': ['Barber Dime', 'Barber Quarter', 'Barber Half Dollar'],
            'indian': 'Indian Head Cent',
            'wheat': 'Lincoln Cent',
            'buffalo': 'Buffalo Nickel',
            'jefferson': 'Jefferson Nickel',
            'washington': 'Washington Quarter',
            'standing liberty': 'Standing Liberty Quarter',
            'walking liberty': 'Walking Liberty Half Dollar',
            'franklin': 'Franklin Half Dollar',
            'kennedy': 'Kennedy Half Dollar',
            'morgan': 'Morgan Dollar',
            'peace': 'Peace Dollar'
        }
        
        for keyword, series_match in series_keywords.items():
            if keyword in text_lower:
                # Filter matches to this series
                if isinstance(series_match, list):
                    filtered = [m for m in matches if m[2] in series_match]
                else:
                    filtered = [m for m in matches if m[2] == series_match]
                
                if filtered:
                    result['matches'] = filtered
                    result['confidence'] = 0.9
                    break
        
        if not result['matches']:
            result['matches'] = matches
            result['confidence'] = 0.5 if matches else 0.0
        
        return result

def main():
    matcher = ListingMatcher()
    
    # Test examples
    test_listings = [
        "1916-D Mercury Dime Good condition",
        "1943 Steel Wheat Penny",
        "Canada 1967 Centennial Quarter",
        "Morgan Dollar 1921 S Mint Mark AU",
        "Indian Head Cent 1906 Fine",
        "Buffalo Nickel 1937D VF",
    ]
    
    for listing in test_listings:
        result = matcher.match_listing(listing)
        print(f"\nListing: {listing}")
        print(f"Country: {result['country']}")
        print(f"Parsed: Year={result['year']}, Mint={result['mint']}, Grade={result['grade']}")
        print(f"Confidence: {result['confidence']}")
        if result['matches']:
            for match in result['matches']:
                print(f"  - {match[0]} {match[1]} {match[2]}")

if __name__ == "__main__":
    main()
```

### Milestone 4: Metal Value Calculator (calculate_melt.py)

```python
#!/usr/bin/env python3
"""
Calculate melt values based on current metal prices.
Works for any country's coins with metal content.
"""

import json
import sqlite3
from datetime import datetime

class MeltCalculator:
    def __init__(self, db_path='database/coins.db'):
        self.conn = sqlite3.connect(db_path)
        # Default spot prices per troy ounce
        self.spot_prices = {
            'gold': 2000.00,
            'silver': 25.00,
            'platinum': 900.00,
            'palladium': 1000.00,
            'copper': 0.0027,  # per gram
            'nickel': 0.0080,  # per gram
            'zinc': 0.0012,    # per gram
            'steel': 0.0001    # per gram
        }
        self.grams_per_troy_oz = 31.1035
    
    def update_spot_prices(self, prices):
        """Update metal spot prices"""
        self.spot_prices.update(prices)
    
    def calculate_melt_value(self, country, year, mint, series):
        """Calculate melt value for a specific coin"""
        coin = self.conn.execute('''
            SELECT composition, weight_grams
            FROM coins
            WHERE country = ? AND year = ? AND mint = ? AND series = ?
        ''', (country, year, mint, series)).fetchone()
        
        if not coin or not coin[0]:
            return None
        
        composition = json.loads(coin[0])
        weight_grams = coin[1]
        
        total_value = 0
        metal_breakdown = {}
        
        for component, percentage in composition.items():
            # Handle clad compositions
            if component in ['copper_core', 'cupronickel_cladding']:
                # Simplified - treat as copper for now
                metal = 'copper'
                percentage = float(percentage)
            else:
                metal = component
                percentage = float(percentage)
            
            metal_weight_grams = weight_grams * percentage
            
            # Calculate value based on metal type
            if metal in ['gold', 'silver', 'platinum', 'palladium']:
                # Precious metals - price per troy oz
                metal_weight_troy_oz = metal_weight_grams / self.grams_per_troy_oz
                metal_value = metal_weight_troy_oz * self.spot_prices.get(metal, 0)
            else:
                # Base metals - price per gram
                metal_value = metal_weight_grams * self.spot_prices.get(metal, 0)
            
            total_value += metal_value
            
            metal_breakdown[metal] = {
                'percentage': percentage,
                'weight_grams': metal_weight_grams,
                'value': metal_value
            }
        
        return {
            'total_melt_value': round(total_value, 3),
            'metal_breakdown': metal_breakdown,
            'spot_prices_used': self.spot_prices,
            'calculation_date': datetime.now().isoformat()
        }

def main():
    calc = MeltCalculator()
    
    # Example calculations
    examples = [
        ('US', 1964, 'D', 'Washington Quarter'),
        ('US', 1943, 'P', 'Lincoln Cent'),  # Steel cent
        ('US', 2020, 'P', 'Jefferson Nickel')  # Modern composition
    ]
    
    for country, year, mint, series in examples:
        result = calc.calculate_melt_value(country, year, mint, series)
        if result:
            print(f"\n{country} {year}-{mint} {series}")
            print(f"Melt value: ${result['total_melt_value']:.3f}")
            for metal, data in result['metal_breakdown'].items():
                print(f"  {metal}: {data['weight_grams']:.3f}g = ${data['value']:.3f}")

if __name__ == "__main__":
    main()
```

## Contributing Guidelines

### Adding New Data

1. **Country Code Convention:**
   - Use 2-letter ISO country codes (US, CA, UK, MX, etc.)
   - Create new country folder under data/ when expanding

2. **File Organization:**
   - Keep all denominations of same type in one file
   - Example: cents.json contains Indian Head, Lincoln Wheat, Lincoln Memorial, etc.

3. **Data Sources:**
   - Always cite sources when available
   - Official mint records preferred
   - Mark unverified data as null with notes

### Grade Standards

We use common collecting terms (Good, Fine, Very Fine, etc.) as primary grade indicators. The numeric equivalents are provided for reference but are not required for basic use.

### Commit Message Format

```
Add: [Country] [Denomination] [Years] [Data Type]
Update: [Country] [Series] [Specific Change]
Fix: [Issue Description]

Examples:
Add: US Dimes 1916-1920 mintages
Update: US Indian Head Cent 1864 composition
Fix: CA quarters schema validation
```

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/coin-taxonomy.git
cd coin-taxonomy

# Create local database directory
mkdir database

# Validate US data files
python scripts/validate.py

# Build database (includes all countries)
python scripts/build_db.py

# Test listing matcher
echo "1916-D Mercury Dime Fine" | python scripts/import_listing.py

# Calculate melt value
python scripts/calculate_melt.py --country US --year 1964 --series "Washington Quarter"
```

## Future Expansion

When adding new countries:

1. Create country folder: `data/xx/` (where xx is country code)
2. Copy schema structure from `data/us/schema/`
3. Adapt grade definitions to local terminology
4. Follow same file structure (coins/, references/)
5. Scripts automatically detect and process new countries

## License

This project is released under the MIT License. See LICENSE file for details.