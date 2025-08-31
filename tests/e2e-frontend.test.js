#!/usr/bin/env node
/**
 * E2E Test for Frontend Canada Support
 * Ensures the frontend properly supports multiple countries including Canada
 */

const fs = require('fs');
const path = require('path');

let testsPassed = 0;
let testsFailed = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
        testsPassed++;
    } catch (error) {
        console.error(`❌ ${name}: ${error.message}`);
        testsFailed++;
    }
}

function assertEqual(actual, expected, message) {
    if (actual !== expected) {
        throw new Error(`${message}: expected ${expected}, got ${actual}`);
    }
}

function assertIncludes(str, substr, message) {
    if (!str.includes(substr)) {
        throw new Error(`${message}: string does not include "${substr}"`);
    }
}

function assertExists(filePath, message) {
    if (!fs.existsSync(filePath)) {
        throw new Error(`${message}: file does not exist at ${filePath}`);
    }
}

console.log('🧪 Running E2E Frontend Tests for Canada Support\n');

// Test 1: Check if Canada data files exist
test('Canada JSON files exist', () => {
    assertExists('data/ca/ca_coins_complete.json', 'Complete Canada coins file');
    assertExists('data/universal/ca_issues.json', 'Universal Canada issues');
    assertExists('docs/data/universal/ca_issues.json', 'Frontend Canada issues');
});

// Test 2: Validate Canada data structure
test('Canada data has correct structure', () => {
    const caData = JSON.parse(fs.readFileSync('data/universal/ca_issues.json', 'utf8'));
    
    assertEqual(caData.country, 'CA', 'Country code');
    assertEqual(caData.countryName, 'Canada', 'Country name');
    
    if (!caData.issues || caData.issues.length === 0) {
        throw new Error('No issues found in Canada data');
    }
    
    // Check first issue has required fields
    const firstIssue = caData.issues[0];
    const requiredFields = ['issueId', 'country', 'denomination', 'year', 'mint', 'seriesName'];
    
    for (const field of requiredFields) {
        if (!(field in firstIssue)) {
            throw new Error(`Missing required field: ${field}`);
        }
    }
});

// Test 3: Check app.js includes Canada
test('Frontend app.js includes Canada', () => {
    const appJs = fs.readFileSync('docs/app.js', 'utf8');
    assertIncludes(appJs, "code: 'CA'", 'Canada country code');
    assertIncludes(appJs, "name: 'Canada'", 'Canada country name');
    assertIncludes(appJs, 'ca_issues.json', 'Canada issues file');
});

// Test 4: Check taxonomy summary includes Canada
test('Taxonomy summary includes Canada', () => {
    const summary = JSON.parse(fs.readFileSync('data/universal/taxonomy_summary.json', 'utf8'));
    
    if (!summary.issue_files) {
        throw new Error('No issue_files in taxonomy summary');
    }
    
    if (!summary.issue_files.includes('ca_issues.json')) {
        throw new Error('Canada not in issue_files');
    }
    
    assertEqual(summary.countries, 2, 'Country count should be 2 (US + CA)');
});

// Test 5: Validate specific Canadian coins exist
test('Key Canadian coins exist', () => {
    const caData = JSON.parse(fs.readFileSync('data/universal/ca_issues.json', 'utf8'));
    
    const keyCoins = [
        'CA-CENT-1858-RM',  // First Canadian cent
        'CA-DOLR-1987-P',   // Loonie
        'CA-TWOD-1996-P',   // Toonie
        'CA-GMPL-1979-P',   // Gold Maple Leaf
    ];
    
    for (const coinId of keyCoins) {
        const found = caData.issues.some(coin => coin.issueId === coinId);
        if (!found) {
            throw new Error(`Key coin not found: ${coinId}`);
        }
    }
});

// Test 6: Check HTML has country selector
test('HTML has country selector', () => {
    const html = fs.readFileSync('docs/index.html', 'utf8');
    assertIncludes(html, 'country-select', 'Country selector element');
    assertIncludes(html, 'Select a country', 'Country selector label');
});

// Test 7: Validate Canada reference files
test('Canada reference files are valid', () => {
    const mints = JSON.parse(fs.readFileSync('data/ca/references/mints.json', 'utf8'));
    const compositions = JSON.parse(fs.readFileSync('data/ca/references/compositions.json', 'utf8'));
    
    if (!mints.mints || mints.mints.length === 0) {
        throw new Error('No mints defined for Canada');
    }
    
    if (!compositions.compositions || compositions.compositions.length === 0) {
        throw new Error('No compositions defined for Canada');
    }
    
    // Check for key Canadian mints
    const mintMarks = mints.mints.map(m => m.mint_mark);
    const requiredMints = ['P', 'W', 'RM'];
    for (const mint of requiredMints) {
        if (!mintMarks.includes(mint)) {
            throw new Error(`Missing required mint: ${mint}`);
        }
    }
});

// Test 8: Frontend data is accessible via relative paths
test('Frontend can access Canada data', () => {
    // Check that the paths in app.js match actual file locations
    const frontendCAPath = 'docs/data/universal/ca_issues.json';
    const frontendUSPath = 'docs/data/universal/us_issues.json';
    
    assertExists(frontendCAPath, 'Frontend Canada data');
    assertExists(frontendUSPath, 'Frontend US data');
    
    // Verify the data is valid JSON
    JSON.parse(fs.readFileSync(frontendCAPath, 'utf8'));
    JSON.parse(fs.readFileSync(frontendUSPath, 'utf8'));
});

// Print summary
console.log('\n' + '='.repeat(50));
console.log(`Tests Passed: ${testsPassed}`);
console.log(`Tests Failed: ${testsFailed}`);
console.log(`Total Tests: ${testsPassed + testsFailed}`);
console.log('='.repeat(50));

if (testsFailed > 0) {
    console.error('\n❌ E2E tests failed!');
    process.exit(1);
} else {
    console.log('\n✅ All E2E tests passed!');
    process.exit(0);
}