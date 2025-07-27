#!/usr/bin/env python3
"""
DEPRECATED: Use export_us_complete.py instead.

This script is kept for compatibility but redirects to the new script.
"""

import subprocess
import sys
import os

def main():
    """Redirect to the new export script"""
    print("⚠️  This script is deprecated. Redirecting to export_us_complete.py...")
    print("🔄 Running: python scripts/export_us_complete.py")
    print()
    
    # Run the new script
    result = subprocess.run([sys.executable, 'scripts/export_us_complete.py'])
    
    if result.returncode == 0:
        print()
        print("✅ Complete! For future use, run:")
        print("   uv run python scripts/export_us_complete.py")
    else:
        print("❌ Export failed. Please run export_us_complete.py directly.")
        sys.exit(1)

if __name__ == "__main__":
    main()