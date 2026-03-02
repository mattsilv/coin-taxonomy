#!/usr/bin/env python3
"""
Expand major US coin series that are stubs (1 coin) or completely missing.

Adds complete year+mint combinations for:
- Peace Dollar (PEAC) - NEW
- Washington Quarter (WASQ) - NEW
- Buffalo Nickel (BUFF) - NEW
- Jefferson Nickel (JEFF) - NEW
- Trade Dollar (TRAD) - NEW
- Lincoln Memorial Cent (LMCT) - NEW
- Kennedy Half Dollar (KENH) - EXPAND
- Franklin Half Dollar (FRNH) - EXPAND
- Walking Liberty Half Dollar (WLHD) - EXPAND
- Eisenhower Dollar (EISE) - EXPAND
- Lincoln Wheat Cent (LWCT) - EXPAND
- Sacagawea Dollar (SACA) - EXPAND

Database-first pipeline: SQLite is source of truth, JSON regenerated via export.
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "coins.db"
BACKUP_DIR = DB_PATH.parent / "backups"


def create_backup():
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"coins_backup_{ts}_before_series_expansion.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def get_existing_coin_ids(conn):
    """Return set of all existing coin_ids."""
    cur = conn.execute("SELECT coin_id FROM coins")
    return {row[0] for row in cur.fetchall()}


# ---------------------------------------------------------------------------
# Mint operation ranges
# ---------------------------------------------------------------------------
# Philadelphia (P): always open
# Denver (D): 1906+
# San Francisco (S): 1854-1955, 1968+
# New Orleans (O): 1838-1909
# Carson City (CC): 1870-1893
# West Point (W): 1984+ (bullion/commemorative)

def mints_for_year(year, series_mints):
    """Return list of mint marks active for a given year, filtered by series_mints config."""
    active = []
    for m in series_mints:
        if m == "P":
            active.append("P")
        elif m == "D" and year >= 1906:
            active.append("D")
        elif m == "S":
            if (1854 <= year <= 1955) or year >= 1968:
                active.append("S")
        elif m == "O" and 1838 <= year <= 1909:
            active.append("O")
        elif m == "CC" and 1870 <= year <= 1893:
            active.append("CC")
        elif m == "W" and year >= 1984:
            active.append("W")
    return active


def generate_coins(type_code, series_name, denomination, years, possible_mints,
                   composition, weight, diameter, edge, designer,
                   obverse_desc, reverse_desc, skip_years=None,
                   key_dates=None, semi_key_dates=None, scarce_dates=None,
                   mint_overrides=None, notes_map=None):
    """Generate coin dicts for all year+mint combos."""
    coins = []
    skip = skip_years or set()
    keys = key_dates or set()
    semi_keys = semi_key_dates or set()
    scarces = scarce_dates or set()
    overrides = mint_overrides or {}
    notes = notes_map or {}

    for year in years:
        if year in skip:
            continue
        # Allow per-year mint overrides
        if year in overrides:
            year_mints = overrides[year]
        else:
            year_mints = mints_for_year(year, possible_mints)

        for mint in year_mints:
            coin_id = f"US-{type_code}-{year}-{mint}"

            # Determine rarity
            ym = (year, mint)
            if ym in keys or year in keys:
                rarity = "key"
            elif ym in semi_keys or year in semi_keys:
                rarity = "semi-key"
            elif ym in scarces or year in scarces:
                rarity = "scarce"
            else:
                rarity = "common"

            coin = {
                "coin_id": coin_id,
                "year": str(year),
                "mint": mint,
                "denomination": denomination,
                "series": series_name,
                "composition": composition,
                "weight_grams": weight,
                "diameter_mm": diameter,
                "edge": edge,
                "designer": designer,
                "obverse_description": obverse_desc,
                "reverse_description": reverse_desc,
                "rarity": rarity,
                "notes": notes.get(ym, notes.get(year, None)),
                "source_citation": "US Mint / Red Book",
            }
            coins.append(coin)
    return coins


# ============================================================================
# Series definitions
# ============================================================================

def peace_dollar():
    """Peace Dollar 1921-1935 (no 1929-1933)."""
    return generate_coins(
        type_code="PEAC",
        series_name="Peace Dollar",
        denomination="Dollars",
        years=range(1921, 1936),
        possible_mints=["P", "D", "S"],
        composition='{"silver": 90, "copper": 10}',
        weight=26.73, diameter=38.1, edge="Reeded",
        designer="Anthony de Francisci",
        obverse_desc="Head of Liberty facing left wearing radiate crown, 'LIBERTY' above, 'IN GOD WE TRUST' below, date at bottom.",
        reverse_desc="Bald eagle at rest on olive branch, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'ONE DOLLAR', rays of sun behind.",
        skip_years={1929, 1930, 1931, 1932, 1933},
        key_dates={(1921, "P"), (1928, "P")},
        semi_key_dates={(1934, "S"), (1925, "S"), (1927, "D")},
        mint_overrides={
            1921: ["P"],  # Only Philadelphia in 1921
            1922: ["P", "D"],  # No S in 1922
            1928: ["P"],  # Only Philadelphia
        },
    )


def washington_quarter():
    """Washington Quarter 1932-1998 (silver through clad era, pre-state quarters)."""
    coins = []
    # Silver era 1932-1964
    coins += generate_coins(
        type_code="WASQ",
        series_name="Washington Quarter",
        denomination="Quarters",
        years=range(1932, 1965),
        possible_mints=["P", "D", "S"],
        composition='{"silver": 90, "copper": 10}',
        weight=6.25, diameter=24.3, edge="Reeded",
        designer="John Flanagan",
        obverse_desc="Bust of George Washington facing left, 'LIBERTY' above, 'IN GOD WE TRUST' at left, date below.",
        reverse_desc="Heraldic eagle with wings spread, olive branches below, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'QUARTER DOLLAR'.",
        skip_years={1933},
        key_dates={(1932, "D"), (1932, "S")},
        semi_key_dates={(1936, "D"), (1935, "D"), (1937, "S")},
        mint_overrides={
            1932: ["P", "D", "S"],
            1933: [],
            1934: ["P", "D"],
            1935: ["P", "D", "S"],
            # 1938 S, 1939 S did not produce quarters
        },
    )
    # Clad era 1965-1998
    coins += generate_coins(
        type_code="WASQ",
        series_name="Washington Quarter",
        denomination="Quarters",
        years=range(1965, 1999),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 75, "nickel": 25}',
        weight=5.67, diameter=24.3, edge="Reeded",
        designer="John Flanagan",
        obverse_desc="Bust of George Washington facing left, 'LIBERTY' above, 'IN GOD WE TRUST' at left, date below.",
        reverse_desc="Heraldic eagle with wings spread, olive branches below, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'QUARTER DOLLAR'.",
    )
    return coins


def kennedy_half():
    """Kennedy Half Dollar 1964-2024."""
    coins = []
    # 1964 - 90% silver
    coins += generate_coins(
        type_code="KENH",
        series_name="Kennedy Half Dollar",
        denomination="Half Dollars",
        years=[1964],
        possible_mints=["P", "D"],
        composition='{"silver": 90, "copper": 10}',
        weight=12.5, diameter=30.6, edge="Reeded",
        designer="Gilroy Roberts / Frank Gasparro",
        obverse_desc="Bust of John F. Kennedy facing left, 'LIBERTY' above, 'IN GOD WE TRUST' below, date at bottom.",
        reverse_desc="Presidential coat of arms (heraldic eagle), 'UNITED STATES OF AMERICA', 'HALF DOLLAR'.",
    )
    # 1965-1970 - 40% silver
    coins += generate_coins(
        type_code="KENH",
        series_name="Kennedy Half Dollar",
        denomination="Half Dollars",
        years=range(1965, 1971),
        possible_mints=["P", "D", "S"],
        composition='{"silver": 40, "copper": 60}',
        weight=11.5, diameter=30.6, edge="Reeded",
        designer="Gilroy Roberts / Frank Gasparro",
        obverse_desc="Bust of John F. Kennedy facing left, 'LIBERTY' above, 'IN GOD WE TRUST' below, date at bottom.",
        reverse_desc="Presidential coat of arms (heraldic eagle), 'UNITED STATES OF AMERICA', 'HALF DOLLAR'.",
        mint_overrides={
            1965: ["P"], 1966: ["P"], 1967: ["P"],  # No mint marks 1965-1967
        },
    )
    # 1971-2024 - Clad
    coins += generate_coins(
        type_code="KENH",
        series_name="Kennedy Half Dollar",
        denomination="Half Dollars",
        years=range(1971, 2025),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 75, "nickel": 25}',
        weight=11.34, diameter=30.6, edge="Reeded",
        designer="Gilroy Roberts / Frank Gasparro",
        obverse_desc="Bust of John F. Kennedy facing left, 'LIBERTY' above, 'IN GOD WE TRUST' below, date at bottom.",
        reverse_desc="Presidential coat of arms (heraldic eagle), 'UNITED STATES OF AMERICA', 'HALF DOLLAR'.",
        mint_overrides={
            # No business strikes some years, but coin exists as proof
            1987: ["P", "D", "S"],
        },
    )
    return coins


def franklin_half():
    """Franklin Half Dollar 1948-1963."""
    return generate_coins(
        type_code="FRNH",
        series_name="Franklin Half Dollar",
        denomination="Half Dollars",
        years=range(1948, 1964),
        possible_mints=["P", "D", "S"],
        composition='{"silver": 90, "copper": 10}',
        weight=12.5, diameter=30.6, edge="Reeded",
        designer="John R. Sinnock",
        obverse_desc="Bust of Benjamin Franklin facing right, 'LIBERTY' above, 'IN GOD WE TRUST' below, date at bottom.",
        reverse_desc="Liberty Bell with small eagle to right, 'UNITED STATES OF AMERICA', 'HALF DOLLAR', 'E PLURIBUS UNUM'.",
        semi_key_dates={(1949, "S"), (1953, "S")},
        mint_overrides={
            1948: ["P", "D"],
            1949: ["P", "D", "S"],
            1950: ["P", "D"],
            1951: ["P", "D", "S"],
            1952: ["P", "D", "S"],
            1953: ["P", "D", "S"],
            1954: ["P", "D", "S"],
            1955: ["P"],  # Only Philadelphia in 1955
            1956: ["P"],
            1957: ["P", "D"],
            1958: ["P", "D"],
            1959: ["P", "D"],
            1960: ["P", "D"],
            1961: ["P", "D"],
            1962: ["P", "D"],
            1963: ["P", "D"],
        },
    )


def walking_liberty_half():
    """Walking Liberty Half Dollar 1916-1947."""
    return generate_coins(
        type_code="WLHD",
        series_name="Walking Liberty Half Dollar",
        denomination="Half Dollars",
        years=range(1916, 1948),
        possible_mints=["P", "D", "S"],
        composition='{"silver": 90, "copper": 10}',
        weight=12.5, diameter=30.6, edge="Reeded",
        designer="Adolph A. Weinman",
        obverse_desc="Full-length figure of Liberty walking toward the sun, draped in American flag, 'LIBERTY', 'IN GOD WE TRUST', date.",
        reverse_desc="Bald eagle standing on a rock with wings raised, pine branch, 'UNITED STATES OF AMERICA', 'HALF DOLLAR', 'E PLURIBUS UNUM'.",
        skip_years={1922, 1924, 1925, 1926, 1930, 1931, 1932},
        key_dates={(1916, "S"), (1921, "P"), (1921, "D")},
        semi_key_dates={(1916, "D"), (1917, "S"), (1938, "D")},
        mint_overrides={
            1916: ["P", "D", "S"],
            1917: ["P", "D", "S"],
            1918: ["P", "D", "S"],
            1919: ["P", "D", "S"],
            1920: ["P", "D", "S"],
            1921: ["P", "D", "S"],
            1923: ["P", "S"],
            1927: ["P", "S"],
            1928: ["P", "S"],
            1929: ["P", "D", "S"],
            1933: ["P", "S"],
            1934: ["P", "D", "S"],
            1935: ["P", "D", "S"],
            1936: ["P", "D", "S"],
            1937: ["P", "D", "S"],
            1938: ["P", "D"],
            1939: ["P", "D", "S"],
            1940: ["P", "S"],
            1941: ["P", "D", "S"],
            1942: ["P", "D", "S"],
            1943: ["P", "D", "S"],
            1944: ["P", "D", "S"],
            1945: ["P", "D", "S"],
            1946: ["P", "D", "S"],
            1947: ["P", "D"],
        },
    )


def buffalo_nickel():
    """Buffalo (Indian Head) Nickel 1913-1938."""
    return generate_coins(
        type_code="BUFF",
        series_name="Buffalo Nickel",
        denomination="Nickels",
        years=range(1913, 1939),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 75, "nickel": 25}',
        weight=5.0, diameter=21.2, edge="Plain",
        designer="James Earle Fraser",
        obverse_desc="Native American chief facing right, 'LIBERTY' at right, date below.",
        reverse_desc="American bison standing on mound, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'FIVE CENTS'.",
        skip_years={1922, 1932, 1933},
        key_dates={(1913, "S"), (1914, "D"), (1926, "S")},
        semi_key_dates={(1913, "D"), (1915, "S"), (1924, "S"), (1925, "S")},
        mint_overrides={
            1921: ["P", "S"],
            1923: ["P", "S"],
            1924: ["P", "D", "S"],
            1925: ["P", "D", "S"],
            1926: ["P", "D", "S"],
            1927: ["P", "D", "S"],
            1928: ["P", "D", "S"],
            1929: ["P", "D", "S"],
            1930: ["P", "S"],
            1931: ["P", "S"],
            1934: ["P", "D"],
            1935: ["P", "D", "S"],
            1936: ["P", "D", "S"],
            1937: ["P", "D", "S"],
            1938: ["P", "D"],
        },
    )


def jefferson_nickel():
    """Jefferson Nickel 1938-2024."""
    coins = []
    # Pre-war 1938-1942
    coins += generate_coins(
        type_code="JEFF",
        series_name="Jefferson Nickel",
        denomination="Nickels",
        years=range(1938, 1943),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 75, "nickel": 25}',
        weight=5.0, diameter=21.2, edge="Plain",
        designer="Felix Schlag",
        obverse_desc="Bust of Thomas Jefferson facing left, 'IN GOD WE TRUST' at left, 'LIBERTY' above, date at right.",
        reverse_desc="Monticello (Jefferson's home), 'MONTICELLO', 'E PLURIBUS UNUM', 'UNITED STATES OF AMERICA', 'FIVE CENTS'.",
    )
    # War nickels 1942-1945 (silver)
    coins += generate_coins(
        type_code="JEFF",
        series_name="Jefferson Nickel",
        denomination="Nickels",
        years=range(1942, 1946),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 56, "silver": 35, "manganese": 9}',
        weight=5.0, diameter=21.2, edge="Plain",
        designer="Felix Schlag",
        obverse_desc="Bust of Thomas Jefferson facing left, 'IN GOD WE TRUST' at left, 'LIBERTY' above, date at right.",
        reverse_desc="Monticello with large mint mark above dome, 'MONTICELLO', 'E PLURIBUS UNUM', 'UNITED STATES OF AMERICA', 'FIVE CENTS'.",
        notes_map={y: "Wartime silver alloy; large mint mark above Monticello dome" for y in range(1942, 1946)},
    )
    # Post-war 1946-2024
    coins += generate_coins(
        type_code="JEFF",
        series_name="Jefferson Nickel",
        denomination="Nickels",
        years=range(1946, 2025),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 75, "nickel": 25}',
        weight=5.0, diameter=21.2, edge="Plain",
        designer="Felix Schlag",
        obverse_desc="Bust of Thomas Jefferson facing left, 'IN GOD WE TRUST' at left, 'LIBERTY' above, date at right.",
        reverse_desc="Monticello (Jefferson's home), 'MONTICELLO', 'E PLURIBUS UNUM', 'UNITED STATES OF AMERICA', 'FIVE CENTS'.",
        skip_years={1950, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964,  # These had S only for proofs
                    1968, 1969, 1970},  # Will handle individually
        mint_overrides={
            1965: ["P"], 1966: ["P"], 1967: ["P"],  # No mint marks
        },
    )
    # Fill in years with specific mints
    coins += generate_coins(
        type_code="JEFF",
        series_name="Jefferson Nickel",
        denomination="Nickels",
        years=range(1950, 1965),
        possible_mints=["P", "D"],
        composition='{"copper": 75, "nickel": 25}',
        weight=5.0, diameter=21.2, edge="Plain",
        designer="Felix Schlag",
        obverse_desc="Bust of Thomas Jefferson facing left, 'IN GOD WE TRUST' at left, 'LIBERTY' above, date at right.",
        reverse_desc="Monticello (Jefferson's home), 'MONTICELLO', 'E PLURIBUS UNUM', 'UNITED STATES OF AMERICA', 'FIVE CENTS'.",
        key_dates={(1950, "D")},
    )
    coins += generate_coins(
        type_code="JEFF",
        series_name="Jefferson Nickel",
        denomination="Nickels",
        years=range(1968, 1971),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 75, "nickel": 25}',
        weight=5.0, diameter=21.2, edge="Plain",
        designer="Felix Schlag",
        obverse_desc="Bust of Thomas Jefferson facing left, 'IN GOD WE TRUST' at left, 'LIBERTY' above, date at right.",
        reverse_desc="Monticello (Jefferson's home), 'MONTICELLO', 'E PLURIBUS UNUM', 'UNITED STATES OF AMERICA', 'FIVE CENTS'.",
    )
    return coins


def lincoln_wheat_cent():
    """Lincoln Wheat Cent 1909-1958."""
    coins = []
    # Bronze 1909-1942
    coins += generate_coins(
        type_code="LWCT",
        series_name="Lincoln Wheat Cent",
        denomination="Cents",
        years=range(1909, 1943),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 95, "tin_zinc": 5}',
        weight=3.11, diameter=19.0, edge="Plain",
        designer="Victor David Brenner",
        obverse_desc="Bust of Abraham Lincoln facing right, 'IN GOD WE TRUST' above, 'LIBERTY' at left, date at right.",
        reverse_desc="Two wheat stalks framing 'ONE CENT' and 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM' above.",
        key_dates={(1909, "S"), (1914, "D")},
        semi_key_dates={(1909, "P"), (1911, "S"), (1912, "S"), (1913, "S"), (1914, "S"), (1915, "S")},
        mint_overrides={
            1909: ["P", "S"],  # VDB variety; D opened 1911 for cents
            1910: ["P", "S"],
            1911: ["P", "D", "S"],
        },
        notes_map={(1909, "P"): "VDB and no-VDB varieties", (1909, "S"): "VDB key date"},
    )
    # Steel cent 1943
    coins += generate_coins(
        type_code="LWCT",
        series_name="Lincoln Wheat Cent",
        denomination="Cents",
        years=[1943],
        possible_mints=["P", "D", "S"],
        composition='{"zinc_coated_steel": 100}',
        weight=2.7, diameter=19.0, edge="Plain",
        designer="Victor David Brenner",
        obverse_desc="Bust of Abraham Lincoln facing right, 'IN GOD WE TRUST' above, 'LIBERTY' at left, date at right.",
        reverse_desc="Two wheat stalks framing 'ONE CENT' and 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM' above.",
        notes_map={1943: "Steel cent due to WWII copper conservation"},
    )
    # Shell case brass 1944-1946
    coins += generate_coins(
        type_code="LWCT",
        series_name="Lincoln Wheat Cent",
        denomination="Cents",
        years=range(1944, 1947),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 95, "zinc": 5}',
        weight=3.11, diameter=19.0, edge="Plain",
        designer="Victor David Brenner",
        obverse_desc="Bust of Abraham Lincoln facing right, 'IN GOD WE TRUST' above, 'LIBERTY' at left, date at right.",
        reverse_desc="Two wheat stalks framing 'ONE CENT' and 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM' above.",
        notes_map={y: "Shell case brass composition" for y in range(1944, 1947)},
    )
    # Back to bronze 1947-1958
    coins += generate_coins(
        type_code="LWCT",
        series_name="Lincoln Wheat Cent",
        denomination="Cents",
        years=range(1947, 1959),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 95, "tin_zinc": 5}',
        weight=3.11, diameter=19.0, edge="Plain",
        designer="Victor David Brenner",
        obverse_desc="Bust of Abraham Lincoln facing right, 'IN GOD WE TRUST' above, 'LIBERTY' at left, date at right.",
        reverse_desc="Two wheat stalks framing 'ONE CENT' and 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM' above.",
        mint_overrides={
            1955: ["P", "D", "S"],
            1956: ["P", "D"],
            1957: ["P", "D"],
            1958: ["P", "D"],
        },
    )
    return coins


def lincoln_memorial_cent():
    """Lincoln Memorial Cent 1959-2008."""
    coins = []
    # Bronze 1959-1982
    coins += generate_coins(
        type_code="LMCT",
        series_name="Lincoln Memorial Cent",
        denomination="Cents",
        years=range(1959, 1983),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 95, "tin_zinc": 5}',
        weight=3.11, diameter=19.0, edge="Plain",
        designer="Victor David Brenner / Frank Gasparro",
        obverse_desc="Bust of Abraham Lincoln facing right, 'IN GOD WE TRUST' above, 'LIBERTY' at left, date at right.",
        reverse_desc="Lincoln Memorial building, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'ONE CENT'.",
        mint_overrides={
            1965: ["P"], 1966: ["P"], 1967: ["P"],  # No mint marks
        },
    )
    # Copper-plated zinc 1982-2008
    coins += generate_coins(
        type_code="LMCT",
        series_name="Lincoln Memorial Cent",
        denomination="Cents",
        years=range(1982, 2009),
        possible_mints=["P", "D", "S"],
        composition='{"zinc": 97.5, "copper": 2.5}',
        weight=2.5, diameter=19.0, edge="Plain",
        designer="Victor David Brenner / Frank Gasparro",
        obverse_desc="Bust of Abraham Lincoln facing right, 'IN GOD WE TRUST' above, 'LIBERTY' at left, date at right.",
        reverse_desc="Lincoln Memorial building, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'ONE CENT'.",
    )
    return coins


def eisenhower_dollar():
    """Eisenhower Dollar 1971-1978."""
    coins = []
    # Clad
    coins += generate_coins(
        type_code="EISE",
        series_name="Eisenhower Dollar",
        denomination="Dollars",
        years=range(1971, 1979),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 75, "nickel": 25}',
        weight=22.68, diameter=38.1, edge="Reeded",
        designer="Frank Gasparro",
        obverse_desc="Bust of Dwight D. Eisenhower facing left, 'LIBERTY' above, 'IN GOD WE TRUST' below, date at bottom.",
        reverse_desc="Eagle landing on the Moon with olive branch (Apollo 11 insignia), Earth above, 'UNITED STATES OF AMERICA', 'ONE DOLLAR', 'E PLURIBUS UNUM'.",
        skip_years={1975},  # No 1975-dated coins; all dated 1776-1976 (Bicentennial)
        notes_map={
            1976: "Bicentennial reverse: Liberty Bell superimposed on the Moon",
        },
    )
    return coins


def sacagawea_dollar():
    """Sacagawea Dollar 2000-2008 (before Native American dollar rebranding)."""
    return generate_coins(
        type_code="SACA",
        series_name="Sacagawea Dollar",
        denomination="Dollars",
        years=range(2000, 2009),
        possible_mints=["P", "D", "S"],
        composition='{"copper": 88.5, "zinc": 6, "manganese": 3.5, "nickel": 2}',
        weight=8.1, diameter=26.5, edge="Plain with lettering",
        designer="Glenna Goodacre",
        obverse_desc="Sacagawea carrying her infant son Jean Baptiste, 'LIBERTY', 'IN GOD WE TRUST', date.",
        reverse_desc="Soaring eagle surrounded by 17 stars, 'UNITED STATES OF AMERICA', 'E PLURIBUS UNUM', 'ONE DOLLAR'.",
        key_dates={(2000, "P")},  # Cheerios variety
        notes_map={(2000, "P"): "Includes rare Cheerios variety with enhanced tail feathers"},
    )


def trade_dollar():
    """Trade Dollar 1873-1885."""
    return generate_coins(
        type_code="TRAD",
        series_name="Trade Dollar",
        denomination="Dollars",
        years=range(1873, 1886),
        possible_mints=["P", "S", "CC"],
        composition='{"silver": 90, "copper": 10}',
        weight=27.22, diameter=38.1, edge="Reeded",
        designer="William Barber",
        obverse_desc="Seated Liberty facing left holding olive branch and wheat, 'LIBERTY' on shield, 'IN GOD WE TRUST' above, date below, 13 stars.",
        reverse_desc="Eagle holding olive branch and three arrows, 'UNITED STATES OF AMERICA', 'TRADE DOLLAR', '420 GRAINS, 900 FINE'.",
        key_dates={(1878, "CC")},
        semi_key_dates={(1875, "CC"), (1876, "CC")},
        mint_overrides={
            1873: ["P", "S", "CC"],
            1874: ["P", "S", "CC"],
            1875: ["P", "S", "CC"],
            1876: ["P", "S", "CC"],
            1877: ["P", "S", "CC"],
            1878: ["P", "S", "CC"],
            1879: ["P"],  # Proof only
            1880: ["P"],
            1881: ["P"],
            1882: ["P"],
            1883: ["P"],
            1884: ["P"],  # Proof only, very rare
            1885: ["P"],  # Proof only, very rare
        },
        scarce_dates={(1884, "P"), (1885, "P")},
        notes_map={
            (1884, "P"): "Proof only, only 10 known",
            (1885, "P"): "Proof only, only 5 known",
        },
    )


# ============================================================================
# Series registry entries
# ============================================================================

NEW_SERIES = [
    {
        "series_id": "Peace Dollar__Dollars",
        "series_name": "Peace Dollar",
        "series_abbreviation": "PEAC",
        "country_code": "US",
        "denomination": "Dollars",
        "start_year": 1921,
        "end_year": 1935,
        "defining_characteristics": "Art Deco design featuring Liberty wearing radiate crown; eagle at rest on olive branch with rays of sunlight",
        "official_name": "Peace Dollar",
        "series_group": "Silver Dollars",
    },
    {
        "series_id": "Washington Quarter__Quarters",
        "series_name": "Washington Quarter",
        "series_abbreviation": "WASQ",
        "country_code": "US",
        "denomination": "Quarters",
        "start_year": 1932,
        "end_year": 1998,
        "defining_characteristics": "George Washington bust obverse; heraldic eagle reverse; silver (1932-1964) then clad",
        "official_name": "Washington Quarter",
        "series_group": "Quarters",
    },
    {
        "series_id": "Buffalo Nickel__Nickels",
        "series_name": "Buffalo Nickel",
        "series_abbreviation": "BUFF",
        "country_code": "US",
        "denomination": "Nickels",
        "start_year": 1913,
        "end_year": 1938,
        "defining_characteristics": "Native American chief obverse; American bison (buffalo) reverse; also called Indian Head Nickel",
        "official_name": "Indian Head Nickel",
        "series_group": "Nickels",
        "aliases": '["Indian Head Nickel", "Indian Head Five Cents"]',
    },
    {
        "series_id": "Jefferson Nickel__Nickels",
        "series_name": "Jefferson Nickel",
        "series_abbreviation": "JEFF",
        "country_code": "US",
        "denomination": "Nickels",
        "start_year": 1938,
        "end_year": 2024,
        "defining_characteristics": "Thomas Jefferson bust obverse; Monticello reverse; wartime silver alloy 1942-1945",
        "official_name": "Jefferson Nickel",
        "series_group": "Nickels",
    },
    {
        "series_id": "Trade Dollar__Dollars",
        "series_name": "Trade Dollar",
        "series_abbreviation": "TRAD",
        "country_code": "US",
        "denomination": "Dollars",
        "start_year": 1873,
        "end_year": 1885,
        "defining_characteristics": "Seated Liberty with olive branch obverse; eagle with 420 GRAINS 900 FINE reverse; heavier than standard silver dollar",
        "official_name": "Trade Dollar",
        "series_group": "Silver Dollars",
    },
    {
        "series_id": "Lincoln Memorial Cent__Cents",
        "series_name": "Lincoln Memorial Cent",
        "series_abbreviation": "LMCT",
        "country_code": "US",
        "denomination": "Cents",
        "start_year": 1959,
        "end_year": 2008,
        "defining_characteristics": "Lincoln bust obverse (same as Wheat Cent); Lincoln Memorial reverse replacing wheat stalks",
        "official_name": "Lincoln Memorial Cent",
        "series_group": "Cents",
    },
]


def insert_coins(conn, coins, existing_ids):
    """Insert coins, skipping duplicates."""
    inserted = 0
    skipped = 0
    for coin in coins:
        if coin["coin_id"] in existing_ids:
            skipped += 1
            continue
        conn.execute(
            """INSERT INTO coins (coin_id, year, mint, denomination, series,
               composition, weight_grams, diameter_mm, edge, designer,
               obverse_description, reverse_description, rarity, notes, source_citation)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                coin["coin_id"], coin["year"], coin["mint"], coin["denomination"],
                coin["series"], coin["composition"], coin["weight_grams"],
                coin["diameter_mm"], coin["edge"], coin["designer"],
                coin["obverse_description"], coin["reverse_description"],
                coin["rarity"], coin.get("notes"), coin["source_citation"],
            ),
        )
        existing_ids.add(coin["coin_id"])
        inserted += 1
    return inserted, skipped


def insert_series_registry(conn, series_list):
    """Insert new series registry entries, skipping existing."""
    inserted = 0
    for s in series_list:
        existing = conn.execute(
            "SELECT 1 FROM series_registry WHERE series_abbreviation = ?",
            (s["series_abbreviation"],),
        ).fetchone()
        if existing:
            # Update start/end years
            conn.execute(
                "UPDATE series_registry SET start_year = ?, end_year = ? WHERE series_abbreviation = ?",
                (s["start_year"], s["end_year"], s["series_abbreviation"]),
            )
            print(f"  Updated {s['series_abbreviation']} year range")
            continue
        conn.execute(
            """INSERT INTO series_registry (series_id, series_name, series_abbreviation,
               country_code, denomination, start_year, end_year, defining_characteristics,
               official_name, series_group, aliases)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                s["series_id"], s["series_name"], s["series_abbreviation"],
                s["country_code"], s["denomination"], s["start_year"], s["end_year"],
                s.get("defining_characteristics"), s.get("official_name"),
                s.get("series_group"), s.get("aliases"),
            ),
        )
        inserted += 1
        print(f"  Added series: {s['series_abbreviation']} - {s['series_name']}")
    return inserted


def update_stub_series_years(conn):
    """Update year ranges for existing stub series that are being expanded."""
    updates = {
        "KEN": (1964, 2024),
        "FRA": (1948, 1963),
        "WAL": (1916, 1947),
        "EIS": (1971, 1978),
        "LIN": (1909, 1958),
        "SAC": (2000, 2008),
    }
    for abbr, (start, end) in updates.items():
        conn.execute(
            "UPDATE series_registry SET start_year = ?, end_year = ? WHERE series_abbreviation = ?",
            (start, end, abbr),
        )
        print(f"  Updated {abbr} year range: {start}-{end}")


def main():
    print("=" * 60)
    print("Expanding major US coin series")
    print("=" * 60)

    # Backup
    create_backup()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    existing_ids = get_existing_coin_ids(conn)
    print(f"\nExisting coins in database: {len(existing_ids)}")

    # Define all series generators
    series_generators = [
        ("Peace Dollar", peace_dollar),
        ("Washington Quarter", washington_quarter),
        ("Kennedy Half Dollar", kennedy_half),
        ("Franklin Half Dollar", franklin_half),
        ("Walking Liberty Half Dollar", walking_liberty_half),
        ("Buffalo Nickel", buffalo_nickel),
        ("Jefferson Nickel", jefferson_nickel),
        ("Lincoln Wheat Cent", lincoln_wheat_cent),
        ("Lincoln Memorial Cent", lincoln_memorial_cent),
        ("Eisenhower Dollar", eisenhower_dollar),
        ("Sacagawea Dollar", sacagawea_dollar),
        ("Trade Dollar", trade_dollar),
    ]

    total_inserted = 0
    total_skipped = 0

    for name, generator in series_generators:
        coins = generator()
        inserted, skipped = insert_coins(conn, coins, existing_ids)
        total_inserted += inserted
        total_skipped += skipped
        print(f"  {name}: +{inserted} coins ({skipped} existing)")

    # Insert new series registry entries
    print("\nUpdating series registry...")
    insert_series_registry(conn, NEW_SERIES)
    update_stub_series_years(conn)

    conn.commit()
    conn.close()

    print(f"\n{'=' * 60}")
    print(f"Total inserted: {total_inserted}")
    print(f"Total skipped (existing): {total_skipped}")
    print(f"New database total: {len(existing_ids)}")
    print("=" * 60)
    print("\nNext: run 'uv run python scripts/export_from_database.py' to regenerate JSON")


if __name__ == "__main__":
    main()
