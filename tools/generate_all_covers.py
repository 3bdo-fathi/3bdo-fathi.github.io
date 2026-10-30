from PIL import Image, ImageDraw, ImageFont

chapters = [
    {
        "num": 2,
        "title": "Social Engineering",
        "subtitle": "Chapter 2: Information Gathering",
        "tagline": "The art of OSINT, communication modeling, and building the target dossier.",
        "badge": "BOOK SUMMARY SERIES • PART 2",
        "accent": (57, 197, 207, 255),
        "accent_bg": (57, 197, 207, 30),
        "pills": [
            ("Information is 90% of War", (57, 197, 207, 40), (57, 197, 207, 220)),
            ("Communication Modeling", (88, 166, 255, 40), (88, 166, 255, 220)),
            ("The Stamp Collection Vector", (210, 153, 34, 40), (210, 153, 34, 220))
        ]
    },
    {
        "num": 3,
        "title": "Social Engineering",
        "subtitle": "Chapter 3: Elicitation & Subconscious Cues",
        "tagline": "Mastering the subtle art of drawing information during innocent conversation.",
        "badge": "BOOK SUMMARY SERIES • PART 3",
        "accent": (188, 140, 255, 255),
        "accent_bg": (188, 140, 255, 30),
        "pills": [
            ("The NSA Elicitation Rules", (188, 140, 255, 40), (188, 140, 255, 220)),
            ("Preloading the Target Mind", (88, 166, 255, 40), (88, 166, 255, 220)),
            ("Open vs Assumptive Questions", (63, 185, 80, 40), (63, 185, 80, 220))
        ]
    },
    {
        "num": 4,
        "title": "Social Engineering",
        "subtitle": "Chapter 4: Pretexting — Becoming Anyone",
        "tagline": "Constructing believable personas, spontaneous delivery, and ethical boundaries.",
        "badge": "BOOK SUMMARY SERIES • PART 4",
        "accent": (240, 136, 62, 255),
        "accent_bg": (240, 136, 62, 30),
        "pills": [
            ("The 7 Principles of Pretexting", (240, 136, 62, 40), (240, 136, 62, 220)),
            ("Stanley Rifkin's $10M Wire Transfer", (248, 81, 73, 40), (248, 81, 73, 220)),
            ("Legal Framework & FTC Act", (88, 166, 255, 40), (88, 166, 255, 220))
        ]
    },
    {
        "num": 5,
        "title": "Social Engineering",
        "subtitle": "Chapter 5: Mind Tricks & Psychology",
        "tagline": "Microexpressions, NLP, rapport building, and the Human Buffer Overflow.",
        "badge": "BOOK SUMMARY SERIES • PART 5",
        "accent": (235, 87, 87, 255),
        "accent_bg": (235, 87, 87, 30),
        "pills": [
            ("Paul Ekman's 7 Microexpressions", (235, 87, 87, 40), (235, 87, 87, 220)),
            ("Human Buffer Overflow (HBO)", (188, 140, 255, 40), (188, 140, 255, 220)),
            ("Active Listening & Rapport", (63, 185, 80, 40), (63, 185, 80, 220))
        ]
    },
    {
        "num": 6,
        "title": "Social Engineering",
        "subtitle": "Chapter 6: Influence & Persuasion",
        "tagline": "Weapons of influence, framing realities, and ethical manipulation tactics.",
        "badge": "BOOK SUMMARY SERIES • PART 6",
        "accent": (63, 185, 80, 255),
        "accent_bg": (63, 185, 80, 30),
        "pills": [
            ("Reciprocity & Obligation", (63, 185, 80, 40), (63, 185, 80, 220)),
            ("Scarcity & Social Proof", (210, 153, 34, 40), (210, 153, 34, 220)),
            ("Cognitive Frame Transformation", (88, 166, 255, 40), (88, 166, 255, 220))
        ]
    },
    {
        "num": 7,
        "title": "Social Engineering",
        "subtitle": "Chapter 7: Tools of the Social Engineer",
        "tagline": "Physical lockpicks, covert cameras, Maltego, SET, and password profilers.",
        "badge": "BOOK SUMMARY SERIES • PART 7",
        "accent": (88, 166, 255, 255),
        "accent_bg": (88, 166, 255, 30),
        "pills": [
            ("Physical Locks & Shove Knives", (240, 136, 62, 40), (240, 136, 62, 220)),
            ("Social Engineer Toolkit (SET)", (88, 166, 255, 40), (88, 166, 255, 220)),
            ("Maltego & Recon Frameworks", (57, 197, 207, 40), (57, 197, 207, 220))
        ]
    },
    {
        "num": 8,
        "title": "Social Engineering",
        "subtitle": "Chapter 8: Real-World Case Studies",
        "tagline": "Dissecting legendary exploits: Kevin Mitnick, Overconfident CEO, and Rogue Hacker.",
        "badge": "BOOK SUMMARY SERIES • PART 8",
        "accent": (210, 153, 34, 255),
        "accent_bg": (210, 153, 34, 30),
        "pills": [
            ("Mitnick's DMV & SSA Exploits", (210, 153, 34, 40), (210, 153, 34, 220)),
            ("The Theme Park Ticket Scandal", (57, 197, 207, 40), (57, 197, 207, 220)),
            ("Social Engineering a Rogue Hacker", (248, 81, 73, 40), (248, 81, 73, 220))
        ]
    },
    {
        "num": 9,
        "title": "Social Engineering",
        "subtitle": "Chapter 9: Prevention & Mitigation",
        "tagline": "Hardening the human firewall: policy verification, defense scripts, and audits.",
        "badge": "BOOK SUMMARY SERIES • PART 9",
        "accent": (56, 139, 253, 255),
        "accent_bg": (56, 139, 253, 30),
        "pills": [
            ("Building a Security Culture", (63, 185, 80, 40), (63, 185, 80, 220)),
            ("Non-Punitive Verification Scripts", (56, 139, 253, 40), (56, 139, 253, 220)),
            ("Conducting Ethical SE Audits", (188, 140, 255, 40), (188, 140, 255, 220))
        ]
    }
]

def generate_covers():
    width, height = 1200, 630
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_subtitle = ImageFont.truetype("arial.ttf", 26)
        font_ch = ImageFont.truetype("arialbd.ttf", 24)
        font_meta = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = font_subtitle = font_ch = font_meta = None

    for c in chapters:
        img = Image.new("RGBA", (width, height), (10, 14, 23, 255))
        draw = ImageDraw.Draw(img)

        # Gradient background
        for y in range(height):
            factor = y / height
            r = int(10 + factor * 8)
            g = int(14 + factor * 16)
            b = int(23 + factor * 28)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # Grid lines
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill=(30, 48, 75, 45), width=1)
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill=(30, 48, 75, 45), width=1)

        # Tech circles on right
        cx, cy = 920, 315
        for radius in [80, 140, 200, 260]:
            draw.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)], outline=(c["accent"][0], c["accent"][1], c["accent"][2], 30), width=1)

        # Chapter Number watermark
        try:
            font_giant = ImageFont.truetype("arialbd.ttf", 210)
            draw.text((820, 180), f"0{c['num']}", fill=(c["accent"][0], c["accent"][1], c["accent"][2], 25), font=font_giant)
        except:
            pass

        # Nodes
        draw.ellipse([(cx - 15, cy - 15), (cx + 15, cy + 15)], fill=c["accent"], outline=(255, 255, 255, 200), width=2)

        # Badge
        draw.rounded_rectangle([(80, 95), (320, 131)], radius=18, fill=c["accent_bg"], outline=c["accent"], width=1)
        draw.text((98, 104), c["badge"], fill=c["accent"])

        # Title
        draw.text((80, 160), c["title"], fill=(255, 255, 255, 255), font=font_title)
        draw.text((80, 220), "The Art of Human Hacking", fill=c["accent"], font=font_title)

        draw.text((80, 295), c["subtitle"], fill=(200, 215, 235, 255), font=font_ch)
        draw.text((80, 340), c["tagline"], fill=(140, 155, 175, 255), font=font_subtitle)

        # Pills
        px, py = 80, 420
        for text, bg, border in c["pills"]:
            tw = len(text) * 11 + 28
            draw.rounded_rectangle([(px, py), (px + tw, py + 34)], radius=8, fill=bg, outline=border, width=1)
            draw.text((px + 14, py + 8), text, fill=(240, 245, 255, 255), font=font_meta)
            px += tw + 14

        # Footer
        draw.line([(80, 520), (620, 520)], fill=(48, 54, 61, 200), width=1)
        draw.text((80, 545), f"Author: Christopher Hadnagy   |   Analysis & Synthesis: Abdulrahman Mohamed", fill=(139, 148, 158, 255), font=font_meta)

        out_path = f"assets/images/posts/social-engineering/chapter-{c['num']}-cover.png"
        img.save(out_path, "PNG")
        print(f"Saved {out_path}")

if __name__ == "__main__":
    generate_covers()
