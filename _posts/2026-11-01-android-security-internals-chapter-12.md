---
title: "Android Security Internals: Chapter 12 - SELinux in Android"
date: 2026-11-01 20:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, selinux, seandroid, mac, access-control, kernel, avc]
description: "An in-depth analysis of Chapter 12 of Nikolay Elenkov's 'Android Security Internals', dissecting SEAndroid Mandatory Access Control (MAC), kernel policy enforcement, domain transitions, and mac_permissions.xml mapping."
image:
  path: /assets/images/posts/android-security/chapter-12-cover.png
  alt: "Android Security Internals Chapter 12 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**.

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
* **Domain Transitions**: Processes cannot execute arbitrary binaries with inherited privileges. Launching an executable triggers a strict, policy-defined **domain transition** (e.g., `init` transitions to `zygote`, which transitions to `untrusted_app`).

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

Policy rules dictate interactions between a **Source Domain** (the process) and a **Target Type** (the file, socket, or service):

```text
allow <source_domain> <target_type>:<class> { <permissions> };
```

#### Real-World Policy Examples:

```text
# Allow untrusted applications to read and write their own data files
allow untrusted_app app_data_file:file { read write open getattr };

# Allow system_server to read property files
allow system_server system_file:file { read open getattr execute };

# Compile-time assertion: NEVER allow third-party apps to access raw block devices!
neverallow untrusted_app block_device:blk_file { read write open };
```

---

## 4. The Policy Compilation & Labeling Pipeline

Android's SELinux policy is compiled during OS build time and consists of several interconnected configuration files:

```text
AOSP / Device Vendor Policy Source
├── /external/sepolicy/*.te          (Type enforcement rules)
├── file_contexts                    (Path regex -> object contexts)
├── property_contexts                (System property -> context)
├── service_contexts                 (Binder service name -> context)
├── seapp_contexts                   (App metadata -> process domain)
└── mac_permissions.xml              (Signature certs -> seinfo tags)
             |
             v [checkpolicy compiler]
       /sepolicy (Compiled monolithic binary loaded into kernel at boot)
```

### The Three-Stage App Labeling Process

When an application is launched, Android determines its SELinux process context through three configuration files:

#### 1. `mac_permissions.xml`
Inspects the APK's cryptographic signing certificate:

```xml
<!-- System apps signed with platform certificate receive "platform" seinfo -->
<signer signature="@PLATFORM">
    <seinfo value="platform" />
</signer>

<!-- Default untrusted third-party apps -->
<default>
    <seinfo value="default" />
</default>
```

#### 2. `seapp_contexts`
Maps the `seinfo` tag and UID boundaries to a target process domain and filesystem type:

```text
# Third-party applications
user=_app seinfo=default domain=untrusted_app type=app_data_file

# System platform applications
user=system seinfo=platform domain=system_app type=system_app_data_file

# Isolated browser processes
user=_isolated domain=isolated_app
```

#### 3. `file_contexts`
Assigns initial contexts to partition paths on flash storage:

```text
/system(/.*)?           u:object_r:system_file:s0
/data/data/.*           u:object_r:app_data_file:s0
/dev/binder             u:object_r:binder_device:s0
/dev/socket/zygote      u:object_r:zygote_socket:s0
```

---

## 5. Domain Transitions: Controlled Execution

In standard Linux, when process A executes binary B via `execve()`, binary B inherits process A's UID and privileges.

In SEAndroid, processes cannot arbitrarily transition between security domains. Transitions occur only if explicitly authorized by a **`domain_auto_trans`** policy macro:

```text
domain_auto_trans(init, zygote_exec, zygote)
```

This macro expands to three required TE rules:
1. `allow init zygote_exec:file { execute open read getattr };` (Init can execute the binary).
2. `allow init zygote:process transition;` (Init is permitted to transition to the zygote domain).
3. `allow zygote zygote_exec:file entrypoint;` (`zygote_exec` is a valid entrypoint for the zygote domain).

Because third-party applications running in `untrusted_app` lack transition rules to privileged domains, executing a setuid root binary or shell script inside an app sandbox simply keeps the resulting process locked inside the constrained `untrusted_app` domain!

---

## 6. SELinux Enforcement Modes & Exploitation Vectors

### Operating Modes

Android supports two operating modes:
* **`Permissive`**: SELinux evaluates rules and logs AVC denials to `dmesg` / `logcat`, but does **not** block unauthorized operations. Used during device bringup and debugging.
* **`Enforcing`**: All rules are strictly enforced; unauthorized operations are halted immediately with `EACCES`.

Current status can be inspected via ADB:
```bash
# Check enforcement mode
getenforce
# Output: Enforcing
```

### Offensive Exploitation Techniques

1. **Kernel Memory Corruption**: Because the enforcement state is stored in a single integer variable (`selinux_enforcing`) inside kernel memory, an attacker who achieves arbitrary kernel write can overwrite this variable to `0`, transitioning the device into `Permissive` mode dynamically!
2. **Permissive Domain Traversal**: Vulnerability researchers audit compiled policies using tools like `sesearch` to identify permissive domains or overprivileged daemons that possess transition rules to unrestricted contexts.
3. **Exploiting Untrusted App Transitions**: Historically, vendor customizations frequently introduced flawed policy rules (e.g., allowing `untrusted_app` to communicate directly with proprietary `/dev/` driver nodes), providing direct attack paths to exploit unpatched kernel drivers.

---

## Next in the Series: Chapter 13 Preview

In [Chapter 13: System Updates and Root Access](/posts/android-security-internals-chapter-13/), we conclude the series with:

* The Recovery OS architecture and Over-The-Air (OTA) update verification.
* Edify scripting and cryptographic signature validation of update packages.
* The evolution of Android rooting: soft root vs. hard root.
* Daemonized `su` architectures, SELinux policy live-patching, and modern root detection evasion.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 12: "SELinux," pp. 319–348.
2. [Android Open Source Project - Security-Enhanced Linux in Android](https://source.android.com/docs/security/features/selinux)
3. Smalley, Stephen, and Craig, Robert. *Security Enhanced (SE) Android: Bringing Flexible MAC to Android*. Network and Distributed System Security Symposium (NDSS), 2013.
4. [SELinux Project Wiki & Policy Language Specification](https://selinuxproject.org/)
5. Tresys Technology. *SELinux by Example: Using Security Engineered Linux*. Prentice Hall, 2006.

---

## Let's Connect

Have you developed custom SEAndroid policies or audited Android device firmware for AVC denials?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
