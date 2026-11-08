import os, re

emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
found = False

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.jekyll-cache' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.md', '.yml', '.yaml', '.css', '.js')):
            path = os.path.join(root, f)
            try:
                content = open(path, encoding='utf-8').read()
                emojis = emoji_pattern.findall(content)
                if emojis:
                    print(f"Emoji in {path}: {set(emojis)}")
                    found = True
            except Exception:
                pass

if not found:
    print("Zero emojis found across all files.")

