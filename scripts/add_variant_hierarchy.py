#!/usr/bin/env python3
"""
Add hierarchical parent-child relationships to coin_variants table.
This allows special varieties to resolve back to their base variant for auction mapping.

For example:
- "1918-D 8/7" resolves to → "1918-D" (base variant)
- "1937-D Three-Legged" resolves to → "1937-D" (base variant)
"""

import sqlite3

def add_parent_variant_column(conn):
    """Add parent_variant_id column to establish hierarchy"""
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(coin_variants)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'parent_variant_id' not in columns:
        cursor.execute('''
            ALTER TABLE coin_variants 
            ADD COLUMN parent_variant_id TEXT 
            REFERENCES coin_variants(variant_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_parent_variant 
            ON coin_variants(parent_variant_id)
        ''')
        print("✅ Added parent_variant_id column")
    else:
        print("ℹ️  parent_variant_id column already exists")

def update_variant_relationships(conn):
    """Update parent relationships for special varieties"""
    cursor = conn.cursor()
    
    # Map special varieties to their base variants
    relationships = [
        # Buffalo Nickel overdates/errors to base variants
        ('US-BUFF-1914-P-4OVER3', 'US-BUFF-1914-P'),
        ('US-BUFF-1918-D-8OVER7', 'US-BUFF-1918-D'),
        ('US-BUFF-1937-D-3LEG', 'US-BUFF-1937-D'),
        
        # Two Cent Piece proofs to business strikes
        ('US-TWOC-1864-P-PROOF', 'US-TWOC-1864-P-LM'),  # Proof to Large Motto (more common)
        ('US-TWOC-1865-P-PROOF', 'US-TWOC-1865-P'),
        ('US-TWOC-1866-P-PROOF', 'US-TWOC-1866-P'),
        ('US-TWOC-1867-P-PROOF', 'US-TWOC-1867-P'),
        ('US-TWOC-1868-P-PROOF', 'US-TWOC-1868-P'),
        ('US-TWOC-1869-P-PROOF', 'US-TWOC-1869-P'),
        ('US-TWOC-1870-P-PROOF', 'US-TWOC-1870-P'),
        ('US-TWOC-1871-P-PROOF', 'US-TWOC-1871-P'),
        ('US-TWOC-1872-P-PROOF', 'US-TWOC-1872-P'),
        ('US-TWOC-1873-P-PROOF', 'US-TWOC-1873-P'),
    ]
    
    for child_id, parent_id in relationships:
        cursor.execute('''
            UPDATE coin_variants 
            SET parent_variant_id = ? 
            WHERE variant_id = ?
        ''', (parent_id, child_id))
    
    print(f"✅ Updated {len(relationships)} parent-child relationships")

def add_resolution_level_column(conn):
    """Add resolution_level to indicate specificity"""
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(coin_variants)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'resolution_level' not in columns:
        cursor.execute('''
            ALTER TABLE coin_variants 
            ADD COLUMN resolution_level INTEGER DEFAULT 1
        ''')
        print("✅ Added resolution_level column")
    else:
        print("ℹ️  resolution_level column already exists")
    
    # Update resolution levels
    # Level 1: Base variant (year + mint)
    # Level 2: Major variety (Type 1/2, Small/Large Motto)
    # Level 3: Special variety (overdates, errors)
    # Level 4: Proof/special strikes
    
    cursor.execute('''
        UPDATE coin_variants 
        SET resolution_level = CASE
            WHEN variant_type LIKE '%Business Strike%' AND parent_variant_id IS NULL THEN 1
            WHEN variant_type IN ('Type 1 - Raised Ground', 'Type 2 - Recessed', 'Small Motto', 'Large Motto') THEN 2
            WHEN variant_type LIKE '%Overdate%' OR variant_type LIKE '%Three-Legged%' THEN 3
            WHEN variant_type = 'Proof' THEN 4
            ELSE 1
        END
    ''')
    print("✅ Updated resolution levels")

def create_auction_mapping_view(conn):
    """Create a view for easy auction mapping"""
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS auction_mapping AS
        SELECT 
            v1.variant_id,
            v1.base_type,
            v1.year,
            v1.mint_mark,
            v1.variant_type,
            v1.resolution_level,
            v1.parent_variant_id,
            COALESCE(v1.parent_variant_id, v1.variant_id) as base_variant_id,
            v2.variant_type as base_variant_type
        FROM coin_variants v1
        LEFT JOIN coin_variants v2 ON COALESCE(v1.parent_variant_id, v1.variant_id) = v2.variant_id
        ORDER BY v1.base_type, v1.year, v1.mint_mark, v1.resolution_level
    ''')
    print("✅ Created auction_mapping view")

def demonstrate_resolution(conn):
    """Show how variants resolve to base"""
    cursor = conn.cursor()
    
    print("\n📊 Variant Resolution Examples:")
    print("=" * 60)
    
    # Example 1: 1918-D Buffalo variants
    print("\n1918-D Buffalo Nickel variants:")
    cursor.execute('''
        SELECT variant_id, variant_type, parent_variant_id, resolution_level
        FROM coin_variants
        WHERE base_type = 'BUFFALO_NICKEL' AND year = 1918 AND mint_mark = 'D'
        ORDER BY resolution_level
    ''')
    for row in cursor.fetchall():
        parent = f" → {row[2]}" if row[2] else " (BASE)"
        print(f"  Level {row[3]}: {row[0]} ({row[1]}){parent}")
    
    # Example 2: 1864 Two Cent variants
    print("\n1864 Two Cent Piece variants:")
    cursor.execute('''
        SELECT variant_id, variant_type, parent_variant_id, resolution_level
        FROM coin_variants
        WHERE base_type = 'TWO_CENT' AND year = 1864
        ORDER BY resolution_level, sort_order
    ''')
    for row in cursor.fetchall():
        parent = f" → {row[2]}" if row[2] else " (BASE)"
        print(f"  Level {row[3]}: {row[0]} ({row[1]}){parent}")

def main():
    """Run migration to add hierarchical relationships"""
    print("🔄 Adding hierarchical variant relationships...")
    
    conn = sqlite3.connect('data/coins.db')
    
    try:
        # Add parent column
        add_parent_variant_column(conn)
        
        # Add resolution level
        add_resolution_level_column(conn)
        
        # Update relationships
        update_variant_relationships(conn)
        
        # Create mapping view
        create_auction_mapping_view(conn)
        
        # Demonstrate
        demonstrate_resolution(conn)
        
        conn.commit()
        print("\n✅ Hierarchical relationships added successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()