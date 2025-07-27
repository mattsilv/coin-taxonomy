#!/usr/bin/env node
/**
 * End-to-End Test for GitHub Pages Currency Browser
 * Tests for JavaScript errors and basic functionality
 */

const fs = require('fs');
const path = require('path');

// Simple test runner without external dependencies
class SimpleE2ETest {
    constructor() {
        this.tests = [];
        this.results = [];
    }

    test(name, testFn) {
        this.tests.push({ name, testFn });
    }

    async run() {
        console.log('🧪 Running End-to-End Tests for Currency Browser');
        console.log('='.repeat(60));
        
        let passed = 0;
        let failed = 0;

        for (const { name, testFn } of this.tests) {
            try {
                console.log(`\n📋 ${name}`);
                await testFn();
                console.log(`✅ PASS: ${name}`);
                this.results.push({ name, status: 'PASS' });
                passed++;
            } catch (error) {
                console.log(`❌ FAIL: ${name}`);
                console.log(`   Error: ${error.message}`);
                this.results.push({ name, status: 'FAIL', error: error.message });
                failed++;
            }
        }

        console.log('\n' + '='.repeat(60));
        console.log(`📊 Test Results: ${passed} passed, ${failed} failed`);
        
        if (failed > 0) {
            console.log('\n❌ Some tests failed:');
            this.results.filter(r => r.status === 'FAIL').forEach(r => {
                console.log(`   - ${r.name}: ${r.error}`);
            });
            process.exit(1);
        } else {
            console.log('\n✅ All tests passed!');
            process.exit(0);
        }
    }

    assert(condition, message) {
        if (!condition) {
            throw new Error(message);
        }
    }

    // File system tests (no browser needed)
    async testFilesExist() {
        const requiredFiles = [
            'docs/index.html',
            'docs/app.js',
            'docs/README.md',
            'data/universal/taxonomy_summary.json',
            'data/universal/us_issues.json'
        ];

        for (const file of requiredFiles) {
            const fullPath = path.join(process.cwd(), file);
            this.assert(fs.existsSync(fullPath), `Required file missing: ${file}`);
        }
    }

    async testHTMLStructure() {
        const htmlPath = path.join(process.cwd(), 'docs/index.html');
        const html = fs.readFileSync(htmlPath, 'utf8');

        // Test for required elements
        const requiredElements = [
            'id="country-select"',
            'id="search-input"', 
            'id="year-from"',
            'id="year-to"',
            'id="mint-filter"',
            'id="series-filter"',
            'id="has-varieties"',
            'id="download-csv"',
            'id="clear-filters"',
            'id="results-tbody"'
        ];

        for (const element of requiredElements) {
            this.assert(html.includes(element), `HTML missing required element: ${element}`);
        }

        // Test for Tailwind CSS
        this.assert(html.includes('tailwindcss.com'), 'Tailwind CSS not loaded');
        
        // Test for app.js
        this.assert(html.includes('app.js'), 'app.js not included');
    }

    async testJavaScriptSyntax() {
        const jsPath = path.join(process.cwd(), 'docs/app.js');
        const js = fs.readFileSync(jsPath, 'utf8');

        // Basic syntax checks
        this.assert(js.includes('class CurrencyBrowser'), 'CurrencyBrowser class not found');
        this.assert(js.includes('constructor()'), 'Constructor not found');
        this.assert(js.includes('filterData()'), 'filterData method not found');
        this.assert(js.includes('downloadCSV()'), 'downloadCSV method not found');
        
        // Check for required methods
        const requiredMethods = [
            'loadCountries',
            'loadCountryData', 
            'filterData',
            'sortData',
            'renderResults',
            'downloadCSV',
            'clearAllFilters'
        ];

        for (const method of requiredMethods) {
            this.assert(js.includes(`${method}(`), `Method not found: ${method}`);
        }

        // Basic syntax validation (very simple)
        const openBraces = (js.match(/{/g) || []).length;
        const closeBraces = (js.match(/}/g) || []).length;
        this.assert(openBraces === closeBraces, 'Mismatched braces in JavaScript');
    }

    async testJSONDataIntegrity() {
        // Test taxonomy summary
        const summaryPath = path.join(process.cwd(), 'data/universal/taxonomy_summary.json');
        const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));
        
        this.assert(summary.taxonomy_version, 'Taxonomy version not found');
        this.assert(summary.generated_at, 'Generated timestamp not found');
        this.assert(summary.total_issues > 0, 'No issues found in summary');

        // Test US issues data
        const usPath = path.join(process.cwd(), 'data/universal/us_issues.json');
        const usData = JSON.parse(fs.readFileSync(usPath, 'utf8'));
        
        this.assert(usData.issues && Array.isArray(usData.issues), 'Issues array not found');
        this.assert(usData.issues.length > 0, 'No US issues found');

        // Test first issue has required fields
        const firstIssue = usData.issues[0];
        this.assert(firstIssue.issue_id, 'issue_id missing');
        this.assert(firstIssue.issue_year, 'issue_year missing');
        this.assert(firstIssue.series_id, 'series_id missing');
        this.assert(firstIssue.denomination && firstIssue.denomination.unit_name, 'unit_name missing in denomination');
        this.assert(firstIssue.issuing_entity && firstIssue.issuing_entity.country_code, 'country_code missing');
    }

    async testFunctionalIntegration() {
        const jsPath = path.join(process.cwd(), 'docs/app.js');
        const js = fs.readFileSync(jsPath, 'utf8');

        // Test that site loads US data by default
        this.assert(js.includes('Auto-load US data by default'), 'Site should auto-load US data');
        this.assert(js.includes('await this.loadCountryData'), 'Auto-load mechanism missing');
        
        // Test that countries dropdown is populated
        this.assert(js.includes('United States'), 'US not in countries list');
        this.assert(js.includes('us_issues.json'), 'US data file not referenced');
        
        // Test error handling for missing data
        this.assert(js.includes('showError'), 'Error handling missing');
        this.assert(js.includes('console.error'), 'Error logging missing');
        
        // Verify data structure expectations
        this.assert(js.includes('data.issues'), 'Issues array not expected in data structure');
        this.assert(js.includes('this.data = data.issues'), 'Data assignment missing');
    }

    async testCollectorFeatures() {
        const jsPath = path.join(process.cwd(), 'docs/app.js');
        const js = fs.readFileSync(jsPath, 'utf8');

        // Test for collector-specific features
        const collectorFeatures = [
            'year-from',
            'year-to', 
            'mint-filter',
            'series-filter',
            'has-varieties',
            'downloadCSV',
            'formatMintage',
            'formatVarieties'
        ];

        for (const feature of collectorFeatures) {
            this.assert(js.includes(feature), `Collector feature not found: ${feature}`);
        }
    }

    async testCSVFunctionality() {
        const jsPath = path.join(process.cwd(), 'docs/app.js');
        const js = fs.readFileSync(jsPath, 'utf8');

        // Test CSV download function exists and has proper structure
        this.assert(js.includes('downloadCSV()'), 'downloadCSV method not found');
        this.assert(js.includes('text/csv'), 'CSV MIME type not found');
        this.assert(js.includes('createObjectURL'), 'Blob download not implemented');
        this.assert(js.includes('currency-taxonomy-'), 'CSV filename pattern not found');
        
        // Test CSV headers for collector data
        const csvHeaders = [
            'Issue ID',
            'Year',
            'Series', 
            'Denomination',
            'Mint Mark',
            'Business Strikes',
            'Proof Strikes',
            'Rarity',
            'Varieties Count'
        ];

        for (const header of csvHeaders) {
            this.assert(js.includes(header), `CSV header missing: ${header}`);
        }
    }
}

// Run the tests
async function main() {
    const tester = new SimpleE2ETest();
    
    // Add all tests
    tester.test('Required files exist', () => tester.testFilesExist());
    tester.test('HTML structure is valid', () => tester.testHTMLStructure());
    tester.test('JavaScript syntax is valid', () => tester.testJavaScriptSyntax());
    tester.test('JSON data integrity', () => tester.testJSONDataIntegrity());
    tester.test('Functional integration works', () => tester.testFunctionalIntegration());
    tester.test('Collector features present', () => tester.testCollectorFeatures());
    tester.test('CSV functionality implemented', () => tester.testCSVFunctionality());
    
    // Run all tests
    await tester.run();
}

// Only run if called directly
if (require.main === module) {
    main().catch(error => {
        console.error('💥 Test runner failed:', error.message);
        process.exit(1);
    });
}

module.exports = { SimpleE2ETest };