#!/usr/bin/env python3
"""Build Budinvest Steel site from partials + src → public/ with i18n support"""

import os, re, glob, shutil, json

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SITE_DIR, 'src')
PARTIALS_DIR = os.path.join(SITE_DIR, '_partials')
PUBLIC_DIR = os.path.join(SITE_DIR, 'public')
I18N_DIR = os.path.join(SITE_DIR, 'i18n')

# Language configurations
LANGUAGES = {
    'pl': {'lang_code': 'pl', 'lang_attr': 'pl', 'dir_prefix': '', 'url_prefix': ''},
    'en': {'lang_code': 'en', 'lang_attr': 'en', 'dir_prefix': 'en', 'url_prefix': '/en'},
    'de': {'lang_code': 'de', 'lang_attr': 'de', 'dir_prefix': 'de', 'url_prefix': '/de'}
}

# URL mappings between languages
URL_MAP = {
    '': {'en': 'index', 'de': 'index'},  # homepage
    'o-nas': {'en': 'about', 'de': 'ueber-uns'},
    'uslugi': {'en': 'services', 'de': 'leistungen'},
    'uslugi/konstrukcje-stalowe': {'en': 'services/steel-structures', 'de': 'leistungen/stahlkonstruktionen'},
    'uslugi/zbiorniki-cisnieniowe': {'en': 'services/pressure-vessels', 'de': 'leistungen/druckbehaelter'},
    'uslugi/rurociagi-przemyslowe': {'en': 'services/industrial-pipelines', 'de': 'leistungen/industrierohrleitungen'},
    'uslugi/obrobka-metali': {'en': 'services/metal-processing', 'de': 'leistungen/metallbearbeitung'},
    'uslugi/prefabrykacja-betonu': {'en': 'services/concrete-prefabrication', 'de': 'leistungen/betonfertigteile'},
    'realizacje': {'en': 'projects', 'de': 'projekte'},
    'certyfikaty': {'en': 'certifications', 'de': 'zertifikate'},
    'park-maszynowy': {'en': 'machinery', 'de': 'maschinenpark'},
    'kariera': {'en': 'careers', 'de': 'karriere'},
    'kontakt': {'en': 'contact', 'de': 'kontakt'}
}

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def load_translations(lang_code):
    """Load translations for given language"""
    trans_path = os.path.join(I18N_DIR, f'{lang_code}.json')
    if os.path.exists(trans_path):
        with open(trans_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def parse_frontmatter(content):
    """Parse YAML-like frontmatter between --- markers"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, content
    meta = {}
    for line in match.group(1).strip().split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            meta[key.strip()] = value.strip()
    body = content[match.end():]
    return meta, body

def get_localized_navbar(lang_code, nav_active=''):
    """Get navbar with localized links"""
    navbar_template = read_file(os.path.join(PARTIALS_DIR, '_navbar.html'))
    
    if lang_code == 'en':
        # Replace Polish links with English
        navbar_template = navbar_template.replace('href="/"', 'href="/en/"')
        navbar_template = navbar_template.replace('href="/o-nas"', 'href="/en/about"')
        navbar_template = navbar_template.replace('href="/uslugi"', 'href="/en/services"')
        navbar_template = navbar_template.replace('href="/certyfikaty"', 'href="/en/certifications"')
        navbar_template = navbar_template.replace('href="/realizacje"', 'href="/en/projects"')
        navbar_template = navbar_template.replace('href="/kontakt"', 'href="/en/contact"')
        # Service links
        navbar_template = navbar_template.replace('href="/uslugi/obrobka-metali"', 'href="/en/services/metal-processing"')
        navbar_template = navbar_template.replace('href="/uslugi/konstrukcje-stalowe"', 'href="/en/services/steel-structures"')
        navbar_template = navbar_template.replace('href="/uslugi/rurociagi-przemyslowe"', 'href="/en/services/industrial-pipelines"')
        navbar_template = navbar_template.replace('href="/uslugi/zbiorniki-cisnieniowe"', 'href="/en/services/pressure-vessels"')
        navbar_template = navbar_template.replace('href="/uslugi/prefabrykacja-betonu"', 'href="/en/services/concrete-prefabrication"')
    elif lang_code == 'de':
        # Replace Polish links with German
        navbar_template = navbar_template.replace('href="/"', 'href="/de/"')
        navbar_template = navbar_template.replace('href="/o-nas"', 'href="/de/ueber-uns"')
        navbar_template = navbar_template.replace('href="/uslugi"', 'href="/de/leistungen"')
        navbar_template = navbar_template.replace('href="/certyfikaty"', 'href="/de/zertifikate"')
        navbar_template = navbar_template.replace('href="/realizacje"', 'href="/de/projekte"')
        navbar_template = navbar_template.replace('href="/kontakt"', 'href="/de/kontakt"')
        # Service links
        navbar_template = navbar_template.replace('href="/uslugi/obrobka-metali"', 'href="/de/leistungen/metallbearbeitung"')
        navbar_template = navbar_template.replace('href="/uslugi/konstrukcje-stalowe"', 'href="/de/leistungen/stahlkonstruktionen"')
        navbar_template = navbar_template.replace('href="/uslugi/rurociagi-przemyslowe"', 'href="/de/leistungen/industrierohrleitungen"')
        navbar_template = navbar_template.replace('href="/uslugi/zbiorniki-cisnieniowe"', 'href="/de/leistungen/druckbehaelter"')
        navbar_template = navbar_template.replace('href="/uslugi/prefabrykacja-betonu"', 'href="/de/leistungen/betonfertigteile"')
    
    # Set active nav
    if nav_active:
        navbar_template = navbar_template.replace(f'data-nav="{nav_active}"', f'data-nav="{nav_active}" class="active"')
    
    return navbar_template

def get_localized_mobile_menu(lang_code, nav_active=''):
    """Get mobile menu with localized links"""
    mobile_menu = read_file(os.path.join(PARTIALS_DIR, '_mobile-menu.html'))
    
    if lang_code == 'en':
        # Replace Polish links with English
        mobile_menu = mobile_menu.replace('href="/"', 'href="/en/"')
        mobile_menu = mobile_menu.replace('href="/o-nas"', 'href="/en/about"')
        mobile_menu = mobile_menu.replace('href="/uslugi"', 'href="/en/services"')
        mobile_menu = mobile_menu.replace('href="/certyfikaty"', 'href="/en/certifications"')
        mobile_menu = mobile_menu.replace('href="/realizacje"', 'href="/en/projects"')
        mobile_menu = mobile_menu.replace('href="/kontakt"', 'href="/en/contact"')
    elif lang_code == 'de':
        # Replace Polish links with German
        mobile_menu = mobile_menu.replace('href="/"', 'href="/de/"')
        mobile_menu = mobile_menu.replace('href="/o-nas"', 'href="/de/ueber-uns"')
        mobile_menu = mobile_menu.replace('href="/uslugi"', 'href="/de/leistungen"')
        mobile_menu = mobile_menu.replace('href="/certyfikaty"', 'href="/de/zertifikate"')
        mobile_menu = mobile_menu.replace('href="/realizacje"', 'href="/de/projekte"')
        mobile_menu = mobile_menu.replace('href="/kontakt"', 'href="/de/kontakt"')
    
    # Set active nav
    if nav_active:
        mobile_menu = mobile_menu.replace(f'data-nav="{nav_active}"', f'data-nav="{nav_active}" class="active"')
    
    return mobile_menu

def generate_hreflang(page_key, current_lang):
    """Generate hreflang tags for a page"""
    hreflangs = []
    
    # Polish (canonical)
    if current_lang == 'pl':
        pl_url = f'https://budinvest-steel.com/{page_key}' if page_key else 'https://budinvest-steel.com'
    else:
        pl_url = f'https://budinvest-steel.com/{page_key}' if page_key else 'https://budinvest-steel.com'
        
    hreflangs.append(f'<link rel="alternate" hreflang="pl" href="{pl_url}" />')
    
    # English
    if page_key in URL_MAP and 'en' in URL_MAP[page_key]:
        en_page = URL_MAP[page_key]['en']
        en_url = f'https://budinvest-steel.com/en/{en_page}.html' if en_page != 'index' else 'https://budinvest-steel.com/en/'
        en_url = en_url.replace('.html', '')
        hreflangs.append(f'<link rel="alternate" hreflang="en" href="{en_url}" />')
    
    # German
    if page_key in URL_MAP and 'de' in URL_MAP[page_key]:
        de_page = URL_MAP[page_key]['de']
        de_url = f'https://budinvest-steel.com/de/{de_page}.html' if de_page != 'index' else 'https://budinvest-steel.com/de/'
        de_url = de_url.replace('.html', '')
        hreflangs.append(f'<link rel="alternate" hreflang="de" href="{de_url}" />')
    
    # Default/canonical
    hreflangs.append(f'<link rel="alternate" hreflang="x-default" href="{pl_url}" />')
    
    return '\n    '.join(hreflangs)

def build_page(src_path, rel_path, lang_code='pl', translations=None):
    """Build a page for specific language"""
    if translations is None:
        translations = {}
        
    content = read_file(src_path)
    meta, body = parse_frontmatter(content)
    
    title = meta.get('title', 'Budinvest Steel')
    description = meta.get('description', '')
    nav_active = meta.get('nav_active', '')
    
    # Load partials
    head = read_file(os.path.join(PARTIALS_DIR, '_head.html'))
    navbar = get_localized_navbar(lang_code, nav_active)
    mobile_menu = get_localized_mobile_menu(lang_code, nav_active)
    footer = read_file(os.path.join(PARTIALS_DIR, '_footer.html'))
    scripts = read_file(os.path.join(PARTIALS_DIR, '_scripts.html'))
    noise = read_file(os.path.join(PARTIALS_DIR, '_noise.html'))
    
    # Build canonical URL and page key for hreflang
    lang_config = LANGUAGES[lang_code]
    page_path = rel_path.replace('index.html', '').replace('.html', '')
    page_key = page_path  # Used for hreflang mapping
    
    if lang_code == 'pl':
        canonical_url = f'https://budinvest-steel.com/{page_path}' if page_path else 'https://budinvest-steel.com'
    else:
        canonical_url = f'https://budinvest-steel.com{lang_config["url_prefix"]}/{page_path}' if page_path else f'https://budinvest-steel.com{lang_config["url_prefix"]}/'
    
    canonical_url = canonical_url.rstrip('/')
    if not canonical_url.endswith('.html') and canonical_url != 'https://budinvest-steel.com':
        canonical_url = canonical_url
    
    # Generate hreflang tags
    hreflangs = generate_hreflang(page_key, lang_code)
    
    # Assemble
    html = f'''<!DOCTYPE html>
<html lang="{lang_config['lang_attr']}">
<head>
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    {hreflangs}
{head}
</head>
<body>
{noise}
{navbar}
{mobile_menu}
{body}
{footer}
{scripts}
</body>
</html>'''
    
    # Determine output path
    if lang_code == 'pl':
        out_path = os.path.join(PUBLIC_DIR, rel_path)
    else:
        out_path = os.path.join(PUBLIC_DIR, lang_config['dir_prefix'], rel_path)
    
    write_file(out_path, html)
    return out_path

def main():
    print('🔨 Building Budinvest Steel (multilingual)...')
    
    # Clean public (only html files, keep images etc)
    for f in glob.glob(os.path.join(PUBLIC_DIR, '**/*.html'), recursive=True):
        os.remove(f)
    
    # Load translations for each language
    translations = {}
    for lang in LANGUAGES.keys():
        translations[lang] = load_translations(lang)
    
    count = 0
    
    # Build all languages
    for lang_code in LANGUAGES.keys():
        print(f'\n📄 Building {lang_code.upper()}...')
        
        # Determine source directory for this language
        if lang_code == 'pl':
            lang_src_dir = SRC_DIR
        else:
            lang_src_dir = os.path.join(SRC_DIR, lang_code)
            # If language-specific folder doesn't exist, use Polish as fallback
            if not os.path.exists(lang_src_dir):
                lang_src_dir = SRC_DIR
        
        # Build all src html files for this language
        for root, dirs, files in os.walk(lang_src_dir):
            for fname in files:
                if fname.endswith('.html'):
                    src_path = os.path.join(root, fname)
                    rel_path = os.path.relpath(src_path, lang_src_dir)
                    
                    # For non-Polish languages, we need to map filenames
                    if lang_code != 'pl':
                        # Map filename according to URL_MAP regardless of source
                        page_key = rel_path.replace('.html', '').replace('index', '')
                        if not page_key:  # homepage
                            page_key = ''
                            
                        mapped_path = None
                        if page_key in URL_MAP and lang_code in URL_MAP[page_key]:
                            mapped_filename = URL_MAP[page_key][lang_code]
                            if mapped_filename == 'index':
                                mapped_path = 'index.html'
                            elif '/' in mapped_filename:
                                mapped_path = f"{mapped_filename}.html"
                            else:
                                mapped_path = f"{mapped_filename}.html"
                        elif page_key == '':  # homepage special case
                            mapped_path = 'index.html'
                        
                        if mapped_path:
                            rel_path = mapped_path
                        else:
                            # Skip pages that don't have mapping for this language
                            continue
                    
                    out_path = build_page(src_path, rel_path, lang_code, translations.get(lang_code, {}))
                    rel_out = os.path.relpath(out_path, PUBLIC_DIR)
                    print(f'  ✅ {rel_out}')
                    count += 1
    
    print(f'\n✅ Built {count} pages → public/')

if __name__ == '__main__':
    main()
