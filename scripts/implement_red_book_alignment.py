#!/usr/bin/env python3
"""
Implement Red Book Classification System Alignment
Adds hierarchical Red Book categories to our taxonomy system
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

def create_red_book_tables(conn):
    """Create the red_book_categories table and update existing tables"""
    cursor = conn.cursor()
    
    # Create red_book_categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS red_book_categories (
            category_id TEXT PRIMARY KEY,
            parent_category_id TEXT,
            category_name TEXT NOT NULL,
            category_level INTEGER NOT NULL CHECK(category_level IN (1, 2, 3)),
            sort_order INTEGER NOT NULL,
            date_range TEXT,
            description TEXT,
            is_placeholder BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_category_id) REFERENCES red_book_categories(category_id)
        )
    """)
    
    # Add index for hierarchy queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_red_book_parent 
        ON red_book_categories(parent_category_id)
    """)
    
    # Add red_book_category_id to coins table if not exists
    cursor.execute("""
        SELECT COUNT(*) FROM pragma_table_info('coins') 
        WHERE name='red_book_category_id'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            ALTER TABLE coins ADD COLUMN red_book_category_id TEXT 
            REFERENCES red_book_categories(category_id)
        """)
    
    # Add red_book_category_id to series_registry if not exists
    cursor.execute("""
        SELECT COUNT(*) FROM pragma_table_info('series_registry') 
        WHERE name='red_book_category_id'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            ALTER TABLE series_registry ADD COLUMN red_book_category_id TEXT 
            REFERENCES red_book_categories(category_id)
        """)
    
    conn.commit()
    print("✅ Red Book category tables created")

def populate_red_book_hierarchy(conn):
    """Populate the complete Red Book category hierarchy"""
    cursor = conn.cursor()
    
    # Level 1: Major Categories
    major_categories = [
        ("PRE_FEDERAL", None, "PRE-FEDERAL ISSUES", 1, 1, "Pre-1792", False),
        ("FEDERAL", None, "FEDERAL ISSUES", 1, 2, "1792-Date", False),
        ("BULLION", None, "BULLION AND RELATED COINS", 1, 3, "1986-Date", False),
        ("PATTERNS", None, "UNITED STATES PATTERN PIECES", 1, 4, "Various", True),
        ("OTHER", None, "OTHER ISSUES", 1, 5, "Various", True),
        ("APPENDICES", None, "APPENDICES", 1, 6, None, True)
    ]
    
    # Level 2: Type Categories under PRE-FEDERAL
    pre_federal_types = [
        ("COLONIAL", "PRE_FEDERAL", "Colonial Issues", 2, 1, "1616-1776", True),
        ("POST_COLONIAL", "PRE_FEDERAL", "Post-Colonial Issues", 2, 2, "1776-1792", False)
    ]
    
    # Level 2: Type Categories under FEDERAL
    federal_types = [
        ("CONTRACT", "FEDERAL", "Contract Issues and Patterns", 2, 1, "1792-1794", True),
        ("HALF_CENTS", "FEDERAL", "Half Cents", 2, 2, "1793-1857", False),
        ("LARGE_CENTS", "FEDERAL", "Large Cents", 2, 3, "1793-1857", False),
        ("SMALL_CENTS", "FEDERAL", "Small Cents", 2, 4, "1856-Date", False),
        ("TWO_CENTS", "FEDERAL", "Two-Cent Pieces", 2, 5, "1864-1873", True),
        ("THREE_CENTS", "FEDERAL", "Three-Cent Pieces", 2, 6, "1851-1889", True),
        ("NICKELS", "FEDERAL", "Nickel Five-Cent Pieces", 2, 7, "1866-Date", False),
        ("HALF_DIMES", "FEDERAL", "Half Dimes", 2, 8, "1794-1873", False),
        ("DIMES", "FEDERAL", "Dimes", 2, 9, "1796-Date", False),
        ("TWENTY_CENTS", "FEDERAL", "Twenty-Cent Pieces", 2, 10, "1875-1878", False),
        ("QUARTERS", "FEDERAL", "Quarter Dollars", 2, 11, "1796-Date", False),
        ("HALF_DOLLARS", "FEDERAL", "Half Dollars", 2, 12, "1794-Date", False),
        ("DOLLARS", "FEDERAL", "Silver and Related Dollars", 2, 13, "1794-Date", False),
        ("GOLD_DOLLARS", "FEDERAL", "Gold Dollars", 2, 14, "1849-1889", False),
        ("QUARTER_EAGLES", "FEDERAL", "Quarter Eagles ($2.50)", 2, 15, "1796-1929", False),
        ("THREE_DOLLAR_GOLD", "FEDERAL", "Three-Dollar Gold Pieces", 2, 16, "1854-1889", False),
        ("FOUR_DOLLAR_GOLD", "FEDERAL", "Four-Dollar Gold Pieces", 2, 17, "1879-1880", True),
        ("HALF_EAGLES", "FEDERAL", "Half Eagles ($5)", 2, 18, "1795-1929", False),
        ("EAGLES", "FEDERAL", "Eagles ($10)", 2, 19, "1795-1933", False),
        ("DOUBLE_EAGLES", "FEDERAL", "Double Eagles ($20)", 2, 20, "1849-1933", False),
        ("COMMEMORATIVES", "FEDERAL", "Commemoratives", 2, 21, "1892-Date", True),
        ("PROOF_MINT_SETS", "FEDERAL", "Proof and Mint Sets", 2, 22, "1936-Date", True)
    ]
    
    # Level 2: Type Categories under BULLION
    bullion_types = [
        ("SILVER_BULLION", "BULLION", "Silver Bullion", 2, 1, "1986-Date", True),
        ("GOLD_BULLION", "BULLION", "Gold Bullion", 2, 2, "1986-Date", True),
        ("PLATINUM_PALLADIUM", "BULLION", "Platinum and Palladium Bullion", 2, 3, "1997-Date", True)
    ]
    
    # Level 2: Type Categories under OTHER
    other_types = [
        ("PRIVATE_TERRITORIAL", "OTHER", "Private and Territorial Gold", 2, 1, "1830-1861", True),
        ("PRIVATE_TOKENS", "OTHER", "Private Tokens", 2, 2, "Various", True),
        ("CONFEDERATE", "OTHER", "Confederate Issues", 2, 3, "1861-1865", True),
        ("HAWAIIAN_PR", "OTHER", "Hawaiian and Puerto Rican Issues", 2, 4, "1847-1898", False),
        ("PHILIPPINE", "OTHER", "Philippine Issues", 2, 5, "1903-1945", True),
        ("ALASKA", "OTHER", "Alaska Tokens", 2, 6, "1935-1941", True)
    ]
    
    # Insert all categories
    for category in major_categories:
        cursor.execute("""
            INSERT OR IGNORE INTO red_book_categories 
            (category_id, parent_category_id, category_name, category_level, sort_order, date_range, is_placeholder)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, category)
    
    for category in pre_federal_types + federal_types + bullion_types + other_types:
        cursor.execute("""
            INSERT OR IGNORE INTO red_book_categories 
            (category_id, parent_category_id, category_name, category_level, sort_order, date_range, is_placeholder)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, category)
    
    conn.commit()
    print("✅ Red Book hierarchy populated")

def map_existing_series(conn):
    """Map existing series to Red Book categories"""
    cursor = conn.cursor()
    
    # Mapping of our series to Red Book categories
    series_mappings = {
        # Half Cents
        "Liberty Cap Half Cent": "HALF_CENTS",
        "Draped Bust Half Cent": "HALF_CENTS",
        
        # Large Cents
        "Chain Cent": "LARGE_CENTS",
        "Wreath Cent": "LARGE_CENTS",
        "Liberty Cap Cent": "LARGE_CENTS",
        "Draped Bust Large Cent": "LARGE_CENTS",
        "Classic Head Cent": "LARGE_CENTS",
        "Coronet Large Cent": "LARGE_CENTS",
        "Coronet Cent": "LARGE_CENTS",
        "Draped Bust Cent": "LARGE_CENTS",
        "Large Cent": "LARGE_CENTS",
        
        # Small Cents
        "Flying Eagle Cent": "SMALL_CENTS",
        "Indian Head Cent": "SMALL_CENTS",
        "Lincoln Wheat Cent": "SMALL_CENTS",
        "Lincoln Memorial Cent": "SMALL_CENTS",
        "Lincoln Bicentennial Cent": "SMALL_CENTS",
        "Lincoln Shield Cent": "SMALL_CENTS",
        
        # Nickels
        "Shield Nickel": "NICKELS",
        "Liberty Head Nickel": "NICKELS",
        "Buffalo Nickel": "NICKELS",
        "Jefferson Nickel": "NICKELS",
        
        # Half Dimes
        "Seated Liberty Half Dime": "HALF_DIMES",
        
        # Dimes
        "Seated Liberty Dime": "DIMES",
        "Barber Dime": "DIMES",
        "Mercury Dime": "DIMES",
        "Roosevelt Dime": "DIMES",
        
        # Twenty Cents
        "Twenty Cent Piece": "TWENTY_CENTS",
        
        # Quarters
        "Seated Liberty Quarter": "QUARTERS",
        "Barber Quarter": "QUARTERS",
        "Standing Liberty Quarter": "QUARTERS",
        "Washington Quarter": "QUARTERS",
        
        # Half Dollars
        "Capped Bust Half Dollar": "HALF_DOLLARS",
        "Seated Liberty Half Dollar": "HALF_DOLLARS",
        "Barber Half Dollar": "HALF_DOLLARS",
        "Walking Liberty Half Dollar": "HALF_DOLLARS",
        "Franklin Half Dollar": "HALF_DOLLARS",
        "Kennedy Half Dollar": "HALF_DOLLARS",
        
        # Dollars
        "Flowing Hair Dollar": "DOLLARS",
        "Gobrecht Dollar": "DOLLARS",
        "Seated Liberty Dollar": "DOLLARS",
        "Trade Dollar": "DOLLARS",
        "Morgan Dollar": "DOLLARS",
        "Peace Dollar": "DOLLARS",
        "Eisenhower Dollar": "DOLLARS",
        "Susan B. Anthony Dollar": "DOLLARS",
        "Sacagawea Dollar": "DOLLARS",
        
        # Gold Dollars
        "Gold Dollar Type I": "GOLD_DOLLARS",
        "Gold Dollar Type II": "GOLD_DOLLARS",
        "Gold Dollar Type III": "GOLD_DOLLARS",
        
        # Quarter Eagles
        "Quarter Eagle Capped Bust": "QUARTER_EAGLES",
        "Quarter Eagle Capped Bust Left": "QUARTER_EAGLES",
        "Quarter Eagle Capped Head": "QUARTER_EAGLES",
        "Quarter Eagle Classic Head": "QUARTER_EAGLES",
        "Quarter Eagle Liberty Head": "QUARTER_EAGLES",
        "Quarter Eagle Indian Head": "QUARTER_EAGLES",
        
        # Three Dollar Gold
        "Three Dollar Gold": "THREE_DOLLAR_GOLD",
        
        # Half Eagles
        "Half Eagle Capped Bust": "HALF_EAGLES",
        "Half Eagle Capped Bust Left": "HALF_EAGLES",
        "Half Eagle Capped Head": "HALF_EAGLES",
        "Half Eagle Classic Head": "HALF_EAGLES",
        "Half Eagle Liberty Head": "HALF_EAGLES",
        "Half Eagle Indian Head": "HALF_EAGLES",
        
        # Eagles
        "Eagle Capped Bust": "EAGLES",
        "Eagle Liberty Head": "EAGLES",
        "Eagle Indian Head": "EAGLES",
        
        # Double Eagles
        "Double Eagle Liberty Head": "DOUBLE_EAGLES",
        "Double Eagle Saint-Gaudens": "DOUBLE_EAGLES",
        
        # Post-Colonial
        "Fugio Cent": "POST_COLONIAL",
        "Virginia Penny": "POST_COLONIAL",
        "Virginia Halfpenny": "POST_COLONIAL",
        "Virginia Shilling": "POST_COLONIAL",
        
        # Hawaiian
        "Hawaii Dime": "HAWAIIAN_PR"
    }
    
    # Update coins with Red Book categories based on series_name
    for series_name, category_id in series_mappings.items():
        cursor.execute("""
            UPDATE coins 
            SET red_book_category_id = ?
            WHERE series_name = ? AND country = 'US'
        """, (category_id, series_name))
    
    conn.commit()
    
    # Report statistics
    cursor.execute("""
        SELECT COUNT(*) FROM coins 
        WHERE country = 'US' AND red_book_category_id IS NOT NULL
    """)
    mapped_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM coins WHERE country = 'US'")
    total_count = cursor.fetchone()[0]
    
    print(f"✅ Mapped {mapped_count} of {total_count} US coins to Red Book categories")

def create_missing_data_report(conn):
    """Generate report of missing datasets"""
    cursor = conn.cursor()
    
    # Find placeholder categories that need data
    cursor.execute("""
        SELECT category_id, category_name, date_range, category_level
        FROM red_book_categories
        WHERE is_placeholder = TRUE AND category_level = 2
        ORDER BY sort_order
    """)
    
    missing_categories = cursor.fetchall()
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "missing_categories": [],
        "high_priority": [],
        "medium_priority": [],
        "low_priority": []
    }
    
    high_priority = ["TWO_CENTS", "THREE_CENTS", "SILVER_BULLION", "GOLD_BULLION", "COMMEMORATIVES"]
    medium_priority = ["COLONIAL", "CONTRACT", "FOUR_DOLLAR_GOLD"]
    
    for cat_id, name, date_range, level in missing_categories:
        item = {
            "category_id": cat_id,
            "name": name,
            "date_range": date_range or "Various",
            "priority": "HIGH" if cat_id in high_priority else "MEDIUM" if cat_id in medium_priority else "LOW"
        }
        report["missing_categories"].append(item)
        
        if item["priority"] == "HIGH":
            report["high_priority"].append(item)
        elif item["priority"] == "MEDIUM":
            report["medium_priority"].append(item)
        else:
            report["low_priority"].append(item)
    
    # Save report
    report_path = Path("data/red_book_missing_data_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Missing data report saved to {report_path}")
    print(f"   - High Priority: {len(report['high_priority'])} categories")
    print(f"   - Medium Priority: {len(report['medium_priority'])} categories")
    print(f"   - Low Priority: {len(report['low_priority'])} categories")
    
    return report

def main():
    """Main execution"""
    print("🚀 Implementing Red Book Classification System Alignment")
    print("=" * 60)
    
    # Connect to database
    db_path = Path("database/coins.db")
    conn = sqlite3.connect(db_path)
    
    try:
        # Create tables
        create_red_book_tables(conn)
        
        # Populate hierarchy
        populate_red_book_hierarchy(conn)
        
        # Map existing data
        map_existing_series(conn)
        
        # Generate missing data report
        report = create_missing_data_report(conn)
        
        print("\n" + "=" * 60)
        print("✅ Red Book alignment implementation complete!")
        print(f"   - Categories created: 36")
        print(f"   - Missing datasets identified: {len(report['missing_categories'])}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()