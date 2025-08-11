#!/usr/bin/env python3
"""
JSON Validation utility for coin taxonomy project.

Provides standardized JSON validation for all export scripts.
Ensures all generated JSON files are valid and properly formatted.
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, Any, Optional, List
import sys

class JSONValidator:
    """Standardized JSON validator for all coin taxonomy exports."""
    
    def __init__(self):
        self.errors = []
    
    def validate_json_syntax(self, json_data: Any, filepath: Optional[str] = None) -> bool:
        """
        Validate that data can be serialized as valid JSON.
        
        Args:
            json_data: Data to validate
            filepath: Optional file path for error reporting
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Test JSON serialization
            json_str = json.dumps(json_data, indent=2)
            
            # Test JSON parsing
            json.loads(json_str)
            
            return True
            
        except (TypeError, ValueError, json.JSONDecodeError) as e:
            error_msg = f"JSON validation failed"
            if filepath:
                error_msg += f" for {filepath}"
            error_msg += f": {e}"
            
            self.errors.append(error_msg)
            return False
    
    def validate_json_file(self, filepath: Path) -> bool:
        """
        Validate an existing JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
            
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            self.errors.append(f"File validation failed for {filepath}: {e}")
            return False
    
    def validate_coin_taxonomy_structure(self, data: Dict[str, Any]) -> bool:
        """
        Validate coin taxonomy specific structure.
        
        Args:
            data: Dictionary to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = []
        
        # Check for common taxonomy fields
        if 'coins' in data:
            # Complete taxonomy format
            if not isinstance(data['coins'], list):
                self.errors.append("Field 'coins' must be a list")
                return False
                
            # Validate each coin entry
            for i, coin in enumerate(data['coins']):
                if not isinstance(coin, dict):
                    self.errors.append(f"Coin entry {i} must be a dictionary")
                    return False
                    
                if 'coin_id' not in coin:
                    self.errors.append(f"Coin entry {i} missing required field 'coin_id'")
                    return False
        
        elif 'series' in data:
            # Series-based taxonomy format
            if not isinstance(data['series'], list):
                self.errors.append("Field 'series' must be a list")
                return False
        
        return True
    
    def safe_json_write(self, data: Any, filepath: Path, indent: int = 2) -> bool:
        """
        Safely write JSON data to file with validation.
        
        Args:
            data: Data to write
            filepath: Output file path
            indent: JSON indentation (default: 2)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate JSON syntax first
        if not self.validate_json_syntax(data, str(filepath)):
            return False
        
        # Validate taxonomy structure if applicable
        if isinstance(data, dict):
            if not self.validate_coin_taxonomy_structure(data):
                return False
        
        try:
            # Create parent directory if needed
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Write with atomic operation (temp file + rename)
            temp_filepath = filepath.with_suffix('.tmp')
            
            with open(temp_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False, sort_keys=True)
            
            # Verify written file is valid
            if not self.validate_json_file(temp_filepath):
                temp_filepath.unlink(missing_ok=True)
                return False
            
            # Atomic rename
            temp_filepath.rename(filepath)
            
            return True
            
        except (OSError, json.JSONEncodeError) as e:
            self.errors.append(f"Failed to write {filepath}: {e}")
            return False
    
    def get_errors(self) -> List[str]:
        """Get list of validation errors."""
        return self.errors.copy()
    
    def clear_errors(self):
        """Clear error list."""
        self.errors.clear()
    
    def print_errors(self):
        """Print all validation errors."""
        if self.errors:
            print("❌ JSON Validation Errors:")
            for error in self.errors:
                print(f"   • {error}")
        else:
            print("✅ No JSON validation errors")

def validate_directory(directory: Path, pattern: str = "*.json") -> bool:
    """
    Validate all JSON files in a directory.
    
    Args:
        directory: Directory to scan
        pattern: File pattern to match (default: "*.json")
        
    Returns:
        bool: True if all files are valid
    """
    validator = JSONValidator()
    
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return False
    
    json_files = list(directory.glob(pattern))
    if not json_files:
        print(f"⚠️  No JSON files found in {directory}")
        return True
    
    print(f"🔍 Validating {len(json_files)} JSON files in {directory}")
    
    all_valid = True
    for json_file in json_files:
        if validator.validate_json_file(json_file):
            print(f"   ✅ {json_file.name}")
        else:
            print(f"   ❌ {json_file.name}")
            all_valid = False
    
    if not all_valid:
        validator.print_errors()
    
    return all_valid

def main():
    """Command line interface for JSON validation."""
    if len(sys.argv) < 2:
        print("Usage: python json_validator.py <file_or_directory>")
        return 1
    
    path = Path(sys.argv[1])
    validator = JSONValidator()
    
    if path.is_file():
        # Validate single file
        if validator.validate_json_file(path):
            print(f"✅ {path} is valid JSON")
            return 0
        else:
            validator.print_errors()
            return 1
    
    elif path.is_dir():
        # Validate directory
        if validate_directory(path):
            print(f"✅ All JSON files in {path} are valid")
            return 0
        else:
            return 1
    
    else:
        print(f"❌ Path not found: {path}")
        return 1

if __name__ == "__main__":
    sys.exit(main())