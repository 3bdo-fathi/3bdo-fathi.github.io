from PIL import Image, ImageDraw, ImageFont
import os

output_path = 'assets/images/posts/android-security/mobile-pentesting-chapter-3.png'

width, height = 1200, 630
img = Image.new('RGB', (width, height), color='#0d1117')
draw = ImageDraw.Draw(img)

# Cyber grid background lines
for x in range(0, width, 40):
    draw.line([(x, 0), (x, height)], fill='#161b22', width=1)
for y in range(0, height, 40):
    draw.line([(0, y), (width, y)], fill='#161b22', width=1)

# Subtle red/orange accent glow border
draw.rectangle([(20, 20), (width - 20, height - 20)], outline='#30363d', width=2)
draw.line([(20, 20), (120, 20)], fill='#ff7b72', width=4)
draw.line([(20, 20), (20, 120)], fill='#ff7b72', width=4)
draw.line([(width - 20, height - 20), (width - 120, height - 20)], fill='#f0883e', width=4)
draw.line([(width - 20, height - 20), (width - 20, height - 120)], fill='#f0883e', width=4)

try:
    font_badge = ImageFont.truetype('arialbd.ttf', 20)
    font_title = ImageFont.truetype('arialbd.ttf', 44)
    font_sub = ImageFont.truetype('arialbd.ttf', 26)
    font_meta = ImageFont.truetype('arial.ttf', 20)
    font_code = ImageFont.truetype('consola.ttf', 18)
except Exception:
    font_badge = font_title = font_sub = font_meta = font_code = ImageFont.load_default()

# Series Badge
draw.rectangle([(60, 60), (380, 100)], fill='#161b22', outline='#ff7b72', width=1)
draw.text((80, 70), "MOBILE PENTESTING GUIDE - CH 03", fill='#ff7b72', font=font_badge)

# Main Title
draw.text((60, 130), "Android Component Security, IPC &", fill='#ffffff', font=font_title)
draw.text((60, 185), "Deep Link Hijacking to RCE", fill='#ff7b72', font=font_title)

# Subtitle / Summary
draw.text((60, 260), "Exported Activities | Broadcast Injection | Intent Redirection", fill='#8b949e', font=font_sub)
draw.text((60, 300), "Drozer Exploitation | Deep Links & App Links Chaining", fill='#8b949e', font=font_sub)

# Terminal / Code Mockup Box
draw.rectangle([(60, 360), (1140, 540)], fill='#090d13', outline='#30363d', width=1)
draw.rectangle([(60, 360), (1140, 395)], fill='#161b22')
draw.ellipse([(75, 373), (87, 385)], fill='#ff5f56')
draw.ellipse([(95, 373), (107, 385)], fill='#ffbd2e')
draw.ellipse([(115, 373), (127, 385)], fill='#27c93f')
draw.text((145, 372), "drozer console connect -- attack-ipc", fill='#8b949e', font=font_code)

draw.text((80, 415), "dz> run app.activity.start --component com.target.app .AdminDashboard", fill='#ff7b72', font=font_code)
draw.text((80, 445), "[+] Intent Spoofing Successful: Bypassed AuthPinLockActivity -> UID u0_a145", fill='#39d353', font=font_code)
draw.text((80, 475), "dz> run app.package.attacksurface com.target.app", fill='#58a6ff', font=font_code)
draw.text((80, 505), "[!] Attack Surface: 4 exported activities, 2 broadcast receivers, 1 vulnerable deep link", fill='#f0883e', font=font_code)

# Footer
draw.text((60, 575), "0x3bdo | Offensive Security & Reverse Engineering", fill='#6e7681', font=font_meta)
draw.text((960, 575), "Comprehensive Master Guide", fill='#ff7b72', font=font_meta)

img.save(output_path, 'PNG', optimize=True)
print("Saved:", output_path)

