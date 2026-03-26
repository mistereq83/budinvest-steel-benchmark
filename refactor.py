import os, re, glob, shutil

SITE_DIR = '/Users/ray/clawd/projects/budinvest-steel/site'
PUBLIC_DIR = os.path.join(SITE_DIR, 'public')
SRC_DIR = os.path.join(SITE_DIR, 'src')
PARTIALS_DIR = os.path.join(SITE_DIR, '_partials')

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(os.path.join(SRC_DIR, 'uslugi'), exist_ok=True)
os.makedirs(PARTIALS_DIR, exist_ok=True)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

index_html = read_file(os.path.join(PUBLIC_DIR, 'index.html'))

# Extract Head
head_match = re.search(r'(<meta charset="UTF-8">.*?</style>)', index_html, re.DOTALL)
if head_match:
    head = head_match.group(1)
    head = head.replace('<title>', '<!-- TITLE i DESCRIPTION będą per-strona -->\n<!-- <title>')
    # We need to clean up title and desc as they are dynamic, and add optimizations
    head = re.sub(r'<title>.*?</title>\n\s*<meta name="description" content=".*?">', '', head, flags=re.DOTALL)
    
    # Add preloads and changes
    head = head.replace('<!-- Google Fonts -->', '<!-- Google Fonts -->\n    <link rel="dns-prefetch" href="https://fonts.googleapis.com">\n    <link rel="preload" href="https://fonts.gstatic.com" as="font" type="font/woff2" crossorigin>\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">')
    head = head.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>')
    head = head.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>')
    head += "\n<!-- GTM (placeholder - odkomentuj gdy gotowy) -->\n<!-- Google Tag Manager -->\n<!--\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>\n-->\n"
    
    write_file(os.path.join(PARTIALS_DIR, '_head.html'), head)

# Extract Noise
write_file(os.path.join(PARTIALS_DIR, '_noise.html'), '<div class="noise-overlay"></div>')

# Extract Navbar
nav_match = re.search(r'(<nav class="navbar.*?</nav>)', index_html, re.DOTALL)
if nav_match:
    navbar = nav_match.group(1)
    # Replace active classes with template tags manually later, for now we will assume the build script does it
    write_file(os.path.join(PARTIALS_DIR, '_navbar.html'), navbar)

# Extract Mobile Menu
mobile_match = re.search(r'(<div class="mobile-menu.*?</nav>\n    </div>)', index_html, re.DOTALL)
if mobile_match:
    write_file(os.path.join(PARTIALS_DIR, '_mobile-menu.html'), mobile_match.group(1))

# Extract Footer
footer_match = re.search(r'(<footer.*</footer>)', index_html, re.DOTALL)
if footer_match:
    write_file(os.path.join(PARTIALS_DIR, '_footer.html'), footer_match.group(1))

# Extract Scripts
scripts_match = re.search(r'(<script>\s*document\.addEventListener.*?)</script>', index_html, re.DOTALL)
if scripts_match:
    s = scripts_match.group(1) + "</script>\n\n<!-- GTM noscript (placeholder) -->\n<!-- <noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX\" height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript> -->"
    write_file(os.path.join(PARTIALS_DIR, '_scripts.html'), s)


for root, dirs, files in os.walk(PUBLIC_DIR):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, PUBLIC_DIR)
            content = read_file(path)
            
            # Extract Title and Description
            title = re.search(r'<title>(.*?)</title>', content).group(1) if re.search(r'<title>(.*?)</title>', content) else "Budinvest Steel"
            desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
            desc = desc_match.group(1) if desc_match else ""
            
            nav_active = rel_path.replace('.html', '')
            if nav_active == 'index': nav_active = 'home'
            if 'uslugi/' in nav_active: nav_active = 'uslugi'
            
            # Extract body (everything between mobile menu and footer)
            # Find end of mobile menu
            mobile_end = content.find('</div>', content.find('<div class="mobile-menu')) + 6 # very rough
            # actually let's use regex to extract everything between </nav>\n    </div> and <footer>
            body_match = re.search(r'</nav>\s*</div>\s*(.*?)<footer', content, re.DOTALL)
            if body_match:
                body = body_match.group(1).strip()
            else:
                body = content # fallback
            
            # Remove noise
            body = body.replace('<div class="noise-overlay"></div>', '').strip()
            
            frontmatter = f"---\ntitle: {title}\ndescription: {desc}\nnav_active: {nav_active}\n---\n\n"
            write_file(os.path.join(SRC_DIR, rel_path), frontmatter + body)

print("Extraction complete.")
