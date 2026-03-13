#!/usr/bin/env python3
"""Replace broken/random Unsplash URLs with verified, thematically correct industrial photos."""

import re, os, glob

# Verified working Unsplash photos — industrial/steel/welding/construction
PHOTOS = {
    # Hero backgrounds (wide, dramatic)
    'hero': [
        'photo-1504917595217-d4dc5ebe6122',  # industrial warehouse interior
        'photo-1565008447742-97f6f38c985c',  # steel mill / factory dark
        'photo-1513828583688-c52646db42da',  # industrial pipes/refinery
        'photo-1486406146926-c627a92ad1ab',  # modern building architecture
    ],
    # Welding / sparks
    'welding': [
        'photo-1504328345606-18bbc8c9d7d1',  # welder at work sparks
        'photo-1605296867304-46d5465a13f1',  # welding closeup
        'photo-1581092162384-8987c1d64718',  # welding sparks flying
        'photo-1623018035782-b269248df916',  # industrial welding
    ],
    # Steel structures / construction
    'steel': [
        'photo-1517420879524-86d64ac2f339',  # steel beams construction
        'photo-1581091226825-a6a2a5aee158',  # steel structure / technology
        'photo-1587293852726-70cdb56c2866',  # metal texture closeup
        'photo-1585771724684-38269d6639fd',  # industrial machinery
    ],
    # Factory / industrial
    'factory': [
        'photo-1567789884554-0b844b597180',  # factory interior
        'photo-1590959651373-a3db0f38a961',  # industrial plant
        'photo-1621905252507-b35492cc74b4',  # heavy machinery
        'photo-1533106497176-45ae19e68ba2',  # industrial engineering
    ],
}

# Flatten all verified IDs
ALL_PHOTOS = []
for cat in ['hero', 'welding', 'steel', 'factory']:
    ALL_PHOTOS.extend(PHOTOS[cat])

def make_url(photo_id, width=1920, quality=80):
    return f'https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={width}&q={quality}'

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Find all Unsplash image URLs
    # Match patterns like: https://images.unsplash.com/photo-XXXXX?...
    # Also match: https://source.unsplash.com/...
    
    unsplash_pattern = r'https?://(?:images\.unsplash\.com|source\.unsplash\.com)[^\s\'")\]]*'
    matches = list(re.finditer(unsplash_pattern, content))
    
    if not matches:
        print(f'  No Unsplash URLs found in {os.path.basename(filepath)}')
        return False
    
    print(f'  Found {len(matches)} Unsplash URLs in {os.path.basename(os.path.dirname(filepath))}')
    
    # Replace each URL with a verified one, cycling through categories
    replacements = []
    photo_index = 0
    
    for i, match in enumerate(matches):
        old_url = match.group(0)
        
        # Determine size based on context (hero = large, cards = medium, gallery = medium)
        # Check surrounding context
        start = max(0, match.start() - 200)
        context = content[start:match.start()].lower()
        
        if 'hero' in context or 'background' in context or 'bg' in context:
            cat_photos = PHOTOS['hero']
            width = 1920
        elif 'weld' in context or 'spaw' in context:
            cat_photos = PHOTOS['welding']
            width = 1200
        elif 'steel' in context or 'stal' in context or 'konstru' in context:
            cat_photos = PHOTOS['steel']
            width = 1200
        else:
            cat_photos = ALL_PHOTOS
            width = 1200
        
        photo_id = cat_photos[i % len(cat_photos)]
        new_url = make_url(photo_id, width)
        replacements.append((old_url, new_url))
    
    # Apply replacements
    for old_url, new_url in replacements:
        content = content.replace(old_url, new_url, 1)
    
    # Also fix any placehold.co or placeholder URLs
    content = re.sub(
        r'https?://placehold\.co/[^\s\'")\]]*',
        lambda m: make_url(ALL_PHOTOS[hash(m.group()) % len(ALL_PHOTOS)], 800),
        content
    )
    
    # Fix source.unsplash.com (deprecated) if any remain
    content = re.sub(
        r'https://source\.unsplash\.com/\d+x\d+/\?[^\s\'")\]]*',
        lambda m: make_url(ALL_PHOTOS[hash(m.group()) % len(ALL_PHOTOS)], 1200),
        content
    )
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'  ✅ Fixed {len(replacements)} URLs')
        return True
    return False

# Process all variant files
design_dir = os.path.dirname(os.path.abspath(__file__))
variants = sorted(glob.glob(os.path.join(design_dir, 'variant-*/index.html')))

fixed = 0
for v in variants:
    if fix_file(v):
        fixed += 1

print(f'\n🎯 Fixed {fixed}/{len(variants)} files')
