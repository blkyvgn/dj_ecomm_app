function getCookieTheme(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const theme_csrftoken = getCookieTheme('csrftoken');

const themes = {
    light: {
        '--bg-html-color': '#FFFFFF',
        '--bg-body-color': '#FFFFFF',
        '--bg-content-color': '#F0F0F0',
        '--bg-nav-color': '#C0C0C0',
        '--bg-footer-color': '#C0C0C0',
        '--text-color': '#404040',
        '--border-color': '#404040',
        '--box-shadow-color': 'gray',
        '--wish-color': '#E498A5',
        '--compare-color': '#7CB9E8',
        '--box-color':  '#8FBC8F',
        '--bg-error-message-color': '#F08080',
        '--error-message-color': '#FFFFFF',
        '--bg-success-message-color': '#90ee90',
        '--success-message-color': '#FFFFFF',
        
    },
    dark: {
        '--bg-html-color': '#FFFFFF',
        '--bg-body-color': '#C0C0C0',
        '--bg-content-color': '#606060',
        '--bg-nav-color': '#404040',
        '--bg-footer-color': '#404040',
        '--text-color': '#F0F0F0',
        '--border-color': '#F0F0F0',
        '--box-shadow-color': '#f0f2f4',
        '--wish-color': '#E498A5',
        '--compare-color': '#7CB9E8',
        '--box-color':  '#8FBC8F',
        '--bg-error-message-color': '#F08080',
        '--error-message-color': '#FFFFFF',
        '--bg-success-message-color': '#90ee90',
        '--success-message-color': '#FFFFFF',
    },
    green: {
        '--bg-html-color': '#FFFFFF',
        '--bg-body-color': 'green',
        '--bg-content-color': '#606060',
        '--bg-nav-color': '#404040',
        '--bg-footer-color': '#404040',
        '--text-color': '#F0F0F0',
        '--border-color': '#F0F0F0',
        '--box-shadow-color': '#f0f2f4',
        '--wish-color': '#E498A5',
        '--compare-color': '#7CB9E8',
        '--box-color':  '#8FBC8F',
        '--bg-error-message-color': '#F08080',
        '--error-message-color': '#FFFFFF',
        '--bg-success-message-color': '#90ee90',
        '--success-message-color': '#FFFFFF',
    },
    blue: {
        '--bg-html-color': '#FFFFFF',
        '--bg-body-color': 'blue',
        '--bg-content-color': '#606060',
        '--bg-nav-color': '#404040',
        '--bg-footer-color': '#404040',
        '--text-color': '#F0F0F0',
        '--border-color': '#F0F0F0',
        '--box-shadow-color': '#f0f2f4',
        '--wish-color': '#E498A5',
        '--compare-color': '#7CB9E8',
        '--box-color':  '#8FBC8F',
        '--bg-error-message-color': '#F08080',
        '--error-message-color': '#FFFFFF',
        '--bg-success-message-color': '#90ee90',
        '--success-message-color': '#FFFFFF',
    }
}

class ThemeManager {
    constructor(options) {
        if ('themeSelector' in options) {
            this.themeElem = document.querySelector(options.themeSelector);
        } else {
            this.themeElem = document.querySelector('html');
        }
        this.themes = options.themes;
        this.themesKeys = Object.keys(options.themes);
        if ('default' in options) {
            this.defaultTheme = options.default;
        } else {
            this.defaultTheme = this.themes[0];
        }
        this.docStyle = document.documentElement.style;
        this.currentTheme = this.defaultTheme;
        this.saveUrl = options.saveUrl;
        this.set();
    }
    getDefaultThemeIfNotExist(theme) {
        if (theme == null || theme == undefined || !this.themesKeys.includes(theme)) { 
            console.log('ERROR: Theme with this key doesn\'t exist. Set default theme.')
            return this.defaultTheme;
        }
        return theme;
    }
    set(theme=this.themeElem.dataset.theme) {
        theme = this.getDefaultThemeIfNotExist(theme);
        Object.entries(this.themes[theme]).forEach(([key, value]) => {
            this.docStyle.setProperty(key, value);
        });
    }
    get() {
        return this.currentTheme;
    }
    next() {
        /* If theme key is null - get next obj from themes obj */
        let currentThemeIndex = this.themesKeys.indexOf(this.currentTheme);
        const nextIndex = (currentThemeIndex + 1) % this.themesKeys.length;
        return this.themesKeys[nextIndex];
    }
    change(theme=null) {
        if (this.currentTheme == theme) { return; }
        const newTheme = (theme == null)? this.next() : theme;
        this.set(newTheme);
        this.themeElem.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        this.currentTheme = newTheme
        if (this.saveUrl != null) {
            this.fetchSaveUrl({'theme':newTheme});
        }
    }
    fetchSaveUrl(themeObj) {
        const data = optionObj;
        fetch(this.saveUrl, {  
            method: 'post',  
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': theme_csrftoken,
            },
            body: JSON.stringify(data)
        })
        .then((response) => {
            return response.json()
        })  
        .then((json) => {
            console.log('Request succeeded with JSON response', json);  
        })  
        .catch(function (error) {  
            console.log('Request failed', error);  
        });
    }
}
const theme = new ThemeManager({
    themeSelector: 'html', 
    themes: themes,
    default: 'light',
    saveUrl: null, // document.querySelector('html').dataset.company + '/options/',
})