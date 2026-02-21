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
    const themeButtons = document.querySelectorAll('.theme-btn');
    const systemThemeMedia = window.matchMedia('(prefers-color-scheme: dark)');

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
        document.body.classList.toggle('theme-dark', isDark);
        const activeTheme = themeName === 'system' ? resolvedTheme : themeName;
        for (let i = 0; i < themeButtons.length; i++) {
            const button = themeButtons[i];
            button.classList.toggle('active', button.dataset.theme === activeTheme);
        }
        if (persistChoice) {
            localStorage.setItem(THEME_KEY, themeName);
        }
    }

    for (let i = 0; i < themeButtons.length; i++) {
        const button = themeButtons[i];
        button.addEventListener('click', function () {
            setTheme(button.dataset.theme, true);
        });
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

    syncLanguageFromStorage();
    setTheme(localStorage.getItem(THEME_KEY) || 'system', false);

    const usernameInput = document.getElementById('username');
    const countryCodeInput = document.getElementById('country_code');
    const gmailSuggestion = document.getElementById('gmail-suggestion');

    function updateGmailSuggestion() {
        const value = usernameInput.value.trim();
        const isPhoneNumber = /^\d{7,}$/.test(value);
        const needsGmailSuggestion = value && !isPhoneNumber && !value.includes('@');

        if (needsGmailSuggestion) {
            const suggestedEmail = value + '@gmail.com';
            gmailSuggestion.textContent = 'Use ' + suggestedEmail;
            gmailSuggestion.dataset.value = suggestedEmail;
            gmailSuggestion.style.display = 'block';
        } else {
            gmailSuggestion.dataset.value = '';
            gmailSuggestion.style.display = 'none';
        }
    }

    function applyGmailSuggestion() {
        const suggestedEmail = gmailSuggestion.dataset.value;
        if (!suggestedEmail) {
            return;
        }
        usernameInput.value = suggestedEmail;
        gmailSuggestion.dataset.value = '';
        gmailSuggestion.style.display = 'none';
        handleInput();
    }

    function handleInput() {
        var val = usernameInput.value.trim();
        var ccDiv = document.getElementById('country-code-div');
        if (/^\d{7,}$/.test(val)) {
            ccDiv.style.display = 'block';
            countryCodeInput.required = true;
        } else {
            ccDiv.style.display = 'none';
            countryCodeInput.required = false;
        }
        updateGmailSuggestion();
    }

    gmailSuggestion.addEventListener('click', applyGmailSuggestion);
    gmailSuggestion.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            applyGmailSuggestion();
        }
    });

    handleInput();
