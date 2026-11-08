import re

path = '_tabs/about.md'
content = open(path, encoding='utf-8').read()

emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
emojis = emoji_pattern.findall(content)
if emojis:
    print("Found emojis:", set(emojis))
else:
    print("Zero emojis in _tabs/about.md")

