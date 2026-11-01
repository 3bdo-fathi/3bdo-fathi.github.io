from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("assets/images/posts/android-security", exist_ok=True)

try:
    font_title = ImageFont.truetype("arialbd.ttf", 24)
    font_bold = ImageFont.truetype("arialbd.ttf", 16)
    font_regular = ImageFont.truetype("arial.ttf", 14)
    font_code = ImageFont.truetype("consola.ttf", 13)
except:
    font_title = font_bold = font_regular = font_code = None

def create_base(width, height, title, subtitle):
    img = Image.new("RGBA", (width, height), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)
    # Background gradient
    for y in range(height):
        factor = y / height
        r = int(13 + factor * 8)
        g = int(17 + factor * 10)
        b = int(23 + factor * 15)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    # Grid
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(30, 41, 59, 40), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(30, 41, 59, 40), width=1)
    # Header
    draw.text((40, 28), title, fill=(240, 246, 252, 255), font=font_title)
    draw.text((40, 62), subtitle, fill=(139, 148, 158, 255), font=font_regular)
    draw.line([(40, 92), (width - 40, 92)], fill=(48, 54, 61, 200), width=1)
    return img, draw

# 4. Multi-User Storage Diagram
def gen_ch4_multiuser():
    img, draw = create_base(1000, 580, "Android Multi-User Storage & UID Translation Architecture", "Deterministic mathematical UID offsets and isolated storage mount namespaces")
    # UID Formula Box
    draw.rounded_rectangle([(60, 115), (940, 185)], radius=10, fill=(168, 85, 247, 25), outline=(168, 85, 247, 255), width=2)
    draw.text((80, 128), "Deterministic Linux UID Formula", fill=(168, 85, 247, 255), font=font_bold)
    draw.text((80, 154), "Linux UID = (User_ID * 100,000) + App_ID   |   User 0 App 87 = UID 10087 (u0_a87)  |  User 10 App 87 = UID 1010087 (u10_a87)", fill=(240, 246, 252, 255), font=font_code)

    # Columns: User 0 vs User 10
    cols = [
        ("User 0 (Owner / Primary)", "Processes:\n  system_server (UID 1000)\n  Twitter (UID 10087, u0_a87)\n  Signal (UID 10092, u0_a92)\n\nFilesystem Paths:\n  /data/data/com.twitter (symlink)\n  /data/user/0/com.twitter (0700)\n  /storage/emulated/0/ (Media)", (56, 189, 248), 60),
        ("Linux Mount Namespaces", "Kernel Mediation (CLONE_NEWNS)\n\nsdcardfs / FUSE Driver\nMaps emulated storage:\n  /storage/emulated/0 -> /data/media/0\n  /storage/emulated/10 -> /data/media/10\n\nCross-User Access Blocked:\nEACCES at Kernel Level", (245, 158, 11), 370),
        ("User 10 (Secondary / Work)", "Processes:\n  Twitter (UID 1010087, u10_a87)\n  Signal (UID 1010092, u10_a92)\n\nFilesystem Paths:\n  /data/user/10/com.twitter (0700)\n  /data/user/10/org.signal (0700)\n  /storage/emulated/10/ (Media)", (74, 222, 128), 680)
    ]
    for title, desc, col, x in cols:
        draw.rounded_rectangle([(x, 210), (x + 260, 540)], radius=12, fill=(col[0], col[1], col[2], 20), outline=col, width=2)
        draw.text((x + 18, 230), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        yy = 270
        for l in lines:
            draw.text((x + 18, yy), l, fill=(201, 209, 217, 255), font=font_code)
            yy += 25
    img.save("assets/images/posts/android-security/ch4-multiuser-storage.png", "PNG")
    print("Generated ch4-multiuser-storage.png")

# 5. Cryptographic Architecture Diagram
def gen_ch5_crypto():
    img, draw = create_base(1000, 580, "Android Cryptographic Architecture & PRNG Entropy Pipeline", "Java Cryptography Architecture (JCA) providers and the CVE-2013-7372 failure point")
    # Boxes
    boxes = [
        ("Application Layer", "Cipher.getInstance(\"AES/GCM/NoPadding\")\nSecureRandom.getInstance(\"SHA1PRNG\")", (56, 189, 248), 120),
        ("JCA Provider Engine (java.security)", "Priority 1: Conscrypt / AndroidOpenSSL (libcrypto.so / BoringSSL)\nPriority 2: Bouncy Castle (BC - Pure Java legacy engine)\nPriority 3: AndroidKeyStoreProvider (TEE / Hardware binding)", (168, 85, 247), 240),
        ("Entropy Sources & CVE-2013-7372 Root Cause", "Kernel: /dev/urandom <- Interrupts, touch input, timing jitter\nFlaw: OpenSSL JNI failed to invoke RAND_seed(/dev/urandom)\nImpact: Static PID/time seed -> duplicate ECDSA k nonces -> private key theft!", (239, 68, 68), 380)
    ]
    for title, desc, col, y in boxes:
        draw.rounded_rectangle([(80, y), (920, y + 90)], radius=10, fill=(col[0], col[1], col[2], 25), outline=col, width=2)
        draw.text((105, y + 16), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        yy = y + 42
        for l in lines:
            draw.text((105, yy), l, fill=(201, 209, 217, 255), font=font_code)
            yy += 22
        if y < 350:
            draw.line([(500, y + 90), (500, y + 120)], fill=(139, 148, 158, 200), width=2)
            draw.polygon([(495, y + 115), (505, y + 115), (500, y + 122)], fill=(139, 148, 158, 200))
    img.save("assets/images/posts/android-security/ch5-crypto-architecture.png", "PNG")
    print("Generated ch5-crypto-architecture.png")

# 6. Network Security & PKI Diagram
def gen_ch6_pki():
    img, draw = create_base(1000, 580, "Android Network PKI & Certificate Validation Hierarchy", "System vs User CA stores, TrustManagerImpl validation chain, and pinning hooks")
    cols = [
        ("TLS Handshake", "Server presents X.509 cert chain\nHost: api.target.com\n\nConscrypt native SSL engine\ncalls TrustManagerImpl\n.verifyChain()", (56, 189, 248), 60),
        ("CA Trust Stores", "System CA Store:\n  /system/etc/security/cacerts/\n  Named: [subject_hash_old].0\n  Trusted by ALL apps\n\nUser CA Store:\n  /data/misc/keychain/cacerts-added\n  Ignored by default in Android 7+", (45, 212, 191), 370),
        ("Enforcement & Pinning", "Validation Steps:\n  1. Root anchor match\n  2. Temporal validity\n  3. Hostname verification\n\nPinning Rules:\n  NetworkSecurityConfig / OkHttp\n  Blocks rogue public CAs\n  Bypassable via Frida hooking", (244, 63, 94), 680)
    ]
    for title, desc, col, x in cols:
        draw.rounded_rectangle([(x, 130), (x + 260, 520)], radius=12, fill=(col[0], col[1], col[2], 20), outline=col, width=2)
        draw.text((x + 18, 155), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        yy = 205
        for l in lines:
            draw.text((x + 18, yy), l, fill=(201, 209, 217, 255), font=font_code)
            yy += 26
    # Connecting Arrows
    draw.line([(320, 310), (370, 310)], fill=(56, 189, 248, 255), width=2)
    draw.line([(630, 310), (680, 310)], fill=(45, 212, 191, 255), width=2)
    img.save("assets/images/posts/android-security/ch6-network-pki.png", "PNG")
    print("Generated ch6-network-pki.png")

# 8. AccountManager Diagram
def gen_ch8_account_manager():
    img, draw = create_base(1000, 580, "AccountManager Authentication & Token Delegation Flow", "Single Sign-On (SSO) architecture, signature checks, and accounts.db storage")
    steps = [
        ("1. App Requests Token", "App calls AccountManager.getAuthToken(account, authTokenType, ...)\nBinder transaction sent to AccountManagerService in system_server", (56, 189, 248)),
        ("2. Identity & Permission Verification", "AMS checks calling UID -> verifies signature against Authenticator package\nIf signatures match -> Silent token release; If signatures differ -> User prompt dialog", (168, 85, 247)),
        ("3. Authenticator Execution", "AMS binds to AbstractAccountAuthenticator service via IBinder\nAuthenticator exchanges credentials with remote OAuth2 server; returns token bundle", (245, 158, 11)),
        ("4. Token Caching in SQLite", "Token stored in /data/system/users/[userId]/accounts.db (authtokens table)\nAMS delivers short-lived access token to client app sandbox", (74, 222, 128))
    ]
    y = 120
    for title, desc, col in steps:
        draw.rounded_rectangle([(80, y), (920, y + 80)], radius=10, fill=(col[0], col[1], col[2], 25), outline=col, width=2)
        draw.text((105, y + 15), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        draw.text((105, y + 40), lines[0], fill=(240, 246, 252, 255), font=font_code)
        if len(lines) > 1:
            draw.text((105, y + 58), lines[1], fill=(139, 148, 158, 255), font=font_code)
        if y < 380:
            draw.line([(500, y + 80), (500, y + 105)], fill=(139, 148, 158, 200), width=2)
            draw.polygon([(495, y + 100), (505, y + 100), (500, y + 107)], fill=(139, 148, 158, 200))
        y += 105
    img.save("assets/images/posts/android-security/ch8-account-manager.png", "PNG")
    print("Generated ch8-account-manager.png")

# 9. Enterprise Security Diagram
def gen_ch9_enterprise():
    img, draw = create_base(1000, 580, "Android Enterprise & Dual-Persona Containerization Architecture", "Comparison between Device Administration API, Managed Profiles, and Samsung KNOX")
    cols = [
        ("Device Administration (Legacy)", "Introduced: Android 2.2\nModel: All-or-nothing control\n\nAbuse Vector:\nRansomware (Koler, Svpeng)\nlocks screen via lockNow()\nand prevents uninstallation\n\nRequires Safe Mode to remove", (239, 68, 68), 60),
        ("Managed Profiles (Work Profile)", "Introduced: Android 5.0 (AOSP)\nModel: Dual-persona container\n\nSegregation:\n  Separate UserHandle (e.g. 11)\n  Independent encryption keys\n  Cross-profile IPC filters\n  Silent remote wipe of work only", (129, 140, 248), 370),
        ("Samsung KNOX (Hardware-Bound)", "Hardware Root of Trust\n\nTIMA (TrustZone Integrity):\n  Monitors kernel code pages\n  eFuse (Warranty Bit) blown\n  on unauthorized root\n\nReal-time Kernel Protection (RKP)", (74, 222, 128), 680)
    ]
    for title, desc, col, x in cols:
        draw.rounded_rectangle([(x, 130), (x + 260, 520)], radius=12, fill=(col[0], col[1], col[2], 20), outline=col, width=2)
        draw.text((x + 18, 155), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        yy = 205
        for l in lines:
            draw.text((x + 18, yy), l, fill=(201, 209, 217, 255), font=font_code)
            yy += 25
    img.save("assets/images/posts/android-security/ch9-enterprise-knox.png", "PNG")
    print("Generated ch9-enterprise-knox.png")

# 11. HCE APDU Diagram
def gen_ch11_hce():
    img, draw = create_base(1000, 580, "Host-based Card Emulation (HCE) & ISO 7816-4 APDU Routing", "Contactless smart card protocol flow between POS terminal and Android application")
    cols = [
        ("POS Contactless Terminal", "ISO 14443-4 Type A/B RF\n\nTransmits Command APDU:\n  CLA: 0x00 (Class)\n  INS: 0xA4 (SELECT)\n  P1-P2: 0x04 0x00\n  Data: AID (Payment AID)\n\nAwaits Response APDU (90 00)", (56, 189, 248), 60),
        ("NfcService (system_server)", "Routes APDU over NCI bus\n\nCardEmulationManager:\n  Extracts AID from SELECT\n  Matches aid-group XML\n  Selects HostApduService\n\nDispatches APDU via Binder", (132, 204, 22), 370),
        ("Payment App (HostApduService)", "processCommandApdu(byte[])\n\nGenerates EMV Cryptogram:\n  Cloud-based Tokenization\n  Limited-Use Key (LUK)\n  Dynamic Cardholder Number\n\nReturns Response [Data, 90 00]", (168, 85, 247), 680)
    ]
    for title, desc, col, x in cols:
        draw.rounded_rectangle([(x, 130), (x + 260, 520)], radius=12, fill=(col[0], col[1], col[2], 20), outline=col, width=2)
        draw.text((x + 18, 155), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        yy = 205
        for l in lines:
            draw.text((x + 18, yy), l, fill=(201, 209, 217, 255), font=font_code)
            yy += 26
    # Connecting Arrows
    draw.line([(320, 310), (370, 310)], fill=(56, 189, 248, 255), width=2)
    draw.line([(630, 310), (680, 310)], fill=(132, 204, 22, 255), width=2)
    img.save("assets/images/posts/android-security/ch11-hce-apdu.png", "PNG")
    print("Generated ch11-hce-apdu.png")

# 13. Root Evolution Diagram
def gen_ch13_root():
    img, draw = create_base(1000, 580, "The Evolution of Android Root Access & Privilege Escalation", "From early setuid binaries to modern daemonized, namespace-isolated root engines")
    eras = [
        ("Era 1: Traditional SUID Binary (Android 1.0 - 4.2)", "/system/xbin/su binary with SUID bit set (chmod 4755)\nBroken by Android 4.3 mounting /system with 'nosuid' and SELinux enforcement", (239, 68, 68)),
        ("Era 2: Daemonized su & SuperSU (Android 4.3 - 7.0)", "su client talks via UNIX socket to standing daemonsu (UID 0) started via init.rc\nPatches kernel SELinux policy dynamically in RAM to create permissive 'su' domain", (245, 158, 11)),
        ("Era 3: Systemless Root & Magisk (Android 8.0 - 13.0)", "Leaves /system partition untouched to pass dm-verity checks\nMount Namespaces transparently overlay root binaries into RAM | Zygisk hooks Zygote", (74, 222, 128)),
        ("Era 4: KernelSU & APatch (Modern Android 13+)", "Direct kernel-level root injection; hooks sys_execve in kernel space\nCompletely invisible to userspace root detection heuristics and hardware attestation", (56, 189, 248))
    ]
    y = 115
    for title, desc, col in eras:
        draw.rounded_rectangle([(80, y), (920, y + 85)], radius=10, fill=(col[0], col[1], col[2], 25), outline=col, width=2)
        draw.text((105, y + 16), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        draw.text((105, y + 42), lines[0], fill=(240, 246, 252, 255), font=font_code)
        if len(lines) > 1:
            draw.text((105, y + 62), lines[1], fill=(139, 148, 158, 255), font=font_code)
        if y < 390:
            draw.line([(500, y + 85), (500, y + 115)], fill=(139, 148, 158, 200), width=2)
            draw.polygon([(495, y + 110), (505, y + 110), (500, y + 117)], fill=(139, 148, 158, 200))
        y += 110
    img.save("assets/images/posts/android-security/ch13-root-evolution.png", "PNG")
    print("Generated ch13-root-evolution.png")

if __name__ == "__main__":
    gen_ch4_multiuser()
    gen_ch5_crypto()
    gen_ch6_pki()
    gen_ch8_account_manager()
    gen_ch9_enterprise()
    gen_ch11_hce()
    gen_ch13_root()
