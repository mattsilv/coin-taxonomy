#!/usr/bin/env python3
"""
Migration script to add complete Lincoln Memorial Cent series (1959-2008)

This script implements the comprehensive research data from Issue #20,
adding 171 Lincoln Memorial Cent varieties covering the complete series
from 1959-2008 including all major varieties and composition changes.
"""

import sqlite3
import json
import csv
import os
from datetime import datetime

def main():
    print("🪙 Adding Lincoln Memorial Cent Series (1959-2008)")
    print("📊 Data source: Issue #20 AI Research")
    
    # Database connection
    db_path = "database/coins.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Step 1: Remove existing incomplete Lincoln Memorial Cent records
        print("\n🗑️  Removing existing incomplete Lincoln Memorial Cent records...")
        cursor.execute("SELECT COUNT(*) FROM coins WHERE series_id = 'lincoln_memorial_cent'")
        existing_count = cursor.fetchone()[0]
        print(f"📄 Found {existing_count} existing records to remove")
        
        cursor.execute("DELETE FROM coins WHERE series_id = 'lincoln_memorial_cent'")
        print(f"✅ Removed {existing_count} existing records")
        
        # Step 2: Load and process CSV data
        print("\n📁 Loading Lincoln Memorial Cent data from CSV...")
        
        # CSV data as embedded content (from AI research)
        # Note: Converting LMC to LMCT to match database constraint (4-letter type codes)
        csv_data = """year,mint_mark,coin_id,composition,weight_grams,rarity_classification,key_dates_varieties
1959,P,US-LMCT-1959-P,"95% copper, 5% zinc (brass)",3.11,common,None
1959,D,US-LMC-1959-D,"95% copper, 5% zinc (brass)",3.11,common,None
1959,S,US-LMC-1959-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1960,P,US-LMC-1960-P-LD,"95% copper, 5% zinc (brass)",3.11,common,1960 Large Date variety
1960,P,US-LMC-1960-P-SD,"95% copper, 5% zinc (brass)",3.11,semi-key,1960 Small Date variety (scarce)
1960,D,US-LMC-1960-D-LD,"95% copper, 5% zinc (brass)",3.11,common,1960-D Large Date variety
1960,D,US-LMC-1960-D-SD,"95% copper, 5% zinc (brass)",3.11,common,1960-D Small Date variety
1960,D,US-LMC-1960-D-RPM,"95% copper, 5% zinc (brass)",3.11,semi-key,1960-D D over D Large Date (semi-key)
1960,S,US-LMC-1960-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1961,P,US-LMC-1961-P,"95% copper, 5% zinc (brass)",3.11,common,None
1961,D,US-LMC-1961-D,"95% copper, 5% zinc (brass)",3.11,common,None
1961,S,US-LMC-1961-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1962,P,US-LMC-1962-P,"95% copper, 5% zinc (brass)",3.11,common,None
1962,D,US-LMC-1962-D,"95% copper, 5% zinc (brass)",3.11,common,None
1962,S,US-LMC-1962-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1963,P,US-LMC-1963-P,"95% copper, 5% zinc (brass)",3.11,common,None
1963,D,US-LMC-1963-D,"95% copper, 5% zinc (brass)",3.11,common,None
1963,S,US-LMC-1963-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1964,P,US-LMC-1964-P,"95% copper, 5% zinc (brass)",3.11,common,None
1964,D,US-LMC-1964-D,"95% copper, 5% zinc (brass)",3.11,common,None
1964,S,US-LMC-1964-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1965,P,US-LMC-1965-P,"95% copper, 5% zinc (brass)",3.11,common,Regular circulation strike
1965,SMS,US-LMC-1965-SMS,"95% copper, 5% zinc (brass)",3.11,scarce,"1965 Special Mint Set (special finish, no mint mark)"
1965,D,US-LMC-1965-D,"95% copper, 5% zinc (brass)",3.11,common,None
1965,S,US-LMC-1965-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1966,P,US-LMC-1966-P,"95% copper, 5% zinc (brass)",3.11,common,Regular circulation strike
1966,SMS,US-LMC-1966-SMS,"95% copper, 5% zinc (brass)",3.11,scarce,"1966 Special Mint Set (special finish, no mint mark)"
1966,D,US-LMC-1966-D,"95% copper, 5% zinc (brass)",3.11,common,None
1966,S,US-LMC-1966-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1967,P,US-LMC-1967-P,"95% copper, 5% zinc (brass)",3.11,common,Regular circulation strike
1967,SMS,US-LMC-1967-SMS,"95% copper, 5% zinc (brass)",3.11,scarce,"1967 Special Mint Set (special finish, no mint mark)"
1967,D,US-LMC-1967-D,"95% copper, 5% zinc (brass)",3.11,common,None
1967,S,US-LMC-1967-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1968,P,US-LMC-1968-P,"95% copper, 5% zinc (brass)",3.11,common,None
1968,D,US-LMC-1968-D,"95% copper, 5% zinc (brass)",3.11,common,None
1968,S,US-LMC-1968-S,"95% copper, 5% zinc (brass)",3.11,semi-key,1968-S (lowest mintage Memorial cent)
1969,P,US-LMC-1969-P,"95% copper, 5% zinc (brass)",3.11,common,Regular strike
1969,D,US-LMC-1969-D,"95% copper, 5% zinc (brass)",3.11,common,None
1969,S,US-LMC-1969-S,"95% copper, 5% zinc (brass)",3.11,common,Regular strike
1969,S,US-LMC-1969-S-DDO,"95% copper, 5% zinc (brass)",3.11,key,"1969-S Doubled Die Obverse (key date, 30-50 known)"
1970,P,US-LMC-1970-P,"95% copper, 5% zinc (brass)",3.11,common,None
1970,D,US-LMC-1970-D,"95% copper, 5% zinc (brass)",3.11,common,None
1970,S,US-LMC-1970-S-LD,"95% copper, 5% zinc (brass)",3.11,common,1970-S Large Date 'Low 7'
1970,S,US-LMC-1970-S-SD,"95% copper, 5% zinc (brass)",3.11,semi-key,1970-S Small Date 'High 7' (semi-key)
1971,P,US-LMC-1971-P,"95% copper, 5% zinc (brass)",3.11,common,Regular strike
1971,P,US-LMC-1971-P-DDO,"95% copper, 5% zinc (brass)",3.11,key,1971 Doubled Die Obverse (key date)
1971,D,US-LMC-1971-D,"95% copper, 5% zinc (brass)",3.11,common,None
1971,S,US-LMC-1971-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1972,P,US-LMC-1972-P,"95% copper, 5% zinc (brass)",3.11,common,Regular strike
1972,P,US-LMC-1972-P-DDO,"95% copper, 5% zinc (brass)",3.11,key,1972 Doubled Die Obverse Type 1 (key date)
1972,D,US-LMC-1972-D,"95% copper, 5% zinc (brass)",3.11,common,None
1972,S,US-LMC-1972-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1973,P,US-LMC-1973-P,"95% copper, 5% zinc (brass)",3.11,common,None
1973,D,US-LMC-1973-D,"95% copper, 5% zinc (brass)",3.11,common,None
1973,S,US-LMC-1973-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1974,P,US-LMC-1974-P,"95% copper, 5% zinc (brass)",3.11,common,None
1974,D,US-LMC-1974-D,"95% copper, 5% zinc (brass)",3.11,common,None
1974,S,US-LMC-1974-S,"95% copper, 5% zinc (brass)",3.11,common,Business strike
1975,P,US-LMC-1975-P,"95% copper, 5% zinc (brass)",3.11,common,None
1975,D,US-LMC-1975-D,"95% copper, 5% zinc (brass)",3.11,common,None
1975,S,US-LMC-1975-S,"95% copper, 5% zinc (brass)",3.11,common,Proof only
1976,P,US-LMC-1976-P,"95% copper, 5% zinc (brass)",3.11,common,None
1976,D,US-LMC-1976-D,"95% copper, 5% zinc (brass)",3.11,common,None
1976,S,US-LMC-1976-S,"95% copper, 5% zinc (brass)",3.11,common,Proof only
1977,P,US-LMC-1977-P,"95% copper, 5% zinc (brass)",3.11,common,None
1977,D,US-LMC-1977-D,"95% copper, 5% zinc (brass)",3.11,common,None
1977,S,US-LMC-1977-S,"95% copper, 5% zinc (brass)",3.11,common,Proof only
1978,P,US-LMC-1978-P,"95% copper, 5% zinc (brass)",3.11,common,None
1978,D,US-LMC-1978-D,"95% copper, 5% zinc (brass)",3.11,common,None
1978,S,US-LMC-1978-S,"95% copper, 5% zinc (brass)",3.11,common,Proof only
1979,P,US-LMC-1979-P,"95% copper, 5% zinc (brass)",3.11,common,None
1979,D,US-LMC-1979-D,"95% copper, 5% zinc (brass)",3.11,common,None
1979,S,US-LMC-1979-S,"95% copper, 5% zinc (brass)",3.11,common,Proof only
1980,P,US-LMC-1980-P,"95% copper, 5% zinc (brass)",3.11,common,None
1980,D,US-LMC-1980-D,"95% copper, 5% zinc (brass)",3.11,common,None
1980,S,US-LMC-1980-S,"95% copper, 5% zinc (brass)",3.11,common,Proof only
1981,P,US-LMC-1981-P,"95% copper, 5% zinc (brass)",3.11,common,None
1981,D,US-LMC-1981-D,"95% copper, 5% zinc (brass)",3.11,common,None
1981,S,US-LMC-1981-S,"95% copper, 5% zinc (brass)",3.11,common,Proof only
1982,P,US-LMC-1982-P-LD-Cu,"95% copper, 5% zinc (brass)",3.11,common,1982 Large Date Copper
1982,P,US-LMC-1982-P-SD-Cu,"95% copper, 5% zinc (brass)",3.11,scarce,1982 Small Date Copper (scarce)
1982,P,US-LMC-1982-P-LD-Zn,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,1982 Large Date Zinc
1982,P,US-LMC-1982-P-SD-Zn,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,key,1982 Small Date Zinc (very rare)
1982,D,US-LMC-1982-D-LD-Cu,"95% copper, 5% zinc (brass)",3.11,common,1982-D Large Date Copper
1982,D,US-LMC-1982-D-SD-Cu,"95% copper, 5% zinc (brass)",3.11,key,"1982-D Small Date Copper (extremely rare, 2 known)"
1982,D,US-LMC-1982-D-LD-Zn,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,1982-D Large Date Zinc (most common 1982)
1982,D,US-LMC-1982-D-SD-Zn,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,1982-D Small Date Zinc
1982,S,US-LMC-1982-S-Cu,"95% copper, 5% zinc (brass)",3.11,common,1982-S Copper (Proof only)
1983,P,US-LMC-1983-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Regular strike
1983,P,US-LMC-1983-P-DDR,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,semi-key,1983 Doubled Die Reverse (semi-key)
1983,P,US-LMC-1983-P-DDO,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,scarce,1983 Doubled Die Obverse
1983,D,US-LMC-1983-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1983,S,US-LMC-1983-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1984,P,US-LMC-1984-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Regular strike
1984,P,US-LMC-1984-P-DDO,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,semi-key,1984 Doubled Die Obverse 'Double Ear' (semi-key)
1984,D,US-LMC-1984-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1984,S,US-LMC-1984-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1985,P,US-LMC-1985-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1985,D,US-LMC-1985-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1985,S,US-LMC-1985-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1986,P,US-LMC-1986-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1986,D,US-LMC-1986-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1986,S,US-LMC-1986-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1987,P,US-LMC-1987-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1987,D,US-LMC-1987-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1987,S,US-LMC-1987-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1988,P,US-LMC-1988-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1988,D,US-LMC-1988-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1988,S,US-LMC-1988-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1989,P,US-LMC-1989-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1989,D,US-LMC-1989-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1989,S,US-LMC-1989-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1990,P,US-LMC-1990-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1990,D,US-LMC-1990-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1990,S,US-LMC-1990-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1991,P,US-LMC-1991-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1991,D,US-LMC-1991-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1991,S,US-LMC-1991-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1992,P,US-LMC-1992-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1992,D,US-LMC-1992-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1992,S,US-LMC-1992-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1993,P,US-LMC-1993-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1993,D,US-LMC-1993-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1993,S,US-LMC-1993-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1994,P,US-LMC-1994-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1994,D,US-LMC-1994-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1994,S,US-LMC-1994-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1995,P,US-LMC-1995-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Regular strike
1995,P,US-LMC-1995-P-DDO,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,semi-key,1995 Doubled Die Obverse (semi-key)
1995,D,US-LMC-1995-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Regular strike
1995,D,US-LMC-1995-D-DDO,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,scarce,1995-D Doubled Die Obverse (scarce)
1995,S,US-LMC-1995-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1996,P,US-LMC-1996-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1996,D,US-LMC-1996-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1996,S,US-LMC-1996-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1997,P,US-LMC-1997-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1997,D,US-LMC-1997-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1997,S,US-LMC-1997-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1998,P,US-LMC-1998-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1998,D,US-LMC-1998-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1998,S,US-LMC-1998-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
1999,P,US-LMC-1999-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1999,D,US-LMC-1999-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
1999,S,US-LMC-1999-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2000,P,US-LMC-2000-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2000,D,US-LMC-2000-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2000,S,US-LMC-2000-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2001,P,US-LMC-2001-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2001,D,US-LMC-2001-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2001,S,US-LMC-2001-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2002,P,US-LMC-2002-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2002,D,US-LMC-2002-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2002,S,US-LMC-2002-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2003,P,US-LMC-2003-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2003,D,US-LMC-2003-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2003,S,US-LMC-2003-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2004,P,US-LMC-2004-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2004,D,US-LMC-2004-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2004,S,US-LMC-2004-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2005,P,US-LMC-2005-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2005,D,US-LMC-2005-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2005,S,US-LMC-2005-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2006,P,US-LMC-2006-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2006,D,US-LMC-2006-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2006,S,US-LMC-2006-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2007,P,US-LMC-2007-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2007,D,US-LMC-2007-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2007,S,US-LMC-2007-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only
2008,P,US-LMC-2008-P,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2008,D,US-LMC-2008-D,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,None
2008,S,US-LMC-2008-S,"97.5% zinc, 2.5% copper (copper-plated zinc)",2.5,common,Proof only"""
        
        # Parse CSV data and fix coin IDs to match database constraint
        csv_data_fixed = csv_data.replace("US-LMC-", "US-LMCT-")
        lines = csv_data_fixed.strip().split('\n')
        csv_reader = csv.DictReader(lines)
        records = list(csv_reader)
        print(f"📊 Loaded {len(records)} Lincoln Memorial Cent records")
        
        # Step 3: Process and insert records
        print("\n💎 Processing Lincoln Memorial Cent records...")
        
        inserted_count = 0
        
        for record in records:
            year = int(record['year'])
            mint_mark = record['mint_mark']
            coin_id = record['coin_id']
            composition_text = record['composition'].strip('"')
            weight_grams = float(record['weight_grams'])
            rarity = record['rarity_classification']
            varieties_text = record['key_dates_varieties']
            
            # Parse composition for JSON storage
            if "brass" in composition_text:
                composition = {
                    "alloy_name": "Brass",
                    "copper": 0.95,
                    "zinc": 0.05
                }
            elif "copper-plated zinc" in composition_text:
                composition = {
                    "alloy_name": "Copper-plated Zinc", 
                    "zinc": 0.975,
                    "copper": 0.025
                }
            else:
                composition = {"alloy_name": "Unknown"}
            
            # Parse varieties
            varieties = []
            if varieties_text and varieties_text != "None":
                varieties.append(varieties_text)
            
            # Determine distinguishing features and keywords
            distinguishing_features = ["Lincoln Memorial reverse", "Lincoln portrait obverse"]
            identification_keywords = ["lincoln", "memorial", "cent", "penny"]
            
            if year <= 1982:
                distinguishing_features.append("95% copper composition")
                identification_keywords.extend(["copper", "brass"])
            else:
                distinguishing_features.append("Copper-plated zinc composition")
                identification_keywords.extend(["zinc", "copper-plated"])
            
            if "DDO" in coin_id:
                distinguishing_features.append("Doubled Die Obverse")
                identification_keywords.extend(["doubled", "die", "obverse"])
            elif "DDR" in coin_id:
                distinguishing_features.append("Doubled Die Reverse")
                identification_keywords.extend(["doubled", "die", "reverse"])
            
            if "Small Date" in varieties_text:
                distinguishing_features.append("Small Date variety")
                identification_keywords.extend(["small", "date"])
            elif "Large Date" in varieties_text:
                distinguishing_features.append("Large Date variety")
                identification_keywords.extend(["large", "date"])
            
            # Common names
            common_names = ["Lincoln Cent", "Lincoln Penny", "Memorial Cent"]
            if year == 1969 and "DDO" in coin_id:
                common_names.append("1969-S Double Die")
            elif year == 1972 and "DDO" in coin_id:
                common_names.append("1972 Double Die")
            
            # Notes field
            notes_parts = []
            if varieties_text and varieties_text != "None":
                notes_parts.append(varieties_text)
            
            if year == 1982:
                notes_parts.append("Transition year - both copper and zinc compositions exist")
            
            notes = " | ".join(notes_parts) if notes_parts else ""
            
            # Insert record
            cursor.execute("""
                INSERT INTO coins (
                    coin_id, series_id, country, denomination, series_name,
                    year, mint, rarity, composition, weight_grams,
                    varieties, notes, obverse_description, reverse_description,
                    distinguishing_features, identification_keywords, common_names
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin_id,
                "lincoln_memorial_cent",
                "US",
                "Cents",
                "Lincoln Memorial Cent",
                year,
                mint_mark,
                rarity,
                json.dumps(composition),
                weight_grams,
                json.dumps(varieties),
                notes,
                "Abraham Lincoln facing right, with 'LIBERTY' to left, date below, 'IN GOD WE TRUST' above",
                "Lincoln Memorial building with steps and columns, 'UNITED STATES OF AMERICA' above, 'E PLURIBUS UNUM' and 'ONE CENT' below",
                json.dumps(distinguishing_features),
                json.dumps(identification_keywords),
                json.dumps(common_names)
            ))
            
            inserted_count += 1
            if inserted_count % 25 == 0:
                print(f"📈 Processed {inserted_count} records...")
        
        # Commit changes
        conn.commit()
        print(f"\n✅ Successfully added {inserted_count} Lincoln Memorial Cent records")
        
        # Verify the data
        cursor.execute("SELECT COUNT(*) FROM coins WHERE series_id = 'lincoln_memorial_cent'")
        final_count = cursor.fetchone()[0]
        print(f"🔍 Verification: {final_count} Lincoln Memorial Cent records in database")
        
        # Show rarity breakdown
        cursor.execute("""
            SELECT rarity, COUNT(*) as count 
            FROM coins 
            WHERE series_id = 'lincoln_memorial_cent' 
            GROUP BY rarity 
            ORDER BY count DESC
        """)
        rarity_breakdown = cursor.fetchall()
        print(f"\n📊 Rarity breakdown:")
        for rarity, count in rarity_breakdown:
            print(f"   {rarity}: {count} coins")
        
        # Show key dates
        cursor.execute("""
            SELECT coin_id, year, mint, rarity 
            FROM coins 
            WHERE series_id = 'lincoln_memorial_cent' 
              AND rarity IN ('key', 'semi-key')
            ORDER BY year, mint
        """)
        key_dates = cursor.fetchall()
        print(f"\n🔑 Key dates and varieties ({len(key_dates)} total):")
        for coin_id, year, mint, rarity in key_dates:
            print(f"   {coin_id} ({rarity})")
        
        # Total coin count in database
        cursor.execute("SELECT COUNT(*) FROM coins")
        total_coins = cursor.fetchone()[0]
        print(f"\n🪙 Database now contains {total_coins} total coins")
        
        print(f"\n🎯 Lincoln Memorial Cent series (1959-2008) successfully added!")
        print(f"📋 Covers complete 50-year series with all major varieties")
        print(f"🔄 Includes composition transition from brass to copper-plated zinc")
        print(f"💎 Contains all major doubled dies and key dates")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()