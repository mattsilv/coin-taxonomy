# Commemorative Half Dollar Series Codes

**SYNCED FROM**: coin-taxonomy database
**Last Updated**: 2025-01-10
**Total Series**: 48

## Classic Commemoratives (1892-1954)

| Code | Official Name | Years |
|------|---------------|-------|
| WCOL | World's Columbian Exposition | 1892-1893 |
| PPIE | Panama-Pacific International Exposition | 1915 |
| ILCN | Illinois Centennial | 1918 |
| MECN | Maine Centennial | 1920 |
| PILG | Pilgrim Tercentenary | 1920 |
| ALCN | Alabama Centennial | 1921 |
| MOCN | Missouri Centennial | 1921 |
| GRNT | Grant Memorial | 1922 |
| MNDO | Monroe Doctrine Centennial | 1923 |
| HUGE | Huguenot-Walloon Tercentenary | 1924 |
| CADJ | California Diamond Jubilee | 1925 |
| FTVA | Fort Vancouver Centennial | 1925 |
| LEXC | Lexington-Concord Sesquicentennial | 1925 |
| STMN | Stone Mountain Memorial | 1925 |
| ORTR | Oregon Trail Memorial | 1926-1939 |
| SEAI | Sesquicentennial of American Independence | 1926 |
| VTSQ | Vermont Sesquicentennial | 1927 |
| HISQ | Hawaiian Sesquicentennial | 1928 |
| DNBO | Daniel Boone Bicentennial | 1934-1938 |
| MDTC | Maryland Tercentenary | 1934 |
| TXCN | Texas Centennial | 1934-1938 |
| ARCN | Arkansas Centennial | 1935-1939 |
| CAPE | California-Pacific Exposition | 1935-1936 |
| CTTC | Connecticut Tercentenary | 1935 |
| HUNY | Hudson, New York, Sesquicentennial | 1935 |
| OSPT | Old Spanish Trail | 1935 |
| ALNY | Albany, New York, Charter | 1936 |
| ARRB | Arkansas-Robinson | 1936 |
| GTYB | Battle of Gettysburg | 1936 |
| BDPT | Bridgeport, Connecticut, Centennial | 1936 |
| CNMC | Cincinnati Music Center | 1936 |
| CLVC | Cleveland Centennial | 1936 |
| COSC | Columbia, South Carolina, Sesquicentennial | 1936 |
| DETC | Delaware Tercentenary | 1936 |
| ELIL | Elgin, Illinois, Centennial | 1936 |
| LITC | Long Island Tercentenary | 1936 |
| LYVA | Lynchburg, Virginia, Sesquicentennial | 1936 |
| NFVA | Norfolk, Virginia, Bicentennial | 1936 |
| PVRI | Providence, Rhode Island, Tercentenary | 1936 |
| SFBB | San Francisco-Oakland Bay Bridge | 1936 |
| WITC | Wisconsin Territorial Centennial | 1936 |
| YCME | York County, Maine, Tercentenary | 1936 |
| ANTM | Battle of Antietam | 1937 |
| ROAN | Roanoke Island | 1937 |
| NWRC | New Rochelle, New York, 250th Anniversary | 1938 |
| BTWH | Booker T. Washington | 1946-1951 |
| IASC | Iowa Statehood Centennial | 1946 |
| CARW | Carver/Washington | 1951-1954 |

## Variety Suffixes

Some commemoratives have significant design varieties that warrant separate tracking:

| Base Code | Suffix | Full ID Example | Variety Description |
|-----------|--------|-----------------|---------------------|
| GRNT | STAR | US-GRNT-1922-P-STAR | Grant Memorial with Star |
| ALCN | 2X2 | US-ALCN-1921-P-2X2 | Alabama 2X2 variety |
| MOCN | 2S4 | US-MOCN-1921-P-2S4 | Missouri 2 Star 4 variety |

## Usage Examples

### Taxonomy ID Format
```
US-{CODE}-{YEAR}-{MINT}
```

### Query Patterns
```sql
-- All Texas Centennial coins
SELECT * FROM coins WHERE coin_id LIKE 'US-TXCN-%'

-- All 1936 commemoratives
SELECT * FROM coins
WHERE denomination = 'Commemorative Half Dollars'
  AND year = 1936

-- Specific coin
SELECT * FROM coins WHERE coin_id = 'US-WCOL-1892-P'
```

### TypeScript Usage
```typescript
const COMMEMORATIVE_CODES = {
  WCOL: "World's Columbian Exposition",
  PPIE: "Panama-Pacific International Exposition",
  ILCN: "Illinois Centennial",
  // ... etc
} as const;

type CommemorativeCode = keyof typeof COMMEMORATIVE_CODES;
```

## Related Documentation

- [Taxonomy ID Format](../taxonomy-id-format.md) - Complete format specification
- [Source of Truth](../SOURCE_OF_TRUTH.md) - Architecture overview
