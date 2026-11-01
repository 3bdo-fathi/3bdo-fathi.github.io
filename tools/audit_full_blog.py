import glob
import os
import re

posts = sorted(glob.glob("_posts/*.md"))
missing_images = []
posts_with_emojis = []

emoji_pattern = re.compile(
    "[\U00010000-\U0010ffff]|"
    "[\u2600-\u27bf]|"
    "[\u2300-\u23ff]|"
    "[\u2b50\u2b55\u2934\u2935\u25aa\u25ab\u25fe\u25fd\u25fb\u25fc\u2049\u203c]"
)

for p in posts:
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()

    # Emojis check
    emojis = emoji_pattern.findall(content)
    if emojis:
        posts_with_emojis.append((p, emojis))

    # Images check
    img_matches = re.findall(r'!\[.*?\]\((/assets/images/[^\s\)]+)\)', content)
    # Frontmatter image check
    fm_img = re.search(r'image:\s*\n\s*path:\s*(/assets/images/[^\s\n]+)', content)
    if fm_img:
        img_matches.append(fm_img.group(1))

    for img_path in img_matches:
        rel_path = img_path.lstrip("/")
        if not os.path.exists(rel_path):
            missing_images.append((p, rel_path))

print(f"Audited {len(posts)} posts.")
print(f"Posts with emojis: {len(posts_with_emojis)}")
if posts_with_emojis:
    for p, ems in posts_with_emojis:
        print(f"  {p}: {ems}")

print(f"\nMissing images: {len(missing_images)}")
if missing_images:
    for p, img in missing_images:
        print(f"  {p} -> {img}")
