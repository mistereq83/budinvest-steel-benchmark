#!/usr/bin/env python3
"""Build Budinvest Steel site from partials + src → public/"""

import os, re, glob, shutil

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SITE_DIR, 'src')
PARTIALS_DIR = os.path.join(SITE_DIR, '_partials')
PUBLIC_DIR = os.path.join(SITE_DIR, 'public')

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def parse_frontmatter(content):
    """Parse YAML-like frontmatter between --- markers"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, content
    meta = {}
    for line in match.group(1).strip().split('\n'):
        key, _, value = line.partition(':')
        meta[key.strip()] = value.strip()
    body = content[match.end():]
    return meta, body

def build_page(src_path, rel_path):
    content = read_file(src_path)
    meta, body = parse_frontmatter(content)
    
    title = meta.get('title', 'Budinvest Steel')
    description = meta.get('description', '')
    nav_active = meta.get('nav_active', '')
    
    # Load partials
    head = read_file(os.path.join(PARTIALS_DIR, '_head.html'))
    navbar = read_file(os.path.join(PARTIALS_DIR, '_navbar.html'))
    mobile_menu = read_file(os.path.join(PARTIALS_DIR, '_mobile-menu.html'))
    footer = read_file(os.path.join(PARTIALS_DIR, '_footer.html'))
    scripts = read_file(os.path.join(PARTIALS_DIR, '_scripts.html'))
    noise = read_file(os.path.join(PARTIALS_DIR, '_noise.html'))
    
    # Replace nav active class
    navbar = navbar.replace(f'data-nav="{nav_active}"', f'data-nav="{nav_active}" class="active"')
    mobile_menu = mobile_menu.replace(f'data-nav="{nav_active}"', f'data-nav="{nav_active}" class="active"')
    
    # Build canonical URL
    page_path = rel_path.replace('index.html', '').replace('.html', '')
    if page_path:
        canonical_url = f'https://budinvest-steel.com/{page_path}'
    else:
        canonical_url = 'https://budinvest-steel.com'
    
    # Assemble
    html = f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
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
    
    out_path = os.path.join(PUBLIC_DIR, rel_path)
    write_file(out_path, html)
    print(f'  ✅ {rel_path}')

def main():
    print('🔨 Building Budinvest Steel...')
    
    # Clean public (only html files, keep images etc)
    for f in glob.glob(os.path.join(PUBLIC_DIR, '**/*.html'), recursive=True):
        os.remove(f)
    
    # Build all src html files
    count = 0
    for root, dirs, files in os.walk(SRC_DIR):
        for fname in files:
            if fname.endswith('.html'):
                src_path = os.path.join(root, fname)
                rel_path = os.path.relpath(src_path, SRC_DIR)
                build_page(src_path, rel_path)
                count += 1
    
    print(f'\n✅ Built {count} pages → public/')

if __name__ == '__main__':
    main()
