from PIL import Image, ImageDraw, ImageFont
import os

chapters = [
    {
        "num": 1,
        "title": "Practical Reverse Engineering",
        "subtitle": "Chapter 1: x86 and x64 Architecture",
        "tagline": "Registers, calling conventions, stack frames, paging, and Sample J walk-through.",
        "badge": "BOOK SUMMARY SERIES • PART 1",
        "accent": (16, 185, 129, 255),       # Emerald
        "accent_bg": (16, 185, 129, 30),
        "pills": [
            ("x86 / x64 Registers & EFLAGS", (16, 185, 129, 40), (16, 185, 129, 220)),
            ("Calling Conventions & Stack", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("Sample J DllMain Dissection", (245, 158, 11, 40), (245, 158, 11, 220))
        ]
    },
    {
        "num": 2,
        "title": "Practical Reverse Engineering",
        "subtitle": "Chapter 2: ARM Architecture & Assembly",
        "tagline": "RISC model, Thumb-2, barrel shifter, coprocessors, and unk_function decompilation.",
        "badge": "BOOK SUMMARY SERIES • PART 2",
        "accent": (56, 189, 248, 255),       # Sky blue
        "accent_bg": (56, 189, 248, 30),
        "pills": [
            ("ARM & Thumb-2 Execution States", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("AAPCS & Barrel Shifter", (168, 85, 247, 40), (168, 85, 247, 220)),
            ("Decompilation Walk-Through", (16, 185, 129, 40), (16, 185, 129, 220))
        ]
    },
    {
        "num": 3,
        "title": "Practical Reverse Engineering",
        "subtitle": "Chapter 3: The Windows Kernel & Rootkits",
        "tagline": "KPCR, system calls, IRQL, IRPs, pool memory, SSDT hooks, and Sample A/B drivers.",
        "badge": "BOOK SUMMARY SERIES • PART 3",
        "accent": (239, 68, 68, 255),       # Crimson Red
        "accent_bg": (239, 68, 68, 30),
        "pills": [
            ("KPCR & Kernel Dispatching", (239, 68, 68, 40), (239, 68, 68, 220)),
            ("IRP Mechanics & IOCTLs", (245, 158, 11, 40), (245, 158, 11, 220)),
            ("x86/x64 Rootkit Deep-Dive", (56, 189, 248, 40), (56, 189, 248, 220))
        ]
    },
    {
        "num": 4,
        "title": "Practical Reverse Engineering",
        "subtitle": "Chapter 4: Debugging & Automation",
        "tagline": "WinDbg, DbgEng scripting, pseudo-registers, automated UPX unpacker, and I/O monitor.",
        "badge": "BOOK SUMMARY SERIES • PART 4",
        "accent": (245, 158, 11, 255),       # Amber Gold
        "accent_bg": (245, 158, 11, 30),
        "pills": [
            ("WinDbg & DbgEng Scripting", (245, 158, 11, 40), (245, 158, 11, 220)),
            ("Breakpoints & Expressions", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("Custom Debugger Extensions", (16, 185, 129, 40), (16, 185, 129, 220))
        ]
    },
    {
        "num": 5,
        "title": "Practical Reverse Engineering",
        "subtitle": "Chapter 5: Obfuscation & Deobfuscation",
        "tagline": "Opaque predicates, CFG flattening, VMs, white-box crypto, and Quetz keygenme.",
        "badge": "BOOK SUMMARY SERIES • PART 5",
        "accent": (168, 85, 247, 255),      # Neon Purple
        "accent_bg": (168, 85, 247, 30),
        "pills": [
            ("CFG Flattening & Opaque Predicates", (168, 85, 247, 40), (168, 85, 247, 220)),
            ("VM-Based Obfuscation", (239, 68, 68, 40), (239, 68, 68, 220)),
            ("Quetz Keygenme Case Study", (56, 189, 248, 40), (56, 189, 248, 220))
        ]
    }
]

def generate_covers():
    width, height = 1200, 630
    os.makedirs("assets/images/posts/reverse-engineering", exist_ok=True)
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_subtitle = ImageFont.truetype("arial.ttf", 25)
        font_ch = ImageFont.truetype("arialbd.ttf", 26)
        font_meta = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = font_subtitle = font_ch = font_meta = None

    for c in chapters:
        img = Image.new("RGBA", (width, height), (10, 16, 26, 255))
        draw = ImageDraw.Draw(img)

        # Gradient background
        for y in range(height):
            factor = y / height
            r = int(8 + factor * 8)
            g = int(12 + factor * 14)
            b = int(22 + factor * 26)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # Grid lines (dark subtle cyan-slate)
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill=(28, 44, 70, 40), width=1)
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill=(28, 44, 70, 40), width=1)

        # Tech circles on right
        cx, cy = 920, 315
        for radius in [80, 140, 200, 260]:
            draw.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)], outline=(c["accent"][0], c["accent"][1], c["accent"][2], 35), width=1)

        # Chapter Number watermark
        try:
            font_giant = ImageFont.truetype("arialbd.ttf", 200)
            prefix = "0" if c['num'] < 10 else ""
            draw.text((820, 180), f"{prefix}{c['num']}", fill=(c["accent"][0], c["accent"][1], c["accent"][2], 26), font=font_giant)
        except:
            pass

        # Nodes & crosshair
        draw.ellipse([(cx - 16, cy - 16), (cx + 16, cy + 16)], fill=c["accent"], outline=(255, 255, 255, 220), width=2)
        draw.line([(cx, cy - 260), (cx, cy + 260)], fill=(c["accent"][0], c["accent"][1], c["accent"][2], 40), width=1)
        draw.line([(cx - 260, cy), (cx + 260, cy)], fill=(c["accent"][0], c["accent"][1], c["accent"][2], 40), width=1)

        # Badge
        draw.rounded_rectangle([(80, 85), (370, 122)], radius=18, fill=c["accent_bg"], outline=c["accent"], width=1)
        draw.text((98, 95), c["badge"], fill=c["accent"], font=font_meta)

        # Title
        draw.text((80, 150), c["title"], fill=(255, 255, 255, 255), font=font_title)
        draw.text((80, 212), "x86, x64, ARM, Windows Kernel, Reversing Tools & Obfuscation", fill=c["accent"], font=ImageFont.truetype("arialbd.ttf", 26))

        draw.text((80, 288), c["subtitle"], fill=(215, 230, 250, 255), font=font_ch)
        draw.text((80, 335), c["tagline"], fill=(145, 165, 190, 255), font=font_subtitle)

        # Pills
        px, py = 80, 420
        for text, bg, border in c["pills"]:
            tw = len(text) * 11 + 28
            draw.rounded_rectangle([(px, py), (px + tw, py + 38)], radius=12, fill=bg, outline=border, width=1)
            draw.text((px + 14, py + 10), text, fill=(230, 240, 255, 240), font=font_meta)
            px += tw + 14

        # Footer attribution
        draw.text((80, 560), "Bruce Dang • Alexandre Gazet • Elias Bachaalany • Sébastien Josse (Wiley)", fill=(100, 120, 150, 255), font=font_meta)

        out_path = f"assets/images/posts/reverse-engineering/chapter-{c['num']}-cover.png"
        img.save(out_path, "PNG")
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    generate_covers()

