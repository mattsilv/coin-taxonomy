# Universal Currency Taxonomy Browser

A client-side web application for browsing and searching currency data from the Universal Currency Taxonomy project.

## Features

- **Country Selection**: Choose from available countries to view their currency data
- **Real-time Search**: Search across issue IDs, series, years, mints, and more
- **Column Sorting**: Click table headers to sort by any field
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Detailed Views**: Click "View" to see full specifications and mintage data
- **Pagination**: Navigate through large datasets efficiently

## Technology Stack

- **HTML5**: Semantic markup with accessibility features
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Vanilla JavaScript**: Client-side filtering and data manipulation
- **GitHub Pages**: Static hosting directly from the repository

## Data Sources

The browser consumes JSON files from the `data/` directory:

- `data/universal/taxonomy_summary.json` - Metadata and available countries
- `data/universal/us_issues.json` - US currency issues
- Additional country files as they become available

## Setup for GitHub Pages

1. **Enable GitHub Pages**:
   - Go to repository Settings > Pages
   - Set Source to "Deploy from a branch"
   - Select branch: `main` or `feature/universal-taxonomy-v1.1`
   - Set folder: `/docs`

2. **Access the Browser**:
   - URL will be: `https://mattsilv.github.io/coin-taxonomy/`
   - Or your custom domain if configured

## File Structure

```
docs/
├── index.html      # Main application page
├── app.js          # JavaScript application logic
└── README.md       # This documentation
```

## Development

The application is fully client-side, so you can:

1. **Local Development**:
   ```bash
   # Serve the docs folder locally
   cd docs
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

2. **Modify Data**:
   - Update JSON files in `data/` directory
   - Browser automatically picks up changes
   - No build process required

3. **Customize Styling**:
   - Tailwind CSS classes in `index.html`
   - Custom colors defined in Tailwind config
   - Fully responsive design

## Features in Detail

### Search Functionality
- Searches across: issue ID, series, denomination, mint, rarity, year, notes
- Case-insensitive with 300ms debounce
- Real-time results as you type

### Sorting Options
- Default: Year (descending)
- Available: Year, Series, Denomination, Mint, Rarity
- Click table headers for custom sorting
- Visual indicators for sort direction

### Pagination
- 25 items per page (configurable)
- Desktop: Full pagination with page numbers
- Mobile: Previous/Next buttons
- Shows current page stats

### Detail Modal
- Complete specifications
- Mintage information
- Design details (when available)
- Easy keyboard/click dismissal

## Extensibility

Adding new countries:

1. **Add JSON file**: `data/universal/{country}_issues.json`
2. **Update summary**: Add country to taxonomy summary
3. **No code changes needed**: Browser auto-detects available countries

## Performance

- **Client-side only**: No server dependencies
- **Fast filtering**: Optimized JavaScript for large datasets
- **Lazy loading**: Only loads selected country data
- **Mobile optimized**: Responsive tables and pagination

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Android Chrome)

## Contributing

1. Test locally before submitting PRs
2. Ensure responsive design on mobile
3. Validate JSON data integrity
4. Follow existing code patterns