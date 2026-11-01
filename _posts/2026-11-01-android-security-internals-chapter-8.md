---
title: "Android Security Internals: Chapter 8 - Online Account Management"
date: 2026-11-01 16:00:00 +0300
categories: [Cyber Security, Android Security]
tags: [android, mobile security, internals, accountmanager, oauth, authentication, sso, access-control]
description: "A technical breakdown of Chapter 8 of Nikolay Elenkov's 'Android Security Internals', focusing on AccountManagerService, AbstractAccountAuthenticator, token delegation protocols, and OAuth security boundaries."
image:
  path: /assets/images/posts/android-security/chapter-8-cover.png
  alt: "Android Security Internals Chapter 8 Cover"
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Hello everyone,

Welcome back to our book summary series covering **"Android Security Internals"** by **Nikolay Elenkov**.

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

```text
Third-Party App (Client)
          |
          | 1. getAuthToken(account, "oauth2:scope")
          v
AccountManagerService (system_server)
   ├── 2. Checks permissions & caller signature
   ├── 3. Queries cache in /data/system/users/0/accounts.db
   └── 4. If token missing/expired, invokes Authenticator
          |
          v
Authenticator Service (e.g., Google Play Services)
   ├── 5. Prompts user login if needed
   ├── 6. Exchanges credentials with remote OAuth server
   └── 7. Returns token to AccountManagerService -> Client
```

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

This XML configuration binds the service to an account type:

```xml
<account-authenticator xmlns:android="http://schemas.android.com/apk/res/android"
    android:accountType="com.example.corporate.account"
    android:icon="@drawable/ic_corp_account"
    android:smallIcon="@drawable/ic_corp_small"
    android:label="@string/corp_account_label"
    android:accountPreferences="@xml/account_preferences" />
```

### The `AbstractAccountAuthenticator` Implementation

The authenticator overrides core lifecycle methods:

```java
public class CorporateAuthenticator extends AbstractAccountAuthenticator {
    @Override
    public Bundle getAuthToken(AccountAuthenticatorResponse response, 
                               Account account, 
                               String authTokenType, 
                               Bundle options) {
        // 1. Check if token exists in internal cache
        AccountManager am = AccountManager.get(mContext);
        String authToken = am.peekAuthToken(account, authTokenType);

        if (!TextUtils.isEmpty(authToken)) {
            Bundle result = new Bundle();
            result.putString(AccountManager.KEY_ACCOUNT_NAME, account.name);
            result.putString(AccountManager.KEY_ACCOUNT_TYPE, account.type);
            result.putString(AccountManager.KEY_AUTHTOKEN, authToken);
            return result;
        }

        // 2. If no valid token exists, return an Intent to launch LoginActivity
        Intent intent = new Intent(mContext, AuthenticatorActivity.class);
        intent.putExtra(AccountManager.KEY_ACCOUNT_AUTHENTICATOR_RESPONSE, response);
        
        Bundle bundle = new Bundle();
        bundle.putParcelable(AccountManager.KEY_INTENT, intent);
        return bundle;
    }
}
```

---

## 3. Storage and Token Persistence: `accounts.db`

The internal state of all registered accounts is managed by `AccountManagerService` inside `/data/system/users/[userId]/accounts.db`.

### Database Schema Structure

The SQLite database contains several critical tables:
* `accounts`: Stores `_id`, `name`, `type`, and an optional `password` field.
* `authtokens`: Stores `_id`, `accounts_id`, `type`, and the actual cached `authtoken` string.
* `grants`: Tracks which application UIDs have received user consent to access specific accounts.
* `extras`: Key-value configuration pairs associated with accounts.

```sql
-- SQLite table schema for authtokens
CREATE TABLE authtokens (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    accounts_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    authtoken TEXT,
    UNIQUE (accounts_id, type)
);
```

> **Security Warning**: Although `AccountManager.setPassword()` exists in the API, storing plaintext user passwords in `accounts.db` is an egregious security anti-pattern. Modern authenticators store **only** short-lived OAuth access tokens and refresh tokens in `authtokens`.

---

## 4. Security Access Controls & Delegation Boundaries

How does Android prevent an untrusted game or flashlight application from stealing corporate email authentication tokens?

### 1. Platform Permissions

To interact with `AccountManager`, applications historically required manifest permissions:
* `android.permission.GET_ACCOUNTS`: Required to query the list of active account names.
* `android.permission.USE_CREDENTIALS`: Required to request auth tokens for existing accounts.
* `android.permission.MANAGE_ACCOUNTS`: Required to create or remove accounts.

### 2. Signature Matching (Zero-Prompt Trust)

When App A requests an authentication token from Authenticator B:
1. `AccountManagerService` extracts the calling UID using `Binder.getCallingUid()`.
2. PMS retrieves the cryptographic signing certificates for both App A and Authenticator B.
3. If both packages are signed with the **exact same developer certificate**, `AccountManagerService` immediately returns the token. No prompt is displayed to the user!
4. This allows a suite of applications from the same vendor (e.g., Google Maps, YouTube, Gmail) to share identity seamlessly.

### 3. Interactive Consent (Third-Party Delegation)

If App A and Authenticator B are signed with different certificates:
1. `AccountManagerService` checks the `grants` table in `accounts.db`.
2. If no explicit grant exists, the framework halts the request and displays a system dialog:
   ```text
   "Allow [App A] to access your [Corporate] account?"
   ```
3. Only if the user explicitly approves does `AccountManagerService` write an authorization record into `grants` and release the auth token to App A.

---

## 5. Attack Surfaces & Exploitation Vectors

### 1. Token Harvesting via Overprivileged Permissions
In early Android versions, applications possessing `android.permission.USE_CREDENTIALS` could request authentication tokens for third-party accounts. Flaws in intent filtering allowed malicious apps to trigger silent token deliveries without proper user consent prompts.

### 2. Rogue Authenticator Spoofing
If an application declares an authenticator for a generic account type (e.g., `com.custom.auth`) that is not pre-installed on the device, the rogue application can capture user credentials entered into system account settings screens.

### 3. Unchecked Invalidation Attacks
An unprivileged application with access to an account can call `AccountManager.invalidateAuthToken()`. If executed in a continuous loop, it can trigger a Denial-of-Service (DoS) against legitimate background synchronization adapters by constantly invalidating cached tokens.

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
3. [Android Developers - Creating a Custom Account Authenticator](https://developer.android.com/training/sync-adapters/creating-authenticator)
4. RFC 6749: *The OAuth 2.0 Authorization Framework*. IETF, 2012.
5. Chin, Erika, et al. *Analyzing Inter-Application Communication in Android*. ACM MobiSys, 2011.

---

## Let's Connect

Have you audited mobile Single Sign-On (SSO) integrations or OAuth token flows on Android?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) | [GitHub](https://github.com/3bdo-fathi) | [Contact Page](/contact-me/)

- Abdulrahman Mohamed
