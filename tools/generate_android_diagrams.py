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
    draw.text((40, 30), title, fill=(240, 246, 252, 255), font=font_title)
    draw.text((40, 65), subtitle, fill=(139, 148, 158, 255), font=font_regular)
    draw.line([(40, 95), (width - 40, 95)], fill=(48, 54, 61, 200), width=1)
    return img, draw

# 1. Android Architecture Diagram
def gen_ch1_architecture():
    img, draw = create_base(1000, 620, "Android Multi-Tier Security Architecture", "Defense-in-depth isolation from Linux kernel to application runtime")
    layers = [
        ("Application Layer (Sandboxed UIDs)", "Third-party & Pre-installed Apps (UID >= 10000) | Isolated per-app process sandboxes", (74, 222, 128)),
        ("Application Framework & System Services", "system_server (ActivityManager, PackageManager, WindowManager) | IPC Security Checks", (56, 189, 248)),
        ("Android Runtime & Core Native Daemons", "ART / Dalvik Virtual Machine | Zygote | servicemanager | vold | netd | keystore | installd", (168, 85, 247)),
        ("Hardware Abstraction Layer (HAL)", "Vendor HAL modules (Keymaster, Camera, Audio, RIL, Sensors, Gralloc)", (245, 158, 11)),
        ("Linux Kernel & Security Subsystems", "SELinux (MAC) | Process Isolation (UID/GID) | Binder Driver (/dev/binder) | dm-crypt | dm-verity", (239, 68, 68))
    ]
    y = 120
    for title, desc, col in layers:
        draw.rounded_rectangle([(60, y), (940, y + 75)], radius=10, fill=(col[0], col[1], col[2], 25), outline=col, width=2)
        draw.text((80, y + 15), title, fill=col, font=font_bold)
        draw.text((80, y + 42), desc, fill=(201, 209, 217, 255), font=font_code)
        if y < 440:
            # Down arrow
            draw.line([(500, y + 75), (500, y + 95)], fill=(139, 148, 158, 200), width=2)
            draw.polygon([(495, y + 90), (505, y + 90), (500, y + 97)], fill=(139, 148, 158, 200))
        y += 95
    img.save("assets/images/posts/android-security/ch1-android-architecture.png", "PNG")
    print("Generated ch1-android-architecture.png")

# 2. Binder IPC Flow Diagram
def gen_ch1_binder():
    img, draw = create_base(1000, 580, "Binder Inter-Process Communication (IPC) Mechanism", "Synchronous RPC transaction flow and kernel-mediated token verification")
    # Client Process Box
    draw.rounded_rectangle([(60, 130), (320, 480)], radius=12, fill=(56, 189, 248, 20), outline=(56, 189, 248, 255), width=2)
    draw.text((80, 150), "Client Process (App)", fill=(56, 189, 248, 255), font=font_bold)
    draw.text((80, 180), "UID: 10087 (u0_a87)", fill=(139, 148, 158, 255), font=font_code)
    draw.rounded_rectangle([(80, 220), (300, 280)], radius=8, fill=(30, 41, 59, 200), outline=(56, 189, 248, 120), width=1)
    draw.text((95, 235), "Service Proxy (BpBinder)", fill=(240, 246, 252, 255), font=font_regular)
    draw.text((95, 255), "transact(CODE, parcel)", fill=(74, 222, 128, 255), font=font_code)
    draw.rounded_rectangle([(80, 320), (300, 380)], radius=8, fill=(30, 41, 59, 200), outline=(56, 189, 248, 120), width=1)
    draw.text((95, 335), "IPCThreadState", fill=(240, 246, 252, 255), font=font_regular)
    draw.text((95, 355), "ioctl(BINDER_WRITE_READ)", fill=(245, 158, 11, 255), font=font_code)

    # Kernel Box (Middle)
    draw.rounded_rectangle([(370, 130), (630, 480)], radius=12, fill=(239, 68, 68, 20), outline=(239, 68, 68, 255), width=2)
    draw.text((390, 150), "Linux Kernel Driver", fill=(239, 68, 68, 255), font=font_bold)
    draw.text((390, 180), "Device: /dev/binder", fill=(139, 148, 158, 255), font=font_code)
    draw.rounded_rectangle([(390, 220), (610, 320)], radius=8, fill=(30, 41, 59, 200), outline=(239, 68, 68, 120), width=1)
    draw.text((405, 235), "Kernel Mediation", fill=(240, 246, 252, 255), font=font_regular)
    draw.text((405, 260), "Injects Real Caller UID/PID", fill=(74, 222, 128, 255), font=font_code)
    draw.text((405, 285), "Direct Memory Copy (mmap)", fill=(56, 189, 248, 255), font=font_code)
    draw.rounded_rectangle([(390, 350), (610, 440)], radius=8, fill=(30, 41, 59, 200), outline=(239, 68, 68, 120), width=1)
    draw.text((405, 365), "Service Manager (Handle 0)", fill=(245, 158, 11, 255), font=font_regular)
    draw.text((405, 390), "Resolves string to handle", fill=(201, 209, 217, 255), font=font_code)
    draw.text((405, 412), "IPC Access Control Check", fill=(244, 63, 94, 255), font=font_code)

    # Server Process Box (Right)
    draw.rounded_rectangle([(680, 130), (940, 480)], radius=12, fill=(74, 222, 128, 20), outline=(74, 222, 128, 255), width=2)
    draw.text((700, 150), "Server Process (System)", fill=(74, 222, 128, 255), font=font_bold)
    draw.text((700, 180), "UID: 1000 (system_server)", fill=(139, 148, 158, 255), font=font_code)
    draw.rounded_rectangle([(700, 220), (920, 280)], radius=8, fill=(30, 41, 59, 200), outline=(74, 222, 128, 120), width=1)
    draw.text((715, 235), "Service Stub (BBinder)", fill=(240, 246, 252, 255), font=font_regular)
    draw.text((715, 255), "onTransact(CODE, parcel)", fill=(74, 222, 128, 255), font=font_code)
    draw.rounded_rectangle([(700, 320), (920, 420)], radius=8, fill=(30, 41, 59, 200), outline=(74, 222, 128, 120), width=1)
    draw.text((715, 335), "Security Verification", fill=(240, 246, 252, 255), font=font_regular)
    draw.text((715, 360), "Binder.getCallingUid()", fill=(245, 158, 11, 255), font=font_code)
    draw.text((715, 385), "checkCallingPermission()", fill=(239, 68, 68, 255), font=font_code)

    # Horizontal connection arrows
    draw.line([(300, 250), (390, 250)], fill=(56, 189, 248, 200), width=2)
    draw.line([(610, 250), (700, 250)], fill=(74, 222, 128, 200), width=2)

    img.save("assets/images/posts/android-security/ch1-binder-ipc.png", "PNG")
    print("Generated ch1-binder-ipc.png")

# 3. Permission Enforcement Architecture
def gen_ch2_permissions():
    img, draw = create_base(1000, 580, "Permission Enforcement & Verification Workflow", "From AndroidManifest declaration to runtime Binder hook enforcement")
    steps = [
        ("1. Manifest Declaration", "<permission android:protectionLevel=\"signature\" ... />\n<uses-permission android:name=\"android.permission.CAMERA\" />", (56, 189, 248)),
        ("2. Package Manager Parsing", "PackageManagerService parses XML -> verifies signatures -> assigns GIDs\nWrites state to /data/system/packages.xml and packages.list", (168, 85, 247)),
        ("3. Kernel GID Assignment", "Zygote forks process with setuid(UID) and setgroups(GIDs)\nParanoia network sockets (AID_INET 3003, AID_NET_RAW 3004)", (245, 158, 11)),
        ("4. System Service Enforcement", "Service method receives IPC -> invokes enforceCallingPermission()\nThrows SecurityException if caller UID does not hold permission", (239, 68, 68))
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
    img.save("assets/images/posts/android-security/ch2-permission-enforcement.png", "PNG")
    print("Generated ch2-permission-enforcement.png")

# 4. APK Signing Scheme
def gen_ch3_apk_signing():
    img, draw = create_base(1000, 580, "APK Structure & Jar Signature Verification", "Digest verification chain across MANIFEST.MF, CERT.SF, and CERT.RSA")
    # File boxes
    boxes = [
        ("ZIP Archive Entries", "classes.dex\nres/layout/main.xml\nAndroidManifest.xml\nassets/...", (96, 165, 250), 60),
        ("META-INF/MANIFEST.MF", "SHA-1-Digest of every\nindividual uncompressed\nfile inside the APK", (74, 222, 128), 290),
        ("META-INF/CERT.SF", "SHA-1-Digest of MANIFEST.MF\nplus per-entry digests\nof manifest sections", (245, 158, 11), 520),
        ("META-INF/CERT.RSA", "PKCS#7 SignedData\nDigital signature of CERT.SF\n+ Developer X.509 Cert", (239, 68, 68), 750)
    ]
    for title, desc, col, x in boxes:
        draw.rounded_rectangle([(x, 140), (x + 200, 460)], radius=10, fill=(col[0], col[1], col[2], 20), outline=col, width=2)
        draw.text((x + 15, 160), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        yy = 210
        for l in lines:
            draw.text((x + 15, yy), l, fill=(201, 209, 217, 255), font=font_code)
            yy += 25
    # Verification arrows from right to left
    draw.line([(750, 300), (720, 300)], fill=(239, 68, 68, 255), width=2)
    draw.line([(520, 300), (490, 300)], fill=(245, 158, 11, 255), width=2)
    draw.line([(290, 300), (260, 300)], fill=(74, 222, 128, 255), width=2)
    img.save("assets/images/posts/android-security/ch3-apk-signing.png", "PNG")
    print("Generated ch3-apk-signing.png")

# 5. Keystore Architecture
def gen_ch7_keystore():
    img, draw = create_base(1000, 580, "Android KeyStore & Hardware Cryptographic Pipeline", "Key isolation between user application, keystore daemon, and TEE Keymaster")
    # Columns
    cols = [
        ("Application Sandbox", "UID: 10087\nKeyStore Provider\njava.security.KeyStore\nEncrypted Key Handle", (56, 189, 248), 60),
        ("System Daemons", "UID: 1017 (keystore)\n/system/bin/keystore\n/data/misc/keystore\nMaster Key (AES-CBC)\nUser Lockscreen PBKDF2", (249, 115, 22), 370),
        ("TrustZone / TEE", "Secure World (Ring -1)\nKeymaster HAL Module\nHardware Root of Trust\nHardware-Enforced Keys\nNo Plaintext in Normal World", (74, 222, 128), 680)
    ]
    for title, desc, col, x in cols:
        draw.rounded_rectangle([(x, 140), (x + 260, 480)], radius=12, fill=(col[0], col[1], col[2], 20), outline=col, width=2)
        draw.text((x + 20, 165), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        yy = 220
        for l in lines:
            draw.text((x + 20, yy), l, fill=(201, 209, 217, 255), font=font_code)
            yy += 28
    # Connecting Arrows
    draw.line([(320, 300), (370, 300)], fill=(56, 189, 248, 255), width=2)
    draw.line([(630, 300), (680, 300)], fill=(249, 115, 22, 255), width=2)
    draw.text((325, 275), "Binder", fill=(139, 148, 158, 255), font=font_code)
    draw.text((640, 275), "SMC", fill=(139, 148, 158, 255), font=font_code)
    img.save("assets/images/posts/android-security/ch7-keystore-architecture.png", "PNG")
    print("Generated ch7-keystore-architecture.png")

# 6. Device Security (FDE & dm-verity)
def gen_ch10_device_security():
    img, draw = create_base(1000, 580, "Full Disk Encryption (FDE) & dm-verity Architecture", "Block-level cryptographic protection and hash-tree boot integrity verification")
    # Top Section: FDE
    draw.rounded_rectangle([(60, 130), (940, 280)], radius=10, fill=(239, 68, 68, 20), outline=(239, 68, 68, 255), width=2)
    draw.text((80, 145), "Full Disk Encryption (dm-crypt & crypto_footer)", fill=(239, 68, 68, 255), font=font_bold)
    draw.text((80, 180), "Header/Footer: /data/footer (16KB) contains encrypted Volume Encryption Key (VEK)", fill=(240, 246, 252, 255), font=font_code)
    draw.text((80, 210), "Key Derivation: User Password + Salt -> scrypt / PBKDF2 -> Keymaster HAL (TrustZone)", fill=(74, 222, 128, 255), font=font_code)
    draw.text((80, 240), "Driver: dm-crypt AES-128/256-CBC-ESSIV creates transparent /dev/block/dm-0 mapped device", fill=(201, 209, 217, 255), font=font_code)

    # Bottom Section: dm-verity
    draw.rounded_rectangle([(60, 320), (940, 500)], radius=10, fill=(56, 189, 248, 20), outline=(56, 189, 248, 255), width=2)
    draw.text((80, 335), "Verified Boot & dm-verity Hash Trees", fill=(56, 189, 248, 255), font=font_bold)
    draw.text((80, 370), "Root Hash: Cryptographically signed with OEM public key in the boot partition", fill=(240, 246, 252, 255), font=font_code)
    draw.text((80, 400), "Merkle Tree: Every 4KB block of /system is hashed -> layer-by-layer up to Root Hash", fill=(74, 222, 128, 255), font=font_code)
    draw.text((80, 430), "Integrity Enforcement: Transparent read-time hash check; block corruption raises EIO", fill=(201, 209, 217, 255), font=font_code)
    draw.text((80, 460), "Tamper Resistance: Modification of a single byte causes verification failure & boot halt", fill=(245, 158, 11, 255), font=font_code)

    img.save("assets/images/posts/android-security/ch10-fde-dmverity.png", "PNG")
    print("Generated ch10-fde-dmverity.png")

# 7. SELinux Architecture
def gen_ch12_selinux():
    img, draw = create_base(1000, 580, "SEAndroid Policy & Mandatory Access Control (MAC)", "Kernel security server mediation, Access Vector Cache (AVC), and type enforcement")
    # Subject, Security Server, Object
    cols = [
        ("Subject (Source)", "Process Context:\nu:r:untrusted_app:s0:c512,c768\n\nCalls open(\"/system/bin/sh\")", (14, 165, 233), 60),
        ("SELinux Subsystem", "Kernel Security Server\nCompiled Policy (sepolicy)\nAccess Vector Cache (AVC)\n\nRule:\nallow untrusted_app\nshell_exec:file { rx };", (74, 222, 128), 370),
        ("Object (Target)", "Object Context:\nu:object_r:shell_exec:s0\n\nFile node in /system/bin/sh\nExtended attribute (xattr):\nsecurity.selinux", (245, 158, 11), 680)
    ]
    for title, desc, col, x in cols:
        draw.rounded_rectangle([(x, 140), (x + 260, 460)], radius=12, fill=(col[0], col[1], col[2], 20), outline=col, width=2)
        draw.text((x + 20, 165), title, fill=col, font=font_bold)
        lines = desc.split("\n")
        yy = 220
        for l in lines:
            draw.text((x + 20, yy), l, fill=(201, 209, 217, 255), font=font_code)
            yy += 26
    # Connecting Arrows
    draw.line([(320, 300), (370, 300)], fill=(14, 165, 233, 255), width=2)
    draw.line([(630, 300), (680, 300)], fill=(74, 222, 128, 255), width=2)
    img.save("assets/images/posts/android-security/ch12-selinux-mac.png", "PNG")
    print("Generated ch12-selinux-mac.png")

if __name__ == "__main__":
    gen_ch1_architecture()
    gen_ch1_binder()
    gen_ch2_permissions()
    gen_ch3_apk_signing()
    gen_ch7_keystore()
    gen_ch10_device_security()
    gen_ch12_selinux()

