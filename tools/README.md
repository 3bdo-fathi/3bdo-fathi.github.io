# Blog Maintenance & Automation Tools

This directory contains automation utilities, generators, and quality-assurance scripts used to maintain the blog's architecture, asset generation, and post standardization.

---

## Key Automation Scripts

### 1. `rebuild_all_covers.py`
The master cover generation engine. It generates unified, high-resolution Open Graph cover banners (`1200x630`) across all 34 technical posts with:
- Deep carbon background (`#0a0d13`) and subtle technical grid.
- Category-specific color accents (Reverse Engineering, Android Internals, Social Engineering, Vulnerability Research, AppSec, Automation).
- Topic pills and category badges.
- Standardized author signature: `Abdulrahman M. Fathi (0x3bdo)`.

```bash
python tools/rebuild_all_covers.py
```

### 2. `standardize_posts.py`
Audits and standardizes all post files in `_posts/`:
- Enforces uniform schema metadata (`author: Abdulrahman M. Fathi`, `toc: true`).
- Removes casual greetings to maintain an authoritative, technical tone.
- Eliminates redundant body image embeds that duplicate the front-matter hero banner.
- Appends the standardized author sign-off block.

```bash
python tools/standardize_posts.py
```

---

*Maintained by Abdulrahman M. Fathi (0x3bdo)*

