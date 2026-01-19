#!/usr/bin/env python3
"""
Query helper functions for coin variant lookups.
Provides easy-to-use functions for developers to query coin variants.
"""

import sqlite3
import json
from typing import List, Dict, Optional

class CoinVariantQuery:
    """Helper class for querying coin variants"""
    
    def __init__(self, db_path: str = 'database/coins.db'):
        self.db_path = db_path
    
    def get_all_variants_for_type(self, base_type: str) -> List[Dict]:
        """
        Get all variants for a specific coin type.
        
        Args:
            base_type: The base coin type (e.g., 'TWO_CENT', 'INDIAN_HEAD_CENT')
        
        Returns:
            List of variant dictionaries sorted by year and sort_order
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM coin_variants
                WHERE base_type = ?
                ORDER BY year, sort_order
            ''', (base_type,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_variants_by_year(self, base_type: str, year: int) -> List[Dict]:
        """
        Get all variants for a specific coin type and year.
        
        Args:
            base_type: The base coin type
            year: The year to query
        
        Returns:
            List of variant dictionaries for that year
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM coin_variants
                WHERE base_type = ? AND year = ?
                ORDER BY sort_order
            ''', (base_type, year))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_major_variants(self, base_type: str) -> List[Dict]:
        """
        Get only major variants for a coin type.
        
        Args:
            base_type: The base coin type
        
        Returns:
            List of major variant dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM coin_variants
                WHERE base_type = ? AND is_major_variant = 1
                ORDER BY year, sort_order
            ''', (base_type,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def count_variants(self, base_type: str) -> Dict[str, int]:
        """
        Get variant counts for a coin type.
        
        Args:
            base_type: The base coin type
        
        Returns:
            Dictionary with total, major, and by-year counts
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total count
            cursor.execute('''
                SELECT COUNT(*) FROM coin_variants WHERE base_type = ?
            ''', (base_type,))
            total = cursor.fetchone()[0]
            
            # Major variant count
            cursor.execute('''
                SELECT COUNT(*) FROM coin_variants 
                WHERE base_type = ? AND is_major_variant = 1
            ''', (base_type,))
            major = cursor.fetchone()[0]
            
            # Count by year
            cursor.execute('''
                SELECT year, COUNT(*) as count
                FROM coin_variants
                WHERE base_type = ?
                GROUP BY year
                ORDER BY year
            ''', (base_type,))
            by_year = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                'total': total,
                'major_variants': major,
                'regular_variants': total - major,
                'by_year': by_year
            }
    
    def search_variants(self, search_term: str) -> List[Dict]:
        """
        Search for variants by description or type.
        
        Args:
            search_term: Term to search for in variant_type or variant_description
        
        Returns:
            List of matching variant dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM coin_variants
                WHERE variant_type LIKE ? OR variant_description LIKE ?
                ORDER BY base_type, year, sort_order
            ''', (f'%{search_term}%', f'%{search_term}%'))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_variant_by_id(self, variant_id: str) -> Optional[Dict]:
        """
        Get a specific variant by its ID.
        
        Args:
            variant_id: The variant ID (e.g., 'US-TWOC-1864-P-SM')
        
        Returns:
            Variant dictionary or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM coin_variants WHERE variant_id = ?
            ''', (variant_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_base_types(self) -> List[str]:
        """
        Get list of all unique base types in the database.
        
        Returns:
            List of base type codes
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT base_type 
                FROM coin_variants 
                ORDER BY base_type
            ''')
            
            return [row[0] for row in cursor.fetchall()]


def print_variant_summary(base_type: str, query: CoinVariantQuery):
    """Print a nice summary of variants for a coin type"""
    variants = query.get_all_variants_for_type(base_type)
    counts = query.count_variants(base_type)
    
    print(f"\n📊 {base_type} Variant Summary")
    print("=" * 60)
    print(f"Total Variants: {counts['total']}")
    print(f"Major Variants: {counts['major_variants']}")
    print(f"Regular Variants: {counts['regular_variants']}")
    
    print(f"\nVariants by Year:")
    for year, count in counts['by_year'].items():
        print(f"  {year}: {count} variant(s)")
    
    print(f"\nMajor Variants Detail:")
    major_variants = query.get_major_variants(base_type)
    for variant in major_variants:
        print(f"  • {variant['variant_id']}: {variant['variant_type']}")
        print(f"    {variant['variant_description']}")


def demo_queries():
    """Demonstrate various query capabilities"""
    query = CoinVariantQuery()
    
    print("🔍 Coin Variant Query Demo")
    print("=" * 60)
    
    # 1. Get all variants for Two Cent Pieces
    print("\n1. All Two Cent Piece variants:")
    two_cent_variants = query.get_all_variants_for_type('TWO_CENT')
    print(f"   Found {len(two_cent_variants)} variants")
    
    # 2. Get 1864 variants specifically
    print("\n2. 1864 Two Cent Piece variants:")
    variants_1864 = query.get_variants_by_year('TWO_CENT', 1864)
    for v in variants_1864:
        print(f"   • {v['variant_id']}: {v['variant_type']}")
    
    # 3. Count summary
    print("\n3. Variant counts for Two Cent Pieces:")
    counts = query.count_variants('TWO_CENT')
    print(f"   Total: {counts['total']}")
    print(f"   Major: {counts['major_variants']}")
    print(f"   Regular: {counts['regular_variants']}")
    
    # 4. Search for Proof variants
    print("\n4. Search for all Proof variants:")
    proof_variants = query.search_variants('Proof')
    print(f"   Found {len(proof_variants)} Proof variants")
    
    # 5. Get specific variant by ID
    print("\n5. Get specific variant US-TWOC-1864-P-SM:")
    variant = query.get_variant_by_id('US-TWOC-1864-P-SM')
    if variant:
        print(f"   {variant['variant_type']}: {variant['variant_description']}")
    
    # 6. Print full summary
    print_variant_summary('TWO_CENT', query)


if __name__ == "__main__":
    demo_queries()