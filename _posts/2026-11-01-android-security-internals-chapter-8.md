---
title: "Android Security Internals: Chapter 8 - Online Account Management"
date: 2026-11-01 16:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, accountmanager, oauth, authentication, sso, access-control, mastg]
description: "A technical breakdown of Chapter 8 of Nikolay Elenkov's 'Android Security Internals', focusing on AccountManagerService, AbstractAccountAuthenticator, token delegation protocols, OAuth security boundaries, and PKCE."
image:
  path: /assets/images/posts/android-security/chapter-8-cover.png
  alt: "Android Security Internals Chapter 8 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**, enriched with identity security research, OAuth 2.0 mobile security profiles, and auditing tradecraft from the **OWASP Mobile Application Security Verification Standard (MASVS-AUTH)**.

In [Chapter 7](/posts/android-security-internals-chapter-7/), we explored credential storage, master key derivation, and ARM TrustZone integration. In this installment, we explore **Chapter 8: Online Account Management**, analyzing how Android centralizes identity, manages authentication tokens, and provides seamless Single Sign-On (SSO) across applications.

Rather than forcing every application to implement its own login screens, store raw user passwords, and handle OAuth token refresh loops independently, Android introduced the **`AccountManager`** framework. In this chapter, we dissect how `AccountManagerService` coordinates authenticators, manages SQLite token storage, and enforces security boundaries to prevent unauthorized token harvesting.

![Android Security Internals Chapter 8](/assets/images/posts/android-security/chapter-8-cover.png)

---

### Series Navigation

| **Previous Chapter** | **Current Chapter** | **Next Chapter** |
| :---: | :---: | :---: |
| [Chapter 7: Credential Storage](/posts/android-security-internals-chapter-7/) | **Chapter 8: Online Account Management** | [Chapter 9: Enterprise Security](/posts/android-security-internals-chapter-9/) |

---

## Key Takeaways

* **Centralized Identity**: Android decouples account authentication from third-party applications. Apps request authentication tokens through `AccountManager` without ever handling raw user passwords.
* **The Authenticator Architecture**: Identity providers (Google, Microsoft, Twitter) implement an `AbstractAccountAuthenticator` service that handles login workflows, multi-factor authentication (MFA), and credential verification.
* **Token Storage in `accounts.db`**: Account metadata, user identifiers, and encrypted authentication tokens are stored per-user in `/data/system/users/[userId]/accounts.db`.
* **Caller Authorization & Signature Matching**: If a requesting application is signed with the **exact same cryptographic key** as the authenticator, `AccountManagerService` grants the auth token silently. Otherwise, an interactive user consent prompt is enforced.
* **Attack Surfaces**: Flawed authenticators that leak tokens via unverified intents, expose exported components, or store plain-text passwords can lead to account hijacking across the device.

---

## 1. The `AccountManager` Architectural Framework

Android's online account management framework is organized around three primary actors:

![AccountManager Authentication & Token Delegation Flow](/assets/images/posts/android-security/ch8-account-manager.png)

### Core Components

1. **`AccountManager`**: The client-side Java facade used by applications to list accounts, request tokens, and register listeners.
2. **`AccountManagerService`**: The centralized system service running inside `system_server`, mediating all account queries and persisting tokens on disk.
3. **`AbstractAccountAuthenticator`**: An abstract base class implemented by identity providers to handle provider-specific authentication flows.
4. **`accounts.db`**: An isolated SQLite database maintained per-user in `/data/system/users/[userId]/accounts.db`.

---

## 2. Implementing an Authenticator Service

To register a custom account type (e.g., `com.example.corporate.account`), a developer must declare a dedicated service in `AndroidManifest.xml`:

```xml
<service
    android:name=".sync.AccountAuthenticatorService"
    android:exported="true">
    <intent-filter>
        <action android:name="android.accounts.AccountAuthenticator" />
    </intent-filter>
    <meta-data
        android:name="android.accounts.AccountAuthenticator"
        android:resource="@xml/authenticator" />
</service>
```

### The Authenticator Metadata: `res/xml/authenticator.xml`

```xml
<account-authenticator xmlns:android="http://schemas.android.com/apk/res/android"
    android:accountType="com.example.corporate.account"
    android:icon="@drawable/ic_corp_account"
    android:smallIcon="@drawable/ic_corp_small"
    android:label="@string/corp_account_label"
    android:accountPreferences="@xml/account_preferences" />
```

---

## 3. Storage and Token Persistence: `accounts.db`

The internal state of all registered accounts is managed by `AccountManagerService` inside `/data/system/users/[userId]/accounts.db`.

```bash
# Inspect registered accounts via ADB shell
dumpsys account

# Inspecting accounts.db directly (requires root)
sqlite3 /data/system/users/0/accounts.db "SELECT _id, name, type FROM accounts;"
```

---

## 4. Modern OAuth 2.0 & Proof Key for Code Exchange (PKCE)

In modern enterprise mobile architectures, authenticators avoid storing static credentials and rely strictly on **OAuth 2.0 with PKCE (RFC 7636)**:

1. **Code Verifier**: The client generates a high-entropy cryptographic random string $V$.
2. **Code Challenge**: The client computes $C = 	ext{BASE64URL}(	ext{SHA256}(V))$.
3. **Authorization Request**: Sends $C$ to the authorization server via an in-app browser tab (Chrome Custom Tabs).
4. **Token Exchange**: When exchanging the authorization code, the client sends the original $V$. The server computes $	ext{SHA256}(V)$ and validates that it matches $C$.
5. **Security Defense**: Even if an attacker registers a rogue URI scheme handler to intercept the authorization code, they cannot exchange it for an access token without the secret code verifier $V$ stored in client memory!

---

## Next in the Series: Chapter 9 Preview

In [Chapter 9: Enterprise Security](/posts/android-security-internals-chapter-9/), we will analyze:

* The Device Administration API and `DevicePolicyManagerService` (DPMS).
* Enforcing lockscreen complexity, hardware camera disablement, and remote device wiping.
* Enterprise containerization architectures: Samsung KNOX and Android for Work (Managed Profiles).
* Mobile Device Management (MDM) enrollment workflows and ransomware abuse of device admin privileges.

---

## References & Authoritative Reading

1. Elenkov, Nikolay. *Android Security Internals*. No Starch Press, 2015. Chapter 8: "Online Account Management," pp. 191–214.
2. [Android Developers - AccountManager API Guide](https://developer.android.com/reference/android/accounts/AccountManager)
3. RFC 7636: *Proof Key for Code Exchange by OAuth Public Clients (PKCE)*. IETF, 2015.
4. [OWASP Mobile Application Security Verification Standard (MASVS-AUTH)](https://mas.owasp.org/)
5. Chin, Erika, et al. *Analyzing Inter-Application Communication in Android*. ACM MobiSys, 2011.

---

## Let's Connect

Have you audited mobile Single Sign-On (SSO) integrations or OAuth token flows on Android?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
