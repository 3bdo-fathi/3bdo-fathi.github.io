import re
import os

posts_data = [
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-1-system-security-x86-assembly.md",
        "diagram_img": "assets/images/posts/ecppt/part-1-diagram.png",
        "diagram_caption": "IA-32 Architecture: 32-bit Process Memory Layout & Stack Frame Anatomy",
        "diagram_section": """## Visual Architecture: Process Memory & Stack Frame Layout

The following technical diagram illustrates the complete memory mapping of a 32-bit process alongside the exact layer-by-layer anatomy of a function stack frame:

![IA-32 Architecture: 32-bit Process Memory Layout & Stack Frame Anatomy](/assets/images/posts/ecppt/part-1-diagram.png)

### Key Architectural Observations from the Diagram:
1. **Memory Separation**: The 4 GB address space is bifurcated between User Space (`0x00000000` to `0xBFFFFFFF` on Linux, or `0x7FFFFFFF` on standard Windows) and Kernel Space (`0xC0000000` to `0xFFFFFFFF`). User code cannot dereference Kernel page tables without generating an immediate `Access Violation (0xC0000005)` fault.
2. **Opposing Memory Growth**: The stack expands downward toward lower numerical memory addresses as items are pushed, while the dynamic heap expands upward toward higher memory addresses. This architectural decision preserves maximum contiguous unallocated space for runtime execution.
3. **The Exploit Bridge**: Notice how local variables at `[ebp - X]` sit directly adjacent to the `Saved EBP` and `Saved EIP` slots at `[ebp + 4]`. Because memory copy routines write from lower addresses toward higher addresses, any unbounded string copy into the local buffer inherently overwrites the return pointer.""",
        "attack_chain": """## Attack Chain Interconnection: Bridging Assembly to the Penetration Testing Lifecycle

Low-level assembly language and memory architecture are not isolated theoretical concepts; they form the operational foundation of the entire offensive assessment lifecycle:

```mermaid
flowchart LR
    Part1["Part 1: x86 Architecture & Stack Frames"] -->|Direct Foundation| Part2["Part 2: Custom Buffer Overflows & SEH Exploits"]
    Part1 -->|Memory Primitives| Part10["Part 10: In-Memory AMSI Patching via Reflection"]
    Part2 -->|Yields Initial Shell| Part5["Part 5: Local Privilege Escalation (SYSTEM / Root)"]
    Part5 -->|Enables Routing & Injections| Part6["Part 6: Multi-Tier Network Pivoting"]
```

* **Direct Feed into Part 2 (Exploit Development)**: Understanding that `EIP` points to the next executable instruction and that the stack pointer `ESP` can be referenced via `JMP ESP` instructions allows us to calculate exact byte offsets and construct weaponized stack buffer overflows.
* **Direct Feed into Part 10 (AMSI Evasion)**: In-memory memory patching techniques (such as replacing `AmsiScanBuffer` with `mov eax, 0x80070057; ret`) require understanding x86/x64 calling conventions and instruction byte opcodes.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Official Architecture & Compiler Specifications
* **Intel 64 and IA-32 Architectures Software Developer’s Manual**: Volumes 1, 2A-2D, and 3A-3D. [Intel Corporation Documentation](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html).
* **System V Application Binary Interface**: *Intel386 Architecture Processor Supplement (Fourth Edition)*.
* **Microsoft Learn: x86 Calling Conventions**: [https://learn.microsoft.com/en-us/cpp/cpp/argument-passing-and-naming-conventions](https://learn.microsoft.com/en-us/cpp/cpp/argument-passing-and-naming-conventions).

### 2. Seminal Security Research & Whitepapers
* **Phrack Magazine Issue 49**: *Smashing The Stack For Fun And Profit* by Aleph One (1996). [http://phrack.org/issues/49/14.html](http://phrack.org/issues/49/14.html).
* **OpenSecurityTraining2**: *Architecture 1001: x86-64 Assembly* by Xeno Kovah. [https://ost2.fyi/](https://ost2.fyi/).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1203**: Exploitation for Client Execution. [https://attack.mitre.org/techniques/T1203/](https://attack.mitre.org/techniques/T1203/).
* **T1055**: Process Injection. [https://attack.mitre.org/techniques/T1055/](https://attack.mitre.org/techniques/T1055/).

### 4. Interactive Practice Labs & Tooling
* **GEF (GDB Enhanced Features)**: Modern debugging environment for exploit developers. [https://github.com/hugsy/gef](https://github.com/hugsy/gef).
* **OverTheWire Wargames: Narnia & Protostar**: Classic hands-on binary exploitation practice. [https://overthewire.org/wargames/narnia/](https://overthewire.org/wargames/narnia/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-2-exploit-development-buffer-overflows.md",
        "diagram_img": "assets/images/posts/ecppt/part-2-diagram.png",
        "diagram_caption": "Binary Exploitation: Stack Buffer Overflows & SEH Overwrite Flow",
        "diagram_section": """## Visual Architecture: The Buffer Overflow & SEH Exploitation Lifecycle

The following diagram maps out the complete 4-stage binary exploitation pipeline alongside the exact memory mechanics of an SEH chain overwrite:

![Binary Exploitation: Stack Buffer Overflows & SEH Overwrite Flow](/assets/images/posts/ecppt/part-2-diagram.png)

### Key Architectural Observations from the Diagram:
1. **The Short Jump Bridge**: Notice how `nSEH` is overwritten with `\xeb\x06\x90\x90`. The opcode `\xeb\x06` instructs the CPU to take an unconditional relative short jump of exactly 6 bytes forward. This cleanly vaults over the 4-byte `SEH Handler` slot (which contains code pointers, not executable instructions), landing squarely into the NOP sled.
2. **SafeSEH Bypass Logic**: The `POP POP RET` address must be sourced from a binary module compiled without the `/SAFESEH` flag. If the target application attempts to dispatch an exception to a handler address not cataloged in the PE header's SafeSEH table, Windows immediately terminates the process.""",
        "attack_chain": """## Attack Chain Interconnection: Weaponizing Memory Corruption for Initial Access

In an enterprise penetration test, exploit development is not an academic puzzle; it is a critical initial access vector:

```mermaid
flowchart LR
    Part3["Part 3: Network Service Discovery (Open Port 9999)"] -->|Custom Service Found| Part2["Part 2: Custom Socket Buffer Overflow Exploit"]
    Part2 -->|Spawns Interactive Shell| Part5["Part 5: Windows Privilege Escalation (SYSTEM)"]
    Part5 -->|Harvests Network Interfaces| Part6["Part 6: Enterprise Pivoting to Internal LAN"]
```

* **Connection to Part 3 (Network Penetration Testing)**: During network service enumeration, you will discover unauthenticated proprietary daemons or legacy management services. Part 2 provides the exact fuzzing and exploitation toolkit to turn an open network port into an interactive shell.
* **Connection to Part 5 (Privilege Escalation)**: Network daemons frequently run under low-privileged service accounts (`LOCAL SERVICE`). Once your buffer overflow shell checks in, you immediately pivot to the Windows Privilege Escalation Playbook in Part 5.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Authoritative Exploit Writing Manuals
* **Corelan Team Exploit Writing Tutorials**: Parts 1 through 10 by Peter Van Eeckhoutte. [https://www.corelan.be/index.php/2009/07/19/exploit-writing-tutorial-part-1-stack-based-overflows/](https://www.corelan.be/index.php/2009/07/19/exploit-writing-tutorial-part-1-stack-based-overflows/).
* **Mona.py Official Repository & Command Reference**: [https://github.com/corelan/mona](https://github.com/corelan/mona).
* **Offensive Security: Exploit Development Prerequisites & Guides**: [https://www.offsec.com/](https://www.offsec.com/).

### 2. Practice Vulnerable Applications & Labs
* **Vulnserver Project**: A TCP-based server with intentionally vulnerable commands by Stephen Bradshaw. [http://www.thegreycorner.com/p/vulnserver.html](http://www.thegreycorner.com/p/vulnserver.html).
* **Exploit Database (Exploit-DB)**: Verified memory corruption exploits and shellcode repository. [https://www.exploit-db.com/](https://www.exploit-db.com/).
* **TryHackMe: Buffer Overflow Prep**: Dedicated hands-on OSCP/eCPPT practice room. [https://tryhackme.com/room/bufferoverflowprep](https://tryhackme.com/room/bufferoverflowprep).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1203**: Exploitation for Client Execution. [https://attack.mitre.org/techniques/T1203/](https://attack.mitre.org/techniques/T1203/).
* **T1059**: Command and Scripting Interpreter. [https://attack.mitre.org/techniques/T1059/](https://attack.mitre.org/techniques/T1059/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-3-network-penetration-testing.md",
        "diagram_img": "assets/images/posts/ecppt/part-3-diagram.png",
        "diagram_caption": "Network Penetration Testing: Discovery, Enumeration & MITM Attacks",
        "diagram_section": """## Visual Architecture: Network Reconnaissance & Attack Vectors

The following diagram breaks down packet-level scanning mechanics alongside the operational execution flow of LLMNR/NBT-NS poisoning and real-time SMB relaying:

![Network Penetration Testing: Discovery, Enumeration & MITM Attacks](/assets/images/posts/ecppt/part-3-diagram.png)

### Key Architectural Observations from the Diagram:
1. **Half-Open Advantage**: The SYN stealth scan never sends the final `ACK` packet. Because the TCP 3-way handshake is never completed, standard application socket APIs (such as `accept()`) never trigger, bypassing application-level connection logging.
2. **Relay Prerequisite**: Notice that SMB Relaying requires **SMB Message Signing to be Disabled** on the target server. If signing is enforced, the target server verifies cryptographic signatures computed with the session key, causing the relayed authentication to fail.""",
        "attack_chain": """## Attack Chain Interconnection: Propagating from Reconnaissance to Network Domination

Network reconnaissance is the strategic engine that drives every subsequent phase of an engagement:

```mermaid
flowchart LR
    Part3["Part 3: Network Recon & LLMNR Poisoning"] -->|Discovers Domain Controller & SPNs| Part4["Part 4: Active Directory Kerberos Exploitation"]
    Part3 -->|Captures NetNTLMv2 Admin Hash| Part6["Part 6: Lateral Movement (Pass-the-Hash via WMIExec)"]
    Part3 -->|Identifies Web Port 80/443| Part8["Part 8: Web Application Exploitation (SQLi / LFI)"]
```

* **Direct Feed into Part 4 (Active Directory)**: Network port scanning identifies the primary Domain Controllers (ports 88 Kerberos, 389 LDAP, 445 SMB) and enumerates service accounts configured with Service Principal Names (SPNs).
* **Direct Feed into Part 6 (Pivoting & Lateral Movement)**: Discovering dual-homed hosts and extracting valid NetNTLMv2 hashes enables immediate lateral movement across internal subnets using Pass-the-Hash.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Networking Standards & Official RFCs
* **RFC 793**: Transmission Control Protocol (TCP) Specification. [https://www.rfc-editor.org/rfc/rfc793](https://www.rfc-editor.org/rfc/rfc793).
* **RFC 1001 / 1002**: Protocol Standard for a NetBIOS Service on a TCP/UDP Transport.
* **RFC 4795**: Link-Local Multicast Name Resolution (LLMNR). [https://www.rfc-editor.org/rfc/rfc4795](https://www.rfc-editor.org/rfc/rfc4795).

### 2. Offensive Tooling Repositories
* **Nmap Network Scanning**: Official Reference by Gordon "Fyodor" Lyon. [https://nmap.org/book/](https://nmap.org/book/).
* **SpiderLabs Responder**: LLMNR/NBT-NS/MDNS poisoner and credential harvester. [https://github.com/SpiderLabs/Responder](https://github.com/SpiderLabs/Responder).
* **SecureAuth Impacket Suite**: Python classes for working with network protocols. [https://github.com/fortra/impacket](https://github.com/fortra/impacket).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1046**: Network Service Discovery. [https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/).
* **T1557.001**: LLMNR/NBT-NS Poisoning and SMB Relay. [https://attack.mitre.org/techniques/T1557/001/](https://attack.mitre.org/techniques/T1557/001/).
* **T1187**: Forced Authentication. [https://attack.mitre.org/techniques/T1187/](https://attack.mitre.org/techniques/T1187/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-4-active-directory-penetration-testing.md",
        "diagram_img": "assets/images/posts/ecppt/part-4-diagram.png",
        "diagram_caption": "Active Directory Attack Vectors: Kerberos Exploitation & Persistence",
        "diagram_section": """## Visual Architecture: Kerberos Authentication Flow & Attack Graph

The following technical diagram contrasts the 5-step Kerberos protocol exchange with the exact interception points for Kerberoasting and AS-REP Roasting, alongside BloodHound shortest attack paths:

![Active Directory Attack Vectors: Kerberos Exploitation & Persistence](/assets/images/posts/ecppt/part-4-diagram.png)

### Key Architectural Observations from the Diagram:
1. **The Kerberoasting Vulnerability**: Notice step 4 of the exchange. When a user requests access to an SPN, the KDC issues a TGS ticket encrypted with the **target service account's NTLM password hash**. Because the client must deliver this ticket to the service, the client receives the encrypted blob, allowing offline brute-force attacks against weak service passwords.
2. **Golden vs. Silver Tickets**: A Golden Ticket requires the `krbtgt` account hash and forges a TGT (Ticket Granting Ticket), making it effective across the entire forest. A Silver Ticket requires only the specific service account's hash, forging a TGS ticket directly. Because the service validates the ticket using its own secret key, **a Silver Ticket never communicates with the Domain Controller**, making it invisible in DC security event logs!""",
        "attack_chain": """## Attack Chain Interconnection: Escalating from Domain User to Forest Enterprise Admin

Active Directory penetration testing represents the strategic center of an internal enterprise compromise:

```mermaid
flowchart LR
    Part3["Part 3: Network Recon / LLMNR Poisoning"] -->|Yields Domain Credentials| Part4["Part 4: BloodHound Enumeration & Kerberoasting"]
    Part4 -->|Extracts Service Account Hash| Part4Crack["Hashcat Mode 13100 Cracking (Domain Admin Pass)"]
    Part4Crack -->|Enables Remote DCSync| Part4DCSync["DCSync: krbtgt Hash Harvested"]
    Part4DCSync -->|Forges Golden Ticket| Part7["Part 7: Persistent C2 Beaconing as Domain Admin"]
```

* **Connection to Part 5 (Privilege Escalation)**: Once BloodHound identifies a workstation on which your domain user has local administrator rights, you execute local privilege escalation (Part 5) to dump the LSASS memory of logged-in Domain Admins.
* **Connection to Part 6 (Pivoting)**: Using harvested NTLM hashes or Kerberos tickets, you establish SOCKS tunnels via Ligolo-ng or SSH (Part 6) to remotely compromise Domain Controllers located in isolated server subnets.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Microsoft Protocol Standards & Whitepapers
* **Microsoft MS-KILE**: Kerberos Protocol Extensions Specification. [https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-kile/](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-kile/).
* **Microsoft MS-DRSR**: Directory Replication Service Remote Protocol (DCSync Primitives).
* **Sean Metcalf's ADSecurity.org**: The premier technical blog on Active Directory security and Kerberos attacks. [https://adsecurity.org/](https://adsecurity.org/).

### 2. Industry-Standard Offensive AD Tooling
* **BloodHound by SpecterOps**: Six Degrees of Domain Admin graph analysis. [https://github.com/SpecterOps/BloodHound](https://github.com/SpecterOps/BloodHound).
* **Rubeus by HarmJ0y (Will Schroeder)**: C# toolset for raw Kerberos interaction. [https://github.com/GhostPack/Rubeus](https://github.com/GhostPack/Rubeus).
* **Mimikatz by Benjamin Delpy**: Extraction of plaintext passwords, hashes, and ticket forging. [https://github.com/gentilkiwi/mimikatz](https://github.com/gentilkiwi/mimikatz).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1558.003**: Steal or Forge Kerberos Tickets: Kerberoasting. [https://attack.mitre.org/techniques/T1558/003/](https://attack.mitre.org/techniques/T1558/003/).
* **T1558.004**: Steal or Forge Kerberos Tickets: AS-REP Roasting. [https://attack.mitre.org/techniques/T1558/004/](https://attack.mitre.org/techniques/T1558/004/).
* **T1558.001**: Steal or Forge Kerberos Tickets: Golden Ticket. [https://attack.mitre.org/techniques/T1558/001/](https://attack.mitre.org/techniques/T1558/001/).
* **T1003.006**: OS Credential Dumping: DCSync. [https://attack.mitre.org/techniques/T1003/006/](https://attack.mitre.org/techniques/T1003/006/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-5-privilege-escalation-playbook.md",
        "diagram_img": "assets/images/posts/ecppt/part-5-diagram.png",
        "diagram_caption": "Windows & Linux Privilege Escalation: Primitives & Decision Engine",
        "diagram_section": """## Visual Architecture: Privilege Escalation Primitives & Decision Engine

The following diagram maps out the primary attack vectors across both operating systems alongside the Potato token impersonation architecture:

![Windows & Linux Privilege Escalation: Primitives & Decision Engine](/assets/images/posts/ecppt/part-5-diagram.png)

### Key Architectural Observations from the Diagram:
1. **The Token Impersonation Pivot**: Service accounts (`LOCAL SERVICE`, `NETWORK SERVICE`, `IIS APPPOOL`) routinely possess `SeImpersonatePrivilege`. The "Potato" family exploits this by running a rogue local RPC listener, forcing a `SYSTEM` process (like DCOM or Print Spooler) to authenticate against it, and invoking `ImpersonateNamedPipeClient()` to grab the elevated token.
2. **Linux Capability Granularity**: Linux capabilities bypass the binary all-or-nothing nature of SUID. When an administrator grants `cap_setuid+ep` to a scripting engine such as Python or Perl, it grants that process the absolute power to invoke `setuid(0)`, yielding immediate root access.""",
        "attack_chain": """## Attack Chain Interconnection: Elevating to SYSTEM / Root to Enable Multi-Tier Pivoting

Privilege escalation is the mandatory bridge between an initial foothold and lateral expansion:

```mermaid
flowchart LR
    Part8["Part 8: Web Exploitation (webshell as www-data)"] -->|Initial Access| Part5["Part 5: Local Privilege Escalation (Root / SYSTEM)"]
    Part5 -->|Enables Memory Dumping| Part4["Part 4: Extract LSASS Domain Admin Hashes"]
    Part5 -->|Enables Interface Promiscuity| Part6["Part 6: Configure Ligolo-ng TUN Pivot Routes"]
```

* **Connection to Part 4 (Active Directory)**: Standard users cannot access the memory space of `lsass.exe`. Escalating to `NT AUTHORITY\SYSTEM` in Part 5 is required before invoking `Invoke-Mimikatz` or executing DCSync attacks.
* **Connection to Part 6 (Pivoting)**: Creating virtual network TUN interfaces via `Ligolo-ng` or binding privileged raw sockets for packet forwarding requires root or administrative privileges on the pivot host.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Curated Privilege Escalation Repositories
* **GTFOBins**: Curated list of Unix binaries used to bypass local security restrictions. [https://gtfobins.github.io/](https://gtfobins.github.io/).
* **LOLBAS Project**: Living Off The Land Binaries, Scripts, and Libraries for Windows. [https://lolbas-project.github.io/](https://lolbas-project.github.io/).
* **PayloadsAllTheThings**: Comprehensive privilege escalation cheatsheets. [https://github.com/swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings).

### 2. Exploit Source Code & Research
* **PrintSpoofer by itm4n**: Named pipe impersonation exploit targeting `SeImpersonatePrivilege`. [https://github.com/itm4n/PrintSpoofer](https://github.com/itm4n/PrintSpoofer).
* **GodPotato by BeichenDream**: Universal token impersonation targeting Windows Server 2012 through 2022. [https://github.com/BeichenDream/GodPotato](https://github.com/BeichenDream/GodPotato).
* **PEASS-ng (WinPEAS & LinPEAS)**: Automated local privilege escalation scanners by Carlos Polop. [https://github.com/peass-ng/PEASS-ng](https://github.com/peass-ng/PEASS-ng).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1548**: Abuse Elevation Control Mechanism (Bypass UAC, SUID/SGID). [https://attack.mitre.org/techniques/T1548/](https://attack.mitre.org/techniques/T1548/).
* **T1134**: Access Token Manipulation. [https://attack.mitre.org/techniques/T1134/](https://attack.mitre.org/techniques/T1134/).
* **T1574**: Hijack Execution Flow (DLL Search Order, PATH Hijacking). [https://attack.mitre.org/techniques/T1574/](https://attack.mitre.org/techniques/T1574/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-6-lateral-movement-and-pivoting.md",
        "diagram_img": "assets/images/posts/ecppt/part-6-diagram.png",
        "diagram_caption": "Multi-Tier Enterprise Pivoting: SSH Tunneling vs Ligolo-ng Routing",
        "diagram_section": """## Visual Architecture: Multi-Tier Pivoting & Tunneling Mechanics

The following technical diagram contrasts the legacy SSH port forwarding techniques with modern Layer-3 TUN interface routing via Ligolo-ng across segmented DMZs:

![Multi-Tier Enterprise Pivoting: SSH Tunneling vs Ligolo-ng Routing](/assets/images/posts/ecppt/part-6-diagram.png)

### Key Architectural Observations from the Diagram:
1. **Layer-3 vs. Layer-7 Proxies**: Traditional SOCKS5 proxies operate at Layer-7 (Application layer). Security tools must explicitly support SOCKS proxies, and tools that rely on raw packet crafting (like Nmap SYN scan `-sS`, masscan, or ICMP ping) fail completely.
2. **The Ligolo-ng TUN Advantage**: By instantiating a virtual Layer-3 network device (`dev ligolo`) on Kali Linux, the operating system kernel handles the IP packet encapsulation. You add routes via `ip route add 172.16.1.0/24 dev ligolo`, allowing all native security tools to operate without `proxychains`!""",
        "attack_chain": """## Attack Chain Interconnection: Traversing Deeply Segmented Enterprise Networks

Pivoting is the logistical backbone of every advanced penetration test:

```mermaid
flowchart LR
    Part5["Part 5: Local PrivEsc (SYSTEM on DMZ Server)"] -->|Enables TUN Interface Setup| Part6["Part 6: Configure Ligolo-ng Layer-3 Pivot"]
    Part6 -->|Direct Access to Internal Subnet| Part4["Part 4: Attack Internal Active Directory Domain Controller"]
    Part6 -->|Direct Access to Database Enclave| Part2["Part 2: Exploit Internal Legacy Services via BOF"]
```

* **Connection to Part 4 (Active Directory)**: Corporate Domain Controllers are rarely placed in internet-facing DMZs. Establishing a Ligolo-ng or Chisel tunnel in Part 6 allows you to run BloodHound, PowerView, and Kerberoasting against internal DCs from your Kali machine.
* **Connection to Part 7 (Command & Control)**: When internal victim machines lack direct egress internet connectivity, you configure C2 internal redirectors or SMB named pipe listeners to pivot C2 beacons out through your established tunnels.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Tunneling & Routing Repositories
* **Ligolo-ng Repository & User Documentation**: [https://github.com/nico-cha/ligolo-ng](https://github.com/nico-cha/ligolo-ng).
* **Chisel by Jaime Pillora**: Fast TCP/UDP tunnel over HTTP with SSH encryption. [https://github.com/jpillora/chisel](https://github.com/jpillora/chisel).
* **Proxychains-ng (New Generation)**: Dynamic SOCKS proxy router. [https://github.com/rofl0r/proxychains-ng](https://github.com/rofl0r/proxychains-ng).

### 2. Lateral Movement Tooling
* **Evil-WinRM by Hackplayers**: The ultimate WinRM shell for offensive operations. [https://github.com/Hackplayers/evil-winrm](https://github.com/Hackplayers/evil-winrm).
* **Impacket WMIExec & PsExec**: High-fidelity lateral movement scripts. [https://github.com/fortra/impacket](https://github.com/fortra/impacket).
* **SANS Institute: Pivoting and Port Forwarding Cheat Sheet**: [https://www.sans.org/posters/pivoting-and-port-forwarding/](https://www.sans.org/posters/pivoting-and-port-forwarding/).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1090**: Proxy (Multi-hop Proxies, External/Internal Proxies). [https://attack.mitre.org/techniques/T1090/](https://attack.mitre.org/techniques/T1090/).
* **T1021**: Remote Services (SMB, WinRM, RDP). [https://attack.mitre.org/techniques/T1021/](https://attack.mitre.org/techniques/T1021/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-7-command-and-control-c2.md",
        "diagram_img": "assets/images/posts/ecppt/part-7-diagram.png",
        "diagram_caption": "Resilient C2 Architecture: Tiered Redirectors, Domain Fronting & OpSec",
        "diagram_section": """## Visual Architecture: Resilient Multi-Tier C2 Infrastructure

The following diagram maps out the tiered defense evasion architecture utilized in modern red team operations, combining CDN edge workers, Apache `mod_rewrite` redirectors, and team servers:

![Resilient C2 Architecture: Tiered Redirectors, Domain Fronting & OpSec](/assets/images/posts/ecppt/part-7-diagram.png)

### Key Architectural Observations from the Diagram:
1. **Sacrificial Edge Layer**: Frontline redirectors bear all the risk. If a threat hunter discovers a beacon IP address and blacklists it, only the disposable redirector is burned. The core team server remains completely hidden on a private WireGuard VPN subnet.
2. **The Malleable Profile**: C2 communications are customized to blend with benign background traffic. HTTP headers, cookies, URIs, and POST parameters are disguised to emulate legitimate enterprise web applications (such as Microsoft Office 365 or Google Analytics telemetry).""",
        "attack_chain": """## Attack Chain Interconnection: Orchestrating Stealthy Campaign Persistence

Command and Control (C2) provides the command infrastructure that powers post-exploitation:

```mermaid
flowchart LR
    Part7["Part 7: Multi-Tier C2 Infrastructure (Empire/Starkiller)"] -->|Generates Obfuscated Stagers| Part9["Part 9: Weaponized Phishing & HTML Smuggling Payloads"]
    Part9 -->|Executes in Victim Memory| Part10["Part 10: In-Memory AMSI Bypass & PowerSploit"]
    Part10 -->|Maintains Persistent Beacon| Part7Checkin["Steady C2 Agent Session Established!"]
```

* **Connection to Part 9 (Client-Side Attacks)**: The listeners configured in Part 7 generate the stager payloads embedded into VBA Office macros and HTML Smuggling downloads in Part 9.
* **Connection to Part 10 (PowerShell for Pentesters)**: The Empire agent executes in-memory PowerShell commands. Combining Empire with in-memory AMSI patching in Part 10 guarantees that Windows Defender will not kill the agent process upon check-in.""",
        "references": """## Categorized References & Authoritative Sources

### 1. C2 Evaluation & Modern Frameworks
* **The C2 Matrix Project** by Jorge Orchilles: Comprehensive taxonomy of C2 frameworks. [https://www.thec2matrix.com/](https://www.thec2matrix.com/).
* **BC-Security PowerShell-Empire & Starkiller Documentation**: [https://bc-security.gitbook.io/empire-wiki/](https://bc-security.gitbook.io/empire-wiki/).
* **BishopFox Sliver C2 Framework**: Cross-platform open-source C2. [https://github.com/BishopFox/sliver](https://github.com/BishopFox/sliver).

### 2. Red Team Infrastructure & OpSec Research
* **Red Team Infrastructure Wiki**: *Automated C2 Redirection with Apache and Nginx* by Steve Borosh & Jeff Dimmock. [https://github.com/bluscreenofjeff/Red-Team-Infrastructure-Wiki](https://github.com/bluscreenofjeff/Red-Team-Infrastructure-Wiki).
* **Salesforce Engineering: Open-Sourcing JA3 & JA3S**: TLS client and server fingerprinting for threat detection.
* **Malleable C2 Profiles Reference Guide**: Customizing beacon telemetry syntax.

### 3. MITRE ATT&CK Enterprise Techniques
* **T1071**: Application Layer Protocol (Web Protocols, DNS). [https://attack.mitre.org/techniques/T1071/](https://attack.mitre.org/techniques/T1071/).
* **T1090.004**: Proxy: Domain Fronting. [https://attack.mitre.org/techniques/T1090/004/](https://attack.mitre.org/techniques/T1090/004/).
* **T1027**: Obfuscated/Encrypted Payloads. [https://attack.mitre.org/techniques/T1027/](https://attack.mitre.org/techniques/T1027/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-8-web-application-penetration-testing.md",
        "diagram_img": "assets/images/posts/ecppt/part-8-diagram.png",
        "diagram_caption": "Web Application Penetration Testing: OWASP WSTG Exploitation Matrix",
        "diagram_section": """## Visual Architecture: OWASP WSTG Exploitation Matrix

The following technical diagram details the exploitation workflows for Union-Based SQL Injection, Local File Inclusion to RCE via Log Poisoning, and multi-layer file upload filter evasion:

![Web Application Penetration Testing: OWASP WSTG Exploitation Matrix](/assets/images/posts/ecppt/part-8-diagram.png)

### Key Architectural Observations from the Diagram:
1. **The Log Poisoning Mechanism**: Web servers log incoming request metadata into filesystem flat files (e.g. `access.log`). If an application contains an LFI vulnerability and has read permissions over the log file, injecting executable code into the `User-Agent` HTTP header causes the PHP interpreter to parse the log contents as code when included.
2. **Image Polyglot Defense Bypass**: Simple extension changes (`.php.jpg`) are often blocked by validation routines that check the initial byte sequence ("Magic Bytes"). By injecting a webshell into a legitimate JPEG's comment block via `exiftool`, the file satisfies both extension checks and binary magic byte inspections.""",
        "attack_chain": """## Attack Chain Interconnection: Transforming Web Access into Internal Network Compromise

Web application security testing is the primary vector for establishing the initial foothold:

```mermaid
flowchart LR
    Part8["Part 8: Web Pentesting (LFI Log Poisoning / SQLi)"] -->|Yields Web Shell as www-data| Part5["Part 5: Linux Privilege Escalation (to root)"]
    Part5 -->|Discovers Internal Network Interfaces| Part6["Part 6: Multi-Tier Pivoting into Internal LAN"]
    Part6 -->|Scans Internal Windows Subnet| Part3["Part 3: Network Attacks & Active Directory"]
```

* **Connection to Part 5 (Privilege Escalation)**: Gaining a webshell gives you code execution under the `www-data` or `apache` user account. You immediately transition to Part 5's Linux Privilege Escalation Playbook (SUID binaries, sudo rules) to gain root.
* **Connection to Part 6 (Pivoting)**: Production web servers reside in the corporate DMZ. Once you gain root on the web server, you configure a Ligolo-ng TUN interface in Part 6 to pivot straight into the company's internal network.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Industry Standards & Testing Methodologies
* **OWASP Web Security Testing Guide (WSTG v4.2)**: The comprehensive guide for testing web applications. [https://owasp.org/www-project-web-security-testing-guide/](https://owasp.org/www-project-web-security-testing-guide/).
* **OWASP Application Security Verification Standard (ASVS)**: Architectural security framework. [https://owasp.org/www-project-application-security-verification-standard/](https://owasp.org/www-project-application-security-verification-standard/).
* **OWASP Top 10:2021**: The official list of critical web security risks. [https://owasp.org/Top10/](https://owasp.org/Top10/).

### 2. Hands-on Training & Exploitation Dictionaries
* **PortSwigger Web Security Academy**: Free, interactive web security labs and learning materials. [https://portswigger.net/web-security](https://portswigger.net/web-security).
* **PayloadsAllTheThings - Web Exploitation Repository**: Curated cheat sheets for SQLi, LFI, SSRF, and file uploads. [https://github.com/swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings).
* **SecLists Fuzzing Dictionaries by Daniel Miessler**: Comprehensive wordlists for directory discovery. [https://github.com/danielmiessler/SecLists](https://github.com/danielmiessler/SecLists).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1190**: Exploit Public-Facing Application. [https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/).
* **T1059.006**: Command and Scripting Interpreter: Python/PHP. [https://attack.mitre.org/techniques/T1059/006/](https://attack.mitre.org/techniques/T1059/006/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-9-client-side-attacks.md",
        "diagram_img": "assets/images/posts/ecppt/part-9-diagram.png",
        "diagram_caption": "Client-Side Attack Architecture: Weaponization, Delivery & MOTW Evasion",
        "diagram_section": """## Visual Architecture: Client-Side Weaponization & Delivery Pipeline

The following technical diagram details the 4-phase client-side attack lifecycle, from psychological pretexting and email deliverability alignment to HTML Smuggling and container-based MOTW evasion:

![Client-Side Attack Architecture: Weaponization, Delivery & MOTW Evasion](/assets/images/posts/ecppt/part-9-diagram.png)

### Key Architectural Observations from the Diagram:
1. **The HTML Smuggling Delivery Mechanism**: By generating a dynamic file inside a JavaScript `Blob` and triggering a synthetic `a.click()` event, the file is assembled directly in browser memory. Perimeter web filtering appliances inspect the HTTP transmission and see only benign HTML and JavaScript, completely failing to detect the compiled executable or ISO container crossing the perimeter.
2. **The MOTW Container Bypass**: Standard files downloaded via web browsers inherit the NTFS `Zone.Identifier=3` alternate data stream. Encapsulating payloads inside an `.iso` container ensures that when a victim double-clicks to mount the ISO, Windows Explorer assigns it a virtual drive letter, stripping the zone flag from files inside!""",
        "attack_chain": """## Attack Chain Interconnection: Bypassing Perimeter Defenses to Deliver C2 Implants

Client-side attacks represent the ultimate initial access vector when server-side perimeters are impenetrable:

```mermaid
flowchart LR
    Part9["Part 9: Phishing / HTML Smuggling Weaponization"] -->|Victim Executes Container Payload| Part7["Part 7: First C2 Beacon Checks into Team Server"]
    Part7 -->|Injects In-Memory Commands| Part10["Part 10: In-Memory AMSI Bypass & PowerSploit"]
    Part10 -->|Dumps Domain Credentials| Part4["Part 4: Lateral Domain Dominance (Active Directory)"]
```

* **Connection to Part 7 (C2 Infrastructure)**: The payload delivered by your HTML Smuggling or VBA macro is configured to establish a reverse HTTPS beacon back to the multi-tier C2 redirectors built in Part 7.
* **Connection to Part 10 (PowerShell for Pentesters)**: Windows endpoints are equipped with Windows Defender and AMSI. Delivering a PowerShell stager via client-side phishing requires executing the in-memory AMSI memory patch from Part 10 to prevent Defender from killing the process upon arrival.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Phishing & Weaponization Tooling
* **GoPhish Official Framework Documentation**: [https://getgophish.com/documentation/](https://getgophish.com/documentation/).
* **MacroPack by Sevagas**: Automated Office document weaponization and macro obfuscation. [https://github.com/sevagas/macro_pack](https://github.com/sevagas/macro_pack).
* **Outflank Research: HTML Smuggling**: Deep-dive analysis of browser blob assembly. [https://outflank.nl/blog/2020/08/18/html-smuggling/](https://outflank.nl/blog/2020/08/18/html-smuggling/).

### 2. Email Deliverability RFC Specifications
* **RFC 7208**: Sender Policy Framework (SPF) for Authorizing Email Senders.
* **RFC 6376**: DomainKeys Identified Mail (DKIM) Signatures.
* **RFC 7489**: Domain-based Message Authentication, Reporting, and Conformance (DMARC).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1566.001**: Phishing: Spearphishing Attachment. [https://attack.mitre.org/techniques/T1566/001/](https://attack.mitre.org/techniques/T1566/001/).
* **T1566.002**: Phishing: Spearphishing Link. [https://attack.mitre.org/techniques/T1566/002/](https://attack.mitre.org/techniques/T1566/002/).
* **T1204.002**: User Execution: Malicious File. [https://attack.mitre.org/techniques/T1204/002/](https://attack.mitre.org/techniques/T1204/002/).
* **T1027.006**: HTML Smuggling. [https://attack.mitre.org/techniques/T1027/006/](https://attack.mitre.org/techniques/T1027/006/)."""
    },
    {
        "filename": "_posts/2026-11-11-ecppt-v3-part-10-powershell-for-pentesters.md",
        "diagram_img": "assets/images/posts/ecppt/part-10-diagram.png",
        "diagram_caption": "Offensive PowerShell & AMSI Evasion Architecture",
        "diagram_section": """## Visual Architecture: Offensive PowerShell & AMSI Memory Hooking

The following technical diagram breaks down the PowerShell in-memory download cradle execution lifecycle, the PowerSploit modular ecosystem, and the internal memory patch applied to `AmsiScanBuffer`:

![Offensive PowerShell & AMSI Evasion Architecture](/assets/images/posts/ecppt/part-10-diagram.png)

### Key Architectural Observations from the Diagram:
1. **The In-Memory Hook**: Because `amsi.dll` is mapped into user-mode address space within the attacker's `powershell.exe` process, no administrator rights are required to alter its memory protection. Calling `VirtualProtect` to make the memory page writable (`0x40`) allows us to overwrite the function entry point with `mov eax, 0x80070057; ret` (Hex: `B8 57 00 07 80 C3`).
2. **Defeating Script Block Logging**: Script Block Logging (EID 4104) logs the full, unobfuscated code block immediately prior to execution. By using AST obfuscation via `Invoke-Obfuscation` or tampering with the internal `ScriptBlockLogging` registry/memory flags, operators prevent forensic audit logging from capturing command syntax.""",
        "attack_chain": """## Attack Chain Interconnection: Executing Fileless In-Memory Operations to Seal Complete Campaign Dominance

Offensive PowerShell is the execution medium that connects post-exploitation objectives across the enterprise:

```mermaid
flowchart LR
    Part9["Part 9: Client-Side Phishing Stager Execution"] -->|Spawns Hidden PowerShell| Part10["Part 10: In-Memory AMSI Patch Hook Applied"]
    Part10 -->|Loads PowerView in RAM| Part4["Part 4: Execute Kerberoasting & DCSync Attacks"]
    Part10 -->|Loads PowerUp in RAM| Part5["Part 5: Local Privilege Escalation Audit"]
    Part10 -->|Injects Shellcode into Explorer| Part7["Part 7: Persistent C2 Agent Communications"]
```

* **Connection to Part 4 (Active Directory)**: Using `PowerView` cmdlets (`Get-DomainUser`, `Find-LocalAdminAccess`), you conduct covert LDAP queries that bypass noisy port scanning.
* **Connection to Part 5 (Privilege Escalation)**: `PowerUp.ps1` automates checking for unquoted service paths and weak service DACLs in a single memory invocation (`Invoke-AllChecks`).
* **Connection to Part 7 (Command & Control)**: In-memory download cradles ensure that C2 implants and staged beacons are fetched directly over HTTPS and executed without ever creating suspicious disk artifacts.""",
        "references": """## Categorized References & Authoritative Sources

### 1. Microsoft Architectural Documentation
* **Microsoft Learn: Antimalware Scan Interface (AMSI) Architecture**: [https://learn.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-portal](https://learn.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-portal).
* **Microsoft Learn: PowerShell Script Block Logging & Auditing**: [https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows).
* **Microsoft Learn: Constrained Language Mode (CLM) Specifications**.

### 2. Authoritative Offensive PowerShell Repositories
* **PowerSploit Offensive PowerShell Repository**: [https://github.com/PowerShellMafia/PowerSploit](https://github.com/PowerShellMafia/PowerSploit).
* **Invoke-Obfuscation by Daniel Bohannon**: PowerShell AST and token obfuscation framework. [https://github.com/danielbohannon/Invoke-Obfuscation](https://github.com/danielbohannon/Invoke-Obfuscation).
* **Rasta-Mouse AMSI Bypass Research**: *Memory Patching AmsiScanBuffer*. [https://rastamouse.me/](https://rastamouse.me/).

### 3. MITRE ATT&CK Enterprise Techniques
* **T1059.001**: Command and Scripting Interpreter: PowerShell. [https://attack.mitre.org/techniques/T1059/001/](https://attack.mitre.org/techniques/T1059/001/).
* **T1562.001**: Impair Defenses: Disable or Modify Tools (AMSI Bypass). [https://attack.mitre.org/techniques/T1562/001/](https://attack.mitre.org/techniques/T1562/001/).
* **T1027**: Obfuscated/Encrypted Payloads. [https://attack.mitre.org/techniques/T1027/](https://attack.mitre.org/techniques/T1027/)."""
    }
]

def enrich_post(p):
    path = p["filename"]
    if not os.path.exists(path):
        print(f"Error: file not found: {path}")
        return
        
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace the References section with the expanded categorized references
    ref_marker = "## References & Further Reading"
    if ref_marker in content:
        parts = content.split(ref_marker)
        body_before_refs = parts[0].rstrip()
    else:
        body_before_refs = content.rstrip()

    # 2. Append the visual diagram section, attack chain section, and expanded references
    author_footer = "\n\n---\n\n*Author: Abdulrahman M. Fathi (0x3bdo) • Cyber Security Engineer & Penetration Tester*\n"
    
    # Strip any trailing author signature from body_before_refs
    body_before_refs = re.sub(r'---\s*\n*\*Author:.*?\*', '', body_before_refs).rstrip()
    
    enriched_content = (
        f"{body_before_refs}\n\n---\n\n"
        f"{p['diagram_section']}\n\n---\n\n"
        f"{p['attack_chain']}\n\n---\n\n"
        f"{p['references']}"
        f"{author_footer}"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(enriched_content)

    print(f"Successfully enriched: {path}")

if __name__ == "__main__":
    for p in posts_data:
        enrich_post(p)
    print("\nAll 10 eCPPT posts have been enriched with diagrams, attack chain connections, and extensive references!")
