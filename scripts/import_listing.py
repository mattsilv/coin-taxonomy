#!/usr/bin/env python3
"""
Match marketplace listings to canonical coin taxonomy.
Automatically detects country when possible.
"""

import re
import sqlite3
import json

class ListingMatcher:
    def __init__(self, db_path='database/coins.db'):
        self.conn = sqlite3.connect(db_path)
        self.load_grade_mappings()
    
    def load_grade_mappings(self):
        """Load grade word mappings from database"""
        self.grade_map = {}
        cursor = self.conn.execute('SELECT grade_word, abbreviation FROM grades')
        for row in cursor:
            self.grade_map[row[0].lower()] = row[0]
            if row[1]:
                self.grade_map[row[1].lower()] = row[0]
        
        # Add common variations
        self.grade_map.update({
            'unc': 'Uncirculated',
            'bu': 'Uncirculated',
            'brilliant uncirculated': 'Uncirculated',
            'xf': 'Extremely Fine',
            'ef': 'Extremely Fine',
            'vf': 'Very Fine',
            'f': 'Fine',
            'vg': 'Very Good',
            'g': 'Good',
            'ag': 'About Good',
            'au': 'About Uncirculated'
        })
    
    def detect_country(self, text):
        """Try to detect country from listing text"""
        # Country indicators
        indicators = {
            'US': ['united states', 'usa', 'us ', 'american', 'liberty', 'cent', 
                   'nickel', 'dime', 'quarter', 'half dollar', 'dollar'],
            'CA': ['canada', 'canadian', 'maple leaf', 'loonie', 'toonie'],
            'UK': ['british', 'britain', 'england', 'pound', 'pence', 'shilling'],
            'MX': ['mexico', 'mexican', 'peso', 'aztec']
        }
        
        text_lower = text.lower()
        for country, keywords in indicators.items():
            if any(kw in text_lower for kw in keywords):
                return country
        
        # Default to US if unclear
        return 'US'
    
    def extract_year(self, text):
        """Extract year from listing text"""
        years = re.findall(r'\b(1[7-9]\d{2}|20\d{2})\b', text)
        if years:
            return int(years[0])
        return None
    
    def extract_mint_mark(self, text):
        """Extract mint mark from listing text"""
        # Direct mint mark patterns
        patterns = [
            r'(\d{4})\s*[-/]?\s*([PDSOCC]+)\b',  # Year-mint pattern like 1916-D
            r'\b([PDSOCC])\s+mint\b',  # P mint, D mint pattern
            r'(\d{4})([PDSOCC])\b'  # Attached like 1937D
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(match.lastindex).upper()
        
        return 'P'  # Default to Philadelphia for US
    
    def extract_grade(self, text):
        """Extract grade from listing text"""
        text_lower = text.lower()
        
        # Check each grade mapping
        for key, grade in sorted(self.grade_map.items(), 
                                key=lambda x: len(x[0]), reverse=True):
            if key in text_lower:
                return grade
        
        return None
    
    def match_listing(self, listing_text):
        """
        Match a listing to canonical coin data.
        Returns dict with matched coin info and confidence score.
        """
        result = {
            'input': listing_text,
            'country': self.detect_country(listing_text),
            'year': self.extract_year(listing_text),
            'mint': self.extract_mint_mark(listing_text),
            'grade': self.extract_grade(listing_text),
            'matches': [],
            'confidence': 0
        }
        
        if not result['year']:
            return result
        
        # Search database
        query = '''
            SELECT DISTINCT country, denomination, series, year, mint, mintage
            FROM coins
            WHERE year = ? AND country = ?
        '''
        params = [result['year'], result['country']]
        
        if result['mint']:
            query += ' AND mint = ?'
            params.append(result['mint'])
        
        matches = self.conn.execute(query, params).fetchall()
        
        # Try to identify series from listing text
        text_lower = listing_text.lower()
        
        # Common series keywords
        series_keywords = {
            'mercury': 'Mercury Dime',
            'winged liberty': 'Mercury Dime',
            'roosevelt': 'Roosevelt Dime',
            'barber': ['Barber Dime', 'Barber Quarter', 'Barber Half Dollar'],
            'indian': 'Indian Head Cent',
            'wheat': 'Lincoln Cent',
            'buffalo': 'Buffalo Nickel',
            'jefferson': 'Jefferson Nickel',
            'washington': 'Washington Quarter',
            'standing liberty': 'Standing Liberty Quarter',
            'walking liberty': 'Walking Liberty Half Dollar',
            'franklin': 'Franklin Half Dollar',
            'kennedy': 'Kennedy Half Dollar',
            'morgan': 'Morgan Dollar',
            'peace': 'Peace Dollar'
        }
        
        for keyword, series_match in series_keywords.items():
            if keyword in text_lower:
                # Filter matches to this series
                if isinstance(series_match, list):
                    filtered = [m for m in matches if m[2] in series_match]
                else:
                    filtered = [m for m in matches if m[2] == series_match]
                
                if filtered:
                    result['matches'] = filtered
                    result['confidence'] = 0.9
                    break
        
        if not result['matches']:
            result['matches'] = matches
            result['confidence'] = 0.5 if matches else 0.0
        
        return result

def main():
    matcher = ListingMatcher()
    
    # Test examples
    test_listings = [
        "1916-D Mercury Dime Good condition",
        "1943 Steel Wheat Penny",
        "Canada 1967 Centennial Quarter",
        "Morgan Dollar 1921 S Mint Mark AU",
        "Indian Head Cent 1906 Fine",
        "Buffalo Nickel 1937D VF",
    ]
    
    for listing in test_listings:
        result = matcher.match_listing(listing)
        print(f"\nListing: {listing}")
        print(f"Country: {result['country']}")
        print(f"Parsed: Year={result['year']}, Mint={result['mint']}, Grade={result['grade']}")
        print(f"Confidence: {result['confidence']}")
        if result['matches']:
            for match in result['matches']:
                print(f"  - {match[0]} {match[1]} {match[2]}")

if __name__ == "__main__":
    main()