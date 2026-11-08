import glob
import re
import os

posts = sorted(glob.glob('_posts/*.md'))
print(f"Total posts to standardize: {len(posts)}")

for p in posts:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Front Matter Processing
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"Skipping malformed file: {p}")
        continue
        
    front_matter = parts[1]
    body = parts[2]
    
    # Standardize author in schema
    if 'schema:' in front_matter:
        front_matter = re.sub(
            r'schema:\s*\n\s*type:\s*Article\s*\n\s*author:\s*.*?\n',
            'schema:\n  type: Article\n  author: Abdulrahman M. Fathi\n',
            front_matter
        )
    else:
        # Add schema block before ending of front matter
        schema_block = "toc: true\nschema:\n  type: Article\n  author: Abdulrahman M. Fathi\n"
        if 'toc: true' not in front_matter:
            front_matter = front_matter.rstrip() + "\n" + schema_block
        else:
            front_matter = front_matter.replace("toc: true", "toc: true\nschema:\n  type: Article\n  author: Abdulrahman M. Fathi")

    if 'toc: true' not in front_matter:
        front_matter = front_matter.rstrip() + "\ntoc: true\n"

    # Standardize author field if present
    front_matter = re.sub(r'author:\s*Abdulrahman Mohamed', 'author: Abdulrahman M. Fathi', front_matter)

    # 2. Body Processing
    # Remove casual greetings
    body = re.sub(r'Hello everyone,\s*\n+', '', body, flags=re.IGNORECASE)
    body = re.sub(r"I hope you're doing well and having a great day\.\s*\n+", '', body, flags=re.IGNORECASE)
    body = re.sub(r"In today's article, (we'll|I'd like to|we will) explore a topic that I found both interesting and worth sharing\..*?Let's get started\.\s*\n+", '', body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"Let's get started\.\s*\n+", '', body, flags=re.IGNORECASE)

    # Remove duplicate cover image embed in body (e.g. ![...](/assets/images/posts/...cover.png))
    body = re.sub(r'!\[.*?\]\(/assets/images/posts/.*?/.*?cover\.png\)\s*\n+', '', body)

    # Standardize sign-off at bottom
    # Remove old sign-offs
    body = re.sub(r'\*?[-—]\s*Abdulrahman (Mohamed|M\. Fathi)\*?', '', body)
    body = re.sub(r'## Let\'s Connect\s*\n+Have a question.*?Contact Page\(/contact-me/\)\s*', '', body, flags=re.DOTALL)
    
    # Strip trailing whitespace and ensure standard footer
    body = body.rstrip()
    
    standard_footer = "\n\n---\n\n*Author: Abdulrahman M. Fathi (0x3bdo) • Cyber Security Engineer & Penetration Tester*\n"
    if not body.endswith("*Author: Abdulrahman M. Fathi (0x3bdo) • Cyber Security Engineer & Penetration Tester*"):
        body += standard_footer

    # Clean multiple consecutive blank lines
    body = re.sub(r'\n{3,}', '\n\n', body)

    new_content = f"---{front_matter.rstrip()}\n---\n{body.lstrip()}"

    with open(p, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Standardized: {os.path.basename(p)}")

print("\nAll posts standardized successfully!")

