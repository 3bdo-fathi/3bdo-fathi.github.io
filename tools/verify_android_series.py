import os
import re

posts = [f"_posts/2026-11-01-android-security-internals-chapter-{i}.md" for i in range(1, 14)]

emoji_pattern = re.compile(
    "[\U00010000-\U0010ffff]|"
    "[\u2600-\u27bf]|"
    "[\u2300-\u23ff]|"
    "[\u2b50\u2b55\u2934\u2935\u25aa\u25ab\u25fe\u25fd\u25fb\u25fc\u2049\u203c]"
)

errors = []

for p in posts:
    if not os.path.exists(p):
        errors.append(f"Missing post: {p}")
        continue
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for emojis
    emojis_found = emoji_pattern.findall(content)
    if emojis_found:
        errors.append(f"Found emojis in {p}: {emojis_found}")

    # Check Series Navigation table format
    nav_matches = re.findall(r"### Series Navigation[^\n]*\n([^\n]+)", content)
    for match in nav_matches:
        if match.strip() != "":
            errors.append(f"Header not followed by empty line in {p}: '{match}'")

    # Check cover image reference
    cover_match = re.search(r"path:\s*([^\n]+)", content)
    if cover_match:
        cover_path = cover_match.group(1).strip().lstrip("/")
        if not os.path.exists(cover_path):
            errors.append(f"Cover image missing for {p}: {cover_path}")

print("Validation Results:")
if errors:
    for e in errors:
        print("ERROR:", e)
else:
    print("ALL 13 CHAPTERS VALIDATED PERFECTLY! Zero emojis, valid navigation tables, and all covers exist.")
