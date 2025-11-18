# eBay Listing → Taxonomy ID Linking Primer

**Audience:** Backend engineer integrating eBay listings with coin taxonomy
**Goal:** Map eBay coin/bullion listings to standardized taxonomy IDs
**Date:** 2025-11-18

---

## Taxonomy ID Format

All coins follow a strict 4-part format:

```
COUNTRY-TYPE-YEAR-MINT
```

### Components

1. **COUNTRY** (2-3 letters)
   - `US` = United States
   - `CA` = Canada
   - `MX` = Mexico

2. **TYPE** (4 alphanumeric characters)
   - Letters and/or numbers (e.g., `IHC`, `MLSO`, `EN01`)
   - Identifies the coin series/design
   - **Recent update:** Now supports alphanumeric (was letters-only)

3. **YEAR** (4 digits OR `XXXX`)
   - Specific year: `1877`, `1909`, `2024`
   - Random year: `XXXX` (for bullion sold "dealer's choice")

4. **MINT** (1-2 letters OR `X`)
   - US: `P` (Philadelphia), `D` (Denver), `S` (San Francisco), `W` (West Point)
   - Canada: `MO` (Montreal), `RM` (Royal Mint)
   - Mexico: `MO` (Mexico City)
   - Unspecified: `X` (common for bullion)

### ID Examples

```
US-IHC-1877-P    = US Indian Head Cent, 1877, Philadelphia
US-LWC-1909-S    = US Lincoln Wheat Cent, 1909, San Francisco
US-AGEO-XXXX-X   = American Gold Eagle 1oz, random year, unspecified mint
US-EN42-XXXX-X   = Engelhard Silver Bar variety #42, random year
MX-MLSO-1982-MO  = Mexican Libertad Silver 1oz, 1982, Mexico City
CA-FIVE-1858-RM  = Canadian 5 Cents, 1858, Royal Mint
```

---

## Linking Strategy

### Step 1: Extract Key Data from eBay Listing

Parse the listing title/description for:

```python
{
  "country": "US",           # From seller location or coin origin
  "series": "Lincoln Cent",  # Coin type/series name
  "year": "1909",            # Minting year
  "mint_mark": "S",          # Mint facility
  "variety": "VDB",          # Optional variety detail
  "is_bullion": false        # True if sold by weight, not numismatic value
}
```

### Step 2: Map to TYPE Codes

Common US coins:

| eBay Term | TYPE Code | Full Name |
|-----------|-----------|-----------|
| Indian Head Cent | `IHC` | Indian Head Cent |
| Lincoln Wheat Cent | `LWC` | Lincoln Wheat Cent |
| Lincoln Memorial Cent | `LMC` | Lincoln Memorial Cent |
| Buffalo Nickel | `BUFN` | Buffalo Nickel |
| Mercury Dime | `WHD` | Winged Liberty Head Dime |
| Standing Liberty Quarter | `SLQ` | Standing Liberty Quarter |
| Washington Quarter | `WASQ` | Washington Quarter |
| Walking Liberty Half | `WLH` | Walking Liberty Half Dollar |
| Morgan Dollar | `MORG` | Morgan Dollar |
| Peace Dollar | `PEAC` | Peace Dollar |

Bullion (random year):

| eBay Term | TYPE Code | Pattern |
|-----------|-----------|---------|
| American Silver Eagle | `ASEA` | `US-ASEA-XXXX-X` |
| American Gold Eagle 1oz | `AGEO` | `US-AGEO-XXXX-X` |
| American Gold Eagle 1/2oz | `AGES` | `US-AGES-XXXX-X` |
| American Gold Eagle 1/4oz | `AGEF` | `US-AGEF-XXXX-X` |
| American Gold Eagle 1/10oz | `AGET` | `US-AGET-XXXX-X` |
| Engelhard Silver Bar (varieties 1-72) | `EN01`-`EN72` | `US-EN42-XXXX-X` |
| Mexican Libertad Silver 1oz | `MLSO` | `MX-MLSO-YYYY-MO` |

### Step 3: Handle Special Cases

**Bullion vs Numismatic:**
```python
if is_bullion and "random year" in listing_title:
    year = "XXXX"
    mint = "X"
else:
    year = extract_year(listing)  # e.g., "1909"
    mint = extract_mint(listing)  # e.g., "S"
```

**Variety Detection:**
```python
# Varieties go in separate field, NOT in the ID
taxonomy_id = f"US-LWC-1909-S"  # Base ID
variety = "VDB"                  # Store separately in varieties array
```

**Missing Mint Mark:**
```python
# If mint mark not specified in listing, default logic:
if year >= 1980:
    mint = "P"  # Modern coins default to Philadelphia
else:
    mint = "UNKNOWN"  # Flag for manual review
```

---

## Data Access

### Database

```sql
-- Find coin by ID
SELECT * FROM coins WHERE coin_id = 'US-IHC-1877-P';

-- Find by year and series
SELECT coin_id, series, year, mint
FROM coins
WHERE year = '1909'
  AND series LIKE '%Lincoln%';

-- Check if ID exists
SELECT EXISTS(SELECT 1 FROM coins WHERE coin_id = ?) as exists;
```

### JSON Files (Read-Only)

```bash
# Location
data/us/coins/*.json           # US coins by denomination
data/ca/coins/*.json           # Canadian coins
data/universal/us_issues.json  # All US coins (universal format)

# Structure
{
  "country": "US",
  "denomination": "Cents",
  "series": [
    {
      "series_name": "Lincoln Wheat Cent",
      "coins": [
        {
          "coin_id": "US-LWC-1909-S",
          "year": "1909",
          "mint": "S",
          "varieties": []
        }
      ]
    }
  ]
}
```

### API Endpoints (if applicable)

```bash
# Get coin by ID
GET /api/coins/US-IHC-1877-P

# Search coins
GET /api/coins/search?year=1909&series=Lincoln

# Validate ID format
GET /api/coins/validate?id=US-LWC-1909-S
```

---

## Matching Algorithm (Pseudocode)

```python
def match_ebay_listing_to_taxonomy(listing):
    """
    Match eBay listing to taxonomy ID

    Returns: {
        "taxonomy_id": "US-LWC-1909-S",
        "confidence": 0.95,
        "variety": "VDB",
        "needs_review": False
    }
    """

    # Extract structured data
    country = extract_country(listing)
    series = extract_series(listing.title)
    year = extract_year(listing.title)
    mint = extract_mint_mark(listing.title)

    # Determine if bullion
    is_bullion = (
        "random year" in listing.title.lower() or
        "our choice" in listing.title.lower() or
        listing.category in ["Bullion", "Investment"]
    )

    # Map series to TYPE code
    type_code = SERIES_TO_TYPE_MAP.get(series)
    if not type_code:
        return {"error": "Unknown series", "needs_review": True}

    # Handle bullion random year
    if is_bullion and year_not_specified(listing):
        year = "XXXX"
        mint = "X"

    # Construct ID
    taxonomy_id = f"{country}-{type_code}-{year}-{mint}"

    # Validate format
    if not validate_id_format(taxonomy_id):
        return {"error": "Invalid ID format", "needs_review": True}

    # Check if exists in database
    if not id_exists(taxonomy_id):
        return {
            "taxonomy_id": taxonomy_id,
            "confidence": 0.5,
            "needs_review": True,
            "reason": "ID not found in taxonomy"
        }

    # Extract variety info (separate from ID)
    variety = extract_variety(listing.title)

    return {
        "taxonomy_id": taxonomy_id,
        "confidence": calculate_confidence(listing, taxonomy_id),
        "variety": variety,
        "needs_review": False
    }
```

---

## ID Validation Regex

```python
import re

# Standard format validation
TAXONOMY_ID_PATTERN = r'^[A-Z]{2,3}-[A-Z0-9]{4}-(\d{4}|XXXX)-[A-Z]{1,2}$'

def validate_taxonomy_id(coin_id):
    """
    Validate taxonomy ID format

    Examples:
        US-IHC-1877-P     ✓
        US-EN42-XXXX-X    ✓
        MX-MLSO-1982-MO   ✓
        US-LWC-1909       ✗ (missing mint)
        us-lwc-1909-s     ✗ (lowercase)
        US-LWC-09-S       ✗ (2-digit year)
    """
    return bool(re.match(TAXONOMY_ID_PATTERN, coin_id))
```

---

## Edge Cases & Gotchas

### 1. Engelhard Bullion (New Format)
**Old format (before 2025-11-18):**
```
US-ENGL-XXXX-ENGELHARD-EARLIEST_1OZ_PRODUCTION_BAR-1  ❌ DEPRECATED
```

**New format (current):**
```
US-EN01-XXXX-X  ✓ Variety 1
US-EN02-XXXX-X  ✓ Variety 2
...
US-EN72-XXXX-X  ✓ Variety 72
```

If you encounter old format in legacy data, map to new:
```python
old_id = "US-ENGL-XXXX-ENGELHARD-EARLIEST_1OZ_PRODUCTION_BAR-1"
# Extract variety number from end
variety_num = extract_number(old_id)  # "1"
new_id = f"US-EN{variety_num:02d}-XXXX-X"  # "US-EN01-XXXX-X"
```

### 2. Proof vs Business Strike
**Same ID, different metadata:**
```python
# Both have same taxonomy ID
taxonomy_id = "US-IHC-1877-P"

# Differentiate in metadata
{
  "taxonomy_id": "US-IHC-1877-P",
  "strike_type": "proof",      # or "business"
  "price_estimate": 5000       # Proof worth much more
}
```

### 3. Commemorative Coins
**Title:** "1936 Albany Half Dollar Commemorative"
```python
taxonomy_id = "US-ALBY-1936-P"  # Not generic "Half Dollar"
series = "Albany, New York, Charter"
```

### 4. Year Ranges in Listings
**Title:** "2015-2024 American Silver Eagle Complete Set"
```python
# Create multiple taxonomy IDs
ids = [f"US-ASEA-{year}-X" for year in range(2015, 2025)]
# OR flag as "set" that requires manual breakdown
```

### 5. Graded Coins
**Title:** "1909-S VDB Lincoln Cent PCGS MS65RD"
```python
taxonomy_id = "US-LWC-1909-S"  # Same ID regardless of grade
variety = "VDB"
grade = {
  "service": "PCGS",
  "grade": "MS65",
  "designation": "RD"
}
```

---

## Testing Checklist

Before deploying eBay integration:

- [ ] Match 100% of American Silver Eagles (should be `US-ASEA-XXXX-X`)
- [ ] Correctly parse mint marks (P, D, S, W)
- [ ] Handle "random year" bullion with `XXXX`
- [ ] Don't embed varieties in ID (use separate field)
- [ ] Validate all IDs match regex pattern
- [ ] Check IDs exist in database before storing link
- [ ] Handle graded coins (grade ≠ taxonomy ID)
- [ ] Flag unknown series for manual review
- [ ] Test with Engelhard varieties (EN01-EN72)
- [ ] Verify Canadian/Mexican coins if applicable

---

## Resources

**Schema Documentation:**
- Database schema: `database/coins.db` (SQLite)
- JSON schema: `data/us/schema/coin.schema.json`
- Issue tracking: GitHub Issues

**Data Files:**
- US coins: `data/us/coins/*.json`
- Universal format: `data/universal/us_issues.json`
- Grade standards: `data/universal/grade_standards.json`

**Contact:**
- Questions about taxonomy: Open GitHub issue
- Schema change requests: Create PR with rationale
- New coin types: Add to migration scripts in `scripts/`

---

## Quick Reference: Common eBay Terms → TYPE Codes

```
Indian Head Penny        → IHC
Lincoln Wheat Penny      → LWC
Lincoln Memorial Penny   → LMC
Buffalo Nickel          → BUFN
Jefferson Nickel        → JEFF
Mercury Dime            → WHD
Roosevelt Dime          → ROOS
Standing Liberty Quarter → SLQ
Washington Quarter      → WASQ
Walking Liberty Half    → WLH
Franklin Half           → FRAN
Kennedy Half            → KENN
Morgan Dollar           → MORG
Peace Dollar            → PEAC
Eisenhower Dollar       → IKE
American Silver Eagle   → ASEA
American Gold Eagle     → AGEO/AGES/AGEF/AGET
Engelhard Silver Bar    → EN01-EN72
Mexican Libertad        → MLSO (Silver), MLGO (Gold)
Canadian Maple Leaf     → varies by metal
```

---

**End of Primer**

For questions or clarifications, reference the main taxonomy documentation or open an issue on GitHub.
