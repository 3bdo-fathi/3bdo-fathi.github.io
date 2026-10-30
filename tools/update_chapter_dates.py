import os
import re

posts_dir = "_posts"
times = [
    (1, "09:00:00"),
    (2, "10:00:00"),
    (3, "11:00:00"),
    (4, "12:00:00"),
    (5, "13:00:00"),
    (6, "14:00:00"),
    (7, "15:00:00"),
    (8, "16:00:00"),
    (9, "17:00:00")
]

for ch_num, time_str in times:
    # Find existing file for this chapter
    pattern = f"social-engineering-art-of-human-hacking-chapter-{ch_num}.md"
    matched_file = None
    for fname in os.listdir(posts_dir):
        if fname.endswith(pattern):
            matched_file = fname
            break
            
    if not matched_file:
        print(f"File for chapter {ch_num} not found!")
        continue
        
    old_path = os.path.join(posts_dir, matched_file)
    new_fname = f"2026-10-29-social-engineering-art-of-human-hacking-chapter-{ch_num}.md"
    new_path = os.path.join(posts_dir, new_fname)
    
    with open(old_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace date: in front matter
    new_date_line = f"date: 2026-10-29 {time_str} +0300"
    content = re.sub(r"date:.*", new_date_line, content, count=1)
    
    with open(old_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    if old_path != new_path:
        os.rename(old_path, new_path)
        print(f"Renamed {matched_file} -> {new_fname}")
    else:
        print(f"Updated date in {new_fname}")

print("All dates and filenames updated to 2026-10-29 successfully!")
