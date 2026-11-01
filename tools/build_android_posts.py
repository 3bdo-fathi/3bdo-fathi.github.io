# Script to build all 13 chapters of Android Security Internals
import os
import re

posts_dir = "_posts"
os.makedirs(posts_dir, exist_ok=True)

chapters_data = [
    {
        "num": 1,
        "title": "Android's Security Model",
        "slug": "android-security-internals-chapter-1",
        "date": "2026-11-01 09:00:00 +0300",
        "desc": "An exhaustive technical breakdown of Chapter 1 of Nikolay Elenkov's 'Android Security Internals', analyzing multi-level sandboxing, Linux kernel isolation, Dalvik/ART virtual machine boundaries, and Binder IPC internals.",
        "cover": "/assets/images/posts/android-security/chapter-1-cover.png",
        "diagrams": [
            ("/assets/images/posts/android-security/ch1-android-architecture.png", "Android Multi-Tier Security Architecture"),
            ("/assets/images/posts/android-security/ch1-binder-ipc.png", "Binder Inter-Process Communication Mechanism")
        ],
        "prev_title": None,
        "prev_url": None,
        "next_title": "Chapter 2: Permissions Architecture",
        "next_url": "/posts/android-security-internals-chapter-2/"
    },
    {
        "num": 2,
        "title": "Permissions Architecture",
        "slug": "android-security-internals-chapter-2",
        "date": "2026-11-01 10:00:00 +0300",
        "desc": "An in-depth technical analysis of Chapter 2 of Nikolay Elenkov's 'Android Security Internals', detailing manifest definitions, protection levels, kernel GID mapping, runtime Binder checks, and content provider URI permissions.",
        "cover": "/assets/images/posts/android-security/chapter-2-cover.png",
        "diagrams": [
            ("/assets/images/posts/android-security/ch2-permission-enforcement.png", "Permission Enforcement & Verification Workflow")
        ],
        "prev_title": "Chapter 1: Android's Security Model",
        "prev_url": "/posts/android-security-internals-chapter-1/",
        "next_title": "Chapter 3: Package Management",
        "next_url": "/posts/android-security-internals-chapter-3/"
    },
    {
        "num": 3,
        "title": "Package Management",
        "slug": "android-security-internals-chapter-3",
        "date": "2026-11-01 11:00:00 +0300",
        "desc": "An in-depth technical breakdown of Chapter 3 of Nikolay Elenkov's 'Android Security Internals', exploring APK zip file anatomy, DEX bytecode structure, JAR/APK signing schemes, package verification, and installd internals.",
        "cover": "/assets/images/posts/android-security/chapter-3-cover.png",
        "diagrams": [
            ("/assets/images/posts/android-security/ch3-apk-signing.png", "APK Structure & Jar Signature Verification")
        ],
        "prev_title": "Chapter 2: Permissions Architecture",
        "prev_url": "/posts/android-security-internals-chapter-2/",
        "next_title": "Chapter 4: User Management",
        "next_url": "/posts/android-security-internals-chapter-4/"
    },
    {
        "num": 4,
        "title": "User Management",
        "slug": "android-security-internals-chapter-4",
        "date": "2026-11-01 12:00:00 +0300",
        "desc": "A technical dissection of Chapter 4 of Nikolay Elenkov's 'Android Security Internals', covering Android multi-user architecture, UID mathematical mapping formulas, per-user storage virtualization, and UserManagerService internals.",
        "cover": "/assets/images/posts/android-security/chapter-4-cover.png",
        "diagrams": [],
        "prev_title": "Chapter 3: Package Management",
        "prev_url": "/posts/android-security-internals-chapter-3/",
        "next_title": "Chapter 5: Cryptographic Providers",
        "next_url": "/posts/android-security-internals-chapter-5/"
    },
    {
        "num": 5,
        "title": "Cryptographic Providers",
        "slug": "android-security-internals-chapter-5",
        "date": "2026-11-01 13:00:00 +0300",
        "desc": "An exhaustive analysis of Chapter 5 of Nikolay Elenkov's 'Android Security Internals', investigating the Java Cryptography Architecture (JCA), AndroidOpenSSL, Bouncy Castle, SecureRandom entropy flaws, and CVE-2013-7372.",
        "cover": "/assets/images/posts/android-security/chapter-5-cover.png",
        "diagrams": [],
        "prev_title": "Chapter 4: User Management",
        "prev_url": "/posts/android-security-internals-chapter-4/",
        "next_title": "Chapter 6: Network Security and PKI",
        "next_url": "/posts/android-security-internals-chapter-6/"
    },
    {
        "num": 6,
        "title": "Network Security and PKI",
        "slug": "android-security-internals-chapter-6",
        "date": "2026-11-01 14:00:00 +0300",
        "desc": "A deep technical exploration of Chapter 6 of Nikolay Elenkov's 'Android Security Internals', dissecting Android's TLS/SSL stack, TrustManager validation, system CA stores, certificate pinning, and MITM interception vectors.",
        "cover": "/assets/images/posts/android-security/chapter-6-cover.png",
        "diagrams": [],
        "prev_title": "Chapter 5: Cryptographic Providers",
        "prev_url": "/posts/android-security-internals-chapter-5/",
        "next_title": "Chapter 7: Credential Storage",
        "next_url": "/posts/android-security-internals-chapter-7/"
    },
    {
        "num": 7,
        "title": "Credential Storage",
        "slug": "android-security-internals-chapter-7",
        "date": "2026-11-01 15:00:00 +0300",
        "desc": "A rigorous technical analysis of Chapter 7 of Nikolay Elenkov's 'Android Security Internals', examining the keystore native daemon, master key derivation, hardware-backed keys, Keymaster HAL, and ARM TrustZone integration.",
        "cover": "/assets/images/posts/android-security/chapter-7-cover.png",
        "diagrams": [
            ("/assets/images/posts/android-security/ch7-keystore-architecture.png", "Android KeyStore & Hardware Cryptographic Pipeline")
        ],
        "prev_title": "Chapter 6: Network Security and PKI",
        "prev_url": "/posts/android-security-internals-chapter-6/",
        "next_title": "Chapter 8: Online Account Management",
        "next_url": "/posts/android-security-internals-chapter-8/"
    },
    {
        "num": 8,
        "title": "Online Account Management",
        "slug": "android-security-internals-chapter-8",
        "date": "2026-11-01 16:00:00 +0300",
        "desc": "A technical breakdown of Chapter 8 of Nikolay Elenkov's 'Android Security Internals', focusing on AccountManagerService, AbstractAccountAuthenticator, token delegation protocols, and OAuth security boundaries.",
        "cover": "/assets/images/posts/android-security/chapter-8-cover.png",
        "diagrams": [],
        "prev_title": "Chapter 7: Credential Storage",
        "prev_url": "/posts/android-security-internals-chapter-7/",
        "next_title": "Chapter 9: Enterprise Security",
        "next_url": "/posts/android-security-internals-chapter-9/"
    },
    {
        "num": 9,
        "title": "Enterprise Security",
        "slug": "android-security-internals-chapter-9",
        "date": "2026-11-01 17:00:00 +0300",
        "desc": "An in-depth review of Chapter 9 of Nikolay Elenkov's 'Android Security Internals', evaluating Device Administration APIs, DevicePolicyManagerService, enterprise containerization, Samsung KNOX, and MDM policy enforcement.",
        "cover": "/assets/images/posts/android-security/chapter-9-cover.png",
        "diagrams": [],
        "prev_title": "Chapter 8: Online Account Management",
        "prev_url": "/posts/android-security-internals-chapter-8/",
        "next_title": "Chapter 10: Device Security",
        "next_url": "/posts/android-security-internals-chapter-10/"
    },
    {
        "num": 10,
        "title": "Device Security",
        "slug": "android-security-internals-chapter-10",
        "date": "2026-11-01 18:00:00 +0300",
        "desc": "An exhaustive technical breakdown of Chapter 10 of Nikolay Elenkov's 'Android Security Internals', covering Full Disk Encryption (dm-crypt), crypto_footer layout, Keymaster key derivation, and Verified Boot (dm-verity) hash trees.",
        "cover": "/assets/images/posts/android-security/chapter-10-cover.png",
        "diagrams": [
            ("/assets/images/posts/android-security/ch10-fde-dmverity.png", "Full Disk Encryption & dm-verity Architecture")
        ],
        "prev_title": "Chapter 9: Enterprise Security",
        "prev_url": "/posts/android-security-internals-chapter-9/",
        "next_title": "Chapter 11: NFC and Secure Elements",
        "next_url": "/posts/android-security-internals-chapter-11/"
    },
    {
        "num": 11,
        "title": "NFC and Secure Elements",
        "slug": "android-security-internals-chapter-11",
        "date": "2026-11-01 19:00:00 +0300",
        "desc": "A technical dissection of Chapter 11 of Nikolay Elenkov's 'Android Security Internals', examining the NFC architecture stack, Host-based Card Emulation (HCE), ISO 7816-4 APDU routing, and hardware Secure Elements (UICC/eSE).",
        "cover": "/assets/images/posts/android-security/chapter-11-cover.png",
        "diagrams": [],
        "prev_title": "Chapter 10: Device Security",
        "prev_url": "/posts/android-security-internals-chapter-10/",
        "next_title": "Chapter 12: SELinux in Android",
        "next_url": "/posts/android-security-internals-chapter-12/"
    },
    {
        "num": 12,
        "title": "SELinux in Android",
        "slug": "android-security-internals-chapter-12",
        "date": "2026-11-01 20:00:00 +0300",
        "desc": "An in-depth analysis of Chapter 12 of Nikolay Elenkov's 'Android Security Internals', dissecting SEAndroid Mandatory Access Control (MAC), kernel policy enforcement, domain transitions, and mac_permissions.xml mapping.",
        "cover": "/assets/images/posts/android-security/chapter-12-cover.png",
        "diagrams": [
            ("/assets/images/posts/android-security/ch12-selinux-mac.png", "SEAndroid Policy & Mandatory Access Control (MAC)")
        ],
        "prev_title": "Chapter 11: NFC and Secure Elements",
        "prev_url": "/posts/android-security-internals-chapter-11/",
        "next_title": "Chapter 13: System Updates and Root Access",
        "next_url": "/posts/android-security-internals-chapter-13/"
    },
    {
        "num": 13,
        "title": "System Updates and Root Access",
        "slug": "android-security-internals-chapter-13",
        "date": "2026-11-01 21:00:00 +0300",
        "desc": "A comprehensive technical conclusion analyzing Chapter 13 of Nikolay Elenkov's 'Android Security Internals', covering Recovery OS mechanics, OTA update verification, privilege escalation exploits, su daemons, and modern root management.",
        "cover": "/assets/images/posts/android-security/chapter-13-cover.png",
        "diagrams": [],
        "prev_title": "Chapter 12: SELinux in Android",
        "prev_url": "/posts/android-security-internals-chapter-12/",
        "next_title": None,
        "next_url": None
    }
]

print(f"Loaded configuration for {len(chapters_data)} chapters.")

