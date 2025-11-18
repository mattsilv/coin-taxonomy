#!/usr/bin/env python3
"""
Add Engelhard Bullion to Taxonomy (Issue #67)

Parses Engelhard data and adds it to the coins database.
"""

import sqlite3
import json
import csv
import io
import re

# Data from Issue #67
# Data will be read from issue_67.txt
ENGELHARD_CSV = ""

def parse_year(text):
    """Extract year from text, default to XXXX."""
    match = re.search(r'\\b(19\\d{2})\\b', text)
    if match:
        return int(match.group(1))
    return 'XXXX'

def clean_mintage(text):
    """Clean mintage text."""
    if not text or text == 'N/A':
        return None
    # Remove <, >, and commas
    clean = text.replace('<', '').replace('>', '').replace(',', '')
    try:
        return int(clean)
    except ValueError:
        return None

def add_engelhard_bullion():
    """Add Engelhard bullion to database."""
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    
    # Read from issue_67.txt
    with open('issue_67.txt', 'r') as f:
        csv_content = f.read()
        
    reader = csv.DictReader(io.StringIO(csv_content))
    
    count = 0
    for i, row in enumerate(reader, start=1):
        # Generate concise ID following 4-part COUNTRY-TYPE-YEAR-MINT format
        # Use zero-padded numeric suffix (EN01, EN02, etc.) to maintain 4-char TYPE code
        year = parse_year(row['commentary'])
        variety_num = str(i).zfill(2)  # Zero-pad to 2 digits
        coin_id = f"US-EN{variety_num}-{year}-X"

        # Store full variety name in series field
        series_name = row['name']

        # Composition
        composition = json.dumps({"silver": 0.999})

        # Notes - include variety details
        notes = f"{row['commentary']} Sample Serials: {row['sample_serials']}. Estimated Mintage: {row['estimated_mintage']}"

        # Mintage (store 0 if unknown/estimate, but we put estimate in notes)
        mintage = 0

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO coins (
                    coin_id, denomination, series, year, mint,
                    composition, weight_grams, diameter_mm,
                    proof_strikes, variety, source_citation, notes,
                    obverse_description, reverse_description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin_id,
                "Engelhard Bullion",  # Custom denomination to group them
                series_name,  # Full variety name stored here
                str(year),
                "X",  # Unspecified mint (like American Eagles)
                composition,
                31.103,  # 1 oz assumed for most
                None,  # Diameter unknown
                0,
                None,  # Variety field - can be null, details are in series/notes
                "Engelhard Production Records",
                notes,
                row['obverse_desc'],
                row['reverse_desc']
            ))
            count += 1
            print(f"✅ Added: {coin_id}")
        except sqlite3.Error as e:
            print(f"❌ Error adding {coin_id}: {e}")

    conn.commit()
    conn.close()
    print(f"\\nSuccessfully added {count} Engelhard items.")

if __name__ == "__main__":
    add_engelhard_bullion()
