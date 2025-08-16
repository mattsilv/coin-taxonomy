#!/usr/bin/env python3
"""
Add seller_name column to coins table.

This migration adds a seller_name column to track the seller/source
of each coin entry for marketplace and inventory tracking purposes.
"""

import sqlite3
import sys
from pathlib import Path

def add_seller_name_column():
    """Add seller_name column to coins table."""
    
    # Get database path
    script_dir = Path(__file__).parent
    db_path = script_dir.parent / "database" / "coins.db"
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(coins)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'seller_name' in columns:
            print("✅ seller_name column already exists")
            return True
        
        # Add the seller_name column
        print("📝 Adding seller_name column to coins table...")
        cursor.execute("""
            ALTER TABLE coins 
            ADD COLUMN seller_name TEXT
        """)
        
        # Create index for better query performance
        print("📝 Creating index on seller_name column...")
        cursor.execute("""
            CREATE INDEX idx_coins_seller_name ON coins(seller_name)
        """)
        
        conn.commit()
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(coins)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'seller_name' in columns:
            print("✅ seller_name column added successfully")
            print("📊 Column can store seller/source information for marketplace tracking")
            return True
        else:
            print("❌ Failed to add seller_name column")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def main():
    """Main execution function."""
    print("🔧 Adding seller_name column to coins database...")
    print("=" * 50)
    
    success = add_seller_name_column()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("💡 You can now track seller information using the seller_name column")
        print("💡 Run export script to update JSON files with new schema")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()