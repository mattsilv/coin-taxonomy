#!/usr/bin/env python3
"""
Visual Descriptions Migration Script
Adds visual description data to the coin taxonomy database.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

class VisualDescriptionsMigrator:
    def __init__(self, db_path="database/coins.db", descriptions_file="docs/temp-us_coin_visual_descriptions.json"):
        self.db_path = Path(db_path)
        self.descriptions_file = Path(descriptions_file)
        self.processed_count = 0
        self.errors = []
        
    def migrate_descriptions(self):
        """Main migration process."""
        print("🖼️  Starting visual descriptions migration...")
        
        # Load descriptions data
        descriptions_data = self._load_descriptions()
        if not descriptions_data:
            return False
            
        # Update database schema
        if not self._update_schema():
            return False
            
        # Process each coin description
        if not self._process_descriptions(descriptions_data):
            return False
            
        print(f"✅ Successfully migrated {self.processed_count} visual descriptions")
        return True
        
    def _load_descriptions(self):
        """Load visual descriptions from JSON file."""
        try:
            with open(self.descriptions_file, 'r') as f:
                data = json.load(f)
            
            coin_descriptions = data.get('coin_descriptions', [])
            print(f"📁 Loaded {len(coin_descriptions)} coin descriptions")
            return coin_descriptions
            
        except FileNotFoundError:
            self.errors.append(f"Descriptions file not found: {self.descriptions_file}")
            return None
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in descriptions file: {e}")
            return None
            
    def _update_schema(self):
        """Add visual description columns to database tables."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if columns already exist
            cursor.execute("PRAGMA table_info(coins)")
            existing_columns = [col[1] for col in cursor.fetchall()]
            
            # Add new columns if they don't exist
            new_columns = [
                ("obverse_description", "TEXT"),
                ("reverse_description", "TEXT"), 
                ("distinguishing_features", "TEXT"),  # JSON array
                ("identification_keywords", "TEXT"),  # JSON array
                ("common_names", "TEXT")  # JSON array
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in existing_columns:
                    cursor.execute(f"ALTER TABLE coins ADD COLUMN {col_name} {col_type}")
                    print(f"   • Added column: {col_name}")
            
            # Also update issues table for universal format
            cursor.execute("PRAGMA table_info(issues)")
            existing_issues_columns = [col[1] for col in cursor.fetchall()]
            
            for col_name, col_type in new_columns:
                if col_name not in existing_issues_columns:
                    cursor.execute(f"ALTER TABLE issues ADD COLUMN {col_name} {col_type}")
            
            conn.commit()
            conn.close()
            print("✅ Database schema updated successfully")
            return True
            
        except Exception as e:
            self.errors.append(f"Schema update failed: {e}")
            return False
            
    def _process_descriptions(self, descriptions):
        """Process and insert visual descriptions."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for desc in descriptions:
                coin_id = desc.get('coin_id')
                if not coin_id:
                    continue
                    
                # Extract description components
                design = desc.get('design_description', {})
                obverse = design.get('obverse', '')
                reverse = design.get('reverse', '')
                features = json.dumps(design.get('distinguishing_features', []))
                keywords = json.dumps(desc.get('identification_keywords', []))
                names = json.dumps(desc.get('common_names', []))
                
                # Update coins table
                cursor.execute("""
                    UPDATE coins 
                    SET obverse_description = ?,
                        reverse_description = ?,
                        distinguishing_features = ?,
                        identification_keywords = ?,
                        common_names = ?
                    WHERE coin_id = ?
                """, (obverse, reverse, features, keywords, names, coin_id))
                
                # Update issues table (for universal format)
                cursor.execute("""
                    UPDATE issues 
                    SET obverse_description = ?,
                        reverse_description = ?,
                        distinguishing_features = ?,
                        identification_keywords = ?,
                        common_names = ?
                    WHERE issue_id = ?
                """, (obverse, reverse, features, keywords, names, coin_id))
                
                if cursor.rowcount > 0:
                    self.processed_count += 1
                else:
                    print(f"⚠️  Coin not found in database: {coin_id}")
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            self.errors.append(f"Description processing failed: {e}")
            return False

def main():
    """Main migration function."""
    migrator = VisualDescriptionsMigrator()
    
    success = migrator.migrate_descriptions()
    
    if migrator.errors:
        print(f"\n❌ Migration completed with {len(migrator.errors)} errors:")
        for error in migrator.errors:
            print(f"   • {error}")
    
    if success:
        print("\n🎯 Visual descriptions migration completed successfully!")
        print("   Next steps:")
        print("   1. Update AI-optimized export to include visual data")
        print("   2. Run full export pipeline to regenerate files")
        return 0
    else:
        print("\n❌ Visual descriptions migration failed!")
        return 1

if __name__ == "__main__":
    exit(main())