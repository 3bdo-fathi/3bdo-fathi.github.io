with open("_layouts/post.html", "r", encoding="utf-8") as f:
    c = f.read()

target = "    {% if page.tags.size > 0 %}"
replacement = """    <!-- Sadaqah Jariyah & Enduring Knowledge Box -->
    <div class="post-dedication-box my-4 p-3 rounded" style="background: rgba(88, 166, 255, 0.05); border: 1px solid rgba(88, 166, 255, 0.2); font-size: 0.88rem; line-height: 1.6;">
      <div class="d-flex align-items-center gap-2 mb-1" style="color: #58a6ff; font-weight: 600;">
        <i class="fas fa-book-reader"></i>
        <span>Sadaqah Jariyah & Knowledge Sharing | صدقة جارية وعلم يُنتفع به</span>
      </div>
      <p class="mb-0 text-muted" style="font-size: 0.84rem;">
        This technical content and everything shared across this blog is dedicated with sincere intention to serve as enduring, beneficial knowledge (علم يُنتفع به) and an ongoing charity (صدقة جارية). If you find value in this research, please remember me and my family in your sincere prayers.
      </p>
    </div>

    {% if page.tags.size > 0 %}"""

if target in c and "post-dedication-box" not in c:
    c = c.replace(target, replacement, 1)
    with open("_layouts/post.html", "w", encoding="utf-8") as f:
        f.write(c)
    print("Added dedication banner to _layouts/post.html successfully!")
else:
    print("Target not found or already added")
