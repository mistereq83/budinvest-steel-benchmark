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

# Remove frontmatter from index_html string for extraction
index_html = re.sub(r'^---.*?---\s*\n', '', index_html, flags=re.DOTALL)

# Extract Navbar
nav_match = re.search(r'(<nav class="navbar.*?</nav>)', index_html, re.DOTALL)
if nav_match: write_file(os.path.join(PARTIALS_DIR, '_navbar.html'), nav_match.group(1))

# Extract Mobile Menu
mobile_match = re.search(r'(<div class="mobile-menu.*?</nav>\n    </div>)', index_html, re.DOTALL)
if mobile_match: write_file(os.path.join(PARTIALS_DIR, '_mobile-menu.html'), mobile_match.group(1))

# Extract Scripts
scripts_match = re.search(r'(<script>\s*document\.addEventListener.*?)</script>', index_html, re.DOTALL)
if scripts_match:
    s = scripts_match.group(1) + "</script>\n\n<!-- GTM noscript (placeholder) -->\n<!-- <noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX\" height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript> -->"
    write_file(os.path.join(PARTIALS_DIR, '_scripts.html'), s)

# Clean up all src files
for root, dirs, files in os.walk(SRC_DIR):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            content = read_file(path)
            
            # Preserve frontmatter
            frontmatter_match = re.search(r'^---.*?---\s*\n', content, re.DOTALL)
            fm = frontmatter_match.group(0) if frontmatter_match else ""
            
            # Find the actual body content between mobile menu and footer
            # A more robust regex:
            # Look for everything after </nav>\s*</div> (mobile menu end)
            # and before <footer
            body_match = re.search(r'</nav>\s*</div>\s*(.*?)<footer', content, re.DOTALL)
            if body_match:
                body = body_match.group(1).strip()
                # remove <div class="noise-overlay"></div> if it's there
                body = body.replace('<div class="noise-overlay"></div>', '').strip()
                write_file(path, fm + body + "\n")
            else:
                print(f"Could not parse body for {path}")

print("Refactor 2 complete.")
