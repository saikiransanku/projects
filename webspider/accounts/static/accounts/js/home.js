function googleTranslateElementInit() {
        new google.translate.TranslateElement(
            { pageLanguage: 'en' },
            'google_translate_element'
        );
        waitForTranslatorAndApply(localStorage.getItem(LANG_KEY) || 'en');
    }

    const THEME_KEY = 'auth_theme';
    const LANG_KEY = 'site_language';
    const THEME_OPTIONS = ['light', 'dark', 'system'];
    const body = document.body;
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const hamburgerToggle = document.getElementById('hamburger-toggle');
    const settingsWrap = document.getElementById('settings-wrap');
    const settingsToggle = document.getElementById('settings-toggle');
    const themeMenuToggle = document.getElementById('theme-menu-toggle');
    const themeCurrent = document.getElementById('theme-current');
    const themeOptionButtons = document.querySelectorAll('.theme-option');
    const languageMenuToggle = document.getElementById('language-menu-toggle');
    const languageCurrent = document.getElementById('language-current');
    const languageOptionButtons = document.querySelectorAll('.language-option');
    const systemThemeMedia = window.matchMedia('(prefers-color-scheme: dark)');
    const LANGUAGE_LABELS = {
        en: 'English',
        hi: 'Hindi',
        bn: 'Bengali',
        te: 'Telugu',
        mr: 'Marathi',
        ta: 'Tamil',
        ur: 'Urdu',
        gu: 'Gujarati',
        kn: 'Kannada',
        or: 'Odia',
        ml: 'Malayalam',
        pa: 'Punjabi',
        as: 'Assamese',
        mai: 'Maithili',
        sat: 'Santali',
        ks: 'Kashmiri',
        ne: 'Nepali',
        kok: 'Konkani',
        sd: 'Sindhi',
        doi: 'Dogri',
        mni: 'Manipuri',
    };
    const SEARCH_SUGGESTIONS = [
        'MSP for rabi crops',
        'Natural farming mission in India',
        'Namo Drone Didi scheme',
        'Wheat and mustard sowing guide',
        'Soil health card benefits',
        'Micro irrigation for small farms',
        'Organic farming methods',
        'Crop insurance for farmers',
        'Government subsidies for fertilizers',
        'Paddy cultivation best practices',
        'Millet farming opportunities',
        'Weather advisory for farmers',
        'Farmer producer organizations',
        'Post-harvest storage tips',
        'Season-wise crop planning',
    ];

    function formatThemeName(themeName) {
        if (themeName === 'dark') {
            return 'Dark';
        }
        if (themeName === 'light') {
            return 'Light';
        }
        return 'System Default';
    }

    function resolveTheme(themeName) {
        if (themeName === 'system') {
            return systemThemeMedia.matches ? 'dark' : 'light';
        }
        return themeName === 'dark' ? 'dark' : 'light';
    }

    function closeThemeSubmenu() {
        settingsWrap.classList.remove('theme-open');
        themeMenuToggle.setAttribute('aria-expanded', 'false');
    }

    function closeLanguageSubmenu() {
        settingsWrap.classList.remove('language-open');
        languageMenuToggle.setAttribute('aria-expanded', 'false');
    }

    function closeHamburgerMenu() {
        if (!hamburgerMenu || !hamburgerToggle) {
            return;
        }
        hamburgerMenu.classList.remove('open');
        hamburgerToggle.setAttribute('aria-expanded', 'false');
    }

    function setTheme(themeName, persistChoice) {
        const safeTheme = THEME_OPTIONS.indexOf(themeName) >= 0 ? themeName : 'system';
        const resolvedTheme = resolveTheme(safeTheme);
        body.classList.toggle('theme-dark', resolvedTheme === 'dark');
        themeCurrent.textContent = formatThemeName(safeTheme);
        for (let i = 0; i < themeOptionButtons.length; i++) {
            const button = themeOptionButtons[i];
            button.classList.toggle('active', button.dataset.themeChoice === safeTheme);
        }
        if (persistChoice !== false) {
            localStorage.setItem(THEME_KEY, safeTheme);
        }
    }

    function applyGoogleTranslateCookie(languageCode) {
        const targetCode = LANGUAGE_LABELS[languageCode] ? languageCode : 'en';
        const cookieValue = '/en/' + targetCode;
        document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/';
        document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;domain=' + window.location.hostname;
        document.cookie = 'googtrans=' + cookieValue + ';path=/';
        document.cookie = 'googtrans=' + cookieValue + ';path=/;domain=' + window.location.hostname;
    }

    function dispatchChangeEvent(element) {
        if (typeof Event === 'function') {
            element.dispatchEvent(new Event('change', { bubbles: true }));
            return;
        }
        const legacyEvent = document.createEvent('HTMLEvents');
        legacyEvent.initEvent('change', true, false);
        element.dispatchEvent(legacyEvent);
    }

    function getGoogleLanguageCode(languageCode, combo) {
        if (languageCode === 'mni') {
            for (let i = 0; i < combo.options.length; i++) {
                if (combo.options[i].value === 'mni-Mtei') {
                    return 'mni-Mtei';
                }
            }
        }
        return languageCode;
    }

    function triggerGoogleTranslate(languageCode) {
        const combo = document.querySelector('.goog-te-combo');
        if (!combo) {
            return false;
        }
        const targetCode = getGoogleLanguageCode(languageCode, combo);
        let optionFound = false;
        for (let i = 0; i < combo.options.length; i++) {
            if (combo.options[i].value === targetCode) {
                optionFound = true;
                break;
            }
        }
        if (!optionFound) {
            return false;
        }
        if (combo.value !== targetCode) {
            combo.value = targetCode;
            dispatchChangeEvent(combo);
        }
        return true;
    }

    function waitForTranslatorAndApply(languageCode) {
        let attempts = 0;
        const maxAttempts = 120;
        const timerId = window.setInterval(function () {
            attempts += 1;
            if (triggerGoogleTranslate(languageCode)) {
                window.clearInterval(timerId);
                return;
            }
            if (attempts >= maxAttempts) {
                window.clearInterval(timerId);
            }
        }, 150);
    }

    function setLanguage(languageCode, persistChoice) {
        const safeLanguage = LANGUAGE_LABELS[languageCode] ? languageCode : 'en';
        languageCurrent.textContent = LANGUAGE_LABELS[safeLanguage];
        for (let i = 0; i < languageOptionButtons.length; i++) {
            const button = languageOptionButtons[i];
            button.classList.toggle('active', button.dataset.langChoice === safeLanguage);
        }
        if (persistChoice !== false) {
            localStorage.setItem(LANG_KEY, safeLanguage);
        }
        applyGoogleTranslateCookie(safeLanguage);
        waitForTranslatorAndApply(safeLanguage);
    }

    const searchForm = document.getElementById('top-search-form');
    const searchInput = document.getElementById('top-search-input');
    const searchSuggestionList = document.getElementById('search-suggestions');
    const searchWrap = document.querySelector('.search-wrap');
    const mobileSearchHost = document.getElementById('mobile-search-host');
    const mobileSearchMedia = window.matchMedia('(max-width: 640px)');
    const searchOriginalParent = searchWrap ? searchWrap.parentElement : null;
    const searchOriginalNextSibling = searchWrap ? searchWrap.nextElementSibling : null;
    const aiAgentPanel = document.getElementById('ai-agent-panel');
    const aiQueryInput = document.getElementById('ai-query');
    const runAiAnalysisButton = document.getElementById('run-ai-analysis');
    const aiOutputPanel = document.getElementById('ai-output');
    const agentFab = document.getElementById('agent-fab');
    const agentPopup = document.getElementById('agent-popup');
    const agentOpenTabButton = document.getElementById('agent-open-tab');
    let visibleSuggestions = [];
    let activeSuggestionIndex = -1;

    function closeSearchSuggestions() {
        if (!searchSuggestionList || !searchInput) {
            return;
        }
        searchSuggestionList.innerHTML = '';
        searchSuggestionList.classList.remove('open');
        searchInput.setAttribute('aria-expanded', 'false');
        visibleSuggestions = [];
        activeSuggestionIndex = -1;
    }

    function placeSearchByViewport() {
        if (!searchWrap || !mobileSearchHost || !searchOriginalParent) {
            return;
        }
        if (mobileSearchMedia.matches) {
            if (searchWrap.parentElement !== mobileSearchHost) {
                mobileSearchHost.appendChild(searchWrap);
            }
            return;
        }
        if (searchWrap.parentElement !== searchOriginalParent) {
            if (searchOriginalNextSibling && searchOriginalNextSibling.parentElement === searchOriginalParent) {
                searchOriginalParent.insertBefore(searchWrap, searchOriginalNextSibling);
            } else {
                searchOriginalParent.appendChild(searchWrap);
            }
        }
    }

    function closeAgentPopup() {
        if (!agentPopup || !agentFab) {
            return;
        }
        agentPopup.classList.remove('open');
        agentPopup.setAttribute('aria-hidden', 'true');
        agentFab.setAttribute('aria-expanded', 'false');
    }

    function buildSearchSuggestions(query) {
        const normalizedQuery = query.toLowerCase().trim();
        if (!normalizedQuery) {
            return [];
        }
        const startsWithMatches = [];
        const containsMatches = [];
        for (let i = 0; i < SEARCH_SUGGESTIONS.length; i++) {
            const candidate = SEARCH_SUGGESTIONS[i];
            const normalizedCandidate = candidate.toLowerCase();
            if (!normalizedCandidate.includes(normalizedQuery)) {
                continue;
            }
            if (normalizedCandidate.startsWith(normalizedQuery)) {
                startsWithMatches.push(candidate);
            } else {
                containsMatches.push(candidate);
            }
        }
        return startsWithMatches.concat(containsMatches).slice(0, 8);
    }

    function updateActiveSuggestion() {
        if (!searchSuggestionList) {
            return;
        }
        const buttons = searchSuggestionList.querySelectorAll('.suggestion-button');
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].classList.toggle('active', i === activeSuggestionIndex);
        }
    }

    function chooseSuggestion(index, submitAfterChoose) {
        if (index < 0 || index >= visibleSuggestions.length || !searchInput) {
            return;
        }
        searchInput.value = visibleSuggestions[index];
        closeSearchSuggestions();
        if (submitAfterChoose && searchForm) {
            searchForm.submit();
        }
    }

    function showSearchSuggestions() {
        if (!searchInput || !searchSuggestionList) {
            return;
        }
        const nextSuggestions = buildSearchSuggestions(searchInput.value);
        if (!nextSuggestions.length) {
            closeSearchSuggestions();
            return;
        }
        visibleSuggestions = nextSuggestions;
        activeSuggestionIndex = -1;
        searchSuggestionList.innerHTML = '';
        for (let i = 0; i < visibleSuggestions.length; i++) {
            const item = document.createElement('li');
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'suggestion-button';
            button.textContent = visibleSuggestions[i];
            button.setAttribute('role', 'option');
            button.dataset.suggestionIndex = String(i);
            button.addEventListener('click', function () {
                chooseSuggestion(i, true);
            });
            item.appendChild(button);
            searchSuggestionList.appendChild(item);
        }
        searchSuggestionList.classList.add('open');
        searchInput.setAttribute('aria-expanded', 'true');
    }

    function normalizeTextValue(value) {
        return String(value || '').trim();
    }

    function parseLandAreaValue(value) {
        const parsedValue = Number.parseFloat(value);
        if (Number.isFinite(parsedValue)) {
            return parsedValue;
        }
        return null;
    }

    function getLandAreaRecommendation(landArea) {
        if (landArea === null) {
            return 'Land area is not set. Update profile land size to get more accurate planning guidance.';
        }
        if (landArea < 1) {
            return 'Your holding is below 1 acre, so focus on high-value crops, micro-irrigation, and low-cost input planning.';
        }
        if (landArea <= 3) {
            return 'For small to medium land, split fields between one stable crop and one market-driven crop to reduce risk.';
        }
        return 'For larger land area, keep crop rotation blocks and stagger sowing to distribute labor and market risk.';
    }

    function getSoilRecommendation(soilType) {
        const normalizedSoil = soilType.toLowerCase();
        if (!normalizedSoil) {
            return 'Soil type is not set. Add soil details to improve crop and fertilizer recommendations.';
        }
        if (normalizedSoil.includes('black')) {
            return 'Black soil can retain moisture well. Avoid over-irrigation and monitor drainage in heavy rain periods.';
        }
        if (normalizedSoil.includes('red')) {
            return 'Red soil often needs stronger nutrient and organic matter support. Use compost and split fertilizer doses.';
        }
        if (normalizedSoil.includes('sandy')) {
            return 'Sandy soil drains fast. Use frequent light irrigation and mulching to retain moisture.';
        }
        if (normalizedSoil.includes('clay')) {
            return 'Clay soil can compact easily. Use organic matter and maintain proper field aeration before sowing.';
        }
        return 'Use soil test-based nutrient planning for ' + soilType + ' soil to reduce cost and improve yield stability.';
    }

    function getSeasonRecommendation(seasonCode, cropName) {
        const normalizedSeason = seasonCode.toLowerCase();
        if (normalizedSeason === 'kharif') {
            return 'For Kharif, prioritize rain-ready seeds, drainage checks, and early pest scouting.';
        }
        if (normalizedSeason === 'rabi') {
            return 'For Rabi, plan irrigation scheduling and monitor nighttime temperature impacts on growth stages.';
        }
        if (normalizedSeason === 'zaid') {
            return 'For Zaid, focus on water efficiency and short-duration crops with strong local demand.';
        }
        if (normalizedSeason === 'all_season') {
            return 'For all-season farming, rotate crops and maintain staggered planning to protect soil health.';
        }
        if (cropName) {
            return 'Current season is not set. Use local agriculture office advisories for ' + cropName + ' crop scheduling.';
        }
        return 'Set your season in profile to get better sowing and input timing guidance.';
    }

    function buildDummyAiLines(requirementText) {
        if (!aiAgentPanel) {
            return [];
        }

        const farmerType = normalizeTextValue(aiAgentPanel.dataset.farmerType);
        const currentCrop = normalizeTextValue(aiAgentPanel.dataset.currentCrop);
        const soilType = normalizeTextValue(aiAgentPanel.dataset.soilType);
        const currentSeason = normalizeTextValue(aiAgentPanel.dataset.currentSeason);
        const landAreaText = normalizeTextValue(aiAgentPanel.dataset.landArea);
        const address = normalizeTextValue(aiAgentPanel.dataset.address);
        const landArea = parseLandAreaValue(landAreaText);
        const cleanRequirement = normalizeTextValue(requirementText);
        const lines = [];

        if (farmerType || currentCrop) {
            const profileSummary = [
                farmerType ? 'farmer type: ' + farmerType : '',
                currentCrop ? 'current crop: ' + currentCrop : '',
            ].filter(Boolean).join(', ');
            lines.push('Profile summary detected - ' + profileSummary + '.');
        } else {
            lines.push('Farmer type and crop are not fully set. Add them in profile for sharper recommendations.');
        }

        lines.push(getLandAreaRecommendation(landArea));
        lines.push(getSoilRecommendation(soilType));
        lines.push(getSeasonRecommendation(currentSeason, currentCrop));

        if (address) {
            lines.push('Location note: use local mandi price and weather alerts for ' + address + ' before finalizing decisions.');
        }

        if (cleanRequirement) {
            lines.push('Requirement received: "' + cleanRequirement + '". Dummy plan: apply the change on a small trial patch for 10-15 days, then scale.');
        } else {
            lines.push('Add your exact requirement above to receive a more targeted dummy recommendation.');
        }

        lines.push('System note: this is a dummy AI output until the trained model is connected.');
        return lines;
    }

    function renderDummyAiOutput(lines) {
        if (!aiOutputPanel) {
            return;
        }
        aiOutputPanel.innerHTML = '';

        const title = document.createElement('p');
        title.className = 'ai-output-title';
        title.textContent = 'Dummy AI Recommendation';
        aiOutputPanel.appendChild(title);

        const list = document.createElement('ul');
        list.className = 'ai-output-list';
        for (let i = 0; i < lines.length; i++) {
            const item = document.createElement('li');
            item.textContent = lines[i];
            list.appendChild(item);
        }
        aiOutputPanel.appendChild(list);

        const meta = document.createElement('p');
        meta.className = 'ai-output-meta';
        meta.textContent = 'Generated on ' + new Date().toLocaleString() + '.';
        aiOutputPanel.appendChild(meta);
    }

    function runDummyAiAnalysis() {
        const requirementText = aiQueryInput ? aiQueryInput.value : '';
        renderDummyAiOutput(buildDummyAiLines(requirementText));
    }

    settingsToggle.addEventListener('click', function () {
        const isOpen = settingsWrap.classList.toggle('open');
        if (!isOpen) {
            closeThemeSubmenu();
            closeLanguageSubmenu();
        }
    });

    if (hamburgerToggle) {
        hamburgerToggle.addEventListener('click', function (event) {
            event.stopPropagation();
            const isOpen = hamburgerMenu.classList.toggle('open');
            hamburgerToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
    }

    themeMenuToggle.addEventListener('click', function () {
        if (!settingsWrap.classList.contains('open')) {
            settingsWrap.classList.add('open');
        }
        closeLanguageSubmenu();
        const isThemeOpen = settingsWrap.classList.toggle('theme-open');
        themeMenuToggle.setAttribute('aria-expanded', isThemeOpen ? 'true' : 'false');
    });

    languageMenuToggle.addEventListener('click', function () {
        if (!settingsWrap.classList.contains('open')) {
            settingsWrap.classList.add('open');
        }
        closeThemeSubmenu();
        const isLanguageOpen = settingsWrap.classList.toggle('language-open');
        languageMenuToggle.setAttribute('aria-expanded', isLanguageOpen ? 'true' : 'false');
    });

    for (let i = 0; i < themeOptionButtons.length; i++) {
        const button = themeOptionButtons[i];
        button.addEventListener('click', function () {
            setTheme(button.dataset.themeChoice, true);
            closeThemeSubmenu();
        });
    }

    for (let i = 0; i < languageOptionButtons.length; i++) {
        const button = languageOptionButtons[i];
        button.addEventListener('click', function () {
            setLanguage(button.dataset.langChoice, true);
            closeLanguageSubmenu();
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', showSearchSuggestions);
        searchInput.addEventListener('focus', function () {
            if (searchInput.value.trim()) {
                showSearchSuggestions();
            }
        });
        searchInput.addEventListener('keydown', function (event) {
            if (!visibleSuggestions.length) {
                return;
            }
            if (event.key === 'ArrowDown') {
                event.preventDefault();
                activeSuggestionIndex = (activeSuggestionIndex + 1) % visibleSuggestions.length;
                updateActiveSuggestion();
                return;
            }
            if (event.key === 'ArrowUp') {
                event.preventDefault();
                activeSuggestionIndex = activeSuggestionIndex <= 0 ? visibleSuggestions.length - 1 : activeSuggestionIndex - 1;
                updateActiveSuggestion();
                return;
            }
            if (event.key === 'Enter' && activeSuggestionIndex >= 0) {
                event.preventDefault();
                chooseSuggestion(activeSuggestionIndex, true);
                return;
            }
            if (event.key === 'Escape') {
                closeSearchSuggestions();
            }
        });
    }

    if (runAiAnalysisButton) {
        runAiAnalysisButton.addEventListener('click', runDummyAiAnalysis);
    }

    if (agentFab) {
        agentFab.addEventListener('click', function (event) {
            event.stopPropagation();
            if (!agentPopup) {
                return;
            }
            const isOpen = agentPopup.classList.toggle('open');
            agentPopup.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
            agentFab.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
    }

    if (agentOpenTabButton) {
        agentOpenTabButton.addEventListener('click', function (event) {
            event.stopPropagation();
            const targetUrl = agentOpenTabButton.dataset.agentUrl || '';
            if (targetUrl) {
                window.location.href = targetUrl;
            }
            closeAgentPopup();
        });
    }

    if (aiQueryInput) {
        aiQueryInput.addEventListener('keydown', function (event) {
            if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
                event.preventDefault();
                runDummyAiAnalysis();
            }
        });
    }

    document.addEventListener('click', function (event) {
        if (hamburgerMenu && !hamburgerMenu.contains(event.target)) {
            closeHamburgerMenu();
        }
        if (searchForm && !searchForm.contains(event.target)) {
            closeSearchSuggestions();
        }
        if (!settingsWrap.contains(event.target)) {
            settingsWrap.classList.remove('open');
            closeThemeSubmenu();
            closeLanguageSubmenu();
        }
        if (agentPopup && agentFab && !agentPopup.contains(event.target) && !agentFab.contains(event.target)) {
            closeAgentPopup();
        }
    });

    if (mobileSearchMedia.addEventListener) {
        mobileSearchMedia.addEventListener('change', placeSearchByViewport);
    } else if (mobileSearchMedia.addListener) {
        mobileSearchMedia.addListener(placeSearchByViewport);
    }

    if (systemThemeMedia.addEventListener) {
        systemThemeMedia.addEventListener('change', function () {
            if ((localStorage.getItem(THEME_KEY) || 'system') === 'system') {
                setTheme('system', false);
            }
        });
    } else if (systemThemeMedia.addListener) {
        systemThemeMedia.addListener(function () {
            if ((localStorage.getItem(THEME_KEY) || 'system') === 'system') {
                setTheme('system', false);
            }
        });
    }

    window.addEventListener('storage', function (event) {
        if (event.key === THEME_KEY) {
            setTheme(event.newValue || 'system', false);
        }
        if (event.key === LANG_KEY) {
            setLanguage(event.newValue || 'en', false);
        }
    });

    setTheme(localStorage.getItem(THEME_KEY) || 'system', false);
    setLanguage(localStorage.getItem(LANG_KEY) || 'en', false);
    placeSearchByViewport();
    if (aiAgentPanel) {
        runDummyAiAnalysis();
    }
