import os
from PIL import Image, ImageDraw, ImageFont

# Font loader
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

FONT_TITLE = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 22)
FONT_SUB = load_font(["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"], 13)
FONT_BOLD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 14)
FONT_REGULAR = load_font(["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"], 12)
FONT_CODE = load_font(["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"], 11)

def create_base(width, height, title, subtitle):
    img = Image.new("RGBA", (width, height), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)
    # Background gradient
    for y in range(height):
        factor = y / height
        r = int(12 + factor * 6)
        g = int(16 + factor * 8)
        b = int(24 + factor * 12)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    # Grid lines
    for x in range(0, width, 44):
        draw.line([(x, 0), (x, height)], fill=(30, 41, 59, 35), width=1)
    for y in range(0, height, 44):
        draw.line([(0, y), (width, y)], fill=(30, 41, 59, 35), width=1)
    # Header
    draw.text((45, 24), title, fill=(240, 246, 252, 255), font=FONT_TITLE)
    draw.text((45, 54), subtitle, fill=(148, 163, 184, 255), font=FONT_SUB)
    draw.line([(45, 80), (width - 45, 80)], fill=(51, 65, 85, 200), width=1)
    return img, draw

# --- 1. RE Chapter 1: x86 / x64 Stack Frame ---
def gen_re_ch1():
    out_path = "assets/images/posts/reverse-engineering/ch1-x86-stack-frame.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "x86 / x64 CALLING CONVENTIONS & STACK FRAME ARCHITECTURE", "Standard cdecl/stdcall vs Microsoft x64 FastCall, Frame Pointer Setup, and Epilogue Teardown")
    
    # Left Box: Standard 32-bit cdecl Stack Frame
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248, 200), width=2)
    draw.text((65, 115), "IA-32 Standard Stack Frame (High -> Low Memory)", fill=(56, 189, 248), font=FONT_BOLD)
    
    blocks_32 = [
        ("[EBP + 16] Function Argument 3", "Pushed right-to-left onto stack", (100, 116, 139)),
        ("[EBP + 12] Function Argument 2", "Pushed right-to-left onto stack", (100, 116, 139)),
        ("[EBP + 08] Function Argument 1", "Pushed right-to-left onto stack", (59, 130, 246)),
        ("[EBP + 04] Saved Return Address (EIP)", "Target instruction upon 'ret' instruction", (239, 68, 68)),
        ("[EBP + 00] Saved Frame Pointer (Old EBP)", "Base of caller function's stack frame", (245, 158, 11)),
        ("[EBP - 04] Local Variable 1 (DWORD)", "Allocated by 'sub esp, N'", (16, 185, 129)),
        ("[EBP - 08] Local Variable 2 (Buffer[4])", "Stack buffer (Vulnerable to overflow)", (168, 85, 247)),
        ("[ESP + 00] Stack Pointer (Top of Stack)", "Grows downwards towards 0x00000000", (56, 189, 248))
    ]
    y = 145
    for title, desc, col in blocks_32:
        draw.rounded_rectangle([(65, y), (500, y + 42)], radius=4, fill=(col[0], col[1], col[2], 30), outline=col, width=1)
        draw.text((75, y + 4), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 22), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 50

    # Right Box: AMD64 Microsoft FastCall ABI
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(168, 85, 247, 200), width=2)
    draw.text((570, 115), "x64 Microsoft FastCall Architecture", fill=(168, 85, 247), font=FONT_BOLD)
    
    blocks_64 = [
        ("Register: RCX / RDX / R8 / R9", "First 4 integer/pointer arguments passed via registers", (56, 189, 248)),
        ("Register: XMM0 / XMM1 / XMM2 / XMM3", "Floating-point arguments 1-4 passed in SSE registers", (16, 185, 129)),
        ("Stack Arguments 5+ [RSP + 40h...]", "Passed on stack beyond first four parameters", (100, 116, 139)),
        ("32-Byte Shadow Space (Home Space)", "Mandatory 4 QWORDs reserved by caller at [RSP + 28h]", (245, 158, 11)),
        ("16-Byte Stack Alignment Rule", "RSP must be a multiple of 16 prior to 'call' instruction", (239, 68, 68)),
        ("Non-Volatile Registers (Callee-Saved)", "RBX, RBP, RDI, RSI, R12-R15 preserved across calls", (59, 130, 246)),
        ("Volatile Registers (Caller-Saved)", "RAX, RCX, RDX, R8, R9, R10, R11 destroyed by callee", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in blocks_64:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56
    
    img.save(out_path)
    print("Generated:", out_path)

# --- 2. RE Chapter 2: ARM Architecture ---
def gen_re_ch2():
    out_path = "assets/images/posts/reverse-engineering/ch2-arm-architecture.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "ARM INSTRUCTION SET ARCHITECTURE (AArch32 & AArch64)", "RISC Register Banks, Condition Code Execution, Pipelining, and Thumb Mode Switching")
    
    # Left: AArch32 Core Registers
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129, 200), width=2)
    draw.text((65, 115), "AArch32 Core Register Bank (R0 - R15)", fill=(16, 185, 129), font=FONT_BOLD)
    
    regs_arm = [
        ("R0 - R3 (Argument & Return Registers)", "Pass parameters to functions; R0-R1 hold return value", (56, 189, 248)),
        ("R4 - R11 (General Purpose / Callee-Saved)", "Scratch & local variables; preserved across calls", (100, 116, 139)),
        ("R11 / FP (Frame Pointer)", "References parameters and local stack allocations", (245, 158, 11)),
        ("R12 / IP (Intra-Procedure Call Scratch)", "Used by linkers as a temporary scratch register", (168, 85, 247)),
        ("R13 / SP (Stack Pointer)", "Points to active stack top (Full Descending Stack)", (59, 130, 246)),
        ("R14 / LR (Link Register)", "Stores return address upon 'BL' or 'BLX' branching", (239, 68, 68)),
        ("R15 / PC (Program Counter)", "Points to instruction being fetched (Current PC + 8 in ARM)", (234, 88, 12)),
        ("CPSR (Current Program Status Register)", "Flags: N (Negative), Z (Zero), C (Carry), V (Overflow), T (Thumb)", (16, 185, 129))
    ]
    y = 145
    for title, desc, col in regs_arm:
        draw.rounded_rectangle([(65, y), (500, y + 42)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 4), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 22), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 50

    # Right: AArch64 & Execution States
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248, 200), width=2)
    draw.text((570, 115), "AArch64 & Operational Execution States", fill=(56, 189, 248), font=FONT_BOLD)
    
    a64_info = [
        ("64-Bit Registers (X0 - X30)", "31 general-purpose registers; W0-W30 for lower 32-bits", (56, 189, 248)),
        ("X30 (Link Register)", "Holds return address; ELR_ELx for exception returns", (239, 68, 68)),
        ("SP & Zero Register (XZR / WZR)", "Dedicated zero register hardwired to 0 value", (16, 185, 129)),
        ("Thumb Mode (16-Bit / Thumb-2 32-Bit)", "CPSR T-bit = 1; toggled via 'BX' instruction LSB bit", (245, 158, 11)),
        ("Conditional Execution Postfixes", "Instructions execute only if condition holds: EQ, NE, CS, MI", (168, 85, 247)),
        ("Barrel Shifter Optimization", "Arithmetic instructions shift second operand with zero cycle cost", (59, 130, 246)),
        ("Load/Store Architecture", "Memory access ONLY via LDR/STR; operations execute in registers", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in a64_info:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

# --- 3. RE Chapter 3: Windows Kernel & IRP ---
def gen_re_ch3():
    out_path = "assets/images/posts/reverse-engineering/ch3-windows-kernel-irp.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "WINDOWS KERNEL I/O SUBSYSTEM & IRP DISPATCH PIPELINE", "User-Mode DeviceIoControl, System Service Call, I/O Manager Request Packets, and Driver Stacks")
    
    # Left: The IRP Request Flow
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(239, 68, 68, 200), width=2)
    draw.text((65, 115), "I/O Request Packet (IRP) Lifecycle", fill=(239, 68, 68), font=FONT_BOLD)
    
    irp_steps = [
        ("1. User-Mode Win32 API Call", "App calls DeviceIoControl(hDevice, IOCTL, inBuf, outBuf)", (56, 189, 248)),
        ("2. Kernel Transition (syscall / sysenter)", "Switches to Ring 0 via KiSystemCall64 handler", (245, 158, 11)),
        ("3. I/O Manager Allocates IRP", "Creates IRP from non-paged pool with I/O stack locations", (168, 85, 247)),
        ("4. Major Function Dispatch (IRP_MJ_*)", "I/O manager invokes DriverObject->MajorFunction[Index]", (59, 130, 246)),
        ("5. Driver Stack Traversal", "Filter Drivers -> Functional Driver (FDO) -> Bus Driver (PDO)", (16, 185, 129)),
        ("6. Hardware Access / DMA Request", "Driver interacts with HAL or hardware registers", (148, 163, 184)),
        ("7. IoCompleteRequest & Status Return", "Kernel copies data, sets IoStatus.Status, unwinds to Ring 3", (239, 68, 68))
    ]
    y = 150
    for title, desc, col in irp_steps:
        draw.rounded_rectangle([(65, y), (500, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    # Right: Kernel Driver Core Structures
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(59, 130, 246, 200), width=2)
    draw.text((570, 115), "Windows Driver Object Hierarchy (Ring 0)", fill=(59, 130, 246), font=FONT_BOLD)
    
    struct_info = [
        ("DRIVER_OBJECT Structure", "Represents loaded image; points to DriverEntry, Unload, Dispatch table", (59, 130, 246)),
        ("DEVICE_OBJECT Structure", "Target of I/O operations; holds DeviceExtension, AttachedDevice", (56, 189, 248)),
        ("IRP Structure (Header & Body)", "IoStatus block, MdlAddress, UserBuffer, AssociatedIrp.SystemBuffer", (168, 85, 247)),
        ("IO_STACK_LOCATION", "MajorFunction, MinorFunction, Parameters (DeviceIoControl info)", (16, 185, 129)),
        ("Buffered vs Direct vs Neither I/O", "METHOD_BUFFERED: Safe copy | METHOD_DIRECT: MDL locked pages", (245, 158, 11)),
        ("Kernel Vulnerability Targets", "Arbitrary pointer dereferences, Type Confusion, Kernel Pool Corruptions", (239, 68, 68)),
        ("Rootkit Interception Points", "Inline function hooks, IRP Hooking, and MajorFunction pointer swaps", (234, 88, 12))
    ]
    y = 150
    for title, desc, col in struct_info:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

# --- 4. RE Chapter 4: Anti-Debugging & Obfuscation ---
def gen_re_ch4():
    out_path = "assets/images/posts/reverse-engineering/ch4-anti-debugging-obfuscation.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "ANTI-REVERSING, CODE OBFUSCATION & PACKER UNPACKING", "Detection Vectors: PEB Flags, Hardware Breakpoints, Timing Checks, and Unpacking State Machines")
    
    # Left: Anti-Debugging Check Mechanisms
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(245, 158, 11, 200), width=2)
    draw.text((65, 115), "Primary Anti-Debugging Detection Vectors", fill=(245, 158, 11), font=FONT_BOLD)
    
    antidebug_methods = [
        ("PEB->BeingDebugged Flag", "FS:[30h] + 2h in x86 / GS:[60h] + 2h in x64 (IsDebuggerPresent)", (239, 68, 68)),
        ("PEB->NtGlobalFlag", "Set to 0x70 (FLG_HEAP_ENABLE_TAIL_CHECK | FREE_CHECK) when attached", (245, 158, 11)),
        ("ProcessDebugPort & ProcessDebugFlags", "Queried via NtQueryInformationProcess system call", (56, 189, 248)),
        ("Hardware Breakpoints (DR0 - DR3)", "Context.Dr0-Dr3 checked via GetThreadContext", (168, 85, 247)),
        ("Timing Analysis via RDTSC", "Measures CPU cycle deltas to detect step-by-step tracing", (16, 185, 129)),
        ("Software Breakpoint Scans (0xCC)", "Memory hash scans detecting INT 3 instructions in function prologues", (59, 130, 246)),
        ("Structured Exception Handling (SEH)", "Intentional invalid memory reads to divert flow to hidden handlers", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in antidebug_methods:
        draw.rounded_rectangle([(65, y), (500, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    # Right: Packer Unpacking Flow
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(168, 85, 247, 200), width=2)
    draw.text((570, 115), "Generic Executable Unpacking Pipeline", fill=(168, 85, 247), font=FONT_BOLD)
    
    unpack_steps = [
        ("Stage 1: Packed Stub Execution", "Initial Entry Point (EP) located in packer section (.upx0 / .packer)", (148, 163, 184)),
        ("Stage 2: Anti-Analysis Self-Check", "Stub validates debugger absence and environment integrity", (245, 158, 11)),
        ("Stage 3: Memory Decompression / Decryption", "Compressed payload expanded into unmapped process memory (VirtualAlloc)", (56, 189, 248)),
        ("Stage 4: Import Address Table (IAT) Resolution", "Stub calls LoadLibraryA and GetProcAddress to resolve APIs", (59, 130, 246)),
        ("Stage 5: Relocation Fixups", "Applies base relocations if image not loaded at preferred BaseAddress", (16, 185, 129)),
        ("Stage 6: The Tail Jump", "Far JMP / CALL to the Original Entry Point (OEP) of payload", (239, 68, 68)),
        ("Stage 7: Memory Dumping & Scylla IAT Rebuilding", "Dump unpacked image from memory and reconstruct PE headers & IAT", (168, 85, 247))
    ]
    y = 150
    for title, desc, col in unpack_steps:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

# --- 5. RE Chapter 5: Rootkits & Kernel Hooking ---
def gen_re_ch5():
    out_path = "assets/images/posts/reverse-engineering/ch5-rootkits-kernel-hooks.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "ROOTKITS & KERNEL HOOKING: INTERCEPTION ARCHITECTURE", "System Service Descriptor Table (SSDT), Direct Kernel Object Manipulation (DKOM), and Inline Hooks")
    
    # Left: Hooking Mechanisms
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(239, 68, 68, 200), width=2)
    draw.text((65, 115), "Ring 0 Interception Strategies", fill=(239, 68, 68), font=FONT_BOLD)
    
    hook_types = [
        ("SSDT Hooking (KeServiceDescriptorTable)", "Overwriting function pointers in system service dispatch table", (239, 68, 68)),
        ("Inline Function Hooking (Detours)", "Overwriting first 5-14 bytes with JMP to malicious hook trampoline", (245, 158, 11)),
        ("IRP MajorFunction Table Hooking", "Redirecting DriverObject->MajorFunction[IRP_MJ_READ] pointer", (56, 189, 248)),
        ("Kernel Callbacks Registration", "Abusing PsSetCreateProcessNotifyRoutine & ObRegisterCallbacks", (16, 185, 129)),
        ("IDT (Interrupt Descriptor Table) Modification", "Hooking interrupt vectors for low-level system interception", (168, 85, 247)),
        ("DKOM (Direct Kernel Object Manipulation)", "Unlinking process from ActiveProcessLinks list in EPROCESS block", (59, 130, 246)),
        ("PatchGuard (KPP) & Driver Signature Enforcement", "Windows 64-bit mitigations enforcing kernel integrity verification", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in hook_types:
        draw.rounded_rectangle([(65, y), (500, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    # Right: DKOM Process Hiding Mechanism
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248, 200), width=2)
    draw.text((570, 115), "DKOM: ActiveProcessLinks Process Cloaking", fill=(56, 189, 248), font=FONT_BOLD)
    
    dkom_steps = [
        ("1. EPROCESS Structure Identification", "Every Windows process is backed by an opaque EPROCESS kernel object", (56, 189, 248)),
        ("2. ActiveProcessLinks LIST_ENTRY", "Circular doubly linked list connecting all active processes (Flink & Blink)", (59, 130, 246)),
        ("3. Target Node (Malicious Process)", "Rootkit locates target PID in kernel memory by traversing the list", (245, 158, 11)),
        ("4. Node Unlinking Operation", "Target->Blink->Flink = Target->Flink | Target->Flink->Blink = Target->Blink", (239, 68, 68)),
        ("5. Task Manager Invisible Status", "Enumeration tools relying on NtQuerySystemInformation cannot find process", (16, 185, 129)),
        ("6. Thread Execution Unhindered", "Threads still scheduled normally via ETHREAD structures in dispatcher", (168, 85, 247)),
        ("7. Forensic Detection via Pool Scanning", "Memory forensics (Volatility) finds hidden process via Tag scanning ('Proc')", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in dkom_steps:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

# --- 6. Mobile Pentest: TLS Pinning Bypass ---
def gen_mobile_tls():
    out_path = "assets/images/posts/android-security/mobile-tls-pinning-diagram.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "ANDROID TLS PINNING BYPASS & DYNAMIC INTERCEPTION", "Certificate Trust Chains, OkHttp/TrustManager Verification, and Frida Runtime In-Memory Hooking")
    
    # Left: Normal vs Pinned TLS
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(239, 68, 68, 200), width=2)
    draw.text((65, 115), "TLS Pinning Enforcement Architecture", fill=(239, 68, 68), font=FONT_BOLD)
    
    tls_steps = [
        ("Standard CA Trust Store", "App trusts any valid certificate signed by System/User CAs", (56, 189, 248)),
        ("MitM Proxy Insertion (Burp Suite)", "Attacker generates proxy CA cert; rejected if pinned", (245, 158, 11)),
        ("Certificate Pinning (X.509 Binary)", "Hardcoded byte array or asset certificate comparison", (239, 68, 68)),
        ("Public Key Pinning (SPKI SHA-256)", "Hashes public key SubjectPublicKeyInfo header", (168, 85, 247)),
        ("OkHttp CertificatePinner Check", "CertificatePinner.check(hostname, peerCertificates)", (59, 130, 246)),
        ("TrustManagerImpl Check", "checkTrustedRecursive() verifies trust chain to pinned root", (16, 185, 129)),
        ("Network Security Config (XML)", "Android res/xml/network_security_config.xml enforcement", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in tls_steps:
        draw.rounded_rectangle([(65, y), (500, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    # Right: Frida Dynamic Bypass Architecture
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129, 200), width=2)
    draw.text((570, 115), "Frida Runtime Memory Hooking Pipeline", fill=(16, 185, 129), font=FONT_BOLD)
    
    frida_steps = [
        ("1. Frida Server / Gadget Injection", "Daemon attaches to target app process; executes V8 engine in RAM", (56, 189, 248)),
        ("2. Java.perform() Reflection Wrapper", "Binds JavaScript thread context to Dalvik/ART virtual machine", (59, 130, 246)),
        ("3. Hook TrustManager.checkServerTrusted()", "Overwrites method implementation with no-op empty function", (16, 185, 129)),
        ("4. Hook OkHttp3 CertificatePinner.check()", "Forces check() to return cleanly without throwing SSLPeerUnverifiedException", (245, 158, 11)),
        ("5. Native OpenSSL Hooking (libssl.so)", "Hooks SSL_CTX_set_verify & SSL_set_verify to SSL_VERIFY_NONE", (239, 68, 68)),
        ("6. Flutter / BoringSSL Bypass", "Patches compiled assembly validation jumps in libflutter.so", (168, 85, 247)),
        ("7. Clean Decrypted MitM Traffic", "Cleartext HTTP/2 REST & GraphQL streams routed to Burp Suite", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in frida_steps:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

# --- 7. Mobile Pentest Ch 1: Android App Architecture ---
def gen_mobile_ch1():
    out_path = "assets/images/posts/android-security/mobile-pentest-ch1-architecture.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "ANDROID APPLICATION INTERNAL ARCHITECTURE & EXECUTION", "APK Container Layout, Java/Kotlin Compilation, Dalvik Bytecode, and ART Runtime Sandboxing")
    
    # Left: APK Packaging & Build Output
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248, 200), width=2)
    draw.text((65, 115), "APK Internal Component Blueprint", fill=(56, 189, 248), font=FONT_BOLD)
    
    apk_parts = [
        ("AndroidManifest.xml (Compiled Binary)", "Permissions, components (Activities, Services, Receivers, Providers)", (56, 189, 248)),
        ("classes.dex (Dalvik Executable)", "Compiled bytecode instructions executed by Dalvik/ART virtual machine", (59, 130, 246)),
        ("resources.arsc", "Pre-compiled resource table linking string IDs to layout elements", (100, 116, 139)),
        ("res/ & assets/", "UI XML definitions, raw binary assets, certificates, configurations", (16, 185, 129)),
        ("lib/ (Native Shared Libraries)", "Compiled C/C++ libraries partitioned by ABI: arm64-v8a, armeabi-v7a, x86", (168, 85, 247)),
        ("META-INF/ (Signatures & Hashes)", "CERT.RSA, CERT.SF, MANIFEST.MF containing APK v1/v2/v3 signatures", (245, 158, 11)),
        ("Apex / Split APK Modules", "Modular dynamic delivery split packages deployed dynamically by Play", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in apk_parts:
        draw.rounded_rectangle([(65, y), (500, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    # Right: The Sandboxed Runtime Environment
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129, 200), width=2)
    draw.text((570, 115), "Multi-Tiered Android Sandboxing Controls", fill=(16, 185, 129), font=FONT_BOLD)
    
    sandbox_layers = [
        ("Tier 1: Linux UID/GID Isolation", "Every app assigned unique UID (u0_aXXX); cannot access other app dirs", (56, 189, 248)),
        ("Tier 2: Android Runtime (ART) Execution", "AOT/JIT compiled native machine code executing within isolated VM", (59, 130, 246)),
        ("Tier 3: Inter-Process Communication (IPC)", "Strict Binder driver mediation; UID/PID verification for Intents", (16, 185, 129)),
        ("Tier 4: SELinux Mandatory Access Control", "untrusted_app domain restricts kernel syscalls and hardware nodes", (245, 158, 11)),
        ("Tier 5: Scoped Storage & Sandbox FS", "Access restricted to /data/data/<pkg> and isolated media stores", (168, 85, 247)),
        ("Tier 6: Android Keystore Hardware Backing", "Key material guarded in hardware Secure World (TEE / StrongBox)", (239, 68, 68)),
        ("Tier 7: Permission Enforcement Gateways", "SystemServer enforces normal/dangerous/signature permissions", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in sandbox_layers:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

# --- 8. Mobile Pentest Ch 2: Static Analysis Pipeline ---
def gen_mobile_ch2():
    out_path = "assets/images/posts/android-security/mobile-pentest-ch2-static-analysis.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "ANDROID STATIC SECURITY ANALYSIS & AUDITING METHODOLOGY", "Decompilation Tools, Manifest Auditing, Hardcoded Secret Hunting, and Cryptographic Reviews")
    
    # Left: Toolchain & Decompilation
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(59, 130, 246, 200), width=2)
    draw.text((65, 115), "Decompilation & Disassembly Pipeline", fill=(59, 130, 246), font=FONT_BOLD)
    
    tools_static = [
        ("APKTool (Disassembly to Smali)", "Decodes resources, AndroidManifest.xml, and generates Smali opcode trees", (56, 189, 248)),
        ("JADX-GUI (Java Source Recovery)", "Translates DEX bytecode back to high-level readable Java/Kotlin sources", (59, 130, 246)),
        ("Baksmali / Smali Assembler", "Modifies Smali code to bypass controls and reassembles with apktool", (16, 185, 129)),
        ("Ghidra / IDA Pro (Native Binaries)", "Reverse engineers .so native shared libraries for proprietary logic", (168, 85, 247)),
        ("MobSF (Automated SAST Framework)", "Automates vulnerability scanning, security score computation, and API calls", (245, 158, 11)),
        ("TruffleHog / GitGuardian Scans", "Scans decompiled sources for API keys, AWS credentials, and tokens", (239, 68, 68)),
        ("Apksigner & Zipalign Inspection", "Verifies cryptographic signature scheme (v1-v4) and alignment", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in tools_static:
        draw.rounded_rectangle([(65, y), (500, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    # Right: Key Vulnerability Audit Checklist
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(239, 68, 68, 200), width=2)
    draw.text((570, 115), "Static Analysis High-Risk Audit Checklist", fill=(239, 68, 68), font=FONT_BOLD)
    
    audit_points = [
        ("Exported Components (android:exported=true)", "Unprotected Activities, Services, Receivers callable by rogue apps", (239, 68, 68)),
        ("Insecure Deep Links & Implicit Intents", "URL scheme hijacking and intent injection without origin validation", (245, 158, 11)),
        ("Hardcoded Cryptographic Secrets", "Static AES encryption keys, IVs, Firebase tokens, Private API credentials", (168, 85, 247)),
        ("Insecure WebView Settings", "setJavaScriptEnabled(true) combined with addJavascriptInterface() RCE", (56, 189, 248)),
        ("Cleartext Traffic Allowed (android:usesCleartextTraffic)", "Enables unencrypted HTTP traffic susceptible to local network interception", (16, 185, 129)),
        ("Backup & Debugging Enabled (allowBackup=true)", "Enables adb backup extraction of private data and run-as debugging", (59, 130, 246)),
        ("Weak Cryptography Implementations", "Use of DES, ECB mode, static seeds in SecureRandom, MD5/SHA-1 hashing", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in audit_points:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

# --- 9. Mobile Pentest Ch 3: Dynamic Frida Architecture ---
def gen_mobile_ch3():
    out_path = "assets/images/posts/android-security/mobile-pentest-ch3-dynamic-frida.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "DYNAMIC INSTRUMENTATION & RUNTIME HOOKING WITH FRIDA", "Frida Core Architecture, V8 JavaScript Injection, Interceptor API, and Objection Runtime Exploration")
    
    # Left: Dynamic Hooking Mechanics
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129, 200), width=2)
    draw.text((65, 115), "Frida In-Process Hooking Architecture", fill=(16, 185, 129), font=FONT_BOLD)
    
    frida_arch = [
        ("Host Controller (Workstation CLI / Python)", "Communicates via ADB socket; sends JavaScript payloads to device", (56, 189, 248)),
        ("Target Device frida-server Daemon", "Runs as root; injects frida-agent.so into target application process", (59, 130, 246)),
        ("In-Process Google V8 Engine", "Executes user JavaScript inside target app memory space", (16, 185, 129)),
        ("Java.use() Class Loading Hook", "Acquires reference to Java class; overrides .implementation function", (245, 158, 11)),
        ("Interceptor.attach() Native API", "Hooks C/C++ functions via trampolines; onEnter and onLeave handlers", (168, 85, 247)),
        ("Memory.protect() & Memory.readByteArray()", "Directly alters memory page permissions and reads process heap/stack", (239, 68, 68)),
        ("Bidirectional RPC Messaging (send / recv)", "Transmits dumped encryption keys and session tokens back to host", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in frida_arch:
        draw.rounded_rectangle([(65, y), (500, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    # Right: Objection & Runtime Exploration
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(168, 85, 247, 200), width=2)
    draw.text((570, 115), "Objection Runtime Pentest Capabilities", fill=(168, 85, 247), font=FONT_BOLD)
    
    objection_caps = [
        ("Automated SSL Pinning Bypass", "Single command ('android sslpinning disable') hooks 20+ TLS libraries", (56, 189, 248)),
        ("Root Detection Evasion", "Hooks su binary checks, Test-Keys, Superuser.apk, build.prop flags", (16, 185, 129)),
        ("Live Class & Method Tracing", "Watches all invocations of targeted packages in real-time with arguments", (59, 130, 246)),
        ("Memory Heap Dumps & Secret Searching", "Scans process memory for strings, auth tokens, and plaintext passwords", (245, 158, 11)),
        ("Keystore & Cryptographic Monitoring", "Logs all Cipher.doFinal(), KeyStore.load(), and SecretKeySpec calls", (239, 68, 68)),
        ("SharedPreferences & SQLite Live Viewing", "Inspects and modifies local database records while the application runs", (168, 85, 247)),
        ("Dynamic Activity Spawning", "Launches exported or non-exported activities directly without authentication", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in objection_caps:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

# --- 10. DNS Recon Framework Architecture ---
def gen_dns_recon():
    out_path = "assets/images/posts/automation/recon-dns-architecture.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img, draw = create_base(1100, 620, "AUTOMATED DNS RECONNAISSANCE & RESOLUTION PIPELINE", "Multi-Stage OSINT Enumeration, Wildcard Detection, Mass Resolution, and Zone Transfer Auditing")
    
    # Left: Recon Pipeline Stages
    draw.rounded_rectangle([(45, 100), (520, 560)], radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248, 200), width=2)
    draw.text((65, 115), "Multi-Stage DNS Reconnaissance Workflow", fill=(56, 189, 248), font=FONT_BOLD)
    
    stages = [
        ("Stage 1: Target Ingestion & Scope Definition", "Domain normalization, CIDR boundaries, out-of-scope filtering", (56, 189, 248)),
        ("Stage 2: Passive OSINT Aggregation", "Certificate Transparency logs (crt.sh), VirusTotal, AlienVault, Shodan", (59, 130, 246)),
        ("Stage 3: Active Zone Transfer Testing (AXFR)", "Queries all authoritative nameservers for full zone disclosure", (239, 68, 68)),
        ("Stage 4: Wildcard DNS Detection", "Probes random UUID subdomains; filters out catch-all IPs dynamically", (245, 158, 11)),
        ("Stage 5: High-Speed Brute-Force Resolution", "Asynchronous parallel DNS queries against massive multi-wordlists", (16, 185, 129)),
        ("Stage 6: Multi-Record Extraction (A/AAAA/CNAME/TXT)", "Correlates MX, NS, SOA, TXT (SPF/DKIM/DMARC), and PTR records", (168, 85, 247)),
        ("Stage 7: Subdomain Takeover Vulnerability Audit", "Flags dangling CNAME records pointing to unclaimed Cloud/SaaS buckets", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in stages:
        draw.rounded_rectangle([(65, y), (500, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((75, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((75, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    # Right: Python Architecture & Performance
    draw.rounded_rectangle([(550, 100), (1055, 560)], radius=8, fill=(15, 23, 42, 220), outline=(16, 185, 129, 200), width=2)
    draw.text((570, 115), "Python Framework Architecture Components", fill=(16, 185, 129), font=FONT_BOLD)
    
    arch_comp = [
        ("asyncio & aiodns Integration", "Non-blocking event loop enabling 10,000+ DNS resolutions per second", (16, 185, 129)),
        ("Trusted Public Resolver Pool", "Round-robin distribution across 1.1.1.1, 8.8.8.8, 9.9.9.9 to bypass rate limits", (56, 189, 248)),
        ("Smart Rate Limiting & Backoff", "Token-bucket rate limiters preventing socket exhaustion and dropped packets", (59, 130, 246)),
        ("Structured JSON & CSV Exporter", "Generates standardized asset inventories for pipeline integration", (100, 116, 139)),
        ("Subdomain Alteration Engine", "Generates permutations: dev-*, staging-*, *-api, *-vpn, *-internal", (245, 158, 11)),
        ("Active HTTP/HTTPS Probe Hook", "Dispatches httpx probes to verify web services on resolved IPs", (168, 85, 247)),
        ("Graph Visualization Output", "Produces network relationship maps connecting IPs, domains, and ASNs", (148, 163, 184))
    ]
    y = 150
    for title, desc, col in arch_comp:
        draw.rounded_rectangle([(570, y), (1035, y + 46)], radius=4, fill=(col[0], col[1], col[2], 25), outline=col, width=1)
        draw.text((580, y + 5), title, fill=col, font=FONT_CODE)
        draw.text((580, y + 24), desc, fill=(203, 213, 225), font=FONT_REGULAR)
        y += 56

    img.save(out_path)
    print("Generated:", out_path)

if __name__ == "__main__":
    print("Building all missing technical diagrams...")
    gen_re_ch1()
    gen_re_ch2()
    gen_re_ch3()
    gen_re_ch4()
    gen_re_ch5()
    gen_mobile_tls()
    gen_mobile_ch1()
    gen_mobile_ch2()
    gen_mobile_ch3()
    gen_dns_recon()
    print("All diagrams built successfully.")

