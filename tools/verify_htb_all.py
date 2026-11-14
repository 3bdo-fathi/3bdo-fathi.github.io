import os
import glob
import re
from PIL import Image

post_files = sorted(glob.glob('_posts/*-htb-academy-*.md'))
print(f"Total HTB posts found: {len(post_files)}")

post_slugs = set()
for pf in post_files:
    fname = os.path.basename(pf)
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-|\.md$', '', fname)
    post_slugs.add(slug)

nav_errors = []
missing_images = []
flag_counts = {}
missing_covers = []
cover_dimensions_errors = []

for pf in post_files:
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nav links check
    nav_links = re.findall(r'href="(/posts/[^"]+/)"', content)
    for link in nav_links:
        target = link.strip('/').replace('posts/', '')
        if target not in post_slugs:
            nav_errors.append((pf, link, target))

    # Image check
    img_matches = re.findall(r'!\[.*?\]\((/assets/images/posts/htb-academy/[^\)]+)\)', content)
    for img in img_matches:
        local_path = img.lstrip('/')
        if not os.path.exists(local_path):
            missing_images.append((pf, img))

    # Cover image in frontmatter
    cover_match = re.search(r'path:\s*(/assets/images/posts/htb-academy/[^\s]+)', content)
    if cover_match:
        cover_path = cover_match.group(1).lstrip('/')
        if not os.path.exists(cover_path):
            missing_covers.append((pf, cover_path))
        else:
            try:
                im = Image.open(cover_path)
                if im.size != (1200, 630):
                    cover_dimensions_errors.append((cover_path, im.size))
            except Exception as e:
                cover_dimensions_errors.append((cover_path, str(e)))

    # Flags check
    flags = re.findall(r'\{\:\s*\.prompt-info\s*\}', content)
    flag_counts[pf] = len(flags)

print(f"Total unique post slugs: {len(post_slugs)}")
print(f"Series Nav link errors: {len(nav_errors)}")
if nav_errors:
    for e in nav_errors:
        print(f"  Nav error: {e}")

print(f"Missing images count: {len(missing_images)}")
if missing_images:
    for m in missing_images[:10]:
        print(f"  Missing img: {m}")

print(f"Missing covers: {len(missing_covers)}")
print(f"Cover dimension errors (expected 1200x630): {len(cover_dimensions_errors)}")
print(f"Total flag callouts verified: {sum(flag_counts.values())}")

