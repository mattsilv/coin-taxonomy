#!/usr/bin/env python3
"""
Marketplace Listing Matcher with Fuzzy Matching
Issue #56: Hierarchical variant resolution for marketplace integration

This module provides fuzzy matching capabilities for marketplace listings
that may have typos, abbreviations, or non-standard formatting.
"""

import re
import sqlite3
from typing import Optional, List, Dict, Tuple, Set
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from collections import defaultdict
import json

# Handle imports for both direct execution and module import
try:
    from scripts.utils.grade_validator import GradeNormalizer, GradeValidator
except ModuleNotFoundError:
    from utils.grade_validator import GradeNormalizer, GradeValidator

@dataclass
class MarketplaceListing:
    """Represents a marketplace listing with confidence scores"""
    raw_text: str
    normalized_text: str = ""
    extracted_features: Dict = field(default_factory=dict)
    possible_matches: List[Tuple[str, float]] = field(default_factory=list)
    final_match: Optional[str] = None
    match_confidence: float = 0.0
    match_method: str = ""

class MarketplaceListingMatcher:
    """Advanced fuzzy matching for marketplace listings"""
    
    def __init__(self, db_path='data/coins.db'):
        self.db_path = db_path
        self._build_lookup_tables()
        self._init_normalizers()
        self.grade_normalizer = GradeNormalizer()
        self.grade_validator = GradeValidator()
        
    def _build_lookup_tables(self):
        """Build in-memory lookup tables for fast matching"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Build variant lookup
            cursor.execute("""
                SELECT variant_id, base_type, year, mint_mark, 
                       variant_type, variant_description,
                       parent_variant_id, is_base_variant, priority_score
                FROM coin_variants
            """)
            
            self.variants = {}
            self.base_variants = defaultdict(list)
            self.variant_keywords = defaultdict(set)
            
            for row in cursor.fetchall():
                variant_id = row[0]
                self.variants[variant_id] = {
                    'base_type': row[1],
                    'year': row[2],
                    'mint_mark': row[3],
                    'variant_type': row[4],
                    'variant_description': row[5],
                    'parent_variant_id': row[6],
                    'is_base_variant': row[7],
                    'priority_score': row[8]
                }
                
                # Build base variant index
                if row[7]:  # is_base_variant
                    key = (row[1], row[2], row[3])  # (base_type, year, mint_mark)
                    self.base_variants[key].append({
                        'variant_id': variant_id,
                        'priority_score': row[8] or 50
                    })
                
                # Extract keywords for fuzzy matching
                if row[4]:  # variant_type
                    keywords = self._extract_keywords(row[4])
                    for kw in keywords:
                        self.variant_keywords[kw].add(variant_id)
                        
                if row[5]:  # variant_description
                    keywords = self._extract_keywords(row[5])
                    for kw in keywords:
                        self.variant_keywords[kw].add(variant_id)
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful keywords from text"""
        if not text:
            return set()
            
        # Remove common words and punctuation
        stopwords = {'the', 'a', 'an', 'and', 'or', 'with', 'of', 'to', 'in'}
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        keywords = {w for w in words if w not in stopwords and len(w) > 2}
        
        # Add common abbreviations
        abbrev_map = {
            'overdate': ['od', 'over'],
            'doubled': ['dd', 'dbl'],
            'large': ['lg', 'lrg'],
            'small': ['sm', 'sml'],
            'proof': ['pf', 'pr'],
            'business': ['bus', 'bs'],
            'strike': ['str', 'stk'],
            'motto': ['mot'],
            'type': ['typ', 'tp'],
        }
        
        for word in keywords.copy():
            if word in abbrev_map:
                keywords.update(abbrev_map[word])
        
        return keywords
    
    def _init_normalizers(self):
        """Initialize text normalization patterns"""
        # Common typos and variations
        self.typo_corrections = {
            'buffallo': 'buffalo',
            'bufalo': 'buffalo',
            'nikle': 'nickel',
            'nickle': 'nickel',
            'penney': 'penny',
            'cnet': 'cent',
            'cetn': 'cent',
            'dolalr': 'dollar',
            'dollor': 'dollar',
            'quearter': 'quarter',
            'quater': 'quarter',
            'mercery': 'mercury',
            'mecury': 'mercury',
            'washignton': 'washington',
            'washinton': 'washington',
            'lincon': 'lincoln',
            'licoln': 'lincoln',
            'jeffrson': 'jefferson',
            'roosvelt': 'roosevelt',
            'kenedy': 'kennedy',
            'kennady': 'kennedy',
        }
        
        # Abbreviation expansions
        self.abbreviations = {
            'ihc': 'indian head cent',
            'lwc': 'lincoln wheat cent',
            'vdb': 'vdb',
            'ddo': 'doubled die obverse',
            'ddr': 'doubled die reverse',
            'rpm': 'repunched mintmark',
            'fs': 'full steps',
            'fb': 'full bands',
            'fh': 'full head',
            'cam': 'cameo',
            'dcam': 'deep cameo',
            'ucam': 'ultra cameo',
            'pr': 'proof',
            'pf': 'proof',
            'au': 'about uncirculated',
            'bu': 'brilliant uncirculated',
            'unc': 'uncirculated',
            'vf': 'very fine',
            'xf': 'extremely fine',
            'ef': 'extremely fine',
        }
        
    def normalize_text(self, text: str) -> str:
        """Normalize marketplace listing text"""
        normalized = text.lower()
        
        # Apply typo corrections
        for typo, correction in self.typo_corrections.items():
            normalized = normalized.replace(typo, correction)
        
        # Expand abbreviations - handle both standalone and compound cases
        # Special handling for grading abbreviations with numbers
        grading_patterns = [
            (r'\bms(\d+)\b', 'mint state \\1'),
            (r'\bpr(\d+)\b', 'proof \\1'),
            (r'\bpf(\d+)\b', 'proof \\1'),
            (r'\bau(\d+)\b', 'about uncirculated \\1'),
            (r'\bvf(\d+)\b', 'very fine \\1'),
            (r'\bxf(\d+)\b', 'extremely fine \\1'),
            (r'\bef(\d+)\b', 'extremely fine \\1'),
        ]
        
        for pattern, replacement in grading_patterns:
            normalized = re.sub(pattern, replacement, normalized, flags=re.I)
        
        # Now handle other abbreviations without numbers
        for abbrev, expansion in self.abbreviations.items():
            # Skip grading abbrevs already handled
            if abbrev not in ['ms', 'pr', 'pf', 'au', 'vf', 'xf', 'ef']:
                pattern = r'\b' + re.escape(abbrev) + r'\b'
                normalized = re.sub(pattern, expansion, normalized, flags=re.I)
        
        # Clean up any double spaces
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Standardize separators
        normalized = re.sub(r'[-/]+', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized.strip()
    
    def extract_grade(self, text: str) -> Optional[str]:
        """
        Extract and normalize grade from text.
        Returns canonical format (MS-65, PR-69, etc.) or None.
        """
        # Try to match grade patterns
        grade_patterns = [
            r'\b(MS|PR|PF|SP|AU|XF|EF|VF|VG|F|G|AG|FR|P)[\s-]?(\d{1,2})\b',
        ]

        for pattern in grade_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                try:
                    # Normalize to canonical format
                    raw_grade = match.group(0)
                    return self.grade_normalizer.normalize(raw_grade)
                except ValueError:
                    # If normalization fails, continue searching
                    continue

        return None

    def extract_features(self, text: str) -> Dict:
        """Extract structured features from normalized text"""
        features = {
            'year': None,
            'mint_mark': None,
            'coin_type': None,
            'grade': None,
            'variants': [],
            'keywords': set()
        }

        # Extract and normalize grade
        features['grade'] = self.extract_grade(text)
        
        # Extract year (1850-2025 range)
        # Try to find standalone 4-digit year first
        year_match = re.search(r'\b(18[5-9]\d|19\d{2}|20[0-2]\d)\b', text)
        if year_match:
            features['year'] = int(year_match.group(1))
        
        # Also check if year is attached to mint mark like "1918d"
        year_mint_match = re.search(r'\b(18[5-9]\d|19\d{2}|20[0-2]\d)([pdsocc])\b', text, re.I)
        if year_mint_match and not features['year']:
            features['year'] = int(year_mint_match.group(1))
            features['mint_mark'] = year_mint_match.group(2).upper()
        
        # Extract mint mark (only if not already extracted from year-mint pattern)
        # Look for patterns like "1918 d" or "1918d" or standalone letters
        if not features.get('mint_mark'):
            mint_patterns = [
                r'\b\d{4}\s*([pdsocc])\b',  # Year followed by mint
                r'\b([pdsocc])\s*mint\b',    # Letter followed by 'mint'
                r'\bdenver\b',                # Full mint names
                r'\bsan\s*francisco\b',
                r'\bphiladelphia\b',
                r'\bcarson\s*city\b',
                r'\bnew\s*orleans\b',
                r'\bwest\s*point\b',
            ]
        
            mint_map = {
                'denver': 'D',
                'san francisco': 'S',
                'philadelphia': 'P',
                'carson city': 'CC',
                'new orleans': 'O',
                'west point': 'W',
            }
            
            for pattern in mint_patterns:
                match = re.search(pattern, text, re.I)
                if match:
                    mint = match.group(1) if match.lastindex else match.group(0)
                    mint = mint.lower().strip()
                    if mint in mint_map:
                        features['mint_mark'] = mint_map[mint]
                    elif len(mint) <= 2:
                        features['mint_mark'] = mint.upper()
                    break
        
        # Default to P if year found but no mint
        if features['year'] and not features['mint_mark']:
            features['mint_mark'] = 'P'
        
        # Extract coin type using fuzzy matching
        coin_types = {
            'buffalo nickel': ['buffalo', 'buff', 'indian head nickel'],
            'mercury dime': ['mercury', 'merc', 'winged liberty'],
            'lincoln cent': ['lincoln', 'wheat'],
            'two cent': ['two cent', '2 cent', '2c'],
            'indian head cent': ['indian head', 'ihc'],
            'morgan dollar': ['morgan'],
            'peace dollar': ['peace'],
            'walking liberty': ['walking', 'walker'],
            'washington quarter': ['washington'],
            'roosevelt dime': ['roosevelt'],
            'kennedy half': ['kennedy'],
            'franklin half': ['franklin'],
        }
        
        best_type_match = None
        best_type_score = 0
        
        for coin_type, patterns in coin_types.items():
            for pattern in patterns:
                if pattern in text:
                    score = len(pattern) / len(text)  # Longer matches are better
                    if score > best_type_score:
                        best_type_match = coin_type
                        best_type_score = score
        
        if best_type_match:
            features['coin_type'] = best_type_match
        
        # Extract variant keywords
        variant_keywords = [
            ('8 over 7', '8/7'),
            ('8/7', '8/7'),
            ('4 over 3', '4/3'),
            ('4/3', '4/3'),
            ('overdate', 'overdate'),
            ('over', 'overdate'),
            ('doubled die', 'doubled die'),
            ('ddo', 'ddo'),
            ('ddr', 'ddr'),
            ('three leg', 'three leg'),
            ('3 leg', 'three leg'),
            ('three-leg', 'three leg'),
            ('small motto', 'small motto'),
            ('large motto', 'large motto'),
            ('type 1', 'type 1'),
            ('type 2', 'type 2'),
            ('type i', 'type 1'),
            ('type ii', 'type 2'),
            ('proof', 'proof'),
            ('specimen', 'specimen'),
            ('cameo', 'cameo'),
            ('deep cameo', 'deep cameo'),
            ('full bands', 'full bands'),
            ('full steps', 'full steps'),
            ('full head', 'full head'),
        ]
        
        for pattern, normalized_variant in variant_keywords:
            if pattern in text:
                if normalized_variant not in features['variants']:
                    features['variants'].append(normalized_variant)
                features['keywords'].add(normalized_variant)
        
        # Extract all keywords for fuzzy matching
        words = text.split()
        features['keywords'].update(w for w in words if len(w) > 2)
        
        return features
    
    def fuzzy_match_variants(self, features: Dict) -> List[Tuple[str, float]]:
        """Find variant matches using fuzzy matching"""
        candidates = []
        
        # Start with exact year/mint matches if available
        if features['year'] and features['mint_mark']:
            for variant_id, variant_data in self.variants.items():
                if (variant_data['year'] == features['year'] and 
                    variant_data['mint_mark'] == features['mint_mark']):
                    
                    # Calculate similarity score
                    score = 0.5  # Base score for year/mint match
                    
                    # Check variant keywords
                    if features['variants']:
                        variant_text = f"{variant_data.get('variant_type', '')} {variant_data.get('variant_description', '')}".lower()
                        
                        for variant_keyword in features['variants']:
                            if variant_keyword in variant_text:
                                score += 0.2
                    
                    # Check if base variant when no specific variants mentioned
                    if not features['variants'] and variant_data['is_base_variant']:
                        score += 0.3
                    
                    # Boost score based on priority
                    priority = variant_data.get('priority_score', 50)
                    score += (priority / 100) * 0.2
                    
                    candidates.append((variant_id, min(1.0, score)))
        
        # Fallback to keyword matching if no year/mint
        elif features['keywords']:
            keyword_matches = defaultdict(int)
            
            for keyword in features['keywords']:
                if keyword in self.variant_keywords:
                    for variant_id in self.variant_keywords[keyword]:
                        keyword_matches[variant_id] += 1
            
            # Convert to scores
            max_matches = max(keyword_matches.values()) if keyword_matches else 1
            
            for variant_id, match_count in keyword_matches.items():
                score = (match_count / max_matches) * 0.7
                candidates.append((variant_id, score))
        
        # Sort by score descending
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        return candidates[:10]  # Return top 10 candidates
    
    def resolve_to_base_variant(self, variant_id: str) -> str:
        """Resolve a specific variant to its base variant"""
        variant_data = self.variants.get(variant_id)
        
        if not variant_data:
            return variant_id
        
        # If already a base variant, return it
        if variant_data['is_base_variant']:
            return variant_id
        
        # If has parent, resolve to parent
        if variant_data['parent_variant_id']:
            return self.resolve_to_base_variant(variant_data['parent_variant_id'])
        
        # Try to find base variant for same year/mint
        key = (variant_data['base_type'], variant_data['year'], variant_data['mint_mark'])
        base_candidates = self.base_variants.get(key, [])
        
        if base_candidates:
            # Return highest priority base variant
            base_candidates.sort(key=lambda x: x['priority_score'], reverse=True)
            return base_candidates[0]['variant_id']
        
        return variant_id
    
    def match_listing(self, raw_text: str, require_base: bool = False) -> MarketplaceListing:
        """
        Match a marketplace listing to coin variants.
        
        Args:
            raw_text: Raw listing text
            require_base: If True, always resolve to base variant
            
        Returns:
            MarketplaceListing with match results
        """
        listing = MarketplaceListing(raw_text=raw_text)
        
        # Normalize text
        listing.normalized_text = self.normalize_text(raw_text)
        
        # Extract features
        listing.extracted_features = self.extract_features(listing.normalized_text)
        
        # Find candidate matches
        listing.possible_matches = self.fuzzy_match_variants(listing.extracted_features)
        
        # Select best match
        if listing.possible_matches:
            best_variant, best_score = listing.possible_matches[0]
            
            # Resolve to base if required
            if require_base:
                best_variant = self.resolve_to_base_variant(best_variant)
                listing.match_method = "fuzzy_base_resolution"
            else:
                listing.match_method = "fuzzy_exact"
            
            listing.final_match = best_variant
            listing.match_confidence = best_score
        
        return listing
    
    def batch_match_listings(self, listings: List[str], require_base: bool = False) -> List[MarketplaceListing]:
        """Match multiple listings in batch"""
        return [self.match_listing(listing, require_base) for listing in listings]
    
    def get_match_statistics(self, results: List[MarketplaceListing]) -> Dict:
        """Generate statistics on matching results"""
        total = len(results)
        matched = sum(1 for r in results if r.final_match)
        high_conf = sum(1 for r in results if r.match_confidence >= 0.7)
        
        methods = defaultdict(int)
        coin_types = defaultdict(int)
        
        for result in results:
            if result.match_method:
                methods[result.match_method] += 1
            
            if result.extracted_features.get('coin_type'):
                coin_types[result.extracted_features['coin_type']] += 1
        
        return {
            'total_listings': total,
            'successfully_matched': matched,
            'match_rate': matched / total if total > 0 else 0,
            'high_confidence': high_conf,
            'high_conf_rate': high_conf / total if total > 0 else 0,
            'match_methods': dict(methods),
            'coin_types': dict(coin_types)
        }

# Command-line interface
if __name__ == "__main__":
    matcher = MarketplaceListingMatcher()
    
    # Test with various marketplace-style listings (with typos and variations)
    test_listings = [
        "1918d buffallo nickle 8 over 7",  # Typos
        "mercury dime 1942 denver mint ms65",
        "Two Cent Piece 1864 Lg Motto Proof",  # Abbreviation
        "1937 D bufalo 3 leg nickel vf",  # Multiple typos
        "lincoln wheat penney 1909 s vdb",  # Typo
        "Walking Liberty Half Dollar 1942-S AU58",
        "morgn dollar 1881 s ms64",  # Typo
        "washinton quarter 1932d key date",  # Typo
    ]
    
    print("Marketplace Listing Fuzzy Matching Results:")
    print("=" * 60)
    
    results = matcher.batch_match_listings(test_listings, require_base=True)
    
    for result, original in zip(results, test_listings):
        print(f"\nOriginal: {original}")
        print(f"  Normalized: {result.normalized_text}")
        print(f"  Features: Year={result.extracted_features['year']}, "
              f"Mint={result.extracted_features['mint_mark']}, "
              f"Type={result.extracted_features['coin_type']}")
        print(f"  Variants: {result.extracted_features['variants']}")
        print(f"  Match: {result.final_match}")
        print(f"  Confidence: {result.match_confidence:.2f}")
        print(f"  Method: {result.match_method}")
        
        if result.possible_matches and len(result.possible_matches) > 1:
            print(f"  Alternatives:")
            for alt_id, alt_score in result.possible_matches[1:3]:
                print(f"    - {alt_id}: {alt_score:.2f}")
    
    stats = matcher.get_match_statistics(results)
    print(f"\n📊 Statistics:")
    print(f"  Total: {stats['total_listings']}")
    print(f"  Matched: {stats['successfully_matched']} ({stats['match_rate']:.1%})")
    print(f"  High Confidence: {stats['high_confidence']} ({stats['high_conf_rate']:.1%})")