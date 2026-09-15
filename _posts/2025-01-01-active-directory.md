---
title: "Active Directory Security & Penetration Testing Overview"
date: 2025-01-01 12:01:00 +0300
categories: [Cyber Security, Active Directory]
tags: [active-directory, kerberos, bloodhound, privilege-escalation, pentesting]
description: "An architectural overview and research roadmap for Active Directory security, covering domain enumeration, Kerberos attacks, attack paths, AD CS vulnerabilities, and defensive hardening."
---

Active Directory (AD) forms the backbone of identity and access management for enterprise networks across the world. Because it controls user identities, computer accounts, authentication protocols, and access privileges, securing—and testing—Active Directory environments is one of the most vital disciplines in cybersecurity.

This overview outlines the fundamental concepts, attack vectors, defensive strategies, and essential resources for Active Directory penetration testing and security research.

---

## Core Domains & Technical Concepts

### 1. Domain Enumeration & Reconnaissance
* **PowerView & LDAP Queries**: Querying Domain Controllers (DCs) for users, groups, computer objects, Domain Admins, and Service Principal Names (SPNs).
* **BloodHound & SharpHound**: Graph-based analysis of Active Directory trust relationships, permission delegation, and hidden attack paths.

### 2. Authentication & Identity Attacks
* **Kerberoasting**: Requesting TGS service tickets for user accounts with SPNs set and cracking their hashes offline.
* **AS-REP Roasting**: Targeting user accounts that do not require Kerberos pre-authentication (`DONT_REQ_PREAUTH`).
* **Pass-the-Hash (PtH) & Pass-the-Ticket (PtT)**: Reusing NTLM hashes or Kerberos tickets (TGT/TGS) to authenticate across domain assets without needing plain-text credentials.

### 3. Active Directory Certificate Services (AD CS)
* **ESC1 to ESC13 Exploitation**: Identifying misconfigured certificate templates permitting arbitrary SAN specification, domain admin impersonation, and persistent credential theft.

### 4. Privilege Escalation & Lateral Movement
* **DCSync Attacks**: Leveraging `DS-Replication-Get-Changes` permissions to request password hashes directly from Domain Controllers.
* **Domain Trust Exploitation**: Traversing child-to-parent domain trusts using SID History injection and trust key compromise.

---

## Defensive Hardening & Mitigation

* **Tiered Administration Model**: Enforcing strict administrative separation (Tier 0, Tier 1, Tier 2) to prevent credential theft across security boundaries.
* **Privileged Access Workstations (PAWs)**: Isolating domain management tasks to dedicated, hardened host environments.
* **LAPS & gMSA Deployment**: Automating local administrator password management and service account credential rotation.
* **Continuous Auditing**: Implementing BloodHound Enterprise or Purple Knight for automated attack path management.

---

## References & Further Reading

1. [Microsoft Learn — Active Directory Domain Services Overview](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-domain-services)
2. [SpecterOps Research — Certified Pre-Owned: Abusing Active Directory Certificate Services](https://specterops.io/wp-content/uploads/2022/06/Certified_Pre-Owned.pdf)
3. [BloodHound Documentation — Graph-Based AD Attack Path Analysis](https://bloodhound.readthedocs.io/)
4. [MITRE ATT&CK Framework — Enterprise Matrix: Active Directory Techniques](https://attack.mitre.org/matrices/enterprise/)
5. [ADSecurity.org — Sean Metcalf's Active Directory Security Resource](https://adsecurity.org/)

---

## Let's Connect

Have a question, suggestion, or topic you'd like to discuss? Feel free to reach out or connect:

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) · [GitHub](https://github.com/3bdo-fathi) · [Contact Page](/contact-me/)

*— Abdulrahman M. Fathi*
