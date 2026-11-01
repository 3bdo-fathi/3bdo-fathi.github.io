import os
import shutil
import re

# 1. Rename image with space
old_img = os.path.join("assets", "images", "Reconnaissance Framework.jpg")
new_img = os.path.join("assets", "images", "reconnaissance-framework.jpg")
if os.path.exists(old_img):
    shutil.move(old_img, new_img)
    print(f"Renamed {old_img} -> {new_img}")

# 2. Update post referencing this image
p_recon = "_posts/2026-05-20-building-recon-dns-enumeration-framework.md"
if os.path.exists(p_recon):
    with open(p_recon, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("Reconnaissance Framework.jpg", "reconnaissance-framework.jpg")
    with open(p_recon, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated image path in {p_recon}")

# 3. Standardize Cloudflare categories
p_cf = "_posts/2026-06-02-understanding-how-cloudflare-really-works.md"
if os.path.exists(p_cf):
    with open(p_cf, "r", encoding="utf-8") as f:
        content = f.read()
    # Replace YAML list categories with single line [Cyber Security, Network Security]
    content = re.sub(
        r"categories:\s*\n\s*-\s*Cyber Security\s*\n\s*-\s*Network Engineering\s*\n\s*-\s*Infrastructure",
        "categories: [Cyber Security, Network Security]",
        content
    )
    with open(p_cf, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Standardized categories in {p_cf}")

# 4. Standardize AppSec categories
p_appsec = "_posts/2026-08-31-sast-dast-iast-rasp-complete-guide.md"
if os.path.exists(p_appsec):
    with open(p_appsec, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        "categories: [Cyber Security, Application Security, DevSecOps]",
        "categories: [Cyber Security, Application Security]"
    )
    with open(p_appsec, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Standardized categories in {p_appsec}")

# 5. Standardize Research -> Cyber Security
p_threat = "_posts/2025-01-01-threat-intelligence-research.md"
if os.path.exists(p_threat):
    with open(p_threat, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        "categories: [Research, Threat Intelligence]",
        "categories: [Cyber Security, Threat Intelligence]"
    )
    with open(p_threat, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Standardized categories in {p_threat}")

p_vuln = "_posts/2025-01-01-vulnerabilities-research.md"
if os.path.exists(p_vuln):
    with open(p_vuln, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        "categories: [Research, Vulnerabilities]",
        "categories: [Cyber Security, Vulnerability Research]"
    )
    with open(p_vuln, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Standardized categories in {p_vuln}")

p_int3x = "_posts/2026-05-28-from-dark-web-fame-to-digital-attribution.md"
if os.path.exists(p_int3x):
    with open(p_int3x, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        "categories: [Research, Security News]",
        "categories: [Cyber Security, Threat Intelligence]"
    )
    with open(p_int3x, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Standardized categories in {p_int3x}")

# 6. Align Python recon date
p_pyrecon = "_posts/2025-10-30-mastering-information-gathering-python-automation.md"
if os.path.exists(p_pyrecon):
    with open(p_pyrecon, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        "date: 2025-05-30 16:03:00 +0300",
        "date: 2025-10-30 16:03:00 +0300"
    )
    with open(p_pyrecon, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Aligned date in {p_pyrecon}")

# 7. Rename Contact Me.md to contact.md
old_contact = os.path.join("_tabs", "Contact Me.md")
new_contact = os.path.join("_tabs", "contact.md")
if os.path.exists(old_contact):
    shutil.move(old_contact, new_contact)
    print(f"Renamed {old_contact} -> {new_contact}")

print("\nBlog organization script executed successfully!")
