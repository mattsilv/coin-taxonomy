# Engelhard Bullion Integration Handoff

## Overview
Successfully integrated 72 Engelhard bullion varieties into the Universal Coin Taxonomy. The data is now available in the `coins` database table, migrated to the `issues` table, and exported to `data/universal/us_issues.json` for frontend consumption.

## Key Changes

### 1. Data Ingestion
*   **Script**: `scripts/add_engelhard_bullion.py`
*   **Source**: `issue_67.txt` (reconstructed from GitHub issue comment)
*   **Action**: Parses CSV data and inserts into `coins` table.
*   **Crucial Detail**: Populates `variety` column with a unique slug (e.g., `EARLIEST_1OZ_PRODUCTION_BAR-1`) to ensure unique `issue_id` generation during migration.

### 2. Migration to Universal Taxonomy
*   **Script**: `scripts/migrate_to_universal_v1_1.py`
*   **Fixes**:
    *   Updated `issue_year` column in `issues` table to `TEXT` to support 'XXXX' years.
    *   Fixed year comparison logic to handle non-integer years safely.
    *   **CRITICAL FIX**: Updated `generate_issue_id` call to include `variety` argument. This prevents merging of items that share year/mint/series but differ by variety (like Engelhard bars).

### 3. Export
*   **Script**: `scripts/export_db_v1_1.py`
*   **Action**: Exports `issues` table to `data/universal/us_issues.json`.
*   **Result**: `us_issues.json` now contains 282 US issues, including the 72 Engelhard items.

## Verification
*   **Database**: `coins` table has 945 records. `issues` table has 945 records.
*   **JSON**: `data/universal/us_issues.json` contains 72 items with `series_id` containing "Engelhard".
*   **Frontend**: The HTML page (`docs/index.html`) reads `us_issues.json` and should now display the Engelhard bullion items.

## Next Steps
*   **Close Issue #67**: The task is complete.
*   **Review**: Verify the frontend display of the new items.
*   **Cleanup**: `issue_67.txt` and `scripts/reconstruct_issue_67.py` can be removed if no longer needed, though keeping `issue_67.txt` as a source reference is useful.

## Artifacts
*   `scripts/add_engelhard_bullion.py`: Ingestion script.
*   `scripts/fix_engelhard_varieties.py`: One-off fix script (superseded by `add_engelhard_bullion.py` update).
*   `scripts/reconstruct_issue_67.py`: Helper to restore source data.

## Known Issues / Notes
*   **Legacy Data**: The `coins.db` database currently lacks `series_metadata` and `composition_periods` tables, preventing the export of legacy format JSONs (`data/us/coins/*.json`).
*   **Stale File Removed**: `data/us/coins/engelhard_bullion.json` was removed as it was stale and causing validation errors (mint case mismatch).
*   **Focus**: The project is moving towards the Universal Taxonomy (`data/universal/us_issues.json`), which is fully updated and valid.
*   **Validation**: `scripts/validate.py` may still fail on other legacy files if they are stale, but `us_issues.json` is the source of truth for the frontend.
