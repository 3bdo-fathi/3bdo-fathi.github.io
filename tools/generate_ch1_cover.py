import math
from PIL import Image, ImageDraw, ImageFont

def create_cover():
    width, height = 1200, 630
    img = Image.new("RGBA", (width, height), (10, 14, 23, 255))
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(height):
        factor = y / height
        r = int(10 + factor * 8)
        g = int(14 + factor * 16)
        b = int(23 + factor * 28)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Decorative tech grid pattern
    grid_color = (30, 48, 75, 50)
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Glowing subtle circuit / network lines on the right side
    cx, cy = 920, 315
    for radius in [80, 140, 200, 260]:
        draw.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)], outline=(57, 197, 207, 30), width=1)

    # Nodes on circles
    nodes = [
        (cx - 140, cy - 50, "Information Gathering"),
        (cx - 60, cy - 120, "Pretexting"),
        (cx + 80, cy - 110, "Elicitation"),
        (cx + 140, cy + 30, "Psychology & NLP"),
        (cx + 60, cy + 130, "Influence & Persuasion"),
        (cx - 70, cy + 120, "Physical & Tech Tools"),
        (cx, cy, "Human Target")
    ]

    for nx, ny, label in nodes:
        draw.line([(cx, cy), (nx, ny)], fill=(88, 166, 255, 60), width=2)
        node_color = (63, 185, 80, 255) if label == "Human Target" else (57, 197, 207, 255)
        draw.ellipse([(nx - 8, ny - 8), (nx + 8, ny + 8)], fill=node_color, outline=(255, 255, 255, 180), width=2)

    # Marionette strings from top
    for nx, ny, _ in nodes[:6]:
        draw.line([(nx, 0), (nx, ny - 10)], fill=(88, 166, 255, 40), width=1)

    # Center target pulse
    draw.ellipse([(cx - 16, cy - 16), (cx + 16, cy + 16)], outline=(63, 185, 80, 100), width=3)
    draw.ellipse([(cx - 24, cy - 24), (cx + 24, cy + 24)], outline=(63, 185, 80, 50), width=1)

    # Left content box / badges
    # Badge: Book Summary Series
    badge_x, badge_y = 80, 95
    badge_w, badge_h = 240, 36
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)], radius=18, fill=(88, 166, 255, 30), outline=(88, 166, 255, 180), width=1)
    draw.text((badge_x + 18, badge_y + 9), "BOOK SUMMARY SERIES • PART 1", fill=(88, 166, 255, 255))

    # Main Book Title
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_subtitle = ImageFont.truetype("arial.ttf", 26)
        font_ch = ImageFont.truetype("arialbd.ttf", 24)
        font_meta = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = font_subtitle = font_ch = font_meta = None

    draw.text((80, 160), "Social Engineering", fill=(255, 255, 255, 255), font=font_title)
    draw.text((80, 220), "The Art of Human Hacking", fill=(57, 197, 207, 255), font=font_title)

    draw.text((80, 295), "Chapter 1: A Look into the World of Social Engineering", fill=(200, 215, 235, 255), font=font_ch)
    draw.text((80, 340), "Deconstructing the mindset, science, and methodology behind human exploitation.", fill=(140, 155, 175, 255), font=font_subtitle)

    # Stats / Takeaways pill cards
    pills = [
        ("The Science of Deception", (63, 185, 80, 40), (63, 185, 80, 220)),
        ("The Master Chef Analogy", (88, 166, 255, 40), (88, 166, 255, 220)),
        ("ROI of Attacking Humans", (210, 153, 34, 40), (210, 153, 34, 220))
    ]
    px = 80
    py = 420
    for text, bg, border in pills:
        tw = len(text) * 11 + 28
        draw.rounded_rectangle([(px, py), (px + tw, py + 34)], radius=8, fill=bg, outline=border, width=1)
        draw.text((px + 14, py + 8), text, fill=(240, 245, 255, 255), font=font_meta)
        px += tw + 14

    # Bottom author line
    draw.line([(80, 520), (620, 520)], fill=(48, 54, 61, 200), width=1)
    draw.text((80, 545), "Author: Christopher Hadnagy   |   Analysis & Synthesis: Abdulrahman Mohamed", fill=(139, 148, 158, 255), font=font_meta)

    img.save("assets/images/posts/social-engineering/chapter-1-cover.png", "PNG")
    print("Cover generated successfully!")

if __name__ == "__main__":
    create_cover()
