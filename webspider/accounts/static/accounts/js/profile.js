function googleTranslateElementInit() {
        new google.translate.TranslateElement(
            { pageLanguage: 'en' },
            'google_translate_element'
        );
        syncLanguageFromStorage();
    }

    const THEME_KEY = 'auth_theme';
    const LANG_KEY = 'site_language';
    const SUPPORTED_LANGS = ['en', 'hi', 'bn', 'te', 'mr', 'ta', 'ur', 'gu', 'kn', 'or', 'ml', 'pa', 'as', 'mai', 'sat', 'ks', 'ne', 'kok', 'sd', 'doi', 'mni'];
    const body = document.body;
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const hamburgerToggle = document.getElementById('hamburger-toggle');
    const themeToggle = document.getElementById('theme-toggle');
    const systemThemeMedia = window.matchMedia('(prefers-color-scheme: dark)');
    const seasonField = document.getElementById('current_season');

    function applyGoogleTranslateCookie(languageCode) {
        const safeLanguage = SUPPORTED_LANGS.indexOf(languageCode) >= 0 ? languageCode : 'en';
        const cookieValue = '/en/' + safeLanguage;
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
            if (triggerGoogleTranslate(languageCode) || attempts >= maxAttempts) {
                window.clearInterval(timerId);
            }
        }, 150);
    }

    function syncLanguageFromStorage() {
        const safeLanguage = localStorage.getItem(LANG_KEY) || 'en';
        applyGoogleTranslateCookie(safeLanguage);
        waitForTranslatorAndApply(safeLanguage);
    }

    function resolveTheme(themeName) {
        if (themeName === 'system') {
            return systemThemeMedia.matches ? 'dark' : 'light';
        }
        return themeName === 'dark' ? 'dark' : 'light';
    }

    function setTheme(themeName, persistChoice) {
        const resolvedTheme = resolveTheme(themeName);
        const isDark = resolvedTheme === 'dark';
        body.classList.toggle('theme-dark', isDark);
        themeToggle.textContent = isDark ? 'Theme: Dark' : 'Theme: Light';
        if (persistChoice) {
            localStorage.setItem(THEME_KEY, themeName);
        }
    }

    function closeHamburgerMenu() {
        if (!hamburgerMenu || !hamburgerToggle) {
            return;
        }
        hamburgerMenu.classList.remove('open');
        hamburgerToggle.setAttribute('aria-expanded', 'false');
    }

    if (hamburgerToggle) {
        hamburgerToggle.addEventListener('click', function (event) {
            event.stopPropagation();
            const isOpen = hamburgerMenu.classList.toggle('open');
            hamburgerToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
    }

    themeToggle.addEventListener('click', function () {
        const currentChoice = localStorage.getItem(THEME_KEY) || 'system';
        const currentResolved = resolveTheme(currentChoice);
        const nextTheme = currentResolved === 'dark' ? 'light' : 'dark';
        setTheme(nextTheme, true);
    });

    function inferSeasonFromMonth(month) {
        if (month >= 6 && month <= 10) {
            return 'kharif';
        }
        if (month === 11 || month === 12 || month <= 3) {
            return 'rabi';
        }
        return 'zaid';
    }

    function setSeasonFromLocationIfEmpty() {
        if (!seasonField || seasonField.value) {
            return;
        }
        const monthBasedSeason = inferSeasonFromMonth(new Date().getMonth() + 1);
        const applySeason = function () {
            seasonField.value = monthBasedSeason;
        };

        if (!navigator.geolocation) {
            applySeason();
            return;
        }

        navigator.geolocation.getCurrentPosition(
            function (position) {
                // TODO: Add Google API credentials here for accurate location-based season logic.
                // const GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_API_KEY';
                // Use `position.coords.latitude` and `position.coords.longitude` with a weather/geocoding API.
                // Example (with valid key):
                // fetch(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${position.coords.latitude},${position.coords.longitude}&key=${GOOGLE_MAPS_API_KEY}`)
                applySeason();
            },
            function () {
                applySeason();
            },
            { enableHighAccuracy: false, timeout: 5000, maximumAge: 300000 }
        );
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
            syncLanguageFromStorage();
        }
    });

    document.addEventListener('click', function (event) {
        if (hamburgerMenu && !hamburgerMenu.contains(event.target)) {
            closeHamburgerMenu();
        }
    });

    syncLanguageFromStorage();
    setTheme(localStorage.getItem(THEME_KEY) || 'system', false);
    setSeasonFromLocationIfEmpty();
