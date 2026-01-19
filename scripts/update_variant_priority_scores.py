#!/usr/bin/env python3
"""
Update priority scores for variant resolution
Issue #56: Set priority scores for ambiguous base variant resolution

This script assigns priority scores to base variants to handle cases where
multiple base variants exist for the same year + mint combination.
"""

import sqlite3

def update_priority_scores(conn):
    """Update priority scores for base variants"""
    cursor = conn.cursor()
    
    # Priority rules for specific coin types and years
    priority_updates = [
        # Two Cent Pieces - 1864
        # Large Motto is more common (produced later in year)
        ("UPDATE coin_variants SET priority_score = 70 WHERE variant_id = 'US-TWOC-1864-P-LM'", "1864 Two Cent Large Motto"),
        ("UPDATE coin_variants SET priority_score = 30 WHERE variant_id = 'US-TWOC-1864-P-SM'", "1864 Two Cent Small Motto"),
        
        # Buffalo Nickels - 1913
        # Type 2 is more common (produced for most of the year)
        ("UPDATE coin_variants SET priority_score = 70 WHERE base_type = 'BUFFALO_NICKEL' AND year = 1913 AND variant_type LIKE '%Type 2%'", "1913 Buffalo Type 2"),
        ("UPDATE coin_variants SET priority_score = 30 WHERE base_type = 'BUFFALO_NICKEL' AND year = 1913 AND variant_type LIKE '%Type 1%'", "1913 Buffalo Type 1"),
        
        # Standing Liberty Quarters - 1916-1917 (future)
        # Type 1 for 1916-early 1917, Type 2 for mid-1917 onwards
        ("UPDATE coin_variants SET priority_score = 70 WHERE base_type = 'STANDING_LIBERTY_QUARTER' AND year = 1916 AND variant_type LIKE '%Type 1%'", "1916 SLQ Type 1"),
        ("UPDATE coin_variants SET priority_score = 30 WHERE base_type = 'STANDING_LIBERTY_QUARTER' AND year = 1917 AND variant_type LIKE '%Type 1%'", "1917 SLQ Type 1"),
        ("UPDATE coin_variants SET priority_score = 70 WHERE base_type = 'STANDING_LIBERTY_QUARTER' AND year = 1917 AND variant_type LIKE '%Type 2%'", "1917 SLQ Type 2"),
        
        # Default scores for regular business strikes
        ("UPDATE coin_variants SET priority_score = 50 WHERE priority_score IS NULL AND variant_type LIKE '%Business Strike%'", "Default business strikes"),
        
        # Lower priority for proofs (less likely in general auctions)
        ("UPDATE coin_variants SET priority_score = 20 WHERE variant_type = 'Proof'", "All Proof coins"),
        
        # Higher priority for regular strikes vs special varieties
        ("UPDATE coin_variants SET priority_score = 60 WHERE is_base_variant = 1 AND parent_variant_id IS NULL AND priority_score IS NULL", "Base variants without special varieties"),
        
        # Lower priority for error coins and overdates
        ("UPDATE coin_variants SET priority_score = 25 WHERE variant_type LIKE '%Overdate%'", "Overdate varieties"),
        ("UPDATE coin_variants SET priority_score = 25 WHERE variant_type LIKE '%Three-Legged%'", "Three-legged varieties"),
        ("UPDATE coin_variants SET priority_score = 25 WHERE variant_type LIKE '%DDO%' OR variant_type LIKE '%DDR%'", "Doubled die varieties"),
    ]
    
    # Apply priority updates
    for query, description in priority_updates:
        cursor.execute(query)
        affected = cursor.rowcount
        if affected > 0:
            print(f"✅ Updated {affected} rows: {description}")
    
    # Set default priority for any remaining NULL values
    cursor.execute("UPDATE coin_variants SET priority_score = 50 WHERE priority_score IS NULL")
    affected = cursor.rowcount
    if affected > 0:
        print(f"✅ Set default priority (50) for {affected} remaining variants")

def add_priority_rules_table(conn):
    """Create a table to document priority rules"""
    cursor = conn.cursor()
    
    # Create priority rules documentation table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS variant_priority_rules (
            rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin_type TEXT NOT NULL,
            year_range_start INTEGER,
            year_range_end INTEGER,
            condition_description TEXT,
            priority_variant TEXT,
            priority_score INTEGER,
            rationale TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert documented priority rules
    rules = [
        ('TWO_CENT', 1864, 1864, 'Multiple motto sizes', 'Large Motto', 70, 
         'Large Motto is more common, produced for most of 1864'),
        
        ('TWO_CENT', 1864, 1864, 'Multiple motto sizes', 'Small Motto', 30,
         'Small Motto is scarcer, produced early in 1864'),
        
        ('BUFFALO_NICKEL', 1913, 1913, 'Type 1 vs Type 2', 'Type 2', 70,
         'Type 2 (Recessed ground) produced for most of year'),
        
        ('BUFFALO_NICKEL', 1913, 1913, 'Type 1 vs Type 2', 'Type 1', 30,
         'Type 1 (Raised ground) produced only early in year'),
        
        ('ALL', None, None, 'Proof vs Business', 'Business Strike', 50,
         'Business strikes more common in general marketplace'),
        
        ('ALL', None, None, 'Proof vs Business', 'Proof', 20,
         'Proof coins less common in general marketplace'),
        
        ('ALL', None, None, 'Regular vs Error', 'Regular Strike', 60,
         'Regular strikes without errors are most common'),
        
        ('ALL', None, None, 'Regular vs Error', 'Error/Variety', 25,
         'Error coins and special varieties are less common'),
    ]
    
    for rule in rules:
        cursor.execute("""
            INSERT OR IGNORE INTO variant_priority_rules 
            (coin_type, year_range_start, year_range_end, condition_description,
             priority_variant, priority_score, rationale)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rule)
    
    print("✅ Created variant_priority_rules documentation table")

def verify_priority_scores(conn):
    """Verify priority scores are properly set"""
    cursor = conn.cursor()
    
    print("\n📊 Priority Score Verification:")
    print("=" * 60)
    
    # Check for ambiguous cases (multiple base variants with same year/mint)
    cursor.execute("""
        SELECT base_type, year, mint_mark, COUNT(*) as variant_count,
               GROUP_CONCAT(variant_id || ' (' || priority_score || ')', ', ') as variants
        FROM coin_variants
        WHERE is_base_variant = 1
        GROUP BY base_type, year, mint_mark
        HAVING COUNT(*) > 1
        ORDER BY base_type, year
    """)
    
    ambiguous = cursor.fetchall()
    
    if ambiguous:
        print("\n⚠️  Ambiguous base variants (multiple per year/mint):")
        for row in ambiguous:
            print(f"\n{row[0]} {row[1]}-{row[2]}:")
            print(f"  Variants: {row[3]}")
            print(f"  Details: {row[4]}")
    else:
        print("✅ No ambiguous base variants found")
    
    # Show priority distribution
    cursor.execute("""
        SELECT priority_score, COUNT(*) as count
        FROM coin_variants
        WHERE is_base_variant = 1
        GROUP BY priority_score
        ORDER BY priority_score DESC
    """)
    
    print("\n📊 Priority Score Distribution (Base Variants):")
    for score, count in cursor.fetchall():
        print(f"  Score {score}: {count} variants")

def main():
    """Run priority score updates"""
    print("🔄 Updating variant priority scores...")
    
    conn = sqlite3.connect('database/coins.db')
    
    try:
        # Update priority scores
        update_priority_scores(conn)
        
        # Add documentation table
        add_priority_rules_table(conn)
        
        # Verify results
        verify_priority_scores(conn)
        
        conn.commit()
        print("\n✅ Priority scores updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()