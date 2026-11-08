import re

path = '_posts/2026-11-08-mobile-pentesting-guide-chapter-2.md'
content = open(path, encoding='utf-8').read()

emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
emojis = emoji_pattern.findall(content)
if emojis:
    print("Found emojis:", set(emojis))
else:
    print("Zero emojis in post:", path)

