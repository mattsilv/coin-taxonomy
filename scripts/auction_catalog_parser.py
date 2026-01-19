#!/usr/bin/env python3
"""
Auction Catalog Parser for Coin Taxonomy Mapping
Issue #54: Parse auction listings and map to coin variants

This module provides functions to parse auction catalog descriptions
and map them to our coin taxonomy with variant detection.
"""

import re
import sqlite3
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime

# Handle imports for both direct execution and module import
try:
    from scripts.utils.grade_validator import GradeNormalizer, GradeValidator
except ModuleNotFoundError:
    from utils.grade_validator import GradeNormalizer, GradeValidator

@dataclass
class AuctionListing:
    """Represents a parsed auction listing"""
    raw_title: str
    year: Optional[int] = None
    mint_mark: Optional[str] = None
    coin_type: Optional[str] = None
    variant_info: Optional[str] = None
    grade: Optional[str] = None
    grading_service: Optional[str] = None
    confidence_score: float = 0.0

class AuctionCatalogParser:
    """Parse auction listings and map to coin variants"""
    
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self._init_patterns()
        self._init_coin_types()
        self.grade_normalizer = GradeNormalizer()
        self.grade_validator = GradeValidator()
        
    def _init_patterns(self):
        """Initialize regex patterns for parsing"""
        # Year patterns
        self.year_pattern = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')
        
        # Mint mark patterns (including compound marks like CC)
        self.mint_patterns = [
            (re.compile(r'\b(\d{4})[- ]([PDSOCC]{1,2})\b'), 2),  # 1918-D or 1918 D
            (re.compile(r'\b([PDSOCC]{1,2})[- ]Mint\b', re.I), 1),  # D-Mint
            (re.compile(r'\bPhiladelphia\b', re.I), 'P'),
            (re.compile(r'\bDenver\b', re.I), 'D'),
            (re.compile(r'\bSan Francisco\b', re.I), 'S'),
            (re.compile(r'\bNew Orleans\b', re.I), 'O'),
            (re.compile(r'\bCarson City\b', re.I), 'CC'),
            (re.compile(r'\bWest Point\b', re.I), 'W'),
        ]
        
        # Grading patterns
        self.grade_patterns = [
            (re.compile(r'\b(MS|PR|PF|SP)[- ]?(\d{1,2})\b', re.I), 'numeric'),
            (re.compile(r'\b(PCGS|NGC|ANACS|ICG|CAC)\b', re.I), 'service'),
            (re.compile(r'\b(Good|Fine|Very Fine|VF|XF|AU|UNC|BU)\b', re.I), 'descriptive'),
            (re.compile(r'\b(VF|XF|AU|MS|PR|PF)[- ]?(\d{1,2})\b', re.I), 'grade_number'),
        ]
        
        # Variant patterns
        self.variant_patterns = {
            '8OVER7': [r'8[/ ]over[/ ]7', r'8/7'],
            '4OVER3': [r'4[/ ]over[/ ]3', r'4/3'],
            '3LEG': [r'3[- ]?legged?', r'three[- ]?legged?'],
            'DDO': [r'\bDDO\b', r'doubled die obverse'],
            'DDR': [r'\bDDR\b', r'doubled die reverse'],
            'RPM': [r'\bRPM\b', r'repunched mint'],
            'VAM': [r'\bVAM[- ]?\d+'],
            'SMALL_MOTTO': [r'small motto', r'sm motto'],
            'LARGE_MOTTO': [r'large motto', r'lg motto'],
            'TYPE1': [r'type[- ]?1\b', r'type[- ]?I\b', r'raised ground'],
            'TYPE2': [r'type[- ]?2\b', r'type[- ]?II\b', r'recessed ground'],
            'PROOF': [r'\bproof\b', r'\bPR\d+', r'\bPF\d+'],
            'SPECIMEN': [r'\bspecimen\b', r'\bSP\d+'],
            'CAMEO': [r'\bcameo\b', r'\bCAM\b'],
            'DCAM': [r'\bdeep cameo\b', r'\bDCAM\b', r'\bultra cameo\b', r'\bUCAM\b'],
        }
        
    def _init_coin_types(self):
        """Initialize coin type mappings from common names"""
        self.coin_type_mappings = {
            # Cents
            'indian head cent': 'INDIAN_HEAD_CENT',
            'indian cent': 'INDIAN_HEAD_CENT',
            'ihc': 'INDIAN_HEAD_CENT',
            'lincoln cent': 'LINCOLN_CENT',
            'lincoln penny': 'LINCOLN_CENT',
            'wheat cent': 'LINCOLN_WHEAT_CENT',
            'wheat penny': 'LINCOLN_WHEAT_CENT',
            'flying eagle': 'FLYING_EAGLE_CENT',
            'large cent': 'LARGE_CENT',
            
            # Two Cents
            'two cent': 'TWO_CENT',
            '2 cent': 'TWO_CENT',
            '2c': 'TWO_CENT',
            
            # Nickels
            'buffalo nickel': 'BUFFALO_NICKEL',
            'indian head nickel': 'BUFFALO_NICKEL',
            'shield nickel': 'SHIELD_NICKEL',
            'liberty nickel': 'LIBERTY_NICKEL',
            'v nickel': 'LIBERTY_NICKEL',
            'jefferson nickel': 'JEFFERSON_NICKEL',
            
            # Dimes
            'mercury dime': 'MERCURY_DIME',
            'winged liberty': 'MERCURY_DIME',
            'barber dime': 'BARBER_DIME',
            'roosevelt dime': 'ROOSEVELT_DIME',
            'seated liberty dime': 'SEATED_LIBERTY_DIME',
            
            # Quarters
            'washington quarter': 'WASHINGTON_QUARTER',
            'standing liberty': 'STANDING_LIBERTY_QUARTER',
            'barber quarter': 'BARBER_QUARTER',
            'seated liberty quarter': 'SEATED_LIBERTY_QUARTER',
            
            # Half Dollars
            'walking liberty': 'WALKING_LIBERTY_HALF',
            'walker': 'WALKING_LIBERTY_HALF',
            'franklin half': 'FRANKLIN_HALF',
            'kennedy half': 'KENNEDY_HALF',
            'barber half': 'BARBER_HALF',
            
            # Dollars
            'morgan dollar': 'MORGAN_DOLLAR',
            'morgan': 'MORGAN_DOLLAR',
            'peace dollar': 'PEACE_DOLLAR',
            'peace': 'PEACE_DOLLAR',
            'trade dollar': 'TRADE_DOLLAR',
            'eisenhower': 'EISENHOWER_DOLLAR',
            'ike dollar': 'EISENHOWER_DOLLAR',
            'susan b anthony': 'SUSAN_B_ANTHONY_DOLLAR',
            'sba': 'SUSAN_B_ANTHONY_DOLLAR',
            'sacagawea': 'SACAGAWEA_DOLLAR',
        }
    
    def parse_listing(self, title: str, description: str = "") -> AuctionListing:
        """
        Parse an auction listing title and description.
        
        Args:
            title: Auction listing title
            description: Optional extended description
            
        Returns:
            Parsed AuctionListing object
        """
        listing = AuctionListing(raw_title=title)
        combined_text = f"{title} {description}".lower()
        
        # Extract year
        year_match = self.year_pattern.search(title)
        if year_match:
            listing.year = int(year_match.group(1))
            listing.confidence_score += 0.3
        
        # Extract mint mark
        for pattern, group in self.mint_patterns:
            if isinstance(pattern, str):
                # Direct string mint mark
                if pattern in title.upper():
                    listing.mint_mark = group
                    listing.confidence_score += 0.2
                    break
            else:
                match = pattern.search(title)
                if match:
                    if isinstance(group, int):
                        listing.mint_mark = match.group(group).upper()
                    else:
                        listing.mint_mark = group
                    listing.confidence_score += 0.2
                    break
        
        # Default to P if no mint mark found
        if not listing.mint_mark and listing.year:
            listing.mint_mark = 'P'
            listing.confidence_score += 0.1
        
        # Identify coin type
        for name, coin_type in self.coin_type_mappings.items():
            if name in combined_text:
                listing.coin_type = coin_type
                listing.confidence_score += 0.3
                break
        
        # Extract variants
        variants_found = []
        for variant_key, patterns in self.variant_patterns.items():
            for pattern in patterns:
                if re.search(pattern, combined_text, re.I):
                    variants_found.append(variant_key)
                    listing.confidence_score += 0.1
                    break
        
        if variants_found:
            listing.variant_info = ','.join(variants_found)
        
        # Extract grade and normalize to canonical format
        for pattern, grade_type in self.grade_patterns:
            match = pattern.search(title)
            if match:
                if grade_type in ['numeric', 'grade_number']:
                    # Normalize grade to canonical format (MS-65, PR-69, etc.)
                    try:
                        raw_grade = match.group(0)
                        listing.grade = self.grade_normalizer.normalize(raw_grade)
                    except ValueError:
                        # If normalization fails, store raw grade
                        listing.grade = match.group(0)
                elif grade_type == 'service':
                    listing.grading_service = match.group(0).upper()
                elif grade_type == 'descriptive':
                    listing.grade = match.group(0)
        
        # Cap confidence score at 1.0
        listing.confidence_score = min(1.0, listing.confidence_score)
        
        return listing
    
    def map_to_variant(self, listing: AuctionListing) -> Optional[str]:
        """
        Map parsed auction listing to coin variant ID.
        
        Args:
            listing: Parsed auction listing
            
        Returns:
            variant_id if found, None otherwise
        """
        if not listing.year or not listing.coin_type:
            return None
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Build query based on available information
            query_parts = ["SELECT variant_id FROM coin_variants WHERE"]
            params = []
            
            # Add base criteria
            query_parts.append("base_type = ?")
            params.append(listing.coin_type)
            
            query_parts.append("AND year = ?")
            params.append(listing.year)
            
            if listing.mint_mark:
                query_parts.append("AND mint_mark = ?")
                params.append(listing.mint_mark)
            
            # Check for specific variants
            if listing.variant_info:
                variants = listing.variant_info.split(',')
                variant_conditions = []
                
                for variant in variants:
                    if variant == 'PROOF':
                        variant_conditions.append("variant_type = 'Proof'")
                    elif variant == 'SMALL_MOTTO':
                        variant_conditions.append("variant_type LIKE '%Small Motto%'")
                    elif variant == 'LARGE_MOTTO':
                        variant_conditions.append("variant_type LIKE '%Large Motto%'")
                    elif variant == 'TYPE1':
                        variant_conditions.append("variant_type LIKE '%Type 1%'")
                    elif variant == 'TYPE2':
                        variant_conditions.append("variant_type LIKE '%Type 2%'")
                    elif variant in ['8OVER7', '4OVER3', '3LEG', 'DDO', 'DDR']:
                        variant_conditions.append(f"variant_id LIKE '%{variant}%'")
                
                if variant_conditions:
                    query_parts.append(f"AND ({' OR '.join(variant_conditions)})")
            else:
                # No specific variant - get base variant
                query_parts.append("AND is_base_variant = 1")
            
            # Order by priority
            query_parts.append("ORDER BY priority_score DESC, resolution_level ASC")
            query_parts.append("LIMIT 1")
            
            query = ' '.join(query_parts)
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            return result[0] if result else None
    
    def batch_parse_listings(self, listings: List[Dict[str, str]]) -> List[Tuple[AuctionListing, Optional[str]]]:
        """
        Parse multiple auction listings in batch.
        
        Args:
            listings: List of dicts with 'title' and optional 'description'
            
        Returns:
            List of (parsed_listing, variant_id) tuples
        """
        results = []
        
        for listing_data in listings:
            title = listing_data.get('title', '')
            description = listing_data.get('description', '')
            
            parsed = self.parse_listing(title, description)
            variant_id = self.map_to_variant(parsed)
            results.append((parsed, variant_id))
        
        return results
    
    def get_parsing_statistics(self, results: List[Tuple[AuctionListing, Optional[str]]]) -> Dict:
        """
        Generate statistics on parsing results.
        
        Args:
            results: List of parsing results
            
        Returns:
            Dict with statistics
        """
        total = len(results)
        mapped = sum(1 for _, variant_id in results if variant_id)
        high_confidence = sum(1 for listing, _ in results if listing.confidence_score >= 0.7)
        
        coin_types = {}
        variants = {}
        
        for listing, variant_id in results:
            if listing.coin_type:
                coin_types[listing.coin_type] = coin_types.get(listing.coin_type, 0) + 1
            
            if listing.variant_info:
                for variant in listing.variant_info.split(','):
                    variants[variant] = variants.get(variant, 0) + 1
        
        return {
            'total_listings': total,
            'successfully_mapped': mapped,
            'mapping_rate': mapped / total if total > 0 else 0,
            'high_confidence': high_confidence,
            'confidence_rate': high_confidence / total if total > 0 else 0,
            'coin_types_found': coin_types,
            'variants_detected': variants
        }

# Command-line interface
if __name__ == "__main__":
    import json
    
    parser = AuctionCatalogParser()
    
    # Example listings
    test_listings = [
        {"title": "1918-D Buffalo Nickel MS64 PCGS"},
        {"title": "1918 D Buffalo Nickel 8 Over 7 Overdate NGC AU55"},
        {"title": "1864 Two Cent Piece Large Motto Proof"},
        {"title": "1937-D Buffalo Nickel Three-Legged VF30"},
        {"title": "1913 Buffalo Nickel Type 1 PCGS MS65"},
        {"title": "1942 Mercury Dime MS67 Full Bands"},
        {"title": "1916-D Mercury Dime Good-4"},
    ]
    
    results = parser.batch_parse_listings(test_listings)
    
    print("Auction Catalog Parsing Results:")
    print("=" * 60)
    
    for (listing, variant_id), original in zip(results, test_listings):
        print(f"\nTitle: {original['title']}")
        print(f"  Year: {listing.year}")
        print(f"  Mint: {listing.mint_mark}")
        print(f"  Type: {listing.coin_type}")
        print(f"  Variants: {listing.variant_info}")
        print(f"  Grade: {listing.grade}")
        print(f"  Confidence: {listing.confidence_score:.2f}")
        print(f"  Mapped to: {variant_id if variant_id else 'NOT FOUND'}")
    
    stats = parser.get_parsing_statistics(results)
    print(f"\n📊 Statistics:")
    print(f"  Total: {stats['total_listings']}")
    print(f"  Mapped: {stats['successfully_mapped']} ({stats['mapping_rate']:.1%})")
    print(f"  High Confidence: {stats['high_confidence']} ({stats['confidence_rate']:.1%})")