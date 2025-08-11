#!/usr/bin/env python3
"""
Validate all JSON exports for coin taxonomy project.

This script is designed to run as part of the pre-commit process
to ensure all JSON files are valid before committing.
"""

import sys
from pathlib import Path
from json_validator import JSONValidator, validate_directory

def main():
    """Validate all JSON export files."""
    print("🔍 Validating JSON exports for coin taxonomy...")
    
    validator = JSONValidator()
    all_valid = True
    
    # Directories to validate
    json_directories = [
        "data/us/coins",
        "data/us",
        "data/ai-optimized",
        "data/universal"
    ]
    
    for dir_path in json_directories:
        directory = Path(dir_path)
        if directory.exists():
            print(f"\n📁 Checking {dir_path}/")
            if not validate_directory(directory):
                all_valid = False
        else:
            print(f"⚠️  Directory {dir_path} not found (skipping)")
    
    # Validate individual important files
    critical_files = [
        "data/us/us_coins_complete.json",
        "data/universal/taxonomy_summary.json"
    ]
    
    print(f"\n📄 Checking critical files...")
    for file_path in critical_files:
        filepath = Path(file_path)
        if filepath.exists():
            if validator.validate_json_file(filepath):
                print(f"   ✅ {filepath.name}")
            else:
                print(f"   ❌ {filepath.name}")
                all_valid = False
        else:
            print(f"   ⚠️  {filepath.name} not found")
    
    if all_valid:
        print(f"\n✅ All JSON files are valid!")
        return 0
    else:
        print(f"\n❌ JSON validation failed!")
        validator.print_errors()
        return 1

if __name__ == "__main__":
    sys.exit(main())