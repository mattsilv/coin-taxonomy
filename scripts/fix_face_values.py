#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('database/coins.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement

# Check current data
cursor.execute('SELECT COUNT(*), unit_name FROM issues GROUP BY unit_name')
print('Unit names in database:')
for row in cursor.fetchall():
    print(f'  {row[1]}: {row[0]} records')

# Update face values based on unit names
updates = [
    ("cent", 0.01),
    ("Cents", 0.01), 
    ("penny", 0.01),
    ("nickel", 0.05),
    ("Nickels", 0.05),
    ("dime", 0.10),
    ("Dimes", 0.10),
    ("quarter", 0.25),
    ("Quarters", 0.25),
    ("half_dollar", 0.50),
    ("Half Dollars", 0.50),
    ("dollar", 1.00),
    ("Dollars", 1.00)
]

for unit_name, face_value in updates:
    cursor.execute("UPDATE issues SET face_value = ? WHERE unit_name = ?", (face_value, unit_name))
    if cursor.rowcount > 0:
        print(f"Updated {cursor.rowcount} records for {unit_name} to ${face_value}")

conn.commit()

# Verify results
cursor.execute('SELECT unit_name, face_value, COUNT(*) FROM issues GROUP BY unit_name, face_value ORDER BY face_value')
print('\nFinal face values:')
for row in cursor.fetchall():
    print(f'  {row[0]}: ${row[1]} ({row[2]} records)')

conn.close()