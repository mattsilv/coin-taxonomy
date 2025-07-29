#!/usr/bin/env python3
"""
4-Letter TYPE Code Mapping for Coin ID Standardization
Based on GitHub Issue #7 proposal
"""

# Current to 4-letter mapping
TYPE_MAPPING = {
    # Cents
    'IHC': 'INCH',  # Indian Head Cent
    'LWC': 'LWCT',  # Lincoln Wheat Cent
    'LMC': 'LMCT',  # Lincoln Memorial Cent
    'LBC': 'LBCT',  # Lincoln Bicentennial Cent
    'LSC': 'LSCT',  # Lincoln Shield Cent
    
    # Nickels
    'SN': 'SHLD',   # Shield Nickel
    'LHN': 'LHNI',  # Liberty Head Nickel
    'BN': 'BUFF',   # Buffalo Nickel
    'JN': 'JEFF',   # Jefferson Nickel
    
    # Dimes
    'BD': 'BARD',   # Barber Dime
    'WHD': 'MERC',  # Mercury Dime (Winged Liberty Head)
    'RD': 'ROOS',   # Roosevelt Dime
    
    # Quarters
    'BQ': 'BARQ',   # Barber Quarter
    'SLQ': 'SLIQ',  # Standing Liberty Quarter
    'WQ': 'WASH',   # Washington Quarter
    
    # Dollars
    'MD': 'MORG',   # Morgan Dollar
    'PD': 'PEAC',   # Peace Dollar
    'ED': 'EISE',   # Eisenhower Dollar
    'SBA': 'SANT',  # Susan B. Anthony Dollar
    'SAC': 'SACA',  # Sacagawea Dollar
}

def validate_uniqueness():
    """Validate that all 4-letter codes are unique"""
    codes = list(TYPE_MAPPING.values())
    unique_codes = set(codes)
    
    print(f"Total mappings: {len(TYPE_MAPPING)}")
    print(f"Unique 4-letter codes: {len(unique_codes)}")
    
    if len(codes) != len(unique_codes):
        print("❌ DUPLICATE CODES FOUND!")
        for code in unique_codes:
            count = codes.count(code)
            if count > 1:
                print(f"  {code}: {count} occurrences")
        return False
    else:
        print("✅ All 4-letter codes are unique!")
        
    # Print mapping table
    print("\n=== 4-LETTER TYPE CODE MAPPING ===")
    for old_code, new_code in sorted(TYPE_MAPPING.items()):
        print(f"{old_code:4} → {new_code}")
        
    return True

if __name__ == "__main__":
    validate_uniqueness()