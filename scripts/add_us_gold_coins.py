#!/usr/bin/env python3
"""
Add comprehensive US gold coin series to the database.

This script adds all major US gold coin denominations from 1849-1933:
1. Gold Dollar ($1) - 1849-1889
2. Quarter Eagle ($2.50) - 1796-1929
3. Three Dollar Gold ($3) - 1854-1889
4. Half Eagle ($5) - 1795-1929
5. Eagle ($10) - 1795-1933
6. Double Eagle ($20) - 1849-1933

Usage:
    python scripts/add_us_gold_coins.py
    python scripts/add_us_gold_coins.py --dry-run
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List

class USGoldCoinsBackfill:
    def __init__(self, db_path='database/coins.db'):
        self.db_path = db_path
        self.backup_path = None
        
    def create_backup(self):
        """Create database backup before migration."""
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = f"{backup_dir}/coins_us_gold_backup_{timestamp}.db"
        
        if os.path.exists(self.db_path):
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✓ Backup created: {self.backup_path}")
    
    def get_gold_dollars(self) -> List[Dict]:
        """Return Gold Dollar ($1) coin data."""
        coins = []
        
        # Type I - Liberty Head (1849-1854)
        for year in range(1849, 1855):
            for mint in ['P', 'C', 'D', 'O']:
                if year == 1849 and mint in ['C', 'D', 'O']:
                    continue  # C,D,O started in 1849 but not all
                if year == 1849 and mint == 'P':
                    coins.append(self._create_gold_coin("GDLA", "Gold Dollar Type I", year, mint, "Gold Dollars", 
                                                        composition={"gold": 90, "copper": 10},
                                                        weight_grams=1.672,
                                                        diameter_mm=13.0))
                elif year >= 1849:
                    if mint == 'C' and year <= 1855:
                        coins.append(self._create_gold_coin("GDLA", "Gold Dollar Type I", year, mint, "Gold Dollars",
                                                            composition={"gold": 90, "copper": 10},
                                                            weight_grams=1.672,
                                                            diameter_mm=13.0))
                    elif mint == 'D' and year in [1849, 1850, 1851, 1852, 1853, 1854]:
                        coins.append(self._create_gold_coin("GDLA", "Gold Dollar Type I", year, mint, "Gold Dollars",
                                                            composition={"gold": 90, "copper": 10},
                                                            weight_grams=1.672,
                                                            diameter_mm=13.0))
                    elif mint == 'O' and year in [1849, 1850, 1851, 1852, 1853, 1854]:
                        coins.append(self._create_gold_coin("GDLA", "Gold Dollar Type I", year, mint, "Gold Dollars",
                                                            composition={"gold": 90, "copper": 10},
                                                            weight_grams=1.672,
                                                            diameter_mm=13.0))
                    elif mint == 'P':
                        coins.append(self._create_gold_coin("GDLA", "Gold Dollar Type I", year, mint, "Gold Dollars",
                                                            composition={"gold": 90, "copper": 10},
                                                            weight_grams=1.672,
                                                            diameter_mm=13.0))
        
        # Type II - Indian Princess Head Small (1854-1856)
        for year in range(1854, 1857):
            for mint in ['P', 'C', 'D', 'O']:
                if year == 1854 and mint in ['C', 'D']:
                    continue
                if year == 1855 and mint == 'D':
                    continue
                if year == 1856 and mint in ['C', 'D', 'O']:
                    continue
                coins.append(self._create_gold_coin("GDLB", "Gold Dollar Type II", year, mint, "Gold Dollars",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=1.672,
                                                    diameter_mm=15.0))
        
        # Type III - Indian Princess Head Large (1856-1889)
        for year in range(1856, 1890):
            mints = self._get_gold_dollar_mints_by_year(year)
            for mint in mints:
                coins.append(self._create_gold_coin("GDLC", "Gold Dollar Type III", year, mint, "Gold Dollars",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=1.672,
                                                    diameter_mm=15.0))
        
        return coins
    
    def get_quarter_eagles(self) -> List[Dict]:
        """Return Quarter Eagle ($2.50) coin data."""
        coins = []
        
        # Capped Bust Right (1796-1807)
        for year in [1796, 1797, 1798, 1802, 1804, 1805, 1806, 1807]:
            coins.append(self._create_gold_coin("QECB", "Quarter Eagle Capped Bust", year, "P", "Quarter Eagles",
                                                composition={"gold": 91.67, "copper": 8.33},
                                                weight_grams=4.37,
                                                diameter_mm=20.0))
        
        # Capped Bust Left (1808)
        coins.append(self._create_gold_coin("QECL", "Quarter Eagle Capped Bust Left", 1808, "P", "Quarter Eagles",
                                            composition={"gold": 91.67, "copper": 8.33},
                                            weight_grams=4.37,
                                            diameter_mm=20.0))
        
        # Capped Head Left (1821-1834)
        for year in [1821, 1824, 1825, 1826, 1827, 1829, 1830, 1831, 1832, 1833, 1834]:
            coins.append(self._create_gold_coin("QECH", "Quarter Eagle Capped Head", year, "P", "Quarter Eagles",
                                                composition={"gold": 91.67, "copper": 8.33},
                                                weight_grams=4.37,
                                                diameter_mm=18.5))
        
        # Classic Head (1834-1839)
        for year in range(1834, 1840):
            for mint in self._get_quarter_eagle_classic_mints(year):
                coins.append(self._create_gold_coin("QECL", "Quarter Eagle Classic Head", year, mint, "Quarter Eagles",
                                                    composition={"gold": 89.92, "copper": 10.08},
                                                    weight_grams=4.18,
                                                    diameter_mm=18.2))
        
        # Liberty Head (1840-1907)
        for year in range(1840, 1908):
            mints = self._get_quarter_eagle_liberty_mints(year)
            for mint in mints:
                coins.append(self._create_gold_coin("QELH", "Quarter Eagle Liberty Head", year, mint, "Quarter Eagles",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=4.18,
                                                    diameter_mm=18.0))
        
        # Indian Head (1908-1929)
        for year in range(1908, 1930):
            if year in [1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924]:
                continue
            mints = ['P'] if year <= 1915 else ['P', 'D']
            for mint in mints:
                if year == 1911 and mint == 'D':
                    coins.append(self._create_gold_coin("QEIH", "Quarter Eagle Indian Head", year, mint, "Quarter Eagles",
                                                        composition={"gold": 90, "copper": 10},
                                                        weight_grams=4.18,
                                                        diameter_mm=18.0,
                                                        rarity="key"))
                else:
                    coins.append(self._create_gold_coin("QEIH", "Quarter Eagle Indian Head", year, mint, "Quarter Eagles",
                                                        composition={"gold": 90, "copper": 10},
                                                        weight_grams=4.18,
                                                        diameter_mm=18.0))
        
        return coins
    
    def get_three_dollar_gold(self) -> List[Dict]:
        """Return Three Dollar Gold coin data."""
        coins = []
        
        # Three Dollar Gold (1854-1889)
        for year in range(1854, 1890):
            mints = self._get_three_dollar_mints(year)
            for mint in mints:
                rarity = "common"
                if year in [1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874]:
                    if mint == 'D' or mint == 'O':
                        rarity = "scarce"
                if year >= 1875:
                    rarity = "key"
                
                coins.append(self._create_gold_coin("TDOG", "Three Dollar Gold", year, mint, "Three Dollar Gold",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=5.015,
                                                    diameter_mm=20.5,
                                                    rarity=rarity))
        
        return coins
    
    def get_half_eagles(self) -> List[Dict]:
        """Return Half Eagle ($5) coin data."""
        coins = []
        
        # Capped Bust Right (1795-1807)
        for year in range(1795, 1808):
            if year == 1801:
                continue
            coins.append(self._create_gold_coin("HECB", "Half Eagle Capped Bust", year, "P", "Half Eagles",
                                                composition={"gold": 91.67, "copper": 8.33},
                                                weight_grams=8.75,
                                                diameter_mm=25.0))
        
        # Capped Bust Left (1807-1812)
        for year in range(1807, 1813):
            coins.append(self._create_gold_coin("HECL", "Half Eagle Capped Bust Left", year, "P", "Half Eagles",
                                                composition={"gold": 91.67, "copper": 8.33},
                                                weight_grams=8.75,
                                                diameter_mm=25.0))
        
        # Capped Head Left (1813-1834)
        for year in range(1813, 1835):
            if year in [1816, 1817]:
                continue
            coins.append(self._create_gold_coin("HECH", "Half Eagle Capped Head", year, "P", "Half Eagles",
                                                composition={"gold": 91.67, "copper": 8.33},
                                                weight_grams=8.75,
                                                diameter_mm=23.8))
        
        # Classic Head (1834-1838)
        for year in range(1834, 1839):
            mints = self._get_half_eagle_classic_mints(year)
            for mint in mints:
                coins.append(self._create_gold_coin("HECL", "Half Eagle Classic Head", year, mint, "Half Eagles",
                                                    composition={"gold": 89.92, "copper": 10.08},
                                                    weight_grams=8.36,
                                                    diameter_mm=22.5))
        
        # Liberty Head (1839-1908)
        for year in range(1839, 1909):
            mints = self._get_half_eagle_liberty_mints(year)
            for mint in mints:
                coins.append(self._create_gold_coin("HELH", "Half Eagle Liberty Head", year, mint, "Half Eagles",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=8.359,
                                                    diameter_mm=21.6))
        
        # Indian Head (1908-1929)
        for year in range(1908, 1930):
            if year in [1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928]:
                continue
            mints = self._get_half_eagle_indian_mints(year)
            for mint in mints:
                coins.append(self._create_gold_coin("HEIH", "Half Eagle Indian Head", year, mint, "Half Eagles",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=8.359,
                                                    diameter_mm=21.6))
        
        return coins
    
    def get_eagles(self) -> List[Dict]:
        """Return Eagle ($10) coin data."""
        coins = []
        
        # Capped Bust Right (1795-1804)
        for year in range(1795, 1805):
            if year in [1798, 1802]:
                continue
            coins.append(self._create_gold_coin("EACB", "Eagle Capped Bust", year, "P", "Eagles",
                                                composition={"gold": 91.67, "copper": 8.33},
                                                weight_grams=17.5,
                                                diameter_mm=33.0))
        
        # Liberty Head (1838-1907)
        for year in range(1838, 1908):
            if year in range(1805, 1838):
                continue
            mints = self._get_eagle_liberty_mints(year)
            for mint in mints:
                coins.append(self._create_gold_coin("EALH", "Eagle Liberty Head", year, mint, "Eagles",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=16.718,
                                                    diameter_mm=27.0))
        
        # Indian Head (1907-1933)
        for year in range(1907, 1934):
            if year in [1917, 1918, 1919, 1921, 1922, 1923, 1924, 1925, 1927, 1928, 1929, 1931]:
                continue
            mints = self._get_eagle_indian_mints(year)
            for mint in mints:
                coins.append(self._create_gold_coin("EAIH", "Eagle Indian Head", year, mint, "Eagles",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=16.718,
                                                    diameter_mm=27.0))
        
        return coins
    
    def get_double_eagles(self) -> List[Dict]:
        """Return Double Eagle ($20) coin data."""
        coins = []
        
        # Liberty Head (1849-1907)
        for year in range(1849, 1908):
            mints = self._get_double_eagle_liberty_mints(year)
            for mint in mints:
                rarity = "common"
                if year == 1849 and mint == 'P':
                    rarity = "key"  # First year, unique design
                elif year == 1861 and mint == 'O':
                    rarity = "key"  # Confederate issue
                elif year in [1854, 1855, 1856] and mint == 'O':
                    rarity = "scarce"
                elif year == 1870 and mint == 'CC':
                    rarity = "key"  # Extremely rare
                
                coins.append(self._create_gold_coin("DELH", "Double Eagle Liberty Head", year, mint, "Double Eagles",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=33.436,
                                                    diameter_mm=34.0,
                                                    rarity=rarity))
        
        # Saint-Gaudens (1907-1933)
        for year in range(1907, 1934):
            if year in [1917, 1918, 1919]:
                continue
            mints = self._get_double_eagle_saint_mints(year)
            for mint in mints:
                rarity = "common"
                if year == 1907 and mint == 'P':
                    # High Relief variety
                    coins.append(self._create_gold_coin("DESG", "Double Eagle Saint-Gaudens", year, mint, "Double Eagles",
                                                        composition={"gold": 90, "copper": 10},
                                                        weight_grams=33.436,
                                                        diameter_mm=34.0,
                                                        rarity="key",
                                                        varieties=json.dumps([{"name": "High Relief", "description": "Ultra High Relief pattern"}])))
                
                if year == 1933:
                    rarity = "key"  # Not released to circulation
                elif year in [1920, 1921] and mint == 'S':
                    rarity = "scarce"
                elif year >= 1929:
                    rarity = "scarce"
                
                coins.append(self._create_gold_coin("DESG", "Double Eagle Saint-Gaudens", year, mint, "Double Eagles",
                                                    composition={"gold": 90, "copper": 10},
                                                    weight_grams=33.436,
                                                    diameter_mm=34.0,
                                                    rarity=rarity))
        
        return coins
    
    def _create_gold_coin(self, series_code: str, series_name: str, year: int, mint: str, 
                         denomination: str, composition: Dict, weight_grams: float, 
                         diameter_mm: float, rarity: str = "common", varieties: str = None) -> Dict:
        """Helper to create a gold coin entry."""
        coin_id = f"US-{series_code}-{year}-{mint}"
        
        # Determine obverse and reverse descriptions based on series
        obverse_desc, reverse_desc = self._get_design_descriptions(series_name)
        
        return {
            "coin_id": coin_id,
            "series_id": series_code.lower(),
            "series_name": series_name,
            "year": year,
            "mint": mint,
            "denomination": denomination,
            "country": "US",
            "composition": json.dumps(composition),
            "weight_grams": weight_grams,
            "diameter_mm": diameter_mm,
            "rarity": rarity,
            "varieties": varieties or json.dumps([]),
            "obverse_description": obverse_desc,
            "reverse_description": reverse_desc,
            "distinguishing_features": f"{series_name} dated {year} with {mint} mint mark",
            "identification_keywords": f"gold {denomination.lower()} {series_name.lower()} {year}",
            "common_names": series_name
        }
    
    def _get_design_descriptions(self, series_name: str) -> tuple:
        """Get obverse and reverse descriptions for each series."""
        designs = {
            "Gold Dollar Type I": ("Liberty Head facing left", "Wreath with denomination"),
            "Gold Dollar Type II": ("Indian Princess Head with feather headdress", "Wreath with denomination and date"),
            "Gold Dollar Type III": ("Indian Princess Head with larger feather headdress", "Wreath with denomination and date"),
            "Quarter Eagle Capped Bust": ("Liberty with cap facing right", "Eagle with shield"),
            "Quarter Eagle Capped Bust Left": ("Liberty with cap facing left", "Eagle with shield"),
            "Quarter Eagle Capped Head": ("Liberty with turban-style cap", "Eagle with shield"),
            "Quarter Eagle Classic Head": ("Classic Liberty Head without turban", "Eagle without shield"),
            "Quarter Eagle Liberty Head": ("Liberty Head with coronet inscribed LIBERTY", "Eagle with shield and arrows"),
            "Quarter Eagle Indian Head": ("Native American head with headdress", "Eagle standing on arrows and olive branch"),
            "Three Dollar Gold": ("Indian Princess Head with feather headdress", "Wreath with denomination and date"),
            "Half Eagle Capped Bust": ("Liberty with cap facing right", "Small eagle"),
            "Half Eagle Capped Bust Left": ("Liberty with cap facing left", "Eagle with shield"),
            "Half Eagle Capped Head": ("Liberty with turban-style cap", "Eagle with shield and motto"),
            "Half Eagle Classic Head": ("Classic Liberty Head without turban", "Eagle without shield"),
            "Half Eagle Liberty Head": ("Liberty Head with coronet inscribed LIBERTY", "Eagle with shield, arrows, and olive branch"),
            "Half Eagle Indian Head": ("Native American head with war bonnet", "Eagle standing on arrows and olive branch"),
            "Eagle Capped Bust": ("Liberty with cap facing right", "Small eagle with wreath"),
            "Eagle Liberty Head": ("Liberty Head with coronet inscribed LIBERTY", "Eagle with shield, arrows, olive branch, and motto"),
            "Eagle Indian Head": ("Native American head with war bonnet", "Eagle standing on arrows and olive branch with motto"),
            "Double Eagle Liberty Head": ("Liberty Head with coronet, stars, and date", "Eagle with shield, arrows, olive branch, rays, and motto"),
            "Double Eagle Saint-Gaudens": ("Standing Liberty with torch and olive branch", "Flying eagle over sun rays with motto")
        }
        return designs.get(series_name, ("Liberty design", "Eagle design"))
    
    def _get_gold_dollar_mints_by_year(self, year: int) -> List[str]:
        """Get active mints for Gold Dollar Type III by year."""
        if year == 1856:
            return ['P', 'D']
        elif year == 1857:
            return ['P', 'C', 'D', 'S']
        elif year == 1858:
            return ['P', 'D', 'S']
        elif year == 1859:
            return ['P', 'C', 'D', 'S']
        elif year == 1860:
            return ['P', 'D', 'S']
        elif year in [1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869]:
            return ['P', 'S']
        elif year in range(1870, 1884):
            return ['P', 'S']
        elif year in range(1884, 1890):
            return ['P']
        else:
            return ['P']
    
    def _get_quarter_eagle_classic_mints(self, year: int) -> List[str]:
        """Get active mints for Quarter Eagle Classic Head by year."""
        if year in [1834, 1835, 1836]:
            return ['P']
        elif year in [1837, 1838, 1839]:
            return ['P', 'C', 'D', 'O']
        else:
            return ['P']
    
    def _get_quarter_eagle_liberty_mints(self, year: int) -> List[str]:
        """Get active mints for Quarter Eagle Liberty Head by year."""
        # Simplified logic - would need full historical data for accuracy
        if year < 1838:
            return ['P']
        elif year < 1861:
            return ['P', 'C', 'D', 'O', 'S'] if year >= 1850 else ['P', 'C', 'D', 'O']
        elif year < 1879:
            return ['P', 'S']
        else:
            return ['P']
    
    def _get_three_dollar_mints(self, year: int) -> List[str]:
        """Get active mints for Three Dollar Gold by year."""
        if year == 1854:
            return ['P', 'D', 'O']
        elif year == 1855:
            return ['P', 'S']
        elif year in range(1856, 1871):
            return ['P', 'S'] if year >= 1856 else ['P']
        elif year in range(1871, 1890):
            return ['P', 'S'] if year in [1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878] else ['P']
        else:
            return ['P']
    
    def _get_half_eagle_classic_mints(self, year: int) -> List[str]:
        """Get active mints for Half Eagle Classic Head by year."""
        if year in [1834, 1835, 1836, 1837]:
            return ['P']
        elif year == 1838:
            return ['P', 'C', 'D']
        else:
            return ['P']
    
    def _get_half_eagle_liberty_mints(self, year: int) -> List[str]:
        """Get active mints for Half Eagle Liberty Head by year."""
        # Simplified - would need complete historical data
        if year < 1838:
            return ['P']
        elif year < 1861:
            mints = ['P']
            if year >= 1838:
                mints.extend(['C', 'D', 'O'])
            if year >= 1854:
                mints.append('S')
            return mints
        elif year < 1907:
            mints = ['P', 'S']
            if year >= 1870 and year <= 1893:
                mints.append('CC')
            if year >= 1892:
                mints.append('O')
            if year >= 1906:
                mints.append('D')
            return mints
        else:
            return ['P', 'D', 'S']
    
    def _get_half_eagle_indian_mints(self, year: int) -> List[str]:
        """Get active mints for Half Eagle Indian Head by year."""
        if year in [1908, 1909]:
            return ['P', 'D', 'S', 'O']
        elif year in [1910, 1911, 1912, 1913, 1914, 1915, 1916]:
            return ['P', 'D', 'S']
        elif year == 1929:
            return ['P']
        else:
            return ['P']
    
    def _get_eagle_liberty_mints(self, year: int) -> List[str]:
        """Get active mints for Eagle Liberty Head by year."""
        if year < 1840:
            return ['P']
        elif year < 1861:
            mints = ['P']
            if year >= 1841:
                mints.append('O')
            if year >= 1850:
                mints.append('S')
            return mints
        elif year < 1908:
            mints = ['P', 'S']
            if year >= 1870 and year <= 1893:
                mints.append('CC')
            if year >= 1879 and year <= 1906:
                mints.append('O')
            if year >= 1906:
                mints.append('D')
            return mints
        else:
            return ['P']
    
    def _get_eagle_indian_mints(self, year: int) -> List[str]:
        """Get active mints for Eagle Indian Head by year."""
        if year in [1907, 1908, 1909]:
            return ['P', 'D']
        elif year in [1910, 1911, 1912, 1913, 1914, 1915, 1916]:
            return ['P', 'D', 'S']
        elif year == 1920:
            return ['S']
        elif year == 1926:
            return ['P']
        elif year == 1930:
            return ['S']
        elif year in [1932, 1933]:
            return ['P']
        else:
            return ['P']
    
    def _get_double_eagle_liberty_mints(self, year: int) -> List[str]:
        """Get active mints for Double Eagle Liberty Head by year."""
        if year == 1849:
            return ['P']
        elif year < 1861:
            mints = ['P']
            if year >= 1850:
                mints.append('O')
            if year >= 1854:
                mints.append('S')
            return mints
        elif year < 1908:
            mints = ['P', 'S']
            if year >= 1870 and year <= 1893:
                mints.append('CC')
            if year >= 1879 and year <= 1907:
                if year not in range(1880, 1907):
                    mints.append('O')
            if year >= 1906:
                mints.append('D')
            return mints
        else:
            return ['P']
    
    def _get_double_eagle_saint_mints(self, year: int) -> List[str]:
        """Get active mints for Double Eagle Saint-Gaudens by year."""
        if year in [1907, 1908]:
            return ['P', 'D']
        elif year in range(1909, 1917):
            return ['P', 'D', 'S']
        elif year in range(1920, 1928):
            return ['P', 'S'] if year != 1921 else ['P']
        elif year in [1928, 1929, 1930, 1931, 1932]:
            return ['P']
        elif year == 1933:
            return ['P']  # Never officially released
        else:
            return ['P']
    
    def add_coins_to_database(self, coins: List[Dict], dry_run: bool = False):
        """Add coins to the database."""
        if dry_run:
            print(f"\nDRY RUN - Would add {len(coins)} gold coins")
            for coin in coins[:5]:
                print(f"  {coin['coin_id']}: {coin['series_name']}")
            print(f"  ... and {len(coins) - 5} more")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        added_count = 0
        skipped_count = 0
        
        for coin in coins:
            try:
                cursor.execute("""
                    INSERT INTO coins (
                        coin_id, series_id, series_name, year, mint, denomination,
                        country, composition, weight_grams, diameter_mm, rarity,
                        varieties, obverse_description, reverse_description,
                        distinguishing_features, identification_keywords, common_names
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    coin['coin_id'], coin['series_id'], coin['series_name'],
                    coin['year'], coin['mint'], coin['denomination'],
                    coin['country'], coin['composition'], coin['weight_grams'],
                    coin['diameter_mm'], coin['rarity'], coin['varieties'],
                    coin['obverse_description'], coin['reverse_description'],
                    coin['distinguishing_features'], coin['identification_keywords'],
                    coin['common_names']
                ))
                added_count += 1
            except sqlite3.IntegrityError:
                skipped_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✓ Added {added_count} gold coins")
        if skipped_count > 0:
            print(f"  Skipped {skipped_count} existing coins")
    
    def run_migration(self, dry_run: bool = False):
        """Run the complete migration."""
        print("Starting US Gold Coins migration...")
        
        if not dry_run:
            self.create_backup()
        
        all_coins = []
        
        # Collect all gold coins
        print("\nCollecting Gold Dollars...")
        gold_dollars = self.get_gold_dollars()
        all_coins.extend(gold_dollars)
        print(f"  Found {len(gold_dollars)} Gold Dollar coins")
        
        print("\nCollecting Quarter Eagles...")
        quarter_eagles = self.get_quarter_eagles()
        all_coins.extend(quarter_eagles)
        print(f"  Found {len(quarter_eagles)} Quarter Eagle coins")
        
        print("\nCollecting Three Dollar Gold...")
        three_dollars = self.get_three_dollar_gold()
        all_coins.extend(three_dollars)
        print(f"  Found {len(three_dollars)} Three Dollar Gold coins")
        
        print("\nCollecting Half Eagles...")
        half_eagles = self.get_half_eagles()
        all_coins.extend(half_eagles)
        print(f"  Found {len(half_eagles)} Half Eagle coins")
        
        print("\nCollecting Eagles...")
        eagles = self.get_eagles()
        all_coins.extend(eagles)
        print(f"  Found {len(eagles)} Eagle coins")
        
        print("\nCollecting Double Eagles...")
        double_eagles = self.get_double_eagles()
        all_coins.extend(double_eagles)
        print(f"  Found {len(double_eagles)} Double Eagle coins")
        
        print(f"\nTotal coins to add: {len(all_coins)}")
        
        # Add to database
        self.add_coins_to_database(all_coins, dry_run)
        
        if not dry_run:
            print("\n✓ Migration complete!")
            print(f"  Backup saved to: {self.backup_path}")
            print("\nNext steps:")
            print("1. Run: python scripts/export_from_database.py")
            print("2. Commit changes: git add . && git commit -m 'Add US gold coins (Issue #35)'")

def main():
    parser = argparse.ArgumentParser(description='Add US gold coins to the database')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying database')
    args = parser.parse_args()
    
    backfill = USGoldCoinsBackfill()
    backfill.run_migration(dry_run=args.dry_run)

if __name__ == "__main__":
    main()