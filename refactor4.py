import os, re

SITE_DIR = '/Users/ray/clawd/projects/budinvest-steel/site'
SRC_DIR = os.path.join(SITE_DIR, 'src')
PARTIALS_DIR = os.path.join(SITE_DIR, '_partials')

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

index_html = read_file(os.path.join(SRC_DIR, 'index.html'))
index_html = re.sub(r'^---.*?---\s*\n', '', index_html, flags=re.DOTALL)

nav_match = re.search(r'(<nav class="navbar".*?</nav>)', index_html, re.DOTALL)
if nav_match:
    write_file(os.path.join(PARTIALS_DIR, '_navbar.html'), nav_match.group(1))
else:
    print("NAV_MATCH FAILED")
