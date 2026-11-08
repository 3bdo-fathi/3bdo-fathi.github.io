---
layout: page
icon: fas fa-user
order: 4
title: About Me
permalink: /about/
image: /assets/images/site/preview.jpg
---

<style>
  /* ── About Me Container & Typography ── */
  .about-container {
    max-width: 820px;
    margin: 0 auto;
    color: #c9d1d9;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }

  [data-mode="light"] .about-container {
    color: #24292f;
  }

  /* ── Hero Profile Card ── */
  .about-hero-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    position: relative;
    overflow: hidden;
  }

  [data-mode="light"] .about-hero-card {
    background: #f6f8fa;
    border-color: #d0d7de;
  }

  .about-hero-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #1f6feb, #58a6ff, #39d353);
  }

  .about-hero-top {
    display: flex;
    align-items: center;
    gap: 1.75rem;
    flex-wrap: wrap;
  }

  .about-avatar-wrap {
    position: relative;
    width: 100px;
    height: 100px;
    flex-shrink: 0;
  }

  .about-avatar-img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #58a6ff;
    box-shadow: 0 0 16px rgba(88, 166, 255, 0.25);
  }

  .about-hero-info {
    flex: 1;
    min-width: 260px;
  }

  .about-hero-name {
    font-size: 1.65rem;
    font-weight: 700;
    color: #f0f6fc;
    margin: 0 0 0.25rem 0;
    line-height: 1.2;
  }

  [data-mode="light"] .about-hero-name {
    color: #1f2328;
  }

  .about-hero-handle {
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
    font-size: 0.95rem;
    color: #58a6ff;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  [data-mode="light"] .about-hero-handle {
    color: #0969da;
  }

  .about-hero-title {
    font-size: 0.95rem;
    color: #8b949e;
    margin: 0;
    line-height: 1.4;
  }

  /* Status Pill */
  .about-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.3rem 0.75rem;
    border-radius: 20px;
    background: rgba(57, 211, 83, 0.1);
    border: 1px solid rgba(57, 211, 83, 0.3);
    font-size: 0.75rem;
    font-weight: 600;
    color: #3fb950;
    margin-top: 0.75rem;
  }

  .status-pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #3fb950;
    box-shadow: 0 0 0 0 rgba(63, 185, 80, 0.7);
    animation: statusPulse 2s infinite cubic-bezier(0.4, 0, 0.6, 1);
  }

  @keyframes statusPulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(63, 185, 80, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(63, 185, 80, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(63, 185, 80, 0); }
  }

  /* Social Action Buttons */
  .about-social-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  [data-mode="light"] .about-social-links {
    border-top-color: #d0d7de;
  }

  .about-social-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.45rem 0.9rem;
    border-radius: 6px;
    background: #161b22;
    border: 1px solid #30363d;
    color: #c9d1d9 !important;
    text-decoration: none !important;
    font-size: 0.82rem;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .about-social-btn:hover {
    background: #21262d;
    border-color: #58a6ff;
    color: #58a6ff !important;
    transform: translateY(-1px);
  }

  [data-mode="light"] .about-social-btn {
    background: #ffffff;
    border-color: #d0d7de;
    color: #24292f !important;
  }

  [data-mode="light"] .about-social-btn:hover {
    background: #f3f4f6;
    border-color: #0969da;
    color: #0969da !important;
  }

  /* ── Section Titles ── */
  .about-section-heading {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f0f6fc;
    margin: 2.25rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #21262d;
  }

  [data-mode="light"] .about-section-heading {
    color: #1f2328;
    border-bottom-color: #d0d7de;
  }

  .about-section-heading i {
    color: #58a6ff;
    font-size: 1.1rem;
  }

  [data-mode="light"] .about-section-heading i {
    color: #0969da;
  }

  /* ── Domain Grid Cards ── */
  .about-domain-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .about-domain-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.25rem;
    transition: all 0.2s ease;
  }

  .about-domain-card:hover {
    border-color: rgba(88, 166, 255, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  }

  [data-mode="light"] .about-domain-card {
    background: #ffffff;
    border-color: #d0d7de;
  }

  [data-mode="light"] .about-domain-card:hover {
    border-color: #0969da;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }

  .about-domain-header {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 1rem;
    font-weight: 600;
    color: #f0f6fc;
    margin-bottom: 0.6rem;
  }

  [data-mode="light"] .about-domain-header {
    color: #1f2328;
  }

  .about-domain-header i {
    color: #58a6ff;
  }

  .about-domain-body {
    font-size: 0.85rem;
    color: #8b949e;
    line-height: 1.5;
    margin: 0;
  }

  [data-mode="light"] .about-domain-body {
    color: #57606a;
  }

  /* ── Technical Stack Matrix ── */
  .about-stack-section {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }

  [data-mode="light"] .about-stack-section {
    background: #f6f8fa;
    border-color: #d0d7de;
  }

  .about-stack-row {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .about-stack-row:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }

  [data-mode="light"] .about-stack-row {
    border-bottom-color: #d0d7de;
  }

  .about-stack-label {
    min-width: 140px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #8b949e;
  }

  [data-mode="light"] .about-stack-label {
    color: #57606a;
  }

  .about-stack-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .about-tag-pill {
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
    font-size: 0.75rem;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    background: #161b22;
    border: 1px solid #30363d;
    color: #e6edf3;
  }

  [data-mode="light"] .about-tag-pill {
    background: #ffffff;
    border-color: #d0d7de;
    color: #24292f;
  }

  /* ── Research Series Showcase ── */
  .about-series-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 1rem;
    margin-bottom: 2.25rem;
  }

  .about-series-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.25rem;
    text-decoration: none !important;
    display: block;
    transition: all 0.2s ease;
  }

  .about-series-card:hover {
    border-color: #58a6ff;
    transform: translateY(-2px);
  }

  [data-mode="light"] .about-series-card {
    background: #ffffff;
    border-color: #d0d7de;
  }

  [data-mode="light"] .about-series-card:hover {
    border-color: #0969da;
  }

  .about-series-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #58a6ff;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  [data-mode="light"] .about-series-title {
    color: #0969da;
  }

  .about-series-count {
    font-size: 0.72rem;
    padding: 0.15rem 0.45rem;
    border-radius: 12px;
    background: rgba(88, 166, 255, 0.15);
    color: #58a6ff;
    font-family: monospace;
  }

  .about-series-desc {
    font-size: 0.82rem;
    color: #8b949e;
    margin: 0;
    line-height: 1.45;
  }

  /* ── Dedication Du'a Card ── */
  .about-dua-box {
    background: #090d13;
    border: 1px solid #30363d;
    border-left: 4px solid #58a6ff;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2.5rem 0 1rem;
    text-align: center;
  }

  [data-mode="light"] .about-dua-box {
    background: #f6f8fa;
    border-color: #d0d7de;
    border-left-color: #0969da;
  }

  .about-dua-ar {
    font-size: 1.05rem;
    line-height: 2;
    color: #f0f6fc;
    font-weight: 600;
    direction: rtl;
    margin-bottom: 0.75rem;
  }

  [data-mode="light"] .about-dua-ar {
    color: #1f2328;
  }

  .about-dua-en {
    font-size: 0.85rem;
    line-height: 1.5;
    color: #8b949e;
    font-style: italic;
    margin: 0;
  }
</style>

<div class="about-container">

  <!-- Hero Profile Header -->
  <div class="about-hero-card">
    <div class="about-hero-top">
      <div class="about-avatar-wrap">
        <img src="/assets/images/site/avatar.jpg" alt="Abdulrahman M. Fathi" class="about-avatar-img">
      </div>
      <div class="about-hero-info">
        <h1 class="about-hero-name">Abdulrahman M. Fathi</h1>
        <div class="about-hero-handle">0x3bdo</div>
        <p class="about-hero-title">
          Offensive Security Engineer &amp; Penetration Tester | Cairo, Egypt
        </p>
        <div class="about-status-pill">
          <span class="status-pulse-dot"></span>
          <span>Available for Technical Audits &amp; Security Research</span>
        </div>
      </div>
    </div>

    <!-- Quick Communication Links -->
    <div class="about-social-links">
      <a href="https://www.linkedin.com/in/3bdo-fathi" target="_blank" rel="noopener noreferrer" class="about-social-btn">
        <i class="fab fa-linkedin"></i> LinkedIn
      </a>
      <a href="https://github.com/3bdo-fathi" target="_blank" rel="noopener noreferrer" class="about-social-btn">
        <i class="fab fa-github"></i> GitHub
      </a>
      <a href="https://twitter.com/3bdofathii" target="_blank" rel="noopener noreferrer" class="about-social-btn">
        <i class="fab fa-twitter"></i> Twitter
      </a>
      <a href="mailto:abdulrahmanmohamedfathi@gmail.com" class="about-social-btn">
        <i class="fas fa-envelope"></i> Email
      </a>
      <a href="/contact-me/" class="about-social-btn">
        <i class="fas fa-paper-plane"></i> Contact Form
      </a>
    </div>
  </div>

  <!-- Engineering Bio -->
  <h2 class="about-section-heading">
    <i class="fas fa-terminal"></i> Security Philosophy &amp; Mindset
  </h2>
  <p style="font-size: 0.95rem; line-height: 1.65; margin-bottom: 1.5rem;">
    I am an offensive security engineer specializing in vulnerability research, binary disassembly, and end-to-end penetration testing across enterprise ecosystems. My primary methodology centers on deep architectural comprehension: uncovering subtle design misconfigurations and chaining them into tangible business impact. Rather than relying on superficial automated scanners, I dissect applications down to their bytecode, kernel interfaces, and network primitives to engineer reliable, actionable remediation frameworks.
  </p>

  <!-- Core Domains Grid -->
  <h2 class="about-section-heading">
    <i class="fas fa-shield-alt"></i> Core Technical Focus Areas
  </h2>
  <div class="about-domain-grid">
    <div class="about-domain-card">
      <div class="about-domain-header">
        <i class="fas fa-mobile-alt"></i> Mobile Application Security
      </div>
      <p class="about-domain-body">
        In-depth Android and iOS penetration testing aligning with the OWASP MASTG framework. Specializing in bytecode reversing (Smali/DEX), dynamic instrumentation via Frida and Objection, TLS/SSL pinning bypasses, native library analysis, and IPC component auditing.
      </p>
    </div>

    <div class="about-domain-card">
      <div class="about-domain-header">
        <i class="fas fa-microchip"></i> Reverse Engineering &amp; Binaries
      </div>
      <p class="about-domain-body">
        Low-level software analysis across x86, x64, and ARM architectures. Decompiling native binaries in Ghidra and IDA Pro, Windows kernel driver inspection, dynamic debugging with WinDbg, memory corruption triage, and software deobfuscation.
      </p>
    </div>

    <div class="about-domain-card">
      <div class="about-domain-header">
        <i class="fas fa-network-wired"></i> Active Directory &amp; Enterprise Infrastructure
      </div>
      <p class="about-domain-body">
        Assessing complex enterprise Windows environments. Attack graph analysis with BloodHound, Kerberos abuse tradecraft (Kerberoasting, AS-REP roasting), Active Directory Certificate Services (AD CS) misconfigurations, and lateral movement defense.
      </p>
    </div>

    <div class="about-domain-card">
      <div class="about-domain-header">
        <i class="fas fa-globe"></i> Web &amp; API Security Architecture
      </div>
      <p class="about-domain-body">
        Comprehensive web application security assessments focusing on high-severity business logic flaws, Broken Object Level Authorization (BOLA/IDOR), OAuth/JWT implementation flaws, and modern API protocols spanning REST, GraphQL, and gRPC.
      </p>
    </div>
  </div>

  <!-- Technical Arsenal Matrix -->
  <h2 class="about-section-heading">
    <i class="fas fa-tools"></i> Technical Arsenal &amp; Toolchain
  </h2>
  <div class="about-stack-section">
    <div class="about-stack-row">
      <div class="about-stack-label">Disassembly &amp; Debugging</div>
      <div class="about-stack-tags">
        <span class="about-tag-pill">Ghidra</span>
        <span class="about-tag-pill">IDA Pro</span>
        <span class="about-tag-pill">WinDbg</span>
        <span class="about-tag-pill">Jadx-GUI</span>
        <span class="about-tag-pill">Apktool</span>
        <span class="about-tag-pill">GDB</span>
      </div>
    </div>

    <div class="about-stack-row">
      <div class="about-stack-label">Dynamic Instrumentation</div>
      <div class="about-stack-tags">
        <span class="about-tag-pill">Frida</span>
        <span class="about-tag-pill">Objection</span>
        <span class="about-tag-pill">Drozer</span>
        <span class="about-tag-pill">Burp Suite Pro</span>
        <span class="about-tag-pill">Caido</span>
        <span class="about-tag-pill">Wireshark</span>
      </div>
    </div>

    <div class="about-stack-row">
      <div class="about-stack-label">Languages &amp; Automation</div>
      <div class="about-stack-tags">
        <span class="about-tag-pill">Python</span>
        <span class="about-tag-pill">Bash</span>
        <span class="about-tag-pill">C / C++</span>
        <span class="about-tag-pill">Java</span>
        <span class="about-tag-pill">Smali Assembly</span>
        <span class="about-tag-pill">PowerShell</span>
      </div>
    </div>

    <div class="about-stack-row">
      <div class="about-stack-label">Testing Environments</div>
      <div class="about-stack-tags">
        <span class="about-tag-pill">Kali Linux</span>
        <span class="about-tag-pill">FlareVM</span>
        <span class="about-tag-pill">Rooted Android (KernelSU / Magisk)</span>
        <span class="about-tag-pill">Docker</span>
      </div>
    </div>
  </div>

  <!-- Authored Research Series -->
  <h2 class="about-section-heading">
    <i class="fas fa-book-open"></i> Authored Research Series &amp; Guides
  </h2>
  <div class="about-series-list">
    <a href="/categories/android-security/" class="about-series-card">
      <div class="about-series-title">
        <span>Mobile Penetration Testing Guide</span>
        <span class="about-series-count">Master Guide</span>
      </div>
      <p class="about-series-desc">
        Comprehensive field manual covering OWASP MASTG, modern lab setups, Smali bytecode tampering, IPC attack surfaces, and deep link exploitation.
      </p>
    </a>

    <a href="/categories/android-security/" class="about-series-card">
      <div class="about-series-title">
        <span>Android Security Internals</span>
        <span class="about-series-count">13 Chapters</span>
      </div>
      <p class="about-series-desc">
        Chapter-by-chapter reference guide dissecting Linux sandboxing, Binder IPC, package manager verification, hardware Keystore, and SELinux policies.
      </p>
    </a>

    <a href="/categories/reverse-engineering/" class="about-series-card">
      <div class="about-series-title">
        <span>Practical Reverse Engineering</span>
        <span class="about-series-count">5 Chapters</span>
      </div>
      <p class="about-series-desc">
        In-depth analysis of x86/x64 assembly, ARM execution models, Windows kernel internals, WinDbg debugging scripts, and rootkit analysis.
      </p>
    </a>

    <a href="/categories/social-engineering/" class="about-series-card">
      <div class="about-series-title">
        <span>The Art of Human Hacking</span>
        <span class="about-series-count">9 Chapters</span>
      </div>
      <p class="about-series-desc">
        Exhaustive breakdown of psychological attack surfaces, elicitation methodologies, non-verbal indicators, and human defense engineering.
      </p>
    </a>
  </div>

  <!-- Sacred Dedication Box (Du'a) -->
  <div class="about-dua-box">
    <div class="about-dua-ar">
      اللهم اجعل هذا العمل علمًا نافعًا وصدقةً جارية، واكتب لي به الأجر والقبول، وانفع به كل من قرأه أو تعلّمه.<br>
      اللهم احفظ لي والديّ وأهلي، وبارك في أعمارهم وصحتهم، وأدم عليهم نعمة الصحة والعافية، ولا تريني فيهم بأسًا يبكيني.
    </div>
    <div class="about-dua-en">
      Dedicated as ongoing charity and beneficial knowledge. May Allah bless my parents and family, protect them, and grant them lasting health and happiness.
    </div>
  </div>

</div>
