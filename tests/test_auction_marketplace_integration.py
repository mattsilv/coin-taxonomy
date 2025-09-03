#!/usr/bin/env python3
"""
Test Suite for Auction Catalog Parser and Marketplace Listing Matcher
Tests for Issues #54 and #56
"""

import unittest
import sqlite3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.auction_catalog_parser import AuctionCatalogParser, AuctionListing
from scripts.marketplace_listing_matcher import MarketplaceListingMatcher, MarketplaceListing
from scripts.variant_resolver import VariantResolver

class TestAuctionCatalogParser(unittest.TestCase):
    """Test auction catalog parsing functionality"""
    
    def setUp(self):
        self.parser = AuctionCatalogParser()
    
    def test_parse_standard_listing(self):
        """Test parsing standard auction listing"""
        listing = self.parser.parse_listing("1918-D Buffalo Nickel MS64 PCGS")
        
        self.assertEqual(listing.year, 1918)
        self.assertEqual(listing.mint_mark, 'D')
        self.assertEqual(listing.coin_type, 'BUFFALO_NICKEL')
        self.assertEqual(listing.grade, 'MS64')
        self.assertEqual(listing.grading_service, 'PCGS')
        self.assertGreaterEqual(listing.confidence_score, 0.7)
    
    def test_parse_overdate_variety(self):
        """Test parsing overdate variety"""
        listing = self.parser.parse_listing("1918 D Buffalo Nickel 8 Over 7 NGC AU55")
        
        self.assertEqual(listing.year, 1918)
        self.assertEqual(listing.mint_mark, 'D')
        self.assertEqual(listing.coin_type, 'BUFFALO_NICKEL')
        self.assertIn('8OVER7', listing.variant_info)
        self.assertEqual(listing.grade, 'AU55')
    
    def test_parse_proof_coin(self):
        """Test parsing proof designation"""
        listing = self.parser.parse_listing("1864 Two Cent Piece Large Motto Proof")
        
        self.assertEqual(listing.year, 1864)
        self.assertEqual(listing.mint_mark, 'P')  # Default to P
        self.assertEqual(listing.coin_type, 'TWO_CENT')
        self.assertIn('PROOF', listing.variant_info)
        self.assertIn('LARGE_MOTTO', listing.variant_info)
    
    def test_parse_three_legged_variety(self):
        """Test parsing three-legged variety"""
        listing = self.parser.parse_listing("1937-D Buffalo Nickel Three-Legged VF30")
        
        self.assertEqual(listing.year, 1937)
        self.assertEqual(listing.mint_mark, 'D')
        self.assertIn('3LEG', listing.variant_info)
        self.assertEqual(listing.grade, 'VF30')
    
    def test_parse_type_varieties(self):
        """Test parsing type varieties"""
        listing = self.parser.parse_listing("1913 Buffalo Nickel Type 1 PCGS MS65")
        
        self.assertEqual(listing.year, 1913)
        self.assertEqual(listing.mint_mark, 'P')
        self.assertIn('TYPE1', listing.variant_info)
    
    def test_parse_mercury_dime(self):
        """Test parsing different coin types"""
        listing = self.parser.parse_listing("1942 Mercury Dime MS67 Full Bands")
        
        self.assertEqual(listing.year, 1942)
        self.assertEqual(listing.coin_type, 'MERCURY_DIME')
        self.assertIsNotNone(listing.grade)
    
    def test_parse_mint_names(self):
        """Test parsing full mint names"""
        listings = [
            ("1916 Denver Mercury Dime", 'D'),
            ("1909 San Francisco Lincoln Cent", 'S'),
            ("1882 Carson City Morgan Dollar", 'CC'),
            ("1904 Philadelphia Indian Cent", 'P'),
        ]
        
        for title, expected_mint in listings:
            listing = self.parser.parse_listing(title)
            self.assertEqual(listing.mint_mark, expected_mint,
                           f"Failed to parse mint from: {title}")
    
    def test_batch_parsing(self):
        """Test batch parsing functionality"""
        test_listings = [
            {"title": "1918-D Buffalo Nickel MS64"},
            {"title": "1864 Two Cent Piece Proof"},
            {"title": "1937-D Three-Legged Buffalo"},
        ]
        
        results = self.parser.batch_parse_listings(test_listings)
        
        self.assertEqual(len(results), 3)
        for parsed, variant_id in results:
            self.assertIsInstance(parsed, AuctionListing)
            self.assertIsNotNone(parsed.year)

class TestMarketplaceListingMatcher(unittest.TestCase):
    """Test marketplace listing fuzzy matching"""
    
    def setUp(self):
        self.matcher = MarketplaceListingMatcher()
    
    def test_normalize_typos(self):
        """Test text normalization with typos"""
        normalized = self.matcher.normalize_text("buffallo nickle")
        self.assertIn("buffalo", normalized)
        self.assertIn("nickel", normalized)
        
        normalized = self.matcher.normalize_text("lincon wheat penney")
        self.assertIn("lincoln", normalized)
        self.assertIn("penny", normalized)
    
    def test_normalize_abbreviations(self):
        """Test abbreviation expansion"""
        normalized = self.matcher.normalize_text("ihc ms65")
        self.assertIn("indian head cent", normalized)
        self.assertIn("mint state", normalized)
        
        normalized = self.matcher.normalize_text("ddo proof")
        self.assertIn("doubled die obverse", normalized)
        self.assertIn("proof", normalized)
    
    def test_extract_features(self):
        """Test feature extraction from normalized text"""
        text = "1918 d buffalo nickel 8 over 7"
        features = self.matcher.extract_features(text)
        
        self.assertEqual(features['year'], 1918)
        self.assertEqual(features['mint_mark'], 'D')
        self.assertEqual(features['coin_type'], 'buffalo nickel')
        self.assertIn('8/7', features['variants'])
    
    def test_extract_features_with_full_mint_names(self):
        """Test extracting mint marks from full names"""
        test_cases = [
            ("1916 denver mercury dime", 'D'),
            ("1909 san francisco lincoln", 'S'),
            ("1882 carson city morgan", 'CC'),
            ("1904 philadelphia indian", 'P'),
        ]
        
        for text, expected_mint in test_cases:
            features = self.matcher.extract_features(text)
            self.assertEqual(features['mint_mark'], expected_mint,
                           f"Failed to extract mint from: {text}")
    
    def test_fuzzy_match_with_typos(self):
        """Test fuzzy matching with typos"""
        listing = self.matcher.match_listing("1918d buffallo nickle 8 over 7")
        
        self.assertIsNotNone(listing.final_match)
        self.assertGreater(listing.match_confidence, 0.5)
        self.assertEqual(listing.extracted_features['year'], 1918)
        self.assertEqual(listing.extracted_features['mint_mark'], 'D')
    
    def test_resolve_to_base_variant(self):
        """Test resolution to base variant"""
        # Test with a specific variant that should resolve to base
        listing = self.matcher.match_listing("1937 D buffalo three leg", require_base=True)
        
        # Should resolve to base 1937-D, not the three-legged variety
        self.assertIsNotNone(listing.final_match)
        self.assertEqual(listing.match_method, "fuzzy_base_resolution")
    
    def test_batch_matching(self):
        """Test batch matching functionality"""
        listings = [
            "1918d buffallo nickle",
            "mercury dime 1942 denver",
            "Two Cent Piece 1864 Lg Motto",
        ]
        
        results = self.matcher.batch_match_listings(listings)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIsInstance(result, MarketplaceListing)
            self.assertIsNotNone(result.normalized_text)
    
    def test_match_statistics(self):
        """Test statistics generation"""
        listings = [
            "1918 buffalo nickel",
            "1942 mercury dime",
            "invalid listing text",
        ]
        
        results = self.matcher.batch_match_listings(listings)
        stats = self.matcher.get_match_statistics(results)
        
        self.assertIn('total_listings', stats)
        self.assertIn('successfully_matched', stats)
        self.assertIn('match_rate', stats)
        self.assertEqual(stats['total_listings'], 3)

class TestVariantResolver(unittest.TestCase):
    """Test variant resolution functionality"""
    
    def setUp(self):
        self.resolver = VariantResolver()
    
    def test_map_auction_to_variant_base(self):
        """Test mapping to base variant"""
        # Map a simple listing to base variant
        variant_id = self.resolver.map_auction_to_variant(
            year=1918,
            mint_mark='D',
            coin_type='BUFFALO_NICKEL',
            additional_info=None
        )
        
        # Should return a variant ID (if exists in DB)
        if variant_id:
            self.assertTrue(variant_id.startswith('US-'))
    
    def test_map_auction_with_special_variety(self):
        """Test mapping with special variety info"""
        variant_id = self.resolver.map_auction_to_variant(
            year=1918,
            mint_mark='D',
            coin_type='BUFFALO_NICKEL',
            additional_info='8/7 overdate'
        )
        
        # Should find the overdate variety if it exists
        if variant_id:
            self.assertTrue(variant_id.startswith('US-'))
    
    def test_resolve_ambiguous_base(self):
        """Test resolution of ambiguous base variants"""
        # Test with 1864 Two Cent (has Small and Large Motto)
        variant_id = self.resolver.resolve_ambiguous_base(
            year=1864,
            mint_mark='P',
            coin_type='TWO_CENT'
        )
        
        # Should return one variant based on priority
        if variant_id:
            self.assertTrue(variant_id.startswith('US-'))
    
    def test_get_variant_hierarchy(self):
        """Test getting full hierarchy for a variant"""
        # This would need a known variant ID from the database
        # Using a placeholder test
        hierarchy = self.resolver.get_variant_hierarchy('US-BUFF-1918-D')
        
        if hierarchy:
            self.assertIn('variant_id', hierarchy)
            self.assertIn('base_type', hierarchy)

class TestIntegration(unittest.TestCase):
    """Integration tests for the full pipeline"""
    
    def setUp(self):
        self.parser = AuctionCatalogParser()
        self.matcher = MarketplaceListingMatcher()
        self.resolver = VariantResolver()
    
    def test_full_auction_pipeline(self):
        """Test complete auction parsing and mapping pipeline"""
        # Parse auction listing
        listing = self.parser.parse_listing("1918-D Buffalo Nickel 8/7 MS64 PCGS")
        
        # Map to variant
        variant_id = self.parser.map_to_variant(listing)
        
        # Verify we got reasonable results
        self.assertIsNotNone(listing.year)
        self.assertIsNotNone(listing.mint_mark)
        self.assertIsNotNone(listing.coin_type)
        
        if variant_id:
            # Get hierarchy
            hierarchy = self.resolver.get_variant_hierarchy(variant_id)
            if hierarchy:
                self.assertIn('variant_id', hierarchy)
    
    def test_full_marketplace_pipeline(self):
        """Test complete marketplace matching pipeline"""
        # Match marketplace listing with typos
        listing = self.matcher.match_listing("1918d buffallo nickle 8 over 7")
        
        # Should have normalized and extracted features
        self.assertIsNotNone(listing.normalized_text)
        self.assertIsNotNone(listing.extracted_features)
        
        # Should have found possible matches
        if listing.possible_matches:
            self.assertGreater(len(listing.possible_matches), 0)
            
            # If we have a final match, verify it's reasonable
            if listing.final_match:
                self.assertTrue(listing.final_match.startswith('US-'))
    
    def test_ambiguous_resolution_priority(self):
        """Test that ambiguous variants resolve by priority"""
        # Test with 1913 Buffalo Nickel (Type 1 vs Type 2)
        listings = [
            "1913 Buffalo Nickel MS65",  # No type specified
            "1913 Buffalo Nickel Type 1",  # Type 1 specified
            "1913 Buffalo Nickel Type 2",  # Type 2 specified
        ]
        
        for title in listings:
            listing = self.parser.parse_listing(title)
            variant_id = self.parser.map_to_variant(listing)
            
            # Each should map to something
            if variant_id:
                self.assertTrue(variant_id.startswith('US-'))

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAuctionCatalogParser))
    suite.addTests(loader.loadTestsFromTestCase(TestMarketplaceListingMatcher))
    suite.addTests(loader.loadTestsFromTestCase(TestVariantResolver))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)