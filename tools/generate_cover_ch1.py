from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('assets/images/posts/android-security', exist_ok=True)
output_path = 'assets/images/posts/android-security/mobile-pentesting-chapter-1.png'

# Canvas 1200x630
width, height = 1200, 630
img = Image.new('RGB', (width, height), color='#0d1117')
draw = ImageDraw.Draw(img)

# Cyber grid background lines
for x in range(0, width, 40):
    draw.line([(x, 0), (x, height)], fill='#161b22', width=1)
for y in range(0, height, 40):
    draw.line([(0, y), (width, y)], fill='#161b22', width=1)

# Subtle cyan/blue accent glow border
draw.rectangle([(20, 20), (width - 20, height - 20)], outline='#30363d', width=2)
draw.line([(20, 20), (120, 20)], fill='#58a6ff', width=4)
draw.line([(20, 20), (20, 120)], fill='#58a6ff', width=4)
draw.line([(width - 20, height - 20), (width - 120, height - 20)], fill='#39d353', width=4)
draw.line([(width - 20, height - 20), (width - 20, height - 120)], fill='#39d353', width=4)

# Load font
try:
    font_badge = ImageFont.truetype('arialbd.ttf', 20)
    font_title = ImageFont.truetype('arialbd.ttf', 44)
    font_sub = ImageFont.truetype('arialbd.ttf', 26)
    font_meta = ImageFont.truetype('arial.ttf', 20)
    font_code = ImageFont.truetype('consola.ttf', 18)
except Exception:
    font_badge = font_title = font_sub = font_meta = font_code = ImageFont.load_default()

# Series Badge
draw.rectangle([(60, 60), (380, 100)], fill='#161b22', outline='#58a6ff', width=1)
draw.text((80, 70), "MOBILE PENTESTING GUIDE - CH 01", fill='#58a6ff', font=font_badge)

# Main Title
draw.text((60, 130), "Modern Lab Setup, Architecture", fill='#ffffff', font=font_title)
draw.text((60, 185), "& Penetration Testing Methodology", fill='#58a6ff', font=font_title)

# Subtitle / Summary
draw.text((60, 260), "OWASP MASTG Workflow | ADB Mastery | Root & Emulators", fill='#8b949e', font=font_sub)
draw.text((60, 300), "Toolchain: Jadx, Apktool, MobSF, Drozer, Frida & Objection", fill='#8b949e', font=font_sub)

# Terminal / Code Mockup Box
draw.rectangle([(60, 360), (1140, 540)], fill='#090d13', outline='#30363d', width=1)
draw.rectangle([(60, 360), (1140, 395)], fill='#161b22')
draw.ellipse([(75, 373), (87, 385)], fill='#ff5f56')
draw.ellipse([(95, 373), (107, 385)], fill='#ffbd2e')
draw.ellipse([(115, 373), (127, 385)], fill='#27c93f')
draw.text((145, 372), "root@0x3bdo-lab: ~# android-pentest-init", fill='#8b949e', font=font_code)

draw.text((80, 415), "[*] Initializing OWASP MASTG Mobile Security Testing Lab...", fill='#39d353', font=font_code)
draw.text((80, 445), "[+] ADB Bridge Established: emulator-5554 [Android 14 / x86_64 / Rooted via Magisk]", fill='#58a6ff', font=font_code)
draw.text((80, 475), "[+] Frida-Server v16.x daemon active on tcp:27042 | Objection Agent linked", fill='#e3b341', font=font_code)
draw.text((80, 505), "[+] Drozer Server connected on 127.0.0.1:31415 | Target package loaded", fill='#ff7b72', font=font_code)

# Footer
draw.text((60, 575), "0x3bdo | Offensive Security & Reverse Engineering", fill='#6e7681', font=font_meta)
draw.text((960, 575), "Comprehensive Master Guide", fill='#58a6ff', font=font_meta)

img.save(output_path, 'PNG', optimize=True)
print("Saved:", output_path)

