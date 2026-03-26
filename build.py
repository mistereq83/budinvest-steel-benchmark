#!/usr/bin/env python3
"""Build Budinvest Steel site from partials + src → public/."""

import glob
import os
import re

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
PARTIALS_DIR = os.path.join(SITE_DIR, '_partials')
PUBLIC_DIR = os.path.join(SITE_DIR, 'public')
SITE_URL = 'https://budinvest-steel.com'

LANG_CONFIG = {
    'pl': {'partials_dir': PARTIALS_DIR, 'html_lang': 'pl', 'og_locale': 'pl_PL', 'prefix': ''},
    'en': {'partials_dir': os.path.join(PARTIALS_DIR, 'en'), 'html_lang': 'en', 'og_locale': 'en_GB', 'prefix': 'en'},
    'de': {'partials_dir': os.path.join(PARTIALS_DIR, 'de'), 'html_lang': 'de', 'og_locale': 'de_DE', 'prefix': 'de'},
}

PAGE_SPECS = [
    ('', {
        'pl': ('src/index.html', 'index.html'),
        'en': ('src/en/index.html', 'index.html'),
        'de': ('src/de/index.html', 'index.html'),
    }),
    ('o-nas', {
        'pl': ('src/o-nas.html', 'o-nas.html'),
        'en': ('src/en/o-nas.html', 'about.html'),
        'de': ('src/de/o-nas.html', 'ueber-uns.html'),
    }),
    ('uslugi', {
        'pl': ('src/uslugi.html', 'uslugi.html'),
        'en': ('src/en/uslugi.html', 'services.html'),
        'de': ('src/de/leistungen.html', 'leistungen.html'),
    }),
    ('uslugi/konstrukcje-stalowe', {
        'pl': ('src/uslugi/konstrukcje-stalowe.html', 'uslugi/konstrukcje-stalowe.html'),
        'en': ('src/en/uslugi/konstrukcje-stalowe.html', 'services/steel-structures.html'),
        'de': ('src/de/leistungen/stahlkonstruktionen.html', 'leistungen/stahlkonstruktionen.html'),
    }),
    ('uslugi/zbiorniki-cisnieniowe', {
        'pl': ('src/uslugi/zbiorniki-cisnieniowe.html', 'uslugi/zbiorniki-cisnieniowe.html'),
        'en': ('src/en/uslugi/zbiorniki-cisnieniowe.html', 'services/pressure-vessels.html'),
        'de': ('src/de/leistungen/druckbehaelter.html', 'leistungen/druckbehaelter.html'),
    }),
    ('uslugi/rurociagi-przemyslowe', {
        'pl': ('src/uslugi/rurociagi-przemyslowe.html', 'uslugi/rurociagi-przemyslowe.html'),
        'en': ('src/en/uslugi/rurociagi-przemyslowe.html', 'services/industrial-pipelines.html'),
        'de': ('src/de/leistungen/industrierohrleitungen.html', 'leistungen/industrierohrleitungen.html'),
    }),
    ('uslugi/obrobka-metali', {
        'pl': ('src/uslugi/obrobka-metali.html', 'uslugi/obrobka-metali.html'),
        'en': ('src/en/uslugi/obrobka-metali.html', 'services/metal-processing.html'),
        'de': ('src/de/leistungen/metallbearbeitung.html', 'leistungen/metallbearbeitung.html'),
    }),
    ('uslugi/prefabrykacja-betonu', {
        'pl': ('src/uslugi/prefabrykacja-betonu.html', 'uslugi/prefabrykacja-betonu.html'),
        'en': ('src/en/uslugi/prefabrykacja-betonu.html', 'services/concrete-prefabrication.html'),
        'de': ('src/de/leistungen/betonfertigteile.html', 'leistungen/betonfertigteile.html'),
    }),
    ('realizacje', {
        'pl': ('src/realizacje.html', 'realizacje.html'),
        'en': ('src/en/realizacje.html', 'projects.html'),
        'de': ('src/de/realizacje.html', 'projekte.html'),
    }),
    ('certyfikaty', {
        'pl': ('src/certyfikaty.html', 'certyfikaty.html'),
        'en': ('src/en/certyfikaty.html', 'certifications.html'),
        'de': ('src/de/certyfikaty.html', 'zertifikate.html'),
    }),
    ('park-maszynowy', {
        'pl': ('src/park-maszynowy.html', 'park-maszynowy.html'),
        'en': ('src/en/park-maszynowy.html', 'machinery.html'),
        'de': ('src/de/park-maszynowy.html', 'maschinenpark.html'),
    }),
    ('kariera', {
        'pl': ('src/kariera.html', 'kariera.html'),
        'en': ('src/en/kariera.html', 'careers.html'),
        'de': ('src/de/kariera.html', 'karriere.html'),
    }),
    ('kontakt', {
        'pl': ('src/kontakt.html', 'kontakt.html'),
        'en': ('src/en/kontakt.html', 'contact.html'),
        'de': ('src/de/kontakt.html', 'kontakt.html'),
    }),
]


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def parse_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, content
    meta = {}
    for line in match.group(1).strip().split('\n'):
        key, _, value = line.partition(':')
        if key:
            meta[key.strip()] = value.strip()
    return meta, content[match.end():]


def url_for(lang, output_rel):
    prefix = LANG_CONFIG[lang]['prefix']
    clean = output_rel.replace('index.html', '').replace('.html', '').rstrip('/')
    if lang == 'pl':
        path = clean
    else:
        path = f'{prefix}/{clean}'.rstrip('/')
    return SITE_URL if not path else f'{SITE_URL}/{path}'


def build_hreflang(route_specs):
    tags = []
    for lang in ('pl', 'en', 'de'):
        tags.append(f'    <link rel="alternate" hreflang="{lang}" href="{url_for(lang, route_specs[lang][1])}">')
    tags.append(f'    <link rel="alternate" hreflang="x-default" href="{url_for("pl", route_specs["pl"][1])}">')
    return '\n'.join(tags)


def build_switcher(route_specs, current_lang):
    items = [('pl', 'Polski', '🇵🇱'), ('en', 'English', '🇬🇧'), ('de', 'Deutsch', '🇩🇪')]
    links = []
    for lang, title, flag in items:
        href = url_for(lang, route_specs[lang][1]).replace(SITE_URL, '') or '/'
        active = ' active' if lang == current_lang else ''
        links.append(
            f'<a href="{href}" class="lang-flag{active}" hreflang="{lang}" lang="{lang}" title="{title}" aria-label="{title}">{flag}</a>'
        )
    return '\n        '.join(links)


def localized_partial(lang, filename):
    return read_file(os.path.join(LANG_CONFIG[lang]['partials_dir'], filename))


def prepare_head(head, canonical_url, hreflang_tags, og_locale):
    head = re.sub(r'<meta property="og:locale" content="[^"]+">', f'<meta property="og:locale" content="{og_locale}">', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{canonical_url}">\n{hreflang_tags}', head, count=1)
    return head


def build_page(route_specs, lang):
    src_rel, output_rel = route_specs[lang]
    src_path = os.path.join(SITE_DIR, src_rel)
    if not os.path.exists(src_path):
        raise FileNotFoundError(src_path)

    meta, body = parse_frontmatter(read_file(src_path))
    title = meta.get('title', 'Budinvest Steel')
    description = meta.get('description', '')
    nav_active = meta.get('nav_active', '')

    head = prepare_head(
        read_file(os.path.join(PARTIALS_DIR, '_head.html')),
        canonical_url=url_for(lang, output_rel),
        hreflang_tags=build_hreflang(route_specs),
        og_locale=LANG_CONFIG[lang]['og_locale'],
    )
    navbar = localized_partial(lang, '_navbar.html')
    mobile_menu = localized_partial(lang, '_mobile-menu.html')
    footer = localized_partial(lang, '_footer.html')
    scripts = read_file(os.path.join(PARTIALS_DIR, '_scripts.html'))
    noise = read_file(os.path.join(PARTIALS_DIR, '_noise.html'))

    navbar = navbar.replace(f'data-nav="{nav_active}"', f'data-nav="{nav_active}" class="active"', 1)
    mobile_menu = mobile_menu.replace(f'data-nav="{nav_active}"', f'data-nav="{nav_active}" class="active"', 1)
    switcher = build_switcher(route_specs, lang)
    navbar = navbar.replace('{{LANG_SWITCHER}}', switcher)
    mobile_menu = mobile_menu.replace('{{LANG_SWITCHER}}', switcher)

    html = f'''<!DOCTYPE html>
<html lang="{LANG_CONFIG[lang]["html_lang"]}">
<head>
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{url_for(lang, output_rel)}">
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

    out_rel = output_rel if lang == 'pl' else os.path.join(LANG_CONFIG[lang]['prefix'], output_rel)
    out_path = os.path.join(PUBLIC_DIR, out_rel)
    write_file(out_path, html)
    print(f'  ✅ {out_rel}')


def main():
    print('🔨 Building Budinvest Steel...')
    for f in glob.glob(os.path.join(PUBLIC_DIR, '**/*.html'), recursive=True):
        os.remove(f)

    count = 0
    for _, route_specs in PAGE_SPECS:
        for lang in ('pl', 'en', 'de'):
            build_page(route_specs, lang)
            count += 1

    print(f'\n✅ Built {count} pages → public/')


if __name__ == '__main__':
    main()
