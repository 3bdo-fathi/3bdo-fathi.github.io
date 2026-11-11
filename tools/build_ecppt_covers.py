import os
from PIL import Image, ImageDraw, ImageFont

out_dir = 'assets/images/posts/ecppt'
os.makedirs(out_dir, exist_ok=True)

# Select robust Linux fonts
FONT_TITLE = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 38)
FONT_SUB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
FONT_BADGE = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf', 13)
FONT_PILL = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
FONT_AUTHOR = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
FONT_AUTHOR_SUB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def render_cover(data):
    w, h = 1200, 630
    img = Image.new('RGBA', (w, h), (10, 13, 19, 255))
    draw = ImageDraw.Draw(img)
    
    accent = data['accent']
    
    # 1. Subtle Background Grid (48px spacing)
    for x in range(0, w, 48):
        draw.line([(x, 0), (x, h)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, h, 48):
        draw.line([(0, y), (w, y)], fill=(255, 255, 255, 6), width=1)
        
    # 2. Ambient Glow in top right corner
    glow_center = (w - 150, 80)
    for r in range(250, 0, -25):
        alpha = int(14 * (1 - r / 250))
        draw.ellipse([
            (glow_center[0] - r, glow_center[1] - r),
            (glow_center[0] + r, glow_center[1] + r)
        ], fill=(accent[0], accent[1], accent[2], alpha))

    # Tech concentric circles on right
    cx, cy = 940, 315
    for radius in [90, 150, 220, 290]:
        draw.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)], 
                     outline=(accent[0], accent[1], accent[2], 28), width=1)
    draw.ellipse([(cx - 12, cy - 12), (cx + 12, cy + 12)], fill=accent, outline=(255, 255, 255, 200), width=2)
    draw.line([(cx, cy - 290), (cx, cy + 290)], fill=(accent[0], accent[1], accent[2], 35), width=1)
    draw.line([(cx - 290, cy), (cx + 290, cy)], fill=(accent[0], accent[1], accent[2], 35), width=1)
        
    # 3. Top Accent Line (Smooth gradient)
    for i in range(4):
        draw.line([(0, i), (w, i)], fill=(accent[0], accent[1], accent[2], 255 - i * 50), width=1)
        
    # 4. Header Row: Badge (Left) & Domain Tag (Right)
    badge = data['badge']
    b_bbox = draw.textbbox((0, 0), badge, font=FONT_BADGE)
    bw = b_bbox[2] - b_bbox[0] + 24
    bh = 28
    draw.rounded_rectangle([(70, 48), (70 + bw, 48 + bh)], radius=5, fill=(accent[0], accent[1], accent[2], 30), outline=(accent[0], accent[1], accent[2], 160), width=1)
    draw.text((82, 54), badge, fill=accent, font=FONT_BADGE)
    
    domain_text = "3bdo-fathi.github.io"
    d_bbox = draw.textbbox((0, 0), domain_text, font=FONT_BADGE)
    dw = d_bbox[2] - d_bbox[0] + 20
    draw.rounded_rectangle([(w - 70 - dw, 48), (w - 70, 48 + bh)], radius=5, fill=(255, 255, 255, 8), outline=(255, 255, 255, 25), width=1)
    draw.text((w - 70 - dw + 10, 54), domain_text, fill=(148, 163, 184, 255), font=FONT_BADGE)
    
    # 5. Kicker
    kicker = data['kicker'].upper()
    draw.text((70, 108), kicker, fill=(148, 163, 184, 255), font=FONT_BADGE)
    
    # 6. Main Title
    title_lines = wrap_text(data['title'], FONT_TITLE, 820, draw)
    cur_y = 138
    for line in title_lines[:2]:
        draw.text((70, cur_y), line, fill=(248, 250, 252, 255), font=FONT_TITLE)
        cur_y += 48
        
    # 7. Tagline
    cur_y += 10
    desc_lines = wrap_text(data['tagline'], FONT_SUB, 820, draw)
    for line in desc_lines[:2]:
        draw.text((70, cur_y), line, fill=(148, 163, 184, 255), font=FONT_SUB)
        cur_y += 28
        
    # 8. Technical Topic Pills
    py = 412
    px = 70
    for pill in data['pills']:
        p_bbox = draw.textbbox((0, 0), pill, font=FONT_PILL)
        pw = p_bbox[2] - p_bbox[0] + 26
        ph = 34
        if px + pw > w - 70:
            break
        draw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=17, fill=(255, 255, 255, 10), outline=(255, 255, 255, 35), width=1)
        draw.text((px + 13, py + 8), pill, fill=(226, 232, 240, 255), font=FONT_PILL)
        px += pw + 10
        
    # 9. Bottom Divider Line
    draw.line([(70, 520), (w - 70, 520)], fill=(255, 255, 255, 25), width=1)
    
    # 10. Standardized Author Signature
    author_name = "Abdulrahman M. Fathi"
    draw.text((70, 544), author_name, fill=(241, 245, 249, 255), font=FONT_AUTHOR)
    
    author_name_w = draw.textbbox((0, 0), author_name, font=FONT_AUTHOR)[2]
    author_sub = " • 0x3bdo | Cyber Security Engineer & Penetration Tester"
    draw.text((70 + author_name_w, 546), author_sub, fill=(100, 116, 139, 255), font=FONT_AUTHOR_SUB)
    
    tag = data.get('footer_tag', "ECPPT MASTERCLASS")
    tw = draw.textbbox((0, 0), tag, font=FONT_BADGE)[2]
    draw.text((w - 70 - tw, 547), tag, fill=(100, 116, 139, 255), font=FONT_BADGE)
    
    img.save(data['out_path'])
    print(f"Generated: {data['out_path']}")

covers = [
    {
        'badge': 'ECPPT MASTERCLASS • PART 1',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'System Security & x86 Assembly Fundamentals',
        'tagline': 'Processor architecture, 32-bit registers, process memory segmentation, stack frames, and calling conventions.',
        'pills': ['x86 Registers & Flags', 'Process Memory Map', 'Stack Anatomy & EBP/ESP', 'Calling Conventions (__cdecl)'],
        'accent': (56, 189, 248, 255), # Sky blue
        'out_path': 'assets/images/posts/ecppt/part-1-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 2',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'Exploit Development: Stack-Based & SEH Buffer Overflows',
        'tagline': 'Fuzzing sockets, EIP control, pattern offsets, bad characters elimination, mona.py gadgets, and SEH overwrite mechanics.',
        'pills': ['Socket Fuzzing', 'EIP Control & Offsets', 'Bad Characters Elimination', 'mona.py & SEH Overflows'],
        'accent': (239, 68, 68, 255), # Crimson Red
        'out_path': 'assets/images/posts/ecppt/part-2-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 3',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'Network Penetration Testing: Discovery & Service Attacks',
        'tagline': 'Host discovery, stealth scanning, service fingerprinting, SNMP/SMB enumeration, LLMNR poisoning, and SMB relaying.',
        'pills': ['Nmap Stealth & NSE', 'Service Enumeration', 'LLMNR/NBT-NS Poisoning', 'SMB Relay & Responder'],
        'accent': (245, 158, 11, 255), # Amber Gold
        'out_path': 'assets/images/posts/ecppt/part-3-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 4',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'Active Directory Pentesting: Kerberos & Domain Attacks',
        'tagline': 'Forest enumeration, BloodHound paths, Kerberoasting, AS-REP Roasting, Pass-the-Hash, and Golden/Silver tickets.',
        'pills': ['BloodHound Graph Analysis', 'Kerberoasting & AS-REP Roasting', 'Pass-the-Hash & Pass-the-Ticket', 'Golden & Silver Tickets'],
        'accent': (168, 85, 247, 255), # Electric Purple
        'out_path': 'assets/images/posts/ecppt/part-4-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 5',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'Windows & Linux Privilege Escalation Playbook',
        'tagline': 'Token impersonation (Potato attacks), insecure services, UAC bypasses, SUID binaries, sudo exploits, and capabilities.',
        'pills': ['Token Impersonation (Potatoes)', 'Insecure Services & AutoRuns', 'Linux SUID & Capabilities', 'Sudo & Dirty Pipe Exploits'],
        'accent': (16, 185, 129, 255), # Emerald Green
        'out_path': 'assets/images/posts/ecppt/part-5-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 6',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'Lateral Movement, Pivoting & Network Port Forwarding',
        'tagline': 'Multi-homed pivot topologies, SSH Local/Remote/Dynamic tunnels, Chisel, Ligolo-ng, Metasploit autoroute, and WMI/PsExec.',
        'pills': ['SSH Port Forwarding (-L / -R / -D)', 'Chisel & Ligolo-ng Routing', 'Proxychains & SOCKS5', 'WMIExec & PsExec Movement'],
        'accent': (249, 115, 22, 255), # Vibrant Orange
        'out_path': 'assets/images/posts/ecppt/part-6-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 7',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'Command and Control (C2): Architecture & Operations',
        'tagline': 'Tiered C2 redirector topologies, Domain Fronting, Cloudflare CDN workers, PowerShell-Empire, and Starkiller workflows.',
        'pills': ['C2 Infrastructure Hygiene', 'Domain Fronting & Cloudflare', 'PowerShell-Empire & Starkiller', 'Beacon Jitter & OpSec'],
        'accent': (236, 72, 153, 255), # Magenta / Hot Pink
        'out_path': 'assets/images/posts/ecppt/part-7-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 8',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'Web Application Pentesting: OWASP WSTG & Critical Flaws',
        'tagline': 'OWASP WSTG reconnaissance, In-Band Union-based SQLi, Error-based SQLi, XSS vectors, LFI log poisoning, and upload bypasses.',
        'pills': ['OWASP WSTG Framework', 'In-Band Union SQL Injection', 'Cross-Site Scripting (XSS)', 'LFI to RCE Log Poisoning'],
        'accent': (20, 184, 166, 255), # Teal
        'out_path': 'assets/images/posts/ecppt/part-8-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 9',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'Client-Side Attacks: Weaponization & Phishing Delivery',
        'tagline': 'Cialdini persuasion principles, GoPhish campaigns, VBA Macro weaponization, MacroPack, HTA attacks, and HTML smuggling.',
        'pills': ['Social Engineering Psychology', 'GoPhish Infrastructure', 'VBA Macro Weaponization', 'HTML Smuggling & MOTW Bypass'],
        'accent': (244, 63, 94, 255), # Coral Rose
        'out_path': 'assets/images/posts/ecppt/part-9-cover.png'
    },
    {
        'badge': 'ECPPT MASTERCLASS • PART 10',
        'kicker': 'eLearnSecurity Certified Professional Penetration Tester',
        'title': 'PowerShell for Pentesters: Offensive Ops & AMSI Evasion',
        'tagline': 'Pipelines, WMI administration, in-memory execution, PowerSploit suite, AMSI memory patching, and AST obfuscation.',
        'pills': ['Living-off-the-Land (LotL)', 'PowerSploit Arsenal', 'AMSI Memory Patching Hook', 'Invoke-Obfuscation AST'],
        'accent': (59, 130, 246, 255), # Royal Blue
        'out_path': 'assets/images/posts/ecppt/part-10-cover.png'
    }
]

if __name__ == '__main__':
    for c in covers:
        render_cover(c)
    print("All 10 eCPPT covers generated successfully!")
