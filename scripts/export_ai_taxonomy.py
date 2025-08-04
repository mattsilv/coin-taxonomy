#!/usr/bin/env python3
"""
AI-Optimized Taxonomy Export
Creates minimal taxonomy format optimized for AI/ML coin classification.

This script generates a token-optimized JSON format that:
- Minimizes file size by 60-70% vs complete format
- Uses abbreviated field names to save tokens
- Excludes non-essential data (detailed specs, citations, etc.)
- Focuses on essential classification features only
"""

import sqlite3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

class AITaxonomyExporter:
    def __init__(self, db_path="database/coins.db", output_dir="data/ai-optimized", use_year_lists=True):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.use_year_lists = use_year_lists  # Toggle: True = comma-delimited years, False = full coin IDs
        
    def extract_type_code(self, coin_id):
        """Extract 4-letter type code from coin_id (US-INCH-1877-P -> INCH)"""
        try:
            parts = coin_id.split('-')
            if len(parts) >= 4:
                return parts[1]  # TYPE code is second part
            return None
        except:
            return None
    
    def process_varieties(self, varieties_json):
        """Convert varieties JSON to simple array of variety names"""
        if not varieties_json:
            return None
        
        try:
            varieties = json.loads(varieties_json) if isinstance(varieties_json, str) else varieties_json
            if not varieties or len(varieties) == 0:
                return None
                
            # Extract just the variety names, not full objects
            variety_names = []
            for variety in varieties:
                if isinstance(variety, dict) and 'name' in variety:
                    variety_names.append(variety['name'])
                elif isinstance(variety, str):
                    variety_names.append(variety)
            
            return variety_names if variety_names else None
        except:
            return None
    
    def get_series_year_ranges(self, cursor):
        """Get the actual production year ranges for each series based on database data"""
        query = """
        SELECT 
            series_id,
            MIN(year) as start_year,
            MAX(year) as end_year,
            COUNT(DISTINCT year) as actual_years,
            GROUP_CONCAT(DISTINCT year ORDER BY year) as existing_years
        FROM coins 
        GROUP BY series_id
        """
        cursor.execute(query)
        series_ranges = {}
        
        for row in cursor.fetchall():
            series_id, start_year, end_year, actual_years, existing_years = row
            series_ranges[series_id] = {
                'start_year': start_year,
                'end_year': end_year,
                'actual_years': actual_years,
                'existing_years': existing_years.split(',') if existing_years else []
            }
        
        return series_ranges

    def generate_complete_year_list(self, start_year, end_year):
        """Generate comma-delimited string of all years in range"""
        if not start_year or not end_year:
            return None
        
        years = list(range(int(start_year), int(end_year) + 1))
        return ','.join(map(str, years))
    
    def generate_complete_coin_ids(self, series_id, start_year, end_year, type_code):
        """Generate complete list of coin IDs for all year/mint combinations"""
        if not start_year or not end_year or not type_code:
            return None
        
        # Standard US mint marks (P, D, S, W for modern; historical ones like CC, O for older series)
        # We'll determine appropriate mints based on year ranges
        mint_marks = []
        
        if end_year >= 1965:  # Modern era - P, D, S, W
            mint_marks = ['P', 'D', 'S']
            if end_year >= 1986:  # West Point started 1986
                mint_marks.append('W')
        elif start_year >= 1900:  # Early modern era - P, D, S
            mint_marks = ['P', 'D', 'S']
        elif start_year >= 1850:  # Historical era including CC, O
            mint_marks = ['P', 'D', 'S', 'CC', 'O']
        else:  # Early era - mainly Philadelphia
            mint_marks = ['P']
        
        # Generate all combinations
        coin_ids = []
        for year in range(int(start_year), int(end_year) + 1):
            for mint in mint_marks:
                coin_id = f"US-{type_code}-{year}-{mint}"
                coin_ids.append(coin_id)
        
        return ','.join(coin_ids)

    def export_ai_taxonomy(self):
        """Export AI-optimized taxonomy with complete year coverage"""
        print("🤖 Exporting AI-optimized taxonomy with complete year coverage...")
        
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get series year ranges first
        series_ranges = self.get_series_year_ranges(cursor)
        
        # Query essential fields including visual descriptions, grouped by series
        query = """
        SELECT 
            series_id,
            series_name,
            coin_id,
            year,
            mint,
            rarity,
            varieties,
            notes,
            obverse_description,
            reverse_description,
            distinguishing_features,
            identification_keywords,
            common_names
        FROM coins
        ORDER BY series_id, year
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Group coins by series for processing
        series_data = {}
        for row in rows:
            series_id, series_name, coin_id, year, mint, rarity, varieties, notes, obverse_desc, reverse_desc, features, keywords, names = row
            
            if series_id not in series_data:
                series_data[series_id] = {
                    'series_name': series_name,
                    'coins': [],
                    'prototype_coin': None  # We'll use first coin as template
                }
            
            coin_record = {
                'coin_id': coin_id, 'year': year, 'mint': mint, 'rarity': rarity,
                'varieties': varieties, 'notes': notes, 'obverse_desc': obverse_desc,
                'reverse_desc': reverse_desc, 'features': features, 
                'keywords': keywords, 'names': names
            }
            
            series_data[series_id]['coins'].append(coin_record)
            
            # Use first coin as prototype for series
            if series_data[series_id]['prototype_coin'] is None:
                series_data[series_id]['prototype_coin'] = coin_record
        
        # Process each series and create series-level records with complete year coverage
        series_records = []
        total_coins_represented = 0
        
        for series_id, data in series_data.items():
            prototype = data['prototype_coin']
            series_name = data['series_name']
            
            # Get year range for this series
            year_range = series_ranges.get(series_id, {})
            start_year = year_range.get('start_year')
            end_year = year_range.get('end_year')
            
            # Extract type code from prototype first
            type_code = self.extract_type_code(prototype['coin_id'])
            if not type_code:
                continue
                
            # Create series record using prototype coin as template
            series_record = {
                "series": series_id,
                "s": series_name,
                "t": type_code,
                "year_range": f"{start_year}-{end_year}",
                "total_years": end_year - start_year + 1 if start_year and end_year else 0
            }
            
            # Choose approach based on configuration
            if self.use_year_lists:
                # APPROACH 1: Comma-delimited year list (more efficient)
                complete_years = self.generate_complete_year_list(start_year, end_year)
                if complete_years:
                    series_record["years"] = complete_years
                else:
                    continue
            else:
                # APPROACH 2: Complete coin ID list (comprehensive but verbose)
                complete_coin_ids = self.generate_complete_coin_ids(series_id, start_year, end_year, type_code)
                if complete_coin_ids:
                    series_record["coin_ids"] = complete_coin_ids  # Complete coin ID coverage
                else:
                    continue
            
            # Add visual descriptions from prototype (these should be consistent across series)
            if prototype['obverse_desc'] and len(prototype['obverse_desc'].strip()) > 0:
                series_record["ob"] = prototype['obverse_desc'].strip()
            
            if prototype['reverse_desc'] and len(prototype['reverse_desc'].strip()) > 0:
                series_record["rv"] = prototype['reverse_desc'].strip()
            
            # Add distinguishing features from prototype
            if prototype['features']:
                try:
                    features_list = json.loads(prototype['features']) if isinstance(prototype['features'], str) else prototype['features']
                    if features_list and len(features_list) > 0:
                        series_record["df"] = features_list
                except:
                    pass
            
            # Add identification keywords from prototype
            if prototype['keywords']:
                try:
                    keywords_list = json.loads(prototype['keywords']) if isinstance(prototype['keywords'], str) else prototype['keywords']
                    if keywords_list and len(keywords_list) > 0:
                        series_record["kw"] = keywords_list
                except:
                    pass
            
            # Add common names from prototype
            if prototype['names']:
                try:
                    names_list = json.loads(prototype['names']) if isinstance(prototype['names'], str) else prototype['names']
                    if names_list and len(names_list) > 0:
                        series_record["cn"] = names_list
                except:
                    pass
            
            # Collect key dates and varieties from actual coins in database
            key_dates = []
            all_varieties = set()
            
            for coin in data['coins']:
                # Collect key dates (non-common rarities)
                if coin['rarity'] and coin['rarity'] != 'common':
                    key_dates.append({
                        'year': coin['year'],
                        'mint': coin['mint'], 
                        'rarity': coin['rarity'],
                        'notes': coin['notes'][:50] + '...' if coin['notes'] and len(coin['notes']) > 50 else coin['notes']
                    })
                
                # Collect varieties
                if coin['varieties']:
                    variety_names = self.process_varieties(coin['varieties'])
                    if variety_names:
                        all_varieties.update(variety_names)
            
            # Add key dates if any
            if key_dates:
                series_record["key_dates"] = key_dates
            
            # Add varieties if any
            if all_varieties:
                series_record["v"] = list(all_varieties)
            
            series_records.append(series_record)
            total_coins_represented += series_record["total_years"]
        
        print(f"📊 Generated {len(series_records)} series covering {total_coins_represented} coin-years")
        
        # Create AI-optimized taxonomy structure with series-based format
        approach_description = "comma-delimited year lists" if self.use_year_lists else "complete coin ID lists"
        format_version = "ai-taxonomy-v2-years" if self.use_year_lists else "ai-taxonomy-v2-coinids"
        
        # Dynamic field abbreviations based on approach
        field_abbreviations = {
            "series": "series_id (database identifier)",
            "s": "series_name (human-readable)",
            "t": "type_code (4-letter abbreviation)",
            "year_range": "human-readable year range (e.g. '1909-1958')",
            "total_years": "total number of years in production",
            "ob": "obverse_description (visual description of front/heads side)",
            "rv": "reverse_description (visual description of back/tails side)",
            "df": "distinguishing_features (array of key identifying characteristics)",
            "kw": "identification_keywords (array of search terms and descriptors)",
            "cn": "common_names (array of popular names for this series)",
            "key_dates": "specific coins with non-common rarity",
            "v": "varieties (array of major variety names)"
        }
        
        if self.use_year_lists:
            field_abbreviations["years"] = "comma-delimited string of all production years"
        else:
            field_abbreviations["coin_ids"] = "complete comma-delimited list of all possible coin IDs for this series"
        
        taxonomy = {
            "format": format_version,
            "country": "US",
            "generated": datetime.now(timezone.utc).isoformat(),
            "approach": approach_description,
            "total_series": len(series_records),
            "total_coin_years": total_coins_represented,
            "metadata": {
                "purpose": f"Series-based taxonomy with complete year coverage using {approach_description} for AI/ML coin classification", 
                "field_abbreviations": field_abbreviations,
                "optimization_strategies": [
                    "Series-based grouping reduces redundancy",
                    f"Complete year coverage via {approach_description}", 
                    "Key date exceptions highlighted separately",
                    "Abbreviated field names to reduce token usage",
                    "Omit null/empty values for compactness",
                    "Compact JSON formatting (no indentation)"
                ]
            },
            "series": series_records
        }
        
        # Write main taxonomy file with embedded metadata
        # Use different filename based on approach to preserve existing implementations
        if self.use_year_lists:
            output_file = self.output_dir / "us_taxonomy_year_list.json"
        else:
            output_file = self.output_dir / "us_taxonomy.json"  # Keep original name for coin ID approach
            
        with open(output_file, 'w') as f:
            # Compact JSON - no indentation to minimize size
            json.dump(taxonomy, f, separators=(',', ':'))
        
        # Calculate size stats  
        file_size = output_file.stat().st_size
        print(f"✅ AI-optimized taxonomy exported: {output_file}")
        print(f"📏 File size: {file_size:,} bytes ({file_size/1024:.1f}KB)")
        print(f"🎯 Total series: {len(series_records)}")
        print(f"🪙 Total coin-years covered: {total_coins_represented}")
        print(f"🔧 Approach: {approach_description}")
        
        # Calculate coverage statistics based on approach
        if self.use_year_lists:
            total_years = sum(len(record.get("years", "").split(",")) for record in series_records if record.get("years"))
            print(f"📅 Total years generated: {total_years:,}")
        else:
            total_coin_ids = sum(len(record.get("coin_ids", "").split(",")) for record in series_records if record.get("coin_ids"))
            print(f"🏷️  Total coin IDs generated: {total_coin_ids:,}")
        
        # Compare to complete format if it exists
        complete_file = Path("data/us/us_coins_complete.json")
        if complete_file.exists():
            complete_size = complete_file.stat().st_size
            reduction = ((complete_size - file_size) / complete_size) * 100 if complete_size > 0 else 0
            print(f"📊 Size vs complete format: {file_size:,} bytes (complete: {complete_size:,} bytes)")
        
        conn.close()
        return output_file, len(series_records)

def export_both_formats():
    """Export both year-list and coin-ID formats to preserve existing implementations"""
    print("🚀 Exporting both AI taxonomy formats...")
    
    # Export year-list version (new, more efficient)
    print("\n📅 Generating year-list format (efficient)...")
    year_exporter = AITaxonomyExporter(use_year_lists=True)
    year_file, year_series = year_exporter.export_ai_taxonomy()
    
    # Export coin-ID version (original format for compatibility)
    print("\n🏷️  Generating coin-ID format (comprehensive, for existing implementations)...")
    coinid_exporter = AITaxonomyExporter(use_year_lists=False)
    coinid_file, coinid_series = coinid_exporter.export_ai_taxonomy()
    
    print(f"\n✅ Both formats exported successfully:")
    print(f"   📅 Year-list format: {year_file}")
    print(f"   🏷️  Coin-ID format:  {coinid_file}")
    
    return year_file, coinid_file

def main():
    """Main export function"""
    # Configuration: Choose export mode
    EXPORT_BOTH = True  # Set to True to generate both formats, False for single format
    
    if EXPORT_BOTH:
        export_both_formats()
    else:
        # Single format export (for development/testing)
        USE_YEAR_LISTS = True  # Default: Use year lists (more efficient)
        
        print(f"🚀 Starting AI taxonomy export with {'YEAR LISTS' if USE_YEAR_LISTS else 'COIN ID LISTS'} approach...")
        
        exporter = AITaxonomyExporter(use_year_lists=USE_YEAR_LISTS)
        exporter.export_ai_taxonomy()

if __name__ == "__main__":
    main()