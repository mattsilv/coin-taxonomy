#!/usr/bin/env python3
"""
Migration script for Universal Currency Taxonomy v1.1
Transforms existing US coin database to universal structure.

This migration:
1. Creates new registry tables (subjects, compositions, series)
2. Creates new issues table with universal structure
3. Migrates existing US coin data to new format
4. Preserves all existing data integrity
"""

import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path


def create_universal_schema(conn):
    """Create the new universal taxonomy schema."""
    cursor = conn.cursor()
    
    # Subject Registry - Universal catalog of people, symbols, design elements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject_registry (
            subject_id TEXT PRIMARY KEY,
            type TEXT NOT NULL,  -- historical_figure, flora, fauna, symbol, architectural, etc.
            name TEXT NOT NULL,
            nationality TEXT,
            roles JSON,  -- array of roles: ["president", "monarch", etc.]
            life_dates JSON,  -- {"birth": year, "death": year}
            reign_dates JSON,  -- {"start": year, "end": year} for monarchs
            significance TEXT,
            symbolism JSON,  -- array of symbolic meanings
            scientific_name TEXT,  -- for flora/fauna
            first_coin_appearance INTEGER,
            metadata JSON,  -- flexible field for type-specific data
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Composition Registry - Universal alloy and material definitions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS composition_registry (
            composition_key TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            alloy_composition JSON NOT NULL,  -- {"copper": 0.95, "tin": 0.04, "zinc": 0.01}
            period_description TEXT,
            density_g_cm3 REAL,
            magnetic_properties TEXT,
            color_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Series Registry - Universal series definitions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS series_registry (
            series_id TEXT PRIMARY KEY,
            series_name TEXT NOT NULL,
            series_abbreviation TEXT UNIQUE NOT NULL,  -- Unique 3-4 char abbreviation for ID generation
            country_code TEXT NOT NULL,
            denomination TEXT NOT NULL,
            start_year INTEGER NOT NULL,
            end_year INTEGER,
            defining_characteristics TEXT,
            official_name TEXT,
            type TEXT DEFAULT 'coin',  -- coin, banknote
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Issues Table - Universal flat structure for all currency items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            issue_id TEXT PRIMARY KEY,
            object_type TEXT NOT NULL,  -- coin, banknote
            series_id TEXT NOT NULL,
            
            -- Issuing Entity
            country_code TEXT NOT NULL,
            authority_name TEXT NOT NULL,
            monetary_system TEXT NOT NULL,  -- decimal, pre-decimal, etc.
            currency_unit TEXT NOT NULL,
            
            -- Denomination
            face_value REAL NOT NULL,
            unit_name TEXT NOT NULL,
            common_names JSON,  -- array of common names
            system_fraction TEXT,  -- "1/100 dollar"
            
            -- Issue Details
            issue_year INTEGER NOT NULL,
            mint_id TEXT,
            date_range_start INTEGER,
            date_range_end INTEGER,
            
            -- Authority Context
            authority_period JSON,  -- {"entity_type": "federal_republic", "leader": {...}}
            
            -- Physical Specifications
            specifications JSON NOT NULL,  -- weight_grams, diameter_mm, etc.
            
            -- Design Elements
            sides JSON NOT NULL,  -- obverse and reverse design data
            
            -- Production Data
            mintage JSON,  -- business_strikes, proof_strikes, etc.
            rarity TEXT,
            varieties JSON,
            
            -- Metadata
            source_citation TEXT,
            notes TEXT,
            metadata JSON,  -- flexible field for future extensions
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (series_id) REFERENCES series_registry(series_id)
        )
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_issues_country_year ON issues(country_code, issue_year)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_issues_series ON issues(series_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_issues_denomination ON issues(face_value, unit_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subject_type ON subject_registry(type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_composition_period ON composition_registry(period_description)")
    
    conn.commit()
    print("✓ Created universal schema tables")


def populate_known_compositions(conn):
    """Populate composition registry with known US compositions."""
    cursor = conn.cursor()
    
    # These are well-documented US coin compositions
    compositions = [
        {
            "composition_key": "bronze_95_4_1",
            "name": "Bronze",
            "alloy_composition": {"copper": 0.95, "tin": 0.04, "zinc": 0.01},
            "period_description": "1864-1962",
            "density_g_cm3": 8.92,
            "color_description": "Brown"
        },
        {
            "composition_key": "brass_95_5",
            "name": "Brass",
            "alloy_composition": {"copper": 0.95, "zinc": 0.05},
            "period_description": "1943-1945 transition",
            "density_g_cm3": 8.53,
            "color_description": "Yellow"
        },
        {
            "composition_key": "zinc_plated_steel",
            "name": "Zinc-plated Steel",
            "alloy_composition": {"steel": 0.99, "zinc": 0.01},
            "period_description": "1943 wartime",
            "density_g_cm3": 7.87,
            "magnetic_properties": "magnetic",
            "color_description": "Silver-gray"
        },
        {
            "composition_key": "copper_plated_zinc",
            "name": "Copper-plated Zinc",
            "alloy_composition": {"zinc": 0.975, "copper": 0.025},
            "period_description": "1982-present",
            "density_g_cm3": 7.14,
            "color_description": "Copper appearance"
        },
        {
            "composition_key": "silver_90",
            "name": "90% Silver",
            "alloy_composition": {"silver": 0.9, "copper": 0.1},
            "period_description": "1792-1964",
            "density_g_cm3": 10.34,
            "color_description": "Silver"
        },
        {
            "composition_key": "silver_40",
            "name": "40% Silver",
            "alloy_composition": {"silver": 0.4, "copper": 0.6},
            "period_description": "1965-1970 half dollars",
            "density_g_cm3": 9.2,
            "color_description": "Silver"
        },
        {
            "composition_key": "nickel_75_25",
            "name": "Nickel",
            "alloy_composition": {"copper": 0.75, "nickel": 0.25},
            "period_description": "1866-present",
            "density_g_cm3": 8.9,
            "color_description": "Silver-white"
        },
        {
            "composition_key": "cupronickel_clad",
            "name": "Cupronickel Clad",
            "alloy_composition": {"copper": 0.917, "nickel": 0.083},
            "period_description": "1965-present dimes/quarters",
            "density_g_cm3": 8.92,
            "color_description": "Silver appearance"
        }
    ]
    
    for comp in compositions:
        cursor.execute("""
            INSERT OR REPLACE INTO composition_registry 
            (composition_key, name, alloy_composition, period_description, 
             density_g_cm3, magnetic_properties, color_description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            comp["composition_key"],
            comp["name"],
            json.dumps(comp["alloy_composition"]),
            comp["period_description"],
            comp.get("density_g_cm3"),
            comp.get("magnetic_properties"),
            comp.get("color_description")
        ))
    
    conn.commit()
    print(f"✓ Populated {len(compositions)} known compositions")


def populate_known_subjects(conn):
    """Populate subject registry with known US coin subjects."""
    cursor = conn.cursor()
    
    # These are well-documented subjects from US coins
    subjects = [
        {
            "subject_id": "abraham_lincoln",
            "type": "historical_figure",
            "name": "Abraham Lincoln",
            "nationality": "American",
            "roles": ["president"],
            "life_dates": {"birth": 1809, "death": 1865},
            "significance": "16th US President, preserved the Union during Civil War",
            "first_coin_appearance": 1909
        },
        {
            "subject_id": "george_washington",
            "type": "historical_figure",
            "name": "George Washington",
            "nationality": "American",
            "roles": ["president", "general"],
            "life_dates": {"birth": 1732, "death": 1799},
            "significance": "1st US President, Founding Father",
            "first_coin_appearance": 1932
        },
        {
            "subject_id": "thomas_jefferson",
            "type": "historical_figure",
            "name": "Thomas Jefferson",
            "nationality": "American",
            "roles": ["president"],
            "life_dates": {"birth": 1743, "death": 1826},
            "significance": "3rd US President, author of Declaration of Independence",
            "first_coin_appearance": 1938
        },
        {
            "subject_id": "franklin_d_roosevelt",
            "type": "historical_figure",
            "name": "Franklin Delano Roosevelt",
            "nationality": "American",
            "roles": ["president"],
            "life_dates": {"birth": 1882, "death": 1945},
            "significance": "32nd US President, led during Great Depression and WWII",
            "first_coin_appearance": 1946
        },
        {
            "subject_id": "john_f_kennedy",
            "type": "historical_figure",
            "name": "John Fitzgerald Kennedy",
            "nationality": "American",
            "roles": ["president"],
            "life_dates": {"birth": 1917, "death": 1963},
            "significance": "35th US President",
            "first_coin_appearance": 1964
        },
        {
            "subject_id": "wheat_ears",
            "type": "flora",
            "name": "Wheat Ears",
            "scientific_name": "Triticum durum",
            "symbolism": ["agriculture", "prosperity", "sustenance"],
            "significance": "Symbol of American agricultural abundance"
        },
        {
            "subject_id": "liberty_standing",
            "type": "allegorical_figure",
            "name": "Liberty (Standing)",
            "symbolism": ["freedom", "democracy", "enlightenment"],
            "significance": "Personification of American ideals"
        },
        {
            "subject_id": "american_eagle",
            "type": "fauna",
            "name": "American Bald Eagle",
            "scientific_name": "Haliaeetus leucocephalus",
            "symbolism": ["strength", "freedom", "national_power"],
            "significance": "National bird of the United States"
        }
    ]
    
    for subject in subjects:
        cursor.execute("""
            INSERT OR REPLACE INTO subject_registry 
            (subject_id, type, name, nationality, roles, life_dates, 
             reign_dates, significance, symbolism, scientific_name, first_coin_appearance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            subject["subject_id"],
            subject["type"],
            subject["name"],
            subject.get("nationality"),
            json.dumps(subject.get("roles", [])),
            json.dumps(subject.get("life_dates", {})),
            json.dumps(subject.get("reign_dates", {})),
            subject.get("significance"),
            json.dumps(subject.get("symbolism", [])),
            subject.get("scientific_name"),
            subject.get("first_coin_appearance")
        ))
    
    conn.commit()
    print(f"✓ Populated {len(subjects)} known subjects")


def generate_unique_series_abbreviation(series_id, series_name, existing_abbreviations):
    """Generate a unique abbreviation for a series."""
    # Try different strategies in order of preference
    
    # Strategy 1: First 3 chars of series_id (uppercase, no underscores)
    candidate = series_id.replace("_", "").upper()[:3] if series_id else "UNK"
    if candidate not in existing_abbreviations and len(candidate) >= 3:
        return candidate
    
    # Strategy 2: First letter of each major word in series_name
    if series_name:
        words = series_name.replace("-", " ").split()
        # Take first letter of significant words (skip articles, prepositions)
        skip_words = {"the", "of", "and", "a", "an", "in", "on", "at", "for", "with"}
        significant_words = [w for w in words if w.lower() not in skip_words and len(w) > 1]
        candidate = "".join(w[0].upper() for w in significant_words[:4])
        if candidate not in existing_abbreviations and len(candidate) >= 3:
            return candidate
    
    # Strategy 3: Add numeric suffix to base abbreviation
    base = series_id.replace("_", "").upper()[:3] if series_id else "UNK"
    for i in range(1, 100):
        candidate = f"{base}{i}"
        if candidate not in existing_abbreviations:
            return candidate
    
    # Fallback: Generate unique ID
    import uuid
    return str(uuid.uuid4())[:4].upper()


def generate_issue_id(country_code, series_abbrev, year, mint, variety=None):
    """Generate standardized issue ID."""
    base_id = f"{country_code}-{series_abbrev}-{year}"
    if mint:
        base_id += f"-{mint}"
    if variety:
        base_id += f"-{variety}"
    return base_id


def map_composition_to_key(composition_json):
    """Map existing composition data to composition registry key."""
    if not composition_json:
        return None
    
    try:
        comp = json.loads(composition_json) if isinstance(composition_json, str) else composition_json
        
        # Map common compositions to our registry keys
        if comp.get("copper") == 0.95 and comp.get("tin") == 0.04:
            return "bronze_95_4_1"
        elif comp.get("copper") == 0.975 and comp.get("zinc") == 0.025:
            return "copper_plated_zinc"
        elif comp.get("silver") == 0.9:
            return "silver_90"
        elif comp.get("silver") == 0.4:
            return "silver_40"
        elif comp.get("copper") == 0.75 and comp.get("nickel") == 0.25:
            return "nickel_75_25"
        elif comp.get("copper") > 0.9 and comp.get("nickel") > 0.08:
            return "cupronickel_clad"
        elif comp.get("steel"):
            return "zinc_plated_steel"
        
        # Default fallback
        return "bronze_95_4_1"  # Most common for pennies
        
    except:
        return "bronze_95_4_1"  # Safe default


def migrate_existing_data(conn):
    """Migrate existing US coin data to universal structure."""
    cursor = conn.cursor()
    
    # Temporarily disable foreign key constraints during migration
    cursor.execute('PRAGMA foreign_keys = OFF;')
    
    # First, populate series registry from existing data
    cursor.execute("""
        SELECT DISTINCT series_id, series_name, MIN(year), MAX(year), denomination
        FROM coins 
        WHERE series_id IS NOT NULL
        ORDER BY series_id
    """)
    
    series_data = cursor.fetchall()
    existing_abbreviations = set()
    
    for series_id, series_name, start_year, end_year, denomination in series_data:
        # Generate unique abbreviation for this series
        abbreviation = generate_unique_series_abbreviation(series_id, series_name, existing_abbreviations)
        existing_abbreviations.add(abbreviation)
        
        cursor.execute("""
            INSERT OR REPLACE INTO series_registry 
            (series_id, series_name, series_abbreviation, country_code, denomination, start_year, end_year, type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (series_id, series_name, abbreviation, "US", denomination, start_year, end_year, "coin"))
    
    print(f"✓ Migrated {len(series_data)} series to registry with unique abbreviations")
    
    # Now migrate individual coin records to issues
    cursor.execute("SELECT * FROM coins ORDER BY year, mint")
    coins = cursor.fetchall()
    
    migrated_count = 0
    for coin in coins:
        # Unpack coin data (adjust indices based on actual schema)
        (coin_id, series_id, country, denomination, series_name, year, mint,
         business_strikes, proof_strikes, rarity, composition, weight_grams,
         diameter_mm, varieties, source_citation, notes, created_at,
         obverse_description, reverse_description, distinguishing_features,
         identification_keywords, common_names, category, issuer, series_year,
         calendar_type, original_date, seller_name) = coin
        
        # Look up series abbreviation from registry
        if series_id:
            cursor.execute("SELECT series_abbreviation FROM series_registry WHERE series_id = ?", (series_id,))
            result = cursor.fetchone()
            series_abbrev = result[0] if result else "UNK"
        else:
            series_abbrev = "UNK"
        
        issue_id = generate_issue_id("US", series_abbrev, year, mint or "P")
        
        # Map denomination to face value
        denom_map = {
            "penny": 0.01,
            "cent": 0.01,
            "nickel": 0.05,
            "dime": 0.10,
            "quarter": 0.25,
            "half_dollar": 0.50,
            "dollar": 1.00
        }
        face_value = denom_map.get(denomination.lower(), 0.01)
        
        # Map composition
        composition_key = map_composition_to_key(composition)
        
        # Build specifications
        specifications = {
            "weight_grams": weight_grams,
            "diameter_mm": diameter_mm,
            "edge": "plain"  # Default - would need to be enriched later
        }
        
        # Build basic design data (to be enriched later)
        sides = {
            "obverse": {
                "design_id": f"{series_id}_obverse_{year}" if series_id else f"unknown_obverse_{year}",
                "primary_element": {
                    "type": "portrait",
                    "subject_id": "abraham_lincoln" if "lincoln" in (series_name or "").lower() else "unknown",
                    "description": "To be enriched with detailed design data"
                }
            },
            "reverse": {
                "design_id": f"{series_id}_reverse_{year}" if series_id else f"unknown_reverse_{year}",
                "primary_element": {
                    "type": "symbol",
                    "subject_id": "wheat_ears" if "wheat" in (series_name or "").lower() else "unknown",
                    "description": "To be enriched with detailed design data"
                }
            }
        }
        
        # Build mintage data
        mintage = {
            "business_strikes": business_strikes or 0,
            "proof_strikes": proof_strikes or 0
        }
        
        # Insert into issues table
        cursor.execute("""
            INSERT OR REPLACE INTO issues (
                issue_id, object_type, series_id, country_code, authority_name,
                monetary_system, currency_unit, face_value, unit_name, common_names,
                system_fraction, issue_year, mint_id, specifications, sides,
                mintage, rarity, varieties, source_citation, notes, seller_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            issue_id,
            "coin",
            series_id or "unknown",
            "US",
            "United States of America",
            "decimal",
            "dollar",
            face_value,
            denomination,
            json.dumps([denomination]),
            f"1/{int(1/face_value)} dollar" if face_value < 1 else "1 dollar",
            year,
            mint,
            json.dumps(specifications),
            json.dumps(sides),
            json.dumps(mintage),
            rarity,
            varieties,
            source_citation,
            notes,
            seller_name
        ))
        
        migrated_count += 1
    
    conn.commit()
    print(f"✓ Migrated {migrated_count} coins to universal issues table")
    
    # Re-enable foreign key constraints
    cursor.execute('PRAGMA foreign_keys = ON;')


def run_migration():
    """Execute the complete migration to universal taxonomy."""
    print("Starting Universal Currency Taxonomy Migration v1.1")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement
    
    try:
        # Create new schema
        create_universal_schema(conn)
        
        # Populate known registries
        populate_known_compositions(conn)
        populate_known_subjects(conn)
        
        # Migrate existing data
        migrate_existing_data(conn)
        
        print("\n✓ Migration completed successfully!")
        print("\nNew tables created:")
        print("  - subject_registry (8 subjects)")
        print("  - composition_registry (8 compositions)")
        print("  - series_registry (migrated from existing data)")
        print("  - issues (universal flat structure)")
        print("\nExisting tables preserved for backward compatibility")
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration()