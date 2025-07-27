#!/usr/bin/env python3
import sqlite3
import json

def check_database_structure():
    conn = sqlite3.connect('database/coins.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement

    # Get the actual schema of the issues table
    cursor.execute('PRAGMA table_info(issues)')
    columns = cursor.fetchall()

    print('Issues table schema:')
    for col in columns:
        nullable = "nullable" if not col[3] else "NOT NULL"
        default = col[4] or "none"
        print(f'  {col[1]} ({col[2]}) - {nullable} - default: {default}')

    print()

    # Get a sample record to see actual data
    cursor.execute('SELECT * FROM issues LIMIT 1')
    sample = cursor.fetchone()

    print('Sample record structure:')
    json_fields = ['specifications', 'sides', 'mintage', 'varieties', 'common_names', 'authority_period', 'metadata']
    
    for i, col in enumerate(columns):
        value = sample[i] if sample else 'N/A'
        if col[1] in json_fields:
            print(f'  {col[1]}: JSON field')
            if value and value != 'N/A':
                try:
                    parsed = json.loads(value)
                    print(f'    Content type: {type(parsed).__name__}')
                    if isinstance(parsed, dict):
                        print(f'    Keys: {list(parsed.keys())}')
                    elif isinstance(parsed, list):
                        print(f'    Length: {len(parsed)}')
                except Exception as e:
                    print(f'    Raw value: {str(value)[:100]}...')
        else:
            print(f'  {col[1]}: {value}')

    conn.close()

if __name__ == "__main__":
    check_database_structure()