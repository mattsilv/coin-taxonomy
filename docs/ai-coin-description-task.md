# AI Task: Generate Visual Descriptions for US Coin Taxonomy

## Objective
Create comprehensive visual descriptions and identification keywords for all 118 coins in our US coin taxonomy database to enhance AI-powered coin identification systems.

## Context
Our current coin taxonomy has excellent technical data (mintages, years, mints) but lacks the visual/descriptive information needed for AI systems to identify coins from user descriptions or images. We need to add visual design descriptions and common identification keywords.

## Required Output Format

For each coin, provide this exact JSON structure:

```json
{
  "coin_id": "US-INCH-1877-P",
  "design_description": {
    "obverse": "Indian head profile facing left, wearing feathered headdress, 'UNITED STATES OF AMERICA' around rim, year at bottom",
    "reverse": "Oak wreath surrounding 'ONE CENT', shield at top of wreath",
    "distinguishing_features": [
      "Bronze composition gives copper color",
      "19.05mm diameter (small cent)",
      "Indian princess design (not actual Native American chief)",
      "Plain edge"
    ]
  },
  "identification_keywords": [
    "indian head cent",
    "indian penny", 
    "bronze cent",
    "small cent",
    "copper colored",
    "feathered headdress",
    "one cent",
    "oak wreath"
  ],
  "common_names": [
    "Indian Head Cent",
    "Indian Penny",
    "Indian Head Penny"
  ]
}
```

## Field Specifications

### `design_description`
- **obverse**: Detailed description of front/heads side design elements, text, positioning
- **reverse**: Detailed description of back/tails side design elements, text, positioning  
- **distinguishing_features**: Array of 3-5 key physical characteristics that help identify this coin type

### `identification_keywords` 
- 5-10 terms people would use to search for or describe this coin
- Include both formal names and slang terms
- Include physical descriptors (color, size, material)
- Include design elements users would notice

### `common_names`
- 2-4 most common ways collectors/public refer to this coin
- Include both formal and informal names

## Complete Coin List (118 coins)

Generate descriptions for ALL of these coins:

**Barber Dimes (6 coins):**
- US-BARD-1894-S (Barber Dime, 1894, San Francisco)
- US-BARD-1895-O (Barber Dime, 1895, New Orleans) 
- US-BARD-1896-S (Barber Dime, 1896, San Francisco)
- US-BARD-1901-S (Barber Dime, 1901, San Francisco)
- US-BARD-1903-S (Barber Dime, 1903, San Francisco)
- US-BARD-1904-S (Barber Dime, 1904, San Francisco)

**Barber Quarters (4 coins):**
- US-BARQ-1892-P (Barber Quarter, 1892, Philadelphia)
- US-BARQ-1896-S (Barber Quarter, 1896, San Francisco)
- US-BARQ-1901-S (Barber Quarter, 1901, San Francisco)
- US-BARQ-1913-S (Barber Quarter, 1913, San Francisco)

**Buffalo Nickels (5 coins):**
- US-BUFF-1913-S (Buffalo Nickel, 1913, San Francisco)
- US-BUFF-1916-P (Buffalo Nickel, 1916, Philadelphia)
- US-BUFF-1918-D (Buffalo Nickel, 1918, Denver)
- US-BUFF-1926-S (Buffalo Nickel, 1926, San Francisco)
- US-BUFF-1937-D (Buffalo Nickel, 1937, Denver)

**Capped Bust Half Dollars (2 coins):**
- US-CBHD-1807-P (Capped Bust Half Dollar, 1807, Philadelphia)
- US-CBHD-1815-P (Capped Bust Half Dollar, 1815, Philadelphia)

**Early Large Cents (4 coins):**
- US-LCHN-1793-P (Chain Cent, 1793, Philadelphia)
- US-LWRE-1793-P (Wreath Cent, 1793, Philadelphia)
- US-DRPB-1799-P (Draped Bust Large Cent, 1799, Philadelphia)
- US-CORL-1856-P (Coronet Large Cent, 1856, Philadelphia)

**Half Cents (2 coins):**
- US-HCLC-1793-P (Liberty Cap Half Cent, 1793, Philadelphia)
- US-HCDB-1800-P (Draped Bust Half Cent, 1800, Philadelphia)

**Early Dollars (3 coins):**
- US-FHDO-1794-P (Flowing Hair Dollar, 1794, Philadelphia)
- US-GBDO-1836-P (Gobrecht Dollar, 1836, Philadelphia)
- US-GBDO-1838-P (Gobrecht Dollar, 1838, Philadelphia)

**Modern Dollars (12 coins):**
- US-EISE-1973-D (Eisenhower Dollar, 1973, Denver)
- US-EISE-1973-P (Eisenhower Dollar, 1973, Philadelphia) 
- US-EISE-1976-P (Eisenhower Dollar, 1976, Philadelphia)
- US-MORG-1879-CC (Morgan Dollar, 1879, Carson City)
- US-MORG-1889-CC (Morgan Dollar, 1889, Carson City)
- US-MORG-1893-S (Morgan Dollar, 1893, San Francisco)
- US-MORG-1894-P (Morgan Dollar, 1894, Philadelphia)
- US-MORG-1895-O (Morgan Dollar, 1895, New Orleans)
- US-MORG-1895-P (Morgan Dollar, 1895, Philadelphia)
- US-MORG-1895-S (Morgan Dollar, 1895, San Francisco)
- US-MORG-1903-O (Morgan Dollar, 1903, New Orleans)
- US-PEAC-1921-P (Peace Dollar, 1921, Philadelphia)
- US-PEAC-1927-D (Peace Dollar, 1927, Denver)
- US-PEAC-1928-P (Peace Dollar, 1928, Philadelphia)
- US-PEAC-1934-S (Peace Dollar, 1934, San Francisco)
- US-SACA-2000-D (Sacagawea Dollar, 2000, Denver)
- US-SACA-2000-P (Sacagawea Dollar, 2000, Philadelphia)
- US-SANT-1979-P (Susan B. Anthony Dollar, 1979, Philadelphia)
- US-SANT-1979-S (Susan B. Anthony Dollar, 1979, San Francisco)
- US-SANT-1999-P (Susan B. Anthony Dollar, 1999, Philadelphia)

**Flying Eagle Cents (2 coins):**
- US-FECN-1857-P (Flying Eagle Cent, 1857, Philadelphia)
- US-FECN-1858-P (Flying Eagle Cent, 1858, Philadelphia)

**Indian Head Cents (6 coins):**
- US-INCH-1864-P (Indian Head Cent, 1864, Philadelphia)
- US-INCH-1869-P (Indian Head Cent, 1869, Philadelphia)
- US-INCH-1877-P (Indian Head Cent, 1877, Philadelphia)
- US-INCH-1888-P (Indian Head Cent, 1888, Philadelphia)
- US-INCH-1908-S (Indian Head Cent, 1908, San Francisco)
- US-INCH-1909-S (Indian Head Cent, 1909, San Francisco)

**Jefferson Nickels (2 coins):**
- US-JEFF-1950-D (Jefferson Nickel, 1950, Denver)
- US-JEFF-1971-S (Jefferson Nickel, 1971, San Francisco)

**Liberty Head Nickels (4 coins):**
- US-LHNI-1883-P (Liberty Head Nickel, 1883, Philadelphia)
- US-LHNI-1885-P (Liberty Head Nickel, 1885, Philadelphia)
- US-LHNI-1912-S (Liberty Head Nickel, 1912, San Francisco)
- US-LHNI-1913-P (Liberty Head Nickel, 1913, Philadelphia)

**Lincoln Cents (15 coins):**
- US-LBCT-2009-D (Lincoln Bicentennial Cent, 2009, Denver)
- US-LBCT-2009-P (Lincoln Bicentennial Cent, 2009, Philadelphia)
- US-LMCT-1969-S (Lincoln Memorial Cent, 1969, San Francisco)
- US-LMCT-1972-P (Lincoln Memorial Cent, 1972, Philadelphia)
- US-LMCT-1983-P (Lincoln Memorial Cent, 1983, Philadelphia)
- US-LSCT-2017-P (Lincoln Shield Cent, 2017, Philadelphia)
- US-LSCT-2019-W (Lincoln Shield Cent, 2019, West Point)
- US-LWCT-1909-S (Lincoln Wheat Cent, 1909, San Francisco)
- US-LWCT-1914-D (Lincoln Wheat Cent, 1914, Denver)
- US-LWCT-1922-D (Lincoln Wheat Cent, 1922, Denver)
- US-LWCT-1931-S (Lincoln Wheat Cent, 1931, San Francisco)
- US-LWCT-1943-P (Lincoln Wheat Cent, 1943, Philadelphia)
- US-LWCT-1944-P (Lincoln Wheat Cent, 1944, Philadelphia)
- US-LWCT-1955-P (Lincoln Wheat Cent, 1955, Philadelphia)

**Mercury Dimes (13 coins):**
- US-MERC-1916-D (Mercury Dime, 1916, Denver)
- US-MERC-1916-P (Mercury Dime, 1916, Philadelphia)
- US-MERC-1916-S (Mercury Dime, 1916, San Francisco)
- US-MERC-1921-D (Mercury Dime, 1921, Denver)
- US-MERC-1921-P (Mercury Dime, 1921, Philadelphia)
- US-MERC-1926-S (Mercury Dime, 1926, San Francisco)
- US-MERC-1931-D (Mercury Dime, 1931, Denver)
- US-MERC-1931-S (Mercury Dime, 1931, San Francisco)
- US-MERC-1942-D (Mercury Dime, 1942, Denver)
- US-MERC-1942-P (Mercury Dime, 1942, Philadelphia)
- US-MERC-1945-D (Mercury Dime, 1945, Denver)
- US-MERC-1945-P (Mercury Dime, 1945, Philadelphia)
- US-MERC-1945-S (Mercury Dime, 1945, San Francisco)

**Roosevelt Dimes (11 coins):**
- US-ROOS-1946-D (Roosevelt Dime, 1946, Denver)
- US-ROOS-1946-P (Roosevelt Dime, 1946, Philadelphia)
- US-ROOS-1946-S (Roosevelt Dime, 1946, San Francisco)
- US-ROOS-1949-S (Roosevelt Dime, 1949, San Francisco)
- US-ROOS-1964-D (Roosevelt Dime, 1964, Denver)
- US-ROOS-1964-P (Roosevelt Dime, 1964, Philadelphia)
- US-ROOS-1965-P (Roosevelt Dime, 1965, Philadelphia)
- US-ROOS-1968-S (Roosevelt Dime, 1968, San Francisco)
- US-ROOS-1975-S (Roosevelt Dime, 1975, San Francisco)
- US-ROOS-1996-W (Roosevelt Dime, 1996, West Point)
- US-ROOS-2009-D (Roosevelt Dime, 2009, Denver)

**Seated Liberty Coins (3 coins):**
- US-SLDI-1837-P (Seated Liberty Dime, 1837, Philadelphia)
- US-SLDI-1844-P (Seated Liberty Dime, 1844, Philadelphia)
- US-SLQU-1838-P (Seated Liberty Quarter, 1838, Philadelphia)

**Shield Nickels (4 coins):**
- US-SHLD-1867-P (Shield Nickel, 1867, Philadelphia)
- US-SHLD-1877-P (Shield Nickel, 1877, Philadelphia)
- US-SHLD-1878-P (Shield Nickel, 1878, Philadelphia)
- US-SHLD-1880-P (Shield Nickel, 1880, Philadelphia)

**Standing Liberty Quarters (5 coins):**
- US-SLIQ-1916-P (Standing Liberty Quarter, 1916, Philadelphia)
- US-SLIQ-1917-P (Standing Liberty Quarter, 1917, Philadelphia)
- US-SLIQ-1918-S (Standing Liberty Quarter, 1918, San Francisco)
- US-SLIQ-1921-P (Standing Liberty Quarter, 1921, Philadelphia)
- US-SLIQ-1927-S (Standing Liberty Quarter, 1927, San Francisco)

**Trade Dollars (2 coins):**
- US-TRDO-1873-P (Trade Dollar, 1873, Philadelphia)
- US-TRDO-1878-CC (Trade Dollar, 1878, Carson City)

**Twenty Cent Piece (1 coin):**
- US-TWCT-1875-P (Twenty Cent Piece, 1875, Philadelphia)

**Washington Quarters (5 coins):**
- US-WASH-1932-D (Washington Quarter, 1932, Denver)
- US-WASH-1932-S (Washington Quarter, 1932, San Francisco)
- US-WASH-1999-P (Washington Quarter, 1999, Philadelphia)
- US-WASH-2019-W (Washington Quarter, 2019, West Point)
- US-WASH-2020-W (Washington Quarter, 2020, West Point)

## Quality Requirements

1. **Accuracy**: Descriptions must be factually correct based on official US Mint design specifications
2. **Completeness**: All 118 coins must be included
3. **Consistency**: Use consistent terminology and format across all entries
4. **User-Focused**: Keywords should reflect terms actual users would search for
5. **AI-Optimized**: Descriptions should help AI systems distinguish between similar coin types

## Research Sources

Use authoritative numismatic sources such as:
- US Mint official specifications
- PCGS CoinFacts
- NGC Coin Explorer  
- Red Book (Guide Book of United States Coins)
- Professional numismatic references

## Output Format

Provide a single JSON file containing an array of all 118 coin description objects following the exact format specified above.

## Critical Notes

- Focus on VISUAL characteristics that help identify coins
- Include both technical and colloquial terms
- Emphasize distinguishing features between similar series
- Consider what a non-expert would notice when looking at the coin
- Include size, color, and material descriptors when relevant