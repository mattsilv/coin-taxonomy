/**
 * Universal Currency Taxonomy Browser
 * Client-side filtering and search for currency data
 */

class CurrencyBrowser {
    constructor() {
        this.data = [];
        this.filteredData = [];
        this.currentPage = 1;
        this.itemsPerPage = 25;
        this.currentSort = { field: 'issue_year', direction: 'asc' };
        this.availableMints = new Set();
        this.availableSeries = new Set();
        
        this.init();
    }

    async init() {
        this.bindEvents();
        await this.loadCountries();
    }

    bindEvents() {
        // Country selection
        document.getElementById('country-select').addEventListener('change', (e) => {
            this.loadCountryData(e.target.value);
        });

        // Search input
        document.getElementById('search-input').addEventListener('input', (e) => {
            this.debounce(() => this.filterData(), 300)();
        });

        // Year range filters
        document.getElementById('year-from').addEventListener('input', (e) => {
            this.debounce(() => this.filterData(), 300)();
        });
        document.getElementById('year-to').addEventListener('input', (e) => {
            this.debounce(() => this.filterData(), 300)();
        });

        // Collector filters
        document.getElementById('mint-filter').addEventListener('change', () => this.filterData());
        document.getElementById('series-filter').addEventListener('change', () => this.filterData());
        document.getElementById('has-varieties').addEventListener('change', () => this.filterData());

        // Clear filters
        document.getElementById('clear-filters').addEventListener('click', () => this.clearAllFilters());

        // CSV Download
        document.getElementById('download-csv').addEventListener('click', () => this.downloadCSV());

        // Sort selection
        document.getElementById('sort-select').addEventListener('change', (e) => {
            this.currentSort.field = e.target.value;
            this.sortAndRender();
        });

        // Table header sorting
        document.querySelectorAll('th[data-sort]').forEach(th => {
            th.addEventListener('click', () => {
                const field = th.dataset.sort;
                if (this.currentSort.field === field) {
                    this.currentSort.direction = this.currentSort.direction === 'asc' ? 'desc' : 'asc';
                } else {
                    this.currentSort.field = field;
                    this.currentSort.direction = 'asc';
                }
                this.sortAndRender();
            });
        });

        // Pagination
        document.getElementById('prev-mobile').addEventListener('click', () => this.prevPage());
        document.getElementById('next-mobile').addEventListener('click', () => this.nextPage());
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async loadCountries() {
        try {
            // For now, we know we have US data
            // This can be expanded when more countries are added
            const countries = [
                { code: 'US', name: 'United States', file: 'data/universal/us_issues.json' }
            ];

            this.populateCountryDropdown(countries);
            
            // Auto-load US data by default
            await this.loadCountryData('data/universal/us_issues.json');
            document.getElementById('country-select').value = 'data/universal/us_issues.json';
            
            // Try to load summary for metadata
            try {
                const response = await fetch('data/universal/taxonomy_summary.json');
                const summary = await response.json();
                
                if (summary.generated_at) {
                    const date = new Date(summary.generated_at);
                    document.getElementById('last-updated').textContent = date.toLocaleDateString();
                }
            } catch (summaryError) {
                console.warn('Could not load summary metadata:', summaryError);
            }
        } catch (error) {
            console.error('Error loading countries:', error);
            this.showError('Failed to load country data');
        }
    }

    populateCountryDropdown(countries) {
        const select = document.getElementById('country-select');
        select.innerHTML = '<option value="">Select a country...</option>';
        
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country.file;
            option.textContent = country.name;
            option.dataset.code = country.code;
            select.appendChild(option);
        });
    }

    async loadCountryData(dataFile) {
        if (!dataFile) {
            this.clearResults();
            return;
        }

        this.showLoading();
        
        try {
            const response = await fetch(dataFile);
            const data = await response.json();
            
            this.data = data.issues || [];
            this.populateFilterDropdowns();
            this.filterData();
            
            // Enable CSV download
            document.getElementById('download-csv').disabled = false;
        } catch (error) {
            console.error('Error loading country data:', error);
            this.showError('Failed to load currency data');
        }
    }

    populateFilterDropdowns() {
        // Populate mint filter
        this.availableMints.clear();
        this.availableSeries.clear();
        
        this.data.forEach(item => {
            if (item.mint_id) this.availableMints.add(item.mint_id);
            if (item.series_id) this.availableSeries.add(item.series_id);
        });
        
        const mintFilter = document.getElementById('mint-filter');
        mintFilter.innerHTML = '<option value="">All Mints</option>';
        [...this.availableMints].sort().forEach(mint => {
            const option = document.createElement('option');
            option.value = mint;
            option.textContent = mint;
            mintFilter.appendChild(option);
        });
        
        const seriesFilter = document.getElementById('series-filter');
        seriesFilter.innerHTML = '<option value="">All Series</option>';
        [...this.availableSeries].sort().forEach(series => {
            const option = document.createElement('option');
            option.value = series;
            option.textContent = this.formatSeriesName(series);
            seriesFilter.appendChild(option);
        });
    }

    formatSeriesName(seriesId) {
        return seriesId.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    filterData() {
        const searchTerm = document.getElementById('search-input').value.toLowerCase().trim();
        const yearFrom = parseInt(document.getElementById('year-from').value) || 0;
        const yearTo = parseInt(document.getElementById('year-to').value) || 9999;
        const mintFilter = document.getElementById('mint-filter').value;
        const seriesFilter = document.getElementById('series-filter').value;
        const hasVarietiesOnly = document.getElementById('has-varieties').checked;
        
        this.filteredData = this.data.filter(item => {
            // Text search
            const unitName = item.denomination?.unit_name || item.unit_name || '';
            const varietiesText = Array.isArray(item.varieties) ? item.varieties.join(' ') : (item.varieties || '');
            const matchesSearch = !searchTerm || (
                (item.issue_id || '').toLowerCase().includes(searchTerm) ||
                (item.series_id || '').toLowerCase().includes(searchTerm) ||
                unitName.toLowerCase().includes(searchTerm) ||
                (item.mint_id || '').toLowerCase().includes(searchTerm) ||
                (item.rarity || '').toLowerCase().includes(searchTerm) ||
                (item.issue_year || '').toString().includes(searchTerm) ||
                (item.notes || '').toLowerCase().includes(searchTerm) ||
                varietiesText.toLowerCase().includes(searchTerm)
            );
            
            // Year range
            const year = parseInt(item.issue_year) || 0;
            const matchesYear = year >= yearFrom && year <= yearTo;
            
            
            // Mint filter
            const matchesMint = !mintFilter || item.mint_id === mintFilter;
            
            // Series filter
            const matchesSeries = !seriesFilter || item.series_id === seriesFilter;
            
            // Varieties filter
            const varieties = Array.isArray(item.varieties) ? item.varieties : [];
            const hasVarieties = varieties.length > 0;
            const matchesVarieties = !hasVarietiesOnly || hasVarieties;
            
            return matchesSearch && matchesYear && matchesMint && matchesSeries && matchesVarieties;
        });

        this.currentPage = 1;
        this.sortAndRender();
    }

    clearAllFilters() {
        document.getElementById('search-input').value = '';
        document.getElementById('year-from').value = '';
        document.getElementById('year-to').value = '';
        document.getElementById('mint-filter').value = '';
        document.getElementById('series-filter').value = '';
        document.getElementById('has-varieties').checked = false;
        this.filterData();
    }

    sortData(data) {
        return data.sort((a, b) => {
            let aVal = a[this.currentSort.field] || '';
            let bVal = b[this.currentSort.field] || '';

            // Handle numeric fields
            if (['issue_year', 'mintage'].includes(this.currentSort.field)) {
                if (this.currentSort.field === 'mintage') {
                    // Extract business strikes from mintage object
                    const aMintage = this.extractMintage(a);
                    const bMintage = this.extractMintage(b);
                    aVal = aMintage;
                    bVal = bMintage;
                } else {
                    aVal = parseFloat(aVal) || 0;
                    bVal = parseFloat(bVal) || 0;
                }
            } else if (this.currentSort.field === 'unit_name') {
                // Sort by denomination face value
                aVal = a.denomination?.face_value || 0;
                bVal = b.denomination?.face_value || 0;
            } else {
                aVal = aVal.toString().toLowerCase();
                bVal = bVal.toString().toLowerCase();
            }

            if (aVal < bVal) return this.currentSort.direction === 'asc' ? -1 : 1;
            if (aVal > bVal) return this.currentSort.direction === 'asc' ? 1 : -1;
            return 0;
        });
    }

    sortAndRender() {
        this.filteredData = this.sortData(this.filteredData);
        this.updateSortIndicators();
        this.renderResults();
    }

    updateSortIndicators() {
        // Update all sortable column headers with indicators
        document.querySelectorAll('th[data-sort]').forEach(th => {
            const field = th.dataset.sort;
            const isActive = this.currentSort.field === field;
            const direction = this.currentSort.direction;
            
            // Remove existing indicators
            const existingIndicator = th.querySelector('.sort-indicator');
            if (existingIndicator) {
                existingIndicator.remove();
            }
            
            // Add sort indicator
            const indicator = document.createElement('span');
            indicator.className = 'sort-indicator ml-2 inline-flex flex-col';
            
            if (isActive) {
                // Show active sort direction
                indicator.innerHTML = `
                    <svg class="w-3 h-3 ${direction === 'asc' ? 'text-blue-600' : 'text-gray-400'}" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg class="w-3 h-3 ${direction === 'desc' ? 'text-blue-600' : 'text-gray-400'} -mt-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                `;
            } else {
                // Show neutral sort indicators
                indicator.innerHTML = `
                    <svg class="w-3 h-3 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg class="w-3 h-3 text-gray-300 -mt-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                `;
            }
            
            th.appendChild(indicator);
        });
    }

    renderResults() {
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const pageData = this.filteredData.slice(startIndex, endIndex);

        if (this.filteredData.length === 0) {
            this.showNoResults();
            return;
        }

        this.hideStates();
        document.getElementById('results-container').classList.remove('hidden');

        // Update results count
        document.getElementById('results-count').textContent = this.filteredData.length;

        // Render table rows
        const tbody = document.getElementById('results-tbody');
        tbody.innerHTML = pageData.map(item => this.renderTableRow(item)).join('');

        // Update pagination
        this.updatePagination();
    }

    extractMintage(item) {
        try {
            const mintage = item.mintage || {};
            return mintage.business_strikes || 0;
        } catch {
            return 0;
        }
    }

    extractVarietiesCount(item) {
        try {
            const varieties = item.varieties ? JSON.parse(item.varieties) : [];
            return varieties.length || 0;
        } catch {
            return 0;
        }
    }

    formatMintage(item) {
        try {
            const mintage = item.mintage || {};
            const business = mintage.business_strikes;
            const proof = mintage.proof_strikes;
            
            let result = '';
            if (business && business > 0) {
                // Format in millions with m suffix
                if (business >= 1000000) {
                    const millions = (business / 1000000).toFixed(1);
                    result += `${millions}m`;
                } else if (business >= 1000) {
                    const thousands = (business / 1000).toFixed(0);
                    result += `${thousands}k`;
                } else {
                    result += business.toLocaleString();
                }
            }
            if (proof && proof > 0) {
                let proofFormatted = '';
                if (proof >= 1000000) {
                    const millions = (proof / 1000000).toFixed(1);
                    proofFormatted = `${millions}m proof`;
                } else if (proof >= 1000) {
                    const thousands = (proof / 1000).toFixed(0);
                    proofFormatted = `${thousands}k proof`;
                } else {
                    proofFormatted = `${proof.toLocaleString()} proof`;
                }
                result += (result ? '<br><span class="text-xs text-gray-500">' + proofFormatted + '</span>' : proofFormatted);
            }
            return result || '-';
        } catch {
            return '-';
        }
    }

    formatDenomination(item) {
        try {
            // Handle nested denomination structure
            const denom = item.denomination || {};
            const unitName = denom.unit_name || item.unit_name;
            const faceValue = denom.face_value || item.face_value;
            
            if (!faceValue || faceValue <= 0) return unitName || '-';
            
            // Format denomination with coin-like appearance
            let valueText = '';
            let coinStyle = '';
            
            if (faceValue >= 1) {
                valueText = `$${faceValue}`;
                // Dollar coins - golden color
                coinStyle = 'bg-yellow-600 text-white';
            } else {
                const cents = Math.round(faceValue * 100);
                valueText = `${cents}¢`;
                
                // Style based on coin type
                if (cents === 1) {
                    // Copper penny
                    coinStyle = 'bg-orange-700 text-white';
                } else if (cents === 5) {
                    // Nickel - grayish
                    coinStyle = 'bg-gray-500 text-white';
                } else {
                    // Dimes, quarters - silver
                    coinStyle = 'bg-gray-400 text-white';
                }
            }
            
            return `
                <div class="flex justify-center">
                    <div class="flex items-center justify-center w-8 h-8 rounded-full ${coinStyle} text-xs font-bold shadow-sm">
                        ${valueText}
                    </div>
                </div>
            `;
        } catch {
            return '-';
        }
    }

    formatVarieties(item) {
        try {
            const varieties = item.varieties || [];
            if (!varieties || varieties.length === 0) {
                return '<span class="text-gray-400 text-xs">None</span>';
            }
            
            return `<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                ${varieties.length} ${varieties.length === 1 ? 'variety' : 'varieties'}
            </span>`;
        } catch {
            return '<span class="text-gray-400 text-xs">Error</span>';
        }
    }

    renderTableRow(item) {
        const rarityBadge = this.getRarityBadge(item.rarity);
        const mintageDisplay = this.formatMintage(item);
        const varietiesDisplay = this.formatVarieties(item);
        
        return `
            <tr class="hover:bg-gray-50 transition-colors duration-150">
                <td class="px-3 py-4 whitespace-nowrap text-xs font-medium text-gray-900">
                    <div class="flex items-center space-x-2">
                        <span>${item.issue_id || '-'}</span>
                        <button onclick="currencyBrowser.copyToClipboard('${item.issue_id}')" 
                                class="inline-flex items-center p-1 text-gray-400 hover:text-gray-600 rounded transition-colors duration-150" 
                                title="Copy ID to clipboard">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                            </svg>
                        </button>
                    </div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                    ${item.issue_year || '-'}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="max-w-40 truncate font-medium" title="${this.formatSeriesName(item.series_id || '')}">
                        ${this.formatSeriesName(item.series_id || '') || '-'}
                    </div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
                    ${this.formatDenomination(item)}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
                    <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800">${item.mint_id || '-'}</span>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                    ${mintageDisplay}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-center">
                    <button onclick="currencyBrowser.showDetails('${item.issue_id}')" 
                            class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-150">
                        View
                    </button>
                </td>
            </tr>
        `;
    }

    getRarityBadge(rarity) {
        if (!rarity) return '<span class="text-gray-400">-</span>';
        
        const badges = {
            'common': 'bg-green-100 text-green-800',
            'uncommon': 'bg-yellow-100 text-yellow-800', 
            'scarce': 'bg-orange-100 text-orange-800',
            'rare': 'bg-red-100 text-red-800',
            'key': 'bg-purple-100 text-purple-800'
        };
        
        const colorClass = badges[rarity.toLowerCase()] || 'bg-gray-100 text-gray-800';
        
        return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colorClass}">
            ${rarity}
        </span>`;
    }

    updatePagination() {
        const totalPages = Math.ceil(this.filteredData.length / this.itemsPerPage);
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = Math.min(startIndex + this.itemsPerPage, this.filteredData.length);

        // Update pagination info
        document.getElementById('page-start').textContent = startIndex + 1;
        document.getElementById('page-end').textContent = endIndex;
        document.getElementById('total-results').textContent = this.filteredData.length;

        // Update mobile pagination buttons
        document.getElementById('prev-mobile').disabled = this.currentPage === 1;
        document.getElementById('next-mobile').disabled = this.currentPage === totalPages;

        // Generate page numbers (simplified for now)
        const pageNumbers = document.getElementById('page-numbers');
        pageNumbers.innerHTML = '';

        if (totalPages <= 1) return;

        // Previous button
        const prevBtn = document.createElement('button');
        prevBtn.className = `relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 ${this.currentPage === 1 ? 'cursor-not-allowed opacity-50' : ''}`;
        prevBtn.innerHTML = '←';
        prevBtn.disabled = this.currentPage === 1;
        prevBtn.onclick = () => this.prevPage();
        pageNumbers.appendChild(prevBtn);

        // Page numbers (show up to 5 pages around current page)
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.className = `relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                i === this.currentPage 
                    ? 'z-10 bg-blue-50 border-blue-500 text-blue-600' 
                    : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
            }`;
            pageBtn.textContent = i;
            pageBtn.onclick = () => this.goToPage(i);
            pageNumbers.appendChild(pageBtn);
        }

        // Next button
        const nextBtn = document.createElement('button');
        nextBtn.className = `relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 ${this.currentPage === totalPages ? 'cursor-not-allowed opacity-50' : ''}`;
        nextBtn.innerHTML = '→';
        nextBtn.disabled = this.currentPage === totalPages;
        nextBtn.onclick = () => this.nextPage();
        pageNumbers.appendChild(nextBtn);
    }

    prevPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.renderResults();
        }
    }

    nextPage() {
        const totalPages = Math.ceil(this.filteredData.length / this.itemsPerPage);
        if (this.currentPage < totalPages) {
            this.currentPage++;
            this.renderResults();
        }
    }

    goToPage(page) {
        this.currentPage = page;
        this.renderResults();
    }

    showDetails(issueId) {
        const item = this.data.find(d => d.issue_id === issueId);
        if (!item) return;

        const specifications = item.specifications || {};
        const mintage = item.mintage || {};
        const denomination = item.denomination || {};

        const modalContent = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                    <h4 class="font-medium text-gray-900 mb-2">Basic Information</h4>
                    <dl class="space-y-1">
                        <div><dt class="inline font-medium">Issue ID:</dt> <dd class="inline">${item.issue_id || '-'}</dd></div>
                        <div><dt class="inline font-medium">Year:</dt> <dd class="inline">${item.issue_year || '-'}</dd></div>
                        <div><dt class="inline font-medium">Series:</dt> <dd class="inline">${this.formatSeriesName(item.series_id || '')}</dd></div>
                        <div><dt class="inline font-medium">Denomination:</dt> <dd class="inline">${denomination.unit_name || '-'}</dd></div>
                        <div><dt class="inline font-medium">Face Value:</dt> <dd class="inline">$${denomination.face_value || '-'}</dd></div>
                        <div><dt class="inline font-medium">Mint:</dt> <dd class="inline">${item.mint_id || '-'}</dd></div>
                    </dl>
                </div>
                
                <div>
                    <h4 class="font-medium text-gray-900 mb-2">Specifications & Production</h4>
                    <dl class="space-y-1">
                        <div><dt class="inline font-medium">Weight:</dt> <dd class="inline">${specifications.weight_grams || '-'} grams</dd></div>
                        <div><dt class="inline font-medium">Diameter:</dt> <dd class="inline">${specifications.diameter_mm || '-'} mm</dd></div>
                        <div><dt class="inline font-medium">Edge:</dt> <dd class="inline">${specifications.edge || '-'}</dd></div>
                        <div><dt class="inline font-medium">Business Strikes:</dt> <dd class="inline">${mintage.business_strikes?.toLocaleString() || '-'}</dd></div>
                        <div><dt class="inline font-medium">Proof Strikes:</dt> <dd class="inline">${mintage.proof_strikes?.toLocaleString() || '-'}</dd></div>
                    </dl>
                </div>
            </div>
            
            ${item.source_citation ? `
                <div class="mt-4">
                    <h4 class="font-medium text-gray-900 mb-2">Source</h4>
                    <p class="text-sm text-gray-600">${item.source_citation}</p>
                </div>
            ` : ''}
        `;

        // Show modal
        document.getElementById('details-modal').classList.remove('hidden');
        document.getElementById('modal-content').innerHTML = modalContent;
    }

    closeDetails() {
        document.getElementById('details-modal').classList.add('hidden');
    }

    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showCopyNotification();
            }).catch(() => {
                this.fallbackCopyToClipboard(text);
            });
        } else {
            this.fallbackCopyToClipboard(text);
        }
    }

    fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            this.showCopyNotification();
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
        textArea.remove();
    }

    showCopyNotification() {
        // Simple notification - could be enhanced
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-md shadow-lg z-50 transition-opacity duration-300';
        notification.textContent = 'ID copied to clipboard!';
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    downloadCSV() {
        if (this.filteredData.length === 0) {
            alert('No data to download. Please select a country and apply filters.');
            return;
        }

        // Define CSV headers - collector focused
        const headers = [
            'Issue ID',
            'Year', 
            'Series',
            'Denomination',
            'Face Value',
            'Mint Mark',
            'Business Strikes',
            'Proof Strikes',
            'Rarity',
            'Varieties Count',
            'Weight (g)',
            'Diameter (mm)',
            'Notes'
        ];

        // Convert data to CSV format
        const csvData = this.filteredData.map(item => {
            const mintage = item.mintage || {};
            const specifications = item.specifications || {};
            const varieties = item.varieties || [];
            const denomination = item.denomination || {};
            
            return [
                item.issue_id || '',
                item.issue_year || '',
                this.formatSeriesName(item.series_id || ''),
                denomination.unit_name || '',
                denomination.face_value || '',
                item.mint_id || '',
                mintage.business_strikes || '',
                mintage.proof_strikes || '',
                item.rarity || '',
                varieties.length || 0,
                specifications.weight_grams || '',
                specifications.diameter_mm || '',
                (item.source_citation || '').replace(/"/g, '""')  // Escape quotes
            ];
        });

        // Create CSV content
        const csvContent = [
            headers.join(','),
            ...csvData.map(row => row.map(field => 
                typeof field === 'string' && field.includes(',') 
                    ? `"${field}"` 
                    : field
            ).join(','))
        ].join('\n');

        // Create and trigger download
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        const timestamp = new Date().toISOString().split('T')[0];
        const countryCode = document.getElementById('country-select').selectedOptions[0]?.dataset.code || 'DATA';
        const filename = `currency-taxonomy-${countryCode.toLowerCase()}-${timestamp}.csv`;
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }

    showLoading() {
        this.hideStates();
        document.getElementById('loading').classList.remove('hidden');
    }

    showNoResults() {
        this.hideStates();
        document.getElementById('no-results').classList.remove('hidden');
    }

    clearResults() {
        this.hideStates();
        this.data = [];
        this.filteredData = [];
        document.getElementById('results-count').textContent = '0';
        document.getElementById('download-csv').disabled = true;
    }

    hideStates() {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('no-results').classList.add('hidden');
        document.getElementById('results-container').classList.add('hidden');
    }

    showError(message) {
        this.hideStates();
        // Could add a proper error state, for now just log
        console.error(message);
        alert(message);
    }
}

// Initialize the application
const currencyBrowser = new CurrencyBrowser();