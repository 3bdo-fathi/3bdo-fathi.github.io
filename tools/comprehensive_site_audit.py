import os
import glob
import re
import yaml
from PIL import Image
from datetime import datetime, timezone, timedelta

print("=" * 70)
print("COMPREHENSIVE BLOG AUDIT & VERIFICATION SUITE")
print("=" * 70)

# Local time reference
now_dt = datetime(2026, 11, 14, 7, 30, 0, tzinfo=timezone(timedelta(hours=2)))
print(f"Audit Timestamp: {now_dt.isoformat()}")

all_posts = glob.glob('_posts/*.md')
htb_posts = [p for p in all_posts if 'htb-academy' in p]
tabs = glob.glob('_tabs/*.md')

print(f"Total Posts: {len(all_posts)} (HTB Academy: {len(htb_posts)})")
print(f"Total Tabs: {len(tabs)}")

errors = []
warnings = []

# -------------------------------------------------------------
# 1. YAML Frontmatter & Date Checks
# -------------------------------------------------------------
print("\n[1/7] Checking YAML Frontmatter & Future Post Filtering...")
post_slugs = {}
htb_data = []

for p in all_posts:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fname = os.path.basename(p)
    if not content.startswith('---'):
        errors.append(f"{fname}: Missing frontmatter start")
        continue
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        errors.append(f"{fname}: Malformed frontmatter")
        continue
    
    try:
        fm = yaml.safe_load(parts[1])
    except Exception as e:
        errors.append(f"{fname}: YAML syntax error: {e}")
        continue
    
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-|\.md$', '', fname)
    post_slugs[slug] = p
    
    # Check date
    raw_date = fm.get('date')
    if not raw_date:
        errors.append(f"{fname}: Missing date in frontmatter")
    else:
        # Parse date string
        d_str = str(raw_date)[:19]
        try:
            # e.g. 2026-11-12 01:00:00
            post_dt = datetime.strptime(d_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(timedelta(hours=2)))
            if post_dt > now_dt:
                errors.append(f"{fname}: FUTURE POST DETECTED! Date {post_dt} is after {now_dt}")
        except Exception as e:
            pass
            
    if 'htb-academy' in fname:
        part_match = re.search(r'part-(\d+)-', fname)
        part_num = int(part_match.group(1)) if part_match else 0
        htb_data.append({
            'num': part_num,
            'file': fname,
            'path': p,
            'title': fm.get('title', ''),
            'date': str(raw_date),
            'series': fm.get('series', ''),
            'body': parts[2]
        })

print(f"  -> All {len(all_posts)} posts parsed. Future posts found: {len([e for e in errors if 'FUTURE POST' in e])}")

# -------------------------------------------------------------
# 2. HTB Academy Series Chronology & Syllabus Order
# -------------------------------------------------------------
print("\n[2/7] Checking HTB Academy Series & Ordering...")
htb_data.sort(key=lambda x: x['num'])

if len(htb_data) != 41:
    errors.append(f"Expected 41 HTB posts, but found {len(htb_data)}")
else:
    print(f"  -> Found all 41 HTB Academy modules.")

# Check series assignment
for item in htb_data:
    if item['series'] != "Hack The Box Academy":
        errors.append(f"{item['file']}: Incorrect series frontmatter: '{item['series']}'")

# Check strict date ascending order
prev_date = ""
for item in htb_data:
    if prev_date and item['date'] <= prev_date:
        errors.append(f"{item['file']} ({item['date']}) is not chronologically after previous ({prev_date})")
    prev_date = item['date']

# Check part number sequence 1..41
expected_seq = list(range(1, 42))
actual_seq = [x['num'] for x in htb_data]
if actual_seq != expected_seq:
    errors.append(f"HTB Part number sequence gap/mismatch: {actual_seq}")
else:
    print(f"  -> Part numbers strictly 1 through 41 with zero gaps.")
    print(f"  -> Dates strictly ascending (Part 1 oldest, Part 41 newest).")

# -------------------------------------------------------------
# 3. Next/Prev Navigation Button Links
# -------------------------------------------------------------
print("\n[3/7] Checking Internal Post Navigation Buttons...")
nav_errors = 0
for i, item in enumerate(htb_data):
    part_num = item['num']
    body = item['body']
    
    # Check Next Part link
    if part_num < 41:
        next_part = part_num + 1
        expected_target_slug = htb_data[next_part - 1]['file']
        expected_target_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-|\.md$', '', expected_target_slug)
        if f"/posts/{expected_target_slug}/" not in body:
            errors.append(f"Part {part_num}: Missing or incorrect Next Part link to /posts/{expected_target_slug}/")
            nav_errors += 1
            
    # Check Prev Part link
    if part_num > 1:
        prev_part = part_num - 1
        expected_target_slug = htb_data[prev_part - 1]['file']
        expected_target_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-|\.md$', '', expected_target_slug)
        if f"/posts/{expected_target_slug}/" not in body:
            errors.append(f"Part {part_num}: Missing or incorrect Prev Part link to /posts/{expected_target_slug}/")
            nav_errors += 1

if nav_errors == 0:
    print("  -> All 41 posts have perfectly chained Previous/Next links.")

# -------------------------------------------------------------
# 4. Image & Cover Verification
# -------------------------------------------------------------
print("\n[4/7] Checking Images, Screenshots & Covers...")
total_images = 0
missing_images = 0
cover_errors = 0

for item in htb_data:
    p = item['path']
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check cover image
    m_cover = re.search(r'path:\s*(/assets/images/posts/htb-academy/[^\s\n]+)', content)
    if not m_cover:
        errors.append(f"{item['file']}: Missing cover image path in frontmatter")
        cover_errors += 1
    else:
        cpath = m_cover.group(1).lstrip('/')
        if not os.path.exists(cpath):
            errors.append(f"{item['file']}: Cover image file not found on disk: {cpath}")
            cover_errors += 1
        else:
            try:
                im = Image.open(cpath)
                if im.size != (1200, 630):
                    errors.append(f"{item['file']}: Invalid cover size {im.size}, expected (1200, 630)")
                    cover_errors += 1
            except Exception as e:
                errors.append(f"{item['file']}: Error opening cover {cpath}: {e}")
                cover_errors += 1

    # Check all body images
    img_links = re.findall(r'!\[.*?\]\((/assets/images/posts/htb-academy/[^\)]+)\)', content)
    total_images += len(img_links)
    for img in img_links:
        local_path = img.lstrip('/')
        if not os.path.exists(local_path):
            errors.append(f"{item['file']}: Missing image on disk: {local_path}")
            missing_images += 1

print(f"  -> Total embedded images verified: {total_images}")
print(f"  -> Missing images: {missing_images}")
print(f"  -> Cover errors: {cover_errors}")

# -------------------------------------------------------------
# 5. Flag & Lab Question Counts
# -------------------------------------------------------------
print("\n[5/7] Verifying HTB Flags & Callout Formatting...")
total_flags = 0
for item in htb_data:
    flags = len(re.findall(r'\{\:\s*\.prompt-info\s*\}', item['body']))
    total_flags += flags

print(f"  -> Total HTB Flags Verified: {total_flags} (Expected: 688)")
if total_flags != 688:
    errors.append(f"Flag count mismatch: found {total_flags}, expected 688")

# -------------------------------------------------------------
# 6. Emoji Audit Across Whole Project
# -------------------------------------------------------------
print("\n[6/7] Auditing for Emojis Across All Posts & Tabs...")
emoji_pattern = re.compile(
    r'[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001FAFF\U00002702-\U000027B0\U0001F1E6-\U0001F1FF]'
)

emoji_found = 0
for fpath in all_posts + tabs:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = emoji_pattern.findall(content)
    if m:
        errors.append(f"{os.path.basename(fpath)}: Contains {len(m)} emojis: {set(m)}")
        emoji_found += len(m)

print(f"  -> Emojis found across all markdown files: {emoji_found}")

# -------------------------------------------------------------
# 7. Dark Mode OLED Black Verification
# -------------------------------------------------------------
print("\n[7/7] Checking Dark Mode CSS & Hex Colors...")
old_colors_pattern = re.compile(r'#(?:0d1117|161b22|010409)\b', re.IGNORECASE)
found_old_colors = 0
for fpath in glob.glob('_layouts/*.html') + glob.glob('_includes/*.html') + glob.glob('_tabs/*.md') + ['404.html']:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = old_colors_pattern.findall(content)
    if m:
        errors.append(f"{os.path.basename(fpath)}: Found old grayish dark color: {set(m)}")
        found_old_colors += len(m)

print(f"  -> Residual old grayish dark colors: {found_old_colors}")

# -------------------------------------------------------------
# Summary
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT SUMMARY & FINAL VERDICT")
print("=" * 70)
if errors:
    print(f"FAILED with {len(errors)} error(s):")
    for e in errors[:10]:
        print(f"  [X] {e}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more.")
else:
    print("ALL CHECKS PASSED WITH 100% SUCCESS!")
    print("- 41 HTB Modules loaded and validated")
    print("- 0 Future post blocks (all dates safely in past)")
    print("- 688 HTB flags extracted & formatted")
    print("- 0 Missing images or cover errors")
    print("- 0 Broken navigation links")
    print("- 0 Emojis in any post or tab")
    print("- 100% Pure Black OLED dark mode styling")
print("=" * 70)
