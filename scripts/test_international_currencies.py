#!/usr/bin/env python3
"""
Test International Currency Implementation

This script tests the universal taxonomy implementation by adding sample
international currencies from the research reports and validating the
database handles them correctly.

Based on research from:
- Issue #10 best practices
- Perplexity research report  
- Gemini research report (temp-geminidr.md)
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any


def get_database_connection():
    """Get connection to the coins database."""
    return sqlite3.connect('database/coins.db')


def validate_coin_id_format(coin_id: str) -> bool:
    """Validate coin ID follows the universal format."""
    parts = coin_id.split('-')
    if len(parts) != 4:
        return False
    
    country, type_code, year, mint = parts
    
    # Country: 2-4 characters
    if not (2 <= len(country) <= 4 and country.isupper() and country.isalpha()):
        return False
    
    # TYPE: exactly 4 characters
    if len(type_code) != 4 or not type_code.isupper():
        return False
    
    # YEAR: 4 digits or 0000
    if not (year.isdigit() and len(year) == 4):
        return False
    
    # MINT: 1-4 characters
    if not (1 <= len(mint) <= 4 and mint.isupper()):
        return False
    
    return True


def create_sample_international_currencies():
    """Create sample international currency entries for testing."""
    
    sample_currencies = [
        # Chinese Yuan (from Gemini research)
        {
            "coin_id": "CN-YUAN-1980-BEI",
            "series_id": "CN_YUAN_MODERN",
            "country": "CN",
            "denomination": "Yuan",
            "series_name": "Modern Yuan",
            "year": 1980,
            "mint": "BEI",
            "category": "COIN",
            "calendar_type": "GREGORIAN",
            "obverse_description": "National emblem of China with Tiananmen Gate",
            "reverse_description": "Denomination numeral with traditional Chinese design",
            "distinguishing_features": json.dumps(["National emblem", "Chinese characters"]),
            "identification_keywords": json.dumps(["Yuan", "China", "Modern"]),
            "common_names": json.dumps(["Chinese Yuan", "Renminbi"])
        },
        
        # Japanese Yen (Showa era conversion from Gemini research)
        {
            "coin_id": "JP-YEN-1970-OSA",
            "series_id": "JP_YEN_SHOWA",
            "country": "JP", 
            "denomination": "Yen",
            "series_name": "Showa Era Yen",
            "year": 1970,
            "mint": "OSA",
            "category": "COIN",
            "calendar_type": "JAPANESE_ERA",
            "original_date": "Showa 45",
            "obverse_description": "Chrysanthemum design with era inscription",
            "reverse_description": "Denomination with stylized plant motif",
            "distinguishing_features": json.dumps(["Chrysanthemum seal", "Era dating"]),
            "identification_keywords": json.dumps(["Yen", "Japan", "Showa"]),
            "common_names": json.dumps(["Japanese Yen", "Showa Yen"])
        },
        
        # German Euro (modern)
        {
            "coin_id": "EU-EURO-2002-A",
            "series_id": "EU_EURO_COINS",
            "country": "EU",
            "denomination": "Euro",
            "series_name": "Euro Coins",
            "year": 2002,
            "mint": "A",
            "category": "COIN",
            "calendar_type": "GREGORIAN",
            "obverse_description": "German eagle with stars of European Union",
            "reverse_description": "Map of Europe with denomination",
            "distinguishing_features": json.dumps(["German eagle", "EU stars", "A mint mark"]),
            "identification_keywords": json.dumps(["Euro", "Germany", "European Union"]),
            "common_names": json.dumps(["Euro coin", "German Euro"])
        },
        
        # East Caribbean Dollar (multi-nation currency from research)
        {
            "coin_id": "XCD-DOLR-2000-ECCB",
            "series_id": "XCD_DOLLAR_MODERN",
            "country": "XCD",
            "denomination": "Dollar",
            "series_name": "East Caribbean Dollar",
            "year": 2000,
            "mint": "ECCB",
            "category": "COIN",
            "calendar_type": "GREGORIAN",
            "obverse_description": "Queen Elizabeth II portrait",
            "reverse_description": "Sailing ship with Caribbean islands",
            "distinguishing_features": json.dumps(["Multi-nation currency", "ECCB authority"]),
            "identification_keywords": json.dumps(["Caribbean", "Dollar", "Eastern Caribbean"]),
            "common_names": json.dumps(["EC Dollar", "Eastern Caribbean Dollar"])
        },
        
        # Canadian Maple Leaf (bullion from research)
        {
            "coin_id": "CA-MAPL-2020-W",
            "series_id": "CA_MAPLE_LEAF",
            "country": "CA",
            "denomination": "Dollars",
            "series_name": "Silver Maple Leaf",
            "year": 2020,
            "mint": "W",
            "category": "BULLION",
            "calendar_type": "GREGORIAN",
            "composition": json.dumps({
                "alloy_name": "Silver",
                "alloy": {"silver": 0.9999}
            }),
            "weight_grams": 31.1,
            "diameter_mm": 38.0,
            "obverse_description": "Queen Elizabeth II portrait with denomination",
            "reverse_description": "Detailed maple leaf with radial lines",
            "distinguishing_features": json.dumps(["999.9 silver purity", "Radial lines security feature"]),
            "identification_keywords": json.dumps(["Maple Leaf", "Canada", "Silver", "Bullion"]),
            "common_names": json.dumps(["Silver Maple Leaf", "Canadian Silver Dollar"])
        },
        
        # German Notgeld (edge case from Gemini research)
        {
            "coin_id": "DE-NG50-1921-BER",
            "series_id": "DE_NOTGELD_1920S",
            "country": "DE",
            "denomination": "Emergency Money",
            "series_name": "Berlin Notgeld",
            "year": 1921,
            "mint": "BER",
            "category": "SCRIP",
            "issuer": "City of Berlin",
            "calendar_type": "GREGORIAN",
            "obverse_description": "Berlin city coat of arms with denomination",
            "reverse_description": "Emergency authorization text in German",
            "distinguishing_features": json.dumps(["Emergency money", "Municipal issue", "Post-WWI period"]),
            "identification_keywords": json.dumps(["Notgeld", "Berlin", "Emergency", "Germany"]),
            "common_names": json.dumps(["Notgeld", "Emergency Money", "Berlin Scrip"])
        },
        
        # Zimbabwe hyperinflation note (edge case from research)
        {
            "coin_id": "ZW-100T-2008-RBZ",
            "series_id": "ZW_HYPERINFLATION",
            "country": "ZW",
            "denomination": "Banknotes",
            "series_name": "Zimbabwe Hyperinflation Notes",
            "year": 2008,
            "mint": "RBZ",
            "category": "BILL",
            "issuer": "Reserve Bank of Zimbabwe",
            "calendar_type": "GREGORIAN",
            "obverse_description": "Zimbabwe coat of arms with astronomical denomination",
            "reverse_description": "Victoria Falls with various wildlife",
            "distinguishing_features": json.dumps(["100 trillion denomination", "Hyperinflation artifact"]),
            "identification_keywords": json.dumps(["Zimbabwe", "Trillion", "Hyperinflation", "Reserve Bank"]),
            "common_names": json.dumps(["Zimbabwe Dollar", "Hyperinflation Note"])
        },
        
        # US Military Payment Certificate (edge case)
        {
            "coin_id": "US-MPC5-1970-DOD",
            "series_id": "US_MPC_SERIES_692",
            "country": "US",
            "denomination": "Military Currency",
            "series_name": "Military Payment Certificate Series 692",
            "year": 1970,
            "mint": "DOD",
            "category": "SCRIP",
            "issuer": "Department of Defense",
            "calendar_type": "GREGORIAN",
            "obverse_description": "Military Payment Certificate designation with serial number",
            "reverse_description": "Department of Defense seal with security elements",
            "distinguishing_features": json.dumps(["Military use only", "Series 692", "DOD authority"]),
            "identification_keywords": json.dumps(["MPC", "Military", "Certificate", "Department of Defense"]),
            "common_names": json.dumps(["Military Payment Certificate", "MPC", "Military Money"])
        }
    ]
    
    return sample_currencies


def insert_sample_currencies(conn, currencies):
    """Insert sample currencies into the database."""
    cursor = conn.cursor()
    
    print("🔍 Testing international currency insertion...")
    
    for currency in currencies:
        coin_id = currency["coin_id"]
        
        # Validate coin ID format
        if not validate_coin_id_format(coin_id):
            print(f"  ❌ Invalid coin ID format: {coin_id}")
            continue
        
        try:
            # Insert the currency
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name,
                    year, mint, category, calendar_type, original_date, issuer,
                    composition, weight_grams, diameter_mm,
                    obverse_description, reverse_description,
                    distinguishing_features, identification_keywords, common_names
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                currency["coin_id"],
                currency["series_id"],
                currency["country"],
                currency["denomination"],
                currency["series_name"],
                currency["year"],
                currency["mint"],
                currency.get("category"),
                currency.get("calendar_type"),
                currency.get("original_date"),
                currency.get("issuer"),
                currency.get("composition"),
                currency.get("weight_grams"),
                currency.get("diameter_mm"),
                currency["obverse_description"],
                currency["reverse_description"],
                currency["distinguishing_features"],
                currency["identification_keywords"],
                currency["common_names"]
            ))
            
            print(f"  ✅ Added: {coin_id}")
            
        except sqlite3.Error as e:
            print(f"  ❌ Failed to insert {coin_id}: {e}")
    
    conn.commit()


def test_database_queries(conn):
    """Test various queries on the international data."""
    cursor = conn.cursor()
    
    print("\n🔍 Testing database queries...")
    
    # Test 1: Count coins by category
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM coins 
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY count DESC
    """)
    
    print("\n📊 Coins by category:")
    for category, count in cursor.fetchall():
        print(f"  {category}: {count}")
    
    # Test 2: Test calendar type handling
    cursor.execute("""
        SELECT calendar_type, COUNT(*) as count
        FROM coins
        WHERE calendar_type IS NOT NULL
        GROUP BY calendar_type
    """)
    
    print("\n📅 Calendar types:")
    for cal_type, count in cursor.fetchall():
        print(f"  {cal_type}: {count}")
    
    # Test 3: Test era date conversion
    cursor.execute("""
        SELECT coin_id, year, original_date, calendar_type
        FROM coins
        WHERE original_date IS NOT NULL
    """)
    
    print("\n🗓️  Era date conversions:")
    for coin_id, year, original_date, cal_type in cursor.fetchall():
        print(f"  {coin_id}: {original_date} → {year} ({cal_type})")
    
    # Test 4: Test multi-nation currencies
    cursor.execute("""
        SELECT coin_id, country, series_name
        FROM coins
        WHERE country IN ('EU', 'XCD', 'XOF', 'XAF')
    """)
    
    print("\n🌍 Multi-nation currencies:")
    for coin_id, country, series_name in cursor.fetchall():
        print(f"  {coin_id}: {country} - {series_name}")
    
    # Test 5: Test edge cases
    cursor.execute("""
        SELECT coin_id, category, issuer
        FROM coins
        WHERE category IN ('SCRIP', 'BILL') AND issuer IS NOT NULL
    """)
    
    print("\n⚡ Edge cases (scrip/special issues):")
    for coin_id, category, issuer in cursor.fetchall():
        print(f"  {coin_id}: {category} by {issuer}")


def test_reference_tables(conn):
    """Test the reference tables functionality."""
    cursor = conn.cursor()
    
    print("\n🔍 Testing reference tables...")
    
    # Test country codes
    cursor.execute("SELECT code, name, type FROM country_codes ORDER BY type, code")
    print("\n🌍 Country codes:")
    for code, name, type_cat in cursor.fetchall():
        print(f"  {code}: {name} ({type_cat})")
    
    # Test TYPE codes by category
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM type_codes
        GROUP BY category
        ORDER BY count DESC
    """)
    print("\n🏷️  TYPE codes by category:")
    for category, count in cursor.fetchall():
        print(f"  {category}: {count}")
    
    # Test mint facilities
    cursor.execute("""
        SELECT country_code, COUNT(*) as facility_count
        FROM mint_facilities
        GROUP BY country_code
        ORDER BY facility_count DESC
    """)
    print("\n🏭 Mint facilities by country:")
    for country, count in cursor.fetchall():
        print(f"  {country}: {count} facilities")


def validate_taxonomy_integrity(conn):
    """Validate that the taxonomy maintains data integrity."""
    cursor = conn.cursor()
    
    print("\n🔍 Validating taxonomy integrity...")
    
    # Check for invalid coin ID formats
    cursor.execute("""
        SELECT coin_id FROM coins
        WHERE coin_id NOT GLOB '*-*-*-*'
    """)
    invalid_formats = cursor.fetchall()
    if invalid_formats:
        print(f"  ❌ Found {len(invalid_formats)} coins with invalid ID format")
        for (coin_id,) in invalid_formats[:3]:  # Show first 3
            print(f"    {coin_id}")
    else:
        print("  ✅ All coin IDs follow 4-part format")
    
    # Check for missing required fields
    cursor.execute("""
        SELECT COUNT(*)
        FROM coins
        WHERE obverse_description IS NULL OR reverse_description IS NULL 
           OR distinguishing_features IS NULL OR identification_keywords IS NULL
           OR common_names IS NULL
    """)
    missing_fields = cursor.fetchone()[0]
    if missing_fields > 0:
        print(f"  ❌ Found {missing_fields} coins missing required visual description fields")
    else:
        print("  ✅ All coins have required visual description fields")
    
    # Check category distribution
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN category IS NOT NULL THEN 1 END) as with_category
        FROM coins
    """)
    total, with_category = cursor.fetchone()
    print(f"  📊 Category coverage: {with_category}/{total} coins ({100*with_category//total}%)")
    
    # Check for TYPE code consistency
    cursor.execute("""
        SELECT coin_id FROM coins
        WHERE length(substr(coin_id, instr(coin_id, '-') + 1, 4)) != 4
    """)
    invalid_types = cursor.fetchall()
    if invalid_types:
        print(f"  ❌ Found {len(invalid_types)} coins with invalid TYPE code length")
    else:
        print("  ✅ All TYPE codes are exactly 4 characters")


def main():
    """Main test function."""
    print("🚀 Starting International Currency Taxonomy Test")
    
    try:
        conn = get_database_connection()
        
        # Create sample international currencies
        sample_currencies = create_sample_international_currencies()
        print(f"📊 Created {len(sample_currencies)} sample international currencies")
        
        # Insert sample currencies
        insert_sample_currencies(conn, sample_currencies)
        
        # Test database queries
        test_database_queries(conn)
        
        # Test reference tables
        test_reference_tables(conn)
        
        # Validate taxonomy integrity
        validate_taxonomy_integrity(conn)
        
        # Get final statistics
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM coins")
        total_coins = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM coins WHERE country != 'US'")
        international_coins = cursor.fetchone()[0]
        
        conn.close()
        
        print("\n🎉 International Currency Test Complete!")
        print(f"📊 Total coins in database: {total_coins}")
        print(f"🌍 International coins: {international_coins}")
        print(f"🇺🇸 US coins: {total_coins - international_coins}")
        
        if international_coins > 0:
            print("✅ Universal taxonomy successfully supports international currencies!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    main()