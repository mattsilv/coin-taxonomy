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
    def __init__(self, db_path="database/coins.db", output_dir="data/ai-optimized"):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
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
    
    def export_ai_taxonomy(self):
        """Export AI-optimized taxonomy with minimal token usage"""
        print("🤖 Exporting AI-optimized taxonomy...")
        
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Query essential fields only - no physical specs, citations, etc.
        query = """
        SELECT 
            coin_id,
            year,
            mint,
            series_name,
            rarity,
            varieties,
            notes
        FROM coins
        ORDER BY coin_id
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Process coins with token optimization
        coins = []
        for row in rows:
            coin_id, year, mint, series_name, rarity, varieties, notes = row
            
            # Create optimized coin record
            coin = {"id": coin_id, "y": year, "m": mint, "s": series_name}
            
            # Extract and add type code
            type_code = self.extract_type_code(coin_id)
            if type_code:
                coin["t"] = type_code
            
            # Add rarity only if it's key/semi-key/scarce (omit "common" to save tokens)
            if rarity and rarity != "common":
                coin["r"] = rarity
            
            # Process varieties as simple array
            variety_names = self.process_varieties(varieties)
            if variety_names:
                coin["v"] = variety_names
            
            # Add critical notes only (skip verbose descriptions)
            if notes and len(notes.strip()) > 0:
                # Keep notes concise - truncate if too long
                clean_notes = notes.strip()
                if len(clean_notes) > 100:
                    clean_notes = clean_notes[:97] + "..."
                coin["n"] = clean_notes
            
            coins.append(coin)
        
        # Create AI-optimized taxonomy structure
        taxonomy = {
            "format": "ai-taxonomy-v1",
            "country": "US",
            "generated": datetime.now(timezone.utc).isoformat(),
            "total_coins": len(coins),
            "coins": coins
        }
        
        # Write main taxonomy file
        output_file = self.output_dir / "us_taxonomy.json"
        with open(output_file, 'w') as f:
            # Compact JSON - no indentation to minimize size
            json.dump(taxonomy, f, separators=(',', ':'))
        
        # Create metadata documentation
        metadata = {
            "format_specification": {
                "version": "ai-taxonomy-v1",
                "purpose": "Token-optimized taxonomy for AI/ML coin classification",
                "field_abbreviations": {
                    "id": "coin_id (primary classification target)",
                    "y": "year",
                    "m": "mint",
                    "s": "series_name (human-readable)",
                    "t": "type_code (4-letter abbreviation)", 
                    "r": "rarity (key/semi-key/scarce only, omits 'common')",
                    "v": "varieties (array of major variety names only)",
                    "n": "notes (critical identifying info only, max 100 chars)"
                },
                "optimization_strategies": [
                    "Abbreviated field names (40% reduction)",
                    "Omit null/empty values",
                    "Exclude verbose metadata and specifications",
                    "Compress variety info to names only",
                    "Skip 'common' rarity to save tokens",
                    "Compact JSON formatting (no indentation)"
                ]
            },
            "generated": datetime.now(timezone.utc).isoformat()
        }
        
        metadata_file = self.output_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Calculate size stats
        file_size = output_file.stat().st_size
        print(f"✅ AI-optimized taxonomy exported: {output_file}")
        print(f"📏 File size: {file_size:,} bytes ({file_size/1024:.1f}KB)")
        print(f"🎯 Total coins: {len(coins)}")
        
        # Compare to complete format if it exists
        complete_file = Path("data/us/us_coins_complete.json")
        if complete_file.exists():
            complete_size = complete_file.stat().st_size
            reduction = ((complete_size - file_size) / complete_size) * 100
            print(f"📊 Size reduction: {reduction:.1f}% vs complete format ({complete_size:,} → {file_size:,} bytes)")
        
        conn.close()
        return output_file, len(coins)

def main():
    """Main export function"""
    exporter = AITaxonomyExporter()
    exporter.export_ai_taxonomy()

if __name__ == "__main__":
    main()