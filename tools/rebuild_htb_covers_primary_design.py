import os
from PIL import Image, ImageDraw, ImageFont

out_dir = 'assets/images/posts/htb-academy'
os.makedirs(out_dir, exist_ok=True)

# Load Fonts matching tools/rebuild_all_covers.py exactly
FONT_TITLE = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 42)
FONT_SUB = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
FONT_BADGE = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 13)
FONT_PILL = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14)
FONT_AUTHOR = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17)
FONT_AUTHOR_SUB = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def render_primary_cover(data):
    w, h = 1200, 630
    img = Image.new('RGBA', (w, h), (10, 13, 19, 255)) # Deep carbon dark
    draw = ImageDraw.Draw(img)
    
    accent = data['accent']
    
    # 1. Subtle Background Grid (48px spacing)
    for x in range(0, w, 48):
        draw.line([(x, 0), (x, h)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, h, 48):
        draw.line([(0, y), (w, y)], fill=(255, 255, 255, 6), width=1)
        
    # 2. Ambient Glow in top right corner
    glow_center = (w - 150, 80)
    for r in range(250, 0, -25):
        alpha = int(14 * (1 - r / 250))
        draw.ellipse([
            (glow_center[0] - r, glow_center[1] - r),
            (glow_center[0] + r, glow_center[1] + r)
        ], fill=(accent[0], accent[1], accent[2], alpha))
        
    # 3. Top Accent Line (Smooth gradient)
    for i in range(4):
        draw.line([(0, i), (w, i)], fill=(accent[0], accent[1], accent[2], 255 - i * 50), width=1)
        
    # 4. Header Row: Badge (Left) & Domain Tag (Right)
    badge = data['badge']
    b_bbox = draw.textbbox((0, 0), badge, font=FONT_BADGE)
    bw = b_bbox[2] - b_bbox[0] + 24
    bh = 28
    draw.rounded_rectangle([(70, 48), (70 + bw, 48 + bh)], radius=5, 
                           fill=(accent[0], accent[1], accent[2], 25), 
                           outline=(accent[0], accent[1], accent[2], 140), width=1)
    draw.text((82, 54), badge, fill=accent, font=FONT_BADGE)
    
    domain_text = "3bdo-fathi.github.io"
    d_bbox = draw.textbbox((0, 0), domain_text, font=FONT_BADGE)
    dw = d_bbox[2] - d_bbox[0] + 20
    draw.rounded_rectangle([(w - 70 - dw, 48), (w - 70, 48 + bh)], radius=5, 
                           fill=(255, 255, 255, 8), outline=(255, 255, 255, 25), width=1)
    draw.text((w - 70 - dw + 10, 54), domain_text, fill=(148, 163, 184, 255), font=FONT_BADGE)
    
    # 5. Kicker
    kicker = data['kicker'].upper()
    draw.text((70, 108), kicker, fill=(148, 163, 184, 255), font=FONT_BADGE)
    
    # 6. Main Title
    title_lines = wrap_text(data['title'], FONT_TITLE, 1060, draw)
    cur_y = 138
    for line in title_lines[:2]:
        draw.text((70, cur_y), line, fill=(248, 250, 252, 255), font=FONT_TITLE)
        cur_y += 52
        
    # 7. Tagline
    cur_y += 8
    desc_lines = wrap_text(data['tagline'], FONT_SUB, 1060, draw)
    for line in desc_lines[:2]:
        draw.text((70, cur_y), line, fill=(148, 163, 184, 255), font=FONT_SUB)
        cur_y += 28
        
    # 8. Technical Topic Pills (py = 412)
    py = 412
    px = 70
    for pill in data['pills']:
        p_bbox = draw.textbbox((0, 0), pill, font=FONT_PILL)
        pw = p_bbox[2] - p_bbox[0] + 26
        ph = 34
        if px + pw > w - 70:
            break
        draw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=17, 
                               fill=(255, 255, 255, 10), outline=(255, 255, 255, 35), width=1)
        draw.text((px + 13, py + 8), pill, fill=(226, 232, 240, 255), font=FONT_PILL)
        px += pw + 10
        
    # 9. Bottom Divider Line
    draw.line([(70, 520), (w - 70, 520)], fill=(255, 255, 255, 25), width=1)
    
    # 10. Standardized Author Signature
    author_name = "Abdulrahman M. Fathi"
    draw.text((70, 544), author_name, fill=(241, 245, 249, 255), font=FONT_AUTHOR)
    
    author_name_w = draw.textbbox((0, 0), author_name, font=FONT_AUTHOR)[2]
    author_sub = " • 0x3bdo | Cyber Security Engineer & Penetration Tester"
    draw.text((70 + author_name_w, 546), author_sub, fill=(100, 116, 139, 255), font=FONT_AUTHOR_SUB)
    
    tag = data.get('footer_tag', "HTB ACADEMY WRITEUP")
    tw = draw.textbbox((0, 0), tag, font=FONT_BADGE)[2]
    draw.text((w - 70 - tw, 547), tag, fill=(100, 116, 139, 255), font=FONT_BADGE)
    
    img.save(data['out_path'])
    print(f"Generated Primary Cover: {data['out_path']}")

# 41 Modules Catalog matching primary design
ALL_COVERS = [
    {
        "out_path": f"{out_dir}/getting-started-cover.png",
        "badge": "HTB ACADEMY • PART 1",
        "kicker": "HACK THE BOX ACADEMY • PENETRATION TESTING FUNDAMENTALS",
        "title": "Getting Started: Methodology, Nmap, Nibbles & PrivEsc",
        "tagline": "Core pentesting stages, service discovery, web exploitation, Metasploit, Linux/Windows privilege escalation, and lab flags.",
        "pills": ["Nmap Recon", "Nibbles Exploitation", "Sudo Environment PrivEsc", "Metasploit Console", "Lab Flags Solved"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "CPTS CURRICULUM"
    },
    {
        "out_path": f"{out_dir}/file-transfers-cover.png",
        "badge": "HTB ACADEMY • PART 2",
        "kicker": "HACK THE BOX ACADEMY • OFFENSIVE FILE DELIVERY",
        "title": "File Transfers: Living-off-the-Land Ingress & Egress",
        "tagline": "PowerShell WebClient, IWR, Certutil, BITS, Python HTTP/FTP daemons, cURL, Wget, and RDP drive redirection.",
        "pills": ["PowerShell WebClient", "BITS Admin", "Python HTTP Daemons", "cURL & Wget", "RDP Drive Redirection"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "OFFENSIVE PLAYBOOK"
    },
    {
        "out_path": f"{out_dir}/information-gathering-web-edition-cover.png",
        "badge": "HTB ACADEMY • PART 3",
        "kicker": "HACK THE BOX ACADEMY • WEB RECONNAISSANCE & OSINT",
        "title": "Information Gathering: Web Edition & Reconnaissance",
        "tagline": "WHOIS registries, DNS zone transfers (AXFR), subdomain discovery, virtual host routing, and certificate transparency.",
        "pills": ["DNS AXFR Zone Transfers", "Virtual Host Fuzzing", "Certificate Transparency", "WHOIS & Passive OSINT"],
        "accent": (14, 165, 233, 255), # Sky blue
        "footer_tag": "WEB RECONNAISSANCE"
    },
    {
        "out_path": f"{out_dir}/footprinting-cover.png",
        "badge": "HTB ACADEMY • PART 4",
        "kicker": "HACK THE BOX ACADEMY • SERVICE FOOTPRINTING",
        "title": "Footprinting: External Infrastructure & Daemon Audit",
        "tagline": "In-depth service enumeration across FTP, SMB, NFS, DNS, SMTP, IMAP/POP3, SNMP, MySQL, MSSQL, Oracle TNS, and IPMI.",
        "pills": ["SMB & RPC Null Sessions", "NFS Share Mounting", "SNMP MIB Enumeration", "Database Footprinting"],
        "accent": (245, 158, 11, 255), # Amber
        "footer_tag": "INFRASTRUCTURE AUDIT"
    },
    {
        "out_path": f"{out_dir}/linux-privilege-escalation-cover.png",
        "badge": "HTB ACADEMY • PART 5",
        "kicker": "HACK THE BOX ACADEMY • LOCAL PRIVILEGE ESCALATION",
        "title": "Linux Privilege Escalation: SUID, Sudo & Capabilities",
        "tagline": "PATH hijacking, SUID/SGID binaries, Linux capabilities (cap_setuid), Screen exploits, Logrotate race, and PwnKit.",
        "pills": ["SUID Exploitation & GTFOBins", "Linux Capabilities", "Docker Escape", "CVE-2021-4034 PwnKit"],
        "accent": (16, 185, 129, 255), # Emerald
        "footer_tag": "HOST EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/login-brute-forcing-cover.png",
        "badge": "HTB ACADEMY • PART 6",
        "kicker": "HACK THE BOX ACADEMY • AUTHENTICATION ATTACKS",
        "title": "Login Brute Forcing with Hydra & Custom Dictionaries",
        "tagline": "Service fuzzing against SSH, FTP, and RDP, HTTP GET/POST form brute-forcing, CeWL profiling, and Burp Intruder.",
        "pills": ["THC Hydra Multi-Threading", "CeWL Wordlist Profiling", "HTTP Form Brute-Forcing", "Burp Suite Intruder"],
        "accent": (239, 68, 68, 255), # Red
        "footer_tag": "CREDENTIAL ATTACKS"
    },
    {
        "out_path": f"{out_dir}/broken-authentication-cover.png",
        "badge": "HTB ACADEMY • PART 7",
        "kicker": "HACK THE BOX ACADEMY • WEB APPLICATION SECURITY",
        "title": "Broken Authentication: Session & Token Exploitation",
        "tagline": "Cookie tampering, session hijacking, JWT attacks (none algorithm, secret cracking), 2FA bypasses, and reset poisoning.",
        "pills": ["JWT Algorithm None", "HMAC Secret Cracking", "2FA Rate-Limit Bypass", "Session Fixation"],
        "accent": (168, 85, 247, 255), # Purple
        "footer_tag": "APPSEC RESEARCH"
    },
    {
        "out_path": f"{out_dir}/command-injections-cover.png",
        "badge": "HTB ACADEMY • PART 8",
        "kicker": "HACK THE BOX ACADEMY • REMOTE CODE EXECUTION",
        "title": "Command Injections: Filter Evasion & Obfuscation",
        "tagline": "OS command injection delimiters, newline injection, space bypasses using ${IFS} and brace expansion, and env slicing.",
        "pills": ["Operator Delimiters (|, ;, \\n)", "Brace Expansion {cat,/etc/passwd}", "Env Slicing ${PATH:0:1}", "Base64 Piping"],
        "accent": (244, 63, 94, 255), # Rose
        "footer_tag": "RCE PLAYBOOK"
    },
    {
        "out_path": f"{out_dir}/file-inclusion-cover.png",
        "badge": "HTB ACADEMY • PART 9",
        "kicker": "HACK THE BOX ACADEMY • WEB APPLICATION ATTACKS",
        "title": "File Inclusion: LFI, RFI, PHP Wrappers & Poisoning",
        "tagline": "Directory traversal bypasses, PHP filter and data wrappers, Remote File Inclusion to RCE, Apache/SSH log poisoning.",
        "pills": ["php://filter Base64", "Log Poisoning to RCE", "PHP Session Poisoning", "Remote File Inclusion"],
        "accent": (234, 88, 12, 255), # Orange
        "footer_tag": "WEB EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/attacking-common-services-cover.png",
        "badge": "HTB ACADEMY • PART 10",
        "kicker": "HACK THE BOX ACADEMY • SERVICE COMPROMISE",
        "title": "Attacking Common Services: SMB, SQL, RDP & SSH",
        "tagline": "Anonymous SMB write abuse, FTP bounce attacks, MSSQL xp_cmdshell execution, MySQL UDF exploitation, and RDP hijacking.",
        "pills": ["SMB Share Abuse", "MSSQL xp_cmdshell RCE", "MySQL UDF Injection", "SSH Credential Reuse"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "SERVICE COMPROMISE"
    },
    {
        "out_path": f"{out_dir}/attacking-common-applications-cover.png",
        "badge": "HTB ACADEMY • PART 11",
        "kicker": "HACK THE BOX ACADEMY • ENTERPRISE APPSEC",
        "title": "Attacking Common Applications: Tomcat, Jenkins, Splunk",
        "tagline": "Apache Tomcat Manager WAR deployment RCE, Jenkins Groovy console exploitation, Splunk app packaging, and GitLab CVE.",
        "pills": ["Tomcat WAR Deployment", "Jenkins Groovy Script RCE", "Splunk App Packaging", "GitLab CVE-2021-22205"],
        "accent": (236, 72, 153, 255), # Pink
        "footer_tag": "ENTERPRISE APPSEC"
    },
    {
        "out_path": f"{out_dir}/active-directory-enumeration-and-attacks-cover.png",
        "badge": "HTB ACADEMY • PART 12",
        "kicker": "HACK THE BOX ACADEMY • ACTIVE DIRECTORY DOMINANCE",
        "title": "Active Directory Attacks: Kerberoasting, ACLs & DCSync",
        "tagline": "BloodHound attack path modeling, PowerView enumeration, Responder poisoning, Kerberoasting, AS-REP Roasting, and DCSync.",
        "pills": ["BloodHound Graph Analysis", "Kerberoasting & AS-REP", "GenericAll & WriteDacl ACLs", "DCSync & Pass-the-Hash"],
        "accent": (220, 38, 38, 255), # Red-orange
        "footer_tag": "DOMAIN DOMINANCE"
    },
    {
        "out_path": f"{out_dir}/attacking-enterprise-networks-cover.png",
        "badge": "HTB ACADEMY • PART 13",
        "kicker": "HACK THE BOX ACADEMY • ENTERPRISE RED TEAM",
        "title": "Attacking Enterprise Networks: Pivoting & Forest Compromise",
        "tagline": "Perimeter breach, multi-tiered pivoting with Chisel/Ligolo-ng, dual-homed routing, and cross-forest trust dominance.",
        "pills": ["Multi-Tier Pivoting", "Chisel & Ligolo-ng", "Dual-Homed Routing", "Forest Trust Exploitation"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "RED TEAM CAPSTONE"
    },
    {
        "out_path": f"{out_dir}/using-web-proxies-cover.png",
        "badge": "HTB ACADEMY • PART 14",
        "kicker": "HACK THE BOX ACADEMY • WEB PROXIES & TRAFFIC ANALYSIS",
        "title": "Using Web Proxies: Burp Suite & OWASP ZAP Playbook",
        "tagline": "Configuring interception proxies, scope management, Repeater request manipulation, and Intruder attack types.",
        "pills": ["Burp Repeater Workflows", "Intruder Attack Modes", "Scope & Target Mapping", "OWASP ZAP Integration"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "WEB PROXIES"
    },
    {
        "out_path": f"{out_dir}/vulnerability-assessment-cover.png",
        "badge": "HTB ACADEMY • PART 15",
        "kicker": "HACK THE BOX ACADEMY • VULNERABILITY MANAGEMENT",
        "title": "Vulnerability Assessment: Scanners, CVSS & Triage",
        "tagline": "Automated scanning methodologies, Nessus and OpenVAS workflows, false-positive elimination, and CVSS v3 calculation.",
        "pills": ["Nessus Automated Scans", "CVSS v3 Vector Metrics", "Vulnerability Triage", "Reporting & Remediation"],
        "accent": (59, 130, 246, 255), # Blue
        "footer_tag": "ASSESSMENT METHODOLOGY"
    },
    {
        "out_path": f"{out_dir}/shells-and-payloads-cover.png",
        "badge": "HTB ACADEMY • PART 16",
        "kicker": "HACK THE BOX ACADEMY • PAYLOAD WEAPONIZATION",
        "title": "Shells & Payloads: Reverse, Bind & Web Shell Delivery",
        "tagline": "Reverse vs bind shell mechanics, TTY stabilization, MSFvenom payload generators, multi-handlers, and Socat relays.",
        "pills": ["Reverse & Bind Shells", "MSFvenom Generation", "TTY Fully Interactive", "Socat Encrypted Relays"],
        "accent": (16, 185, 129, 255),
        "footer_tag": "OFFENSIVE PLAYBOOK"
    },
    {
        "out_path": f"{out_dir}/sql-injection-fundamentals-cover.png",
        "badge": "HTB ACADEMY • PART 17",
        "kicker": "HACK THE BOX ACADEMY • DATABASE EXPLOITATION",
        "title": "SQL Injection Fundamentals: UNION, Error & Blind Attacks",
        "tagline": "In-band UNION attacks, determining column counts, database schema fingerprinting, file reading, and INTO OUTFILE shells.",
        "pills": ["UNION-Based Injection", "Database Fingerprinting", "Arbitrary File Read/Write", "INTO OUTFILE Web Shells"],
        "accent": (239, 68, 68, 255),
        "footer_tag": "DATABASE EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/sqlmap-essentials-cover.png",
        "badge": "HTB ACADEMY • PART 18",
        "kicker": "HACK THE BOX ACADEMY • AUTOMATED EXPLOITATION",
        "title": "SQLMap Essentials: Automated Database & OS Takeover",
        "tagline": "Target crawling, tamper scripts for WAF evasion, schema dumping, hash extraction, and interactive OS command shells.",
        "pills": ["Automated Injection", "WAF Bypass Tamper Scripts", "Database Enumeration", "--os-shell Execution"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "AUTOMATED TOOLING"
    },
    {
        "out_path": f"{out_dir}/password-attacks-cover.png",
        "badge": "HTB ACADEMY • PART 19",
        "kicker": "HACK THE BOX ACADEMY • CREDENTIAL EXTRACTION",
        "title": "Password Attacks: SAM, LSASS, Hashcat & John",
        "tagline": "Windows SAM/LSASS memory dumping, Linux shadow cracking, rule-based Hashcat attacks, John the Ripper, and mutating rules.",
        "pills": ["LSASS Memory Dumping", "SAM Database Secrets", "Hashcat Rule-Based Attacks", "John The Ripper"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "CREDENTIAL ATTACKS"
    },
    {
        "out_path": f"{out_dir}/server-side-attacks-cover.png",
        "badge": "HTB ACADEMY • PART 20",
        "kicker": "HACK THE BOX ACADEMY • SERVER-SIDE VULNERABILITIES",
        "title": "Server-Side Attacks: SSRF, SSTI & XXE Exploitation",
        "tagline": "Server-Side Request Forgery against cloud metadata, Server-Side Template Injection to RCE, and XXE data exfiltration.",
        "pills": ["SSRF Cloud Metadata", "SSTI Jinja2 / Twig RCE", "XXE External Entity DTD", "Out-of-Band Exfiltration"],
        "accent": (244, 63, 94, 255),
        "footer_tag": "WEB EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/windows-privilege-escalation-cover.png",
        "badge": "HTB ACADEMY • PART 21",
        "kicker": "HACK THE BOX ACADEMY • WINDOWS PRIVILEGE ESCALATION",
        "title": "Windows Privilege Escalation: Token Abuse & Services",
        "tagline": "SeImpersonate token abuse (PrintSpoofer, GodPotato), unquoted service paths, weak DACLs, silent UAC bypasses, and DLL hijacking.",
        "pills": ["Potato Exploit Family", "Unquoted Service Paths", "Silent UAC Bypasses", "AlwaysInstallElevated MSI"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "HOST EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/pivoting-tunneling-and-port-forwarding-cover.png",
        "badge": "HTB ACADEMY • PART 22",
        "kicker": "HACK THE BOX ACADEMY • LATERAL MOVEMENT & PIVOTING",
        "title": "Pivoting, Tunneling & Port Forwarding Masterclass",
        "tagline": "SSH local/remote/dynamic port forwarding, Proxychains SOCKS integration, Chisel HTTP tunnels, and Ligolo-ng TUN interfaces.",
        "pills": ["SSH Port Forwarding", "Dynamic SOCKS Proxies", "Chisel Reverse Tunnels", "Ligolo-ng Virtual TUN"],
        "accent": (6, 182, 212, 255),
        "footer_tag": "NETWORK PIVOTING"
    },
    {
        "out_path": f"{out_dir}/api-attacks-cover.png",
        "badge": "HTB ACADEMY • PART 23",
        "kicker": "HACK THE BOX ACADEMY • API SECURITY & RECON",
        "title": "Web Service & API Attacks: REST, GraphQL & SOAP",
        "tagline": "REST API reconnaissance, GraphQL schema introspection, batching attacks, SOAP XML injection, and IDOR vulnerabilities.",
        "pills": ["REST Endpoint Auditing", "GraphQL Introspection", "IDOR & Broken Access", "Mass Assignment"],
        "accent": (147, 51, 234, 255),
        "footer_tag": "API SECURITY"
    },
    {
        "out_path": f"{out_dir}/introduction-to-penetration-testing-cover.png",
        "badge": "HTB ACADEMY • PART 24",
        "kicker": "HACK THE BOX ACADEMY • PROFESSIONAL STANDARDS",
        "title": "Introduction to Penetration Testing & Standards",
        "tagline": "Industry testing standards (PTES, OSSTMM, NIST), Rules of Engagement, legal frameworks, and ethical testing workflows.",
        "pills": ["PTES Standards", "Rules of Engagement (RoE)", "Legal Compliance", "Vulnerability Scoring"],
        "accent": (59, 130, 246, 255),
        "footer_tag": "PROFESSIONAL PENTESTING"
    },
    {
        "out_path": f"{out_dir}/network-enumeration-with-nmap-cover.png",
        "badge": "HTB ACADEMY • PART 25",
        "kicker": "HACK THE BOX ACADEMY • NETWORK RECONNAISSANCE",
        "title": "Network Enumeration with Nmap: Scanning & Scripting",
        "tagline": "TCP SYN/Connect scans, UDP probing, service versioning, NSE scripting engine automation, and firewall evasion.",
        "pills": ["TCP SYN / Connect Scans", "NSE Script Automation", "Service Fingerprinting", "Firewall Bypass Options"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "NETWORK RECON"
    },
    {
        "out_path": f"{out_dir}/attacking-web-applications-with-ffuf-cover.png",
        "badge": "HTB ACADEMY • PART 26",
        "kicker": "HACK THE BOX ACADEMY • HIGH-SPEED WEB FUZZING",
        "title": "Attacking Web Applications with Ffuf Mastery",
        "tagline": "Directory and file fuzzing, wordlist tuning, virtual host routing, GET/POST parameter discovery, and filter regexes.",
        "pills": ["Directory Fuzzing", "Virtual Host Discovery", "Parameter Fuzzing", "Filter Status & Regex"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "WEB FUZZING"
    },
    {
        "out_path": f"{out_dir}/hacking-wordpress-cover.png",
        "badge": "HTB ACADEMY • PART 27",
        "kicker": "HACK THE BOX ACADEMY • CMS PENETRATION TESTING",
        "title": "Hacking WordPress: WPScan, Plugins & Web Shell RCE",
        "tagline": "WPScan automated auditing, user enumeration, vulnerable plugin/theme exploitation, and admin web shell injection.",
        "pills": ["WPScan Automated Audits", "Theme & Plugin Exploitation", "User Enumeration", "Malicious Plugin RCE"],
        "accent": (14, 165, 233, 255),
        "footer_tag": "CMS EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/cross-site-scripting-xss-cover.png",
        "badge": "HTB ACADEMY • PART 28",
        "kicker": "HACK THE BOX ACADEMY • CLIENT-SIDE ATTACKS",
        "title": "Cross-Site Scripting (XSS): Stored, Reflected & DOM",
        "tagline": "Context-aware payload delivery, stored/reflected/DOM vectors, session hijacking via cookie theft, and defense bypasses.",
        "pills": ["Stored & Reflected XSS", "DOM-Based Vulnerabilities", "Session Cookie Hijacking", "Context-Aware Payloads"],
        "accent": (236, 72, 153, 255),
        "footer_tag": "CLIENT-SIDE SECURITY"
    },
    {
        "out_path": f"{out_dir}/file-upload-attacks-cover.png",
        "badge": "HTB ACADEMY • PART 29",
        "kicker": "HACK THE BOX ACADEMY • ARBITRARY FILE UPLOAD",
        "title": "File Upload Attacks: Extension Bypasses & Polyglots",
        "tagline": "Client-side validation bypasses, black/whitelist evasion (double extensions, casing), MIME spoofing, and polyglot web shells.",
        "pills": ["Extension Filter Bypasses", "Magic Bytes Spoofing", "Polyglot Web Shells", "Reverse Shell Execution"],
        "accent": (239, 68, 68, 255),
        "footer_tag": "WEB EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/web-attacks-cover.png",
        "badge": "HTB ACADEMY • PART 30",
        "kicker": "HACK THE BOX ACADEMY • WEB VULNERABILITIES",
        "title": "Web Attacks: HTTP Verb Tampering & Insecure IDOR",
        "tagline": "HTTP Verb Tampering to bypass authorization filters, Insecure Direct Object References (IDOR), and mass parameter tampering.",
        "pills": ["HTTP Verb Tampering", "IDOR Access Exploitation", "Parameter Pollution", "Broken Access Control"],
        "accent": (244, 63, 94, 255),
        "footer_tag": "APPSEC PLAYBOOK"
    },
    {
        "out_path": f"{out_dir}/session-security-cover.png",
        "badge": "HTB ACADEMY • PART 31",
        "kicker": "HACK THE BOX ACADEMY • SESSION MANAGEMENT",
        "title": "Session Security: Fixation, Hijacking & CSRF Defense",
        "tagline": "Session state manipulation, predictable identifier generation, Cross-Site Request Forgery (CSRF), and cookie security flags.",
        "pills": ["Session Fixation Attacks", "CSRF Token Bypass", "Cookie Flag Analysis", "State Manipulation"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "SESSION SECURITY"
    },
    {
        "out_path": f"{out_dir}/cracking-passwords-with-hashcat-cover.png",
        "badge": "HTB ACADEMY • PART 32",
        "kicker": "HACK THE BOX ACADEMY • GPU PASSWORD CRACKING",
        "title": "Cracking Passwords with Hashcat: Modes & Rules",
        "tagline": "Hash identification, GPU attack modes (straight, combination, mask), custom mutation rules (OneRule, d3ad0ne), and speeds.",
        "pills": ["Hashcat GPU Acceleration", "Attack Modes (0, 1, 3, 6)", "Custom Rule Generation", "Hash Type Identification"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "PASSWORD CRACKING"
    },
    {
        "out_path": f"{out_dir}/using-the-metasploit-framework-cover.png",
        "badge": "HTB ACADEMY • PART 33",
        "kicker": "HACK THE BOX ACADEMY • EXPLOITATION FRAMEWORKS",
        "title": "Using the Metasploit Framework: Modules & Meterpreter",
        "tagline": "Operational mastery of msfconsole: exploit selection, payload staging, multi-handler setups, and Meterpreter post-exploitation.",
        "pills": ["msfconsole Architecture", "Meterpreter Commands", "Multi-Handler Payloads", "Post-Exploitation Modules"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "FRAMEWORK OPERATIONS"
    },
    {
        "out_path": f"{out_dir}/using-crackmapexec-cover.png",
        "badge": "HTB ACADEMY • PART 34",
        "kicker": "HACK THE BOX ACADEMY • ACTIVE DIRECTORY DOMINANCE",
        "title": "Using CrackMapExec: Multi-Protocol Network Dominance",
        "tagline": "SMB, WinRM, WMI, and MSSQL credential validation, password spraying across domains, dumping SAM/LSASS, and scraping shares.",
        "pills": ["Domain Password Spraying", "SAM & LSA Secrets Dump", "Share & File Scraping", "MSSQL Command Exec"],
        "accent": (220, 38, 38, 255),
        "footer_tag": "AD POST-EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/stack-based-buffer-overflows-on-linux-x86-cover.png",
        "badge": "HTB ACADEMY • PART 35",
        "kicker": "HACK THE BOX ACADEMY • BINARY EXPLOITATION (PWN)",
        "title": "Stack-Based Buffer Overflows on Linux x86",
        "tagline": "x86 architecture fundamentals, memory layout, stack frames, cyclic pattern EIP control, bad character analysis, and shellcode.",
        "pills": ["x86 Memory Stack Layout", "EIP Overwrite via GDB", "Bad Character Analysis", "Shellcode Injection"],
        "accent": (139, 92, 246, 255), # Violet
        "footer_tag": "BINARY EXPLOITATION"
    },
    {
        "out_path": f"{out_dir}/stack-based-buffer-overflows-on-windows-x86-cover.png",
        "badge": "HTB ACADEMY • PART 36",
        "kicker": "HACK THE BOX ACADEMY • WINDOWS EXPLOIT DEVELOPMENT",
        "title": "Stack-Based Buffer Overflows on Windows x86",
        "tagline": "Immunity Debugger and Mona.py automation, fuzzing TCP services, offset calculation, JMP ESP pointer resolution, and weaponization.",
        "pills": ["Immunity Debugger & Mona", "Fuzzing Network Services", "JMP ESP Opcode Pointers", "Weaponized Exploit Delivery"],
        "accent": (99, 102, 241, 255), # Indigo
        "footer_tag": "EXPLOIT DEVELOPMENT"
    },
    {
        "out_path": f"{out_dir}/attacking-wifi-protected-setup-wps-cover.png",
        "badge": "HTB ACADEMY • PART 37",
        "kicker": "HACK THE BOX ACADEMY • WIRELESS PENETRATION TESTING",
        "title": "Attacking Wi-Fi Protected Setup (WPS) & WPA2",
        "tagline": "Wireless frame capturing, monitor mode, Pixie-Dust offline PIN recovery, Reaver PIN brute-forcing, and WPA2 key extraction.",
        "pills": ["Airmon-ng Monitor Mode", "Pixie-Dust Attack", "Reaver WPS Pin Recovery", "WPA2 Pre-Shared Keys"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "WIRELESS PENTESTING"
    },
    {
        "out_path": f"{out_dir}/web-fuzzing-cover.png",
        "badge": "HTB ACADEMY • PART 38",
        "kicker": "HACK THE BOX ACADEMY • WEB APPLICATION FUZZING",
        "title": "Web Fuzzing Methodologies & Wfuzz Playbook",
        "tagline": "High-throughput directory discovery, SecLists wordlists, HTTP status code filtering, recursive fuzzing, and parameter discovery.",
        "pills": ["Wfuzz Command Workflows", "SecLists Dictionaries", "Recursive Directory Fuzzing", "HTTP Code Filtering"],
        "accent": (245, 158, 11, 255),
        "footer_tag": "WEB FUZZING"
    },
    {
        "out_path": f"{out_dir}/web-service-and-api-attacks-cover.png",
        "badge": "HTB ACADEMY • PART 39",
        "kicker": "HACK THE BOX ACADEMY • WEB SERVICES & API SECURITY",
        "title": "Web Service & API Attacks: WSDL, SOAP & REST",
        "tagline": "WSDL interface inspection, SOAPAction header tampering, XML injection, REST API authentication bypasses, and IDOR exploitation.",
        "pills": ["WSDL Service Enumeration", "SOAPAction XML Tampering", "REST API Auth Bypasses", "IDOR Data Exfiltration"],
        "accent": (168, 85, 247, 255),
        "footer_tag": "API SECURITY"
    },
    {
        "out_path": f"{out_dir}/wifi-penetration-testing-basics-cover.png",
        "badge": "HTB ACADEMY • PART 40",
        "kicker": "HACK THE BOX ACADEMY • 802.11 RADIO ANALYSIS",
        "title": "Wi-Fi Penetration Testing Basics & 802.11 Frames",
        "tagline": "802.11 management frames, beacon probing, deauthentication attacks with aireplay-ng, and 4-way WPA/WPA2 handshake capture.",
        "pills": ["802.11 Frame Dissection", "Airodump-ng Capture", "Aireplay-ng Deauth", "WPA2 4-Way Handshake"],
        "accent": (14, 165, 233, 255),
        "footer_tag": "WIRELESS SECURITY"
    },
    {
        "out_path": f"{out_dir}/wired-equivalent-privacy-wep-attacks-cover.png",
        "badge": "HTB ACADEMY • PART 41",
        "kicker": "HACK THE BOX ACADEMY • WIRELESS CRYPTANALYSIS",
        "title": "Wired Equivalent Privacy (WEP) Attacks & Cracking",
        "tagline": "RC4 keystream flaws, IV collision attacks, ARP replay injection, Chopchop and Fragmentation attacks, and instant key recovery.",
        "pills": ["RC4 Cryptographic Flaws", "ARP Replay Injection", "Chopchop Attack Method", "Instant WEP Key Recovery"],
        "accent": (159, 239, 0, 255),
        "footer_tag": "WIRELESS CRYPTANALYSIS"
    }
]

for item in ALL_COVERS:
    render_primary_cover(item)

print(f"\nSUCCESS: All {len(ALL_COVERS)} covers rendered to exact primary design specifications!")

