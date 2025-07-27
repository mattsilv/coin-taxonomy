# Local Testing Instructions

## Run GitHub Pages Site Locally

### Option 1: Smart Serve Script (Recommended)
```bash
# Auto-finds available port starting from 8000
uv run python scripts/serve_site.py

# Specific port with auto-fallback
uv run python scripts/serve_site.py --port 3000

# Kill existing processes and use specific port
uv run python scripts/serve_site.py --port 8000 --kill-existing

# Force specific port without auto-fallback
uv run python scripts/serve_site.py --port 8000 --no-auto-port
```

### Option 2: Python HTTP Server
```bash
# Navigate to the docs directory
cd docs

# Start local server on port 8000
python -m http.server 8000

# Open in browser
open http://localhost:8000
```

### Option 2: Node.js HTTP Server
```bash
# Install a simple HTTP server (if you don't have one)
npm install -g http-server

# Navigate to docs and serve
cd docs
http-server -p 8000

# Open in browser
open http://localhost:8000
```

### Option 3: PHP Server (if you have PHP)
```bash
cd docs
php -S localhost:8000
open http://localhost:8000
```

## Test the Complete System

### 1. Run End-to-End Tests
```bash
node scripts/test_github_pages.js
```

### 2. Test Data Pipeline
```bash
# Regenerate database (optional)
uv run python scripts/migrate_to_universal_v1_1.py

# Export fresh JSON files
uv run python scripts/export_db_v1_1.py

# Validate everything
uv run python scripts/validate.py
uv run python scripts/data_integrity_check.py
```

### 3. Test Pre-commit Hook
```bash
# Make a small change and commit to test the full pipeline
echo "# test" >> README.md
git add README.md
git commit -m "Test commit"
git reset HEAD~1  # Undo the commit after testing
```

## What to Test

1. **Site Loading**: Verify no JavaScript errors in browser console
2. **Country Selection**: Select "United States" from dropdown
3. **Search Functionality**: Search for "1909", "lincoln", "key"
4. **Filters**: Test year range (1900-1920), rarity filter, mint filter
5. **Sorting**: Click table headers to sort by different columns
6. **Details Modal**: Click "View" button on any coin
7. **CSV Download**: Click "Download CSV" button after selecting country
8. **Mobile Responsive**: Test on mobile device or browser dev tools

## Expected Results

- **Data loads**: Should see 99 US coin issues
- **Filters work**: Results update in real-time
- **CSV downloads**: File named like `currency-taxonomy-us-2025-07-27.csv`
- **No JS errors**: Clean browser console
- **Responsive**: Works on mobile and desktop

## Troubleshooting

### CORS Issues
If you see CORS errors, make sure you're using an HTTP server (not opening the HTML file directly).

### Missing Data
If no data loads, check that these files exist:
- `../data/universal/taxonomy_summary.json`
- `../data/universal/us_issues.json`

### Test Failures
Run the e2e tests to diagnose issues:
```bash
node scripts/test_github_pages.js
```