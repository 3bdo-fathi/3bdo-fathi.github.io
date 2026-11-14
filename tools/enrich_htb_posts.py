import os
import glob
import re

MODULE_ENRICHMENTS = {
    "getting-started": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Nibbles Blog RCE via arbitrary PHP upload"),
            ("T1059.004", "Command and Scripting Interpreter: Unix Shell", "Execution", "Bash interactive shell via reverse shell payload"),
            ("T1548.003", "Sudo and Sudo Caching", "Privilege Escalation", "Sudo privileges on monitor.sh script to execute root shell"),
            ("T1046", "Network Service Discovery", "Discovery", "Nmap port and service banner discovery")
        ],
        "cwe": [
            ("CWE-78", "Improper Neutralization of Special Elements used in an OS Command"),
            ("CWE-434", "Unrestricted Upload of File with Dangerous Type"),
            ("CWE-269", "Improper Privilege Management")
        ],
        "detection": [
            "Monitor web server process trees (e.g., Apache/nginx) spawning `/bin/bash` or `/bin/sh` via Linux Auditd or Sysmon for Linux.",
            "Alert on unauthorized edits to script files specified in `sudoers` configurations (`/etc/sudoers` or `/etc/sudoers.d/*`).",
            "Deploy Web Application Firewall (WAF) inspection rules filtering multipart form uploads containing PHP executable signatures."
        ],
        "references": [
            ("[HTB Academy: Getting Started Module](https://academy.hackthebox.com/module/77)", "Official Hack The Box curriculum track"),
            ("[OWASP Web Security Testing Guide (WSTG)](https://owasp.org/www-project-web-security-testing-guide/)", "Comprehensive testing standard for web applications"),
            ("[GTFOBins: Sudo Privilege Escalation](https://gtfobins.github.io/)", "Curated list of Unix binaries that can be exploited for privilege escalation"),
            ("[Exploit-DB Nibbleblog 4.0.3 RCE (CVE-2015-6967)](https://www.exploit-db.com/exploits/38489)", "Public vulnerability details and exploit proof-of-concept")
        ]
    },
    "file-transfers": {
        "mitre": [
            ("T1105", "Ingress Tool Transfer", "Command and Control", "Downloading exploitation binaries, LinPEAS/WinPEAS, and scripts"),
            ("T1041", "Exfiltration Over C2 Channel", "Exfiltration", "Exfiltrating SAM, SYSTEM, shadow files over HTTP/SMB/FTP"),
            ("T1048.003", "Exfiltration Over Alternative Protocol: Symmetric Protocol", "Exfiltration", "Base64 string exfiltration through DNS or ICMP"),
            ("T1071.001", "Application Layer Protocol: Web Protocols", "Command and Control", "Python SimpleHTTPServer, Certutil, Bitsadmin transfers")
        ],
        "cwe": [
            ("CWE-200", "Exposure of Sensitive Information to an Unauthorized Actor"),
            ("CWE-319", "Cleartext Transmission of Sensitive Information")
        ],
        "detection": [
            "Sysmon Event ID 1: Monitor execution of `certutil.exe -urlcache -split -f`, `bitsadmin.exe /transfer`, or `curl.exe` with external IP destinations.",
            "Sysmon Event ID 3: High-volume outbound network connections from non-browser administrative binaries (`powershell.exe`, `cmd.exe`).",
            "Linux Auditd: Alert on curl/wget child processes spawned from web service daemon users (`www-data`, `apache`, `nginx`)."
        ],
        "references": [
            ("[HTB Academy: File Transfers Module](https://academy.hackthebox.com/module/24)", "Official Hack The Box curriculum track"),
            ("[LOLBAS Project: Windows Living Off The Land Binaries](https://lolbas-project.github.io/)", "Complete reference of built-in Windows binaries usable for file ingress/egress"),
            ("[GTFOBins: File Transfer Binaries](https://gtfobins.github.io/)", "Unix binaries capable of remote file upload and download"),
            ("[PayloadsAllTheThings: File Transfer Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings)", "Comprehensive operational transfer commands across OS platforms")
        ]
    },
    "information-gathering-web-edition": {
        "mitre": [
            ("T1595.001", "Active Scanning: Scanning IP Blocks", "Reconnaissance", "Target host enumeration and port probing"),
            ("T1596.001", "Search Open Technical Databases: DNS/Passive DNS", "Reconnaissance", "Passive DNS enumeration via crt.sh and VirusTotal"),
            ("T1590.002", "Gather Victim Network Information: DNS", "Reconnaissance", "Zone transfer queries (AXFR) and subdomain brute-forcing")
        ],
        "cwe": [
            ("CWE-200", "Information Exposure Through DNS and Metadata")
        ],
        "detection": [
            "Monitor DNS servers for unauthorized AXFR zone transfer requests from unvetted external IP addresses.",
            "Inspect web proxy logs for high-frequency requests from non-standard user-agents or automated recon tools (Amass, Sublist3r).",
            "Rate-limit public DNS and reverse DNS query endpoints to mitigate automated enumeration campaigns."
        ],
        "references": [
            ("[HTB Academy: Information Gathering Web Edition](https://academy.hackthebox.com/module/144)", "Official Hack The Box curriculum track"),
            ("[OWASP WSTG: Information Gathering](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/)", "Web reconnaissance methodology"),
            ("[crt.sh: Certificate Search Engine](https://crt.sh/)", "Public Certificate Transparency log inspection"),
            ("[RFC 1035: Domain Names - Implementation and Specification](https://www.ietf.org/rfc/rfc1035.txt)", "Standard DNS protocol specification")
        ]
    },
    "footprinting": {
        "mitre": [
            ("T1046", "Network Service Discovery", "Discovery", "Scanning TCP/UDP ports, identifying daemon versions and exposed services"),
            ("T1595.002", "Active Scanning: Vulnerability Scanning", "Reconnaissance", "Probing FTP, SMB, NFS, SNMP, and SMTP interfaces for defaults"),
            ("T1018", "Remote System Discovery", "Discovery", "Network topology mapping and active subnet identification")
        ],
        "cwe": [
            ("CWE-200", "Information Exposure Through Environmental Information"),
            ("CWE-287", "Improper Authentication - Anonymous Access to Network Shares")
        ],
        "detection": [
            "Deploy Zeek and Suricata rules triggering alerts on SYN scans, ACK scans, or UDP sweeps targeting common enterprise ports.",
            "Log anonymous SMB sessions (`IPC$`, `SYSVOL`, `NETLOGON`) and anonymous FTP logins in centralized SIEM.",
            "Restrict SNMP access by replacing community strings `public` and `private` with SNMPv3 encrypted authentication."
        ],
        "references": [
            ("[HTB Academy: Footprinting Module](https://academy.hackthebox.com/module/112)", "Official Hack The Box curriculum track"),
            ("[Nmap Official Documentation & Book](https://nmap.org/book/man.html)", "Fyodor's official reference for network scanning and NSE scripts"),
            ("[HackTricks: Pentesting Network Services](https://book.hacktricks.xyz/network-services-pentesting)", "In-depth cheat sheets for foot printing individual ports"),
            ("[RFC 793: Transmission Control Protocol](https://www.ietf.org/rfc/rfc793.txt)", "Core TCP protocol specification")
        ]
    },
    "linux-privilege-escalation": {
        "mitre": [
            ("T1548.001", "Abuse Elevation Control Mechanism: Setuid and Setgid", "Privilege Escalation", "Exploiting misconfigured SUID binaries"),
            ("T1053.003", "Scheduled Task/Job: Cron", "Privilege Escalation", "Hijacking root cron jobs through writeable scripts or wildcards"),
            ("T1543.002", "Create or Modify System Process: systemd Service", "Privilege Escalation", "Misconfigured service unit files with root privileges"),
            ("T1068", "Exploitation for Privilege Escalation", "Privilege Escalation", "Kernel exploitation (e.g., Dirty Pipe, Dirty Cow, PwnKit)")
        ],
        "cwe": [
            ("CWE-269", "Improper Privilege Management"),
            ("CWE-732", "Incorrect Permission Assignment for Critical Resource"),
            ("CWE-276", "Incorrect Default Permissions")
        ],
        "detection": [
            "Linux Auditd: Monitor `execve` calls where EUID is 0 but RUID is unprivileged.",
            "Enforce file integrity monitoring (FIM) over `/etc/crontab`, `/etc/cron.*`, and `/etc/sudoers`.",
            "Audit system binaries with `find / -perm -4000 -type f 2>/dev/null` and flag unknown SUID executables."
        ],
        "references": [
            ("[HTB Academy: Linux Privilege Escalation](https://academy.hackthebox.com/module/51)", "Official Hack The Box curriculum track"),
            ("[GTFOBins: Unix SUID / Sudo Reference](https://gtfobins.github.io/)", "Authoritative repository for Unix binary abuse"),
            ("[HackTricks: Linux Local Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)", "Complete Linux post-exploitation methodology"),
            ("[PayloadsAllTheThings: Linux Privilege Escalation](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation)", "Practical privilege escalation commands")
        ]
    },
    "login-brute-forcing": {
        "mitre": [
            ("T1110.001", "Brute Force: Password Guessing", "Credential Access", "Systematic automated credential guessing against login endpoints"),
            ("T1110.003", "Brute Force: Password Spraying", "Credential Access", "Testing single common passwords against multiple accounts to evade lockouts"),
            ("T1110.004", "Brute Force: Credential Stuffing", "Credential Access", "Replaying leaked credential pairs against authentication portals")
        ],
        "cwe": [
            ("CWE-307", "Improper Restriction of Excessive Authentication Attempts")
        ],
        "detection": [
            "Monitor Windows Security Event ID 4625 (An account failed to log on) with threshold-based alerting.",
            "Implement progressive delay and CAPTCHA mechanisms after multiple consecutive authentication failures.",
            "Enforce rate-limiting and IP throttling at the API gateway or reverse proxy layer."
        ],
        "references": [
            ("[HTB Academy: Login Brute Forcing](https://academy.hackthebox.com/module/57)", "Official Hack The Box curriculum track"),
            ("[OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)", "Best practices for authentication security"),
            ("[NIST SP 800-63B: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)", "Standard for authentication lifecycle and password policies"),
            ("[Hydra GitHub Repository](https://github.com/vanhauser-thc/thc-hydra)", "Fast network logon cracker reference")
        ]
    },
    "broken-authentication": {
        "mitre": [
            ("T1078", "Valid Accounts", "Initial Access / Persistence", "Compromising accounts via weak session tokens and credential flaws"),
            ("T1556", "Modify Authentication Process", "Credential Access", "Bypassing 2FA, tampering with password reset workflows"),
            ("T1539", "Steal Web Session Cookie", "Credential Access", "Hijacking active session identifiers via insecure cookies")
        ],
        "cwe": [
            ("CWE-287", "Improper Authentication"),
            ("CWE-384", "Session Fixation"),
            ("CWE-640", "Weak Password Recovery Mechanism for Forgotten Password")
        ],
        "detection": [
            "Flag concurrent active sessions originating from geographically disparate IP addresses within impossible travel timeframes.",
            "Audit password reset endpoint requests lacking verification token validation or rate limits.",
            "Enforce cryptographic signing and expiration checks on all stateless tokens (JWT, OAuth Bearer)."
        ],
        "references": [
            ("[HTB Academy: Broken Authentication](https://academy.hackthebox.com/module/135)", "Official Hack The Box curriculum track"),
            ("[OWASP Top 10 A07:2021 Identification & Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)", "OWASP standard risk profile"),
            ("[RFC 7519: JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)", "JWT standard specifications"),
            ("[PortSwigger: Authentication Vulnerabilities](https://portswigger.net/web-security/authentication)", "Web Security Academy lab guides")
        ]
    },
    "command-injections": {
        "mitre": [
            ("T1059", "Command and Scripting Interpreter", "Execution", "Injecting arbitrary shell commands via unsanitized user inputs"),
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Command injection via web parameters, headers, or file names"),
            ("T1027", "Obfuscated Files or Information", "Defense Evasion", "Using space separators, variables, and encoding to bypass filters")
        ],
        "cwe": [
            ("CWE-78", "Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')")
        ],
        "detection": [
            "Alert on web processes (e.g., `php`, `httpd`, `nginx`, `python`) invoking shell binaries (`/bin/sh`, `/bin/bash`, `powershell.exe`).",
            "Monitor web access logs for command separators: `;`, `|`, `&`, `$(`, backticks, and URI-encoded variations (`%0A`, `%26`).",
            "Enforce strict input parameterization and avoid system command wrappers (`exec()`, `system()`, `passthru()`)."
        ],
        "references": [
            ("[HTB Academy: Command Injections](https://academy.hackthebox.com/module/109)", "Official Hack The Box curriculum track"),
            ("[OWASP OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)", "Hardening and code-level remediation"),
            ("[PayloadsAllTheThings: Command Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection)", "Exhaustive filter bypasses and payload variations"),
            ("[PortSwigger: OS Command Injection](https://portswigger.net/web-security/os-command-injection)", "Interactive testing guides")
        ]
    },
    "file-inclusion": {
        "mitre": [
            ("T1059", "Command and Scripting Interpreter", "Execution", "Remote File Inclusion (RFI) code execution via remote scripts"),
            ("T1083", "File and Directory Discovery", "Discovery", "Local File Inclusion (LFI) reading `/etc/passwd`, logs, or sensitive configs"),
            ("T1505.003", "Server Software Component: Web Shell", "Persistence", "Log poisoning or session poisoning to achieve RCE")
        ],
        "cwe": [
            ("CWE-22", "Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')"),
            ("CWE-98", "Improper Control of Generation of Code ('PHP Remote File Inclusion')")
        ],
        "detection": [
            "Log and block HTTP requests containing directory traversal sequences: `../`, `..%2f`, `....//`, and PHP wrappers (`php://filter`, `php://input`, `data://`).",
            "Disable `allow_url_include` and `allow_url_fopen` in `php.ini` configuration.",
            "Confine web application file access using chroot jails, containerization, or PHP `open_basedir` restrictions."
        ],
        "references": [
            ("[HTB Academy: File Inclusion](https://academy.hackthebox.com/module/23)", "Official Hack The Box curriculum track"),
            ("[OWASP File Inclusion Vulnerabilities](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion)", "Methodology and exploitation analysis"),
            ("[PayloadsAllTheThings: File Inclusion](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion)", "Comprehensive LFI/RFI cheat sheet"),
            ("[PortSwigger: Directory Traversal](https://portswigger.net/web-security/file-path-traversal)", "Practical exploitation scenarios")
        ]
    },
    "attacking-common-services": {
        "mitre": [
            ("T1021.002", "Remote Services: SMB/Windows Admin Shares", "Lateral Movement", "Enumerating and writing payloads to accessible SMB shares"),
            ("T1078", "Valid Accounts", "Initial Access / Persistence", "Authenticating with default or leaked credentials against SSH, FTP, MSSQL"),
            ("T1110", "Brute Force", "Credential Access", "Automated dictionary attacks against database and remote access protocols")
        ],
        "cwe": [
            ("CWE-287", "Improper Authentication"),
            ("CWE-200", "Information Exposure Through Misconfigured Service ACLs")
        ],
        "detection": [
            "Centralize and alert on unauthorized SMB administrative share queries (`C$`, `ADMIN$`, `IPC$`) from unmanaged endpoints.",
            "Deploy network segmentation ensuring critical database ports (1433, 3306, 5432) and SSH (22) are non-routable from the public internet.",
            "Enforce key-based authentication on SSH and disable root SSH login (`PermitRootLogin no`)."
        ],
        "references": [
            ("[HTB Academy: Attacking Common Services](https://academy.hackthebox.com/module/116)", "Official Hack The Box curriculum track"),
            ("[HackTricks: Pentesting Services](https://book.hacktricks.xyz/network-services-pentesting)", "Complete protocol enumeration and attack cheat sheet"),
            ("[Impacket Network Protocols Toolkit](https://github.com/fortra/impacket)", "Standard Python library for network protocol manipulation"),
            ("[Nmap NSE Script Reference](https://nmap.org/nsedoc/)", "Official NSE scripts for service probing")
        ]
    },
    "attacking-common-applications": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Targeting vulnerable software packages (Tomcat, Jenkins, Splunk, Drupal)"),
            ("T1212", "Exploitation for Credential Access", "Credential Access", "Extracting plain-text configuration passwords and cryptographic keys"),
            ("T1505.003", "Server Software Component: Web Shell", "Persistence", "Deploying WAR files or plugins containing web shells")
        ],
        "cwe": [
            ("CWE-20", "Improper Input Validation"),
            ("CWE-284", "Improper Access Control"),
            ("CWE-306", "Missing Authentication for Critical Function")
        ],
        "detection": [
            "Monitor application managers (e.g., Tomcat `/manager/html`, Jenkins `/script`) for external IP access and unauthorized deployments.",
            "Alert on unauthorized WAR or JAR package deployments via application container logs.",
            "Enforce strict role-based access control (RBAC) and mandatory multi-factor authentication (MFA) on enterprise administrative dashboards."
        ],
        "references": [
            ("[HTB Academy: Attacking Common Applications](https://academy.hackthebox.com/module/113)", "Official Hack The Box curriculum track"),
            ("[Exploit-DB Applications Archive](https://www.exploit-db.com/)", "Verified exploit database for common enterprise applications"),
            ("[Apache Tomcat Security Advisories](https://tomcat.apache.org/security.html)", "Official vulnerabilities and patch releases"),
            ("[Jenkins Security Bulletins](https://www.jenkins.io/security/advisories/)", "Advisories and remediation guidelines")
        ]
    },
    "active-directory-enumeration-and-attacks": {
        "mitre": [
            ("T1087.002", "Account Discovery: Domain Account", "Discovery", "Enumerating AD users, groups, and service accounts using LDAP/RPC"),
            ("T1558.003", "Steal or Forge Kerberos Tickets: Kerberoasting", "Credential Access", "Requesting TGS tickets for SPNs and offline hash cracking"),
            ("T1558.004", "Steal or Forge Kerberos Tickets: AS-REP Roasting", "Credential Access", "Harvesting AS-REP tickets for accounts with 'Do not require Kerberos preauthentication'"),
            ("T1003.006", "OS Credential Dumping: DCSync", "Credential Access", "Replicating domain credentials via MS-DRSR protocol")
        ],
        "cwe": [
            ("CWE-287", "Improper Authentication"),
            ("CWE-269", "Improper Privilege Management in Directory Services")
        ],
        "detection": [
            "Windows Event ID 4769: Audit Kerberos service ticket requests using RC4 encryption (`Ticket Options: 0x40810000`, `Ticket Encryption: 0x17`).",
            "Windows Event ID 4768: Audit Kerberos TGT requests with pre-authentication disabled (`Pre-Authentication Type: 0`).",
            "Monitor MS-DRSR directory replication network traffic originating from non-domain controller IP addresses (DCSync alerting)."
        ],
        "references": [
            ("[HTB Academy: Active Directory Enumeration & Attacks](https://academy.hackthebox.com/module/143)", "Official Hack The Box curriculum track"),
            ("[BloodHound GUI & SharpHound Documentation](https://bloodhound.readthedocs.io/)", "Active Directory attack graph modeling"),
            ("[ADSecurity.org (Sean Metcalf)](https://adsecurity.org/)", "Premier Active Directory security reference and defensive guidance"),
            ("[Mimikatz Wiki & Guide (Gentilkiwi)](https://github.com/gentilkiwi/mimikatz)", "Authoritative post-exploitation credentials extraction tool")
        ]
    },
    "attacking-enterprise-networks": {
        "mitre": [
            ("T1021", "Remote Services", "Lateral Movement", "Traversing network segments via WinRM, SSH, RDP, and WMI"),
            ("T1090", "Proxy", "Command and Control", "Deploying multi-hop proxy chains across segmented zones"),
            ("T1078.002", "Valid Accounts: Domain Accounts", "Defense Evasion", "Using compromised service credentials to cross trust boundaries")
        ],
        "cwe": [
            ("CWE-284", "Improper Access Control in Network Architectures"),
            ("CWE-200", "Exposure of Sensitive Information Across Subnets")
        ],
        "detection": [
            "Implement Zero Trust Network Access (ZTNA) requiring explicit authentication and continuous posture checks per connection.",
            "Deploy internal east-west network IDS/IPS sensors to detect lateral movement protocols traversing internal VLANs.",
            "Enforce tiering administration models (Tier 0 / Tier 1 / Tier 2) preventing domain admin credentials from touching lower-tier workstations."
        ],
        "references": [
            ("[HTB Academy: Attacking Enterprise Networks](https://academy.hackthebox.com/module/164)", "Official Hack The Box curriculum track"),
            ("[NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)", "Authoritative zero trust guidance"),
            ("[MITRE ATT&CK Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/)", "Global knowledge base of adversary tactics and techniques"),
            ("[Microsoft Security Documentation: Enterprise Access Model](https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model)", "Privileged access management guidance")
        ]
    },
    "using-web-proxies": {
        "mitre": [
            ("T1595.002", "Active Scanning: Vulnerability Scanning", "Reconnaissance", "Automated crawler and scanner proxy suites"),
            ("T1071.001", "Application Layer Protocol: Web Protocols", "Command and Control", "Intercepting, modifying, and replaying HTTP requests")
        ],
        "cwe": [
            ("CWE-200", "Information Exposure Through HTTP Headers and Traffic Analysis")
        ],
        "detection": [
            "Monitor web server access logs for anomalous header structures, repeated requests with incrementing parameters, or known proxy test headers.",
            "Enforce strict HTTP Strict Transport Security (HSTS) and public key pinning where applicable to disrupt rogue proxy certificate spoofing.",
            "Deploy Web Application Firewalls (WAF) to detect request tampering patterns."
        ],
        "references": [
            ("[HTB Academy: Using Web Proxies](https://academy.hackthebox.com/module/110)", "Official Hack The Box curriculum track"),
            ("[PortSwigger Burp Suite User Documentation](https://portswigger.net/burp/documentation)", "Official guide to proxy configuration and extensions"),
            ("[OWASP Zed Attack Proxy (ZAP) Documentation](https://www.zaproxy.org/docs/)", "Open-source web proxy and vulnerability scanner"),
            ("[Caido Web Security Tool](https://caido.io/)", "Modern lightweight interception proxy")
        ]
    },
    "vulnerability-assessment": {
        "mitre": [
            ("T1595.002", "Active Scanning: Vulnerability Scanning", "Reconnaissance", "Automated scanning of network infrastructure for known CVEs"),
            ("T1046", "Network Service Discovery", "Discovery", "Automated discovery of open ports, software versions, and banners")
        ],
        "cwe": [
            ("CWE-1035", "OWASP Top Ten 2021 Flaws"),
            ("CWE-937", "Using Components with Known Vulnerabilities")
        ],
        "detection": [
            "Track vulnerability scanning bursts originating from internal or external IP ranges using network telemetry (NetFlow, Suricata).",
            "Establish automated patch management pipelines prioritizing CVEs with high CVSS scores and active in-the-wild exploit maturity.",
            "Conduct routine authorized credentialed vulnerability assessments to detect outdated packages before adversaries exploit them."
        ],
        "references": [
            ("[HTB Academy: Vulnerability Assessment](https://academy.hackthebox.com/module/108)", "Official Hack The Box curriculum track"),
            ("[NIST National Vulnerability Database (NVD)](https://nvd.nist.gov/)", "Global repository of standards-based vulnerability management data"),
            ("[CVSS v3.1 Specification Guide](https://www.first.org/cvss/v3.1/specification-document)", "Common Vulnerability Scoring System standard"),
            ("[Greenbone OpenVAS Community Documentation](https://greenbone.github.io/docs/)", "Open-source vulnerability management suite")
        ]
    },
    "shells-and-payloads": {
        "mitre": [
            ("T1059", "Command and Scripting Interpreter", "Execution", "Reverse shells via Bash, PowerShell, Python, PHP, Perl, and Ruby"),
            ("T1071", "Application Layer Protocol", "Command and Control", "Encrypted reverse shells over TLS (Socat, OpenSSL)"),
            ("T1027", "Obfuscated Files or Information", "Defense Evasion", "Base64 encoded payloads and living-off-the-land reverse shell launchers")
        ],
        "cwe": [
            ("CWE-78", "Improper Neutralization of Special Elements used in an OS Command"),
            ("CWE-94", "Improper Control of Generation of Code ('Code Injection')")
        ],
        "detection": [
            "Monitor process lineage for interactive shells (`sh`, `bash`, `cmd`, `powershell`) whose parent process is a non-shell daemon or network worker.",
            "Detect unencrypted interactive terminal sequences (e.g., `sh -i >& /dev/tcp/...` or `whoami` strings) in raw network stream inspection.",
            "Enforce egress network filtering permitting only required outbound business ports, blocking non-standard outbound TCP/UDP connections."
        ],
        "references": [
            ("[HTB Academy: Shells & Payloads](https://academy.hackthebox.com/module/115)", "Official Hack The Box curriculum track"),
            ("[RevShells: Interactive Reverse Shell Generator](https://www.revshells.com/)", "Exhaustive repository of multi-language reverse shell one-liners"),
            ("[PayloadsAllTheThings: Reverse Shells](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)", "Technical reverse and bind shell tradecraft"),
            ("[Rapid7 MSFvenom Payload Generation Guide](https://docs.rapid7.com/metasploit/msfvenom/)", "Metasploit payload compiler reference")
        ]
    },
    "sql-injection-fundamentals": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Injecting SQL commands through web application input vectors"),
            ("T1003", "OS Credential Dumping", "Credential Access", "Extracting database password hashes via UNION and Blind SQLi"),
            ("T1505.003", "Server Software Component: Web Shell", "Persistence", "Writing web shells to document root using `INTO OUTFILE` or `xp_cmdshell`")
        ],
        "cwe": [
            ("CWE-89", "Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')")
        ],
        "detection": [
            "Implement parameterized queries and prepared statements across all database access layers to completely neutralize SQL injection.",
            "Monitor database query logs for abnormal SQL syntax (`UNION SELECT`, `SLEEP()`, `BENCHMARK()`, `waitfor delay`).",
            "Disable administrative database features like `xp_cmdshell` (MSSQL) and revoke file-write permissions (`FILE` privilege) from MySQL web accounts."
        ],
        "references": [
            ("[HTB Academy: SQL Injection Fundamentals](https://academy.hackthebox.com/module/33)", "Official Hack The Box curriculum track"),
            ("[OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)", "Authoritative remediation guidelines"),
            ("[PortSwigger: SQL Injection Vulnerabilities](https://portswigger.net/web-security/sql-injection)", "Interactive Web Security Academy training"),
            ("[PayloadsAllTheThings: SQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)", "Complete cheat sheet by SQL dialect (MySQL, MSSQL, PostgreSQL, Oracle)")
        ]
    },
    "sqlmap-essentials": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Automated SQL injection scanning and exploitation"),
            ("T1003", "OS Credential Dumping", "Credential Access", "Automated extraction of database schemas, tables, and credentials")
        ],
        "cwe": [
            ("CWE-89", "SQL Injection")
        ],
        "detection": [
            "Detect default SQLmap User-Agents (`sqlmap/X.X...`) and characteristic heuristic probe patterns (`AND 1=1`, `OR 1=1`).",
            "Deploy Web Application Firewall (WAF) rate limits triggering IP blocks on high-frequency error-generating query streams.",
            "Audit database query volumes per web request to prevent bulk table dumping."
        ],
        "references": [
            ("[HTB Academy: SQLMap Essentials](https://academy.hackthebox.com/module/58)", "Official Hack The Box curriculum track"),
            ("[SQLmap Official Documentation & User's Manual](https://github.com/sqlmapproject/sqlmap/wiki)", "Full manual of parameters, techniques, and tamper scripts"),
            ("[OWASP Testing for SQL Injection (WSTG-INPV-05)](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection)", "Methodological testing reference")
        ]
    },
    "password-attacks": {
        "mitre": [
            ("T1110.002", "Brute Force: Password Cracking", "Credential Access", "Cracking hashes offline via wordlists and rules"),
            ("T1003", "OS Credential Dumping", "Credential Access", "Dumping hashes from SAM, NTDS.dit, LSASS, and `/etc/shadow`"),
            ("T1555", "Credentials from Password Stores", "Credential Access", "Extracting credentials from browser storage, Keepass, and DPAPI")
        ],
        "cwe": [
            ("CWE-522", "Insufficiently Protected Credentials"),
            ("CWE-328", "Use of Weak Hash")
        ],
        "detection": [
            "Windows Event ID 4663 / 4656: Monitor unauthorized access requests to `LSASS.exe` process handles.",
            "Deploy Microsoft Defender Credential Guard to isolate LSASS memory in a virtualized container.",
            "Enforce modern slow hashing algorithms (Argon2id, bcrypt, PBKDF2) for stored application credentials instead of fast hashes (MD5, SHA1)."
        ],
        "references": [
            ("[HTB Academy: Password Attacks](https://academy.hackthebox.com/module/147)", "Official Hack The Box curriculum track"),
            ("[John the Ripper Official Documentation](https://www.openwall.com/john/doc/)", "Password cracker reference"),
            ("[SecLists Password Dictionaries](https://github.com/danielmiessler/SecLists/tree/master/Passwords)", "Standard wordlist collections"),
            ("[NIST SP 800-63B Authentication Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)", "Modern password complexity and length requirements")
        ]
    },
    "server-side-attacks": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Exploiting SSRF, XXE, and SSTI vulnerabilities"),
            ("T1552.005", "Unsecured Credentials: Cloud Instance Metadata", "Credential Access", "Querying AWS/Azure/GCP metadata endpoints (`169.254.169.254`) via SSRF"),
            ("T1059", "Command and Scripting Interpreter", "Execution", "Achieving remote code execution via Server-Side Template Injection")
        ],
        "cwe": [
            ("CWE-918", "Server-Side Request Forgery (SSRF)"),
            ("CWE-611", "Improper Restriction of XML External Entity Reference (XXE)"),
            ("CWE-1336", "Improper Neutralization of Special Elements Used in a Template Engine (SSTI)")
        ],
        "detection": [
            "Block outbound web server traffic to internal network addresses (RFC 1918) and cloud metadata service (`169.254.169.254/32`).",
            "Disable DTD external entity resolution (`DOCTYPE`, `ENTITY`) in all XML parsers (`libxml_disable_entity_loader(true)`).",
            "Sanitize input strings and avoid concatenating user inputs into template engine rendering functions (Jinja2, Twig, Freemarker)."
        ],
        "references": [
            ("[HTB Academy: Server-side Attacks](https://academy.hackthebox.com/module/145)", "Official Hack The Box curriculum track"),
            ("[OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)", "Comprehensive SSRF defense architecture"),
            ("[OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)", "XML parser hardening configurations"),
            ("[PortSwigger: Server-Side Template Injection (SSTI)](https://portswigger.net/web-security/server-side-template-injection)", "Analysis of template engine sandboxes")
        ]
    },
    "windows-privilege-escalation": {
        "mitre": [
            ("T1548.002", "Bypass User Account Control", "Privilege Escalation", "Abusing auto-elevating Windows binaries and registry hijacks"),
            ("T1543.003", "Create or Modify System Process: Windows Service", "Privilege Escalation", "Unquoted service paths and weak service permissions"),
            ("T1134", "Access Token Manipulation", "Privilege Escalation", "Potato exploits abusing `SeImpersonatePrivilege` or `SeAssignPrimaryToken`"),
            ("T1053.005", "Scheduled Task/Job: Scheduled Task", "Privilege Escalation", "Modifying binaries executed by SYSTEM scheduled tasks")
        ],
        "cwe": [
            ("CWE-269", "Improper Privilege Management"),
            ("CWE-428", "Unquoted Search Path or Element"),
            ("CWE-732", "Incorrect Permission Assignment for Critical Resource")
        ],
        "detection": [
            "Sysmon Event ID 1: Monitor anomalous child processes spawned by service binaries running as `NT AUTHORITY\\SYSTEM`.",
            "Sysmon Event ID 12 / 13: Monitor registry key changes under `HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run` or UAC registry keys.",
            "Audit service file permissions and ensure non-admin accounts do not have write access to service binaries or directories."
        ],
        "references": [
            ("[HTB Academy: Windows Privilege Escalation](https://academy.hackthebox.com/module/67)", "Official Hack The Box curriculum track"),
            ("[LOLBAS Project: Living Off The Land Binaries and Scripts](https://lolbas-project.github.io/)", "Complete repository of built-in Windows privilege abuse tools"),
            ("[HackTricks: Windows Local Privilege Escalation](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)", "Methodical Windows exploitation checklist"),
            ("[PayloadsAllTheThings: Windows Privilege Escalation](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation)", "Practical commands and scripts")
        ]
    },
    "pivoting-tunneling-and-port-forwarding": {
        "mitre": [
            ("T1090.001", "Proxy: Internal Proxy", "Command and Control", "Routing traffic through compromised intermediate hosts"),
            ("T1090.002", "Proxy: External Proxy", "Command and Control", "Chaining reverse tunnels out of restricted internal zones"),
            ("T1572", "Protocol Tunneling", "Command and Control", "Encapsulating raw TCP/UDP within SSH, HTTP, or DNS tunnels")
        ],
        "cwe": [
            ("CWE-284", "Improper Access Control - Insufficient Network Perimeter Isolation")
        ],
        "detection": [
            "Monitor network edge firewalls for sustained SSH or reverse SOCKS proxy connections originating from internal servers.",
            "Deploy deep packet inspection (DPI) to detect protocol tunneling (e.g., SSH over port 80/443, DNS tunneling).",
            "Restrict host-to-host lateral communication through host-based firewalls (Windows Defender Firewall, iptables)."
        ],
        "references": [
            ("[HTB Academy: Pivoting, Tunneling, and Port Forwarding](https://academy.hackthebox.com/module/158)", "Official Hack The Box curriculum track"),
            ("[Chisel Fast TCP/UDP Tunneling Documentation](https://github.com/jpillora/chisel)", "Chisel HTTP-based tunnel implementation"),
            ("[Ligolo-ng Modern Tun/Tap Pivoting Tool](https://github.com/nico-cha/ligolo-ng)", "Modern multi-platform tunneling framework"),
            ("[RFC 4251: The Secure Shell (SSH) Protocol Architecture](https://www.ietf.org/rfc/rfc4251.txt)", "Technical SSH port forwarding standards")
        ]
    },
    "api-attacks": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Targeting REST, GraphQL, and SOAP API endpoints"),
            ("T1059", "Command and Scripting Interpreter", "Execution", "Injecting commands or SQL through API parameters"),
            ("T1552", "Unsecured Credentials", "Credential Access", "Harvesting exposed API keys and JWT secrets from client scripts")
        ],
        "cwe": [
            ("CWE-284", "Improper Access Control (Broken Object Level Authorization - BOLA)"),
            ("CWE-287", "Improper Authentication (Broken Authentication)"),
            ("CWE-942", "Permissive Cross-Domain Policy with Untrusted Domains")
        ],
        "detection": [
            "Enforce object-level authorization checks at the controller level ensuring requesting users own requested resource IDs.",
            "Implement rate-limiting and quota controls per API client token and IP address.",
            "Validate and sanitize all API input payloads against a strict schema definition (OpenAPI / JSON Schema)."
        ],
        "references": [
            ("[HTB Academy: API Attacks](https://academy.hackthebox.com/module/160)", "Official Hack The Box curriculum track"),
            ("[OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x00-header/)", "Authoritative standard for API threat vectors"),
            ("[Postman API Security Testing Guide](https://learning.postman.com/docs/api-governance/api-security/)", "Standard testing workflows"),
            ("[PortSwigger: API Testing](https://portswigger.net/web-security/api-testing)", "Web Security Academy interactive modules")
        ]
    },
    "introduction-to-penetration-testing": {
        "mitre": [
            ("TA0043", "Reconnaissance", "Initial Phase", "Gathering victim intelligence and footprinting targets"),
            ("TA0001", "Initial Access", "Execution Phase", "Exploiting discovered weaknesses to establish foot hold"),
            ("TA0004", "Privilege Escalation", "Post-Exploitation", "Elevating permissions to administrative tier"),
            ("TA0008", "Lateral Movement", "Post-Exploitation", "Expanding control across internal enterprise network")
        ],
        "cwe": [
            ("CWE-1035", "Vulnerability Management and Remediation Standards")
        ],
        "detection": [
            "Maintain comprehensive audit trails of all vulnerability remediation activities and penetration testing engagements.",
            "Establish rules of engagement (RoE) and secure communication channels for immediate disclosure of critical zero-day discoveries.",
            "Deploy continuous red team / blue team adversary emulation exercises (Purple Teaming)."
        ],
        "references": [
            ("[HTB Academy: Introduction to Penetration Testing](https://academy.hackthebox.com/module/90)", "Official Hack The Box curriculum track"),
            ("[Penetration Testing Execution Standard (PTES)](http://www.pentest-standard.org/)", "Standard industry penetration testing workflow"),
            ("[NIST SP 800-115: Technical Guide to Information Security Testing](https://csrc.nist.gov/publications/detail/sp/800-115/final)", "Federal testing standard"),
            ("[OSSTMM 3.0: Open Source Security Testing Methodology Manual](https://www.isecom.org/OSSTMM.3.pdf)", "Scientific security testing framework")
        ]
    },
    "network-enumeration-with-nmap": {
        "mitre": [
            ("T1595.001", "Active Scanning: Scanning IP Blocks", "Reconnaissance", "Subnet host discovery and ping sweeps"),
            ("T1046", "Network Service Discovery", "Discovery", "SYN, TCP connect, and UDP port scans"),
            ("T1018", "Remote System Discovery", "Discovery", "OS detection and service version fingerprinting")
        ],
        "cwe": [
            ("CWE-200", "Information Exposure Through Banner and Network Metadata")
        ],
        "detection": [
            "Configure network intrusion detection systems (Snort/Suricata) to alert on TCP scan signatures (SYN without ACK, FIN, Xmas, Null scans).",
            "Rate-limit ICMP echo requests and drop responses to unexpected network probes at edge firewalls.",
            "Suppress service banner version disclosure in daemon configurations (Apache `ServerTokens Prod`, OpenSSH banners)."
        ],
        "references": [
            ("[HTB Academy: Network Enumeration with Nmap](https://academy.hackthebox.com/module/19)", "Official Hack The Box curriculum track"),
            ("[Nmap Official Documentation & Book](https://nmap.org/book/man.html)", "Authoritative manual for Nmap scanning techniques"),
            ("[Nmap Scripting Engine (NSE) Documentation](https://nmap.org/nsedoc/)", "Official library of NSE automation scripts"),
            ("[RFC 793: Transmission Control Protocol](https://www.ietf.org/rfc/rfc793.txt)", "TCP specifications regarding flag handling")
        ]
    },
    "attacking-web-applications-with-ffuf": {
        "mitre": [
            ("T1595.002", "Active Scanning: Vulnerability Scanning", "Reconnaissance", "Fuzzing web directories, endpoints, and hidden parameters"),
            ("T1083", "File and Directory Discovery", "Discovery", "Discovering unlinked administrative files and backup scripts")
        ],
        "cwe": [
            ("CWE-200", "Information Exposure Through Directory Listing and Discovery"),
            ("CWE-548", "Exposure of Information Through Directory Listing")
        ],
        "detection": [
            "Monitor web server logs for high request-per-second spikes from single IP addresses resulting in high ratios of 404/403 responses.",
            "Deploy rate-limiting reverse proxies (Cloudflare, Nginx `limit_req`) to throttle rapid request streams.",
            "Disable directory listing (`Options -Indexes` in Apache) and remove sensitive backup files (`.bak`, `.old`, `.swp`) from web roots."
        ],
        "references": [
            ("[HTB Academy: Attacking Web Applications with Ffuf](https://academy.hackthebox.com/module/54)", "Official Hack The Box curriculum track"),
            ("[ffuf Official GitHub Repository](https://github.com/ffuf/ffuf)", "Fast web fuzzer implementation and documentation"),
            ("[SecLists Web Discovery Wordlists](https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content)", "Standard wordlists for directory and file discovery"),
            ("[OWASP WSTG: Testing for Directory Traversal / File Inclusion](https://owasp.org/www-project-web-security-testing-guide/)", "Standard testing methodologies")
        ]
    },
    "hacking-wordpress": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Targeting vulnerable WordPress plugins, themes, and core CVEs"),
            ("T1078", "Valid Accounts", "Initial Access", "Logging into `wp-login.php` with brute-forced administrative credentials"),
            ("T1505.003", "Server Software Component: Web Shell", "Persistence", "Modifying theme templates (`404.php`) or uploading malicious plugins to achieve RCE")
        ],
        "cwe": [
            ("CWE-200", "Information Exposure Through WordPress User Enumeration"),
            ("CWE-434", "Unrestricted Upload of File with Dangerous Type"),
            ("CWE-89", "SQL Injection in Plugins")
        ],
        "detection": [
            "Monitor access to `wp-login.php` and `xmlrpc.php` and enforce IP allowlisting or multi-factor authentication.",
            "Disable the built-in theme and plugin file editor by configuring `define('DISALLOW_FILE_EDIT', true);` in `wp-config.php`.",
            "Run continuous vulnerability scans using WPScan or automated CI/CD dependency checkers."
        ],
        "references": [
            ("[HTB Academy: Hacking WordPress](https://academy.hackthebox.com/module/17)", "Official Hack The Box curriculum track"),
            ("[WPScan Vulnerability Database](https://wpscan.com/vulnerabilities)", "Authoritative repository of WordPress core, plugin, and theme vulnerabilities"),
            ("[WordPress Developer Resources: Hardening WordPress](https://wordpress.org/documentation/article/hardening-wordpress/)", "Official WordPress security recommendations"),
            ("[OWASP WordPress Security Implementation](https://owasp.org/www-community/vulnerabilities/WordPress_Security)", "OWASP community guide to WordPress hardening")
        ]
    },
    "cross-site-scripting-xss": {
        "mitre": [
            ("T1189", "Drive-by Compromise", "Initial Access", "Delivering malicious scripts to victim browsers via stored or reflected inputs"),
            ("T1059.007", "Command and Scripting Interpreter: JavaScript", "Execution", "Executing JavaScript in the context of the user's session"),
            ("T1539", "Steal Web Session Cookie", "Credential Access", "Exfiltrating session cookies via `document.cookie`")
        ],
        "cwe": [
            ("CWE-79", "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')")
        ],
        "detection": [
            "Implement a robust Content Security Policy (CSP) with `script-src 'self'` and nonces, disallowing `unsafe-inline` and `unsafe-eval`.",
            "Set the `HttpOnly` cookie flag on all sensitive session cookies to prevent programmatic access via JavaScript.",
            "Apply contextual output encoding (HTML, JavaScript, Attribute, CSS) before rendering dynamic data into HTML documents."
        ],
        "references": [
            ("[HTB Academy: Cross-Site Scripting (XSS)](https://academy.hackthebox.com/module/103)", "Official Hack The Box curriculum track"),
            ("[OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)", "Authoritative remediation guidelines"),
            ("[PortSwigger: Cross-site Scripting (XSS)](https://portswigger.net/web-security/cross-site-scripting)", "Web Security Academy comprehensive tutorials"),
            ("[PayloadsAllTheThings: XSS Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection)", "Modern XSS filter bypasses and payloads")
        ]
    },
    "file-upload-attacks": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Bypassing extension, MIME-type, and magic byte validation"),
            ("T1505.003", "Server Software Component: Web Shell", "Persistence", "Uploading executable web shells (PHP, ASPX, JSP) to web root"),
            ("T1059", "Command and Scripting Interpreter", "Execution", "Executing uploaded scripts via direct HTTP requests")
        ],
        "cwe": [
            ("CWE-434", "Unrestricted Upload of File with Dangerous Type")
        ],
        "detection": [
            "Store uploaded files outside the public web root directory and serve them strictly via an application-level download handler.",
            "Enforce strict file extension allowlists (not blocklists) and re-encode images to strip embedded PHP/polyglot payloads.",
            "Ensure the upload storage directory is mounted with the `noexec` flag and disable script execution handlers."
        ],
        "references": [
            ("[HTB Academy: File Upload Attacks](https://academy.hackthebox.com/module/136)", "Official Hack The Box curriculum track"),
            ("[OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)", "Secure file upload architecture"),
            ("[PortSwigger: File Upload Vulnerabilities](https://portswigger.net/web-security/file-upload)", "Practical testing labs"),
            ("[PayloadsAllTheThings: File Upload](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files)", "Polyglot and extension bypass techniques")
        ]
    },
    "web-attacks": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Targeting web vulnerabilities (CSRF, SSRF, XXE, IDOR)"),
            ("T1552", "Unsecured Credentials", "Credential Access", "Exploiting IDOR to access sensitive user records"),
            ("T1566", "Phishing", "Initial Access", "Leveraging CSRF to force state-changing actions on authenticated users")
        ],
        "cwe": [
            ("CWE-352", "Cross-Site Request Forgery (CSRF)"),
            ("CWE-639", "Authorization Bypass Through User-Controlled Key (IDOR)"),
            ("CWE-918", "Server-Side Request Forgery (SSRF)")
        ],
        "detection": [
            "Enforce anti-CSRF tokens with cryptographic validation and set `SameSite=Lax` or `SameSite=Strict` on session cookies.",
            "Implement indirect reference maps or GUIDs to prevent direct object enumeration in IDOR-susceptible endpoints.",
            "Deploy Web Application Firewalls (WAF) to inspect request anomalies and enforce strict input boundaries."
        ],
        "references": [
            ("[HTB Academy: Web Attacks](https://academy.hackthebox.com/module/134)", "Official Hack The Box curriculum track"),
            ("[OWASP Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)", "Standard CSRF defense"),
            ("[PortSwigger: Insecure Direct Object References (IDOR)](https://portswigger.net/web-security/access-control/idor)", "Web Security Academy IDOR labs"),
            ("[RFC 6454: The Web Origin Concept](https://www.ietf.org/rfc/rfc6454.txt)", "Technical foundation of browser same-origin policies")
        ]
    },
    "session-security": {
        "mitre": [
            ("T1539", "Steal Web Session Cookie", "Credential Access", "Harvesting session tokens via XSS, network sniffing, or log disclosure"),
            ("T1550.004", "Use Alternate Authentication Material: Web Session Cookie", "Defense Evasion", "Replaying valid session tokens to impersonate users"),
            ("T1078", "Valid Accounts", "Initial Access", "Session fixation attacks forcing known session IDs onto victims")
        ],
        "cwe": [
            ("CWE-384", "Session Fixation"),
            ("CWE-613", "Insufficient Session Expiration"),
            ("CWE-614", "Sensitive Cookie in HTTPS Session Without 'Secure' Attribute")
        ],
        "detection": [
            "Always regenerate session IDs upon successful authentication to completely eliminate session fixation risks.",
            "Set `Secure`, `HttpOnly`, and `SameSite` flags on all session cookies.",
            "Enforce idle timeouts and absolute session expirations, and revoke server-side session stores on explicit logout."
        ],
        "references": [
            ("[HTB Academy: Session Security](https://academy.hackthebox.com/module/153)", "Official Hack The Box curriculum track"),
            ("[OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)", "Authoritative session security practices"),
            ("[RFC 6265: HTTP State Management Mechanism](https://www.ietf.org/rfc/rfc6265.txt)", "Official cookie specification"),
            ("[OWASP Application Security Verification Standard (ASVS) - Session Handling](https://owasp.org/www-project-application-security-verification-standard/)", "Standard verification checklist")
        ]
    },
    "cracking-passwords-with-hashcat": {
        "mitre": [
            ("T1110.002", "Brute Force: Password Cracking", "Credential Access", "Accelerated GPU-based password hash cracking"),
            ("T1555", "Credentials from Password Stores", "Credential Access", "Cracking hashes dumped from Active Directory or local shadow files")
        ],
        "cwe": [
            ("CWE-522", "Insufficiently Protected Credentials"),
            ("CWE-328", "Use of Weak Hash")
        ],
        "detection": [
            "Enforce enterprise password filters (e.g., Azure AD Password Protection) to block passwords matching known leaked dictionary entries.",
            "Migrate from legacy NTLM and MD5/SHA1 storage to modern slow-hashing functions (Argon2id, PBKDF2 with high iterations).",
            "Monitor compromised credential repositories (HaveIBeenPwned API) to continuously flag compromised internal user accounts."
        ],
        "references": [
            ("[HTB Academy: Cracking Passwords with Hashcat](https://academy.hackthebox.com/module/20)", "Official Hack The Box curriculum track"),
            ("[Hashcat Official Wiki & Manual](https://hashcat.net/wiki/)", "Complete guide to attack modes (-a 0, 1, 3, 6, 7) and rule files"),
            ("[Hashcat Example Hashes](https://hashcat.net/wiki/doku.php?id=example_hashes)", "List of supported hash modes and formats"),
            ("[NIST SP 800-63B: Password Storage Recommendations](https://pages.nist.gov/800-63-3/sp800-63b.html)", "Standard government guidelines for hash security")
        ]
    },
    "using-the-metasploit-framework": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Executing pre-compiled exploits against remote daemons"),
            ("T1059", "Command and Scripting Interpreter", "Execution", "Deploying Meterpreter stages and executing interactive commands"),
            ("T1021", "Remote Services", "Lateral Movement", "Using PsExec and auxiliary login modules to pivot")
        ],
        "cwe": [
            ("CWE-1035", "Vulnerability Exploitation Framework")
        ],
        "detection": [
            "Monitor network traffic for known Meterpreter default communication patterns and TLS certificate fingerprints.",
            "Sysmon Event ID 1: Alert on processes spawning from abnormal binaries or executing typical Meterpreter migration targets (`explorer.exe`, `svchost.exe`).",
            "Keep systems patched against known CVEs indexed in the Metasploit module repository."
        ],
        "references": [
            ("[HTB Academy: Using the Metasploit Framework](https://academy.hackthebox.com/module/39)", "Official Hack The Box curriculum track"),
            ("[Metasploit Unleashed (Offensive Security)](https://www.offensive-security.com/metasploit-unleashed/)", "Free comprehensive Metasploit training guide"),
            ("[Rapid7 Metasploit Documentation](https://docs.rapid7.com/metasploit/)", "Official Rapid7 documentation"),
            ("[Metasploit Framework GitHub Repository](https://github.com/rapid7/metasploit-framework)", "Source code and module contributions")
        ]
    },
    "using-crackmapexec": {
        "mitre": [
            ("T1021.002", "Remote Services: SMB/Windows Admin Shares", "Lateral Movement", "Executing commands across hosts via SMB"),
            ("T1078", "Valid Accounts", "Initial Access / Persistence", "Testing credentials across broad network ranges (Password Spraying)"),
            ("T1003", "OS Credential Dumping", "Credential Access", "Dumping LSA secrets, SAM, and NTDS.dit hashes via CME")
        ],
        "cwe": [
            ("CWE-287", "Improper Authentication"),
            ("CWE-269", "Improper Privilege Management in Windows Environments")
        ],
        "detection": [
            "Windows Event ID 4624 (Type 3 network logon) occurring in rapid succession across multiple workstations from a single source IP.",
            "Deploy SMB signing requirements across all workstations and servers to block relay attacks.",
            "Disable Local Administrator account re-use across workstations (deploy Microsoft LAPS)."
        ],
        "references": [
            ("[HTB Academy: Using CrackMapExec](https://academy.hackthebox.com/module/98)", "Official Hack The Box curriculum track"),
            ("[NetExec (Next Generation CrackMapExec) Documentation](https://www.netexec.org/)", "Modern fork and documentation of CME capabilities"),
            ("[Impacket Library Repository](https://github.com/fortra/impacket)", "Underlying Python library powering network protocols"),
            ("[Microsoft LAPS Deployment Guide](https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview)", "Local Administrator Password Solution")
        ]
    },
    "stack-based-buffer-overflows-on-linux-x86": {
        "mitre": [
            ("T1203", "Exploitation for Client Execution", "Execution", "Corrupting stack frames to overwrite EIP register"),
            ("T1068", "Exploitation for Privilege Escalation", "Privilege Escalation", "Executing shellcode in SUID context to spawn root shell")
        ],
        "cwe": [
            ("CWE-121", "Stack-based Buffer Overflow"),
            ("CWE-676", "Use of Potentially Dangerous Function (`strcpy`, `gets`, `sprintf`)")
        ],
        "detection": [
            "Compile binaries with modern compiler defenses: Stack Canaries (`-fstack-protector-all`), ASLR, and Non-Executable Stack (`NX`/`-z noexecstack`).",
            "Monitor Linux coredump events in system logs (`/var/log/messages`, `dmesg`) for `SIGSEGV` segmentation faults in critical binaries.",
            "Adopt memory-safe programming languages (Rust, Go) or safe string handling functions (`strncpy`, `snprintf`)."
        ],
        "references": [
            ("[HTB Academy: Stack-Based Buffer Overflows on Linux x86](https://academy.hackthebox.com/module/31)", "Official Hack The Box curriculum track"),
            ("[Aleph One: Smashing The Stack For Fun And Profit](http://phrack.org/issues/49/14.html)", "Foundational Phrack paper on stack overflow mechanics"),
            ("[GDB GEF / Pwndbg Exploit Development Plugins](https://github.com/hugsy/gef)", "GDB enhancements for vulnerability research"),
            ("[Corelan Team Exploit Writing Series](https://www.corelan.be/)", "Premier binary exploitation tutorials")
        ]
    },
    "stack-based-buffer-overflows-on-windows-x86": {
        "mitre": [
            ("T1203", "Exploitation for Client Execution", "Execution", "Overwriting Extended Instruction Pointer (EIP) or Structured Exception Handler (SEH)"),
            ("T1068", "Exploitation for Privilege Escalation", "Privilege Escalation", "Executing shellcode to spawn elevated process")
        ],
        "cwe": [
            ("CWE-121", "Stack-based Buffer Overflow"),
            ("CWE-120", "Buffer Copy without Checking Size of Input")
        ],
        "detection": [
            "Enable Windows exploit mitigations system-wide: Data Execution Prevention (DEP), Address Space Layout Randomization (ASLR), and SafeSEH.",
            "Audit application crashes via Windows Event ID 1000 (Application Error) with exception code `0xc0000005` (Access Violation).",
            "Deploy Microsoft Exploit Guard to enforce runtime mitigation policies on legacy unmanaged binaries."
        ],
        "references": [
            ("[HTB Academy: Stack-Based Buffer Overflows on Windows x86](https://academy.hackthebox.com/module/32)", "Official Hack The Box curriculum track"),
            ("[Corelan Team: Exploit Writing Tutorial Part 1 (Stack Based Overflow)](https://www.corelan.be/index.php/2009/07/19/exploit-writing-tutorial-part-1-stack-based-overflows/)", "Authoritative Windows stack overflow guide"),
            ("[Mona.py Plugin for Immunity Debugger / x64dbg](https://github.com/corelan/mona)", "Corelan automation script for finding jumps and bad characters"),
            ("[Microsoft Security: Exploit Protection Documentation](https://learn.microsoft.com/en-us/defender-endpoint/exploit-protection)", "Windows platform defenses")
        ]
    },
    "attacking-wifi-protected-setup-wps": {
        "mitre": [
            ("T1110", "Brute Force", "Credential Access", "Brute-forcing 8-digit WPS PIN in halves (10,000 + 1,000 combinations)"),
            ("T1040", "Network Sniffing", "Credential Access", "Capturing EAP-WSC authentication frames")
        ],
        "cwe": [
            ("CWE-330", "Use of Insufficiently Random Values"),
            ("CWE-307", "Improper Restriction of Excessive Authentication Attempts")
        ],
        "detection": [
            "Permanently disable Wi-Fi Protected Setup (WPS) on all wireless access points and routers.",
            "Deploy Wireless Intrusion Prevention Systems (WIPS) that detect anomalous EAP-WSC exchanges and alert on PIN brute force attempts.",
            "Migrate wireless infrastructure to WPA3-Enterprise using 802.1X EAP-TLS authentication."
        ],
        "references": [
            ("[HTB Academy: Attacking Wi-Fi Protected Setup (WPS)](https://academy.hackthebox.com/module/131)", "Official Hack The Box curriculum track"),
            ("[Stefan Viehböck: Brute Forcing Wi-Fi Protected Setup](https://sviehb.files.wordpress.com/2011/12/viehboeck_wps.pdf)", "Original research paper detailing the WPS PIN vulnerability"),
            ("[Reaver-wps-fork GitHub Repository](https://github.com/t6x/reaver-wps-fork-t6x)", "Community tool for WPS security auditing"),
            ("[Wi-Fi Alliance WPA3 Specification](https://www.wi-fi.org/discover-wi-fi/security)", "Modern Wi-Fi security standards")
        ]
    },
    "web-fuzzing": {
        "mitre": [
            ("T1595.002", "Active Scanning: Vulnerability Scanning", "Reconnaissance", "Fuzzing endpoints, directories, headers, and JSON/XML keys"),
            ("T1083", "File and Directory Discovery", "Discovery", "Locating hidden administrative surfaces and staging environments")
        ],
        "cwe": [
            ("CWE-200", "Information Exposure Through Direct Request"),
            ("CWE-548", "Exposure of Information Through Directory Listing")
        ],
        "detection": [
            "Implement rate-limiting rules at the API gateway or reverse proxy to throttle burst HTTP requests.",
            "Monitor web access logs for cyclical 404, 403, and 500 error spikes originating from single client signatures.",
            "Enforce standardized routing policies that return uniform 404 responses for all non-existent paths, preventing content differentiation."
        ],
        "references": [
            ("[HTB Academy: Web Fuzzing](https://academy.hackthebox.com/module/188)", "Official Hack The Box curriculum track"),
            ("[ffuf GitHub Repository](https://github.com/ffuf/ffuf)", "Fast web fuzzer implementation"),
            ("[wfuzz Documentation](https://wfuzz.readthedocs.io/)", "Python web application fuzzer manual"),
            ("[SecLists Project](https://github.com/danielmiessler/SecLists)", "Standard collections of fuzzing wordlists")
        ]
    },
    "web-service-and-api-attacks": {
        "mitre": [
            ("T1190", "Exploit Public-Facing Application", "Initial Access", "Targeting SOAP XML and REST endpoints with injection and deserialization"),
            ("T1059", "Command and Scripting Interpreter", "Execution", "Achieving remote command execution through API payload handling")
        ],
        "cwe": [
            ("CWE-611", "Improper Restriction of XML External Entity Reference (XXE)"),
            ("CWE-918", "Server-Side Request Forgery (SSRF)"),
            ("CWE-89", "SQL Injection in Web Services")
        ],
        "detection": [
            "Disable XML external entity parsing across all SOAP web service endpoints and XML parsers.",
            "Deploy API gateways (Kong, Apigee) that enforce strict JSON/XML schema validation before routing requests to backend services.",
            "Implement mutual TLS (mTLS) for internal microservice-to-microservice API communication."
        ],
        "references": [
            ("[HTB Academy: Web Service & API Attacks](https://academy.hackthebox.com/module/161)", "Official Hack The Box curriculum track"),
            ("[OWASP API Security Top 10 2023](https://owasp.org/API-Security/)", "Official standard for API vulnerabilities"),
            ("[W3C SOAP 1.2 Specification](https://www.w3.org/TR/soap12-part1/)", "Official SOAP messaging framework specification"),
            ("[PortSwigger: Web Service Vulnerabilities](https://portswigger.net/web-security/api-testing)", "Interactive testing guides")
        ]
    },
    "wifi-penetration-testing-basics": {
        "mitre": [
            ("T1040", "Network Sniffing", "Credential Access", "Capturing 802.11 beacon, probe, and 4-way handshake frames"),
            ("T1557", "Adversary-in-the-Middle", "Credential Access", "Rogue Access Points and Evil Twin credential harvesting")
        ],
        "cwe": [
            ("CWE-319", "Cleartext Transmission of Sensitive Information"),
            ("CWE-287", "Improper Authentication in Wireless Protocols")
        ],
        "detection": [
            "Deploy Wireless Intrusion Detection Systems (WIDS) to monitor for deauthentication frame floods (`aireplay-ng -0`).",
            "Monitor for duplicate BSSIDs or rogue APs broadcasting identical SSIDs with stronger signal strengths.",
            "Transition wireless infrastructure to WPA3-Enterprise with protected management frames (802.11w) enforced."
        ],
        "references": [
            ("[HTB Academy: Wi-Fi Penetration Testing Basics](https://academy.hackthebox.com/module/130)", "Official Hack The Box curriculum track"),
            ("[Aircrack-ng Official Suite Documentation](https://www.aircrack-ng.org/doku.php)", "Complete documentation for airodump-ng, aireplay-ng, and aircrack-ng"),
            ("[Wireshark 802.11 Wireless Capture Guide](https://wiki.wireshark.org/CaptureSetup/WLAN)", "Network packet capture and frame analysis"),
            ("[IEEE 802.11 Wireless LAN Standards](https://standards.ieee.org/ieee/802.11/)", "Official standard specifications")
        ]
    },
    "wired-equivalent-privacy-wep-attacks": {
        "mitre": [
            ("T1040", "Network Sniffing", "Credential Access", "Capturing weak Initialization Vectors (IVs) via ARP request replay"),
            ("T1557", "Adversary-in-the-Middle", "Credential Access", "Decrypting RC4 keystreams and recovering WEP root key")
        ],
        "cwe": [
            ("CWE-327", "Use of a Broken or Risky Cryptographic Algorithm (RC4 in WEP)"),
            ("CWE-328", "Use of Weak Hash / 24-bit Initialization Vector")
        ],
        "detection": [
            "Completely decommission and ban WEP encryption across all legacy enterprise and consumer wireless hardware.",
            "Deploy 802.1X network access control with dynamic encryption keys generated per session (EAP-TLS/PEAP).",
            "Monitor RF spectrum for high-frequency ARP packet injection attacks (`aireplay-ng -3`)."
        ],
        "references": [
            ("[HTB Academy: Wired Equivalent Privacy (WEP) Attacks](https://academy.hackthebox.com/module/132)", "Official Hack The Box curriculum track"),
            ("[Fluhrer, Mantin, Shamir (FMS) Attack on WEP](https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf)", "Foundational cryptanalytic attack on RC4 key scheduling"),
            ("[Aircrack-ng PTW Attack Documentation](https://www.aircrack-ng.org/doku.php?id=ptw)", "Pyshkin, Tews, Weinmann fast WEP key recovery paper"),
            ("[IEEE 802.11i Security Amendment](https://standards.ieee.org/)", "Standard deprecating WEP in favor of WPA/WPA2/WPA3")
        ]
    }
}

post_files = sorted(glob.glob('_posts/*-htb-academy-*.md'))
print(f"Total HTB posts to enrich: {len(post_files)}")

updated_count = 0

for pf in post_files:
    fname = os.path.basename(pf)
    # Extract module key: 2026-11-12-htb-academy-part-1-getting-started.md -> getting-started
    m = re.search(r'htb-academy-part-\d+-(.+)\.md$', fname)
    if not m:
        print(f"Skipping {fname}, cannot match pattern")
        continue
    slug = m.group(1)
    
    if slug not in MODULE_ENRICHMENTS:
        print(f"Warning: slug {slug} not found in MODULE_ENRICHMENTS!")
        continue
        
    data = MODULE_ENRICHMENTS[slug]
    
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if already enriched with MITRE
    if "## MITRE ATT&CK Mapping & Threat Matrix" in content:
        print(f"Already enriched: {fname}")
        continue
        
    # Build MITRE Table
    mitre_table = "| Technique ID | Technique Name | Tactic | Applied Offensive / Defensive Context |\n"
    mitre_table += "| :--- | :--- | :--- | :--- |\n"
    for tech_id, tech_name, tactic, ctx in data["mitre"]:
        mitre_url = f"https://attack.mitre.org/techniques/{tech_id.split('.')[0]}/"
        mitre_table += f"| [`{tech_id}`]({mitre_url}) | **{tech_name}** | `{tactic}` | {ctx} |\n"
        
    # Build CWE list
    cwe_list = ""
    for cwe_id, cwe_name in data["cwe"]:
        cwe_num = cwe_id.replace("CWE-", "")
        cwe_url = f"https://cwe.mitre.org/data/definitions/{cwe_num}.html"
        cwe_list += f"- [`{cwe_id}`: {cwe_name}]({cwe_url})\n"
        
    # Build Detection list
    detection_list = ""
    for d in data["detection"]:
        detection_list += f"- {d}\n"
        
    # Build References list
    refs_list = ""
    for label, desc in data["references"]:
        refs_list += f"- {label} — *{desc}*\n"
        
    enrichment_section = f"""

---

## MITRE ATT&CK Mapping & Threat Matrix

| Security Domain | Mapping Specification |
| :--- | :--- |
| **Primary Tactic** | Enterprise Penetration Testing & Adversary Simulation |
| **Mitre Techniques** | `{', '.join([t[0] for t in data['mitre']])}` |
| **Common Weakness Enumerations** | `{', '.join([c[0] for c in data['cwe']])}` |

### Adversary Tradecraft & Technique Breakdown

{mitre_table}

### Identified Common Weakness Enumerations (CWE)

{cwe_list}

---

## Detection Engineering & Defensive Countermeasures

Modern enterprise security programs must implement proactive, layered defense-in-depth controls to detect and mitigate the techniques covered in this module:

{detection_list}

---

## Authoritative References & Recommended Reading

{refs_list}
"""

    # We want to insert this enrichment section right before the final series nav or right before the end
    # Let's check where to place it: usually before the last `<div class="ff-series-nav">`
    if '<div class="ff-series-nav">' in content:
        # Find the last occurrence
        parts = content.rsplit('<div class="ff-series-nav">', 1)
        # Check if Enterprise Defense was already there
        # We can place it before or after Enterprise Defense
        new_content = parts[0].rstrip() + "\n" + enrichment_section + "\n" + '<div class="ff-series-nav">' + parts[1]
    else:
        new_content = content + "\n" + enrichment_section

    with open(pf, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    updated_count += 1

print(f"Successfully enriched {updated_count} HTB posts with MITRE ATT&CK, CWEs, Detection, and Authoritative References!")

