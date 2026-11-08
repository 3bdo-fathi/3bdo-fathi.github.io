import os
import re
from PIL import Image, ImageDraw, ImageFont

# Define Output Directories
dirs = [
    'assets/images/posts/reverse-engineering',
    'assets/images/posts/android-security',
    'assets/images/posts/social-engineering',
    'assets/images/posts/vulnerability-research',
    'assets/images/posts/automation',
    'assets/images/posts/threat-intel',
    'assets/images/posts/appsec'
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# Load Fonts
FONT_TITLE = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 42)
FONT_SUB = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
FONT_BADGE = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 13)
FONT_PILL = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14)
FONT_AUTHOR = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17)
FONT_AUTHOR_SUB = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)

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
    img = Image.new('RGBA', (w, h), (10, 13, 19, 255)) # Deep carbon dark
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
        alpha = int(12 * (1 - r / 250))
        draw.ellipse([
            (glow_center[0] - r, glow_center[1] - r),
            (glow_center[0] + r, glow_center[1] + r)
        ], fill=(accent[0], accent[1], accent[2], alpha))
        
    # 3. Top Accent Line (Smooth gradient)
    for i in range(4):
        draw.line([(0, i), (w, i)], fill=(accent[0], accent[1], accent[2], 255 - i * 50), width=1)
        
    # 4. Header Row: Badge (Left) & Domain Tag (Right)
    badge = data['badge']
    b_bbox = draw.textbbox((0, 0), badge, font=FONT_BADGE)
    bw = b_bbox[2] - b_bbox[0] + 24
    bh = 28
    draw.rounded_rectangle([(70, 48), (70 + bw, 48 + bh)], radius=5, fill=(accent[0], accent[1], accent[2], 25), outline=(accent[0], accent[1], accent[2], 140), width=1)
    draw.text((82, 54), badge, fill=accent, font=FONT_BADGE)
    
    domain_text = "0x3bdo.github.io"
    d_bbox = draw.textbbox((0, 0), domain_text, font=FONT_BADGE)
    dw = d_bbox[2] - d_bbox[0] + 20
    draw.rounded_rectangle([(w - 70 - dw, 48), (w - 70, 48 + bh)], radius=5, fill=(255, 255, 255, 8), outline=(255, 255, 255, 25), width=1)
    draw.text((w - 70 - dw + 10, 54), domain_text, fill=(148, 163, 184, 255), font=FONT_BADGE)
    
    # 5. Kicker
    kicker = data['kicker'].upper()
    draw.text((70, 108), kicker, fill=(148, 163, 184, 255), font=FONT_BADGE)
    
    # 6. Main Title
    title_lines = wrap_text(data['title'], FONT_TITLE, 1060, draw)
    cur_y = 138
    for line in title_lines[:2]:
        draw.text((70, cur_y), line, fill=(248, 250, 252, 255), font=FONT_TITLE)
        cur_y += 52
        
    # 7. Tagline
    cur_y += 8
    desc_lines = wrap_text(data['tagline'], FONT_SUB, 1060, draw)
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
    
    tag = data.get('footer_tag', "SECURITY RESEARCH")
    tw = draw.textbbox((0, 0), tag, font=FONT_BADGE)[2]
    draw.text((w - 70 - tw, 547), tag, fill=(100, 116, 139, 255), font=FONT_BADGE)
    
    img.save(data['out_path'])
    print(f"Generated: {data['out_path']}")

# ==========================================
# DATA CATALOG FOR ALL 34 POSTS
# ==========================================

covers = [
    # ------------------------------------------
    # 1. PRACTICAL REVERSE ENGINEERING (5)
    # ------------------------------------------
    {
        "out_path": "assets/images/posts/reverse-engineering/chapter-1-cover.png",
        "badge": "REVERSE ENGINEERING • CHAPTER 1",
        "kicker": "PRACTICAL REVERSE ENGINEERING • BRUCE DANG",
        "title": "x86 and x64 Architecture & Assembly",
        "tagline": "Deep analysis of x86/x64 registers, calling conventions, stack frames, virtual paging, and Sample J.",
        "pills": ["x86/x64 Calling Conventions", "Stack Frame & RBP/RSP", "Page Tables & Virtual Memory", "Sample J Disassembly"],
        "accent": (16, 185, 129, 255), # Emerald
        "footer_tag": "BINARY ANALYSIS"
    },
    {
        "out_path": "assets/images/posts/reverse-engineering/chapter-2-cover.png",
        "badge": "REVERSE ENGINEERING • CHAPTER 2",
        "kicker": "PRACTICAL REVERSE ENGINEERING • BRUCE DANG",
        "title": "ARM Architecture, Assembly & Decompilation",
        "tagline": "Dissecting the ARM RISC model, Thumb-2, condition flags, barrel shifter, and decompiling unk_function.",
        "pills": ["ARM & Thumb-2 Execution", "AAPCS Calling Convention", "Barrel Shifter Mechanics", "Decompilation Walk-Through"],
        "accent": (6, 182, 212, 255), # Cyan
        "footer_tag": "BINARY ANALYSIS"
    },
    {
        "out_path": "assets/images/posts/reverse-engineering/chapter-3-cover.png",
        "badge": "REVERSE ENGINEERING • CHAPTER 3",
        "kicker": "PRACTICAL REVERSE ENGINEERING • BRUCE DANG",
        "title": "The Windows Kernel, Architecture & Rootkits",
        "tagline": "KPCR, kernel dispatching, system calls, IRQL, IRPs, pool memory, SSDT hooks, and Sample A/B drivers.",
        "pills": ["KPCR & Kernel Dispatching", "IRP Mechanics & IOCTLs", "SSDT Hooking Architecture", "Rootkit Analysis"],
        "accent": (239, 68, 68, 255), # Crimson
        "footer_tag": "KERNEL SECURITY"
    },
    {
        "out_path": "assets/images/posts/reverse-engineering/chapter-4-cover.png",
        "badge": "REVERSE ENGINEERING • CHAPTER 4",
        "kicker": "PRACTICAL REVERSE ENGINEERING • BRUCE DANG",
        "title": "Dynamic Debugging & WinDbg Automation",
        "tagline": "Kernel dynamic debugging, DbgEng scripts, conditional breakpoints, memory search, and automation.",
        "pills": ["WinDbg Kernel Debugging", "DbgEng Automation Scripts", "Conditional Breakpoints", "Memory Pattern Scanning"],
        "accent": (59, 130, 246, 255), # Blue
        "footer_tag": "DEBUGGING & TOOLS"
    },
    {
        "out_path": "assets/images/posts/reverse-engineering/chapter-5-cover.png",
        "badge": "REVERSE ENGINEERING • CHAPTER 5",
        "kicker": "PRACTICAL REVERSE ENGINEERING • BRUCE DANG",
        "title": "Software Obfuscation & Deobfuscation",
        "tagline": "CFG flattening, dead code injection, opaque predicates, custom VM architectures, and symbolic execution.",
        "pills": ["CFG Flattening & Opaque Predicates", "Custom Bytecode VMs", "Virtual Instruction Handlers", "Symbolic Execution & SMT"],
        "accent": (168, 85, 247, 255), # Purple
        "footer_tag": "OBFUSCATION ANALYSIS"
    },

    # ------------------------------------------
    # 2. ANDROID SECURITY INTERNALS (13)
    # ------------------------------------------
    {
        "out_path": "assets/images/posts/android-security/chapter-1-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 1",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Android Security Architecture & Linux Sandbox",
        "tagline": "The foundation of Android OS security: Linux UID isolation, Zygote process spawning, and permission models.",
        "pills": ["Linux Kernel UID Sandboxing", "Zygote & App Spawning", "SELinux Domain Isolation", "Permission Enforcement"],
        "accent": (245, 158, 11, 255), # Amber
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-2-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 2",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Application Model & Permissions Architecture",
        "tagline": "Permission declarations, enforcement hooks in system server, runtime permission grants, and signature checks.",
        "pills": ["App Permissions & Framework", "Normal vs Dangerous Perms", "Signature & Privileged Checks", "Manifest Declarations"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-3-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 3",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Package Management & Cryptographic Signing",
        "tagline": "How PackageManagerService parses, verifies, and installs APKs across signature schemes v1 through v4.",
        "pills": ["APK Signing Schemes (v1-v4)", "PackageManagerService", "Certificate Verification", "Signature Alignment"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-4-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 4",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Multi-User Architecture & Storage Isolation",
        "tagline": "Scoped storage, FUSE emulation, Unix GID boundaries, and multi-user profile separation in Android.",
        "pills": ["Multi-User Isolation", "Scoped Storage & FUSE", "Unix Group ID Mapping", "Emulated External Storage"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-5-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 5",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Cryptographic Provider Architecture",
        "tagline": "Java Cryptography Architecture (JCA/JCE) in Android, Bouncy Castle, Conscrypt, and OpenSSL engine bindings.",
        "pills": ["Bouncy Castle & Conscrypt", "JCA / JCE Providers", "Key Derivation & PBKDF2", "Secure Random Generation"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-6-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 6",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Network Security, PKI & Certificate Pinning",
        "tagline": "Network Security Config, custom trust anchors, TLS certificate validation, and pinning implementations.",
        "pills": ["Network Security Config", "Custom Trust Anchors", "CA Store Validation", "Certificate Pinning Defense"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-7-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 7",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Android Keystore System & Key Management",
        "tagline": "Hardware-backed key storage, Trusted Execution Environment (TEE), Keymaster HAL, and StrongBox.",
        "pills": ["Hardware-Backed Keystore", "TEE & Keymaster HAL", "StrongBox & Secure Enclave", "Non-Exportable Keys"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-8-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 8",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Account Manager & Single Sign-On (SSO)",
        "tagline": "AccountManagerService internals, authenticator plugins, token caching, and cross-application identity sharing.",
        "pills": ["AccountManagerService", "Authenticator Plugins", "OAuth 2.0 Token Storage", "Cross-App Authentication"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-9-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 9",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Enterprise Security & Knox Framework",
        "tagline": "DevicePolicyManager, work profiles, MDM/EMM integration, and Samsung Knox TrustZone-based Integrity (TIMA).",
        "pills": ["DevicePolicyManager", "Work Profiles & MDM/EMM", "Samsung Knox TIMA", "Hardware Trust Architecture"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-10-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 10",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Device Encryption & Verified Boot",
        "tagline": "Full-Disk Encryption (FDE), File-Based Encryption (FBE), dm-crypt, dm-verity, and Android Verified Boot (AVB).",
        "pills": ["Full-Disk vs File-Based Enc", "dm-crypt & dm-verity", "AVB 2.0 Root of Trust", "Key Derivation in Ext4"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-11-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 11",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "NFC, Smart Cards & Host Card Emulation",
        "tagline": "Near Field Communication (NFC) protocol stack, Host Card Emulation (HCE), APDU dispatching, and Secure Elements.",
        "pills": ["Host Card Emulation (HCE)", "APDU Command Dispatching", "Secure Element (SE) Routing", "NFC Payment Architecture"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-12-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 12",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "SELinux Mandatory Access Control in Android",
        "tagline": "SEAndroid policy architecture, Type Enforcement (TE), domain transitions, and Access Vector Cache (AVC).",
        "pills": ["SELinux TE Policies", "Domain Transitions", "Audit Log Analysis (AVC)", "Policy Enforcement Engine"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },
    {
        "out_path": "assets/images/posts/android-security/chapter-13-cover.png",
        "badge": "ANDROID SECURITY • CHAPTER 13",
        "kicker": "ANDROID SECURITY INTERNALS • NIKOLAY ELENKOV",
        "title": "Android Root Mechanics & Superuser Management",
        "tagline": "Evolution of Android rooting: su binary injection, systemless root, Magisk Zygisk, and KernelSU architecture.",
        "pills": ["Bootloader Unlock Mechanics", "Magisk Zygisk & KernelSU", "Superuser Daemon (su)", "Root Defense Architecture"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "MOBILE INTERNALS"
    },

    # ------------------------------------------
    # 3. SOCIAL ENGINEERING (9)
    # ------------------------------------------
    {
        "out_path": "assets/images/posts/social-engineering/chapter-1-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 1",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "The Fundamentals of Human Hacking",
        "tagline": "Understanding the human attack surface, the psychological mindset of manipulation, and defensive awareness.",
        "pills": ["Human Attack Surfaces", "Security Awareness Fallacy", "Ethical Boundaries", "Adversary Mindset"],
        "accent": (168, 85, 247, 255), # Purple
        "footer_tag": "HUMAN HACKING"
    },
    {
        "out_path": "assets/images/posts/social-engineering/chapter-2-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 2",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "Information Gathering & Passive Reconnaissance",
        "tagline": "OSINT collection, digital footprint mapping, corporate metadata extraction, and target profiling techniques.",
        "pills": ["OSINT Profiling", "Social Media Intelligence", "Search Engine Dorking", "Digital Footprints"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "HUMAN HACKING"
    },
    {
        "out_path": "assets/images/posts/social-engineering/chapter-3-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 3",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "Elicitation Methodologies & Conversational Extraction",
        "tagline": "Conversational extraction tradecraft: false statements, flattery, intentional ignorance, and information funnels.",
        "pills": ["Conversational Extraction", "Elicitation Funnels", "Subtle Information Prompts", "Counter-Elicitation"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "HUMAN HACKING"
    },
    {
        "out_path": "assets/images/posts/social-engineering/chapter-4-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 4",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "Pretexting Principles & Identity Fabrication",
        "tagline": "Crafting believable identities, role creation, voice inflection, and maintaining credibility under suspicion.",
        "pills": ["Identity Fabrication", "Role Playing & Scenarios", "Believability Mechanics", "De-escalation Tradecraft"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "HUMAN HACKING"
    },
    {
        "out_path": "assets/images/posts/social-engineering/chapter-5-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 5",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "Persuasion, Psychological Triggers & Cognitive Bias",
        "tagline": "Exploiting human cognitive shortcuts, authority compliance, social proof, and neuro-linguistic fundamentals.",
        "pills": ["Cognitive Biases", "Heuristic Exploitation", "Rapport & Mirroring", "Psychological Framing"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "HUMAN HACKING"
    },
    {
        "out_path": "assets/images/posts/social-engineering/chapter-6-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 6",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "The Weapons of Influence: Cialdini's Six Principles",
        "tagline": "Reciprocity, Scarcity, Authority, Consistency, Liking, and Consensus applied to social engineering assessments.",
        "pills": ["Reciprocity & Obligation", "Scarcity & Urgency", "Authority Signaling", "Consensus & Social Proof"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "HUMAN HACKING"
    },
    {
        "out_path": "assets/images/posts/social-engineering/chapter-7-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 7",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "The Physical & Digital Tool Arsenal",
        "tagline": "Technical weaponization: Social-Engineer Toolkit (SET), credential harvesters, USB implants, and lock bypass tools.",
        "pills": ["Social-Engineer Toolkit (SET)", "Hardware Payloads", "RFID Cloning & Proxmark", "Lock Bypass Tools"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "HUMAN HACKING"
    },
    {
        "out_path": "assets/images/posts/social-engineering/chapter-8-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 8",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "Case Studies, Historical Heists & Attack Anatomy",
        "tagline": "Dissecting famous social engineering attacks, real-world breach retrospectives, and adversary methodologies.",
        "pills": ["Historical Heist Analysis", "Corporate Breach Retrospectives", "Attack Vector Breakdown", "Failure Points"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "HUMAN HACKING"
    },
    {
        "out_path": "assets/images/posts/social-engineering/chapter-9-cover.png",
        "badge": "SOCIAL ENGINEERING • CHAPTER 9",
        "kicker": "THE ART OF HUMAN HACKING • CHRISTOPHER HADNAGY",
        "title": "Defensive Engineering & Resilience Frameworks",
        "tagline": "Building organizational resilience: verification protocols, simulated attack campaigns, and human firewalls.",
        "pills": ["Human Firewall Engineering", "Verification Protocols", "Security Culture Auditing", "Incident Response"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "HUMAN HACKING"
    },

    # ------------------------------------------
    # 5. STANDALONE POSTS (6)
    # ------------------------------------------
    {
        "out_path": "assets/images/posts/automation/keylogger-audit-cover.png",
        "badge": "OFFENSIVE SECURITY • PRACTICAL AUDITING",
        "kicker": "LOW-LEVEL WINDOWS HOOKING & PERSISTENCE",
        "title": "Creating a Keylogger for Authorized Security Audits",
        "tagline": "Low-level Windows API hooking, keystroke telemetry, covert local persistence, and EDR detection mechanics.",
        "pills": ["Windows SetWindowsHookEx", "GetAsyncKeyState API", "Covert Data Persistence", "EDR Telemetry & Detection"],
        "accent": (20, 184, 166, 255), # Teal
        "footer_tag": "SYSTEMS SECURITY"
    },
    {
        "out_path": "assets/images/posts/automation/python-sysinfo-cover.png",
        "badge": "SECURITY AUTOMATION • OFFENSIVE TOOLING",
        "kicker": "HOST RECONNAISSANCE & PROFILING",
        "title": "Building a Python-Based System Information Tool",
        "tagline": "Automated host reconnaissance, cross-platform hardware inspection, network discovery, and data serialization.",
        "pills": ["Cross-Platform Host Recon", "WMI & System Profiling", "Network Interface Discovery", "JSON/CSV Serialization"],
        "accent": (6, 182, 212, 255), # Cyan
        "footer_tag": "SECURITY AUTOMATION"
    },
    {
        "out_path": "assets/images/posts/automation/recon-dns-framework-cover.png",
        "badge": "ATTACK SURFACE MANAGEMENT • TOOLING",
        "kicker": "DNS ENUMERATION & RECONNAISSANCE",
        "title": "Building an Advanced Recon & DNS Enumeration Framework",
        "tagline": "High-speed asynchronous DNS resolution, zone transfer discovery, subbrute dictionaries, and asset mapping.",
        "pills": ["Async DNS Enumeration", "DNS Zone Transfers (AXFR)", "Certificate Transparency", "Subdomain Permutation"],
        "accent": (14, 165, 233, 255), # Sky Blue
        "footer_tag": "ATTACK SURFACE MGMT"
    },
    {
        "out_path": "assets/images/posts/threat-intel/opsec-attribution-cover.png",
        "badge": "THREAT INTELLIGENCE • CASE STUDY",
        "kicker": "DIGITAL FORENSICS & ADVERSARY ATTRIBUTION",
        "title": "From Dark Web Fame to Digital Attribution: OPSEC Failures",
        "tagline": "Case study analyzing threat actor operational security failures, PGP leaks, metadata, and digital forensics.",
        "pills": ["Adversary OPSEC Failures", "PGP Fingerprint Analysis", "Git Metadata Reconstruction", "Digital Attribution Tradecraft"],
        "accent": (244, 63, 94, 255), # Rose / Coral
        "footer_tag": "THREAT INTELLIGENCE"
    },
    {
        "out_path": "assets/images/posts/appsec/cloudflare-architecture-cover.png",
        "badge": "INFRASTRUCTURE & EDGE SECURITY",
        "kicker": "GLOBAL CLOUD & EDGE NETWORK ARCHITECTURE",
        "title": "The Deep Infrastructure Architecture of Cloudflare",
        "tagline": "BGP Anycast routing, Unimog Layer 4 load balancing, eBPF XDP DDoS mitigation, and global edge workers.",
        "pills": ["BGP Anycast Routing", "Unimog Layer 4 Load Balancing", "eBPF / XDP Packet Filtering", "WAF Engine & SSL Termination"],
        "accent": (249, 115, 22, 255), # Orange
        "footer_tag": "INFRASTRUCTURE SECURITY"
    },
    {
        "out_path": "assets/images/posts/appsec/appsec-sast-dast-rasp-cover.png",
        "badge": "APPLICATION SECURITY • COMPREHENSIVE GUIDE",
        "kicker": "CODE ANALYSIS & RUNTIME APPLICATION PROTECTION",
        "title": "SAST vs DAST vs IAST vs RASP: The Complete Guide",
        "tagline": "Architectural comparison of code analysis paradigms, instrumentation agents, CI/CD pipeline gating, and ASPM.",
        "pills": ["SAST Static Code Analysis", "DAST Dynamic Blackbox Scans", "IAST Interactive Runtime Agents", "RASP Application Self-Protection"],
        "accent": (59, 130, 246, 255), # Blue
        "footer_tag": "APPLICATION SECURITY"
    },
    {
        "out_path": "assets/images/posts/android-security/mobile-tls-pinning-cover.png",
        "badge": "MOBILE PENTESTING PLAYBOOK • PART 1",
        "kicker": "TLS PINNING & RUNTIME TRAFFIC INTERCEPTION",
        "title": "Bypassing Modern TLS Pinning in Android & Hybrid Apps",
        "tagline": "Battle-tested methodology bypassing TLS pinning across Java Conscrypt, OkHttp3, BoringSSL, and compiled Flutter runtimes.",
        "pills": ["Conscrypt TrustManager Hooks", "OkHttp3 CertificatePinner Bypass", "Flutter BoringSSL Memory Patching", "Invisible Proxy & iptables"],
        "accent": (16, 185, 129, 255), # Emerald Green
        "footer_tag": "MOBILE SECURITY"
    },
    # ------------------------------------------
    # 8. MOBILE PENETRATION TESTING GUIDE
    # ------------------------------------------
    {
        "out_path": "assets/images/posts/android-security/mobile-pentesting-chapter-1.png",
        "badge": "MOBILE PENTESTING GUIDE • CHAPTER 1",
        "kicker": "OWASP MASTG • ARCHITECTURE & LAB SETUP",
        "title": "Modern Lab Setup, Architecture & Testing Methodology",
        "tagline": "OWASP MASTG testing lifecycle, Android UID sandboxing, SELinux enforcement, ADB mastery, and toolchain setup.",
        "pills": ["OWASP MASTG Lifecycle", "UID Sandboxing & SELinux", "ADB Daemon & Port Forwarding", "MobSF, Drozer & Frida"],
        "accent": (59, 130, 246, 255), # Azure Blue
        "footer_tag": "MOBILE APPLICATION SECURITY"
    },
    {
        "out_path": "assets/images/posts/android-security/mobile-pentesting-chapter-2.png",
        "badge": "MOBILE PENTESTING GUIDE • CHAPTER 2",
        "kicker": "REVERSE ENGINEERING • DALVIK & JNI NATIVE",
        "title": "APK Dissection, Smali Patching & Native Layer Analysis",
        "tagline": "Decompiling DEX bytecode, Smali opcode modification, root bypass patching, and Ghidra native .so analysis.",
        "pills": ["APK Signing Schemes (v1-v4)", "Smali Opcode Patching", "Root & License Bypass", "Ghidra JNI Native Reversing"],
        "accent": (168, 85, 247, 255), # Purple
        "footer_tag": "REVERSE ENGINEERING"
    },
    {
        "out_path": "assets/images/posts/android-security/mobile-pentesting-chapter-3.png",
        "badge": "MOBILE PENTESTING GUIDE • CHAPTER 3",
        "kicker": "IPC SECURITY • INTENT SPOOFING & DEEP LINKS",
        "title": "Android Component Security, IPC & Deep Link Hijacking",
        "tagline": "Exported activities, Intent spoofing, broadcast injection, Intent redirection, and Deep Links chained to RCE.",
        "pills": ["Exported Component Auditing", "Intent Spoofing with Drozer", "Confused Deputy Redirection", "Deep Links to RCE"],
        "accent": (244, 63, 94, 255), # Rose / Coral
        "footer_tag": "IPC EXPLOITATION"
    }
]

print(f"Total covers to generate: {len(covers)}")
for c in covers:
    render_cover(c)

print("\nAll 34 covers generated successfully!")

# ==========================================
# UPDATE FRONT-MATTER IN POSTS
# ==========================================

updates = [
    (
        "_posts/2025-03-05-creating-a-keylogger-for-security-audits.md",
        "assets/images/posts/automation/keylogger-audit-cover.png",
        "Creating a Keylogger for Authorized Security Audits Cover Banner"
    ),
    (
        "_posts/2025-10-30-mastering-information-gathering-python-automation.md",
        "assets/images/posts/automation/python-sysinfo-cover.png",
        "Building a Python-Based System Information Gathering Tool Cover Banner"
    ),
    (
        "_posts/2026-05-20-building-recon-dns-enumeration-framework.md",
        "assets/images/posts/automation/recon-dns-framework-cover.png",
        "Building an Advanced Reconnaissance & DNS Enumeration Framework Cover Banner"
    ),
    (
        "_posts/2026-05-28-from-dark-web-fame-to-digital-attribution.md",
        "assets/images/posts/threat-intel/opsec-attribution-cover.png",
        "From Dark Web Fame to Digital Attribution Cover Banner"
    ),
    (
        "_posts/2026-06-02-understanding-how-cloudflare-really-works.md",
        "assets/images/posts/appsec/cloudflare-architecture-cover.png",
        "The Deep Infrastructure Architecture of Cloudflare Cover Banner"
    ),
    (
        "_posts/2026-08-31-sast-dast-iast-rasp-complete-guide.md",
        "assets/images/posts/appsec/appsec-sast-dast-rasp-cover.png",
        "SAST vs DAST vs IAST vs RASP Cover Banner"
    )
]

for post_path, img_path, alt in updates:
    if os.path.exists(post_path):
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace image section in front matter
        image_block = f"image:\n  path: /{img_path}\n  alt: \"{alt}\""
        if 'image:' in content:
            new_content = re.sub(r'image:.*?(?=\ntags:|\ndate:|\ndescription:|\ntoc:|\nschema:|\n---)', image_block, content, flags=re.DOTALL)
        else:
            # insert before tags or description
            new_content = content.replace("description:", f"{image_block}\ndescription:")
            
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated front matter in {post_path}")

print("All front matter updates complete.")
