---
title: "Android Security Internals: Chapter 7 - Credential Storage"
date: 2026-11-01 15:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, keystore, cryptography, trustzone, tee, keymaster, credentials]
description: "A rigorous technical analysis of Chapter 7 of Nikolay Elenkov's 'Android Security Internals', examining the keystore native daemon, master key derivation, hardware-backed keys, Keymaster HAL, and ARM TrustZone integration."
image:
  path: /assets/images/posts/android-security/chapter-7-cover.png
  alt: "Android Security Internals Chapter 7 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**.

In [Chapter 6](/posts/android-security-internals-chapter-6/), we dissected network security, the system CA store, and TLS certificate validation. In this installment, we explore **Chapter 7: Credential Storage**, examining the architecture responsible for protecting cryptographic keys, digital certificates, and user secrets when the device is at rest.

Storing private cryptographic keys on a mobile device presents a classic security paradox: **If malicious code or a local root exploit compromises the Android operating system, how can private keys remain secure?**

Android resolves this through a multi-layered credential subsystem anchored by the native `/system/bin/keystore` daemon, user-derived master keys, and hardware isolation powered by the Keymaster Hardware Abstraction Layer (HAL) running inside ARM TrustZone.

![Android Security Internals Chapter 7](/assets/images/posts/android-security/chapter-7-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| [Chapter 6: Network Security and PKI](/posts/android-security-internals-chapter-6/) | **Chapter 7: Credential Storage** | [Chapter 8: Online Account Management](/posts/android-security-internals-chapter-8/) |

---

## Key Takeaways

* **The Insecurity of Software Storage**: Storing cryptographic secrets in `SharedPreferences`, SQLite databases, or hardcoded strings leaves them vulnerable to backup extraction, memory dumping, and root compromise.
* **The `keystore` Daemon**: Android offloads key operations to `/system/bin/keystore`, a dedicated native daemon running under its own isolated UID (`1017`, `AID_KEYSTORE`).
* **Per-UID Key Namespaces**: Keys stored in the keystore are indexed by the calling application's Linux UID, cryptographically isolating one application's keys from another.
* **Master Key Derivation**: Keystore files on disk are encrypted using an AES master key, which is itself encrypted using a key derived from the user's lockscreen PIN/password via PBKDF2 or scrypt.
* **Hardware-Backed Root of Trust**: Modern Android integrates Keymaster HAL modules running inside ARM TrustZone (TEE). Private keys never enter Linux kernel or userspace RAM; cryptographic signing and decryption occur exclusively inside the secure enclave.

---

## 1. The Credential Storage Landscape

Before diving into the native KeyStore architecture, let's contrast the storage models available to Android applications:

| Storage Mechanism | Storage Path | Encryption State | Threat Exposure |
| :--- | :--- | :--- | :--- |
| **`SharedPreferences`** | `/data/data/<pkg>/shared_prefs/` | Plaintext XML | Trivial extraction via ADB backup or root |
| **SQLite Database** | `/data/data/<pkg>/databases/` | Plaintext binary | Direct extraction; requires third-party SQLCipher for encryption |
| **Internal Flash File** | `/data/data/<pkg>/files/` | Plaintext | Readable by any process sharing the UID or root |
| **Android KeyStore** | `/data/misc/keystore/` | Encrypted AES blob / TEE | Hardware-isolated; private keys never leave secure hardware |

---

## 2. The `keystore` Native Daemon

The core of Android's credential management is `/system/bin/keystore`, launched by `init` during boot:

```text
service keystore /system/bin/keystore /data/misc/keystore
    class main
    user keystore
    group keystore drmrpc readproc
```

![Android KeyStore Architecture](/assets/images/posts/android-security/ch7-keystore-architecture.png)

### IPC and UID Separation

1. **Client Interface**: Applications communicate with the daemon via the `android.security.KeyStore` Java wrapper, which sends Binder IPC requests to the `keystore` service.
2. **Caller UID Enforcement**: The `keystore` daemon interrogates the Binder kernel driver using `IPCThreadState::getCallingUid()` to determine the true caller UID.
3. **Storage Namespace**: Encrypted keys are saved to disk in `/data/misc/keystore/user_0/` using a strict naming pattern:
   ```text
   <caller_uid>_<key_type>_<key_alias>
   ```
   For example, an RSA private key named `auth_key` owned by UID `10087` is stored on disk as:
   ```text
   10087_USRPKEY_auth_key
   ```
   If UID `10088` attempts to read or sign with `auth_key`, the `keystore` daemon checks the calling UID against the file prefix and terminates the operation with a permission error.

---

## 3. Master Key Generation & Encryption Architecture

How does the `keystore` daemon protect keys written to physical flash memory?

### The Encryption Hierarchy

1. **The Master Key**: When credential storage is initialized, the daemon generates a 128-bit or 256-bit AES master key.
2. **Lockscreen Key Derivation**: When the user configures a lockscreen PIN or password:
   * The system passes the user's password string and a 128-bit random salt into a Key Derivation Function (PBKDF2 with HMAC-SHA1 or scrypt).
   * The derived key is used to encrypt the master key via AES-CBC.
   * The encrypted master key blob is saved to disk as `/data/misc/keystore/user_0/.masterkey`.
3. **Individual Key Encryption**: Every private key saved by an application is encrypted using the master key before being written to disk.

### Lock and Unlock States

* **Device Locked**: When the screen locks or device boots, the master key is purged from the `keystore` daemon's volatile memory. Any attempt to use keys encrypted with user authentication fails with `KeyStore.LOCKED`.
* **Device Unlocked**: When the user enters their PIN/password on the Keyguard screen, `LockSettingsService` sends the verified credentials over IPC to the `keystore` daemon. The daemon decrypts the master key into RAM, allowing applications to execute cryptographic operations.

---

## 4. Hardware-Backed Keys: Keymaster HAL & ARM TrustZone

Software encryption in userspace has a fatal vulnerability: if an attacker exploits a Linux kernel vulnerability to gain root privileges, they can read the master key directly from `keystore` daemon memory.

To neutralize this threat, Android introduced **hardware-backed credential storage** via the **Keymaster HAL**.

### ARM TrustZone Architecture

ARM processors feature two hardware execution states:
1. **Normal World (Non-Secure)**: Executes the Linux kernel, Android framework, system daemons, and all sandboxed applications.
2. **Secure World (Trusted Execution Environment - TEE)**: An entirely isolated hardware realm with its own memory space, secure registers, and dedicated microkernel (e.g., Qualcomm QSEE, Trusty OS).

Communication between the Normal World and Secure World occurs exclusively through a special processor instruction: **`SMC` (Secure Monitor Call)**.

### The Keymaster Hardware Pipeline

When an application generates a hardware-backed key:
1. The app calls `KeyPairGenerator.getInstance("RSA", "AndroidKeyStore")`.
2. The `keystore` daemon invokes the Keymaster HAL module (`keymaster.default.so`).
3. The HAL issues an `SMC` instruction to switch the CPU core into the Secure World.
4. **Key Generation in TEE**: The TEE generates the RSA private key using a hardware true random number generator (TRNG).
5. **Key Blob Wrapping**: The private key **never leaves the TEE in plaintext**. Instead, the TEE encrypts the private key using an internal device-unique hardware master key fused into the silicon during manufacturing.
6. The resulting encrypted key blob is handed back to Android userspace to store on flash.

### Signing in Hardware

When the app needs to sign a cryptographic challenge:
* The app sends the data to `keystore`.
* The `keystore` daemon passes the encrypted key blob and data to the Keymaster TEE.
* The TEE decrypts the key blob inside isolated secure memory, computes the digital signature, and returns only the completed signature to Android userspace.
* **Even a compromised Linux kernel running with full root access cannot extract the plaintext private key!**

Developers can verify hardware backing programmatically:

```java
KeyFactory factory = KeyFactory.getInstance("RSA", "AndroidKeyStore");
KeyInfo keyInfo = factory.getKeySpec(privateKey, KeyInfo.class);
boolean isHardwareBacked = keyInfo.isInsideSecureHardware();
```

---

## 5. `KeyChain` API vs. `AndroidKeyStore` Provider

Android provides two distinct APIs for credential operations:

### 1. The `KeyChain` API (`android.security.KeyChain`)
* **Purpose**: System-wide credential management for client authentication (enterprise mutual TLS, IPSec/IKEv2 VPNs, 802.1X corporate Wi-Fi).
* **User Interaction**: Invoking `KeyChain.choosePrivateKeyAlias()` triggers an interactive system activity prompting the user to select a certificate and authorize the requesting application.
* **Shared Access**: Multiple authorized applications can access the same imported certificate.

### 2. The `AndroidKeyStore` Provider
* **Purpose**: Application-private cryptographic keys.
* **User Interaction**: Zero user interaction; silent, programmatic key generation and usage.
* **Isolation**: Strictly private to the declaring application's UID; inaccessible to any other application on the device.

---

## 6. Attack Surfaces & Exploitation Vectors

### 1. Memory Dumping of Unlocked Master Keys
If a device is unlocked and an attacker obtains kernel root access, they can inspect the `/system/bin/keystore` process memory map (`/proc/<pid>/mem`) to dump the decrypted master key from volatile memory, decrypting all software-backed keys stored on disk.

### 2. Lockscreen Bypass via System Server Exploitation
If an attacker can compromise `system_server` before the device is unlocked, they can inject code into `LockSettingsService` or hook `KeyguardViewMediator` to simulate successful authentication, causing `keystore` to unlock without the user's password.

### 3. TEE & TrustZone Vulnerabilities
While hardware-backed keys resist OS-level attacks, vulnerabilities in the TEE microkernel itself (e.g., memory corruption bugs in Qualcomm's QSEE or TrustZone Widevine components) allow local attackers to execute arbitrary code in Secure World (Ring -1), extracting hardware-wrapped keys.

---

## Next in the Series: Chapter 8 Preview

In [Chapter 8: Online Account Management](/posts/android-security-internals-chapter-8/), we will examine:

* Centralized single sign-on via the `AccountManager` architecture.
* Developing custom authenticators with `AbstractAccountAuthenticator`.
* OAuth token delegation, caching in `accounts.db`, and invalidation.
* Security risks including account token hijacking and rogue authenticators.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 7: "Credential Storage," pp. 171–190.
2. [Android Developers - Hardware-backed Keystore Guide](https://developer.android.com/privacy-and-security/keystore)
3. [AOSP Documentation - Keymaster & KeyMint Architecture](https://source.android.com/docs/security/features/keystore)
4. [ARM TrustZone Technology Architecture Overview](https://www.arm.com/technologies/trustzone)
5. Beniamini, Gal. *Extracting Qualcomm's KeyMaster Keys - Breaking the Encryption of Android Full Disk Encryption*. Project Zero Research, 2016.

---

## Let's Connect

Have you analyzed Android hardware key attestation or audited KeyStore implementations?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
