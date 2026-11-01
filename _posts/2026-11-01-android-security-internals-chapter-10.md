---
title: "Android Security Internals: Chapter 10 - Device Security"
date: 2026-11-01 18:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, full-disk-encryption, fde, fbe, dm-crypt, dm-verity, verified-boot, direct-boot]
description: "An exhaustive technical breakdown of Chapter 10 of Nikolay Elenkov's 'Android Security Internals', covering Full Disk Encryption (dm-crypt), File-Based Encryption (FBE), Direct Boot, crypto_footer layout, Keymaster key derivation, and Verified Boot (dm-verity) hash trees."
image:
  path: /assets/images/posts/android-security/chapter-10-cover.png
  alt: "Android Security Internals Chapter 10 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**, enriched with storage encryption analysis, File-Based Encryption (FBE), Direct Boot architecture, and Android Verified Boot (AVB 2.0).

Operating system access controls (such as Linux UIDs and SELinux policies) only protect data while the Android kernel is running. If an adversary steals a physical smartphone, connects high-speed hardware programmers to the eMMC flash chip, or boots a custom recovery kernel, all software-level protections vanish.

To counter physical and hardware attacks, Android implements two formidable defenses: **Storage Encryption** (Full Disk Encryption via `dm-crypt` and File-Based Encryption via `fscrypt`), and **Verified Boot** via `dm-verity`.

![Android Security Internals Chapter 10](/assets/images/posts/android-security/chapter-10-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| [Chapter 9: Enterprise Security](/posts/android-security-internals-chapter-9/) | **Chapter 10: Device Security** | [Chapter 11: NFC and Secure Elements](/posts/android-security-internals-chapter-11/) |

---

## Key Takeaways

* **The Physical Attack Threat**: Software sandboxes are irrelevant if an attacker can read raw flash memory sectors via chip-off forensics, JTAG debugging, or unauthorized bootloader flashing.
* **Full Disk Encryption (FDE)**: Android leverages the Linux kernel's `dm-crypt` subsystem to transparently encrypt the entire `/data` partition at the block level using AES-CBC-ESSIV or AES-XTS.
* **The `crypto_footer` Layout**: Metadata required to decrypt the volume resides in a 16 KB footer located at the physical end of the `/data` partition. It contains the encrypted Volume Encryption Key (VEK), salt, and KDF parameters.
* **Evolution to File-Based Encryption (FBE)**: In Android 7.0+, FDE was superseded by FBE, enabling **Direct Boot mode**. Storage is split into Credential Encrypted (CE) and Device Encrypted (DE) areas.
* **Hardware-Bound Key Derivation**: The encryption key is derived by passing the user's PIN/password through scrypt or PBKDF2, then signing or binding the result inside ARM TrustZone via the Keymaster HAL. Offline dictionary attacks on stolen flash chips are rendered impossible without the physical device silicon.
* **Verified Boot & `dm-verity`**: While FDE/FBE ensures confidentiality of user data at rest, `dm-verity` guarantees the cryptographic integrity of the read-only `/system` partition using a tree of SHA-256 hashes (Merkle Tree). Any byte modified on `/system` halts the device immediately.

---

## 1. Physical Device Partition Layout

Flash storage in an Android device is partitioned into specialized blocks:

```text
eMMC / UFS Physical Flash Storage
├── /boot          (Linux kernel + initial ramdisk rootfs)
├── /system        (Read-only OS binaries, framework JARs, system apps)
├── /recovery      (Minimal recovery kernel for OTA updates and wipes)
├── /cache         (Temporary download space for OTA update packages)
├── /vendor        (Proprietary OEM hardware binaries and HAL drivers)
├── /misc          (Bootloader control flags and recovery boot messages)
└── /data          (UserData: application sandboxes, databases, photos)
    └── [crypto_footer] (16 KB encrypted metadata at end of partition)
```

---

## 2. Full Disk Encryption (FDE) & `dm-crypt`

Full Disk Encryption protects all user data stored in the `/data` partition (`/userdata`).

![Full Disk Encryption and dm-verity Architecture](/assets/images/posts/android-security/ch10-fde-dmverity.png)

### The `dm-crypt` Kernel Driver

Android implements FDE using the Linux **Device Mapper (`dm`)** framework:
* When encryption is active, the physical partition (e.g., `/dev/block/mmcblk0p28`) is wrapped by the `dm-crypt` driver.
* The driver exposes a virtual mapped block device: `/dev/block/dm-0`.
* The ext4 filesystem is mounted onto `/dev/block/dm-0`.
* Whenever an application reads or writes data, `dm-crypt` transparently encrypts and decrypts 512-byte sectors on the fly using hardware-accelerated AES (AES-128-CBC with ESSIV or AES-256-XTS).

### The Volume Encryption Key (VEK)

The actual encryption of the disk blocks is performed using a randomly generated 128-bit or 256-bit symmetric key known as the **Volume Encryption Key (VEK)**.
* The VEK is never written to disk in plaintext.
* Instead, it is encrypted by a **Key Encryption Key (KEK)** derived from the user's lockscreen password and hardware secrets.

---

## 3. The `crypto_footer` Structure

At the final 16 KB offset of the `/data` partition resides the `crypto_footer`. Its internal C struct layout is defined in `system/vold/cryptfs.h`:

```c
struct crypt_footer {
    uint32_t magic;                   /* 0xD0B5B1C4 (Magic Identifier) */
    uint16_t major_version;           /* Crypto major version (e.g. 1) */
    uint16_t minor_version;           /* Crypto minor version (e.g. 3) */
    uint32_t ftr_size;                /* Size of footer struct */
    uint32_t flags;                   /* Encryption state flags */
    uint32_t key_size;                /* Key size in bytes (16 or 32) */
    uint32_t crypt_type;              /* AES-128-CBC-ESSIV or AES-XTS */
    uint64_t fs_size;                 /* Filesystem size in 512-byte sectors */
    uint32_t failed_decrypt_count;    /* Consecutive failed PIN attempts */
    char     crypto_type_name[64];    /* Cipher string name */
    uint32_t kdf_type;                /* 1 = PBKDF2, 2 = scrypt */
    uint8_t  kdf_salt[16];            /* Cryptographic salt for KDF */
    uint8_t  encrypted_key[32];       /* The encrypted VEK blob */
};
```

---

## 4. Modern Evolution: File-Based Encryption (FBE) & Direct Boot

In Android 7.0, Google introduced **File-Based Encryption (FBE)**, solving a major usability flaw of FDE: in FDE, the device could not perform basic functions (sound alarms, receive phone calls) after rebooting until the user entered their PIN.

### The Two FBE Storage Domains

1. **Credential Encrypted (CE) Storage**:
   * Encrypted using a key derived from the user's lockscreen PIN/password.
   * Path: `/data/user/0/<pkg>`
   * Inaccessible until the user unlocks the screen after boot.
2. **Device Encrypted (DE) Storage**:
   * Encrypted using a key tied exclusively to hardware secrets (accessible immediately on boot).
   * Path: `/data/user_de/0/<pkg>`
   * Enables **Direct Boot mode**: alarms, incoming calls, and accessibility services operate seamlessly before user unlock!

```xml
<!-- Supporting Direct Boot mode in AndroidManifest.xml -->
<receiver
    android:name=".AlarmReceiver"
    android:directBootAware="true"
    android:exported="false">
    <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED" />
    </intent-filter>
</receiver>
```

---

## 5. Verified Boot: `dm-verity` & AVB 2.0

While Full Disk Encryption guarantees data privacy, it does not prevent an adversary from tampering with the operating system binaries in `/system`.

Android solves this using **Verified Boot** powered by the kernel's **`dm-verity`** block integrity driver.

### The Merkle Hash Tree Architecture

Instead of calculating a single hash over the entire multi-gigabyte `/system` partition, `dm-verity` organizes hashes into a hierarchical **Merkle Tree**:

1. **Layer 0**: The `/system` partition is divided into 4096-byte (4 KB) blocks. A SHA-256 hash is computed for every individual block.
2. **Intermediate Layers**: Hashes from Layer 0 are grouped into 4 KB blocks, and each block is hashed again.
3. **The Root Hash**: At the apex sits a single 32-byte cryptographic hash: the **Root Hash**.
4. **AVB 2.0 (`vbmeta`)**: In modern Android Verified Boot 2.0, the root hash and partition descriptors are signed and packed into a dedicated `vbmeta` partition, verified directly by the hardware bootloader.

---

## Next in the Series: Chapter 11 Preview

In [Chapter 11: NFC and Secure Elements](/posts/android-security-internals-chapter-11/), we will analyze:

* The Near Field Communication (NFC) architecture stack and operating modes.
* Hardware Secure Elements: UICC (SIM cards) and embedded Secure Elements (eSE).
* Android 4.4's breakthrough: Host-based Card Emulation (HCE) and ISO 7816-4 APDU routing.
* Cloud tokenization architectures and NFC relay attack surfaces.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 10: "Device Security," pp. 251–288.
2. [Android Open Source Project - Verified Boot (AVB / dm-verity)](https://source.android.com/docs/security/features/verifiedboot)
3. [AOSP Documentation - Full-Disk Encryption Implementation Details](https://source.android.com/docs/security/features/encryption/full-disk)
4. Beniamini, Gal. *Extracting Qualcomm's KeyMaster Keys - Breaking Android Full Disk Encryption*. Project Zero, 2016.
5. Percival, Colin. *Stronger Key Derivation via Sequential Memory-Hard Functions (scrypt)*. BSDCan, 2009.

---

## Let's Connect

Have you audited mobile verified boot chains or analyzed storage encryption mechanisms?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
