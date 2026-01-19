#!/usr/bin/env python3
"""
Variant Resolution Functions for Auction Mapping

This module provides functions to map auction listings to the correct coin variant.
"""

import sqlite3
import json
from typing import Optional, List, Dict, Tuple

class VariantResolver:
    def __init__(self, db_path='database/coins.db'):
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
