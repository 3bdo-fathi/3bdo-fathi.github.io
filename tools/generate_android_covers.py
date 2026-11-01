from PIL import Image, ImageDraw, ImageFont
import os

chapters = [
    {
        "num": 1,
        "title": "Android Security Internals",
        "subtitle": "Chapter 1: Android's Security Model",
        "tagline": "Linux kernel isolation, Dalvik VM, Binder IPC, and the Android sandbox.",
        "badge": "BOOK SUMMARY SERIES • PART 1",
        "accent": (74, 222, 128, 255),
        "accent_bg": (74, 222, 128, 30),
        "pills": [
            ("Multi-Level Sandboxing", (74, 222, 128, 40), (74, 222, 128, 220)),
            ("Binder IPC Architecture", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("UID/GID Separation", (251, 191, 36, 40), (251, 191, 36, 220))
        ]
    },
    {
        "num": 2,
        "title": "Android Security Internals",
        "subtitle": "Chapter 2: Permissions Architecture",
        "tagline": "Manifest definitions, protection levels, signature enforcement, and runtime checks.",
        "badge": "BOOK SUMMARY SERIES • PART 2",
        "accent": (56, 189, 248, 255),
        "accent_bg": (56, 189, 248, 30),
        "pills": [
            ("Protection Levels & Flags", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("PackageManagerService", (168, 85, 247, 40), (168, 85, 247, 220)),
            ("Permission Enforcement Points", (74, 222, 128, 40), (74, 222, 128, 220))
        ]
    },
    {
        "num": 3,
        "title": "Android Security Internals",
        "subtitle": "Chapter 3: Package Management",
        "tagline": "APK file anatomy, DEX bytecode format, code signing, and package verification.",
        "badge": "BOOK SUMMARY SERIES • PART 3",
        "accent": (96, 165, 250, 255),
        "accent_bg": (96, 165, 250, 30),
        "pills": [
            ("JAR / APK Signature Scheme", (96, 165, 250, 40), (96, 165, 250, 220)),
            ("DEX Structure & ODEX/OAT", (251, 146, 60, 40), (251, 146, 60, 220)),
            ("Package Verification Protocol", (74, 222, 128, 40), (74, 222, 128, 220))
        ]
    },
    {
        "num": 4,
        "title": "Android Security Internals",
        "subtitle": "Chapter 4: User Management",
        "tagline": "Android multi-user architecture, isolated storage, and daemon segregation.",
        "badge": "BOOK SUMMARY SERIES • PART 4",
        "accent": (168, 85, 247, 255),
        "accent_bg": (168, 85, 247, 30),
        "pills": [
            ("Multi-User UID Offsets", (168, 85, 247, 40), (168, 85, 247, 220)),
            ("Per-User Storage Mounts", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("UserManagerService Mechanics", (244, 63, 94, 40), (244, 63, 94, 220))
        ]
    },
    {
        "num": 5,
        "title": "Android Security Internals",
        "subtitle": "Chapter 5: Cryptographic Providers",
        "tagline": "Java Cryptography Architecture (JCA), OpenSSL/BoringSSL, and Harmony engine.",
        "badge": "BOOK SUMMARY SERIES • PART 5",
        "accent": (245, 158, 11, 255),
        "accent_bg": (245, 158, 11, 30),
        "pills": [
            ("JCA Engine Architecture", (245, 158, 11, 40), (245, 158, 11, 220)),
            ("AndroidOpenSSL Provider", (74, 222, 128, 40), (74, 222, 128, 220)),
            ("SecureRandom & PRNG Entropy", (239, 68, 68, 40), (239, 68, 68, 220))
        ]
    },
    {
        "num": 6,
        "title": "Android Security Internals",
        "subtitle": "Chapter 6: Network Security & PKI",
        "tagline": "TrustManager implementation, CA store management, and TLS validation mechanisms.",
        "badge": "BOOK SUMMARY SERIES • PART 6",
        "accent": (45, 212, 191, 255),
        "accent_bg": (45, 212, 191, 30),
        "pills": [
            ("System CA Store /etc/security/cacerts", (45, 212, 191, 40), (45, 212, 191, 220)),
            ("Custom TrustManagers & TLS", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("Certificate Pinning Vectors", (244, 63, 94, 40), (244, 63, 94, 220))
        ]
    },
    {
        "num": 7,
        "title": "Android Security Internals",
        "subtitle": "Chapter 7: Credential Storage",
        "tagline": "Android KeyStore daemon, hardware-backed keys, and keystore security internals.",
        "badge": "BOOK SUMMARY SERIES • PART 7",
        "accent": (249, 115, 22, 255),
        "accent_bg": (249, 115, 22, 30),
        "pills": [
            ("keystore Daemon & IPC", (249, 115, 22, 40), (249, 115, 22, 220)),
            ("Master Key Derivation", (168, 85, 247, 40), (168, 85, 247, 220)),
            ("TEE & Keymaster HAL", (74, 222, 128, 40), (74, 222, 128, 220))
        ]
    },
    {
        "num": 8,
        "title": "Android Security Internals",
        "subtitle": "Chapter 8: Online Account Management",
        "tagline": "AccountManager internals, Authenticator services, and OAuth token mediation.",
        "badge": "BOOK SUMMARY SERIES • PART 8",
        "accent": (244, 63, 94, 255),
        "accent_bg": (244, 63, 94, 30),
        "pills": [
            ("AccountManagerService", (244, 63, 94, 40), (244, 63, 94, 220)),
            ("AbstractAccountAuthenticator", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("OAuth Token Delegation", (245, 158, 11, 40), (245, 158, 11, 220))
        ]
    },
    {
        "num": 9,
        "title": "Android Security Internals",
        "subtitle": "Chapter 9: Enterprise Security",
        "tagline": "Device administration API, policy management, and containerized profiles.",
        "badge": "BOOK SUMMARY SERIES • PART 9",
        "accent": (129, 140, 248, 255),
        "accent_bg": (129, 140, 248, 30),
        "pills": [
            ("DevicePolicyManagerService", (129, 140, 248, 40), (129, 140, 248, 220)),
            ("DeviceAdminReceiver Policies", (74, 222, 128, 40), (74, 222, 128, 220)),
            ("Managed Profiles & KNOX", (249, 115, 22, 40), (249, 115, 22, 220))
        ]
    },
    {
        "num": 10,
        "title": "Android Security Internals",
        "subtitle": "Chapter 10: Device Security",
        "tagline": "Full disk encryption (FDE), dm-crypt, Keymaster HAL, and Verified Boot (dm-verity).",
        "badge": "BOOK SUMMARY SERIES • PART 10",
        "accent": (239, 68, 68, 255),
        "accent_bg": (239, 68, 68, 30),
        "pills": [
            ("dm-crypt & Crypto Footer", (239, 68, 68, 40), (239, 68, 68, 220)),
            ("Verified Boot & dm-verity", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("Hardware Key Derivation", (245, 158, 11, 40), (245, 158, 11, 220))
        ]
    },
    {
        "num": 11,
        "title": "Android Security Internals",
        "subtitle": "Chapter 11: NFC & Secure Elements",
        "tagline": "Near Field Communication stack, Host-based Card Emulation (HCE), and UICC/eSE.",
        "badge": "BOOK SUMMARY SERIES • PART 11",
        "accent": (132, 204, 22, 255),
        "accent_bg": (132, 204, 22, 30),
        "pills": [
            ("Host-based Card Emulation (HCE)", (132, 204, 22, 40), (132, 204, 22, 220)),
            ("ISO 7816-4 APDU Dispatch", (56, 189, 248, 40), (56, 189, 248, 220)),
            ("Embedded Secure Element (eSE)", (168, 85, 247, 40), (168, 85, 247, 220))
        ]
    },
    {
        "num": 12,
        "title": "Android Security Internals",
        "subtitle": "Chapter 12: SELinux in Android",
        "tagline": "Security-Enhanced Linux in Android, MAC vs DAC, policy compilation, and domains.",
        "badge": "BOOK SUMMARY SERIES • PART 12",
        "accent": (14, 165, 233, 255),
        "accent_bg": (14, 165, 233, 30),
        "pills": [
            ("SEAndroid Mandatory Access Control", (14, 165, 233, 40), (14, 165, 233, 220)),
            ("Domain Transitions & Types", (74, 222, 128, 40), (74, 222, 128, 220)),
            ("mac_permissions.xml Mapping", (245, 158, 11, 40), (245, 158, 11, 220))
        ]
    },
    {
        "num": 13,
        "title": "Android Security Internals",
        "subtitle": "Chapter 13: System Updates & Root Access",
        "tagline": "Recovery OS, OTA update packages, root exploitation techniques, and Superuser daemons.",
        "badge": "BOOK SUMMARY SERIES • PART 13",
        "accent": (225, 29, 72, 255),
        "accent_bg": (225, 29, 72, 30),
        "pills": [
            ("Recovery OS & OTA Verification", (225, 29, 72, 40), (225, 29, 72, 220)),
            ("Root Exploitation Vectors", (239, 68, 68, 40), (239, 68, 68, 220)),
            ("su Daemon & Superuser Management", (168, 85, 247, 40), (168, 85, 247, 220))
        ]
    }
]

def generate_covers():
    width, height = 1200, 630
    os.makedirs("assets/images/posts/android-security", exist_ok=True)
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
            r = int(9 + factor * 8)
            g = int(14 + factor * 14)
            b = int(24 + factor * 26)
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
            draw.text((800 if c['num'] >= 10 else 820, 180), f"{prefix}{c['num']}", fill=(c["accent"][0], c["accent"][1], c["accent"][2], 26), font=font_giant)
        except:
            pass

        # Nodes & rings
        draw.ellipse([(cx - 16, cy - 16), (cx + 16, cy + 16)], fill=c["accent"], outline=(255, 255, 255, 220), width=2)
        draw.line([(cx, cy - 260), (cx, cy + 260)], fill=(c["accent"][0], c["accent"][1], c["accent"][2], 40), width=1)
        draw.line([(cx - 260, cy), (cx + 260, cy)], fill=(c["accent"][0], c["accent"][1], c["accent"][2], 40), width=1)

        # Badge
        draw.rounded_rectangle([(80, 85), (350, 122)], radius=18, fill=c["accent_bg"], outline=c["accent"], width=1)
        draw.text((98, 95), c["badge"], fill=c["accent"], font=font_meta)

        # Title
        draw.text((80, 150), c["title"], fill=(255, 255, 255, 255), font=font_title)
        draw.text((80, 212), "An In-Depth Guide to Android Security Architecture", fill=c["accent"], font=ImageFont.truetype("arialbd.ttf", 30))

        draw.text((80, 288), c["subtitle"], fill=(215, 230, 250, 255), font=font_ch)
        draw.text((80, 335), c["tagline"], fill=(145, 165, 190, 255), font=font_subtitle)

        # Pills
        px, py = 80, 420
        for text, bg, border in c["pills"]:
            tw = len(text) * 11 + 28
            draw.rounded_rectangle([(px, py), (px + tw, py + 34)], radius=8, fill=bg, outline=border, width=1)
            draw.text((px + 14, py + 8), text, fill=(240, 245, 255, 255), font=font_meta)
            px += tw + 14

        # Footer
        draw.line([(80, 520), (620, 520)], fill=(48, 54, 61, 200), width=1)
        draw.text((80, 545), "Author: Nikolay Elenkov   |   Technical Deep Dive: Abdulrahman Mohamed", fill=(139, 148, 158, 255), font=font_meta)

        out_path = f"assets/images/posts/android-security/chapter-{c['num']}-cover.png"
        img.save(out_path, "PNG")
        print(f"Saved {out_path}")

if __name__ == "__main__":
    generate_covers()

