import os, re

for f in sorted(os.listdir('_posts')):
    if f.endswith('.md'):
        c = open('_posts/' + f, encoding='utf-8').read()
        # strip yaml
        if c.startswith('---'):
            parts = c.split('---', 2)
            body = parts[2] if len(parts) > 2 else c
        else:
            body = c
        words = len(re.findall(r'\b\w+\b', body))
        read_time_int = max(1, words // 180)
        # what if ceil?
        read_time_ceil = max(1, (words + 179) // 180)
        print(f"{f[:45]:<45} | Words: {words:<5} | ReadTime: {read_time_int} min (ceil: {read_time_ceil})")

