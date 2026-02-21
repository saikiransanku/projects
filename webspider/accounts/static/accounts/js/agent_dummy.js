const THEME_KEY = 'auth_theme';
    const THEME_OPTIONS = ['light', 'dark', 'system'];
    const body = document.body;
    const systemThemeMedia = window.matchMedia('(prefers-color-scheme: dark)');

    function resolveTheme(themeName) {
        if (themeName === 'system') {
            return systemThemeMedia.matches ? 'dark' : 'light';
        }
        return themeName === 'dark' ? 'dark' : 'light';
    }

    function setTheme(themeName) {
        const safeTheme = THEME_OPTIONS.indexOf(themeName) >= 0 ? themeName : 'system';
        const resolvedTheme = resolveTheme(safeTheme);
        body.classList.toggle('theme-dark', resolvedTheme === 'dark');
    }

    if (systemThemeMedia.addEventListener) {
        systemThemeMedia.addEventListener('change', function () {
            if ((localStorage.getItem(THEME_KEY) || 'system') === 'system') {
                setTheme('system');
            }
        });
    } else if (systemThemeMedia.addListener) {
        systemThemeMedia.addListener(function () {
            if ((localStorage.getItem(THEME_KEY) || 'system') === 'system') {
                setTheme('system');
            }
        });
    }

    window.addEventListener('storage', function (event) {
        if (event.key === THEME_KEY) {
            setTheme(event.newValue || 'system');
        }
    });

    setTheme(localStorage.getItem(THEME_KEY) || 'system');
