#!/usr/bin/env python3
"""
Migration script to add coin_variants table for explicit variant tracking.
Issue #54: Add explicit coin variant tracking system to database

This table allows developers to easily query all variants for a specific coin type.
Starting with 2-cent pieces as the initial implementation.
"""

import sqlite3
import json
from datetime import datetime

def create_variants_table(conn):
    """Create the coin_variants table"""
    conn.executescript('''
        -- Create coin_variants table for explicit variant tracking
        CREATE TABLE IF NOT EXISTS coin_variants (
            variant_id TEXT PRIMARY KEY,
            base_type TEXT NOT NULL,
            denomination TEXT NOT NULL,
            series_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            mint_mark TEXT,
            variant_type TEXT NOT NULL,
            variant_description TEXT,
            
            -- Ordering and categorization
            sort_order INTEGER NOT NULL,
            is_major_variant BOOLEAN DEFAULT 0,
            
            -- Metadata
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- Constraints for ID format
            CHECK (variant_id GLOB 'US-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]-[A-Z]*'),
            CHECK (LENGTH(variant_id) - LENGTH(REPLACE(variant_id, '-', '')) >= 3)
        );
        
        -- Create indexes for efficient querying
        CREATE INDEX IF NOT EXISTS idx_variants_base_type ON coin_variants(base_type);
        CREATE INDEX IF NOT EXISTS idx_variants_year ON coin_variants(year);
        CREATE INDEX IF NOT EXISTS idx_variants_sort ON coin_variants(base_type, year, sort_order);
        CREATE INDEX IF NOT EXISTS idx_variants_denomination ON coin_variants(denomination);
    ''')

def populate_two_cent_variants(conn):
    """Populate variants for 2-cent pieces"""
    
    # 2-cent pieces were minted from 1864-1873 at Philadelphia only (no mint marks)
    # Major variants: 1864 Small Motto, 1864 Large Motto, regular business strikes, and proofs
    
    two_cent_variants = [
        # 1864 variants
        {
            'variant_id': 'US-TWOC-1864-P-SM',
            'base_type': 'TWO_CENT',
            'denomination': '2 cents',
            'series_name': 'Two Cent Piece',
            'year': 1864,
            'mint_mark': 'P',
            'variant_type': 'Small Motto',
            'variant_description': '1864 Two Cent Piece with Small Motto variety - "IN GOD WE TRUST" in smaller letters',
            'sort_order': 10,
            'is_major_variant': 1,
            'notes': 'Scarcer variety from early 1864 production'
        },
        {
            'variant_id': 'US-TWOC-1864-P-LM',
            'base_type': 'TWO_CENT',
            'denomination': '2 cents',
            'series_name': 'Two Cent Piece',
            'year': 1864,
            'mint_mark': 'P',
            'variant_type': 'Large Motto',
            'variant_description': '1864 Two Cent Piece with Large Motto variety - "IN GOD WE TRUST" in larger letters',
            'sort_order': 20,
            'is_major_variant': 1,
            'notes': 'More common variety from later 1864 production'
        },
        {
            'variant_id': 'US-TWOC-1864-P-PROOF',
            'base_type': 'TWO_CENT',
            'denomination': '2 cents',
            'series_name': 'Two Cent Piece',
            'year': 1864,
            'mint_mark': 'P',
            'variant_type': 'Proof',
            'variant_description': '1864 Two Cent Piece Proof strike',
            'sort_order': 30,
            'is_major_variant': 0,
            'notes': 'Special proof strike for collectors'
        }
    ]
    
    # Add regular business strikes and proofs for remaining years (1865-1873)
    for year in range(1865, 1874):
        # Business strike
        two_cent_variants.append({
            'variant_id': f'US-TWOC-{year}-P',
            'base_type': 'TWO_CENT',
            'denomination': '2 cents',
            'series_name': 'Two Cent Piece',
            'year': year,
            'mint_mark': 'P',
            'variant_type': 'Business Strike',
            'variant_description': f'{year} Two Cent Piece regular business strike',
            'sort_order': 10,
            'is_major_variant': 0,
            'notes': None
        })
        
        # Proof strike
        two_cent_variants.append({
            'variant_id': f'US-TWOC-{year}-P-PROOF',
            'base_type': 'TWO_CENT',
            'denomination': '2 cents',
            'series_name': 'Two Cent Piece',
            'year': year,
            'mint_mark': 'P',
            'variant_type': 'Proof',
            'variant_description': f'{year} Two Cent Piece Proof strike',
            'sort_order': 20,
            'is_major_variant': 0,
            'notes': 'Special proof strike for collectors'
        })
    
    # Insert all variants
    for variant in two_cent_variants:
        conn.execute('''
            INSERT OR REPLACE INTO coin_variants (
                variant_id, base_type, denomination, series_name, year, mint_mark,
                variant_type, variant_description, sort_order, is_major_variant, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            variant['variant_id'],
            variant['base_type'],
            variant['denomination'],
            variant['series_name'],
            variant['year'],
            variant['mint_mark'],
            variant['variant_type'],
            variant['variant_description'],
            variant['sort_order'],
            variant['is_major_variant'],
            variant['notes']
        ))

def verify_variants(conn):
    """Verify the variants were added correctly"""
    cursor = conn.cursor()
    
    # Count total variants
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "TWO_CENT"')
    total_count = cursor.fetchone()[0]
    
    # Count major variants
    cursor.execute('SELECT COUNT(*) FROM coin_variants WHERE base_type = "TWO_CENT" AND is_major_variant = 1')
    major_count = cursor.fetchone()[0]
    
    # Get years covered
    cursor.execute('SELECT MIN(year), MAX(year) FROM coin_variants WHERE base_type = "TWO_CENT"')
    min_year, max_year = cursor.fetchone()
    
    print(f"✅ Added {total_count} total Two Cent Piece variants")
    print(f"   - {major_count} major variants (1864 Small/Large Motto)")
    print(f"   - Years covered: {min_year}-{max_year}")
    
    # Show sample query result
    print("\n📊 Sample query - All 1864 variants:")
    cursor.execute('''
        SELECT variant_id, variant_type, variant_description
        FROM coin_variants
        WHERE base_type = "TWO_CENT" AND year = 1864
        ORDER BY sort_order
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]} - {row[2][:50]}...")

def main():
    """Run migration"""
    print("🔄 Running migration: Adding coin_variants table...")
    
    # Connect to database
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    try:
        # Create the variants table
        create_variants_table(conn)
        print("✅ Created coin_variants table")
        
        # Populate with Two Cent Piece data
        populate_two_cent_variants(conn)
        print("✅ Populated Two Cent Piece variants")
        
        # Verify the data
        verify_variants(conn)
        
        # Commit changes
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()