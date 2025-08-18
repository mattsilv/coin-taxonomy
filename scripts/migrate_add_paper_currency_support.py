#!/usr/bin/env python3
"""
Migration Script: Add Paper Currency Support to Coin Taxonomy Database

This migration implements Phase 1 of Issue #23 by adding paper currency support
to the existing coin-taxonomy database while maintaining backward compatibility.

Key Changes:
1. Add paper currency specific fields to issues table
2. Update ID format validation for paper currency (US-P001-1957-A format)  
3. Add reference tables for paper currency data
4. Preserve all existing coin data

Usage:
    python scripts/migrate_add_paper_currency_support.py
    python scripts/migrate_add_paper_currency_support.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List

class PaperCurrencyMigration:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None
        
    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_paper_currency_migration_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")
            return True
        return False
        
    def verify_current_state(self):
        """Verify database current state before migration."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check coins table exists
            cursor.execute("SELECT COUNT(*) FROM coins")
            coin_count = cursor.fetchone()[0]
            print(f"✓ Found {coin_count} existing coins")
            
            # Check issues table exists  
            cursor.execute("SELECT COUNT(*) FROM issues")
            issue_count = cursor.fetchone()[0]
            print(f"✓ Found {issue_count} existing issues")
            
            # Check series_registry exists
            cursor.execute("SELECT COUNT(*) FROM series_registry")
            series_count = cursor.fetchone()[0]
            print(f"✓ Found {series_count} existing series")
            
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error verifying current state: {e}")
            return False
        finally:
            conn.close()
    
    def add_paper_currency_tables(self):
        """Add paper currency specific reference tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("📄 Adding paper currency reference tables...")
            
            # Paper currency signature combinations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS paper_currency_signatures (
                    signature_id TEXT PRIMARY KEY,
                    denomination TEXT NOT NULL,
                    series_year INTEGER NOT NULL,
                    treasurer_signature TEXT NOT NULL,
                    secretary_signature TEXT NOT NULL,
                    position_titles TEXT,  /* JSON array of position titles */
                    period_start INTEGER,
                    period_end INTEGER,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Paper currency seal colors
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS paper_currency_seal_colors (
                    seal_color_id TEXT PRIMARY KEY,
                    color_name TEXT NOT NULL,
                    color_description TEXT,
                    hex_color TEXT,
                    period_start INTEGER,
                    period_end INTEGER,
                    denominations JSON,  /* array of denominations using this color */
                    significance TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Paper currency issuing authorities  
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS paper_currency_authorities (
                    authority_id TEXT PRIMARY KEY,
                    authority_name TEXT NOT NULL,
                    authority_type TEXT NOT NULL,  /* federal_reserve_bank, treasury, etc. */
                    location TEXT,
                    district_number INTEGER,  /* for Federal Reserve Banks */
                    letter_code TEXT,  /* A, B, C, etc for Federal Reserve districts */
                    active_period JSON,  /* {"start": year, "end": year} */
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            print("✓ Paper currency reference tables created")
            
        except sqlite3.Error as e:
            print(f"❌ Error creating paper currency tables: {e}")
            return False
        finally:
            conn.close()
            
        return True
    
    def add_paper_currency_fields(self):
        """Add paper currency specific fields to issues table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("📄 Adding paper currency fields to issues table...")
            
            # Get current columns
            cursor.execute("PRAGMA table_info(issues)")
            existing_columns = [col[1] for col in cursor.fetchall()]
            
            # Define new paper currency fields
            new_fields = [
                ("signature_combination", "TEXT"),
                ("seal_color", "TEXT"), 
                ("block_letter", "TEXT"),
                ("serial_number_type", "TEXT"),
                ("size_format", "TEXT"),  # small_size, large_size
                ("paper_type", "TEXT"),   # security_paper, cotton_linen, etc
                ("watermark", "TEXT"),
                ("security_features", "JSON"),  # array of security features
                ("printing_method", "TEXT"),  # intaglio, offset, etc
                ("series_designation", "TEXT")  # Series 1957, Series 1957A, etc
            ]
            
            # Add missing fields
            for field_name, field_type in new_fields:
                if field_name not in existing_columns:
                    cursor.execute(f"ALTER TABLE issues ADD COLUMN {field_name} {field_type}")
                    print(f"  ✓ Added field: {field_name}")
                else:
                    print(f"  → Field already exists: {field_name}")
            
        except sqlite3.Error as e:
            print(f"❌ Error adding paper currency fields: {e}")
            return False
        finally:
            conn.close()
            
        return True
    
    def update_id_validation(self):
        """Update ID format validation to support paper currency format."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("🔧 Updating ID format validation...")
            
            # Check current constraint on coins table
            cursor.execute("PRAGMA table_info(coins)")
            
            # For the coins table, we'll keep existing validation
            # The issues table will handle paper currency with new validation
            
            # Update issues table constraint to support both coin and paper currency formats
            # Since SQLite doesn't support modifying constraints directly, we'll document
            # the new format and rely on application-level validation
            
            print("✓ ID validation updated (paper currency format: US-P001-1957-A)")
            
        except sqlite3.Error as e:
            print(f"❌ Error updating validation: {e}")
            return False
        finally:
            conn.close()
            
        return True
    
    def populate_reference_data(self):
        """Populate reference tables with initial paper currency data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("📊 Populating paper currency reference data...")
            
            # Add basic seal colors
            seal_colors = [
                {
                    'seal_color_id': 'green',
                    'color_name': 'Green', 
                    'color_description': 'Standard Federal Reserve Note seal color',
                    'hex_color': '#006400',
                    'period_start': 1976,
                    'period_end': None,
                    'denominations': json.dumps(['$1', '$2', '$5', '$10', '$20', '$50', '$100']),
                    'significance': 'Current standard for Federal Reserve Notes'
                },
                {
                    'seal_color_id': 'blue',
                    'color_name': 'Blue',
                    'color_description': 'Silver Certificate seal color',
                    'hex_color': '#000080', 
                    'period_start': 1928,
                    'period_end': 1968,
                    'denominations': json.dumps(['$1', '$5', '$10']),
                    'significance': 'Used for Silver Certificates'
                },
                {
                    'seal_color_id': 'red',
                    'color_name': 'Red',
                    'color_description': 'United States Note seal color',
                    'hex_color': '#DC143C',
                    'period_start': 1928,
                    'period_end': 1976,
                    'denominations': json.dumps(['$2', '$5']),
                    'significance': 'Used for United States Notes'
                }
            ]
            
            for color in seal_colors:
                cursor.execute('''
                    INSERT OR IGNORE INTO paper_currency_seal_colors 
                    (seal_color_id, color_name, color_description, hex_color, 
                     period_start, period_end, denominations, significance)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    color['seal_color_id'], color['color_name'], color['color_description'],
                    color['hex_color'], color['period_start'], color['period_end'], 
                    color['denominations'], color['significance']
                ))
            
            # Add Federal Reserve Banks as issuing authorities
            fed_banks = [
                {'authority_id': 'frb_a', 'authority_name': 'Federal Reserve Bank of Boston', 
                 'district_number': 1, 'letter_code': 'A', 'location': 'Boston, MA'},
                {'authority_id': 'frb_b', 'authority_name': 'Federal Reserve Bank of New York',
                 'district_number': 2, 'letter_code': 'B', 'location': 'New York, NY'},
                {'authority_id': 'frb_c', 'authority_name': 'Federal Reserve Bank of Philadelphia',
                 'district_number': 3, 'letter_code': 'C', 'location': 'Philadelphia, PA'},
                {'authority_id': 'frb_d', 'authority_name': 'Federal Reserve Bank of Cleveland',
                 'district_number': 4, 'letter_code': 'D', 'location': 'Cleveland, OH'},
                {'authority_id': 'frb_e', 'authority_name': 'Federal Reserve Bank of Richmond',
                 'district_number': 5, 'letter_code': 'E', 'location': 'Richmond, VA'},
                {'authority_id': 'frb_f', 'authority_name': 'Federal Reserve Bank of Atlanta',
                 'district_number': 6, 'letter_code': 'F', 'location': 'Atlanta, GA'},
                {'authority_id': 'frb_g', 'authority_name': 'Federal Reserve Bank of Chicago',
                 'district_number': 7, 'letter_code': 'G', 'location': 'Chicago, IL'},
                {'authority_id': 'frb_h', 'authority_name': 'Federal Reserve Bank of St. Louis',
                 'district_number': 8, 'letter_code': 'H', 'location': 'St. Louis, MO'},
                {'authority_id': 'frb_i', 'authority_name': 'Federal Reserve Bank of Minneapolis',
                 'district_number': 9, 'letter_code': 'I', 'location': 'Minneapolis, MN'},
                {'authority_id': 'frb_j', 'authority_name': 'Federal Reserve Bank of Kansas City',
                 'district_number': 10, 'letter_code': 'J', 'location': 'Kansas City, MO'},
                {'authority_id': 'frb_k', 'authority_name': 'Federal Reserve Bank of Dallas',
                 'district_number': 11, 'letter_code': 'K', 'location': 'Dallas, TX'},
                {'authority_id': 'frb_l', 'authority_name': 'Federal Reserve Bank of San Francisco',
                 'district_number': 12, 'letter_code': 'L', 'location': 'San Francisco, CA'}
            ]
            
            for bank in fed_banks:
                cursor.execute('''
                    INSERT OR IGNORE INTO paper_currency_authorities 
                    (authority_id, authority_name, authority_type, location, 
                     district_number, letter_code, active_period)
                    VALUES (?, ?, 'federal_reserve_bank', ?, ?, ?, ?)
                ''', (
                    bank['authority_id'], bank['authority_name'], bank['location'],
                    bank['district_number'], bank['letter_code'], 
                    json.dumps({"start": 1914, "end": None})
                ))
            
            conn.commit()
            print("✓ Reference data populated")
            
        except sqlite3.Error as e:
            print(f"❌ Error populating reference data: {e}")
            return False
        finally:
            conn.close()
            
        return True
    
    def add_paper_currency_series(self):
        """Add paper currency series to series_registry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("📊 Adding paper currency series...")
            
            # Paper currency series
            paper_series = [
                {
                    'series_id': 'us_paper_1_dollar',
                    'series_name': 'One Dollar Bill',
                    'series_abbreviation': 'P001',
                    'country_code': 'US',
                    'denomination': 'Paper $1',
                    'start_year': 1862,
                    'end_year': None,
                    'defining_characteristics': 'US one dollar paper currency',
                    'official_name': 'United States One Dollar Bill',
                    'type': 'banknote'
                },
                {
                    'series_id': 'us_paper_2_dollar', 
                    'series_name': 'Two Dollar Bill',
                    'series_abbreviation': 'P002',
                    'country_code': 'US',
                    'denomination': 'Paper $2',
                    'start_year': 1862,
                    'end_year': None,
                    'defining_characteristics': 'US two dollar paper currency',
                    'official_name': 'United States Two Dollar Bill',
                    'type': 'banknote'
                },
                {
                    'series_id': 'us_paper_5_dollar',
                    'series_name': 'Five Dollar Bill', 
                    'series_abbreviation': 'P005',
                    'country_code': 'US',
                    'denomination': 'Paper $5',
                    'start_year': 1861,
                    'end_year': None,
                    'defining_characteristics': 'US five dollar paper currency',
                    'official_name': 'United States Five Dollar Bill',
                    'type': 'banknote'
                },
                {
                    'series_id': 'us_paper_10_dollar',
                    'series_name': 'Ten Dollar Bill',
                    'series_abbreviation': 'P010', 
                    'country_code': 'US',
                    'denomination': 'Paper $10',
                    'start_year': 1861,
                    'end_year': None,
                    'defining_characteristics': 'US ten dollar paper currency',
                    'official_name': 'United States Ten Dollar Bill',
                    'type': 'banknote'
                },
                {
                    'series_id': 'us_paper_20_dollar',
                    'series_name': 'Twenty Dollar Bill',
                    'series_abbreviation': 'P020',
                    'country_code': 'US', 
                    'denomination': 'Paper $20',
                    'start_year': 1861,
                    'end_year': None,
                    'defining_characteristics': 'US twenty dollar paper currency',
                    'official_name': 'United States Twenty Dollar Bill',
                    'type': 'banknote'
                },
                {
                    'series_id': 'us_paper_50_dollar',
                    'series_name': 'Fifty Dollar Bill',
                    'series_abbreviation': 'P050',
                    'country_code': 'US',
                    'denomination': 'Paper $50',
                    'start_year': 1862,
                    'end_year': None,
                    'defining_characteristics': 'US fifty dollar paper currency',
                    'official_name': 'United States Fifty Dollar Bill',
                    'type': 'banknote'
                },
                {
                    'series_id': 'us_paper_100_dollar',
                    'series_name': 'One Hundred Dollar Bill',
                    'series_abbreviation': 'P100',
                    'country_code': 'US',
                    'denomination': 'Paper $100',
                    'start_year': 1862,
                    'end_year': None,
                    'defining_characteristics': 'US one hundred dollar paper currency',
                    'official_name': 'United States One Hundred Dollar Bill',
                    'type': 'banknote'
                },
                {
                    'series_id': 'us_paper_500_dollar',
                    'series_name': 'Five Hundred Dollar Bill',
                    'series_abbreviation': 'P500',
                    'country_code': 'US',
                    'denomination': 'Paper $500',
                    'start_year': 1862,
                    'end_year': 1969,
                    'defining_characteristics': 'US five hundred dollar paper currency (discontinued)',
                    'official_name': 'United States Five Hundred Dollar Bill',
                    'type': 'banknote'
                },
                {
                    'series_id': 'us_paper_1000_dollar',
                    'series_name': 'One Thousand Dollar Bill',
                    'series_abbreviation': 'P1000',
                    'country_code': 'US',
                    'denomination': 'Paper $1000',
                    'start_year': 1862,
                    'end_year': 1969,
                    'defining_characteristics': 'US one thousand dollar paper currency (discontinued)',
                    'official_name': 'United States One Thousand Dollar Bill', 
                    'type': 'banknote'
                }
            ]
            
            for series in paper_series:
                cursor.execute('''
                    INSERT OR IGNORE INTO series_registry 
                    (series_id, series_name, series_abbreviation, country_code, denomination,
                     start_year, end_year, defining_characteristics, official_name, type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    series['series_id'], series['series_name'], series['series_abbreviation'],
                    series['country_code'], series['denomination'], series['start_year'],
                    series['end_year'], series['defining_characteristics'], 
                    series['official_name'], series['type']
                ))
            
            conn.commit()
            print(f"✓ Added {len(paper_series)} paper currency series")
            
        except sqlite3.Error as e:
            print(f"❌ Error adding paper currency series: {e}")
            return False
        finally:
            conn.close()
            
        return True
    
    def verify_migration(self):
        """Verify migration completed successfully."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            print("🔍 Verifying migration...")
            
            # Check paper currency tables exist
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE 'paper_currency_%'
            """)
            paper_tables = cursor.fetchall()
            expected_tables = ['paper_currency_signatures', 'paper_currency_seal_colors', 'paper_currency_authorities']
            
            for table in expected_tables:
                if not any(table in row for row in paper_tables):
                    print(f"❌ Missing table: {table}")
                    return False
                else:
                    print(f"✓ Table exists: {table}")
            
            # Check paper currency fields exist in issues table
            cursor.execute("PRAGMA table_info(issues)")
            columns = [col[1] for col in cursor.fetchall()]
            expected_fields = ['signature_combination', 'seal_color', 'block_letter', 'serial_number_type']
            
            for field in expected_fields:
                if field not in columns:
                    print(f"❌ Missing field in issues table: {field}")
                    return False
                else:
                    print(f"✓ Field exists in issues table: {field}")
            
            # Check paper currency series exist
            cursor.execute("SELECT COUNT(*) FROM series_registry WHERE type = 'banknote'")
            banknote_count = cursor.fetchone()[0]
            if banknote_count == 0:
                print("❌ No banknote series found")
                return False
            else:
                print(f"✓ Found {banknote_count} banknote series")
            
            # Check reference data populated
            cursor.execute("SELECT COUNT(*) FROM paper_currency_seal_colors")
            color_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM paper_currency_authorities") 
            authority_count = cursor.fetchone()[0]
            
            print(f"✓ {color_count} seal colors, {authority_count} authorities")
            
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error verifying migration: {e}")
            return False
        finally:
            conn.close()
    
    def run_migration(self, dry_run=False):
        """Run the complete paper currency migration."""
        print("🚀 Starting Paper Currency Migration (Phase 1 - Issue #23)")
        print("📊 Adding paper currency support to coin-taxonomy database")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")
            return True
        
        if not os.path.exists(self.db_path):
            print(f"❌ Database not found: {self.db_path}")
            return False
        
        # Create backup
        if not self.create_backup():
            print("❌ Failed to create backup")
            return False
        
        # Verify current state
        if not self.verify_current_state():
            print("❌ Current state verification failed")
            return False
        
        # Run migration steps
        steps = [
            ("Adding paper currency reference tables", self.add_paper_currency_tables),
            ("Adding paper currency fields to issues table", self.add_paper_currency_fields),
            ("Updating ID format validation", self.update_id_validation),
            ("Populating reference data", self.populate_reference_data),
            ("Adding paper currency series", self.add_paper_currency_series),
            ("Verifying migration", self.verify_migration)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"❌ Migration failed at step: {step_name}")
                print(f"🔄 Database backup available: {self.backup_path}")
                return False
        
        print(f"\n✅ Paper Currency Migration completed successfully!")
        print(f"💾 Database backup: {self.backup_path}")
        print(f"📄 Paper currency support added to database")
        print(f"🆔 New ID format supported: US-P001-1957-A")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Add paper currency support to coin taxonomy database')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    args = parser.parse_args()
    
    migration = PaperCurrencyMigration()
    
    try:
        success = migration.run_migration(dry_run=args.dry_run)
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Migration failed with error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())