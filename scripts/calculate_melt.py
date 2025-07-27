#!/usr/bin/env python3
"""
Calculate melt values based on current metal prices.
Works for any country's coins with metal content.
"""

import json
import sqlite3
from datetime import datetime

class MeltCalculator:
    def __init__(self, db_path='database/coins.db'):
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key enforcement
        # Default spot prices per troy ounce
        self.spot_prices = {
            'gold': 2000.00,
            'silver': 25.00,
            'platinum': 900.00,
            'palladium': 1000.00,
            'copper': 0.0027,  # per gram
            'nickel': 0.0080,  # per gram
            'zinc': 0.0012,    # per gram
            'steel': 0.0001    # per gram
        }
        self.grams_per_troy_oz = 31.1035
    
    def update_spot_prices(self, prices):
        """Update metal spot prices"""
        self.spot_prices.update(prices)
    
    def calculate_melt_value(self, country, year, mint, series):
        """Calculate melt value for a specific coin"""
        coin = self.conn.execute('''
            SELECT composition, weight_grams
            FROM coins
            WHERE country = ? AND year = ? AND mint = ? AND series = ?
        ''', (country, year, mint, series)).fetchone()
        
        if not coin or not coin[0]:
            return None
        
        composition = json.loads(coin[0])
        weight_grams = coin[1]
        
        total_value = 0
        metal_breakdown = {}
        
        for component, percentage in composition.items():
            # Handle clad compositions
            if component in ['copper_core', 'cupronickel_cladding']:
                # Simplified - treat as copper for now
                metal = 'copper'
                percentage = float(percentage)
            else:
                metal = component
                percentage = float(percentage)
            
            metal_weight_grams = weight_grams * percentage
            
            # Calculate value based on metal type
            if metal in ['gold', 'silver', 'platinum', 'palladium']:
                # Precious metals - price per troy oz
                metal_weight_troy_oz = metal_weight_grams / self.grams_per_troy_oz
                metal_value = metal_weight_troy_oz * self.spot_prices.get(metal, 0)
            else:
                # Base metals - price per gram
                metal_value = metal_weight_grams * self.spot_prices.get(metal, 0)
            
            total_value += metal_value
            
            metal_breakdown[metal] = {
                'percentage': percentage,
                'weight_grams': metal_weight_grams,
                'value': metal_value
            }
        
        return {
            'total_melt_value': round(total_value, 3),
            'metal_breakdown': metal_breakdown,
            'spot_prices_used': self.spot_prices,
            'calculation_date': datetime.now().isoformat()
        }

def main():
    calc = MeltCalculator()
    
    # Example calculations
    examples = [
        ('US', 1964, 'D', 'Roosevelt Dime'),
        ('US', 1946, 'P', 'Roosevelt Dime'),
        ('US', 1916, 'D', 'Mercury Dime')
    ]
    
    for country, year, mint, series in examples:
        result = calc.calculate_melt_value(country, year, mint, series)
        if result:
            print(f"\n{country} {year}-{mint} {series}")
            print(f"Melt value: ${result['total_melt_value']:.3f}")
            for metal, data in result['metal_breakdown'].items():
                print(f"  {metal}: {data['weight_grams']:.3f}g = ${data['value']:.3f}")

if __name__ == "__main__":
    main()