#!/usr/bin/env python3
"""
Unit tests for hierarchical variant resolution system.
"""

import unittest
import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.variant_resolver import VariantResolver

class TestHierarchicalVariantResolution(unittest.TestCase):
    """Test cases for hierarchical variant resolution."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class with database connection."""
        cls.db_path = 'database/coins.db'
        cls.resolver = VariantResolver(db_path=cls.db_path)
    
    def test_database_schema(self):
        """Test that required columns exist in coin_variants table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(coin_variants)")
            columns = [col[1] for col in cursor.fetchall()]
            
            required_columns = ['parent_variant_id', 'resolution_level', 'is_base_variant', 'priority_score']
            for col in required_columns:
                self.assertIn(col, columns, f"Column {col} missing from coin_variants table")
    
    def test_auction_mapping_view(self):
        """Test that auction_mapping view exists and works."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM auction_mapping")
            count = cursor.fetchone()[0]
            self.assertGreater(count, 0, "auction_mapping view should have data")
    
    def test_base_variant_identification(self):
        """Test that base variants are properly identified."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check Buffalo Nickel 1918-D base
            cursor.execute("""
                SELECT is_base_variant FROM coin_variants
                WHERE variant_id = 'US-BUFF-1918-D'
            """)
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 1, "US-BUFF-1918-D should be a base variant")
            
            # Check Buffalo Nickel 1918-D 8/7 is NOT base
            cursor.execute("""
                SELECT is_base_variant FROM coin_variants
                WHERE variant_id = 'US-BUFF-1918-D-8OVER7'
            """)
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 0, "US-BUFF-1918-D-8OVER7 should NOT be a base variant")
    
    def test_parent_relationships(self):
        """Test parent-child relationships between variants."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Test Buffalo Nickel overdate parent
            cursor.execute("""
                SELECT parent_variant_id FROM coin_variants
                WHERE variant_id = 'US-BUFF-1918-D-8OVER7'
            """)
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 'US-BUFF-1918-D', "8/7 overdate should have base as parent")
            
            # Test Two Cent Proof parent
            cursor.execute("""
                SELECT parent_variant_id FROM coin_variants
                WHERE variant_id = 'US-TWOC-1864-P-PROOF'
            """)
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 'US-TWOC-1864-P-LM', "Proof should have Large Motto as parent")
    
    def test_resolution_levels(self):
        """Test that resolution levels are correctly assigned."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Base variant should be level 1 or 2 (major variety)
            cursor.execute("""
                SELECT resolution_level FROM coin_variants
                WHERE variant_id = 'US-BUFF-1918-D'
            """)
            level = cursor.fetchone()[0]
            self.assertIn(level, [1, 2], "Base variant should be level 1 or 2")
            
            # Special variety should be level 3
            cursor.execute("""
                SELECT resolution_level FROM coin_variants
                WHERE variant_id = 'US-BUFF-1918-D-8OVER7'
            """)
            level = cursor.fetchone()[0]
            self.assertEqual(level, 3, "Overdate should be level 3")
            
            # Proof should be level 4
            cursor.execute("""
                SELECT resolution_level FROM coin_variants
                WHERE variant_id = 'US-TWOC-1864-P-PROOF'
            """)
            level = cursor.fetchone()[0]
            self.assertEqual(level, 4, "Proof should be level 4")
    
    def test_priority_scores(self):
        """Test priority scores for ambiguous base variant resolution."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Test Two Cent 1864 priority scores
            cursor.execute("""
                SELECT variant_id, priority_score FROM coin_variants
                WHERE base_type = 'TWO_CENT' AND year = 1864 
                AND is_base_variant = 1
                ORDER BY priority_score DESC
            """)
            results = cursor.fetchall()
            
            # Large Motto should have higher priority than Small Motto
            lm_priority = next((score for vid, score in results if 'LM' in vid), None)
            sm_priority = next((score for vid, score in results if 'SM' in vid), None)
            
            if lm_priority and sm_priority:
                self.assertGreater(lm_priority, sm_priority, 
                                 "Large Motto should have higher priority than Small Motto")
    
    def test_auction_mapping_basic(self):
        """Test basic auction mapping without variety info."""
        # Test Buffalo Nickel 1918-D (no variety specified)
        variant_id = self.resolver.map_auction_to_variant(1918, 'D', 'BUFFALO_NICKEL')
        self.assertEqual(variant_id, 'US-BUFF-1918-D', 
                        "Should map to base variant when no variety specified")
        
        # Test Two Cent 1864 (should default to Large Motto)
        variant_id = self.resolver.map_auction_to_variant(1864, 'P', 'TWO_CENT')
        self.assertEqual(variant_id, 'US-TWOC-1864-P-LM',
                        "Should default to Large Motto for 1864 Two Cent")
    
    def test_auction_mapping_with_variety(self):
        """Test auction mapping with variety information."""
        # Test Buffalo Nickel 1918-D with overdate
        variant_id = self.resolver.map_auction_to_variant(1918, 'D', 'BUFFALO_NICKEL', '8/7')
        self.assertEqual(variant_id, 'US-BUFF-1918-D-8OVER7',
                        "Should map to overdate variant when specified")
        
        # Test with different format
        variant_id = self.resolver.map_auction_to_variant(1918, 'D', 'BUFFALO_NICKEL', '8 over 7')
        self.assertEqual(variant_id, 'US-BUFF-1918-D-8OVER7',
                        "Should handle '8 over 7' format")
        
        # Test Two Cent Small Motto
        variant_id = self.resolver.map_auction_to_variant(1864, 'P', 'TWO_CENT', 'Small Motto')
        self.assertEqual(variant_id, 'US-TWOC-1864-P-SM',
                        "Should map to Small Motto when specified")
        
        # Test Two Cent Proof
        variant_id = self.resolver.map_auction_to_variant(1864, 'P', 'TWO_CENT', 'Proof')
        self.assertEqual(variant_id, 'US-TWOC-1864-P-PROOF',
                        "Should map to Proof when specified")
    
    def test_variant_hierarchy(self):
        """Test getting complete variant hierarchy."""
        # Test overdate hierarchy
        hierarchy = self.resolver.get_variant_hierarchy('US-BUFF-1918-D-8OVER7')
        self.assertIsNotNone(hierarchy)
        self.assertEqual(hierarchy['variant_id'], 'US-BUFF-1918-D-8OVER7')
        self.assertIn('parent', hierarchy)
        self.assertEqual(hierarchy['parent']['variant_id'], 'US-BUFF-1918-D')
        
        # Test base variant hierarchy (should have children)
        hierarchy = self.resolver.get_variant_hierarchy('US-BUFF-1918-D')
        self.assertIsNotNone(hierarchy)
        self.assertEqual(hierarchy['variant_id'], 'US-BUFF-1918-D')
        self.assertIn('children', hierarchy)
        child_ids = [child['variant_id'] for child in hierarchy['children']]
        self.assertIn('US-BUFF-1918-D-8OVER7', child_ids)
    
    def test_resolve_ambiguous_base(self):
        """Test resolution of ambiguous base variants."""
        # Test Two Cent 1864 (multiple bases)
        variant_id = self.resolver.resolve_ambiguous_base(1864, 'P', 'TWO_CENT')
        self.assertEqual(variant_id, 'US-TWOC-1864-P-LM',
                        "Should resolve to Large Motto by priority")
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        # Test non-existent coin
        variant_id = self.resolver.map_auction_to_variant(1999, 'D', 'BUFFALO_NICKEL')
        self.assertIsNone(variant_id, "Should return None for non-existent variant")
        
        # Test invalid mint mark
        variant_id = self.resolver.map_auction_to_variant(1918, 'Z', 'BUFFALO_NICKEL')
        self.assertIsNone(variant_id, "Should return None for invalid mint mark")
        
        # Test empty variant hierarchy
        hierarchy = self.resolver.get_variant_hierarchy('INVALID-ID')
        self.assertEqual(hierarchy, {}, "Should return empty dict for invalid variant")
    
    def test_performance(self):
        """Test query performance."""
        import time
        
        # Test variant resolution performance
        start = time.time()
        for _ in range(100):
            self.resolver.map_auction_to_variant(1918, 'D', 'BUFFALO_NICKEL')
        elapsed = time.time() - start
        avg_time = elapsed / 100 * 1000  # Convert to ms
        
        self.assertLess(avg_time, 10, f"Variant resolution should be < 10ms, got {avg_time:.2f}ms")

class TestDataIntegrity(unittest.TestCase):
    """Test data integrity after migration."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class with database connection."""
        cls.db_path = 'database/coins.db'
    
    def test_variant_id_format(self):
        """Test all variant IDs follow correct format."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT variant_id FROM coin_variants
                WHERE variant_id NOT GLOB 'US-[A-Z]*-[0-9][0-9][0-9][0-9]-[A-Z]*'
            """)
            invalid = cursor.fetchall()
            self.assertEqual(len(invalid), 0, 
                           f"Found invalid variant IDs: {invalid}")
    
    def test_parent_references_valid(self):
        """Test all parent_variant_id references are valid."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cv1.variant_id, cv1.parent_variant_id
                FROM coin_variants cv1
                LEFT JOIN coin_variants cv2 ON cv1.parent_variant_id = cv2.variant_id
                WHERE cv1.parent_variant_id IS NOT NULL 
                AND cv2.variant_id IS NULL
            """)
            orphans = cursor.fetchall()
            self.assertEqual(len(orphans), 0,
                           f"Found orphaned parent references: {orphans}")
    
    def test_circular_references(self):
        """Test no circular parent-child references exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check for direct circular references
            cursor.execute("""
                SELECT cv1.variant_id
                FROM coin_variants cv1
                JOIN coin_variants cv2 ON cv1.parent_variant_id = cv2.variant_id
                WHERE cv2.parent_variant_id = cv1.variant_id
            """)
            circular = cursor.fetchall()
            self.assertEqual(len(circular), 0,
                           f"Found circular references: {circular}")
    
    def test_base_variants_have_no_parents(self):
        """Test base variants don't have parent relationships."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT variant_id FROM coin_variants
                WHERE is_base_variant = 1 AND parent_variant_id IS NOT NULL
            """)
            invalid = cursor.fetchall()
            self.assertEqual(len(invalid), 0,
                           f"Base variants should not have parents: {invalid}")

def run_tests():
    """Run all tests."""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHierarchicalVariantResolution))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDataIntegrity))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)