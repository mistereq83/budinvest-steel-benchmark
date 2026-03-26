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

mobile_match = re.search(r'(<div class="mobile-menu".*?</div>)', index_html, re.DOTALL)
if mobile_match:
    write_file(os.path.join(PARTIALS_DIR, '_mobile-menu.html'), mobile_match.group(1))

for root, dirs, files in os.walk(SRC_DIR):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            content = read_file(path)
            
            fm_match = re.search(r'^---.*?---\s*\n', content, re.DOTALL)
            fm = fm_match.group(0) if fm_match else ""
            
            # Find the actual body
            # It starts after <div class="mobile-menu" id="mobileMenu">...</div>
            # Let's find the closing tag of mobile menu
            mobile_start = content.find('<div class="mobile-menu"')
            if mobile_start != -1:
                mobile_end = content.find('</div>', mobile_start) + 6
                body_start = mobile_end
            else:
                body_start = len(fm)
            
            # Find the footer start
            footer_start = content.rfind('<footer')
            if footer_start != -1:
                body_content = content[body_start:footer_start].strip()
            else:
                body_content = content[body_start:].strip()
                
            body_content = body_content.replace('<div class="noise-overlay"></div>', '').strip()
            
            write_file(path, fm + body_content + "\n")

print("Refactor 3 complete.")
