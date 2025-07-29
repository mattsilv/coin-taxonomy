#!/usr/bin/env python3
"""
Comprehensive rebuild and export script for coin taxonomy database.

This script:
1. Removes existing database
2. Rebuilds database from migration scripts (source of truth)
3. Runs data integrity checks
4. Exports JSON files
5. Copies universal data to docs folder

This ensures that all data is rebuilt from the migration scripts,
maintaining the database as a build artifact paradigm.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def main():
    """Main rebuild and export process."""
    print("🏗️  Coin Taxonomy Database Rebuild & Export")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Step 1: Remove existing database
    db_path = Path("database/coins.db")
    if db_path.exists():
        print(f"🗑️  Removing existing database: {db_path}")
        db_path.unlink()
    
    # Step 2: Initialize database from JSON data
    if not run_command("uv run python scripts/init_database_from_json.py", 
                      "Initializing database from JSON data"):
        sys.exit(1)
    
    # Step 3: Run universal migration to add universal tables
    if not run_command("uv run python scripts/migrate_to_universal_v1_1.py", 
                      "Running universal migration"):
        sys.exit(1)
    
    # Step 4: Run data integrity checks
    if not run_command("uv run python scripts/data_integrity_check.py", 
                      "Running data integrity checks"):
        sys.exit(1)
    
    # Step 5: Export JSON files
    if not run_command("uv run python scripts/export_db_v1_1.py", 
                      "Exporting JSON files from database"):
        sys.exit(1)
    
    # Step 6: Validate JSON exports
    if not run_command("uv run python scripts/validate.py", 
                      "Validating JSON exports"):
        sys.exit(1)
    
    # Step 7: Copy universal data to docs folder for GitHub Pages
    docs_universal = Path("docs/data/universal")
    docs_universal.mkdir(parents=True, exist_ok=True)
    
    if not run_command("cp -r data/universal/* docs/data/universal/", 
                      "Copying universal data to docs folder"):
        sys.exit(1)
    
    print("\n🎉 Rebuild and export completed successfully!")
    print("📊 Database rebuilt from migration scripts")
    print("📁 JSON files exported and validated")
    print("🌐 Universal data copied to docs folder")

if __name__ == "__main__":
    main()