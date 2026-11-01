---
title: "Android Security Internals: Chapter 11 - NFC and Secure Elements"
date: 2026-11-01 19:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, nfc, hce, secure-element, contactless, smart-cards, apdu, emv]
description: "A technical dissection of Chapter 11 of Nikolay Elenkov's 'Android Security Internals', examining the NFC architecture stack, Host-based Card Emulation (HCE), ISO 7816-4 APDU routing, and hardware Secure Elements (UICC/eSE)."
image:
  path: /assets/images/posts/android-security/chapter-11-cover.png
  alt: "Android Security Internals Chapter 11 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**, enriched with EMV contactless payment specifications and wireless security research.

In [Chapter 10](/posts/android-security-internals-chapter-10/), we examined physical device security, full disk encryption, and verified boot integrity. In this installment, we explore **Chapter 11: NFC and Secure Elements**, dissecting the short-range wireless radio stack that powers contactless mobile payments, transit ticketing, access control badges, and cryptographic identity tokens.

For years, contactless mobile transactions were trapped behind a formidable architectural barrier: **telecom carrier control of the physical SIM card.**

In this deep dive, we trace the evolution from hardware-bound Secure Elements (UICC and eSE) to Android 4.4's industry-disrupting innovation: **Host-based Card Emulation (HCE)**. We will analyze the ISO 7816-4 smart card protocol, trace how `NfcService` dispatches APDUs, and evaluate contactless attack surfaces like relay attacks and rogue AID registrations.

![Android Security Internals Chapter 11](/assets/images/posts/android-security/chapter-11-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| [Chapter 10: Device Security](/posts/android-security-internals-chapter-10/) | **Chapter 11: NFC and Secure Elements** | [Chapter 12: SELinux in Android](/posts/android-security-internals-chapter-12/) |

---

## Key Takeaways

* **The Three Operating Modes**: Android's NFC subsystem operates in three distinct modes: Reader/Writer mode, Peer-to-Peer mode (Android Beam), and Card Emulation mode.
* **The Hardware Secure Element Bottleneck**: Early mobile payment deployments required a dedicated hardware Secure Element (UICC/SIM card or embedded eSE). Telecom carriers controlled cryptographic domain keys on the SIM via Single Wire Protocol (SWP), effectively preventing banks and software developers from issuing payment cards.
* **Host-based Card Emulation (HCE)**: Introduced in Android 4.4 (KitKat), HCE allows software applications to emulate contactless smart cards directly inside Android userspace, bypassing carrier-controlled hardware chips entirely.
* **ISO 7816-4 Smart Card Protocol**: NFC card transactions communicate via Application Protocol Data Units (APDUs). `NfcService` routes incoming command APDUs to registered applications using Application Identifiers (AIDs).
* **Payment Tokenization Defenses**: Because software-emulated cards running in Android userspace are theoretically vulnerable to memory inspection on rooted devices, the payment industry adopted **Cloud-Based Tokenization (DPANs)** and single-use transaction cryptograms.

---

## 1. The Android NFC Architecture Stack

Android's Near Field Communication stack spans from the physical radio controller chip to high-level framework services:

![Host-based Card Emulation & ISO 7816-4 APDU Routing](/assets/images/posts/android-security/ch11-hce-apdu.png)

### The Three NFC Operating Modes

1. **Reader/Writer Mode**: The device acts as an active NFC reader, powering and reading data from passive RFID/NFC tags, smart posters, and contactless cards (NDEF format).
2. **Peer-to-Peer (P2P) Mode**: Two Android devices communicate bidirectionally using the Simple NDEF Exchange Protocol (SNEP) to exchange URLs, contacts, or photos (Android Beam).
3. **Card Emulation Mode**: The Android smartphone behaves as a passive contactless smart card, responding to RF queries from point-of-sale (POS) payment terminals and transit gates.

---

## 2. Hardware Secure Elements: UICC vs. eSE

Before Host-based Card Emulation existed, mobile payment security relied exclusively on dedicated **Hardware Secure Elements (SE)**.

### Types of Hardware Secure Elements

1. **UICC (SIM Card)**: The subscriber identity module provided by the mobile operator. It contains a secure microcontroller running Java Card OS. The NFC controller links to the SIM card via a physical wire using the **Single Wire Protocol (SWP)**.
2. **eSE (Embedded Secure Element)**: A dedicated tamper-resistant silicon chip soldered directly onto the device motherboard by the OEM (e.g., Google Nexus S, modern Apple iPhones).

### Why Hardware SE Failed as a Mass Payment Solution

* **The Carrier Tollgate**: Because carriers owned the SIM card, any bank or merchant wishing to deploy a mobile wallet had to negotiate proprietary business and technical agreements with hundreds of regional telecom carriers globally.
* **Fragmentation**: Devices possessed incompatible secure element configurations, severely limiting developer adoption.

---

## 3. Host-based Card Emulation (HCE) Architecture

In Android 4.4, Google bypassed the hardware Secure Element bottleneck by introducing **Host-based Card Emulation (HCE)**:

```text
Contactless POS Terminal
          |
          | 13.56 MHz RF Field (ISO 14443-4)
          v
NFC Radio Controller
          |
          | Routes APDU packets directly over NCI bus
          v
libnfc-nci.so (Native HAL)
          |
          v
NfcService (system_server)
   ├── Extracts Application Identifier (AID) from SELECT command
   ├── Queries AID routing table
   └── Dispatches APDU to target application's HostApduService
          |
          v (Binder IPC)
Bank / Payment Application (HostApduService)
   └── Computes cryptogram and returns Response APDU
```

---

## 4. ISO 7816-4 APDU Protocol & AID Routing

Contactless smart cards communicate with terminals using **Application Protocol Data Units (APDUs)** conforming to the ISO/IEC 7816-4 standard.

### The APDU Communication Format

An APDU exchange follows a strict Command-Response cycle:

```text
Command APDU (Terminal -> Device):
[CLA (1B)] [INS (1B)] [P1 (1B)] [P2 (1B)] [Lc (1B)] [Data (variable)] [Le (1B)]

Response APDU (Device -> Terminal):
[Data (variable)] [Status Word SW1 (1B)] [Status Word SW2 (1B)]
```

For example, a successful transaction response terminates with the status bytes:
```text
SW1 SW2 = 0x90 0x00  (Success / OK)
```

### Implementing a `HostApduService`

```xml
<!-- In AndroidManifest.xml -->
<service android:name=".PaymentService"
         android:exported="true"
         android:permission="android.permission.BIND_NFC_SERVICE">
    <intent-filter>
        <action android:name="android.nfc.cardemulation.action.HOST_APDU_SERVICE"/>
    </intent-filter>
    <meta-data android:name="android.nfc.cardemulation.host_apdu_service"
               android:resource="@xml/apduservice"/>
</service>
```

```xml
<!-- res/xml/apduservice.xml -->
<host-apdu-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:description="@string/service_desc"
    android:requireDeviceUnlock="true">
    <aid-group android:description="@string/payment_group" android:category="payment">
        <!-- MasterCard Contactless AID -->
        <aid-filter android:name="A0000000041010" />
        <!-- Visa Contactless AID -->
        <aid-filter android:name="A0000000031010" />
    </aid-group>
</host-apdu-service>
```

---

## 5. EMV Transaction Flow & Cloud Tokenization

In a real-world contactless EMV transaction, the terminal and the phone exchange several standardized APDUs:

1. `SELECT PPSE`: Terminal queries the Proximity Payment System Environment (`2PAY.SYS.DDF01`).
2. `SELECT AID`: Terminal selects the specific payment network (Visa or MasterCard AID).
3. `GET PROCESSING OPTIONS (GPO)`: Phone supplies Application Interchange Profile (AIP) and Application File Locator (AFL).
4. `READ RECORDS`: Terminal extracts card metadata.
5. `GENERATE AC`: Phone generates an Application Cryptogram using a **Limited-Use Key (LUK)** provided by a cloud Token Service Provider (TSP).

Even if a malicious root app dumps memory, it only compromises a single-use token that cannot be used for subsequent unauthorized payments!

---

## Next in the Series: Chapter 12 Preview

In [Chapter 12: SELinux in Android](/posts/android-security-internals-chapter-12/), we will analyze:

* Mandatory Access Control (MAC) vs. Discretionary Access Control (DAC).
* The SEAndroid architecture, kernel security server, and Access Vector Cache (AVC).
* Compiling policy files (`sepolicy`, `file_contexts`, `seapp_contexts`, `mac_permissions.xml`).
* Project Treble split policies (`plat_sepolicy` vs `vendor_sepolicy`) and SELinux bypass exploitation.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 11: "NFC and Secure Elements," pp. 289–318.
2. [Android Developers - Host-based Card Emulation Overview](https://developer.android.com/develop/connectivity/nfc/hce)
3. ISO/IEC 7816-4: *Identification cards - Integrated circuit cards*.
4. EMVCo: *EMV Contactless Specifications for Payment Systems*.
5. Francis, Lishoy, et al. *Practical Relay Attack on Contactless POS Terminals*. IEEE RFID, 2012.

---

## Let's Connect

Have you audited mobile payment architectures or analyzed NFC smart card protocols?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
