#!/usr/bin/env python3
"""Fix varieties format to match schema requirements."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

class VarietiesFormatFixer:
    def __init__(self):
        self.db_path = Path("database/coins.db")
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self):
        """Create database backup before modifications."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"coins_varieties_fix_{timestamp}.db"
        
        import shutil
        shutil.copy(self.db_path, backup_path)
        print(f"Created backup: {backup_path}")
        return backup_path
    
    def format_variety(self, variety_value):
        """Convert a variety value to proper object format."""
        if isinstance(variety_value, str):
            # Generate variety ID from name
            variety_id = variety_value.lower().replace(' ', '_').replace('-', '_').replace('/', '_')
            return {
                "variety_id": variety_id,
                "name": variety_value,
                "description": None,
                "estimated_mintage": None
            }
        elif isinstance(variety_value, dict):
            # Already in correct format
            return variety_value
        else:
            return None
    
    def fix_varieties(self):
        """Fix varieties format in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all coins with varieties
        cursor.execute("SELECT coin_id, varieties FROM coins WHERE varieties IS NOT NULL AND varieties != '[]'")
        rows = cursor.fetchall()
        
        fixes_needed = 0
        fixes_applied = 0
        
        for coin_id, varieties_json in rows:
            try:
                varieties = json.loads(varieties_json)
                
                # Check if fix is needed
                needs_fix = False
                if isinstance(varieties, list):
                    for v in varieties:
                        if isinstance(v, str):
                            needs_fix = True
                            break
                
                if needs_fix:
                    fixes_needed += 1
                    # Convert string varieties to objects
                    fixed_varieties = []
                    for v in varieties:
                        formatted = self.format_variety(v)
                        if formatted:
                            fixed_varieties.append(formatted)
                    
                    # Update database
                    cursor.execute(
                        "UPDATE coins SET varieties = ? WHERE coin_id = ?",
                        (json.dumps(fixed_varieties), coin_id)
                    )
                    fixes_applied += 1
                    print(f"Fixed varieties for {coin_id}: {varieties} -> {fixed_varieties}")
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing varieties for {coin_id}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        print(f"\nSummary:")
        print(f"  Total coins checked: {len(rows)}")
        print(f"  Fixes needed: {fixes_needed}")
        print(f"  Fixes applied: {fixes_applied}")
        
        return fixes_applied > 0

def main():
    print("Fixing varieties format in database...")
    fixer = VarietiesFormatFixer()
    
    # Create backup
    backup_path = fixer.create_backup()
    
    # Fix varieties
    if fixer.fix_varieties():
        print("\nVarieties format fixed successfully!")
        print("Now re-run the export script to generate JSON files.")
    else:
        print("\nNo varieties format fixes needed.")

if __name__ == "__main__":
    main()