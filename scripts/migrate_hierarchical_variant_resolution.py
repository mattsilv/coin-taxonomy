#!/usr/bin/env python3
"""
Migration Script: Implement Hierarchical Variant Resolution for Auction Mapping

This migration implements Issue #56 by:
1. Adding parent_variant_id and resolution_level columns to coin_variants table
2. Adding is_base_variant flag for base variants
3. Establishing parent-child relationships between variants
4. Creating auction_mapping view for easy queries
5. Implementing priority rules for ambiguous cases

Usage:
    python scripts/migrate_hierarchical_variant_resolution.py
    python scripts/migrate_hierarchical_variant_resolution.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class HierarchicalVariantResolutionMigration:
    def __init__(self, db_path='data/coins.db'):
        self.db_path = db_path
        self.backup_path = None
        
        # Define resolution levels
        self.LEVEL_BASE = 1  # Base variant (year + mint)
        self.LEVEL_MAJOR_VARIETY = 2  # Type 1/2, Small/Large Motto
        self.LEVEL_SPECIAL_VARIETY = 3  # Overdates, errors, DDO
        self.LEVEL_STRIKE_TYPE = 4  # Proof, Specimen, etc.
        
        # Define variant type to resolution level mapping
        self.variant_type_levels = {
            'Business Strike': self.LEVEL_BASE,
            'Type 1 - Business Strike': self.LEVEL_MAJOR_VARIETY,
            'Type 2 - Business Strike': self.LEVEL_MAJOR_VARIETY,
            'Small Motto': self.LEVEL_MAJOR_VARIETY,
            'Large Motto': self.LEVEL_MAJOR_VARIETY,
            'Small Date': self.LEVEL_MAJOR_VARIETY,
            'Large Date': self.LEVEL_MAJOR_VARIETY,
            'Proof': self.LEVEL_STRIKE_TYPE,
            'Specimen': self.LEVEL_STRIKE_TYPE,
            'Pattern': self.LEVEL_STRIKE_TYPE
        }
        
        # Priority rules for ambiguous base variant selection
        # Higher priority = default selection when multiple bases exist
        self.base_variant_priorities = {
            # 1864 Two Cent: Large Motto is more common
            ('TWO_CENT', 1864, 'Large Motto'): 100,
            ('TWO_CENT', 1864, 'Small Motto'): 50,
            
            # 1913 Buffalo Nickel: Type 2 is more common (later production)
            ('BUFFALO_NICKEL', 1913, 'Type 2'): 100,
            ('BUFFALO_NICKEL', 1913, 'Type 1'): 50
        }
        
    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = os.path.join(backup_dir, f'coins_backup_variant_hierarchy_{timestamp}.db')
        
        # Copy database
        import shutil
        shutil.copy2(self.db_path, self.backup_path)
        print(f"✅ Created backup at: {self.backup_path}")
        
        return self.backup_path
    
    def add_new_columns(self, conn: sqlite3.Connection):
        """Add parent_variant_id, resolution_level, and is_base_variant columns."""
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(coin_variants)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        # Add parent_variant_id column if not exists
        if 'parent_variant_id' not in existing_columns:
            cursor.execute("""
                ALTER TABLE coin_variants 
                ADD COLUMN parent_variant_id TEXT REFERENCES coin_variants(variant_id)
            """)
            print("✅ Added parent_variant_id column")
        
        # Add resolution_level column if not exists  
        if 'resolution_level' not in existing_columns:
            cursor.execute("""
                ALTER TABLE coin_variants 
                ADD COLUMN resolution_level INTEGER DEFAULT 1
            """)
            print("✅ Added resolution_level column")
        
        # Add is_base_variant column if not exists
        if 'is_base_variant' not in existing_columns:
            cursor.execute("""
                ALTER TABLE coin_variants 
                ADD COLUMN is_base_variant BOOLEAN DEFAULT 0
            """)
            print("✅ Added is_base_variant column")
        
        # Add priority_score column for base variant selection
        if 'priority_score' not in existing_columns:
            cursor.execute("""
                ALTER TABLE coin_variants
                ADD COLUMN priority_score INTEGER DEFAULT 50
            """)
            print("✅ Added priority_score column")
        
        # Create indexes for efficient lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_parent_variant 
            ON coin_variants(parent_variant_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_base_variants 
            ON coin_variants(is_base_variant)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_resolution_level
            ON coin_variants(resolution_level)
        """)
        
        print("✅ Created indexes for hierarchical lookups")
        
    def identify_base_variants(self, conn: sqlite3.Connection) -> List[str]:
        """Identify and mark base variants."""
        cursor = conn.cursor()
        base_variant_ids = []
        
        # Get all variants
        cursor.execute("""
            SELECT variant_id, base_type, year, mint_mark, variant_type, variant_description
            FROM coin_variants
            ORDER BY variant_id
        """)
        variants = cursor.fetchall()
        
        for variant_id, base_type, year, mint_mark, variant_type, variant_description in variants:
            # Check if this is a base variant
            is_base = False
            
            # Check for basic business strikes or Type 2 (default type)
            if any(x in variant_type for x in ['Business Strike', 'Type 2']):
                # Check if it's NOT a special variety (no overdate, DDO, etc.)
                if not any(x in (variant_id + variant_type + (variant_description or '')).upper() 
                          for x in ['OVER', 'DDO', 'DDR', 'RPM', 'ERROR', 'VAM', 'FS-']):
                    is_base = True
            
            # Special case for Two Cent Large/Small Motto
            if base_type == 'TWO_CENT' and any(x in variant_type for x in ['Large Motto', 'Small Motto']):
                is_base = True
            
            # Special case for Buffalo Nickel Type 1
            if base_type == 'BUFFALO_NICKEL' and 'Type 1' in variant_type:
                is_base = True
            
            if is_base:
                base_variant_ids.append(variant_id)
                cursor.execute("""
                    UPDATE coin_variants 
                    SET is_base_variant = 1
                    WHERE variant_id = ?
                """, (variant_id,))
        
        print(f"✅ Identified {len(base_variant_ids)} base variants")
        return base_variant_ids
        
    def set_resolution_levels(self, conn: sqlite3.Connection):
        """Set resolution levels based on variant types."""
        cursor = conn.cursor()
        
        # Get all variants
        cursor.execute("SELECT variant_id, variant_type FROM coin_variants")
        variants = cursor.fetchall()
        
        for variant_id, variant_type in variants:
            # Determine resolution level
            level = self.LEVEL_BASE  # Default
            
            # Check for special varieties (overdates, errors, etc.)
            if any(x in variant_id.upper() for x in ['8OVER7', 'DDO', 'DDR', 'RPM', 'ERROR']):
                level = self.LEVEL_SPECIAL_VARIETY
            # Check for proof/pattern strikes
            elif any(x in variant_type for x in ['Proof', 'Pattern', 'Specimen']):
                level = self.LEVEL_STRIKE_TYPE
            # Check for major varieties (Type 1/2, Large/Small Motto)
            elif any(x in variant_type for x in ['Type 1', 'Type 2', 'Small Motto', 'Large Motto', 'Small Date', 'Large Date']):
                level = self.LEVEL_MAJOR_VARIETY
            
            cursor.execute("""
                UPDATE coin_variants 
                SET resolution_level = ?
                WHERE variant_id = ?
            """, (level, variant_id))
        
        print("✅ Set resolution levels for all variants")
        
    def establish_parent_relationships(self, conn: sqlite3.Connection):
        """Establish parent-child relationships between variants."""
        cursor = conn.cursor()
        relationships_created = 0
        
        # Get all non-base variants
        cursor.execute("""
            SELECT variant_id, base_type, year, mint_mark, variant_type, resolution_level
            FROM coin_variants
            WHERE is_base_variant = 0
            ORDER BY variant_id
        """)
        non_base_variants = cursor.fetchall()
        
        for variant_id, base_type, year, mint_mark, variant_type, resolution_level in non_base_variants:
            # Find potential parent variant
            parent_id = None
            
            # Special varieties should link to their base variant
            if resolution_level == self.LEVEL_SPECIAL_VARIETY:
                # For 1918-D 8/7 overdate, parent should be US-BUFF-1918-D
                if '8OVER7' in variant_id:
                    parent_id = variant_id.replace('-8OVER7', '')
                    
            # Proof strikes should link to their base variant
            elif resolution_level == self.LEVEL_STRIKE_TYPE:
                if variant_type == 'Proof':
                    # For 1864 Two Cent Proof, determine parent based on existing Large Motto variant
                    if base_type == 'TWO_CENT' and year == 1864:
                        parent_id = 'US-TWOC-1864-P-LM'  # Default to Large Motto
                    else:
                        # Remove -PROOF suffix to find parent
                        parent_id = variant_id.replace('-PROOF', '')
            
            # Major varieties (Type 1/2, Motto variants) should link to conceptual base
            elif resolution_level == self.LEVEL_MAJOR_VARIETY:
                # These ARE base variants themselves, no parent needed
                parent_id = None
            
            if parent_id:
                # Verify parent exists
                cursor.execute("SELECT COUNT(*) FROM coin_variants WHERE variant_id = ?", (parent_id,))
                if cursor.fetchone()[0] > 0:
                    cursor.execute("""
                        UPDATE coin_variants 
                        SET parent_variant_id = ?
                        WHERE variant_id = ?
                    """, (parent_id, variant_id))
                    relationships_created += 1
                else:
                    print(f"⚠️  Warning: Parent variant {parent_id} not found for {variant_id}")
        
        print(f"✅ Established {relationships_created} parent-child relationships")
        
    def set_priority_scores(self, conn: sqlite3.Connection):
        """Set priority scores for base variant selection."""
        cursor = conn.cursor()
        
        for (base_type, year, variant_type), priority in self.base_variant_priorities.items():
            cursor.execute("""
                UPDATE coin_variants
                SET priority_score = ?
                WHERE base_type = ? AND year = ? AND variant_type LIKE ?
            """, (priority, base_type, year, f'%{variant_type}%'))
        
        print("✅ Set priority scores for ambiguous base variant resolution")
        
    def create_auction_mapping_view(self, conn: sqlite3.Connection):
        """Create view for simplified auction mapping queries."""
        cursor = conn.cursor()
        
        # Drop existing view if it exists
        cursor.execute("DROP VIEW IF EXISTS auction_mapping")
        
        # Create comprehensive auction mapping view
        cursor.execute("""
            CREATE VIEW auction_mapping AS
            SELECT 
                cv.variant_id,
                cv.base_type,
                cv.denomination,
                cv.series_name,
                cv.year,
                cv.mint_mark,
                cv.variant_type,
                cv.variant_description,
                cv.resolution_level,
                cv.is_base_variant,
                cv.priority_score,
                cv.parent_variant_id,
                -- Get base variant ID (either self if base, or parent)
                COALESCE(
                    CASE 
                        WHEN cv.is_base_variant = 1 THEN cv.variant_id
                        ELSE cv.parent_variant_id
                    END,
                    cv.variant_id
                ) as base_variant_id,
                -- Count of child variants
                (SELECT COUNT(*) FROM coin_variants cv2 
                 WHERE cv2.parent_variant_id = cv.variant_id) as child_variant_count
            FROM coin_variants cv
            ORDER BY cv.base_type, cv.year, cv.mint_mark, cv.priority_score DESC
        """)
        
        print("✅ Created auction_mapping view for easy queries")
        
    def create_resolution_functions(self, conn: sqlite3.Connection):
        """Create stored procedures for variant resolution (as a Python script)."""
        
        # Create a Python module for resolution functions
        resolution_module = '''#!/usr/bin/env python3
"""
Variant Resolution Functions for Auction Mapping

This module provides functions to map auction listings to the correct coin variant.
"""

import sqlite3
from typing import Optional, List, Dict, Tuple

class VariantResolver:
    def __init__(self, db_path='data/coins.db'):
        self.db_path = db_path
        
    def map_auction_to_variant(self, year: int, mint_mark: str, coin_type: str, 
                               additional_info: Optional[str] = None) -> Optional[str]:
        """
        Map auction listing to most specific variant possible.
        
        Args:
            year: Coin year
            mint_mark: Mint mark (P, D, S, CC, etc.)
            coin_type: Coin type/series (e.g., BUFFALO_NICKEL, TWO_CENT)
            additional_info: Additional variety info (e.g., "8/7", "Small Motto")
            
        Returns:
            variant_id of the best match, or None if no match found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # First try to find exact match with additional info
            if additional_info:
                # Check for special varieties
                special_keywords = {
                    '8/7': '8OVER7',
                    '8 over 7': '8OVER7',
                    'overdate': 'OVER',
                    'DDO': 'DDO',
                    'DDR': 'DDR',
                    'Small Motto': 'SM',
                    'Large Motto': 'LM',
                    'Type 1': 'Type 1',
                    'Type 2': 'Type 2',
                    'Proof': 'PROOF'
                }
                
                for keyword, variant_suffix in special_keywords.items():
                    if keyword.lower() in additional_info.lower():
                        # Try to find variant with this suffix
                        cursor.execute("""
                            SELECT variant_id FROM auction_mapping
                            WHERE base_type = ? AND year = ? AND mint_mark = ?
                            AND (variant_id LIKE ? OR variant_type LIKE ? OR variant_description LIKE ?)
                            ORDER BY resolution_level DESC
                            LIMIT 1
                        """, (coin_type, year, mint_mark, 
                              f'%{variant_suffix}%', f'%{keyword}%', f'%{keyword}%'))
                        
                        result = cursor.fetchone()
                        if result:
                            return result[0]
            
            # Fall back to base variant
            cursor.execute("""
                SELECT variant_id FROM auction_mapping
                WHERE base_type = ? AND year = ? AND mint_mark = ?
                AND is_base_variant = 1
                ORDER BY priority_score DESC
                LIMIT 1
            """, (coin_type, year, mint_mark))
            
            result = cursor.fetchone()
            return result[0] if result else None
            
    def get_variant_hierarchy(self, variant_id: str) -> Dict:
        """
        Get complete hierarchy for a variant.
        
        Returns dict with variant info and all related variants.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get variant info
            cursor.execute("""
                SELECT * FROM auction_mapping
                WHERE variant_id = ?
            """, (variant_id,))
            
            variant = cursor.fetchone()
            if not variant:
                return {}
            
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            variant_dict = dict(zip(columns, variant))
            
            # Get parent if exists
            if variant_dict.get('parent_variant_id'):
                cursor.execute("""
                    SELECT variant_id, variant_type, variant_description
                    FROM coin_variants
                    WHERE variant_id = ?
                """, (variant_dict['parent_variant_id'],))
                parent = cursor.fetchone()
                if parent:
                    variant_dict['parent'] = {
                        'variant_id': parent[0],
                        'variant_type': parent[1],
                        'variant_description': parent[2]
                    }
            
            # Get children if any
            cursor.execute("""
                SELECT variant_id, variant_type, variant_description, resolution_level
                FROM coin_variants
                WHERE parent_variant_id = ?
                ORDER BY resolution_level, variant_id
            """, (variant_id,))
            
            children = cursor.fetchall()
            if children:
                variant_dict['children'] = [
                    {
                        'variant_id': child[0],
                        'variant_type': child[1],
                        'variant_description': child[2],
                        'resolution_level': child[3]
                    }
                    for child in children
                ]
            
            return variant_dict
            
    def resolve_ambiguous_base(self, year: int, mint_mark: str, coin_type: str) -> Optional[str]:
        """
        Resolve ambiguous base variants using priority rules.
        
        When multiple base variants exist for year+mint, uses priority scores.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT variant_id, variant_type, priority_score
                FROM auction_mapping
                WHERE base_type = ? AND year = ? AND mint_mark = ?
                AND is_base_variant = 1
                ORDER BY priority_score DESC
            """, (coin_type, year, mint_mark))
            
            results = cursor.fetchall()
            
            if not results:
                return None
            elif len(results) == 1:
                return results[0][0]
            else:
                # Multiple bases - use highest priority
                print(f"Multiple base variants for {coin_type} {year}-{mint_mark}:")
                for variant_id, variant_type, priority in results:
                    print(f"  - {variant_id}: {variant_type} (priority: {priority})")
                print(f"Selected: {results[0][0]} (highest priority)")
                return results[0][0]

# Command-line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Resolve coin variants for auction mapping')
    parser.add_argument('--year', type=int, help='Coin year')
    parser.add_argument('--mint', default='P', help='Mint mark (default: P)')
    parser.add_argument('--type', required=True, help='Coin type (e.g., BUFFALO_NICKEL, TWO_CENT)')
    parser.add_argument('--info', help='Additional variety info')
    parser.add_argument('--hierarchy', help='Show hierarchy for variant ID')
    
    args = parser.parse_args()
    
    resolver = VariantResolver()
    
    if args.hierarchy:
        hierarchy = resolver.get_variant_hierarchy(args.hierarchy)
        print(json.dumps(hierarchy, indent=2))
    else:
        variant_id = resolver.map_auction_to_variant(
            args.year, args.mint, args.type, args.info
        )
        if variant_id:
            print(f"Matched variant: {variant_id}")
            hierarchy = resolver.get_variant_hierarchy(variant_id)
            print(f"Type: {hierarchy.get('variant_type')}")
            print(f"Description: {hierarchy.get('variant_description')}")
        else:
            print("No matching variant found")
'''
        
        # Write resolution module
        with open('scripts/variant_resolver.py', 'w') as f:
            f.write(resolution_module)
        
        print("✅ Created variant_resolver.py module for resolution functions")
        
    def verify_migration(self, conn: sqlite3.Connection):
        """Verify migration was successful."""
        cursor = conn.cursor()
        
        # Check new columns exist
        cursor.execute("PRAGMA table_info(coin_variants)")
        columns = [col[1] for col in cursor.fetchall()]
        required_columns = ['parent_variant_id', 'resolution_level', 'is_base_variant', 'priority_score']
        
        for col in required_columns:
            if col not in columns:
                raise Exception(f"Missing required column: {col}")
        
        # Check base variants
        cursor.execute("SELECT COUNT(*) FROM coin_variants WHERE is_base_variant = 1")
        base_count = cursor.fetchone()[0]
        print(f"✅ Verification: {base_count} base variants marked")
        
        # Check parent relationships
        cursor.execute("SELECT COUNT(*) FROM coin_variants WHERE parent_variant_id IS NOT NULL")
        parent_count = cursor.fetchone()[0]
        print(f"✅ Verification: {parent_count} parent relationships established")
        
        # Check auction_mapping view
        cursor.execute("SELECT COUNT(*) FROM auction_mapping")
        mapping_count = cursor.fetchone()[0]
        print(f"✅ Verification: auction_mapping view has {mapping_count} rows")
        
        # Test cases
        print("\n📋 Testing variant resolution:")
        
        # Test 1: Buffalo Nickel 1918-D with overdate
        cursor.execute("""
            SELECT variant_id, variant_type, parent_variant_id, is_base_variant
            FROM coin_variants
            WHERE base_type = 'BUFFALO_NICKEL' AND year = 1918 AND mint_mark = 'D'
            ORDER BY variant_id
        """)
        results = cursor.fetchall()
        for row in results:
            print(f"  {row[0]}: {row[1]} (parent: {row[2]}, base: {row[3]})")
        
        # Test 2: Two Cent 1864 hierarchy
        cursor.execute("""
            SELECT variant_id, variant_type, parent_variant_id, is_base_variant
            FROM coin_variants
            WHERE base_type = 'TWO_CENT' AND year = 1864
            ORDER BY variant_id
        """)
        results = cursor.fetchall()
        for row in results:
            print(f"  {row[0]}: {row[1]} (parent: {row[2]}, base: {row[3]})")
        
        print("\n✅ Migration verification complete")
        
    def migrate(self, dry_run=False):
        """Execute the migration."""
        print(f"\n{'='*60}")
        print("Hierarchical Variant Resolution Migration")
        print(f"{'='*60}\n")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No changes will be saved\n")
        
        # Create backup
        if not dry_run:
            self.create_backup()
        
        # Connect to database
        conn = sqlite3.connect(self.db_path if not dry_run else ':memory:')
        
        try:
            if dry_run:
                # Copy data to memory for dry run
                source_conn = sqlite3.connect(self.db_path)
                source_conn.backup(conn)
                source_conn.close()
            
            # Execute migration steps
            print("\n📊 Starting migration...")
            
            # 1. Add new columns
            self.add_new_columns(conn)
            
            # 2. Identify and mark base variants
            self.identify_base_variants(conn)
            
            # 3. Set resolution levels
            self.set_resolution_levels(conn)
            
            # 4. Establish parent relationships
            self.establish_parent_relationships(conn)
            
            # 5. Set priority scores
            self.set_priority_scores(conn)
            
            # 6. Create auction mapping view
            self.create_auction_mapping_view(conn)
            
            # 7. Create resolution functions
            self.create_resolution_functions(conn)
            
            # 8. Verify migration
            self.verify_migration(conn)
            
            if not dry_run:
                conn.commit()
                print("\n✅ Migration completed successfully!")
                print(f"Backup saved at: {self.backup_path}")
            else:
                print("\n✅ Dry run completed successfully!")
                print("Run without --dry-run to apply changes")
                
        except Exception as e:
            conn.rollback()
            print(f"\n❌ Migration failed: {e}")
            if not dry_run and self.backup_path:
                print(f"Database unchanged. Backup available at: {self.backup_path}")
            raise
        finally:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='Migrate database for hierarchical variant resolution')
    parser.add_argument('--dry-run', action='store_true', help='Test migration without saving changes')
    parser.add_argument('--db-path', default='data/coins.db', help='Path to database file')
    
    args = parser.parse_args()
    
    migration = HierarchicalVariantResolutionMigration(db_path=args.db_path)
    migration.migrate(dry_run=args.dry_run)

if __name__ == "__main__":
    main()