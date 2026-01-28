#!/usr/bin/env python3
"""Trevarn brand gallery — auto-discovers HTML files in the working directory."""

import os
import re
import html
from http.server import HTTPServer, SimpleHTTPRequestHandler

SERVE_DIR = os.path.dirname(os.path.abspath(__file__)) or "."
PORT = 8080

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)

# Page metadata: filename -> (icon, description_en, description_fr)
PAGE_META = {
    "trevarn-name.html": (
        "Aa",
        "Etymology, pronunciation, and the Cornish-Breton linguistic heritage behind the name.",
        "Étymologie, prononciation et héritage linguistique cornouaillais-breton du nom."
    ),
    "trevarn-origins.html": (
        "◈",
        "From Carnac menhirs to Vera Molnár's algorithmic art — the visual DNA of the mark.",
        "Des menhirs de Carnac à l'art algorithmique de Vera Molnár — l'ADN visuel de la marque."
    ),
    "trevarn-logo-mark.html": (
        "△",
        "Primary and secondary marks, variants, background treatments, and favicon specifications.",
        "Marques primaire et secondaire, variantes, traitements de fond et spécifications favicon."
    ),
    "trevarn-colour-palette.html": (
        "●",
        "Aour Glaz, Aour Balan, and the complete colour system with accessibility guidance.",
        "Aour Glaz, Aour Balan et le système de couleurs complet avec conseils d'accessibilité."
    ),
    "trevarn-typography.html": (
        "Tt",
        "IBM Plex Sans for display, Inter for body — the type system and specifications.",
        "IBM Plex Sans pour les titres, Inter pour le corps — le système typographique."
    ),
    "trevarn-usage.html": (
        "☰",
        "Lockups, clear space, minimum sizes, brand voice, and usage guidelines.",
        "Compositions, espaces de protection, tailles minimales, ton de marque et directives."
    ),
}

# French page titles
TITLES_FR = {
    "trevarn-name.html": "Le Nom",
    "trevarn-origins.html": "Origines de la Marque",
    "trevarn-logo-mark.html": "La Marque",
    "trevarn-colour-palette.html": "Palette de Couleurs",
    "trevarn-typography.html": "Typographie",
    "trevarn-usage.html": "Utilisation",
}

ORDER = [
    "trevarn-name.html",
    "trevarn-origins.html",
    "trevarn-logo-mark.html",
    "trevarn-colour-palette.html",
    "trevarn-typography.html",
    "trevarn-usage.html",
]


def scan_pages(lang="en"):
    """Return sorted list of (filename, title) for all trevarn-*.html files."""
    pages = []
    for f in os.listdir(SERVE_DIR):
        if f.startswith("trevarn-") and f.endswith(".html") and not f.startswith("trevarn-fr-"):
            if lang == "fr":
                title = TITLES_FR.get(f, f.replace(".html", "").replace("-", " ").title())
            else:
                title = f.replace(".html", "").replace("-", " ").title()
                filepath = os.path.join(SERVE_DIR, f)
                try:
                    with open(filepath, "r", encoding="utf-8") as fh:
                        head = fh.read(2048)
                    m = TITLE_RE.search(head)
                    if m:
                        raw = m.group(1).strip()
                        title = re.sub(r"^Trevarn\s*[—–-]\s*", "", raw)
                except Exception:
                    pass
            pages.append((f, title))

    def sort_key(item):
        fname = item[0]
        try:
            return ORDER.index(fname)
        except ValueError:
            return len(ORDER)
    pages.sort(key=sort_key)
    return pages


def render_index(lang="en"):
    pages = scan_pages(lang)
    is_fr = lang == "fr"

    # Language-specific content
    if is_fr:
        page_title = "Trevarn — Charte Graphique"
        hero_label = "Charte Graphique"
        hero_statement = 'Intelligence connectée pour <strong>l\'environnement bâti</strong>. Enraciné en Bretagne. Conçu pour un déploiement mondial.'
        hero_sub = "Ce site documente l'identité de marque Trevarn dans son intégralité — de l'étymologie du nom aux spécifications de chaque marque, couleur et police."
        section_title = "Documentation"
        sections_label = "sections"
        lang_switch_href = "/"
        lang_switch_label = "EN"
        page_prefix = "/FR/"
    else:
        page_title = "Trevarn — Brand Guidelines"
        hero_label = "Brand Guidelines"
        hero_statement = 'Connected intelligence for the <strong>built environment</strong>. Rooted in Brittany. Built for global deployment.'
        hero_sub = "This site documents the complete Trevarn brand identity — from the etymology of the name to the specifications of every mark, colour, and typeface."
        section_title = "Documentation"
        sections_label = "sections"
        lang_switch_href = "/FR/"
        lang_switch_label = "FR"
        page_prefix = "/"

    cards = ""
    for i, (fname, title) in enumerate(pages):
        safe_title = html.escape(title)
        if is_fr:
            fr_fname = fname.replace("trevarn-", "trevarn-fr-")
            safe_fname = html.escape(fr_fname)
        else:
            safe_fname = html.escape(fname)
        meta = PAGE_META.get(fname, ("•", "", ""))
        icon = meta[0]
        desc = meta[2] if is_fr else meta[1]
        num = str(i + 1).zfill(2)

        cards += f"""
            <a href="{page_prefix}{safe_fname}" class="card">
                <div class="card-icon">{icon}</div>
                <div class="card-content">
                    <div class="card-num">{num}</div>
                    <h3>{safe_title}</h3>
                    <p>{html.escape(desc)}</p>
                </div>
                <div class="card-arrow">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M4 10h12M12 6l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
            </a>"""

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<title>{page_title}</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
    --aour-glaz: #4A6FA5;
    --aour-balan: #D8A23A;
    --lin-violet: #5B6B9D;
    --ink: #11181C;
    --slate: #1F3A4A;
    --mist: #8A9094;
    --cloud: #E5E7EB;
    --pearl: #F8F9FA;
    --white: #FFFFFF;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
    background: var(--ink); color: var(--white); line-height:1.6;
    min-height:100vh;
}}

/* Navbar */
.nav-bar {{
    position: absolute; top: 0; left: 0; right: 0; z-index: 100;
    padding: 20px 60px;
    display: flex; align-items: center; justify-content: space-between;
}}
.nav-logo {{ display: inline-flex; align-items: center; text-decoration: none; }}
.nav-logo:hover {{ opacity: 0.7; }}
.nav-right {{ display: flex; align-items: center; gap: 12px; }}
.pdf-download {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px; border-radius: 4px;
    border: 1px solid rgba(255,255,255,0.2);
    color: var(--mist); text-decoration: none;
    transition: all 0.15s ease;
}}
.pdf-download:hover {{
    color: var(--white); border-color: rgba(255,255,255,0.4);
}}
.pdf-download svg {{ width: 14px; height: 14px; }}
.lang-switch {{
    font-size: 12px; font-weight: 600; letter-spacing: 0.08em;
    color: var(--mist); text-decoration: none;
    padding: 6px 12px; border: 1px solid rgba(255,255,255,0.2);
    border-radius: 4px; transition: all 0.15s ease;
}}
.lang-switch:hover {{
    color: var(--white); border-color: rgba(255,255,255,0.4);
}}

/* Hero */
.hero {{
    padding: 120px 60px 100px;
    background: linear-gradient(180deg, var(--ink) 0%, #1a2a3a 100%);
    position: relative;
    overflow: hidden;
}}
.hero::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolygon points='50,380 60,180 100,160 110,380' fill='%234A6FA5' opacity='0.03'/%3E%3Cpolygon points='140,380 170,80 200,90 230,380' fill='%234A6FA5' opacity='0.03'/%3E%3Cpolygon points='260,380 300,40 360,30 390,380' fill='%234A6FA5' opacity='0.03'/%3E%3C/svg%3E") no-repeat center;
    background-size: 600px;
    opacity: 0.5;
}}
.hero-inner {{
    max-width: 1000px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}}
.hero-label {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--aour-glaz);
    margin-bottom: 40px;
}}
.hero-lockup {{
    margin-bottom: 48px;
}}
.hero-statement {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 32px;
    font-weight: 300;
    line-height: 1.4;
    color: var(--white);
    max-width: 600px;
    margin-bottom: 24px;
}}
.hero-statement strong {{
    font-weight: 600;
    color: var(--aour-balan);
}}
.hero-sub {{
    font-size: 15px;
    color: var(--mist);
    max-width: 500px;
    line-height: 1.7;
}}

/* Main content */
.main {{
    background: var(--pearl);
    padding: 80px 60px 100px;
}}
.main-inner {{
    max-width: 1000px;
    margin: 0 auto;
}}
.section-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--cloud);
}}
.section-title {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--mist);
}}
.section-count {{
    font-size: 12px;
    color: var(--cloud);
}}

/* Cards grid */
.cards {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}}
.card {{
    background: var(--white);
    border-radius: 12px;
    padding: 32px;
    text-decoration: none;
    color: inherit;
    display: grid;
    grid-template-columns: 48px 1fr 24px;
    gap: 20px;
    align-items: start;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}}
.card:hover {{
    border-color: var(--aour-glaz);
    box-shadow: 0 8px 32px rgba(74, 111, 165, 0.12);
    transform: translateY(-2px);
}}
.card-icon {{
    width: 48px;
    height: 48px;
    background: var(--pearl);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: var(--aour-glaz);
}}
.card-content {{
    min-width: 0;
}}
.card-num {{
    font-size: 11px;
    font-weight: 600;
    color: var(--cloud);
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
}}
.card-content h3 {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: var(--slate);
    margin-bottom: 8px;
}}
.card-content p {{
    font-size: 13px;
    color: var(--mist);
    line-height: 1.6;
}}
.card-arrow {{
    color: var(--cloud);
    transition: all 0.2s ease;
    margin-top: 4px;
}}
.card:hover .card-arrow {{
    color: var(--aour-glaz);
    transform: translateX(4px);
}}

/* Footer */
.footer {{
    background: var(--ink);
    padding: 60px;
    text-align: center;
}}
.footer-mark {{
    opacity: 0.2;
    margin-bottom: 24px;
}}
.footer-text {{
    font-size: 12px;
    color: var(--mist);
    letter-spacing: 0.05em;
}}
.footer-text a {{
    color: var(--aour-glaz);
    text-decoration: none;
}}
.footer-text a:hover {{
    text-decoration: underline;
}}

/* Responsive */
@media (max-width: 768px) {{
    .nav-bar {{ padding: 16px 24px; }}
    .hero {{ padding: 100px 24px 80px; }}
    .hero-statement {{ font-size: 26px; }}
    .main {{ padding: 60px 24px 80px; }}
    .cards {{ grid-template-columns: 1fr; }}
    .card {{ padding: 24px; }}
    .card-content h3 {{ font-size: 18px; }}
}}
@media (max-width: 480px) {{
    .hero {{ padding: 88px 20px 60px; }}
    .hero-lockup svg {{ width: 100%; max-width: 300px; }}
    .hero-statement {{ font-size: 22px; }}
    .main {{ padding: 48px 20px 60px; }}
    .card {{ grid-template-columns: 40px 1fr 20px; gap: 16px; padding: 20px; }}
    .card-icon {{ width: 40px; height: 40px; font-size: 16px; }}
}}
</style>
</head>
<body>

<div class="nav-bar">
    <a href="{'/' if not is_fr else '/FR/'}" class="nav-logo">
        <svg viewBox="0 0 64 36" width="40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polyline points="2.3,34.1 4.8,16.2 11.2,13.5 13.8,34.5 17.5,33.5 23.2,4.8 28.8,6.5 34.5,34.2 37.2,33.8 43.8,2.8 56.2,0.5 62.5,34.8" stroke="#4A6FA5" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </a>
    <div class="nav-right">
        <a href="/trevarn-brand-guidelines.pdf" class="pdf-download" title="{'Télécharger le Guide de Marque (PDF)' if is_fr else 'Download Brand Guidelines (PDF)'}" download>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="12" y1="18" x2="12" y2="12"></line>
                <polyline points="9 15 12 18 15 15"></polyline>
            </svg>
        </a>
        <a href="{lang_switch_href}" class="lang-switch">{lang_switch_label}</a>
    </div>
</div>

<div class="hero">
    <div class="hero-inner">
        <div class="hero-label">{hero_label}</div>
        <div class="hero-lockup">
            <svg viewBox="0 0 420 50" width="380" fill="none" xmlns="http://www.w3.org/2000/svg">
                <polyline points="2.3,40.1 5.6,19.0 13.2,15.8 16.5,40.6 20.6,39.4 27.3,5.6 33.9,7.6 40.6,40.3 43.8,39.8 51.5,3.3 66.1,0.6 73.6,41.0" stroke="#4A6FA5" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                <text x="92" y="36" font-family="Inter, sans-serif" font-weight="600" font-size="32" letter-spacing="0.12em" fill="#FFFFFF">TREVARN</text>
            </svg>
        </div>
        <p class="hero-statement">
            {hero_statement}
        </p>
        <p class="hero-sub">
            {hero_sub}
        </p>
    </div>
</div>

<div class="main">
    <div class="main-inner">
        <div class="section-header">
            <div class="section-title">{section_title}</div>
            <div class="section-count">{len(pages)} {sections_label}</div>
        </div>
        <div class="cards">{cards}
        </div>
    </div>
</div>

<div class="footer">
    <div class="footer-mark">
        <svg viewBox="0 0 64 38" width="48" xmlns="http://www.w3.org/2000/svg">
            <polygon points="2.3,34.1 4.8,16.2 11.2,13.5 13.8,34.5" fill="#4A6FA5"/>
            <polygon points="17.5,33.5 23.2,4.8 28.8,6.5 34.5,34.2" fill="#4A6FA5"/>
            <polygon points="37.2,33.8 43.8,2.8 56.2,0.5 62.5,34.8" fill="#4A6FA5"/>
        </svg>
    </div>
    <p class="footer-text">
        Trevarn Brand Identity System &middot; {'Janvier' if is_fr else 'January'} 2026<br>
        <a href="https://trevarn.com">trevarn.com</a>
    </p>
</div>

</body>
</html>"""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)

    def do_GET(self):
        # English homepage
        if self.path == "/" or self.path == "/index.html":
            content = render_index("en").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        # French homepage
        elif self.path == "/FR/" or self.path == "/FR" or self.path == "/fr/" or self.path == "/fr":
            content = render_index("fr").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        # French detail pages - serve from /FR/ prefix
        elif self.path.startswith("/FR/") or self.path.startswith("/fr/"):
            # Normalize path and serve file
            filename = self.path.split("/")[-1]
            self.path = "/" + filename
            super().do_GET()
        else:
            super().do_GET()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Serving Trevarn brand gallery on port {PORT}")
    server.serve_forever()
