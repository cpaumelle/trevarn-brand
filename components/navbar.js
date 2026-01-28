// Trevarn Brand Guidelines - Shared Navigation Component
(function() {
    const currentPath = window.location.pathname;
    const isFrencH = currentPath.includes('/FR/') || currentPath.includes('-fr-');

    // Determine which page is active
    const getActiveClass = (href) => {
        if (currentPath.endsWith(href) || currentPath.endsWith(href.replace('.html', ''))) {
            return 'active';
        }
        return '';
    };

    // Navigation links
    const navLinks = isFrencH ? [
        { href: '/FR/trevarn-fr-name.html', label: 'Nom' },
        { href: '/FR/trevarn-fr-origins.html', label: 'Origines' },
        { href: '/FR/trevarn-fr-logo-mark.html', label: 'Marque' },
        { href: '/FR/trevarn-fr-colour-palette.html', label: 'Couleurs' },
        { href: '/FR/trevarn-fr-typography.html', label: 'Typographie' },
        { href: '/FR/trevarn-fr-icons.html', label: 'Icones' },
        { href: '/FR/trevarn-fr-usage.html', label: 'Usage' }
    ] : [
        { href: '/trevarn-name.html', label: 'Name' },
        { href: '/trevarn-origins.html', label: 'Mark Origins' },
        { href: '/trevarn-logo-mark.html', label: 'Mark' },
        { href: '/trevarn-colour-palette.html', label: 'Colours' },
        { href: '/trevarn-typography.html', label: 'Typography' },
        { href: '/trevarn-icons.html', label: 'Icons' },
        { href: '/trevarn-usage.html', label: 'Usage' }
    ];

    // Get the corresponding page in the other language
    const getLangSwitchHref = () => {
        if (isFrencH) {
            return currentPath.replace('/FR/', '/').replace('-fr-', '-').replace('trevarn-fr-', 'trevarn-');
        } else {
            const filename = currentPath.split('/').pop();
            return '/FR/trevarn-fr-' + filename.replace('trevarn-', '');
        }
    };

    const langSwitchHref = getLangSwitchHref();
    const langSwitchLabel = isFrencH ? 'EN' : 'FR';
    const pdfTitle = isFrencH ? 'Télécharger le Guide de Marque (PDF)' : 'Download Brand Guidelines (PDF)';

    // Build navigation HTML
    const navHTML = `
        <a href="/" class="nav-logo">
            <svg viewBox="0 0 64 36" width="40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <polyline points="2.3,34.1 4.8,16.2 11.2,13.5 13.8,34.5 17.5,33.5 23.2,4.8 28.8,6.5 34.5,34.2 37.2,33.8 43.8,2.8 56.2,0.5 62.5,34.8" stroke="#4A6FA5" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </a>
        <nav class="nav-center">
            ${navLinks.map(link => `<a href="${link.href}" class="${getActiveClass(link.href)}">${link.label}</a>`).join('\n            ')}
        </nav>
        <div class="nav-right">
            <a href="/trevarn-brand-guidelines.pdf" class="pdf-download" title="${pdfTitle}" download>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="12" y1="18" x2="12" y2="12"></line>
                    <polyline points="9 15 12 18 15 15"></polyline>
                </svg>
            </a>
            <a href="${langSwitchHref}" class="lang-switch">${langSwitchLabel}</a>
        </div>
    `;

    // Insert navbar when DOM is ready
    const insertNavbar = () => {
        const navbar = document.querySelector('.nav-bar');
        if (navbar) {
            navbar.innerHTML = navHTML;
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', insertNavbar);
    } else {
        insertNavbar();
    }
})();
