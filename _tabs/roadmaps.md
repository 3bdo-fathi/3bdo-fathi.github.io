---
layout: page
icon: fas fa-route
order: 3
title: Roadmaps
permalink: /roadmaps/
---

<style>
  .roadmaps-container {
    margin: 0.5rem 0 3rem;
  }

  /* Attribution Hero Banner */
  .fahemsec-attribution-hero {
    position: relative;
    padding: 1.6rem 1.75rem;
    border-radius: 12px;
    background: radial-gradient(circle at 10% 20%, rgba(88, 166, 255, 0.08) 0%, rgba(8, 8, 8, 0.95) 90%);
    border: 1px solid rgba(88, 166, 255, 0.22);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    margin-bottom: 2rem;
  }

  html[data-mode="light"] .fahemsec-attribution-hero,
  html[data-bs-theme="light"] .fahemsec-attribution-hero {
    background: radial-gradient(circle at 10% 20%, rgba(9, 105, 218, 0.06) 0%, #ffffff 90%) !important;
    border: 1px solid #d0d7de !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
  }

  .attribution-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #58a6ff;
    background: rgba(88, 166, 255, 0.12);
    border: 1px solid rgba(88, 166, 255, 0.3);
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    margin-bottom: 0.85rem;
  }

  html[data-mode="light"] .attribution-badge,
  html[data-bs-theme="light"] .attribution-badge {
    color: #0969da !important;
    background: #ddf4ff !important;
    border-color: rgba(9, 105, 218, 0.3) !important;
  }

  .attribution-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  html[data-mode="light"] .attribution-title,
  html[data-bs-theme="light"] .attribution-title {
    color: #1f2328 !important;
  }

  .attribution-desc {
    font-size: 0.9rem;
    color: #8b949e;
    line-height: 1.6;
    margin-bottom: 1.25rem;
  }

  html[data-mode="light"] .attribution-desc,
  html[data-bs-theme="light"] .attribution-desc {
    color: #57606a !important;
  }

  .attribution-action-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .fahemsec-visit-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.82rem;
    font-weight: 600;
    padding: 0.45rem 1rem;
    border-radius: 6px;
    background: #238636;
    color: #ffffff !important;
    text-decoration: none !important;
    transition: all 0.2s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .fahemsec-visit-btn:hover {
    background: #2ea043;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(46, 160, 67, 0.3);
  }

  /* Filter and Search Bar */
  .roadmap-toolbar {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.8rem;
  }

  .roadmap-search-input {
    width: 100%;
    max-width: 420px;
    padding: 0.5rem 0.9rem;
    font-size: 0.86rem;
    border-radius: 8px;
    background: #080808;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #f0f6fc;
    outline: none;
    transition: all 0.2s ease;
  }

  .roadmap-search-input:focus {
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2);
  }

  html[data-mode="light"] .roadmap-search-input,
  html[data-bs-theme="light"] .roadmap-search-input {
    background: #ffffff !important;
    border-color: #d0d7de !important;
    color: #24292f !important;
  }

  .roadmap-filter-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem 0.55rem;
  }

  .rm-filter-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.32rem 0.75rem;
    border-radius: 20px;
    background: #0d0d0d;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #8b949e;
    font-size: 0.78rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .rm-filter-btn:hover {
    color: #58a6ff;
    border-color: rgba(88, 166, 255, 0.4);
    background: #121212;
  }

  .rm-filter-btn.active {
    background: #58a6ff !important;
    color: #000000 !important;
    border-color: #58a6ff !important;
    font-weight: 700 !important;
  }

  html[data-mode="light"] .rm-filter-btn,
  html[data-bs-theme="light"] .rm-filter-btn {
    background: #f6f8fa !important;
    border-color: #d0d7de !important;
    color: #57606a !important;
  }

  html[data-mode="light"] .rm-filter-btn:hover,
  html[data-bs-theme="light"] .rm-filter-btn:hover {
    color: #0969da !important;
    border-color: #0969da !important;
    background: #ffffff !important;
  }

  html[data-mode="light"] .rm-filter-btn.active,
  html[data-bs-theme="light"] .rm-filter-btn.active {
    background: #0969da !important;
    color: #ffffff !important;
    border-color: #0969da !important;
  }

  /* Grid Layout for Roadmap Cards */
  .roadmaps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.15rem;
  }

  @media (max-width: 576px) {
    .roadmaps-grid {
      grid-template-columns: 1fr;
    }
  }

  .roadmap-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 1.25rem;
    background: #080808;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .roadmap-card:hover {
    transform: translateY(-3px);
    border-color: rgba(88, 166, 255, 0.4);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  }

  html[data-mode="light"] .roadmap-card,
  html[data-bs-theme="light"] .roadmap-card {
    background: #ffffff !important;
    border: 1px solid #d0d7de !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
  }

  html[data-mode="light"] .roadmap-card:hover,
  html[data-bs-theme="light"] .roadmap-card:hover {
    border-color: #0969da !important;
    box-shadow: 0 6px 18px rgba(9, 105, 218, 0.12) !important;
  }

  .roadmap-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
  }

  .roadmap-icon-box {
    width: 38px;
    height: 38px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    background: rgba(88, 166, 255, 0.1);
    color: #58a6ff;
    border: 1px solid rgba(88, 166, 255, 0.2);
  }

  .roadmap-category-badge {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    color: #8b949e;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }

  html[data-mode="light"] .roadmap-category-badge,
  html[data-bs-theme="light"] .roadmap-category-badge {
    color: #57606a !important;
    background: #f6f8fa !important;
    border-color: #d0d7de !important;
  }

  .roadmap-card-title {
    font-size: 1.08rem;
    font-weight: 700;
    color: #f0f6fc;
    margin-bottom: 0.45rem;
    line-height: 1.35;
  }

  html[data-mode="light"] .roadmap-card-title,
  html[data-bs-theme="light"] .roadmap-card-title {
    color: #1f2328 !important;
  }

  .roadmap-card-desc {
    font-size: 0.82rem;
    color: #8b949e;
    line-height: 1.5;
    margin-bottom: 0.95rem;
  }

  html[data-mode="light"] .roadmap-card-desc,
  html[data-bs-theme="light"] .roadmap-card-desc {
    color: #57606a !important;
  }

  .roadmap-skills-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    margin-bottom: 1.25rem;
  }

  .skill-pill {
    font-size: 0.68rem;
    font-family: ui-monospace, SFMono-Regular, monospace;
    padding: 0.12rem 0.4rem;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #c9d1d9;
  }

  html[data-mode="light"] .skill-pill,
  html[data-bs-theme="light"] .skill-pill {
    background: #f6f8fa !important;
    border-color: #d0d7de !important;
    color: #24292f !important;
  }

  .roadmap-card-actions {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding-top: 0.85rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  html[data-mode="light"] .roadmap-card-actions,
  html[data-bs-theme="light"] .roadmap-card-actions {
    border-top-color: #e1e4e8 !important;
  }

  .rm-btn-primary {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    padding: 0.42rem 0.8rem;
    font-size: 0.78rem;
    font-weight: 600;
    border-radius: 6px;
    background: rgba(88, 166, 255, 0.1);
    color: #58a6ff !important;
    border: 1px solid rgba(88, 166, 255, 0.3);
    text-decoration: none !important;
    transition: all 0.2s ease;
  }

  .rm-btn-primary:hover {
    background: #58a6ff;
    color: #000000 !important;
    border-color: #58a6ff;
  }

  html[data-mode="light"] .rm-btn-primary,
  html[data-bs-theme="light"] .rm-btn-primary {
    background: #ddf4ff !important;
    color: #0969da !important;
    border-color: rgba(9, 105, 218, 0.3) !important;
  }

  html[data-mode="light"] .rm-btn-primary:hover,
  html[data-bs-theme="light"] .rm-btn-primary:hover {
    background: #0969da !important;
    color: #ffffff !important;
    border-color: #0969da !important;
  }

  .rm-btn-secondary {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    padding: 0.38rem 0.8rem;
    font-size: 0.76rem;
    font-weight: 500;
    border-radius: 6px;
    background: transparent;
    color: #8b949e !important;
    border: 1px solid rgba(255, 255, 255, 0.08);
    text-decoration: none !important;
    transition: all 0.2s ease;
  }

  .rm-btn-secondary:hover {
    color: #f0f6fc !important;
    border-color: rgba(255, 255, 255, 0.25);
    background: rgba(255, 255, 255, 0.04);
  }

  html[data-mode="light"] .rm-btn-secondary,
  html[data-bs-theme="light"] .rm-btn-secondary {
    color: #57606a !important;
    border-color: #d0d7de !important;
  }

  html[data-mode="light"] .rm-btn-secondary:hover,
  html[data-bs-theme="light"] .rm-btn-secondary:hover {
    color: #1f2328 !important;
    border-color: #afb8c1 !important;
    background: #f6f8fa !important;
  }
</style>

<div class="roadmaps-container">
  <!-- FahemSec Attribution Banner -->
  <div class="fahemsec-attribution-hero">
    <div class="attribution-badge">
      <i class="fas fa-handshake"></i> Community Attribution & Credits
    </div>
    <h1 class="attribution-title">Cybersecurity Learning Roadmaps</h1>
    <p class="attribution-desc">
      مسارات تعليمية مهيكلة تهدف إلى إرشاد المتعلمين والباحثين الأمنيين خلال رحلتهم من الأساسيات حتى الاحتراف، تم إعدادها وتوثيقها بالرجوع والإسناد الكامل لمنصة <strong><a href="https://fahemsec.com/roadmaps" target="_blank" rel="noopener noreferrer">FahemSec</a></strong> الرائدة في التدريب الأمني العربي، وربطها بالمقالات والشروحات والتحليلات المتوفرة على مدونة <strong>0x3bdo</strong>.
    </p>
    <div class="attribution-action-row">
      <a href="https://fahemsec.com/roadmaps" target="_blank" rel="noopener noreferrer" class="fahemsec-visit-btn">
        <i class="fas fa-external-link-alt"></i> Visit FahemSec Official Roadmaps
      </a>
      <span class="text-muted small">
        <i class="fas fa-check-circle text-success me-1"></i> Interactive Node-Based Maps & Guided Topics
      </span>
    </div>
  </div>

  <!-- Filter & Search Toolbar -->
  <div class="roadmap-toolbar">
    <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
      <input
        type="search"
        id="roadmap-search"
        class="roadmap-search-input"
        placeholder="Search roadmaps by domain or skill (e.g. Android, Frida, Active Directory)..."
      />
      <span class="text-muted small" id="roadmap-counter">Showing all 13 roadmaps</span>
    </div>

    <div class="roadmap-filter-pills" id="roadmap-filters">
      <button type="button" class="rm-filter-btn active" data-category="all">
        <i class="fas fa-border-all"></i> All Roadmaps (13)
      </button>
      <button type="button" class="rm-filter-btn" data-category="mobile">
        <i class="fas fa-mobile-alt"></i> Mobile Security (2)
      </button>
      <button type="button" class="rm-filter-btn" data-category="reverse">
        <i class="fas fa-microchip"></i> Reverse & Binary (2)
      </button>
      <button type="button" class="rm-filter-btn" data-category="offensive">
        <i class="fas fa-shield-virus"></i> Offensive Pentesting (5)
      </button>
      <button type="button" class="rm-filter-btn" data-category="foundations">
        <i class="fas fa-graduation-cap"></i> Foundations (1)
      </button>
      <button type="button" class="rm-filter-btn" data-category="appsec">
        <i class="fas fa-lock"></i> AppSec & Crypto (2)
      </button>
      <button type="button" class="rm-filter-btn" data-category="defensive">
        <i class="fas fa-user-shield"></i> Defensive & IR (1)
      </button>
    </div>
  </div>

  <!-- Roadmaps Grid -->
  <div class="roadmaps-grid" id="roadmaps-grid">
    <!-- 1. Android Security Roadmap -->
    <div class="roadmap-card" data-category="mobile" data-keywords="android security mobile pentesting frida smali jadx binder ipc masvs apk drozer">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(63, 185, 80, 0.12); color: #3fb950; border-color: rgba(63, 185, 80, 0.3);">
            <i class="fab fa-android"></i>
          </div>
          <span class="roadmap-category-badge">Mobile Security</span>
        </div>
        <h2 class="roadmap-card-title">Android Security Roadmap</h2>
        <p class="roadmap-card-desc">
          Master Android OS security architecture, reverse engineering APKs, IPC exploitation, Binder boundaries, Frida hooking, and OWASP MASVS compliance.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Linux Kernel / UID</span>
          <span class="skill-pill">Binder IPC</span>
          <span class="skill-pill">Smali & APKTool</span>
          <span class="skill-pill">Frida Instrumentation</span>
          <span class="skill-pill">OWASP MASVS</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/android-security" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
        <a href="{{ '/categories/android-security/' | relative_url }}" class="rm-btn-secondary">
          <i class="fas fa-book-open"></i> Read 0x3bdo Series (17 Parts) &rarr;
        </a>
      </div>
    </div>

    <!-- 2. Reverse Engineering Roadmap -->
    <div class="roadmap-card" data-category="reverse" data-keywords="reverse engineering assembly x86 x64 arm ida pro ghidra windbg x64dbg malware analysis">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(163, 113, 247, 0.12); color: #a371f7; border-color: rgba(163, 113, 247, 0.3);">
            <i class="fas fa-microchip"></i>
          </div>
          <span class="roadmap-category-badge">Reverse Engineering</span>
        </div>
        <h2 class="roadmap-card-title">Reverse Engineering Roadmap</h2>
        <p class="roadmap-card-desc">
          Master low-level programming, x86/x64 and ARM assembly, binary formats (PE/ELF), disassemblers (IDA Pro & Ghidra), and Windows kernel rootkit analysis.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">x86 / x64 Assembly</span>
          <span class="skill-pill">ARM Architecture</span>
          <span class="skill-pill">IDA Pro & Ghidra</span>
          <span class="skill-pill">WinDbg & x64dbg</span>
          <span class="skill-pill">Kernel Rootkits</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/reverse-engineering" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
        <a href="{{ '/categories/reverse-engineering/' | relative_url }}" class="rm-btn-secondary">
          <i class="fas fa-book-open"></i> Read 0x3bdo Series (5 Parts) &rarr;
        </a>
      </div>
    </div>

    <!-- 3. Active Directory Pentesting Roadmap -->
    <div class="roadmap-card" data-category="offensive" data-keywords="active directory kerberos bloodhound mimikatz kerberoasting pass the ticket ad cs domain admin">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(240, 136, 62, 0.12); color: #f0883e; border-color: rgba(240, 136, 62, 0.3);">
            <i class="fas fa-sitemap"></i>
          </div>
          <span class="roadmap-category-badge">Offensive Pentesting</span>
        </div>
        <h2 class="roadmap-card-title">Active Directory Pentesting Roadmap</h2>
        <p class="roadmap-card-desc">
          Master graph-based attack paths in Windows enterprise environments, Kerberos attacks (Roasting, Delegation), BloodHound mapping, and Domain Admin takeover.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Kerberos Authentication</span>
          <span class="skill-pill">BloodHound Graph Analysis</span>
          <span class="skill-pill">Kerberoasting / AS-REP</span>
          <span class="skill-pill">AD CS Certificate Abuse</span>
          <span class="skill-pill">Lateral Movement</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/active-directory" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
        <a href="{{ '/categories/cyber-security/' | relative_url }}" class="rm-btn-secondary">
          <i class="fas fa-book-open"></i> Read Related AD Write-ups &rarr;
        </a>
      </div>
    </div>

    <!-- 4. Essentials Roadmap -->
    <div class="roadmap-card" data-category="foundations" data-keywords="essentials foundations networking tcp ip linux bash python basic scripting routing dns">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border-color: rgba(88, 166, 255, 0.3);">
            <i class="fas fa-graduation-cap"></i>
          </div>
          <span class="roadmap-category-badge">Foundations</span>
        </div>
        <h2 class="roadmap-card-title">Cybersecurity Essentials Roadmap</h2>
        <p class="roadmap-card-desc">
          Build essential technical foundations: Computer networks (OSI, TCP/IP, DNS, Routing), Linux command line & permissions, Windows internals, and Python automation.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">OSI & TCP/IP Model</span>
          <span class="skill-pill">Linux CLI & Permissions</span>
          <span class="skill-pill">Windows Architecture</span>
          <span class="skill-pill">Python Automation</span>
          <span class="skill-pill">Security Fundamentals</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/essentials" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
        <a href="{{ '/categories/python/' | relative_url }}" class="rm-btn-secondary">
          <i class="fas fa-book-open"></i> Python Automation Guides &rarr;
        </a>
      </div>
    </div>

    <!-- 5. Network Pentesting Roadmap -->
    <div class="roadmap-card" data-category="offensive" data-keywords="network pentesting nmap wireshark pivoting lateral movement port scanning exploitation metasploit">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border-color: rgba(88, 166, 255, 0.3);">
            <i class="fas fa-network-wired"></i>
          </div>
          <span class="roadmap-category-badge">Offensive Pentesting</span>
        </div>
        <h2 class="roadmap-card-title">Network Pentesting Roadmap</h2>
        <p class="roadmap-card-desc">
          Master external and internal infrastructure assessment: host discovery, port scanning with Nmap, vulnerability identification, exploitation, pivoting, and pivoting.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Nmap Scanning Engine</span>
          <span class="skill-pill">Wireshark Packet Analysis</span>
          <span class="skill-pill">Metasploit Framework</span>
          <span class="skill-pill">Network Pivoting</span>
          <span class="skill-pill">Privilege Escalation</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/network-pentesting" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
        <a href="{{ '/categories/network-security/' | relative_url }}" class="rm-btn-secondary">
          <i class="fas fa-book-open"></i> Read Network Security Guides &rarr;
        </a>
      </div>
    </div>

    <!-- 6. OSINT Roadmap -->
    <div class="roadmap-card" data-category="offensive" data-keywords="osint open source intelligence shodan reconnaissance footprinting maltego dorking dark web">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(227, 179, 65, 0.12); color: #e3b341; border-color: rgba(227, 179, 65, 0.3);">
            <i class="fas fa-search-location"></i>
          </div>
          <span class="roadmap-category-badge">Intelligence & Recon</span>
        </div>
        <h2 class="roadmap-card-title">OSINT Roadmap</h2>
        <p class="roadmap-card-desc">
          Open Source Intelligence: gathering and analyzing publicly available data, search engine dorking, Shodan recon, social media profiling, and digital footprinting.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Google & Shodan Dorking</span>
          <span class="skill-pill">Digital Footprinting</span>
          <span class="skill-pill">Social Profiling</span>
          <span class="skill-pill">Metadata Analysis</span>
          <span class="skill-pill">Dark Web Attribution</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/osint" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
        <a href="{{ '/posts/from-dark-web-fame-to-digital-attribution/' | relative_url }}" class="rm-btn-secondary">
          <i class="fas fa-book-open"></i> Read OSINT & Attribution Case Study &rarr;
        </a>
      </div>
    </div>

    <!-- 7. Web Security Roadmap -->
    <div class="roadmap-card" data-category="offensive" data-keywords="web security owasp burp suite sql injection xss ssrf csrf idor api testing appsec">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(248, 81, 73, 0.12); color: #ff7b72; border-color: rgba(248, 81, 73, 0.3);">
            <i class="fas fa-globe"></i>
          </div>
          <span class="roadmap-category-badge">Offensive Pentesting</span>
        </div>
        <h2 class="roadmap-card-title">Web Security Roadmap</h2>
        <p class="roadmap-card-desc">
          Master web application security: HTTP/S protocol internals, OWASP Top 10 vulnerabilities, authentication bypass, SQL injection, XSS, SSRF, and business logic flaws.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Burp Suite Pro</span>
          <span class="skill-pill">OWASP Top 10</span>
          <span class="skill-pill">SQLi / XSS / SSRF</span>
          <span class="skill-pill">IDOR & Auth Bypass</span>
          <span class="skill-pill">REST / GraphQL APIs</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/web-security" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
        <a href="{{ '/categories/application-security/' | relative_url }}" class="rm-btn-secondary">
          <i class="fas fa-book-open"></i> Read AppSec Write-ups &rarr;
        </a>
      </div>
    </div>

    <!-- 8. Cloud Pentesting Roadmap -->
    <div class="roadmap-card" data-category="offensive" data-keywords="cloud security aws azure gcp iam privilege escalation s3 bucket misconfiguration lambda serverless">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border-color: rgba(88, 166, 255, 0.3);">
            <i class="fas fa-cloud"></i>
          </div>
          <span class="roadmap-category-badge">Offensive Pentesting</span>
        </div>
        <h2 class="roadmap-card-title">Cloud Pentesting Roadmap</h2>
        <p class="roadmap-card-desc">
          Systematic learning of cloud architectures, offensive techniques, and penetration testing across AWS, Azure, and Google Cloud Platform infrastructures.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">AWS / Azure / GCP</span>
          <span class="skill-pill">IAM Escalation Paths</span>
          <span class="skill-pill">Storage Misconfigurations</span>
          <span class="skill-pill">Serverless & Container Pentest</span>
          <span class="skill-pill">Cloud Security Posture</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/cloud-security" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
      </div>
    </div>

    <!-- 9. Binary Exploitation Roadmap -->
    <div class="roadmap-card" data-category="reverse" data-keywords="binary exploitation pwn buffer overflow rop chain shellcode memory corruption format string aslr dep">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(248, 81, 73, 0.12); color: #ff7b72; border-color: rgba(248, 81, 73, 0.3);">
            <i class="fas fa-bomb"></i>
          </div>
          <span class="roadmap-category-badge">Binary Exploitation</span>
        </div>
        <h2 class="roadmap-card-title">Binary Exploitation Roadmap</h2>
        <p class="roadmap-card-desc">
          Foundations of binary exploitation: memory architecture, stack buffer overflows, Return-Oriented Programming (ROP), shellcoding, and bypassing ASLR/DEP.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Stack Overflows</span>
          <span class="skill-pill">ROP Gadget Chaining</span>
          <span class="skill-pill">Format String Exploits</span>
          <span class="skill-pill">ASLR / DEP Bypass</span>
          <span class="skill-pill">GDB & Pwntools</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/exploitation" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
      </div>
    </div>

    <!-- 10. iOS Security Roadmap -->
    <div class="roadmap-card" data-category="mobile" data-keywords="ios security mobile pentesting jailbreak frida objection swift objective c keychain mach o">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(200, 200, 200, 0.12); color: #e6edf3; border-color: rgba(200, 200, 200, 0.3);">
            <i class="fab fa-apple"></i>
          </div>
          <span class="roadmap-category-badge">Mobile Security</span>
        </div>
        <h2 class="roadmap-card-title">iOS Security Roadmap</h2>
        <p class="roadmap-card-desc">
          Systematic learning of iOS application security, Mach-O binaries, Objective-C/Swift runtime manipulation, jailbreak mechanics, and Frida hooking.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Mach-O Binary Format</span>
          <span class="skill-pill">Swift / Obj-C Runtime</span>
          <span class="skill-pill">Jailbreak Detection Bypass</span>
          <span class="skill-pill">Keychain & Secure Enclave</span>
          <span class="skill-pill">Frida Instrumentation</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/ios-pentesting" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
      </div>
    </div>

    <!-- 11. Incident Response Roadmap -->
    <div class="roadmap-card" data-category="defensive" data-keywords="incident response forensics dfir memory analysis volatility triage event logs threat hunting blue team">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(63, 185, 80, 0.12); color: #3fb950; border-color: rgba(63, 185, 80, 0.3);">
            <i class="fas fa-user-shield"></i>
          </div>
          <span class="roadmap-category-badge">Defensive & IR</span>
        </div>
        <h2 class="roadmap-card-title">Incident Response Roadmap</h2>
        <p class="roadmap-card-desc">
          Systematic learning of attacker techniques, evidence collection, memory forensics (Volatility), timeline analysis, threat hunting, and enterprise containment.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Memory Forensics</span>
          <span class="skill-pill">Windows Event Logs</span>
          <span class="skill-pill">Volatility Framework</span>
          <span class="skill-pill">Threat Hunting</span>
          <span class="skill-pill">Incident Containment</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/incident-response" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
      </div>
    </div>

    <!-- 12. Cryptography Roadmap -->
    <div class="roadmap-card" data-category="appsec" data-keywords="cryptography aes rsa ecc hashing tls certificates math padding oracle public key">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(163, 113, 247, 0.12); color: #a371f7; border-color: rgba(163, 113, 247, 0.3);">
            <i class="fas fa-key"></i>
          </div>
          <span class="roadmap-category-badge">Cryptography</span>
        </div>
        <h2 class="roadmap-card-title">Cryptography Roadmap</h2>
        <p class="roadmap-card-desc">
          Mathematical foundations and practical implementation of cryptographic primitives: AES, RSA, ECC, digital signatures, hashing, and protocol weaknesses.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Symmetric & Asymmetric</span>
          <span class="skill-pill">RSA & Elliptic Curves (ECC)</span>
          <span class="skill-pill">Hash Functions (SHA/MD)</span>
          <span class="skill-pill">TLS / PKI Infrastructure</span>
          <span class="skill-pill">Cryptanalysis & Padding Oracle</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/cryptography" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
      </div>
    </div>

    <!-- 13. Desktop App Pentesting Roadmap -->
    <div class="roadmap-card" data-category="offensive" data-keywords="desktop pentesting thick client dll hijacking named pipes reverse engineering net c++ privilege escalation">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border-color: rgba(88, 166, 255, 0.3);">
            <i class="fas fa-desktop"></i>
          </div>
          <span class="roadmap-category-badge">Offensive Pentesting</span>
        </div>
        <h2 class="roadmap-card-title">Desktop App Pentesting Roadmap</h2>
        <p class="roadmap-card-desc">
          Thick client application security: DLL search-order hijacking, insecure IPC and named pipes, local memory tampering, and privilege escalation vulnerabilities.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Thick Client Architecture</span>
          <span class="skill-pill">DLL Hijacking</span>
          <span class="skill-pill">Insecure IPC & Named Pipes</span>
          <span class="skill-pill">Process Memory Tampering</span>
          <span class="skill-pill">.NET & C++ Reversing</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/desktop-app-pentesting" target="_blank" rel="noopener noreferrer" class="rm-btn-primary">
          <i class="fas fa-external-link-alt"></i> Open on FahemSec
        </a>
      </div>
    </div>
  </div>

  <div id="roadmaps-empty" class="text-center py-5 d-none text-muted">
    <p class="mb-2"><i class="fas fa-search me-1"></i> No roadmaps matched your filter or search query.</p>
    <button type="button" class="btn btn-sm btn-outline-primary mt-2" id="reset-roadmap-filter">
      Reset Filter & Show All
    </button>
  </div>
</div>

<script>
  (function () {
    function initRoadmaps() {
      var filterBtns = document.querySelectorAll('.rm-filter-btn');
      var searchInput = document.getElementById('roadmap-search');
      var cards = Array.from(document.querySelectorAll('.roadmap-card'));
      var counter = document.getElementById('roadmap-counter');
      var emptyNotice = document.getElementById('roadmaps-empty');
      var resetBtn = document.getElementById('reset-roadmap-filter');

      if (!cards.length) return;

      var currentCategory = 'all';
      var currentSearch = '';

      function applyFilter() {
        var visibleCount = 0;

        cards.forEach(function (card) {
          var cardCategory = (card.getAttribute('data-category') || '').toLowerCase();
          var cardKeywords = (card.getAttribute('data-keywords') || '').toLowerCase();
          var cardTitle = (card.querySelector('.roadmap-card-title') ? card.querySelector('.roadmap-card-title').textContent : '').toLowerCase();
          var cardDesc = (card.querySelector('.roadmap-card-desc') ? card.querySelector('.roadmap-card-desc').textContent : '').toLowerCase();

          var matchesCategory = (currentCategory === 'all') || (cardCategory === currentCategory);
          var matchesSearch = true;

          if (currentSearch.length > 0) {
            var fullText = (cardKeywords + ' ' + card.textContent).toLowerCase();
            matchesSearch = fullText.indexOf(currentSearch) !== -1;
          }

          if (matchesCategory && matchesSearch) {
            card.style.display = 'flex';
            visibleCount++;
          } else {
            card.style.display = 'none';
          }
        });

        if (counter) {
          if (visibleCount === cards.length) {
            counter.textContent = 'Showing all ' + visibleCount + ' roadmaps';
          } else {
            counter.textContent = 'Showing ' + visibleCount + ' of ' + cards.length + ' roadmaps';
          }
        }

        if (emptyNotice) {
          if (visibleCount === 0) {
            emptyNotice.classList.remove('d-none');
            emptyNotice.style.display = 'block';
          } else {
            emptyNotice.classList.add('d-none');
            emptyNotice.style.display = 'none';
          }
        }
      }

      filterBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          filterBtns.forEach(function (b) { b.classList.remove('active'); });
          btn.classList.add('active');
          currentCategory = (btn.getAttribute('data-category') || 'all').toLowerCase();
          applyFilter();
        });
      });

      if (searchInput) {
        searchInput.addEventListener('input', function () {
          currentSearch = searchInput.value.trim().toLowerCase();
          applyFilter();
        });
      }

      if (resetBtn) {
        resetBtn.addEventListener('click', function () {
          currentCategory = 'all';
          currentSearch = '';
          if (searchInput) searchInput.value = '';
          filterBtns.forEach(function (b) {
            if (b.getAttribute('data-category') === 'all') {
              b.classList.add('active');
            } else {
              b.classList.remove('active');
            }
          });
          applyFilter();
        });
      }
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initRoadmaps);
    } else {
      initRoadmaps();
    }
  })();
</script>
