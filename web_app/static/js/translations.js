const translations = {
    'en': {
        // Language Selection
        'english': 'English',
        'spanish': 'Spanish',
        'french': 'French',
        
        // Welcome Page Content
        'view_wrapped': 'View Your Wrapped',
        'view_wraps': 'View Your Wraps',
        'play_game': 'Play a game?'
    },
    'es': {
        // Language Selection
        'english': 'Inglés',
        'spanish': 'Español',
        'french': 'Francés',
        
        // Welcome Page Content
        'view_wrapped': 'Ver tu Wrapped',
        'view_wraps': 'Ver tus Wraps',
        'play_game': '¿Jugar un juego?'
    },
    'fr': {
        // Language Selection
        'english': 'Anglais',
        'spanish': 'Espagnol',
        'french': 'Français',
        
        // Welcome Page Content
        'view_wrapped': 'Voir votre Wrapped',
        'view_wraps': 'Voir vos Wraps',
        'play_game': 'Jouer à un jeu ?'
    }
};

// Function to update page content based on selected language
function updateContent(lang) {
    // Save language preference
    localStorage.setItem('preferred_language', lang);
    
    // Update all translatable elements
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
}

// Function to get current language
function getCurrentLanguage() {
    return localStorage.getItem('preferred_language') || 'en';
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
    const currentLang = getCurrentLanguage();
    document.getElementById('languageSelect').value = currentLang;
    updateContent(currentLang);
});
