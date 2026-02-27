#!/usr/bin/env python3
"""
Fix Engelhard country codes — bars produced in Canada, Australia, and UK
were incorrectly tagged as US.

Remaps coin_id country prefix:
- Canadian bars: US → CA
- Australian bars: US → AU
- UK bars (London, Sheffield): US → GB
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

DB_PATH = Path("database/coins.db")
BACKUP_DIR = Path("backups")

# old_coin_id → new_coin_id
REMAPS = {
    # Canadian — Engelhard Industries of Canada
    "US-EN02-XXXX-X": "CA-EN02-XXXX-X",
    "US-EN03-XXXX-X": "CA-EN03-XXXX-X",
    "US-EN04-XXXX-X": "CA-EN04-XXXX-X",
    "US-EN05-XXXX-X": "CA-EN05-XXXX-X",
    "US-EN06-XXXX-X": "CA-EN06-XXXX-X",
    "US-EN07-XXXX-X": "CA-EN07-XXXX-X",
    "US-EN08-XXXX-X": "CA-EN08-XXXX-X",
    "US-EN09-XXXX-X": "CA-EN09-XXXX-X",
    "US-EN10-XXXX-X": "CA-EN10-XXXX-X",
    "US-EN11-XXXX-X": "CA-EN11-XXXX-X",
    # Canadian — Maple Leaf logo bars (produced in Canada)
    "US-EN43-XXXX-X": "CA-EN43-XXXX-X",
    "US-EN44-XXXX-X": "CA-EN44-XXXX-X",
    "US-EN45-XXXX-X": "CA-EN45-XXXX-X",
    "US-EN46-XXXX-X": "CA-EN46-XXXX-X",
    "US-EN47-XXXX-X": "CA-EN47-XXXX-X",  # Argentor Dealers (Montreal)
    "US-EN48-XXXX-X": "CA-EN48-XXXX-X",
    "US-EN49-XXXX-X": "CA-EN49-XXXX-X",
    # Canadian — branded bars for Canadian companies
    "US-EN66-XXXX-X": "CA-EN66-XXXX-X",  # Scotiabank
    "US-EN67-XXXX-X": "CA-EN67-XXXX-X",  # Toronto Dominion Bank
    "US-EN68-XXXX-X": "CA-EN68-XXXX-X",  # Victoria General Hospital
    "US-EN69-XXXX-X": "CA-EN69-XXXX-X",  # Litton Systems Canada
    "US-EN70-XXXX-X": "CA-EN70-XXXX-X",  # Club of Kings (PAR EXCELLENCE)
    # Australian
    "US-EN50-XXXX-X": "AU-EN50-XXXX-X",
    "US-EN51-XXXX-X": "AU-EN51-XXXX-X",
    "US-EN52-XXXX-X": "AU-EN52-XXXX-X",
    "US-EN53-XXXX-X": "AU-EN53-XXXX-X",
    # UK — London and Sheffield
    "US-EN31-XXXX-X": "GB-EN31-XXXX-X",  # Engelhard London
    "US-EN54-XXXX-X": "GB-EN54-XXXX-X",  # Sheffield Smelting
    "US-EN55-XXXX-X": "GB-EN55-XXXX-X",  # Sheffield Smelting (Serial)
}


def main():
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"coins_backup_{ts}.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup: {backup_path}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    remapped = 0
    for old_id, new_id in REMAPS.items():
        cur.execute("SELECT coin_id, series FROM coins WHERE coin_id=?", (old_id,))
        row = cur.fetchone()
        if not row:
            print(f"  SKIP {old_id}: not found")
            continue

        # Read old entry
        cur.execute("SELECT * FROM coins WHERE coin_id=?", (old_id,))
        old = dict(cur.fetchone())

        # Insert new entry with updated coin_id
        old["coin_id"] = new_id
        cols = list(old.keys())
        placeholders = ",".join("?" * len(cols))
        cur.execute(
            f"INSERT OR IGNORE INTO coins ({','.join(cols)}) VALUES ({placeholders})",
            list(old.values()),
        )

        # Delete old entry
        cur.execute("DELETE FROM coins WHERE coin_id=?", (old_id,))
        print(f"  {old_id} → {new_id}  ({row['series']})")
        remapped += 1

    print(f"\nRemapped {remapped} entries")

    # Summary by country
    for country in ["CA", "AU", "GB", "US"]:
        cur.execute(
            "SELECT COUNT(*) as cnt FROM coins WHERE coin_id LIKE ? AND coin_id LIKE '%-EN%-XXXX-%'",
            (f"{country}-%",),
        )
        print(f"  {country}: {cur.fetchone()['cnt']} Engelhard entries")

    conn.commit()
    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
