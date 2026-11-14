import os
import glob
import re

MODULE_META = {
    "getting-started": {
        "title": "Getting Started",
        "clean_name": "Getting Started",
        "tier": "Tier 0",
        "diff": "Fundamental",
        "cat": "Fundamental",
        "url": "https://academy.hackthebox.com/module/77",
        "core_topic": "penetration testing fundamentals, network reconnaissance with Nmap, public-facing CMS vulnerability exploitation (Nibblesblog), Metasploit fundamentals, and privilege escalation on both Linux and Windows systems",
        "takeaways": [
            "**Structured Assessment Lifecycle**: Follows the industry-standard penetration testing phases: reconnaissance, scanning, vulnerability identification, exploitation, post-exploitation, and structured reporting.",
            "**Nmap Network Discovery**: Leverages TCP SYN scans (`-sS`), default scripts (`-sC`), and version detection (`-sV`) to uncover open services and attack surfaces without crashing target daemons.",
            "**Web Application Exploitation**: Identifies exposed management interfaces and executes arbitrary PHP file uploads via vulnerable plugins (Nibblesblog CVE-2015-6967) to establish reverse shell access.",
            "**Privilege Escalation Fundamentals**: Inspects user sudo privileges (`sudo -l`) and abuses writeable shell scripts executed as root to escalate from `nibbler` to `root`.",
            "**Lab Flag Verification**: Provides verified terminal commands, interactive bash prompts, and complete flag extractions across all sections."
        ],
        "exec_summary": """The **Getting Started** module serves as the operational baseline for the entire Hack The Box CPTS curriculum. The engagement begins with target host reconnaissance using Nmap, cataloging active network ports (HTTP port 80 and SSH port 22) and analyzing exposed application banners.

Upon fingerprinting the target web server, we discover a Nibbles blogging platform instance. By navigating administrative directories, analyzing source comments, and performing credential verification, we gain access to the administrative panel. Exploitation is achieved by abusing unrestricted image upload functionality to execute a PHP web shell, establishing initial access as the `nibbler` user. Post-exploitation inspection of `sudo -l` reveals write permissions to `/home/nibbler/personal/stuff/monitor.sh`, which is leveraged to achieve full root privileges and capture all assessment flags."""
    },
    "file-transfers": {
        "title": "File Transfers",
        "clean_name": "File Transfers",
        "tier": "Tier 0",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/24",
        "core_topic": "cross-platform file transfer tradecraft, living-off-the-land ingress/egress mechanisms, PowerShell download cradles, SMB/WebDAV shares, and payload staging across Linux and Windows environments",
        "takeaways": [
            "**Windows Ingress Primitives**: Employs PowerShell WebClient cradles (`DownloadFile`, `DownloadString`), `Invoke-WebRequest`, `certutil.exe -urlcache`, and BITSAdmin to stage payloads on hardened hosts.",
            "**Linux Ingress Primitives**: Utilizes native command-line tools including `curl`, `wget`, Python `urllib`, Netcat pipes, and Bash `/dev/tcp` file redirections.",
            "**Encrypted & Obfuscated Egress**: Exfiltrates sensitive host data (SAM hives, shadow hashes, SSH keys) using Base64 string encoding over DNS, HTTP POST requests, and WebDAV tunnels.",
            "**Air-Gapped & Restricted Bypass**: Implements multi-stage file transfers through intermediate jump hosts using Netcat relays, SSH tunnels, and Base64 clipboard pasting.",
            "**Detection Evasion Considerations**: Avoids writing binaries directly to disk by executing memory-resident scripts via `IEX (New-Object Net.WebClient).DownloadString()`."
        ],
        "exec_summary": """File transfer tradecraft is an essential core capability in offensive operations, bridging the gap between initial code execution and full operational capability. In hardened enterprise environments, security controls such as AppLocker, restricted outbound firewall rules, and endpoint detection agents severely restrict arbitrary binary downloads.

This module deconstructs cross-platform file delivery techniques across Windows and Linux targets. We examine living-off-the-land (LOL) utilities native to the operating system, fileless memory execution cradles, non-interactive shell transfer strategies, and techniques for bypassing strict perimeter inspection. Every exercise is accompanied by verified command executions and flag validations."""
    },
    "information-gathering-web-edition": {
        "title": "Information Gathering - Web Edition",
        "clean_name": "Information Gathering (Web Edition)",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "General",
        "url": "https://academy.hackthebox.com/module/144",
        "core_topic": "passive and active web reconnaissance, domain footprinting, DNS record analysis, virtual host (vhost) discovery, and search engine open-source intelligence (OSINT)",
        "takeaways": [
            "**Passive OSINT Tradecraft**: Leverages public databases, Certificate Transparency (crt.sh) logs, WHOIS registries, and search engine dorking without transmitting direct packets to the target.",
            "**DNS Infrastructure Enumeration**: Maps target nameservers, MX records, TXT verification strings, and tests for misconfigured DNS Zone Transfers (`dig axfr`).",
            "**Subdomain & VHost Discovery**: Utilizes dictionary-based tools and HTTP Host header fuzzing to identify hidden development environments, staging portals, and internal administrative APIs.",
            "**Web Technology Fingerprinting**: Dissects HTTP response headers, cookies, favicon hashes, and DOM framework signatures using Wappalyzer and Curl.",
            "**Data Correlation**: Aggregates disparate reconnaissance data into an actionable adversary attack tree before launching active exploitation."
        ],
        "exec_summary": """Reconnaissance dictates the success of every penetration testing engagement. High-profile web applications frequently protect their primary domain with sophisticated Web Application Firewalls (WAF) and Content Delivery Networks (CDN), while internal staging environments and forgotten subdomains remain completely unhardened.

In this module, we conduct comprehensive external reconnaissance against target domains. We analyze passive certificate transparency logs, perform active DNS sweeps, enumerate virtual hosts sharing the same IP infrastructure, and extract hidden endpoints, successfully recovering all flags across every assessment objective."""
    },
    "footprinting": {
        "title": "Footprinting External Infrastructure & Services",
        "clean_name": "Footprinting",
        "tier": "Tier I",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/112",
        "core_topic": "systematic enumeration of enterprise network daemons including FTP, SMB, NFS, DNS, SMTP, IMAP, SNMP, MySQL, MSSQL, Oracle TNS, and IPMI",
        "takeaways": [
            "**Protocol-Level Interrogation**: Probes default daemon behaviors, banner strings, and authentication states across standard enterprise TCP and UDP service ports.",
            "**Anonymous Access Exploitation**: Identifies and extracts sensitive configuration files and backups from unauthenticated SMB shares, anonymous FTP trees, and NFS exports.",
            "**Service-Specific Tooling**: Commands specialized enumeration utilities including `smbclient`, `rpcclient`, `enum4linux-ng`, `showmount`, `snmpwalk`, and `mysql`.",
            "**Network Infrastructure Mapping**: Interrogates SNMP MIB trees and IPMI Baseboard Management Controllers (BMC) to harvest hardware configurations and user credentials.",
            "**Actionable Intelligence Synthesis**: Transforms raw service banners and user listings into actionable exploit paths for subsequent attack phases."
        ],
        "exec_summary": """Footprinting is the systematic gathering of technical specifications from exposed network services. By interrogating daemons using native protocol commands, penetration testers uncover misconfigurations, unpatched service releases, and unauthenticated administrative interfaces that bypass perimeter security controls.

This comprehensive module covers the enumeration of core enterprise infrastructure protocols: SMB shares, RPC endpoints, NFS directory trees, DNS resolvers, SMTP mail relays, database engines (MySQL, MSSQL, Oracle), and remote management controllers. Each protocol is examined through practical terminal sessions with complete flag verifications."""
    },
    "linux-privilege-escalation": {
        "title": "Linux Privilege Escalation",
        "clean_name": "Linux Privilege Escalation",
        "tier": "Tier II",
        "diff": "Easy",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/51",
        "core_topic": "local Linux privilege escalation tradecraft, SUID/SGID binary exploitation, Linux capabilities, cron job hijacking, vulnerable system services, Docker container escapes, and kernel exploitation",
        "takeaways": [
            "**SUID/SGID Abuse**: Scans the filesystem for binaries with setuid permissions and cross-references them against GTFOBins to spawn root shells.",
            "**Linux Capabilities Exploitation**: Inspects process capabilities (`getcap -r /`) and weaponizes `cap_setuid` to elevate permissions without traditional SUID flags.",
            "**Cron & Timer Hijacking**: Exploits unquoted paths, writeable scripts, and wildcard expansions in automated cron tasks executed by UID 0.",
            "**Environment Variable Hijacking**: Manipulates `LD_PRELOAD`, `LD_LIBRARY_PATH`, and `PATH` variable resolution within sudoer execution blocks.",
            "**Container & Kernel Exploitation**: Identifies container breakouts via writeable Docker sockets (`/var/run/docker.sock`) and analyzes CVE exploits such as PwnKit and Dirty Pipe."
        ],
        "exec_summary": """Attaining initial shell access on a Linux server typically grants privileges restricted to unprivileged service accounts (`www-data`, `nobody`). Transforming this foothold into unrestricted root access requires a methodical audit of host configurations, system binaries, scheduled tasks, and the kernel boundary.

This module delivers a battle-tested playbook for Linux local privilege escalation. We analyze automated enumeration scripts (LinPEAS), dissect manual inspection commands, exploit file permissions, abuse sudo rules, and escape virtualized containers, validating every exercise with full flag captures."""
    },
    "login-brute-forcing": {
        "title": "Login Brute Forcing",
        "clean_name": "Login Brute Forcing",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/57",
        "core_topic": "automated credential guessing, password spraying, dictionary attacks, and authentication bypasses against SSH, FTP, RDP, and HTTP POST login interfaces",
        "takeaways": [
            "**Attack Methodology Selection**: Differentiates between horizontal password spraying (one password across many accounts) and vertical brute-forcing (many passwords against one account).",
            "**High-Performance Cracking Tools**: Leverages `hydra`, `medusa`, `ncrack`, and custom Python scripts to optimize connection concurrency and throughput.",
            "**HTTP Form Interception**: Inspects authentication request payloads, identifies dynamic anti-CSRF tokens, and crafts customized parameter dictionaries.",
            "**Lockout Avoidance Strategies**: Tunes thread counts, request delays, and user-agent rotations to operate beneath defensive detection thresholds.",
            "**Flag Extraction Automation**: Captures and validates user credentials to unlock administrative access across all module challenges."
        ],
        "exec_summary": """Weak and reused passwords remain the single most pervasive vulnerability across enterprise IT environments. When systems lack account lockout policies or multi-factor authentication, automated credential attacks provide an immediate pathway to valid access.

In this module, we dissect login brute-forcing and password spraying tradecraft across network services (SSH, FTP, SMB) and web authentication forms. We configure request parameters, inspect failure condition responses, tune operational concurrency, and extract all module flags."""
    },
    "broken-authentication": {
        "title": "Broken Authentication",
        "clean_name": "Broken Authentication",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/135",
        "core_topic": "web authentication flaws, session fixation, credential stuffing, insecure password reset flows, 2FA bypasses, and JSON Web Token (JWT) signature vulnerabilities",
        "takeaways": [
            "**Authentication Logic Flaws**: Identifies structural logic flaws in multi-step authentication processes and password reset mechanisms.",
            "**Session Fixation & Hijacking**: Exploits applications that fail to regenerate session IDs upon user authentication.",
            "**JWT Vulnerability Exploitation**: Tampers with JSON Web Tokens by modifying algorithms (`none` alg), abusing weak HMAC secrets, and manipulating claims.",
            "**Two-Factor Authentication (2FA) Bypasses**: Exploits missing rate limiting on verification codes, response manipulation, and direct endpoint access.",
            "**Defensive Hardening Standards**: Maps identified flaws against OWASP ASVS guidelines to implement cryptographically secure authentication architectures."
        ],
        "exec_summary": """Authentication mechanisms verify identity and grant access to protected application resources. When authentication logic is improperly designed or implemented, attackers can bypass login controls, impersonate privileged users, and compromise backend systems without valid credentials.

This module explores web application authentication vulnerabilities in detail. We examine insecure direct password reset endpoints, brute-force short OTP codes, tamper with JSON Web Tokens, and bypass multi-factor authentication controls, providing complete exploit walkthroughs and verified flag solutions."""
    },
    "command-injections": {
        "title": "Command Injections",
        "clean_name": "Command Injections",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/109",
        "core_topic": "OS command injection vulnerabilities, filter evasion, special character bypasses, blind injection techniques (time-based & out-of-band), and reverse shell weaponization",
        "takeaways": [
            "**Injection Operators**: Masterfully weaponizes command separators: semicolons (`;`), pipes (`|`), ampersands (`&`), AND operators (`&&`), and subshell syntax (`$()`, `` ` ``).",
            "**WAF & Blacklist Evasion**: Bypasses string and whitespace filters using internal environment variables (`$IFS`), string concatenation, wildcard expansions, and Base64 decoding.",
            "**Blind Command Injection**: Dissects systems that suppress command output by leveraging time delays (`sleep`) and Out-of-Band (OOB) DNS/HTTP exfiltration.",
            "**Interactive Shell Spawning**: Converts single-line command injection flaws into fully interactive, encrypted reverse shell sessions.",
            "**Secure Coding Standards**: Replaces insecure system execution functions (`system()`, `exec()`, `passthru()`) with parameterized process execution APIs."
        ],
        "exec_summary": """Operating System Command Injection occurs when an application passes unvalidated user input directly to a system shell interpreter. This flaw grants attackers the ability to execute arbitrary OS commands under the security context of the web server process.

In this module, we conduct an exhaustive technical study of command injection vectors. We analyze input sanitization filters, craft multi-stage character evasion payloads, validate blind execution using time-based techniques, and establish stable reverse shells to capture all lab flags."""
    },
    "file-inclusion": {
        "title": "File Inclusion",
        "clean_name": "File Inclusion",
        "tier": "Tier I",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/23",
        "core_topic": "Local File Inclusion (LFI), Remote File Inclusion (RFI), directory traversal filters, PHP wrappers (filter, input, data), and log poisoning to achieve Remote Code Execution (RCE)",
        "takeaways": [
            "**Path Traversal Tradecraft**: Bypasses prefix/suffix path concatenation using relative traversal sequences (`../`, `..%2f`), absolute paths, and null-byte termination.",
            "**PHP Stream Wrappers**: Exploits `php://filter` for base64 source code extraction, `php://input` for direct payload execution, and `data://` wrappers.",
            "**Log Poisoning to RCE**: Injects PHP payloads into Apache/Nginx access logs, SSH auth logs, or mail logs and executes them via LFI inclusion.",
            "**Session File Poisoning**: Manipulates PHP session data (`/var/lib/php/sessions/sess_*`) to achieve reliable code execution.",
            "**RFI Exploitation Chains**: Leverages external HTTP/FTP servers to force remote file loading when `allow_url_include` is enabled."
        ],
        "exec_summary": """File Inclusion vulnerabilities arise when web applications dynamically include local or remote files without validating user-supplied path parameters. Local File Inclusion (LFI) exposes critical server files, while Remote File Inclusion (RFI) enables direct arbitrary code execution.

This module provides a comprehensive technical walkthrough of file inclusion mechanics. We analyze path traversal filters, weaponize PHP stream wrappers for source code disclosure, execute log poisoning attacks, and achieve full remote code execution to extract every flag."""
    },
    "attacking-common-services": {
        "title": "Attacking Common Services",
        "clean_name": "Attacking Common Services",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/116",
        "core_topic": "exploiting common network infrastructure services including SMB, FTP, SSH, RDP, MySQL, MSSQL, Oracle TNS, and DNS",
        "takeaways": [
            "**SMB Exploitation**: Harvests sensitive documents, writes payloads to accessible shares, and executes remote commands via PsExec and Impacket.",
            "**Database Attacks**: Interrogates MySQL and MSSQL servers, abuses `xp_cmdshell` for command execution, and extracts password hashes.",
            "**Remote Management Vectors**: Bypasses SSH key restrictions, audits RDP security levels, and captures NTLM authentication handshakes.",
            "**Protocol Misconfigurations**: Exploits anonymous FTP uploads, DNS zone transfers, and exposed Oracle TNS listener procedures.",
            "**Privilege Escalation Paths**: Converts compromised service accounts into full operating system administrative access."
        ],
        "exec_summary": """Enterprise networks rely on a suite of common infrastructure services for file sharing, database storage, and remote administration. When these daemons are improperly configured, vulnerable to credential reuse, or running unpatched software versions, they represent prime targets for initial compromise and lateral movement.

This module deconstructs offensive techniques targeting SMB, FTP, SSH, RDP, MySQL, and MSSQL. We walk through credential attacks, command execution primitives, share manipulation, and database exploitation, validating every exercise with complete flag solutions."""
    },
    "attacking-common-applications": {
        "title": "Attacking Common Applications",
        "clean_name": "Attacking Common Applications",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/113",
        "core_topic": "exploiting ubiquitous enterprise applications including Apache Tomcat, Jenkins, Splunk, Drupal, Joomla, and WordPress",
        "takeaways": [
            "**Application Profiling**: Identifies deployed web application packages, plugins, themes, and framework versions through fingerprinting.",
            "**Tomcat Manager Exploitation**: Authenticates with default or brute-forced credentials and uploads malicious WAR packages to achieve RCE.",
            "**Jenkins Script Console Abuse**: Leverages administrative Groovy script consoles to execute OS commands under the Jenkins daemon context.",
            "**CMS Exploitation**: Weaponizes known CVEs in Drupal (Drupalgeddon), WordPress, and Joomla to achieve arbitrary file uploads.",
            "**Credential Harvesting**: Dissects application configuration files, database connections, and encrypted keystores to uncover enterprise credentials."
        ],
        "exec_summary": """Modern organizations deploy a diverse array of off-the-shelf and open-source applications to manage builds, monitor infrastructure, and deliver web content. These applications often possess extensive administrative capabilities and run with elevated system privileges.

In this module, we examine offensive tradecraft targeting common enterprise applications: Apache Tomcat, Jenkins automation servers, Splunk enterprise monitors, and content management systems. We exploit management interfaces, deploy malicious packages, execute server-side code, and capture all assessment flags."""
    },
    "active-directory-enumeration-and-attacks": {
        "title": "Active Directory Enumeration & Attacks",
        "clean_name": "Active Directory Enumeration & Attacks",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/143",
        "core_topic": "Active Directory architecture, LDAP enumeration, BloodHound graph analysis, Kerberoasting, AS-REP Roasting, DCSync, and domain privilege escalation",
        "takeaways": [
            "**Domain Discovery**: Queries Active Directory domain objects, trusts, group policies, and access control lists (ACLs) using PowerView and BloodHound.",
            "**Kerberos Ticket Attacks**: Weaponizes Kerberoasting against service accounts with Service Principal Names (SPNs) and AS-REP Roasting against pre-authentication disabled accounts.",
            "**Credential Dumping**: Extracts NTDS.dit hashes via DCSync (`secretsdump.py`), dumps LSASS memory, and parses SAM registry hives.",
            "**ACL & Permission Abuse**: Hijacks user accounts and security groups through `GenericAll`, `WriteDacl`, and `ForceChangePassword` rights.",
            "**Domain Dominance**: Establishes persistence and complete forest compromise through Golden and Silver Ticket forge attacks."
        ],
        "exec_summary": """Active Directory (AD) is the identity and access management backbone of enterprise corporate networks. Mastering AD enumeration and attack paths is the cornerstone of advanced penetration testing and red teaming.

This extensive module provides a deep technical exploration of Active Directory exploitation. We map domain attack paths using BloodHound, extract and crack Kerberos service tickets, abuse misconfigured object permissions, execute DCSync replication attacks, and achieve full Domain Admin dominance, accompanied by verified terminal outputs and flag solutions."""
    },
    "attacking-enterprise-networks": {
        "title": "Attacking Enterprise Networks",
        "clean_name": "Attacking Enterprise Networks",
        "tier": "Tier III",
        "diff": "Hard",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/164",
        "core_topic": "multi-tiered enterprise network penetration testing, lateral movement, pivoting across segmented VLANs, defense evasion, and full-scope adversary simulation",
        "takeaways": [
            "**Network Segmentation Traversal**: Navigates complex internal network boundaries, firewalls, and isolated DMZ subnets using proxy chains and reverse tunnels.",
            "**Lateral Movement Tradecraft**: Moves horizontally across Windows and Linux domains using WinRM, WMI, SSH, and Pass-the-Hash protocols.",
            "**Host Enumeration & Situational Awareness**: Audits compromised endpoints for sensitive documentation, cached credentials, and network routing tables.",
            "**Adversary Infrastructure Staging**: Deploys scalable multi-hop command and control architectures to maintain persistent internal access.",
            "**Engagement Synthesis**: Correlates multi-host vulnerabilities into comprehensive attack chains that compromise enterprise business objectives."
        ],
        "exec_summary": """Enterprise penetration testing transcends isolated host exploitation, demanding the ability to navigate segmented networks, bypass defensive controls, and compromise multi-tier Active Directory forests.

In this advanced module, we execute a full-scale simulated enterprise assessment. We breach external perimeters, establish multi-hop pivots across restricted subnets, harvest domain credentials, exploit internal management servers, and compromise high-value enterprise targets, providing rigorous technical breakdowns and flag solutions for every exercise."""
    },
    "using-web-proxies": {
        "title": "Using Web Proxies",
        "clean_name": "Using Web Proxies",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "General",
        "url": "https://academy.hackthebox.com/module/110",
        "core_topic": "interception proxies, Burp Suite, OWASP ZAP, request manipulation, intruder fuzzing, repeater workflows, and proxy chaining",
        "takeaways": [
            "**Traffic Interception**: Routes web browser and application traffic through proxy listeners, managing SSL/TLS certificate installation and inspection.",
            "**Request Manipulation**: Intercepts, modifies, and replays HTTP/HTTPS requests and responses in real-time to analyze backend processing logic.",
            "**Automated Fuzzing**: Configures Burp Intruder and ZAP Fuzzer with custom payload positions, attack types (Sniper, Pitchfork), and match/replace rules.",
            "**Proxy Chaining & Upstream Routing**: Configures upstream SOCKS/HTTP proxies to route assessment traffic through internal pivots and anonymous gateways.",
            "**Automated Extension Integration**: Leverages BApp store extensions (Logger++, Turbo Intruder) to accelerate vulnerability discovery."
        ],
        "exec_summary": """Interception proxies are the foundational workbench of every web application penetration tester. By sitting between the client browser and the target server, proxies allow testers to inspect, manipulate, and automate every transaction in the HTTP protocol.

This module explores practical workflows using Burp Suite and OWASP ZAP. We master manual request tampering, automate high-throughput parameter fuzzing, configure proxy chaining, and analyze complex session states, successfully solving every challenge and flag."""
    },
    "vulnerability-assessment": {
        "title": "Vulnerability Assessment",
        "clean_name": "Vulnerability Assessment",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "General",
        "url": "https://academy.hackthebox.com/module/108",
        "core_topic": "systematic vulnerability discovery, automated scanner operations (Nessus, OpenVAS), CVSS scoring metrics, false-positive triage, and remediation prioritization",
        "takeaways": [
            "**Scanning Methodologies**: Configures credentialed and non-credentialed vulnerability scans across network subnets and application endpoints.",
            "**Vulnerability Scoring & Triage**: Analyzes CVSS v3.1 vector strings to accurately evaluate vulnerability severity, exploitability, and organizational impact.",
            "**False Positive Elimination**: Manually validates automated scanner findings through protocol-level verification before client reporting.",
            "**Asset Risk Prioritization**: Synthesizes vulnerability scan outputs into actionable risk matrices prioritizing externally exposed and critical assets.",
            "**Compliance & Patch Management**: Formulates defensive patching roadmaps aligned with enterprise risk frameworks."
        ],
        "exec_summary": """Vulnerability assessment is the systematic identification, evaluation, and ranking of security flaws across organizational assets. Unlike unstructured testing, formal assessments require structured methodologies to ensure broad coverage and actionable remediation guidance.

In this module, we examine vulnerability scanning architectures, configure automated scanners, analyze CVSS vulnerability vectors, filter scanner false positives through manual verification, and formulate prioritized remediation roadmaps, validating every assessment flag."""
    },
    "shells-and-payloads": {
        "title": "Shells & Payloads",
        "clean_name": "Shells & Payloads",
        "tier": "Tier I",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/115",
        "core_topic": "reverse shells, bind shells, web shells, MSFvenom payload generation, shell stabilization (TTY upgrading), and encrypted command-and-control channels",
        "takeaways": [
            "**Shell Architecture**: Distinguishes between reverse shells (target connects back to tester) and bind shells (target opens listening port for tester).",
            "**Payload Engineering**: Compiles customized payloads using `msfvenom` across multiple formats: ELF, EXE, ASPX, WAR, PHP, and raw shellcode.",
            "**Shell Stabilization & TTY Spawning**: Upgrades dumb netcat sessions into fully functional interactive TTY shells using Python `pty`, `stty raw -echo`, and Socat.",
            "**Encrypted Reverse Shells**: Establishes secure communication channels using OpenSSL certificates and Socat to evade network intrusion detection systems.",
            "**Egress Filtering Bypass**: Routes reverse shell connections over standard allowed outbound ports (TCP 80, 443, 53) to bypass egress firewalls."
        ],
        "exec_summary": """Gaining command execution is only the first step in host exploitation. Transforming raw execution primitives into stable, interactive, and encrypted shell sessions is essential for effective post-exploitation and privilege escalation.

This module provides a comprehensive technical study of shells and payloads. We examine reverse, bind, and web shells across Linux and Windows platforms, compile customized payloads with MSFvenom, master TTY terminal stabilization, and configure encrypted communication channels, solving all module flags."""
    },
    "sql-injection-fundamentals": {
        "title": "SQL Injection Fundamentals",
        "clean_name": "SQL Injection Fundamentals",
        "tier": "Tier I",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/33",
        "core_topic": "SQL injection mechanics, In-Band UNION-based SQLi, Error-based SQLi, Blind Boolean and Time-based SQLi, database schema enumeration, and data extraction",
        "takeaways": [
            "**SQLi Mechanics**: Explains how unsanitized user inputs break SQL query syntax to alter database execution logic.",
            "**UNION-Based Exploitation**: Determines column counts and data types via `ORDER BY` and extracts data across tables using `UNION SELECT`.",
            "**Database Schema Enumeration**: Queries `information_schema` to enumerate database names, table structures, and sensitive column definitions.",
            "**Blind SQL Injection**: Extracts data character-by-character using conditional boolean logic (`AND 1=1`) and time-delay functions (`SLEEP()`).",
            "**Administrative File Operations**: Reads sensitive operating system files (`LOAD_FILE()`) and writes web shells to disk (`INTO OUTFILE`)."
        ],
        "exec_summary": """SQL Injection (SQLi) remains one of the most devastating web vulnerabilities, allowing attackers to bypass authentication, extract entire databases, tamper with critical records, and achieve remote operating system command execution.

This module covers the core principles of SQL injection across multiple database management systems (MySQL, MSSQL, PostgreSQL). We analyze syntax breaking, weaponize UNION queries to dump database contents, execute blind time-based attacks, and leverage database file-writing primitives to compromise the host, validating every flag."""
    },
    "sqlmap-essentials": {
        "title": "SQLMap Essentials",
        "clean_name": "SQLMap Essentials",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/58",
        "core_topic": "automated SQL injection testing with SQLMap, tamper script evasion, database fingerprinting, schema dumping, and OS shell spawning",
        "takeaways": [
            "**Target Specification**: Feeds target URLs, HTTP request files (`-r`), and parameters directly into SQLMap for comprehensive testing.",
            "**Technique Tuning**: Customizes detection techniques: Boolean-based (`B`), Error-based (`E`), UNION query (`U`), Stacked queries (`S`), and Time-based (`T`).",
            "**Tamper Script Evasion**: Evades Web Application Firewalls (WAF) using built-in tamper scripts (`space2comment`, `charencode`, `randomcase`).",
            "**Automated Data Extraction**: Dumps specific databases, tables, and columns with high efficiency using multi-threading (`--threads`).",
            "**Operating System Takeover**: Spawns interactive system shells via `--os-shell` and `--os-cmd` when database administrative rights are present."
        ],
        "exec_summary": """SQLMap is the industry-standard automated penetration testing tool for detecting and exploiting SQL injection flaws. While manual testing is crucial for understanding, SQLMap provides the speed and efficiency required to thoroughly audit complex applications.

In this module, we master SQLMap operations. We analyze request files captured from interception proxies, tune injection boundaries, apply tamper scripts to bypass defensive filters, dump sensitive database schemas, and escalate to operating system shells, completing all lab objectives."""
    },
    "password-attacks": {
        "title": "Password Attacks",
        "clean_name": "Password Attacks",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/147",
        "core_topic": "offline password cracking, hash identification, John the Ripper, Hashcat, Windows credential dumping (SAM, LSASS), and Linux shadow parsing",
        "takeaways": [
            "**Hash Identification**: Fingerprints cryptographic hash algorithms (MD5, SHA-256, NTLM, Kerberos, bcrypt) using `hashid` and `hash-identifier`.",
            "**Offline Cracking with Hashcat**: Weaponizes GPU acceleration across attack modes: dictionary (`-a 0`), combinator (`-a 1`), mask (`-a 3`), and rule-based.",
            "**John the Ripper Operations**: Converts encrypted formats (ZIP, KeePass, SSH keys, PDF) into crackable hashes using `*2john` utilities.",
            "**Windows Credential Extraction**: Dumps local SAM database hashes, parses LSASS memory handles, and extracts DPAPI secrets.",
            "**Custom Wordlist Generation**: Generates targeted wordlists based on target OSINT using `cewl` and rule-based permutations."
        ],
        "exec_summary": """Capturing password hashes is common during penetration testing, but transforming those cryptographic digests into plaintext credentials requires structured offline cracking tradecraft.

This module deconstructs password cracking methodologies and tooling. We examine hash formats, optimize GPU cracking workflows with Hashcat, leverage John the Ripper for specialty archives, extract Windows SAM and LSASS credentials, and crack protected hashes to obtain all assessment flags."""
    },
    "server-side-attacks": {
        "title": "Server-side Attacks",
        "clean_name": "Server-side Attacks",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/145",
        "core_topic": "Server-Side Request Forgery (SSRF), XML External Entity (XXE) injection, Server-Side Template Injection (SSTI), and cloud metadata exploitation",
        "takeaways": [
            "**SSRF Mechanics**: Forces web servers to issue unauthorized HTTP requests to internal network resources, loopback interfaces (`127.0.0.1`), and cloud metadata APIs.",
            "**Cloud Metadata Extraction**: Targets AWS, Azure, and GCP metadata endpoints (`169.254.169.254`) to harvest IAM credentials and temporary API tokens.",
            "**XXE Injection**: Manipulates XML parser DTD definitions to achieve local file disclosure, internal service scanning, and blind out-of-band data exfiltration.",
            "**SSTI to RCE**: Identifies vulnerable template engines (Jinja2, Twig, Freemarker) and escapes sandboxes to achieve operating system command execution.",
            "**Secure Architecture Controls**: Disables XML external entity parsing and implements network-level egress filtering to neutralize SSRF."
        ],
        "exec_summary": """Server-side vulnerabilities target backend application logic, parsers, and internal communication channels. Flaws such as SSRF, XXE, and SSTI frequently bypass perimeter firewalls and expose internal microservices to remote attackers.

In this module, we conduct an in-depth technical analysis of server-side attack vectors. We exploit SSRF to access internal administration portals, weaponize XXE to disclose sensitive server files, escape template engine sandboxes via SSTI for full RCE, and extract all lab flags."""
    },
    "windows-privilege-escalation": {
        "title": "Windows Privilege Escalation",
        "clean_name": "Windows Privilege Escalation",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/67",
        "core_topic": "local Windows privilege escalation, service misconfigurations, unquoted service paths, weak permissions, token manipulation (Potato exploits), UAC bypasses, and registry hijacks",
        "takeaways": [
            "**Service Misconfiguration Abuse**: Exploits unquoted service paths, insecure service binary permissions, and weak service configurations (`sc.exe config`).",
            "**Token Privileges & Potato Exploits**: Weaponizes `SeImpersonatePrivilege` and `SeAssignPrimaryToken` using RoguePotato, PrintSpoofer, and GodPotato.",
            "**User Account Control (UAC) Bypasses**: Identifies auto-elevating Windows binaries and hijacks registry keys (`hkcu\\software\\classes`) to bypass UAC prompts.",
            "**DLL Hijacking**: Injects malicious DLLs into search paths of elevated executables missing standard library dependencies.",
            "**AlwaysInstallElevated & Credential Harvesting**: Exploits MSI installer registry flags and extracts stored credentials from unattended installation scripts."
        ],
        "exec_summary": """Gaining a low-privileged shell on a Windows system is only the starting point. Achieving complete host control requires escalating privileges to `NT AUTHORITY\\SYSTEM` or local administrator by auditing host misconfigurations, service permissions, and kernel tokens.

This module provides a battle-tested roadmap for Windows local privilege escalation. We analyze automated tools (WinPEAS, Seatbelt), manually inspect service permissions, execute potato token impersonation attacks, bypass UAC controls, and secure full system control, validating every flag."""
    },
    "pivoting-tunneling-and-port-forwarding": {
        "title": "Pivoting, Tunneling & Port Forwarding",
        "clean_name": "Pivoting, Tunneling, and Port Forwarding",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/158",
        "core_topic": "network pivoting, dynamic port forwarding, SSH tunneling (local & remote), SOCKS proxies, Chisel, Ligolo-ng, and multi-hop routing",
        "takeaways": [
            "**Pivoting Concepts**: Routes offensive traffic through compromised dual-homed hosts to reach isolated internal subnets.",
            "**SSH Port Forwarding**: Masters local port forwarding (`-L`), remote reverse forwarding (`-R`), and dynamic SOCKS proxies (`-D`).",
            "**Modern Tunneling Tools**: Deploys lightweight tunneling binaries such as `chisel` and `ligolo-ng` to establish high-performance reverse tunnels.",
            "**ProxyChains Configuration**: Configures `/etc/proxychains4.conf` to seamlessly route Nmap, Metasploit, and custom scripts through multi-hop SOCKS proxies.",
            "**Windows Native Port Forwarding**: Uses `netsh interface portproxy` to redirect network traffic on compromised Windows endpoints without third-party tools."
        ],
        "exec_summary": """In modern enterprise environments, critical servers and database systems reside in isolated internal subnets that are completely unreachable from the internet. Penetration testers must pivot through compromised boundary systems to interact with these internal targets.

This module delivers a comprehensive guide to network pivoting and tunneling tradecraft. We explore SSH tunnels, configure dynamic SOCKS proxies with Proxychains, deploy Chisel and Ligolo-ng for reverse tunneling, and route traffic across multi-tiered corporate networks to capture all flags."""
    },
    "api-attacks": {
        "title": "API Attacks",
        "clean_name": "API Attacks",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/160",
        "core_topic": "REST and GraphQL API security, Broken Object Level Authorization (BOLA/IDOR), excessive data exposure, mass assignment, and API token manipulation",
        "takeaways": [
            "**API Endpoint Discovery**: Discovers undocumented API versions, staging endpoints, and Swagger/OpenAPI documentation files.",
            "**Broken Object Level Authorization (BOLA)**: Manipulates object identifiers in API requests to access and modify unauthorized user records.",
            "**Mass Assignment Vulnerabilities**: Injects privileged parameters (e.g., `is_admin: true`, `role: administrator`) during account updates.",
            "**GraphQL Introspection & Abuse**: Discloses entire database schemas by querying GraphQL introspection endpoints and bypassing query depth limits.",
            "**Rate Limiting & Token Flaws**: Exploits missing rate limits on sensitive endpoints and tampers with API authorization tokens."
        ],
        "exec_summary": """Application Programming Interfaces (APIs) represent the primary communication layer for modern web and mobile applications. APIs frequently expose broad business logic and direct database records, making them high-value targets when authorization controls are neglected.

In this module, we conduct comprehensive testing of REST and GraphQL APIs. We analyze the OWASP API Security Top 10, exploit BOLA/IDOR vulnerabilities, extract hidden schemas via GraphQL introspection, execute mass assignment attacks, and capture all assessment flags."""
    },
    "introduction-to-penetration-testing": {
        "title": "Introduction to Penetration Testing",
        "clean_name": "Introduction to Penetration Testing",
        "tier": "Tier 0",
        "diff": "Fundamental",
        "cat": "Fundamental",
        "url": "https://academy.hackthebox.com/module/90",
        "core_topic": "penetration testing methodologies, ethics, legal frameworks, Rules of Engagement (RoE), vulnerability management, and technical reporting",
        "takeaways": [
            "**Professional Standards**: Follows recognized industry frameworks including PTES, NIST SP 800-115, and OSSTMM.",
            "**Engagement Scoping**: Defines Rules of Engagement (RoE), testing boundaries, communication protocols, and emergency procedures.",
            "**Vulnerability Lifecycle**: Tracks vulnerabilities from discovery and validation through risk assessment and verified remediation.",
            "**Technical Documentation**: Structures professional penetration testing reports containing executive summaries, risk matrices, and reproducible steps.",
            "**Ethics & Legal Compliance**: Adheres to strict legal boundaries and responsible disclosure practices."
        ],
        "exec_summary": """Professional penetration testing is a structured, authorized, and ethical assessment of organizational security posture. Beyond technical exploitation skills, professionals must master legal scoping, ethical frameworks, risk communication, and technical report writing.

This module establishes the foundational principles of professional penetration testing. We study testing methodologies, formulate rules of engagement, analyze risk scoring frameworks, and examine the lifecycle of technical assessments, solving all curriculum challenges."""
    },
    "network-enumeration-with-nmap": {
        "title": "Network Enumeration with Nmap",
        "clean_name": "Network Enumeration with Nmap",
        "tier": "Tier I",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/19",
        "core_topic": "advanced Nmap scanning techniques, host discovery, TCP/UDP port scans, service fingerprinting, Nmap Scripting Engine (NSE), and firewall evasion",
        "takeaways": [
            "**Scan Type Mechanics**: Analyzes packet-level differences between TCP SYN (`-sS`), TCP Connect (`-sT`), UDP (`-sU`), and FIN/Null/Xmas scans.",
            "**Host Discovery Optimization**: Conducts fast network sweeps using ICMP echo (`-PE`), timestamp (`-PP`), and TCP SYN/ACK ping probes (`-PS`, `-PA`).",
            "**Nmap Scripting Engine (NSE)**: Deploys specialized Lua scripts across categories (`vuln`, `auth`, `default`, `safe`) for automated vulnerability discovery.",
            "**Firewall & IDS Evasion**: Bypasses network inspection using packet fragmentation (`-f`), decoy addresses (`-D`), source port manipulation (`--source-port 53`), and data padding.",
            "**Performance Tuning**: Optimizes scanning speed and accuracy using timing templates (`-T0` through `-T5`) and min-rate parameters."
        ],
        "exec_summary": """Nmap (Network Mapper) is the quintessential network discovery and vulnerability scanning tool used by security professionals worldwide. Efficient network enumeration requires an intimate understanding of low-level TCP/IP packet interactions and firewall filtering behaviors.

This module provides an exhaustive deep-dive into Nmap. We analyze packet captures of various scan types, deploy advanced NSE scripts to uncover vulnerabilities, bypass defensive firewall filters, optimize timing parameters, and extract all lab flags."""
    },
    "attacking-web-applications-with-ffuf": {
        "title": "Attacking Web Applications with Ffuf",
        "clean_name": "Attacking Web Applications with Ffuf",
        "tier": "Tier I",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/54",
        "core_topic": "high-performance web fuzzing with ffuf, directory discovery, page fuzzing, parameter fuzzing (GET & POST), virtual host enumeration, and advanced filtering",
        "takeaways": [
            "**High-Speed Fuzzing**: Harnesses Go-based multi-threaded fuzzing with `ffuf` to process tens of thousands of requests per minute.",
            "**Directory & Extension Fuzzing**: Uncovers hidden web directories, backup files (`.bak`, `.old`), and scripts using targeted SecLists wordlists.",
            "**Parameter Discovery**: Identifies hidden GET and POST parameters that trigger undocumented backend functionality or vulnerabilities.",
            "**Virtual Host (VHost) Enumeration**: Fuzzes HTTP `Host` headers to identify internal subdomains and unlinked administrative sites.",
            "**Advanced Filter Tuning**: Filters out false positives by calibrating HTTP status codes (`-fc`), response sizes (`-fs`), and word counts (`-fw`)."
        ],
        "exec_summary": """Web application fuzzing is the automated testing of input spaces and endpoints to discover hidden administrative portals, backup files, undocumented parameters, and virtual hosts that are not linked in public HTML pages.

In this module, we master the operation of `ffuf`. We learn how to structure high-throughput fuzzing commands, apply precision response filtering to eliminate false positives, discover hidden endpoints and VHosts, and solve every assessment flag."""
    },
    "hacking-wordpress": {
        "title": "Hacking WordPress",
        "clean_name": "Hacking WordPress",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/17",
        "core_topic": "WordPress architecture, user enumeration, WPScan operations, vulnerable plugin/theme exploitation, credential attacks, and achieving RCE via theme modification",
        "takeaways": [
            "**WordPress Architecture**: Analyzes core directories (`wp-admin`, `wp-content`, `wp-includes`) and critical files (`wp-config.php`).",
            "**Reconnaissance & Enumeration**: Identifies WordPress core versions, installed plugins, active themes, and user accounts via WPScan and REST API endpoints.",
            "**Vulnerable Plugin Exploitation**: Weaponizes known CVEs in outdated plugins to achieve arbitrary file uploads, SQL injection, and authentication bypasses.",
            "**Theme Modification to RCE**: Injects PHP reverse shells into theme template files (e.g., `404.php`, `header.php`) through the administrative theme editor.",
            "**Credential Harvesting**: Dissects `wp-config.php` to extract MySQL database credentials and cryptographic security salts."
        ],
        "exec_summary": """Powering over 40% of the world's websites, WordPress is the most widely deployed Content Management System (CMS) on the internet. While core WordPress code is actively maintained, third-party plugins and themes frequently introduce critical vulnerabilities.

This module explores the complete WordPress attack lifecycle. We perform detailed user and plugin enumeration, execute dictionary attacks against `wp-login.php`, weaponize vulnerable plugin exploits, modify theme templates to execute reverse shells, and extract all module flags."""
    },
    "cross-site-scripting-xss": {
        "title": "Cross-Site Scripting (XSS)",
        "clean_name": "Cross-Site Scripting (XSS)",
        "tier": "Tier I",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/103",
        "core_topic": "Reflected XSS, Stored XSS, DOM-based XSS, JavaScript payload execution, session hijacking, cookie exfiltration, and filter bypass techniques",
        "takeaways": [
            "**XSS Types**: Differentiates between Reflected (non-persistent), Stored (persistent database injection), and DOM-based client-side execution.",
            "**Payload Construction**: Crafts functional JavaScript payloads to steal session cookies, capture keystrokes, and forge administrative requests.",
            "**Filter Evasion Tradecraft**: Bypasses input validation and WAF blacklists using mixed-case tags, HTML event handlers, and character encodings.",
            "**Session Hijacking**: Sets up listener infrastructure to exfiltrate `document.cookie` and impersonate victim user sessions.",
            "**Modern Defensive Mitigations**: Implements Content Security Policy (CSP), contextual output encoding, and `HttpOnly` cookie flags."
        ],
        "exec_summary": """Cross-Site Scripting (XSS) occurs when an application includes untrusted user input in a web page without proper validation or encoding, allowing attackers to execute arbitrary JavaScript in the victim's browser context.

In this module, we dissect Reflected, Stored, and DOM-based XSS vectors. We craft custom exploit payloads, bypass defensive input filters, exfiltrate session cookies, and solve every lab challenge with complete technical walkthroughs and flags."""
    },
    "file-upload-attacks": {
        "title": "File Upload Attacks",
        "clean_name": "File Upload Attacks",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/136",
        "core_topic": "unrestricted file upload vulnerabilities, extension validation bypasses, MIME-type spoofing, magic byte manipulation, polyglot payloads, and web shell execution",
        "takeaways": [
            "**Validation Architecture**: Analyzes client-side JavaScript validation, server-side extension checks, MIME-type verification, and magic byte inspection.",
            "**Extension Bypass Techniques**: Bypasses blacklists using alternate extensions (`.phtml`, `.php5`, `.phar`, `.pht`), case variations, and double extensions (`.php.jpg`).",
            "**MIME-Type & Magic Byte Spoofing**: Modifies `Content-Type` headers to `image/jpeg` and prepends GIF/PNG magic bytes (`GIF89a;`) to executable scripts.",
            "**Polyglot Payload Engineering**: Embeds functional PHP web shells into valid image metadata (EXIF data) that survive image processing libraries.",
            "**Upload Storage Exploitation**: Leverages directory traversal in file names (`../../shell.php`) to force file placement into executable web roots."
        ],
        "exec_summary": """File upload functionality is a common feature in modern web applications for user profile images, documents, and media. When upload handlers fail to strictly validate file types, extensions, and content, attackers can upload executable web shells that grant instant remote code execution.

This module delivers an exhaustive technical breakdown of file upload exploitation. We bypass client-side validation, circumvent extension blacklists, craft polyglot payloads, execute web shells, and capture all assessment flags."""
    },
    "web-attacks": {
        "title": "Web Attacks",
        "clean_name": "Web Attacks",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/134",
        "core_topic": "HTTP request smuggling, Cross-Site Request Forgery (CSRF), Insecure Direct Object References (IDOR), XML External Entity (XXE), and parameter tampering",
        "takeaways": [
            "**IDOR Vulnerabilities**: Modifies numeric and GUID references in request parameters to access and modify unauthorized user resources.",
            "**CSRF Exploitation**: Crafts weaponized HTML forms that trick authenticated victim browsers into executing unwanted state-changing actions.",
            "**Request Smuggling**: Exploits discrepancies in frontend and backend HTTP request length handling (`Content-Length` vs `Transfer-Encoding`).",
            "**Parameter Tampering**: Manipulates hidden form fields, cookies, and JSON parameters to bypass business logic and access control gates.",
            "**Comprehensive Remediation**: Implements robust anti-CSRF tokens, SameSite cookie attributes, and indirect reference maps."
        ],
        "exec_summary": """Web application vulnerabilities encompass a diverse spectrum of logic, architectural, and protocol-level flaws that can compromise user sessions and backend infrastructure.

This module provides a detailed technical exploration of essential web attacks. We analyze IDOR data exposure, craft CSRF exploitation chains, dissect HTTP request smuggling mechanics, and solve all lab challenges with complete flag solutions."""
    },
    "session-security": {
        "title": "Session Security",
        "clean_name": "Session Security",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "General",
        "url": "https://academy.hackthebox.com/module/153",
        "core_topic": "web session management, cookie attributes (Secure, HttpOnly, SameSite), session fixation, session hijacking, predictable tokens, and token lifecycle management",
        "takeaways": [
            "**Session Lifecycle Management**: Analyzes session creation, maintenance, expiration timeouts, and proper server-side invalidation.",
            "**Cookie Security Attributes**: Evaluates the defensive impact of `HttpOnly` (XSS protection), `Secure` (TLS-only), and `SameSite` (CSRF defense).",
            "**Session Fixation Attacks**: Exploits applications that preserve pre-authentication session identifiers after successful user login.",
            "**Session Token Analysis**: Analyzes entropy and randomness in session tokens using Burp Suite Sequencer to identify predictable generation algorithms.",
            "**Session Hijacking Vectors**: Captures session tokens through network sniffing, XSS exfiltration, and application log exposure."
        ],
        "exec_summary": """Web applications use session management mechanisms to maintain authenticated state across stateless HTTP transactions. Flaws in session token generation, transmission, or invalidation allow attackers to hijack legitimate user sessions and assume their identities.

In this module, we examine web session security architectures. We audit cookie security attributes, exploit session fixation flaws, analyze session entropy, hijack active user sessions, and extract all module flags."""
    },
    "cracking-passwords-with-hashcat": {
        "title": "Cracking Passwords with Hashcat",
        "clean_name": "Cracking Passwords with Hashcat",
        "tier": "Tier I",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/20",
        "core_topic": "advanced password cracking with Hashcat, GPU acceleration, attack modes (0, 1, 3, 6, 7), rule-based cracking, and mask-based brute forcing",
        "takeaways": [
            "**Hashcat Performance Tuning**: Optimizes GPU workload profiles (`-w 3`, `-w 4`) and tuning parameters for maximum hash processing speed.",
            "**Attack Modes Deep-Dive**: Masters Straight (`-a 0`), Combination (`-a 1`), Brute-force/Mask (`-a 3`), and Hybrid attacks (`-a 6`, `-a 7`).",
            "**Rule-Based Wordlist Expansion**: Applies mutation rules (`OneRuleToRuleThemAll`, `best64.rule`) to expand standard dictionaries with common user patterns.",
            "**Mask Attacks & Custom Charsets**: Constructs targeted mask patterns (`?u?l?l?l?d?d?s`) and defines custom character sets for constrained brute-forcing.",
            "**Hash Formats Mastery**: Identifies and cracks NTLM, Kerberos 5 TGS/AS-REP, Linux SHA-512, MD5, and bcrypt hashes."
        ],
        "exec_summary": """Hashcat is recognized as the world's fastest and most versatile password recovery utility, leveraging hardware GPU acceleration to test billions of candidate hashes per second against complex cryptographic algorithms.

This module delivers a comprehensive technical guide to Hashcat operations. We explore GPU benchmarking, configure dictionary and mask attacks, write custom mutation rules, crack enterprise password hashes, and solve all module challenges with verified flags."""
    },
    "using-the-metasploit-framework": {
        "title": "Using the Metasploit Framework",
        "clean_name": "Using the Metasploit Framework",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/39",
        "core_topic": "Metasploit Framework architecture, msfconsole navigation, auxiliary scanner modules, exploit execution, Meterpreter post-exploitation, and database workspace management",
        "takeaways": [
            "**Framework Architecture**: Dissects module types: exploits, payloads (singles, stagers, stages), auxiliary scanners, encoders, and post modules.",
            "**Database & Workspace Management**: Integrates PostgreSQL with `msfconsole` to manage engagement workspaces, hosts, services, and credentials.",
            "**Module Configuration**: Searches, configures targets, payloads, and parameters (`RHOSTS`, `LHOST`, `LPORT`) for reliable exploitation.",
            "**Meterpreter Deep-Dive**: Masters in-memory post-exploitation: process migration, credential dumping, port forwarding, and token stealing.",
            "**Automation with Resource Scripts**: Automates repetitive reconnaissance and multi-handler listeners using `.rc` resource scripts."
        ],
        "exec_summary": """The Metasploit Framework is the world's most widely used penetration testing platform, providing an extensive repository of vetted exploits, network scanners, and sophisticated post-exploitation payloads.

In this module, we conduct a structured technical walkthrough of Metasploit. We manage database workspaces, launch auxiliary scanners, execute public exploits against vulnerable services, operate Meterpreter sessions, and extract all assessment flags."""
    },
    "using-crackmapexec": {
        "title": "Using CrackMapExec",
        "clean_name": "Using CrackMapExec",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/98",
        "core_topic": "network penetration testing with CrackMapExec (CME/NetExec), SMB enumeration, password spraying, Pass-the-Hash, LSA/SAM dumping, and WMI/WinRM remote execution",
        "takeaways": [
            "**Multi-Protocol Auditing**: Assesses network services across SMB, WinRM, WMI, RDP, MSSQL, SSH, and LDAP from a single unified CLI.",
            "**Password Spraying at Scale**: Executes high-volume credential testing across subnets while avoiding account lockout thresholds.",
            "**Pass-the-Hash Execution**: Replays NTLM password hashes across hosts via SMB and WMI to execute commands without plaintext passwords.",
            "**Credential Extraction**: Dumps local SAM database hashes, LSA secrets, and Active Directory NTDS.dit hashes directly over the wire.",
            "**Custom Modules & Post-Exploitation**: Deploys CME modules (`spider_plus`, `bloodhound`, `mimikatz`) to accelerate lateral movement."
        ],
        "exec_summary": """CrackMapExec (now maintained as NetExec) is the Swiss Army knife for pentesting Windows and Active Directory networks. It automates network enumeration, password spraying, and post-exploitation across multiple enterprise protocols.

This module provides an in-depth operational guide to CrackMapExec. We audit SMB shares, execute password spray campaigns, perform Pass-the-Hash lateral movement, extract domain credentials, and solve every assessment flag."""
    },
    "stack-based-buffer-overflows-on-linux-x86": {
        "title": "Stack-Based Buffer Overflows on Linux x86",
        "clean_name": "Stack-Based Buffer Overflows on Linux x86",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/31",
        "core_topic": "x86 Linux binary exploitation, stack frame anatomy, CPU registers, buffer overflow offsets, bad character analysis, EIP overwrite, and custom shellcode injection",
        "takeaways": [
            "**Stack Frame Architecture**: Deconstructs function prologues, local buffer allocation, base pointer (`EBP`), and saved instruction pointer (`EIP`).",
            "**Offset Identification**: Uses cyclic pattern generation and calculation (`pattern_create`, `pattern_offset`) to precisely pinpoint the EIP overwrite offset.",
            "**Bad Character Analysis**: Systematically identifies byte values that get truncated or corrupted by vulnerable string handling functions.",
            "**Shellcode Development**: Compiles and injects custom Linux x86 `/bin/sh` shellcode into memory buffers.",
            "**NOP Sleds & Jump Instructions**: Employs NOP sleds (`\\x90`) and `JMP ESP` instructions to achieve reliable execution flow hijacking."
        ],
        "exec_summary": """Stack-based buffer overflows represent the foundational class of memory corruption vulnerabilities. Corrupting the execution stack allows an attacker to overwrite the saved instruction pointer and redirect processor execution to arbitrary shellcode.

In this module, we conduct a low-level disassembly and exploitation study of Linux x86 binaries. We inspect registers using GDB, identify exact EIP offsets, eliminate bad characters, inject custom shellcode, and capture all assessment flags."""
    },
    "stack-based-buffer-overflows-on-windows-x86": {
        "title": "Stack-Based Buffer Overflows on Windows x86",
        "clean_name": "Stack-Based Buffer Overflows on Windows x86",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/32",
        "core_topic": "x86 Windows binary exploitation, Immunity Debugger, Mona.py, EIP redirection, bad character filtering, finding JMP ESP in non-protected modules, and shellcode execution",
        "takeaways": [
            "**Debugger Operations**: Utilizes Immunity Debugger and `mona.py` to inspect memory, register states, and module protection mitigations.",
            "**EIP Overwrite Pinpointing**: Determines exact buffer length and offset to control the Windows `EIP` register.",
            "**Bad Character Filtering**: Employs `mona bytearray` and memory comparison to detect and eliminate bad characters.",
            "**Reliable Pointer Selection**: Searches executable modules for reliable `JMP ESP` instructions that lack SafeSEH, ASLR, and DEP protections.",
            "**MSFvenom Shellcode Generation**: Generates encoded Windows reverse shell payloads that avoid bad characters and fit within available buffer space."
        ],
        "exec_summary": """Exploiting memory corruption flaws on Windows x86 requires structured debugging tradecraft and an understanding of operating system binary protections. Overwriting the instruction pointer grants full execution control over the application.

This module delivers a step-by-step technical guide to Windows x86 stack overflow exploitation. We use Immunity Debugger and Mona.py to analyze memory, find reliable `JMP ESP` instructions, generate encoded reverse shell payloads, and solve every lab flag."""
    },
    "attacking-wifi-protected-setup-wps": {
        "title": "Attacking Wi-Fi Protected Setup (WPS)",
        "clean_name": "Attacking Wi-Fi Protected Setup (WPS)",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/131",
        "core_topic": "wireless penetration testing, Wi-Fi Protected Setup (WPS) PIN architecture, Reaver, Bully, Pixie Dust attack, and recovering WPA/WPA2 pre-shared keys",
        "takeaways": [
            "**WPS Architecture Flaws**: Analyzes the structural design flaw dividing the 8-digit WPS PIN into two separately validated halves (10,000 + 1,000 possibilities).",
            "**Pixie Dust Attack**: Exploits weak pseudo-random number generators (PRNG) in Access Point chipsets to recover the WPS PIN offline in seconds.",
            "**Online PIN Brute-Forcing**: Leverages `reaver` and `bully` to systematically brute-force WPS PINs while managing AP lockout throttling.",
            "**WPA/WPA2 Key Recovery**: Obtains the plaintext WPA/WPA2 network passphrase directly upon successful WPS PIN validation.",
            "**Wireless Hardening**: Decommissions WPS functionality across enterprise and consumer wireless access points."
        ],
        "exec_summary": """Wi-Fi Protected Setup (WPS) was designed to simplify connecting devices to secure wireless networks. However, severe design flaws in its 8-digit PIN validation mechanism allow attackers to brute-force access in hours, or recover keys in seconds via the Pixie Dust attack.

In this module, we examine wireless security auditing targeting WPS. We inspect wireless frames, execute online PIN brute-force attacks, leverage offline Pixie Dust techniques to recover WPA2 passphrases, and capture all assessment flags."""
    },
    "web-fuzzing": {
        "title": "Web Fuzzing",
        "clean_name": "Web Fuzzing",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/188",
        "core_topic": "web application fuzzing techniques, directory fuzzing, extension discovery, parameter discovery, POST data fuzzing, VHost routing, and filter calibration",
        "takeaways": [
            "**Systematic Fuzzing Methodology**: Employs dictionary-driven fuzzing across all components of HTTP requests: URI paths, parameters, headers, and bodies.",
            "**High-Speed Tools**: Operates `ffuf` and `wfuzz` with tuned concurrency to rapidly discover unlinked web application assets.",
            "**Recursive Directory Discovery**: Automates multi-level directory traversal to uncover deeply nested administrative consoles.",
            "**Precision Response Calibration**: Calibrates filter flags (`-fs`, `-fc`, `-fl`, `-fw`) to eliminate false-positive responses generated by generic error handlers.",
            "**Targeted Wordlist Selection**: Cross-references application frameworks with tailored wordlists from the SecLists project."
        ],
        "exec_summary": """Web fuzzing is an indispensable technique for uncovering hidden attack surfaces that are absent from public sitemaps and search engine indexes. By systematically submitting wordlists against web inputs, testers reveal unlinked files, administrative portals, and debugging parameters.

This module provides a comprehensive technical walkthrough of web fuzzing tradecraft. We explore high-speed fuzzing configurations, recursive endpoint discovery, parameter enumeration, and response filtering, solving all lab challenges and flags."""
    },
    "web-service-and-api-attacks": {
        "title": "Web Service & API Attacks",
        "clean_name": "Web Service & API Attacks",
        "tier": "Tier II",
        "diff": "Medium",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/161",
        "core_topic": "SOAP web services, REST APIs, WSDL enumeration, XML signature wrapping, XXE injection in web services, command injection, and API authorization flaws",
        "takeaways": [
            "**WSDL Discovery & Analysis**: Discovers and parses Web Services Description Language (WSDL) files to map all exposed operations and parameters.",
            "**SOAP Message Manipulation**: Crafts and tampers with XML-based SOAP envelopes to bypass business logic and authentication controls.",
            "**XML Injection & XXE**: Injects malicious entity definitions into XML payloads to achieve file disclosure and internal SSRF.",
            "**API Command & SQL Injection**: Tests REST and SOAP endpoints for underlying command and database injection vulnerabilities.",
            "**Modern Defensive Controls**: Deploys API gateways, schema validators, and disallows external DTD processing across web services."
        ],
        "exec_summary": """Web services and enterprise APIs facilitate machine-to-machine communication using standardized XML (SOAP) or JSON (REST) protocols. When these services fail to validate XML schemas or implement robust authorization, they become susceptible to severe injection and data disclosure attacks.

In this module, we conduct an exhaustive study of web service and API attacks. We parse WSDL files, manipulate SOAP envelopes, exploit XML External Entity flaws, execute arbitrary commands, and extract all module flags."""
    },
    "wifi-penetration-testing-basics": {
        "title": "Wi-Fi Penetration Testing Basics",
        "clean_name": "Wi-Fi Penetration Testing Basics",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/130",
        "core_topic": "IEEE 802.11 wireless fundamentals, monitor mode, packet sniffing (Airodump-ng), deauthentication attacks (Aireplay-ng), and capturing 4-way WPA/WPA2 handshakes",
        "takeaways": [
            "**802.11 Protocol Architecture**: Dissects wireless frame types: Management frames (beacons, probe requests), Control frames (RTS/CTS, ACK), and Data frames.",
            "**Monitor Mode Configuration**: Puts wireless NICs into monitor mode using `airmon-ng` to capture raw RF traffic across 2.4 GHz and 5 GHz bands.",
            "**Active Reconnaissance**: Identifies BSSIDs, ESSIDs, operational channels, client MAC addresses, and encryption types using `airodump-ng`.",
            "**Deauthentication Attacks**: Injects 802.11 deauthentication frames with `aireplay-ng` to force clients to disconnect and re-authenticate.",
            "**4-Way Handshake Capture**: Captures the EAPOL 4-way handshake required for offline WPA/WPA2 Pre-Shared Key (PSK) cracking."
        ],
        "exec_summary": """Wireless networks expand enterprise connectivity beyond physical building walls, making robust wireless security auditing a critical discipline. Understanding 802.11 frame structures and the WPA/WPA2 4-way authentication handshake is essential for wireless assessments.

This module covers the core fundamentals of Wi-Fi penetration testing. We configure wireless interfaces into monitor mode, sniff beacon and data frames, inject targeted deauthentication packets, capture cryptographic handshakes, and solve all assessment flags."""
    },
    "wired-equivalent-privacy-wep-attacks": {
        "title": "Wired Equivalent Privacy (WEP) Attacks",
        "clean_name": "Wired Equivalent Privacy (WEP) Attacks",
        "tier": "Tier I",
        "diff": "Easy",
        "cat": "Offensive",
        "url": "https://academy.hackthebox.com/module/132",
        "core_topic": "legacy WEP encryption flaws, RC4 stream cipher vulnerabilities, 24-bit Initialization Vector (IV) collisions, ARP request replay attacks, and statistical key recovery (FMS/PTW)",
        "takeaways": [
            "**WEP Cryptographic Weaknesses**: Explains how 24-bit Initialization Vectors (IVs) combined with the RC4 stream cipher result in rapid IV reuse and keystream leakage.",
            "**ARP Request Replay**: Injects captured ARP request frames with `aireplay-ng -3` to force the Access Point to generate thousands of fresh IVs per minute.",
            "**Statistical Key Recovery**: Employs `aircrack-ng` to execute the PTW (Pyshkin, Tews, Weinmann) and FMS attacks to reconstruct the master WEP key.",
            "**Chopchop & Fragmentation Attacks**: Decrypts WEP data packets and generates valid PRGA keystreams without knowing the encryption key.",
            "**Enterprise Decommissioning**: Highlights the urgent necessity of removing legacy WEP hardware in favor of WPA2/WPA3-Enterprise."
        ],
        "exec_summary": """Wired Equivalent Privacy (WEP) was the original security algorithm introduced in the IEEE 802.11 standard. Severe mathematical vulnerabilities in its implementation of the RC4 stream cipher and short 24-bit Initialization Vectors allow complete key recovery within minutes.

In this module, we conduct a technical analysis of WEP cryptanalytic attacks. We capture initialization vectors, execute ARP request replay packet injection, perform statistical key recovery using Aircrack-ng, and capture all assessment flags."""
    }
}

post_files = sorted(glob.glob('_posts/*-htb-academy-*.md'))
print(f"Total HTB posts to standardize: {len(post_files)}")

standardized_count = 0

for pf in post_files:
    fname = os.path.basename(pf)
    # Extract slug and part number: 2026-11-12-htb-academy-part-1-getting-started.md
    m = re.search(r'htb-academy-part-(\d+)-(.+)\.md$', fname)
    if not m:
        print(f"Skipping {fname}, cannot match pattern")
        continue
    part_num = m.group(1)
    slug = m.group(2)

    if slug not in MODULE_META:
        print(f"Warning: slug {slug} not found in MODULE_META!")
        continue

    meta = MODULE_META[slug]

    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split on the main lab heading: '## Comprehensive Lab Walkthrough & Flag Solutions'
    if '## Comprehensive Lab Walkthrough & Flag Solutions' not in content:
        print(f"Error: {fname} missing '## Comprehensive Lab Walkthrough & Flag Solutions'")
        continue

    parts = content.split('## Comprehensive Lab Walkthrough & Flag Solutions', 1)
    frontmatter_and_old_intro = parts[0]
    lab_content = '## Comprehensive Lab Walkthrough & Flag Solutions' + parts[1]

    # Extract frontmatter (between first and second '---')
    fm_match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        print(f"Error: cannot find frontmatter in {fname}")
        continue
    frontmatter_block = f"---\n{fm_match.group(1)}\n---\n\n"

    # Extract pristine series nav from the bottom of the file
    series_nav = '<div class="ff-series-nav">' + content.split('<div class="ff-series-nav">')[-1].strip()

    # Format takeaways
    takeaways_formatted = "\n".join([f"* {t}" for t in meta["takeaways"]])

    # Build standardized introduction block
    standardized_intro = f"""{frontmatter_block}Welcome to **Part {part_num}** of our comprehensive, production-grade masterclass covering the **Hack The Box (HTB) Academy Certified Penetration Testing Specialist (CPTS)** curriculum. Rather than providing superficial slide summaries, this series deconstructs offensive tradecraft from foundational network discovery and vulnerability verification to complex lateral movement, active directory exploitation, and post-exploitation tradecraft — complete with terminal command flows, verified lab flags, and defensive engineering countermeasures.

In this installment, we conduct an exhaustive technical deep-dive into **{meta['clean_name']}** ({meta['tier']} • {meta['diff']} • {meta['cat']}). We break down the underlying mechanics of {meta['core_topic']}, dissect hands-on offensive vectors, analyze realistic defensive telemetry, and walk through every exercise step-by-step with 100% verified solutions.

{series_nav}

## Module Specifications & Target Architecture

| Attribute | Specification |
| :--- | :--- |
| **Module Name** | `{meta['clean_name']}` |
| **Official HTB Academy Track** | [{meta['url']}]({meta['url']}) |
| **Curriculum Tier & Difficulty** | `{meta['tier']}` • `{meta['diff']}` |
| **Certification Pathway** | `HTB Certified Penetration Testing Specialist (CPTS)` (Part {part_num} of 41) |
| **Author & Technical Attribution** | `Abdulrahman M. Fathi (0x3bdo)` |
| **Lab Flag Verification** | `100% Fully Solved & Validated` |

## Key Technical Takeaways

{takeaways_formatted}

## Executive Summary & Assessment Scope

{meta['exec_summary']}

---

"""

    new_full_content = standardized_intro + lab_content

    with open(pf, 'w', encoding='utf-8') as f:
        f.write(new_full_content)

    standardized_count += 1

print(f"Successfully applied standardized introduction to {standardized_count} posts!")
