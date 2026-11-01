---
title: "Android Security Internals: Chapter 12 - SELinux in Android"
date: 2026-11-01 20:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, selinux, seandroid, mac, access-control, kernel, avc, treble]
description: "An in-depth analysis of Chapter 12 of Nikolay Elenkov's 'Android Security Internals', dissecting SEAndroid Mandatory Access Control (MAC), kernel policy enforcement, domain transitions, Project Treble split policies, and mac_permissions.xml mapping."
image:
  path: /assets/images/posts/android-security/chapter-12-cover.png
  alt: "Android Security Internals Chapter 12 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**, enriched with kernel security research, Project Treble architecture, and mandatory access control exploitation tradecraft.

In [Chapter 11](/posts/android-security-internals-chapter-11/), we investigated NFC architecture, Host-based Card Emulation, and smart card protocols. In this installment, we explore **Chapter 12: SELinux in Android**, dissecting the single most impactful security enhancement introduced to the platform: **Security-Enhanced Linux (SEAndroid)**.

Before Android 4.3, Android's security model relied entirely on Discretionary Access Control (DAC) through Linux UIDs. This created an all-or-nothing vulnerability: **if an attacker compromised a daemon running as `root` (UID 0), the game was over.** The attacker had unfettered access to all files, devices, memory regions, and kernel system calls.

SELinux dismantled this paradigm by introducing **Mandatory Access Control (MAC)**, enforcing strict containment rules that confine processes even if they run as root.

![Android Security Internals Chapter 12](/assets/images/posts/android-security/chapter-12-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| [Chapter 11: NFC and Secure Elements](/posts/android-security-internals-chapter-11/) | **Chapter 12: SELinux in Android** | [Chapter 13: System Updates and Root Access](/posts/android-security-internals-chapter-13/) |

---

## Key Takeaways

* **DAC vs. MAC**: Discretionary Access Control allows object owners to set permissions, meaning a compromised root process owns the system. Mandatory Access Control enforces a centralized policy compiled into the kernel that no userspace process—not even root—can alter or bypass.
* **The SEAndroid Architecture**: SELinux hooks into the Linux kernel via Linux Security Modules (LSM). Access decisions are evaluated by the Security Server and cached in the Access Vector Cache (AVC) for wire-speed performance.
* **Security Context Anatomy**: Every process and filesystem object is tagged with a label formatted as `user:role:type:sensitivity[:categories]` (e.g., `u:r:untrusted_app:s0:c512,c768`).
* **The Android Policy Mapping Pipeline**: Android maps apps to SELinux domains during installation and launch using a combination of `mac_permissions.xml` (signature-based keys), `seapp_contexts`, and `file_contexts`.
* **Project Treble Split Policy**: In Android 8.0+, monolithic policies were split into `plat_sepolicy` (Google-maintained core) and `vendor_sepolicy` (OEM hardware drivers), preventing OEMs from weakening core platform security rules.

---

## 1. The Fall of DAC: Why Linux UIDs Were Not Enough

Under traditional Linux Discretionary Access Control (DAC):
* The superuser (`root`, UID `0`) bypasses all standard permission checks (`rwxrwxrwx`).
* Core system daemons (`vold`, `netd`, `installd`, `debuggerd`, `rild`) traditionally executed as UID `0`.
* A single memory corruption vulnerability (buffer overflow, format string, or integer overflow) in any of these daemons handed the attacker full root execution, disabling security mechanisms and compromising user privacy.

To contain vulnerabilities, Android integrated the NSA's **Security-Enhanced Linux (SELinux)** framework, operating on the principle of **Least Privilege**.

---

## 2. SEAndroid Architecture & Kernel Mediation

SELinux operates at the lowest levels of the Linux kernel:

![SEAndroid Policy and Mandatory Access Control](/assets/images/posts/android-security/ch12-selinux-mac.png)

### The Decision Pipeline

1. **Operation Attempt**: A process (Subject) executes a system call attempting an operation (e.g., `open("/system/bin/sh", O_RDONLY)`) against an Object.
2. **Standard DAC Check**: The kernel evaluates standard Linux UID/GID permissions. If DAC denies the request, the call fails immediately.
3. **LSM Hook & AVC Cache**: If DAC allows it, the kernel Linux Security Module (LSM) hook intercepts the operation and queries the **Access Vector Cache (AVC)** in RAM.
4. **Security Server Evaluation**:
   * If a matching rule exists in the AVC cache, the cached allow/deny decision is returned instantly.
   * If there is a cache miss, the kernel Security Server evaluates the loaded compiled binary policy (`/sepolicy`), caches the decision, and either permits the syscall or logs an **AVC Denial** audit event (`avc: denied`).

---

## 3. SELinux Security Contexts & Type Enforcement

In SEAndroid, access control is governed primarily by **Type Enforcement (TE)**.

### The Security Context String

Every process, file node, device socket, and Binder handle has an associated security context:

```text
u:r:untrusted_app:s0:c512,c768
| |       |       |     |
| |       |       |     +--> Multi-Category Security (MCS Categories)
| |       |       +--------> Sensitivity Level (s0 = standard)
| |       +----------------> Type / Domain (untrusted_app)
| +------------------------> Role (r = process role, object_r = file/device)
+--------------------------> User (u = system default user)
```

### The Type Enforcement Rule Syntax

```text
# Allow untrusted applications to read and write their own data files
allow untrusted_app app_data_file:file { read write open getattr };

# Compile-time assertion: NEVER allow third-party apps to access raw block devices!
neverallow untrusted_app block_device:blk_file { read write open };
```

---

## 4. The Treble Policy Architecture Split

In Android 8.0, Google introduced **Project Treble**, re-architecting SELinux from a single monolithic policy into a modular, split-policy hierarchy:

```text
/system/etc/selinux/plat_sepolicy.cil   (Platform Policy - Owned by Google)
/vendor/etc/selinux/vendor_sepolicy.cil (Vendor Policy - Hardware HALs)
/system/etc/selinux/mapping/            (Compatibility version mapping)
```

This prevents hardware vendors from accidentally weakening core application sandboxes or introducing permissive exceptions into system domains!

---

## 5. Kernel-Level SELinux Exploitation

When security researchers achieve arbitrary kernel read/write, how do they neutralize SELinux?

### 1. Overwriting `selinux_enforcing`
In older kernels, the global variable `selinux_enforcing` determined the enforcement state:
```bash
# Setting this integer to 0 transitions SELinux to Permissive mode!
```

### 2. Overwriting Process Credentials (`current->cred`)
In modern kernels with read-only memory protections on `selinux_enforcing`, attackers locate their process's `task_struct` in kernel memory:
* Locates the `cred` struct pointer.
* Overwrites `cred->security` with the security label of the `kernel` or `init` domain (`u:r:kernel:s0`).
* The process immediately inherits unrestricted kernel privileges, bypassing all AVC checks!

---

## Next in the Series: Chapter 13 Preview

In [Chapter 13: System Updates and Root Access](/posts/android-security-internals-chapter-13/), we conclude the series with:

* The Recovery OS architecture and Over-The-Air (OTA) update verification.
* Edify scripting and cryptographic signature validation of update packages.
* The evolution of Android rooting: soft root vs. hard root.
* Daemonized `su` architectures, Magisk systemless root, KernelSU, and hardware attestation bypasses.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 12: "SELinux," pp. 319–348.
2. [Android Open Source Project - Security-Enhanced Linux in Android](https://source.android.com/docs/security/features/selinux)
3. Smalley, Stephen, and Craig, Robert. *Security Enhanced (SE) Android: Bringing Flexible MAC to Android*. NDSS, 2013.
4. [AOSP Documentation - Project Treble SELinux Policy Architecture](https://source.android.com/docs/core/architecture/kernel/sepolicy)
5. Tresys Technology. *SELinux by Example: Using Security Engineered Linux*. Prentice Hall, 2006.

---

## Let's Connect

Have you developed custom SEAndroid policies or audited Android device firmware for AVC denials?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
