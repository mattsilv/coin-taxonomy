#!/usr/bin/env python3
"""
Initialize database schema for Canada coins support.
Creates tables with proper constraints for multi-country support.
"""

import sqlite3
from pathlib import Path

def create_database_schema(conn):
    """Create database schema that supports multiple countries."""
    cursor = conn.cursor()
    
    # Drop existing table if it has the wrong constraint
    cursor.execute("DROP TABLE IF EXISTS coins")
    
    # Create coins table with multi-country support
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coins (
            coin_id TEXT PRIMARY KEY,
            year INTEGER NOT NULL,
            mint TEXT NOT NULL,
            denomination TEXT NOT NULL,
            series TEXT,
            variety TEXT,
            grade TEXT,
            composition TEXT,
            weight_grams REAL,
            diameter_mm REAL,
            thickness_mm REAL,
            edge TEXT,
            designer TEXT,
            obverse_description TEXT,
            reverse_description TEXT,
            business_strikes INTEGER,
            proof_strikes INTEGER,
            uncirculated_strikes INTEGER,
            mint_state_strikes INTEGER,
            special_strikes INTEGER,
            total_mintage INTEGER,
            notes TEXT,
            rarity TEXT CHECK(rarity IN ('key', 'semi-key', 'common', 'scarce', NULL)),
            source_citation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- Multi-country coin ID format: COUNTRY-TYPE-YEAR-MINT
            CONSTRAINT valid_coin_id_format CHECK (
                coin_id GLOB '[A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*' OR
                coin_id GLOB '[A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'
            )
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coin_country ON coins(substr(coin_id, 1, 2))')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coin_year ON coins(year)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coin_denomination ON coins(denomination)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coin_series ON coins(series)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_coin_rarity ON coins(rarity)')
    
    # Create issues table for universal format
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            issue_id TEXT PRIMARY KEY,
            country TEXT NOT NULL,
            object_type TEXT NOT NULL DEFAULT 'coin',
            series_id TEXT NOT NULL,
            series_name TEXT NOT NULL,
            denomination TEXT NOT NULL,
            currency_unit TEXT NOT NULL,
            face_value REAL NOT NULL,
            year_start INTEGER NOT NULL,
            year_end INTEGER,
            composition_summary TEXT,
            diameter_mm REAL,
            weight_grams REAL,
            thickness_mm REAL,
            shape TEXT DEFAULT 'round',
            edge_type TEXT,
            obverse_design TEXT,
            reverse_design TEXT,
            obverse_designer TEXT,
            reverse_designer TEXT,
            obverse_legend TEXT,
            reverse_legend TEXT,
            total_mintage INTEGER,
            proof_mintage INTEGER,
            business_mintage INTEGER,
            special_strikes INTEGER,
            known_varieties INTEGER,
            major_varieties TEXT,
            rarity_category TEXT,
            pcgs_number TEXT,
            ngc_number TEXT,
            krause_number TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            CONSTRAINT valid_issue_id CHECK (
                issue_id GLOB '[A-Z][A-Z]-[A-Z]*-[0-9][0-9][0-9][0-9]*' OR
                issue_id GLOB '[A-Z][A-Z][A-Z]-[A-Z]*-[0-9][0-9][0-9][0-9]*'
            )
        )
    ''')
    
    # Create composition registry table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS composition_registry (
            composition_id TEXT PRIMARY KEY,
            composition_name TEXT NOT NULL,
            primary_metal TEXT,
            silver_content REAL,
            gold_content REAL,
            copper_content REAL,
            nickel_content REAL,
            zinc_content REAL,
            tin_content REAL,
            manganese_content REAL,
            iron_content REAL,
            other_metals TEXT,
            is_precious BOOLEAN DEFAULT 0,
            is_base_metal BOOLEAN DEFAULT 0,
            magnetic_properties TEXT,
            color TEXT,
            density_g_cm3 REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create series registry table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS series_registry (
            series_id TEXT PRIMARY KEY,
            country TEXT NOT NULL,
            series_name TEXT NOT NULL,
            series_type TEXT,
            start_year INTEGER,
            end_year INTEGER,
            is_active BOOLEAN DEFAULT 0,
            denomination TEXT,
            category TEXT,
            subcategory TEXT,
            design_theme TEXT,
            legislation TEXT,
            authorizing_act TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create subject registry table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject_registry (
            subject_id TEXT PRIMARY KEY,
            subject_name TEXT NOT NULL,
            subject_type TEXT,
            birth_year INTEGER,
            death_year INTEGER,
            nationality TEXT,
            occupation TEXT,
            significance TEXT,
            appears_on_coins TEXT,
            appears_on_bills TEXT,
            first_appearance_year INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    print("✅ Database schema created successfully")

def main():
    """Main function."""
    print("🏗️ Initializing Database Schema for Multi-Country Support")
    print("=" * 60)
    
    db_path = Path(__file__).parent.parent / "coins.db"
    conn = sqlite3.connect(str(db_path))
    
    try:
        create_database_schema(conn)
        
        # Verify tables were created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\n📊 Created tables:")
        for table in tables:
            print(f"  ✓ {table[0]}")
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()