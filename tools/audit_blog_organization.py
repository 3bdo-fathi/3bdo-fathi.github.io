import glob
import re
import os

posts = sorted(glob.glob("_posts/*.md"))
print(f"Total posts: {len(posts)}\n")
print(f"{'Date':<12} | {'Filename':<45} | {'Categories':<35} | {'Title'}")
print("-" * 130)

for p in posts:
    fname = os.path.basename(p)
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    
    title_match = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
    title = title_match.group(1) if title_match else "No Title"
    
    date_match = re.search(r'date:\s*([0-9\-]+)', content)
    date = date_match.group(1) if date_match else "No Date"
    
    cats_match = re.search(r'categories:\s*\[(.*?)\]', content)
    cats = cats_match.group(1) if cats_match else "None"
    
    print(f"{date:<12} | {fname:<45} | {cats:<35} | {title[:40]}")

