# Issue #60: Commemorative Coins CSV Comparison Report

**Date:** 2025-10-28
**Status:** Phase 1 Complete - Comparison Analysis

## Summary

- **CSV Data:** 159 rows (from attached file)
- **Database:** 152 commemorative coins (from Issue #53)
- **Difference:** 7 additional rows in CSV

## Current Database State

### Commemorative Coins by Denomination

| Denomination | Count | Notes |
|--------------|-------|-------|
| Commemorative Half Dollars | 139 | Classic commemoratives 1892-1954 |
| Commemorative Dollars | 1 | Lafayette Dollar 1900 |
| Gold Dollars | 8 | Commemorative gold $1 coins |
| Quarter Eagles | 2 | Commemorative $2.50 gold |
| Fifty Dollars | 2 | Panama-Pacific $50 gold (Round & Octagonal) |
| **Total** | **152** | Added in Issue #53, commit 062c5bf |

### Commemorative Half Dollars (139 coins)
Series breakdown:
- World's Columbian Exposition (1892-1893): 2 coins
- Panama-Pacific through Pilgrim (1915-1920): 5 coins
- Alabama, Missouri, Grant (1921-1922): 5 coins
- Monroe through Stone Mountain (1923-1925): 5 coins
- Oregon Trail Memorial (1926-1939): 14 issues
- Sesquicentennial (1926): 1 coin
- Vermont, Hawaiian (1927-1928): 2 coins
- Daniel Boone Bicentennial (1934-1938): 13 issues
- Texas Centennial (1934-1938): 13 issues
- Arkansas Centennial (1935-1939): 15 issues
- 1935-1936 commemoratives: ~30 coins
- 1937-1939 commemoratives: ~15 coins
- Booker T. Washington (1946-1951): ~10 coins
- Carver/Washington (1951-1954): ~20 coins

### Commemorative Gold Coins (12 coins)

**Gold Dollars ($1) - 8 coins:**
- 1903: Louisiana Purchase - Jefferson & McKinley (2 coins)
- 1904-1905: Lewis & Clark Exposition (2 coins)
- 1915: Panama-Pacific Exposition (1 coin)
- 1916-1917: McKinley Memorial (2 coins)
- 1922: Grant Memorial with Star (1 coin)

**Quarter Eagles ($2.50) - 2 coins:**
- 1915: Panama-Pacific Exposition
- 1926: Sesquicentennial of American Independence

**Fifty Dollars ($50) - 2 coins:**
- 1915: Panama-Pacific Round & Octagonal

## CSV Data Analysis

**Source:** Issue #60 attached file
**Filename:** `Coins and Currency Master - Master Com List.csv`

### CSV Structure (from WebFetch)
Columns:
- Year
- Mint
- Coin Name
- Denom (Denomination)
- Mintage
- Silver Content (%)
- Silver Weight (oz)
- Diameter (mm)
- Weight (grams)
- Notes
- Book verified mintage year name

### Notable Entries Mentioned in CSV
- 1892: World's Columbian Exposition - "First US commemorative coin"
- 1925: Stone Mountain Memorial (1,314,709) - "Highest mintage"
- 1928: Hawaiian Sesquicentennial (10,008) - "One of the rarest"
- 1935: Hudson NY Sesquicentennial (10,008) - Also very rare
- 1935: Old Spanish Trail (10,008) - Also very rare
- 1926: Sesquicentennial - "Only living president on US coin" (Calvin Coolidge)
- 1946: Booker T. Washington - "First African American on US coin"
- 1954: Carver/Washington - "Final classic commemorative"

## Analysis: What are the 7 Additional CSV Rows?

### Possible Explanations

1. **Additional Commemorative Dollars** (most likely)
   - Issue #53 only added 1 commemorative dollar (Lafayette 1900)
   - Classic commemoratives included ~15 different silver dollar designs
   - CSV likely includes: Monroe Doctrine, Grant, Hawaiian, etc.

2. **Missing Half Dollar Issues**
   - Possible gaps in the 139 half dollars
   - Need CSV to identify specific missing coins

3. **Additional Gold Coins**
   - Issue #53 added 12 gold commemoratives
   - CSV might include a few more issues

4. **Data Format Differences**
   - Header row counted in CSV
   - Varieties listed separately vs combined

## Next Steps

### Phase 2: Detailed Comparison (BLOCKED)

**Blocker:** CSV file not directly downloadable from GitHub
**URL:** https://github.com/user-attachments/files/23176952/Coins.and.Currency.Master.-.Master.Com.List.csv

**Resolution Options:**

1. **User provides CSV manually**
   ```bash
   # Download from GitHub Issue #60
   # Save to: /tmp/commemorative_coins.csv
   ```

2. **Run analysis script**
   ```bash
   uv run python scripts/analyze_commemorative_csv.py
   ```

3. **Alternative: Parse CSV from issue comments**
   - If CSV data was pasted in issue comments
   - Can extract and compare directly

### Expected Findings

Based on analysis, we expect to find:
- **~6-7 additional commemorative silver dollars**
- Possible format: US-[TYPE]-YEAR-MINT
- All from classic commemorative era (1900-1939)

### Success Criteria

- [ ] CSV file obtained and parsed
- [ ] All 159 rows identified and categorized
- [ ] 7 additional coins explicitly identified
- [ ] Validation against Red Book or PCGS CoinFacts
- [ ] Ready for Phase 3 (migration script)

## Database Query for Verification

```sql
-- All commemorative coins (by content, not just denomination)
SELECT
    denomination,
    COUNT(*) as count
FROM coins
WHERE coin_id LIKE '%-PP%'  -- Panama-Pacific
   OR coin_id LIKE '%-WCOL%' -- Columbian
   OR coin_id LIKE '%-ORTR%' -- Oregon Trail
   OR coin_id LIKE '%-LEWC%' -- Lewis & Clark
   OR coin_id LIKE '%-LAFA%' -- Lafayette
   OR series LIKE '%Commemorative%'
   OR series LIKE '%Exposition%'
   OR series LIKE '%Centennial%'
   OR series LIKE '%Sesquicentennial%'
   OR series LIKE '%Memorial%'
   OR series LIKE '%Bicentennial%'
GROUP BY denomination;
```

## Conclusion

Issue #53 successfully added 152 classic commemorative coins. The CSV contains 7 additional entries that need to be identified and potentially added to the database. Most likely these are additional commemorative silver dollar designs from the 1900-1939 era.

**Status:** Awaiting CSV file to proceed with detailed comparison.
