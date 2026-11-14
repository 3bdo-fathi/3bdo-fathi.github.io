import glob
import re

post_files = sorted(glob.glob('_posts/*.md'))
print(f"Total posts to process: {len(post_files)}")

total_emojis_removed = 0
modified_files = 0

for pf in post_files:
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    # Specific cleanups for HTB questions and flags
    new_content = new_content.replace('> 🎯 **Lab Question', '> **Lab Question')
    new_content = new_content.replace('> 🚩 **Flag / Answer', '> **Flag / Answer')

    # Remove any stray target or flag or other emojis
    # List of known emojis to strip: 🎯, 🚩, 🚀, 🛡️, 🔍, 📊, ⚡, 💡, 📌, ⚠️, 🛠️, etc.
    stray_emojis = ['🎯', '🚩', '🚀', '🛡️', '🛡', '🔍', '📊', '⚡', '💡', '📌', '⚠️', '🛠️', '🛠', '✨', '🔥', '✅', '❌', '👉', '👇']
    for em in stray_emojis:
        new_content = new_content.replace(em, '')

    if new_content != content:
        with open(pf, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified_files += 1

print(f"Successfully cleaned emojis from {modified_files} posts!")

