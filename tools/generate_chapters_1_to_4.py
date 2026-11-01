# Generator for Chapters 1 through 4
import os

posts_dir = "_posts"
os.makedirs(posts_dir, exist_ok=True)

def write_post(filename, content):
    filepath = os.path.join(posts_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created {filepath}")

# Chapter 1
ch1_content = """---
title: "Android Security Internals: Chapter 1 - Android's Security Model"
date: 2026-11-01 09:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, linux kernel, binder, sandboxing, dalvik, architecture]
description: "An exhaustive technical breakdown of Chapter 1 of Nikolay Elenkov's 'Android Security Internals', analyzing multi-level sandboxing, Linux kernel isolation, Dalvik/ART virtual machine boundaries, and Binder IPC internals."
image:
  path: /assets/images/posts/android-security/chapter-1-cover.png
  alt: "Android Security Internals Chapter 1 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome to the inaugural post of our deep-dive book summary series covering **"Android Security Internals: An In-Depth Guide to Android's Security Architecture"** by **Nikolay Elenkov** (No Starch Press).

Android is the most widely deployed operating system on the planet, running on billions of smartphones, tablets, IoT devices, automotive infotainment systems, and enterprise wearables. While traditional operating systems rely heavily on discretionary user accounts and network-perimeter firewalls, Android was engineered from the ground up on a radical security paradigm: **treating every single installed application as an untrusted, mutually hostile tenant on a multi-user Linux system.**

In this chapter, we dissect the foundational pillars of the Android security model: the modified Linux kernel, userspace privilege separation, Dalvik/ART runtime isolation, and the low-level mechanics of the Binder Inter-Process Communication (IPC) subsystem.

![Android Security Internals Chapter 1](/assets/images/posts/android-security/chapter-1-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| *First Chapter in Series* | **Chapter 1: Android's Security Model** | [Chapter 2: Permissions Architecture](/posts/android-security-internals-chapter-2/) |

---

## Key Takeaways

* **Defense in Depth**: Android implements multi-tiered security boundaries. A compromise at the application layer must bypass runtime controls, Binder IPC authentication, Linux UID/GID boundaries, and SELinux mandatory access controls before reaching the kernel.
* **The Application Sandbox**: Android fundamentally repurposed Linux multi-user architecture. Instead of mapping one human user to a UID, each installed application is assigned a unique, immutable Linux User ID (UID) starting at `10000` (`AID_APP`).
* **Kernel Androidisms**: Google modified the standard upstream Linux kernel by introducing custom subsystems including Ashmem (Anonymous Shared Memory), the Low Memory Killer (LMK), Paranoid Network Routing, and the high-performance `/dev/binder` driver.
* **The Zygote Spawning Model**: All Dalvik/ART application processes are forked from a pre-warmed parent daemon called `zygote`. This enables Copy-on-Write (COW) memory sharing of core framework libraries and guarantees rapid startup times.
* **Binder as the Security Backbone**: Inter-Process Communication (IPC) does not rely on traditional POSIX pipes or System V queues. The Binder kernel driver mediates all cross-process messaging, cryptographically enforcing caller UID and PID tokens that cannot be forged by userspace.

---

## 1. Architectural Overview: Multi-Tier Isolation

Android's architecture separates untrusted userland applications from high-privilege hardware interfaces and operating system daemons through distinct hierarchical layers:

![Android Multi-Tier Security Architecture](/assets/images/posts/android-security/ch1-android-architecture.png)

### The Layer Hierarchy

1. **Linux Kernel**: Serves as the ultimate hardware abstraction layer and security enforcer. Provides process isolation, memory protection, hardware drivers, and kernel-level mandatory access control (SELinux).
2. **Native Userspace & Hardware Abstraction Layer (HAL)**: Contains low-level native binaries (`init`, `vold`, `netd`, `keystore`, `installd`, `servicemanager`) and vendor-specific dynamic libraries (`.so`) that expose hardware capabilities (camera, audio, radio, sensors) without revealing proprietary hardware registers to upper layers.
3. **Android Runtime (ART / Dalvik)**: Executes compiled Dalvik Executable (`.dex`) bytecode inside managed memory spaces with garbage collection, JIT/AOT compilation, and strict memory safety boundaries.
4. **Application Framework**: Houses system services compiled into Java bytecode running inside the monolithic `system_server` process. Services include `ActivityManagerService` (AMS), `PackageManagerService` (PMS), `WindowManagerService` (WMS), and `ConnectivityService`.
5. **Application Sandbox**: User-installed applications and non-privileged pre-installed system apps. Each application runs inside its own isolated Linux process under a unique UID.

---

## 2. Kernel Hardening & "Androidisms"

Rather than deploying a standard GNU/Linux distribution, Google modified the upstream Linux kernel to accommodate battery, memory, and security constraints peculiar to mobile devices.

### Ashmem (Anonymous Shared Memory)

Traditional POSIX shared memory (`shmget`, `shmat`) exposes broad memory regions that persist across application lifecycles and lack fine-grained access revocation. Android implemented **Ashmem**, accessible via `/dev/ashmem`:

* Ashmem allows processes to share memory buffers via file descriptor passing over Binder IPC.
* Provides a kernel-level memory reclamation mechanism known as **pinning and unpinning**.
* When system memory is constrained, the kernel can purge unpinned Ashmem memory pages without terminating the owner process.
* If a process attempts to access an unpinned region that was purged, the kernel returns an error code, requiring graceful handling.

### Low Memory Killer (LMK)

Android does not utilize a swap partition on physical flash storage due to flash wear-leveling and write endurance limits. Instead, the kernel's Low Memory Killer monitors available memory thresholds and kills processes based on their Out-Of-Memory adjustment score (`oom_score_adj`), located in `/proc/[pid]/oom_score_adj`:

| Process Category | `oom_score_adj` Range | Description |
| :--- | :--- | :--- |
| **Foreground App** | `0` | Active application visible on screen interacting with the user |
| **Visible App** | `100` | Process hosting an activity visible but partially obscured (e.g., dialog overlay) |
| **Perceptible App** | `200` | Background process executing user-audible work (e.g., music playback) |
| **Service App** | `500` | Background service performing pending network or synchronization tasks |
| **Cached / Empty App**| `900 - 1000` | Process with no active components retained in RAM for fast relaunch |

### Paranoid Networking (Socket Restraints)

In standard desktop Linux, any local process can open network sockets via `socket(AF_INET, SOCK_STREAM, 0)`. Android historically restricted raw network socket creation by patching the Linux kernel network stack (`af_inet.c`) to inspect process supplementary group IDs (GIDs):

* `AID_INET` (GID `3003`): Required to create IP sockets (`SOCK_STREAM`, `SOCK_DGRAM`).
* `AID_NET_RAW` (GID `3004`): Required to create raw sockets (`SOCK_RAW`) or packet sockets (`AF_PACKET`).
* If an application lacks the `android.permission.INTERNET` permission in its manifest, the Android framework omits GID `3003` when forking its process, causing the kernel `socket()` system call to fail immediately with `EACCES` (Permission Denied).

---

## 3. Sandboxing & Process Isolation: The UID/GID Mapping

The cornerstone of Android's application isolation is the transformation of the traditional Linux multi-user security model into an application-level isolation sandbox.

### UID Allocation Matrix

Android reserves specific ranges of Linux UIDs for system daemons, hardware components, and sandboxed applications:

```text
0          - AID_ROOT (Kernel root user)
1000       - AID_SYSTEM (System server and core management framework)
1001       - AID_RADIO (Telephony and RIL subsystem)
1002       - AID_BLUETOOTH (Bluetooth stack)
1003       - AID_GRAPHICS (SurfaceFlinger and graphics drivers)
1004       - AID_INPUT (Input device event processing)
1005       - AID_AUDIO (AudioFlinger and sound daemons)
1006       - AID_CAMERA (Camera hardware daemon)
1017       - AID_KEYSTORE (Android KeyStore daemon)
1023       - AID_MEDIA_RW (Internal media storage access)
2000       - AID_SHELL (ADB shell environment)
10000      - FIRST_APPLICATION_UID (AID_APP_START)
19999      - LAST_APPLICATION_UID (AID_APP_END)
99000+     - FIRST_ISOLATED_UID (Isolated process sandbox)
```

### Sandbox Directory Isolation

When `PackageManagerService` installs an application, it registers an assigned UID in `/data/system/packages.list`:

```bash
# Viewing installed application UIDs and sandbox paths
cat /data/system/packages.list | grep example
com.example.secureapp 10087 0 /data/data/com.example.secureapp default 3003
```

The application's private data directory `/data/data/com.example.secureapp` is created on disk with strict Discretionary Access Control (DAC) permissions:

```text
drwx------ 4 u0_a87 u0_a87 4096 2026-11-01 09:12 /data/data/com.example.secureapp
```

Under these Linux filesystem permissions:
* Only process threads running with effective UID `10087` (`u0_a87`) or UID `0` (`root`) can traverse the directory or read/write files inside it.
* A malicious application running as `10088` (`u0_a88`) receives an immediate kernel-level `EACCES` error if it attempts to access the files of `10087`.

### Isolated Processes (`isolatedProcess="true"`)

Android provides an extreme isolation mechanism for high-risk untrusted code, such as browser HTML rendering engines:

```xml
<service
    android:name=".RendererService"
    android:isolatedProcess="true"
    android:process=":renderer" />
```

Processes launched with `isolatedProcess="true"`:
* Are assigned UIDs in the isolated range (`99000` to `99999`).
* Possess zero supplementary GIDs (cannot access the network, external storage, or camera).
* Are blocked from invoking standard Binder IPC calls to system services, communicating exclusively through dedicated IPC pipes with their parent application.

---

## 4. Native Userspace Initialization & The Zygote Architecture

The boot sequence transitions from the raw Linux kernel to the rich Android application framework through a series of carefully orchestrated steps.

```text
Linux Kernel -> /init (PID 1) -> init.rc parsing -> daemons spawned
                                       |
                                       v
                                /system/bin/app_process (Zygote)
                                       |
                                       +--> Preloads 3000+ Classes & System Drawables
                                       +--> Opens /dev/socket/zygote
                                       +--> Forks system_server (PID ~500)
                                       +--> Forks Application Sandboxes on demand
```

### The `init` Daemon (PID 1)

The first userspace process spawned by the Linux kernel is `/init`. Guided by configuration files (`/init.rc` and `/init.{hardware}.rc`), `init`:

1. Mounts virtual filesystems: `/dev`, `/proc`, `/sys`, `/mnt`.
2. Creates essential device nodes and configures global memory and CPU cgroups.
3. Initializes the kernel SELinux security policy by loading `/sepolicy`.
4. Spawns core system daemons (`servicemanager`, `vold`, `netd`, `debuggerd`, `surfaceflinger`).
5. Launches the **Zygote** runtime parent process.

### The Zygote Architecture & COW Efficiency

In standard Java environments, starting a JVM instance incurs substantial startup latency while the virtual machine initializes heaps, loads standard runtime classes (`rt.jar`), and links native libraries.

Android solves this problem through **Zygote**:
1. `app_process` starts and initializes a pristine Dalvik/ART virtual machine instance.
2. Zygote reads `/system/etc/preloaded-classes` and loads thousands of core Android framework classes into memory.
3. Zygote loads common framework resources and drawables (`com.android.internal.R`).
4. Zygote binds to a local UNIX domain socket located at `/dev/socket/zygote` and enters an event polling loop.

When a user taps an application icon:
* `ActivityManagerService` sends an IPC request to `/dev/socket/zygote` specifying the target APK, package name, and assigned UID/GID parameters.
* Zygote calls the Linux `fork()` system call.
* **Copy-on-Write (COW)**: Because the newly created child process shares the physical memory pages of the parent Zygote process, memory is only duplicated when the child writes to a page. All preloaded framework code and read-only memory structures remain shared across all applications on the device.
* Inside the child process, Zygote drops root privileges by calling `setgroups()`, `setgid()`, and `setuid()`, configures the process SELinux context, and invokes `ActivityThread.main()`.

---

## 5. Binder Inter-Process Communication (IPC) Deep Dive

Because every application runs in a strictly isolated process sandbox under a distinct Linux UID, processes cannot directly access each other's memory address spaces. Traditional Linux IPC mechanisms (pipes, FIFOs, POSIX message queues) lack authenticated caller identification and impose high data copying overhead.

Android solves this by making **Binder** the central nervous system of the entire OS:

![Binder IPC Architecture](/assets/images/posts/android-security/ch1-binder-ipc.png)

### Why Binder?

1. **High Performance**: Binder utilizes shared memory buffers mapped into the receiving process's address space via `mmap()`, requiring only **a single memory copy** (`copy_from_user`) from the sender into kernel space, then directly mapped to the receiver.
2. **Kernel-Enforced Caller Identity**: The Binder driver injects the authentic `UID` and `PID` of the calling process directly into every transaction message. The caller cannot spoof, manipulate, or disguise its security identity.
3. **Reference Counting & Death Notifications**: Binder automatically tracks object references across process boundaries. If a client process crashes, Binder notifies registered server objects via `linkToDeath()`, preventing memory leaks and orphaned system handles.

### The Binder Transaction Pipeline

When an application invokes a system service method (e.g., querying GPS location):

1. **Service Proxy (`BpBinder`)**: The application interacts with a local Java/C++ interface proxy (`BpLocationManager`). The method arguments are serialized into a binary buffer known as a **Parcel**.
2. **`IPCThreadState`**: The proxy hands the Parcel to `IPCThreadState`, which executes an `ioctl()` system call against `/dev/binder`:
   ```c
   struct binder_write_read bwr;
   bwr.write_buffer = (uintptr_t)writebuf;
   bwr.write_size = write_size;
   bwr.read_buffer = (uintptr_t)readbuf;
   bwr.read_size = read_size;
   ioctl(binder_fd, BINDER_WRITE_READ, &bwr);
   ```
3. **Binder Kernel Driver (`/dev/binder`)**:
   * Inspects the transaction command (`BC_TRANSACTION`).
   * Determines the destination node from the target handle.
   * Allocates a memory buffer in the receiver's memory map.
   * Copies the parcel payload from the client address space into the receiver's mapped buffer.
   * Attaches the calling process credentials:
     ```c
     tr.sender_pid = task_tgid_nr(current);
     tr.sender_euid = task_euid(current);
     ```
   * Wakes up a worker thread in the destination process thread pool.
4. **Service Stub (`BBinder`)**: The server thread unmarshals the Parcel and invokes `onTransact()`.
5. **Security Enforcement**: The system service extracts caller identity using:
   ```java
   int callingUid = Binder.getCallingUid();
   int callingPid = Binder.getCallingPid();
   ```
   The service validates whether `callingUid` possesses the requisite permissions before executing privileged logic.

### The Service Manager (Handle 0)

How do processes discover where system services reside?
* During boot, the native daemon `/system/bin/servicemanager` registers itself as the **Context Manager** of the device by calling `ioctl(fd, BINDER_SET_CONTEXT_MGR, 0)`.
* In the Binder protocol, handle `0` is universally reserved for the Service Manager.
* When `system_server` initializes, it registers services by name:
  ```java
  ServiceManager.addService("activity", new ActivityManagerService());
  ServiceManager.addService("package", new PackageManagerService());
  ```
* When an app needs to communicate with `ActivityManagerService`, it sends an IPC request to handle `0` asking for `"activity"`, receiving a valid Binder reference handle in return.

---

## 6. Dalvik vs. ART Virtual Machine Security

Historically, Android utilized the Dalvik Virtual Machine (DVM). Modern Android uses the Android Runtime (ART). Both run Dalvik Executable (`.dex`) bytecode designed specifically for mobile memory constraints.

| Architecture Dimension | Standard Java Virtual Machine (JVM) | Android Dalvik / ART Virtual Machine |
| :--- | :--- | :--- |
| **Execution Architecture** | Stack-based architecture | Register-based architecture |
| **Bytecode Container** | Multiple `.class` files in JAR archives | Single unified `classes.dex` binary |
| **Instruction Size** | 1-byte opcode, variable operand length | 2-byte fixed opcode structure |
| **Constant Pool** | Duplicated across every individual `.class` file | Consolidated string and type pools across whole APK |
| **Compilation Model** | Just-In-Time (JIT) runtime compilation | Ahead-Of-Time (AOT via `dex2oat`) + Profile-Guided JIT |

### Bytecode Verification as a Security Barrier

Before executing untrusted bytecode, the runtime conducts a rigorous verification pass:
* Checks branch instructions to ensure jumps target valid instruction boundaries inside method code.
* Enforces register type safety (prevents reading a floating point register as an object reference).
* Validates method access modifiers (`public`, `private`, `protected`).
* Guarantees that local variables are initialized before use, blocking raw memory pointer arithmetic and classic stack-smashing buffer overflows in managed application code.

---

## 7. Attack Surfaces & Offensive Insights

Understanding Android's security model reveals the primary attack vectors targeted by vulnerability researchers and offensive security engineers:

### 1. Confused Deputy Attacks via Binder
Because the Binder driver transparently transmits caller credentials, a vulnerability arises when a privileged application (e.g., a system service running as UID `1000`) performs actions on behalf of an unprivileged application without verifying permissions. If a system service exposes an IPC interface that accepts an arbitrary intent or file path without checking `Binder.getCallingUid()`, unprivileged apps can execute privileged operations through the "confused" system deputy.

### 2. Kernel Driver Vulnerabilities
The kernel `/dev/binder` driver runs in Ring 0 (kernel space). Memory management flaws, race conditions in transaction buffer allocations, or use-after-free bugs in `binder_thread` or `binder_node` refcounting (such as CVE-2019-2215) can allow an unprivileged sandbox application to achieve arbitrary kernel read/write, disabling SELinux and obtaining full root access.

### 3. Zygote Socket Hijacking
Historically, if an attacker could establish a local connection to the `/dev/socket/zygote` UNIX domain socket, they could instruct Zygote to fork arbitrary processes under arbitrary UIDs. Modern Android kernels strictly restrict access to the Zygote socket via SELinux type rules (`zygote_socket`), permitting only `system_server` to connect.

---

## Next in the Series: Chapter 2 Preview

In the next installment, we explore [Chapter 2: Permissions Architecture](/posts/android-security-internals-chapter-2/), dissecting:

* Permission declaration syntax and protection levels (`normal`, `dangerous`, `signature`, `signatureOrSystem`).
* How `PackageManagerService` parses permissions into `/data/system/packages.xml`.
* Kernel GID mapping and Supplementary Group allocation.
* Runtime Binder hook checks and Content Provider URI grant mechanics (`grantUriPermission`).
* Real-world attack surfaces including permission escalation and confused deputy exploitation.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals: An In-Depth Guide to Android's Security Architecture*. No Starch Press, 2015. Chapter 1: "Android's Security Model," pp. 1–20.
2. [Android Open Source Project (AOSP) - Security Architecture Overview](https://source.android.com/docs/security/overview/kernel-security)
3. [Android Binder IPC Architecture & Driver Documentation](https://source.android.com/docs/core/architecture/hidl/binder-ipc)
4. Levin, Jonathan. *Android Internals: A Confectioner's Cookbook*. Technologeeks, 2014.
5. [Chromium Projects - Android Sandbox Architecture](https://www.chromium.org/developers/design-documents/sandbox/)

---

## Let's Connect

Have questions or insights regarding Android's kernel sandbox or Binder IPC mechanics?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
"""

write_post("2026-11-01-android-security-internals-chapter-1.md", ch1_content)

# Chapter 2
ch2_content = """---
title: "Android Security Internals: Chapter 2 - Permissions Architecture"
date: 2026-11-01 10:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, permissions, packagemanager, binder, access-control]
description: "An in-depth technical analysis of Chapter 2 of Nikolay Elenkov's 'Android Security Internals', detailing manifest definitions, protection levels, kernel GID mapping, runtime Binder checks, and content provider URI permissions."
image:
  path: /assets/images/posts/android-security/chapter-2-cover.png
  alt: "Android Security Internals Chapter 2 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**.

In [Chapter 1](/posts/android-security-internals-chapter-1/), we dissected Android's kernel sandbox, UID allocation, and Binder IPC mechanics. In this installment, we explore **Chapter 2: Permissions**, the primary mechanism Android employs to restrict access to sensitive device APIs, hardware sensors, network interfaces, and private user datasets.

While users typically perceive permissions as interactive prompt dialogs, under the hood Android's permission model is a multi-tier enforcement architecture spanning **compiled XML manifests**, **Linux kernel Supplementary Group IDs (GIDs)**, **framework-level Binder hook checks**, and **transient Content Provider URI delegation tokens**.

Let's dive into the technical internals of Android's permission framework.

![Android Security Internals Chapter 2](/assets/images/posts/android-security/chapter-2-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| [Chapter 1: Android's Security Model](/posts/android-security-internals-chapter-1/) | **Chapter 2: Permissions Architecture** | [Chapter 3: Package Management](/posts/android-security-internals-chapter-3/) |

---

## Key Takeaways

* **Declaration vs. Request**: Applications define new permissions using `<permission>` tags and request access to existing permissions via `<uses-permission>` tags in `AndroidManifest.xml`.
* **Protection Levels**: The granting policy of a permission is governed strictly by its `protectionLevel` (`normal`, `dangerous`, `signature`, and `signatureOrSystem`).
* **Hardware & Network Isolation via Kernel GIDs**: Permissions that touch sockets (`INTERNET`) or physical storage (`WRITE_EXTERNAL_STORAGE`) are mapped directly to Linux kernel GIDs (`AID_INET`, `AID_SDCARD_RW`) during process forking.
* **IPC Hook Enforcement**: System services enforce permissions inside Binder stubs using `checkCallingPermission()` and `enforceCallingPermission()`, extracting verified caller credentials via `Binder.getCallingUid()`.
* **Transient Capability Delegation**: Content Provider URI permissions (`grantUriPermission`) allow an application to pass temporary read/write access to specific data objects without granting global database permissions.

---

## 1. Permission Declaration and Protection Levels

Every permission in the Android ecosystem has a unique identifier formatted as a reverse-domain string (e.g., `android.permission.ACCESS_FINE_LOCATION`).

![Permission Enforcement Workflow](/assets/images/posts/android-security/ch2-permission-enforcement.png)

### The Permission Declaration Syntax

Third-party and system applications declare custom permissions inside `AndroidManifest.xml`:

```xml
<permission
    android:name="com.example.myapp.permission.READ_VAULT"
    android:label="@string/perm_vault_label"
    android:description="@string/perm_vault_desc"
    android:permissionGroup="android.permission-group.PERSONAL_INFO"
    android:protectionLevel="signature" />
```

### Protection Level Matrix

The `protectionLevel` attribute defines how Android evaluates and grants the permission:

| Protection Level | Granting Policy | User Prompts | Common Examples |
| :--- | :--- | :--- | :--- |
| **`normal`** | Granted automatically at install time. Poses minimal risk to user privacy or device operation. | None | `ACCESS_NETWORK_STATE`, `SET_WALLPAPER`, `VIBRATE` |
| **`dangerous`** | Grants access to private user data or device hardware. Historically granted at install; runtime prompts in modern Android. | Explicit prompt required | `CAMERA`, `RECORD_AUDIO`, `READ_CONTACTS`, `ACCESS_FINE_LOCATION` |
| **`signature`** | Granted **only** if the requesting application is signed with the identical cryptographic certificate as the declaring application. | None (Silent grant) | Enterprise internal APIs, proprietary OEM app-to-app communication |
| **`signatureOrSystem`** (Privileged) | Granted if signed by the declaring certificate **OR** if the app is pre-installed in the `/system/priv-app` partition. | None | `REBOOT`, `SHUTDOWN`, `INJECT_EVENTS`, `STATUS_BAR` |

### Modern Protection Flags

In newer Android framework revisions, protection levels are decomposed into a base level plus additive bitwise flags:

* `privileged`: Limits access to apps located in `/system/priv-app`.
* `development`: Can be granted to test applications via ADB shell commands:
  ```bash
  pm grant com.example.app android.permission.DUMP
  ```
* `preinstalled`: Restricted to pre-loaded firmware packages.

---

## 2. Permission Registration & `PackageManagerService`

During system boot, `PackageManagerService` (PMS) scans system partitions and third-party directories:
1. Parses `/system/framework/framework-res.apk` to register all core platform permissions.
2. Scans `/system/app`, `/system/priv-app`, `/vendor/app`, and `/data/app`.
3. Verifies cryptographic signatures of declaring and requesting packages.
4. Serializes the entire device permission state into `/data/system/packages.xml`.

### Deep Dive: `/data/system/packages.xml`

Inside this critical XML database, granted permissions and assigned UIDs are permanently tracked:

```xml
<package name="com.example.secureclient" 
         codePath="/data/app/com.example.secureclient-1" 
         nativeLibraryPath="/data/app-lib/com.example.secureclient-1" 
         flags="4793910" 
         ft="192a3b4c500" 
         it="192a3b4c500" 
         ut="192a3b4c500" 
         version="10" 
         userId="10087">
    <sigs count="1">
        <cert index="1" key="3082024a308201b3a003020102..." />
    </sigs>
    <perms>
        <item name="android.permission.INTERNET" granted="true" flags="0" />
        <item name="android.permission.CAMERA" granted="true" flags="0" />
        <item name="com.example.myapp.permission.READ_VAULT" granted="true" flags="0" />
    </perms>
</package>
```

---

## 3. Kernel-Level Permission Enforcement: GID Mapping

Not all Android permissions are enforced inside Dalvik/ART userspace. Low-level operating system resources (such as raw IP sockets, Bluetooth hardware controllers, and external SD card partitions) are enforced directly by the **Linux kernel** through Supplementary Group IDs (GIDs).

### The Mapping Configuration: `platform.xml`

Android defines the static bridge between high-level Java permission strings and low-level Linux GIDs in `/etc/permissions/platform.xml`:

```xml
<permissions>
    <!-- Maps android.permission.INTERNET to Linux GID inet (3003) -->
    <permission name="android.permission.INTERNET">
        <group gid="inet" />
    </permission>

    <!-- Maps raw networking permission to Linux GID net_raw (3004) -->
    <permission name="android.permission.ACCESS_NETWORK_STATE">
        <group gid="net_raw" />
    </permission>

    <!-- Maps SD card write permission to Linux GID sdcard_rw (1015) -->
    <permission name="android.permission.WRITE_EXTERNAL_STORAGE">
        <group gid="sdcard_rw" />
    </permission>
</permissions>
```

### Zygote Fork & `setgroups()`

When `ActivityManagerService` instructs Zygote to spawn an application process:
1. PMS inspects the permissions granted to the application UID in `packages.xml`.
2. PMS compiles an array of corresponding integer GIDs (e.g., `[3003, 1015]`).
3. Zygote forks its process and calls the native Linux system call:
   ```c
   setgroups(gid_count, gid_array);
   ```
4. If an app requests to open a network socket:
   ```c
   int sock = socket(AF_INET, SOCK_STREAM, 0);
   ```
   The kernel network subsystem checks if the calling process belongs to group `3003` (`AID_INET`). If missing, the kernel immediately halts the call with `EACCES` (Permission Denied), completely independent of the Dalvik/ART virtual machine!

---

## 4. Framework-Level Permission Enforcement

For system services running inside `system_server` (e.g., location, telephony, camera), permissions are enforced programmatically at the entry point of each Binder transaction.

### The Enforcement API

System services verify callers using methods exposed by `android.content.Context`:

```java
// Throws SecurityException if caller lacks permission
context.enforceCallingPermission(
    Manifest.permission.ACCESS_FINE_LOCATION, 
    "Caller lacks fine location access");

// Returns PackageManager.PERMISSION_GRANTED or PERMISSION_DENIED
int status = context.checkCallingPermission(
    Manifest.permission.CAMERA);
```

### Internal Implementation Inside `system_server`

When an app calls `LocationManager.getLastKnownLocation()`:

```java
// Inside LocationManagerService.java (system_server)
@Override
public Location getLastKnownLocation(LocationRequest request, String packageName) {
    // 1. Extract verified UID and PID from the Binder driver
    int callingUid = Binder.getCallingUid();
    int callingPid = Binder.getCallingPid();

    // 2. Query PackageManagerService
    int permissionCheck = mContext.checkPermission(
        Manifest.permission.ACCESS_FINE_LOCATION, 
        callingPid, 
        callingUid
    );

    if (permissionCheck != PackageManager.PERMISSION_GRANTED) {
        throw new SecurityException("UID " + callingUid + " requires ACCESS_FINE_LOCATION");
    }

    // 3. Permission verified; execute privileged hardware access
    return mProvider.getLastLocation();
}
```

### Identity Switching: `clearCallingIdentity()`

When a system service needs to execute an operation on behalf of a client that requires the service's own elevated system credentials (UID `1000`), it uses `Binder.clearCallingIdentity()`:

```java
// Temporarily reset calling identity to UID 1000
long identityToken = Binder.clearCallingIdentity();
try {
    // Privileged operation executed as system_server
    mInternalStorageHelper.allocateSystemBlock();
} finally {
    // Restore the client's original UID/PID token
    Binder.restoreCallingIdentity(identityToken);
}
```

> **Offensive Security Note**: Failing to restore calling identity or performing client-directed operations while running under cleared identity is a classic root-cause of **Confused Deputy** vulnerabilities in Android system services.

---

## 5. Content Provider URI Permissions

Standard Android permissions grant broad, persistent access to an entire component. However, sharing a specific document, photo, or private SQLite record with an external application requires fine-grained, temporary capability delegation.

Android solves this via **URI Permissions**:

```xml
<provider
    android:name="com.example.securenotes.NotesProvider"
    android:authorities="com.example.securenotes"
    android:exported="false"
    android:grantUriPermissions="true" />
```

### Dynamic Capability Delegation

When an application wants to share a private file with a viewer:

```java
Uri noteUri = Uri.parse("content://com.example.securenotes/note/42");

Intent viewIntent = new Intent(Intent.ACTION_VIEW);
viewIntent.setData(noteUri);

// Attach temporary read capability to the Intent
viewIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);

// Launch viewer; ActivityManager grants temporary access to note/42 only!
context.startActivity(viewIntent);
```

### How `ActivityManagerService` Mediates URI Grants

1. When `startActivity()` is invoked, `ActivityManagerService` intercepts the Intent.
2. AMS verifies that the sender has permission to access `noteUri`.
3. AMS creates an ephemeral `UriPermission` record mapping `(noteUri, targetUid, READ_FLAG)`.
4. When the target application queries `noteUri`, the Content Provider checks with AMS, which confirms the temporary grant.
5. Once the viewer's activity lifecycle finishes, AMS revokes the grant automatically.

---

## 6. Attack Surfaces & Exploitation Vectors

### 1. Confused Deputy Vulnerabilities
A confused deputy occurs when an unprivileged application (App A) cannot access a sensitive resource directly, but tricks a privileged exported component (App B) into fetching or modifying the resource on its behalf. If App B accepts an Intent containing an arbitrary URI and forwards it without checking permissions, App A can read private files or trigger system changes.

### 2. Signature Spoofing
Custom ROMs or compromised system frameworks that disable signature validation in `PackageManagerService.checkSignatures()` allow malicious applications to declare arbitrary signature-protected permissions, completely compromising enterprise and OEM security boundaries.

### 3. Permission Hijacking / Pre-grant Races
In older Android versions, if an unprivileged app was installed *before* a system app that declared a custom permission, the unprivileged app could declare the permission first with a `normal` protection level. Subsequent apps requesting the permission would receive it automatically, hijacking the permission namespace. Modern Android strictly rejects duplicate permission declarations from different signing certificates.

---

## Next in the Series: Chapter 3 Preview

In [Chapter 3: Package Management](/posts/android-security-internals-chapter-3/), we will analyze:

* The anatomy of the APK archive and compiled binary XML formats.
* Dalvik Executable (DEX) bytecode structure and verification algorithms.
* The v1 JAR signing scheme (`MANIFEST.MF`, `CERT.SF`, `CERT.RSA`).
* The package installation lifecycle and the native `installd` daemon.
* The historic Master Key vulnerabilities (CVE-2013-4787) that allowed silent payload injection.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 2: "Permissions," pp. 21–50.
2. [AOSP Documentation - System Permissions Architecture](https://source.android.com/docs/core/permissions)
3. [Android Developers - Permissions Overview & Guidelines](https://developer.android.com/guide/topics/permissions/overview)
4. Enck, William, et al. *Understanding Android Security*. IEEE Security & Privacy, 2009.
5. [Android Security Team - Reviewing Android Platform Permissions](https://source.android.com/docs/security/features)

---

## Let's Connect

Have you audited Android apps for confused deputy or URI grant vulnerabilities? Share your findings or questions below:

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
"""

write_post("2026-11-01-android-security-internals-chapter-2.md", ch2_content)

# Chapter 3
ch3_content = """---
title: "Android Security Internals: Chapter 3 - Package Management"
date: 2026-11-01 11:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, apk, dex, code-signing, packagemanager, installd]
description: "An in-depth technical breakdown of Chapter 3 of Nikolay Elenkov's 'Android Security Internals', exploring APK zip file anatomy, DEX bytecode structure, JAR/APK signing schemes, package verification, and installd internals."
image:
  path: /assets/images/posts/android-security/chapter-3-cover.png
  alt: "Android Security Internals Chapter 3 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**.

In [Chapter 2](/posts/android-security-internals-chapter-2/), we analyzed the Android permissions framework and runtime Binder hook checks. In this installment, we explore **Chapter 3: Package Management**, dissecting the exact file structures, cryptographic verification algorithms, bytecode containers, and installation daemons that convert an untrusted APK archive into an active, sandboxed application.

We will deconstruct the anatomy of the APK archive, trace how `PackageManagerService` orchestrates installations with the native `installd` daemon, inspect the Java JAR signing architecture (`MANIFEST.MF`, `CERT.SF`, `CERT.RSA`), and examine the mechanics behind historic APK tampering exploits like the famous Master Key vulnerability.

![Android Security Internals Chapter 3](/assets/images/posts/android-security/chapter-3-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| [Chapter 2: Permissions Architecture](/posts/android-security-internals-chapter-2/) | **Chapter 3: Package Management** | [Chapter 4: User Management](/posts/android-security-internals-chapter-4/) |

---

## Key Takeaways

* **The APK Container**: An Android application package (`.apk`) is a standard ZIP 32 archive containing compiled Dalvik Executable bytecode (`classes.dex`), binary XML manifests, compiled resources (`resources.arsc`), native ELF shared libraries (`lib/`), and a cryptographic signature directory (`META-INF/`).
* **Binary XML Efficiency**: To optimize mobile CPU and battery performance, XML configuration files (including `AndroidManifest.xml`) are compiled into a compact binary format that tokenizes tag strings and attribute namespaces into integer indices.
* **JAR / APK v1 Signing Scheme**: Code signing in early Android is based on Java JAR signing. Verification requires three interconnected files: `MANIFEST.MF` (file hashes), `CERT.SF` (manifest hashes), and `CERT.RSA` (a PKCS#7 signed signature block containing the developer's public certificate).
* **Package Installation via `installd`**: The Java-based `PackageManagerService` cannot execute low-level filesystem operations directly with root privileges. It issues commands over a UNIX domain socket to `/system/bin/installd`, which creates sandbox directories and assigns file ownership.
* **Shared User IDs**: The `android:sharedUserId` manifest directive enables two or more distinct APKs signed with the exact same certificate to share a single Linux UID, execute inside the same process space, and freely read each other's private data directories.

---

## 1. Anatomy of an APK Package

An Android application package is structured as an uncompressed or Deflate-compressed ZIP archive:

```text
my-app.apk
├── AndroidManifest.xml       (Compiled binary XML format)
├── classes.dex               (Compiled Dalvik bytecode)
├── resources.arsc            (Compiled resource table)
├── res/                      (Application assets: layouts, drawables)
│   ├── layout/activity_main.xml
│   └── drawable-xxhdpi/ic_launcher.png
├── assets/                   (Raw uncompiled application assets)
├── lib/                      (Compiled native architectures)
│   ├── arm64-v8a/libnative.so
│   └── x86_64/libnative.so
└── META-INF/                 (Cryptographic code signature)
    ├── MANIFEST.MF           (Per-file SHA-1 / SHA-256 digests)
    ├── CERT.SF               (Manifest section digests)
    └── CERT.RSA              (PKCS#7 signature + X.509 Certificate)
```

### Binary XML Format (AXML)

Android does not store plain-text XML manifests inside an APK. Parsing raw text XML at application startup would consume unnecessary CPU cycles and RAM. Android compiles XML files into **AXML (Android Binary XML)**:

1. **String Pool**: All attribute names, tag names, and string literals are collected into a global string pool located at the head of the file.
2. **Tokenized Elements**: XML tags (e.g., `<manifest>`, `<application>`, `<activity>`) and attributes (e.g., `android:name`, `android:exported`) are replaced with 32-bit integer token IDs.
3. **Resource Mapping**: Attribute IDs correspond directly to system resource constants defined in the platform framework (`0x01010003` maps to `android:name`).

---

## 2. DEX Bytecode & Execution Optimization

Java source code (`.java`) is first compiled into standard Java bytecode (`.class`) by the Java compiler (`javac`). The Android SDK's `dx` or `d8` tool then translates and consolidates all `.class` files into a unified Dalvik Executable binary: `classes.dex`.

### The DEX Header Specification

The `classes.dex` file begins with a fixed 112-byte header:

```text
Offset | Field Name       | Size    | Description
-------|------------------|---------|---------------------------------------------
0x00   | magic            | 8 bytes | 'dex\n035\0' (DEX version identifier)
0x08   | checksum         | 4 bytes | Adler32 checksum of rest of file
0x0C   | signature        | 20 bytes| SHA-1 signature of rest of file
0x20   | file_size        | 4 bytes | Total size of the DEX file in bytes
0x24   | header_size      | 4 bytes | Header size in bytes (typically 0x70 / 112)
0x28   | endian_tag       | 4 bytes | Endianness flag (0x12345678 = Little Endian)
0x38   | string_ids_size  | 4 bytes | Number of strings in string table
0x40   | type_ids_size    | 4 bytes | Number of type descriptors
0x48   | proto_ids_size   | 4 bytes | Number of method prototype descriptors
0x50   | field_ids_size   | 4 bytes | Number of field identifiers
0x58   | method_ids_size  | 4 bytes | Number of method identifiers
0x60   | class_defs_size  | 4 bytes | Number of class definitions
0x68   | data_size        | 4 bytes | Size of the data section
```

### Optimization: `dexopt` and `dex2oat`

During installation, Android optimizes the raw DEX bytecode to maximize execution speed:

* **Dalvik Era (`dexopt`)**: The system daemon runs `dexopt` against the APK. It verifies bytecode, replaces high-overhead virtual method invocations with direct inline calls, and generates an **Optimized DEX (`.odex`)** file saved in `/data/dalvik-cache`.
* **ART Era (`dex2oat`)**: The Android Runtime compiles DEX bytecode Ahead-Of-Time (AOT) into native ARM/x86 machine instructions, packing them into an **ELF shared library (`.oat`)**.

---

## 3. Code Signing Architecture: The v1 JAR Signing Scheme

Unlike traditional desktop platforms where certificates must be issued by a trusted commercial Certificate Authority (CA), **Android allows developers to sign APKs using self-signed X.509 certificates.**

The primary function of an Android APK signature is **not** identity attestation; it is **origin authentication, update integrity, and mutual trust establishment.**

![APK Structure & Jar Signature Verification](/assets/images/posts/android-security/ch3-apk-signing.png)

### The Verification Chain

The v1 signing scheme verifies archive integrity through a three-stage hashing pipeline inside the `META-INF/` directory:

#### Stage 1: `META-INF/MANIFEST.MF`
Lists the Base64-encoded cryptographic digest of every individual uncompressed file inside the APK:

```text
Manifest-Version: 1.0
Created-By: 1.0 (Android)

Name: AndroidManifest.xml
SHA1-Digest: 8y9L2/Q1zV9lJ8wZ7xN0kM1pQ4s=

Name: classes.dex
SHA1-Digest: 4fA7r8Y9+k0L1m2N3p4Q5r6S7t8=

Name: res/layout/activity_main.xml
SHA1-Digest: 9u8V7w6X5y4Z3a2B1c0D9e8F7g6=
```

#### Stage 2: `META-INF/CERT.SF`
The Signature File (`CERT.SF`) protects `MANIFEST.MF` against tampering. It contains:
1. A SHA-1 digest of the entire `MANIFEST.MF` file.
2. Individual digests for each section of `MANIFEST.MF`.

```text
Signature-Version: 1.0
Created-By: 1.0 (Android)
SHA1-Digest-Manifest: 3kA9s8D7f6G5h4J3k2L1m0N9p8q=

Name: AndroidManifest.xml
SHA1-Digest: b8N7m6V5c4X3z2A1s0D9f8G7h6J=

Name: classes.dex
SHA1-Digest: q1W2e3R4t5Y6u7I8o9P0a1S2d3F=
```

#### Stage 3: `META-INF/CERT.RSA`
A binary PKCS#7 `SignedData` structure containing:
* The digital signature computed over the exact contents of `CERT.SF` using the developer's private key (e.g., RSA with SHA-256).
* The developer's public X.509 certificate.

### Signature Verification Algorithm

When an APK is installed or updated:
1. `PackageManagerService` extracts `CERT.RSA`.
2. It parses the developer's public certificate and verifies the PKCS#7 signature over `CERT.SF`.
3. It recomputes the SHA-1 digest of `MANIFEST.MF` and compares it against the `SHA1-Digest-Manifest` header in `CERT.SF`.
4. It iterates through every file inside the APK, uncompresses the bytes, calculates the SHA-1 hash, and validates it against `MANIFEST.MF`.
5. If any byte in any file was altered, added, or deleted, verification aborts and installation fails.

---

## 4. The Package Installation Lifecycle

Package installation is orchestrated by `PackageManagerService` (PMS) inside `system_server` in coordination with the native `installd` daemon:

```text
Client (ADB / App Store)
          |
          v
PackageManager.installPackage()
          |
          v
PackageManagerService (system_server)
   ├── 1. Copies APK to /data/app/vmdl<id>.tmp
   ├── 2. Parses AndroidManifest.xml (PackageParser)
   ├── 3. Verifies Signatures (JarVerifier / KeyStore)
   ├── 4. Checks Update Permissions & Version Codes
   └── 5. Connects via UNIX socket to /system/bin/installd
                    |
                    v
          installd (Native Daemon - UID root)
             ├── mkdir /data/data/<package_name>
             ├── chown u0_a87:u0_a87 /data/data/<package_name>
             ├── chmod 0751 /data/data/<package_name>
             └── dexopt / classes optimization
```

### Why Does `installd` Exist?

Android's `system_server` runs as user `system` (UID `1000`). Under Linux DAC permissions, user `system` cannot arbitrary change file ownership across all other UIDs on the system.

To create private application directories owned by new UIDs (`chown u0_a87:u0_a87`), Android uses `/system/bin/installd`, which runs as **root (UID 0)**. `PackageManagerService` communicates with `installd` over a secure local UNIX domain socket at `/dev/socket/installd`, issuing controlled IPC commands:

* `install`: Creates application data directories.
* `dexopt`: Triggers bytecode optimization.
* `rmuserdata`: Cleans up application storage on uninstall.

---

## 5. Shared User IDs (`sharedUserId`)

By default, every application receives an isolated UID. However, Android provides a feature allowing distinct applications from the same vendor to merge into a single security boundary:

```xml
<!-- In both App A and App B manifests -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app_a"
    android:sharedUserId="com.example.shared_identity">
```

### Security Invariants for `sharedUserId`

1. **Identical Cryptographic Signatures**: Both APKs **must** be signed with the exact same certificate. If a third-party attempts to claim the shared user ID, installation fails with `INSTALL_FAILED_SHARED_USER_INCOMPATIBLE`.
2. **Unified Linux UID**: Both applications are assigned the same UID (e.g., `10087`).
3. **Shared Filesystem Access**: App A can read and write files in App B's `/data/data/com.example.app_b` directory without permission errors.
4. **Shared Process Execution**: By specifying `android:process`, both applications can run threads inside the exact same Dalvik/ART virtual machine process.

---

## 6. Historic Exploitation: The Master Key Vulnerability

In 2013, vulnerability researcher Jeff Forristal (Bluebox Security) discovered **CVE-2013-4787**, commonly known as the **Android Master Key Vulnerability**. It remains one of the most critical flaws in Android package management history.

### The Root Cause: Zip Implementation Divergence

An APK is a ZIP archive. The ZIP file format allows multiple entries to share the exact same filename.

When Android verified and executed APKs, two different software components parsed the archive:
1. **Java `JarFile` Verifier**: Used during signature validation. It iterated through the archive from the beginning and verified the first occurrence of each file.
2. **C / C++ Native Unzipper (`dexopt`)**: Extracted `classes.dex` for optimization. It read the Central Directory header from the end of the ZIP file, extracting the **last** occurrence of `classes.dex`.

```text
[Malicious APK Layout]
-------------------------------------------------------------------------
Entry 1: classes.dex (Original, signed by Google / OEM) -> Verified by Java!
Entry 2: classes.dex (Trojaned backdoor bytecode)       -> Executed by C++!
-------------------------------------------------------------------------
```

### Exploitation Impact

An attacker could take an authentic system update APK signed by Samsung or Google, insert a modified `classes.dex` containing arbitrary exploit payloads, and install it on the device:
* The Java signature verifier inspected Entry 1 and confirmed the cryptographic signature was valid.
* The native `dexopt` daemon extracted Entry 2 and executed the attacker's payload as UID `1000` (`system`), granting full device takeover without invalidating the cryptographic signature!

Google resolved the vulnerability by updating `ZipFile.java` to explicitly reject any ZIP archive containing duplicate entry names.

---

## Next in the Series: Chapter 4 Preview

In [Chapter 4: User Management](/posts/android-security-internals-chapter-4/), we will examine:

* The evolution of Android's multi-user model (tablets, phones, secondary users, and guest accounts).
* The deterministic UID calculation formula: `userId * 100000 + appId`.
* Storage virtualization and per-user directory sandboxing (`/data/user/[userId]`).
* `UserManagerService` mechanics and restricted profile policy enforcement.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 3: "Package Management," pp. 51–86.
2. [AOSP Documentation - Application Signing Schemes (v1, v2, v3, v4)](https://source.android.com/docs/security/features/apksigning)
3. [Bluebox Security - Android Master Key Vulnerability (CVE-2013-4787) Technical Report](https://bluebox.com/)
4. [Android Open Source Project - Dalvik Executable Format Specification](https://source.android.com/docs/core/runtime/dex-format)
5. Levin, Jonathan. *Android Internals: A Confectioner's Cookbook*. Technologeeks, 2014.

---

## Let's Connect

Have questions regarding DEX bytecode manipulation or APK signature analysis?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
"""

write_post("2026-11-01-android-security-internals-chapter-3.md", ch3_content)

# Chapter 4
ch4_content = """---
title: "Android Security Internals: Chapter 4 - User Management"
date: 2026-11-01 12:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, multi-user, usermanager, storage, namespaces, access-control]
description: "A technical dissection of Chapter 4 of Nikolay Elenkov's 'Android Security Internals', covering Android multi-user architecture, UID mathematical mapping formulas, per-user storage virtualization, and UserManagerService internals."
image:
  path: /assets/images/posts/android-security/chapter-4-cover.png
  alt: "Android Security Internals Chapter 4 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**.

In [Chapter 3](/posts/android-security-internals-chapter-3/), we examined APK anatomy, DEX bytecode structure, and the v1 JAR code signing scheme. In this installment, we explore **Chapter 4: User Management**, analyzing how Android implemented genuine multi-user support on top of an operating system that had already hijacked the Linux multi-user model for application sandboxing.

When Google introduced multi-user functionality in Android 4.2 (initially for tablets, and later in Android 5.0 for phones), they faced an architectural challenge: **If Linux UIDs were already assigned to individual apps (UIDs 10000+), how could multiple human users coexist on the same filesystem without breaking process sandboxing?**

The solution was an elegant mathematical range allocation formula combined with kernel-level storage virtualization.

![Android Security Internals Chapter 4](/assets/images/posts/android-security/chapter-4-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| [Chapter 3: Package Management](/posts/android-security-internals-chapter-3/) | **Chapter 4: User Management** | [Chapter 5: Cryptographic Providers](/posts/android-security-internals-chapter-5/) |

---

## Key Takeaways

* **The Multi-User Formula**: Android maps multiple human users to distinct Linux UID spaces using the deterministic formula: `UID = (User_ID * 100000) + App_ID`.
* **Primary vs. Secondary Users**: User `0` is the primary owner account that boots the device and runs core system daemons. Additional users (`10`, `11`, etc.) represent secondary profiles, guest accounts, or managed enterprise work profiles.
* **Storage Virtualization**: Physical internal storage is partitioned into per-user directories (`/data/user/[userId]`). Filesystem isolation is enforced via Discretionary Access Control (DAC) and Linux mount namespaces.
* **Shared Binaries, Isolated State**: When multiple users install the same application, only a single APK binary is stored in `/data/app`. However, each user receives a completely isolated data sandbox and private SQLite databases.
* **`UserManagerService`**: The centralized framework service running inside `system_server` that manages user creation, lifecycle transitions, state serialization (`/data/system/users/`), and restricted profile policy enforcement.

---

## 1. The Multi-User UID Architecture

To accommodate multiple human profiles without altering the fundamental rule that each application must run in an isolated Linux UID sandbox, Android established a mathematical UID translation layer:

$$\text{Linux UID} = (\text{User\_ID} \times 100000) + \text{App\_ID}$$

Where:
* `User_ID`: Integer identifying the human user profile (starting at `0` for the primary owner, followed by `10`, `11`, `12` for secondary accounts).
* `App_ID`: The application's base identifier (ranging from `10000` to `19999`).

### The Multi-User UID Allocation Matrix

| Entity | Base App ID | User 0 (Primary) | User 10 (Secondary User) | User 11 (Work Profile) |
| :--- | :--- | :--- | :--- | :--- |
| `AID_ROOT` | `0` | `0` | `1000000` | `1100000` |
| `AID_SYSTEM` | `1000` | `1000` | `1001000` | `1101000` |
| `AID_MEDIA` | `1013` | `1013` | `1001013` | `1101013` |
| App: Twitter | `10087` | `10087` (`u0_a87`) | `1010087` (`u10_a87`) | `1110087` (`u11_a87`) |
| App: Signal | `10092` | `10092` (`u0_a92`) | `1010092` (`u10_a92`) | `1110092` (`u11_a92`) |

### Linux Process Isolation Across Users

If User 0 and User 10 both launch Twitter simultaneously:
* User 0's instance executes under Linux UID `10087`.
* User 10's instance executes under Linux UID `1010087`.
* To the Linux kernel, these are two entirely different security principals. Neither process can inspect the memory, attach a `ptrace` debugger, or send signals (`kill`) to the other.

---

## 2. Storage Virtualization & Isolated Namespaces

In a multi-user environment, private application files, external storage, and media downloads must be segregated so that User 10 cannot browse the photos or database records of User 0.

### Internal Sandbox Virtualization

Internal application storage is laid out across isolated directory paths:

```text
/data/
├── app/                              (Shared read-only APK binaries)
│   └── com.example.notes-1.apk
├── data/                             (Symlink to /data/user/0)
└── user/
    ├── 0/                            (User 0 Private Sandbox)
    │   └── com.example.notes/
    │       ├── databases/notes.db    (Owned by u0_a87:u0_a87 - 0700)
    │       └── shared_prefs/
    └── 10/                           (User 10 Private Sandbox)
        └── com.example.notes/
            ├── databases/notes.db    (Owned by u10_a87:u10_a87 - 0700)
            └── shared_prefs/
```

Under standard Linux filesystem DAC permissions:
* `/data/user/0/com.example.notes/databases/notes.db` is readable exclusively by UID `10087`.
* `/data/user/10/com.example.notes/databases/notes.db` is readable exclusively by UID `1010087`.
* Even though both processes execute the exact same bytecode from `/data/app/com.example.notes-1.apk`, their SQLite databases remain strictly isolated.

### External Storage & FUSE / sdcardfs

External storage (`/sdcard`) introduces complexity because FAT32 and standard exFAT filesystems do not natively support Linux POSIX file ownership and permissions.

Android resolves this using filesystem virtualization:
1. The physical storage partition `/data/media` is owned by `media_rw:media_rw`.
2. Storage is partitioned into subdirectories: `/data/media/0` and `/data/media/10`.
3. An in-kernel FUSE daemon or **sdcardfs** driver mounts these directories:
   * When User 0 accesses `/storage/emulated/0`, the driver transparently maps requests to `/data/media/0`.
   * When User 10 accesses `/storage/emulated/10`, requests map to `/data/media/10`.
4. Using Linux **Mount Namespaces (`unshare(CLONE_NEWNS)`)**, each user's Zygote child process sees only their own emulated storage mounted at `/storage/emulated/`, preventing path traversal into other user media folders.

---

## 3. `UserManagerService` & Lifecycle Architecture

User lifecycle events are coordinated by `UserManagerService` (UMS), a system service registered with `ServiceManager`:

```text
SystemServer
    └── UserManagerService
            ├── /data/system/users/userlist.xml  (Registry of active users)
            ├── /data/system/users/0.xml         (User 0 metadata & flags)
            ├── /data/system/users/10.xml        (User 10 metadata & flags)
            └── /data/system/users/10/           (User 10 wallpaper, accounts)
```

### User Types & Roles

Android supports multiple distinct user categories:

| User Type | Flags | Capabilities |
| :--- | :--- | :--- |
| **Owner (Primary)** | `FLAG_PRIMARY \| FLAG_ADMIN` | Boots first; cannot be deleted; can configure global hardware, Wi-Fi, and create new users. |
| **Secondary User** | `FLAG_FULL` | Independent user account; can install apps and customize settings; cannot configure device-wide radios. |
| **Guest User** | `FLAG_GUEST \| FLAG_EPHEMERAL` | Temporary session; displays a prompt to wipe all user data upon logout. |
| **Restricted Profile** | `FLAG_RESTRICTED` | Parentally-controlled or kiosk account; app access is whitelisted by User 0. |
| **Managed Profile (Work)** | `FLAG_MANAGED_PROFILE` | Enterprise container coexisting alongside User 0; governed by an MDM Device Policy Controller. |

### The User Switching Flow

When the device switches from User 0 to User 10:
1. `ActivityManagerService` pauses and stops User 0's foreground activities.
2. Broadcasts `Intent.ACTION_USER_BACKGROUND` to registered User 0 services.
3. Mounts User 10's virtualized storage namespaces.
4. Broadcasts `Intent.ACTION_USER_FOREGROUND` and `Intent.ACTION_USER_SWITCHED` to User 10 processes.
5. Restores User 10's window manager focus and personal wallpaper.

---

## 4. Multi-User Broadcast Routing & IPC Mediation

When an event occurs in the operating system (e.g., `ACTION_BATTERY_LOW` or `ACTION_PACKAGE_ADDED`), how does Android route the broadcast across multiple users?

### Cross-User Broadcast APIs

System components utilize explicit multi-user messaging primitives:

```java
// Broadcast delivered exclusively to User 10
context.sendBroadcastAsUser(intent, new UserHandle(10));

// System-wide broadcast delivered to all active users simultaneously
context.sendBroadcastAsUser(intent, UserHandle.ALL);
```

### Security Verification: `INTERACT_ACROSS_USERS`

Regular applications are strictly prohibited from sending or receiving cross-user broadcasts. If an application attempts to interact across user boundaries, `ActivityManagerService` validates permissions:

* `android.permission.INTERACT_ACROSS_USERS`: SignatureOrSystem permission allowing an application to query status across user profiles.
* `android.permission.INTERACT_ACROSS_USERS_FULL`: Higher-privilege permission required to initiate actions and modify settings on behalf of other users.

---

## 5. Attack Surfaces & Security Considerations

### 1. Cross-User IPC Data Leakage
System services that maintain in-memory caches or SQLite databases must tag every entry with the originating `userId`. Historically, vulnerabilities occurred in telephony and notification services that broadcasted incoming caller IDs or SMS snippet previews to `UserHandle.ALL`, leaking private notifications across user boundaries while a device was in Guest mode.

### 2. Shared External SD Card Vulnerabilities
If a physical removable MicroSD card is inserted into the device, FAT32 formatting prevents Linux UID segregation. Unless encrypted or managed via Storage Access Framework (SAF), any application with storage permissions running in User 10 can read files written to the external card by User 0.

### 3. Lockscreen Bypass via User Switching
In earlier Android releases, switching between a secure user profile (protected by a cryptographic PIN) and an unprotected Guest account caused race conditions in `KeyguardViewMediator`, temporarily exposing background activities of the primary user before Keyguard locked the display.

---

## Next in the Series: Chapter 5 Preview

In [Chapter 5: Cryptographic Providers](/posts/android-security-internals-chapter-5/), we will analyze:

* The Java Cryptography Architecture (JCA) in Android.
* The transition from Apache Harmony to `AndroidOpenSSL` / BoringSSL.
* `SecureRandom` entropy architecture and the historic Android PRNG vulnerability (CVE-2013-7372) that drained Bitcoin wallets.
* Hardware-backed cryptographic operations and Keymaster provider integration.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 4: "User Management," pp. 87–114.
2. [AOSP Documentation - Supporting Multiple Users](https://source.android.com/docs/devices/admin/multi-user)
3. [Android Enterprise - Work Profiles & Device Management](https://source.android.com/docs/devices/admin/managed-profiles)
4. Levin, Jonathan. *Android Internals: A Confectioner's Cookbook*. Technologeeks, 2014.
5. [LWN.net - Android storage and the sdcardfs filesystem](https://lwn.net/Articles/716447/)

---

## Let's Connect

Have you analyzed enterprise MDM containers or multi-user isolation on Android? Share your perspective:

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
"""

write_post("2026-11-01-android-security-internals-chapter-4.md", ch4_content)

