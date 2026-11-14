---
layout: page
icon: fas fa-compass
order: 3
title: Roadmaps
permalink: /roadmaps/
---

<style>
  .roadmaps-container {
    margin: 0.5rem 0 3.5rem;
  }

  /* Header Title & Intro */
  .roadmaps-header {
    margin-bottom: 1.75rem;
  }

  .roadmaps-page-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  html[data-mode="light"] .roadmaps-page-title,
  html[data-bs-theme="light"] .roadmaps-page-title {
    color: #1f2328 !important;
  }

  .roadmaps-page-subtitle {
    font-size: 0.96rem;
    color: #8b949e;
    line-height: 1.6;
    max-width: 820px;
    margin-bottom: 1.25rem;
  }

  html[data-mode="light"] .roadmaps-page-subtitle,
  html[data-bs-theme="light"] .roadmaps-page-subtitle {
    color: #57606a !important;
  }

  /* Essential Disclaimer Callout */
  .roadmap-disclaimer-card {
    position: relative;
    padding: 1.25rem 1.45rem;
    border-radius: 10px;
    background: rgba(88, 166, 255, 0.05);
    border: 1px solid rgba(88, 166, 255, 0.22);
    border-left: 4px solid #58a6ff;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
  }

  html[data-mode="light"] .roadmap-disclaimer-card,
  html[data-bs-theme="light"] .roadmap-disclaimer-card {
    background: #f0f7ff !important;
    border: 1px solid #c8e1ff !important;
    border-left: 4px solid #0969da !important;
    box-shadow: 0 2px 10px rgba(9, 105, 218, 0.06) !important;
  }

  .disclaimer-badge-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.55rem;
  }

  .disclaimer-badge {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #58a6ff;
    background: rgba(88, 166, 255, 0.12);
    border: 1px solid rgba(88, 166, 255, 0.3);
    padding: 0.18rem 0.55rem;
    border-radius: 4px;
  }

  html[data-mode="light"] .disclaimer-badge,
  html[data-bs-theme="light"] .disclaimer-badge {
    color: #0969da !important;
    background: #ddf4ff !important;
    border-color: rgba(9, 105, 218, 0.3) !important;
  }

  .disclaimer-quote {
    font-size: 0.94rem;
    font-style: italic;
    color: #e6edf3;
    line-height: 1.65;
    margin: 0;
  }

  html[data-mode="light"] .disclaimer-quote,
  html[data-bs-theme="light"] .disclaimer-quote {
    color: #1f2328 !important;
    font-weight: 500;
  }

  .disclaimer-attribution {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-top: 0.65rem;
    font-size: 0.78rem;
    color: #8b949e;
  }

  html[data-mode="light"] .disclaimer-attribution,
  html[data-bs-theme="light"] .disclaimer-attribution {
    color: #57606a !important;
  }

  .disclaimer-attribution a {
    color: #58a6ff;
    text-decoration: none;
    font-weight: 600;
  }

  html[data-mode="light"] .disclaimer-attribution a,
  html[data-bs-theme="light"] .disclaimer-attribution a {
    color: #0969da !important;
  }

  /* Toolbar: Search & Categories */
  .roadmap-toolbar {
    display: flex;
    flex-direction: column;
    gap: 1.15rem;
    margin-bottom: 2rem;
  }

  .roadmap-search-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .roadmap-search-input {
    width: 100%;
    max-width: 440px;
    padding: 0.52rem 0.95rem;
    font-size: 0.88rem;
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

  .roadmap-counter-pill {
    font-size: 0.78rem;
    font-weight: 600;
    color: #8b949e;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 0.3rem 0.75rem;
    border-radius: 20px;
  }

  html[data-mode="light"] .roadmap-counter-pill,
  html[data-bs-theme="light"] .roadmap-counter-pill {
    background: #f6f8fa !important;
    border-color: #d0d7de !important;
    color: #57606a !important;
  }

  .roadmap-filter-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem 0.55rem;
  }

  .rm-filter-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.38rem;
    padding: 0.35rem 0.8rem;
    border-radius: 20px;
    background: #0d0d0d;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #8b949e;
    font-size: 0.78rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
  }

  .rm-filter-btn:hover {
    color: #58a6ff;
    border-color: rgba(88, 166, 255, 0.4);
    background: #141414;
  }

  .rm-filter-btn.active {
    background: #58a6ff !important;
    color: #000000 !important;
    border-color: #58a6ff !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(88, 166, 255, 0.3);
  }

  .rm-filter-btn.btn-featured {
    border-color: rgba(227, 179, 65, 0.4);
    color: #e3b341;
  }

  .rm-filter-btn.btn-featured.active {
    background: #e3b341 !important;
    color: #000000 !important;
    border-color: #e3b341 !important;
    box-shadow: 0 2px 8px rgba(227, 179, 65, 0.3);
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
    box-shadow: 0 2px 8px rgba(9, 105, 218, 0.2);
  }

  html[data-mode="light"] .rm-filter-btn.btn-featured {
    border-color: #d29922 !important;
    color: #9a6700 !important;
  }

  html[data-mode="light"] .rm-filter-btn.btn-featured.active {
    background: #d29922 !important;
    color: #ffffff !important;
  }

  /* Grid Layout for Roadmap Cards */
  .roadmaps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
    gap: 1.25rem;
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
    padding: 1.35rem;
    background: #080808;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
  }

  .roadmap-card:hover {
    transform: translateY(-3px);
    border-color: rgba(88, 166, 255, 0.45);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  }

  .roadmap-card.is-featured {
    border-left: 3px solid #e3b341;
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

  html[data-mode="light"] .roadmap-card.is-featured,
  html[data-bs-theme="light"] .roadmap-card.is-featured {
    border-left: 3px solid #d29922 !important;
  }

  .roadmap-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.85rem;
  }

  .roadmap-icon-box {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
  }

  .card-badges-wrap {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    flex-wrap: wrap;
  }

  .rm-badge {
    font-size: 0.66rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
  }

  .rm-badge-category {
    color: #8b949e;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }

  html[data-mode="light"] .rm-badge-category,
  html[data-bs-theme="light"] .rm-badge-category {
    color: #57606a !important;
    background: #f6f8fa !important;
    border-color: #d0d7de !important;
  }

  .rm-badge-source {
    color: #58a6ff;
    background: rgba(88, 166, 255, 0.1);
    border: 1px solid rgba(88, 166, 255, 0.25);
  }

  html[data-mode="light"] .rm-badge-source,
  html[data-bs-theme="light"] .rm-badge-source {
    color: #0969da !important;
    background: #ddf4ff !important;
    border-color: rgba(9, 105, 218, 0.3) !important;
  }

  .rm-badge-featured {
    color: #e3b341;
    background: rgba(210, 153, 34, 0.12);
    border: 1px solid rgba(210, 153, 34, 0.3);
  }

  html[data-mode="light"] .rm-badge-featured,
  html[data-bs-theme="light"] .rm-badge-featured {
    color: #9a6700 !important;
    background: #fff8c5 !important;
    border-color: rgba(154, 103, 0, 0.35) !important;
  }

  .roadmap-card-title {
    font-size: 1.1rem;
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
    font-size: 0.84rem;
    color: #8b949e;
    line-height: 1.5;
    margin-bottom: 1rem;
  }

  html[data-mode="light"] .roadmap-card-desc,
  html[data-bs-theme="light"] .roadmap-card-desc {
    color: #57606a !important;
  }

  .roadmap-skills-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.32rem;
    margin-bottom: 1.35rem;
  }

  .skill-pill {
    font-size: 0.68rem;
    font-family: ui-monospace, SFMono-Regular, monospace;
    padding: 0.14rem 0.42rem;
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
    padding-top: 0.95rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  html[data-mode="light"] .roadmap-card-actions,
  html[data-bs-theme="light"] .roadmap-card-actions {
    border-top-color: #e1e4e8 !important;
  }

  .rm-external-link-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    width: 100%;
    padding: 0.48rem 1rem;
    font-size: 0.82rem;
    font-weight: 600;
    border-radius: 6px;
    background: rgba(88, 166, 255, 0.1);
    color: #58a6ff !important;
    border: 1px solid rgba(88, 166, 255, 0.3);
    text-decoration: none !important;
    transition: all 0.2s ease;
  }

  .rm-external-link-btn:hover {
    background: #58a6ff;
    color: #000000 !important;
    border-color: #58a6ff;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(88, 166, 255, 0.25);
  }

  html[data-mode="light"] .rm-external-link-btn,
  html[data-bs-theme="light"] .rm-external-link-btn {
    background: #ddf4ff !important;
    color: #0969da !important;
    border-color: rgba(9, 105, 218, 0.3) !important;
  }

  html[data-mode="light"] .rm-external-link-btn:hover,
  html[data-bs-theme="light"] .rm-external-link-btn:hover {
    background: #0969da !important;
    color: #ffffff !important;
    border-color: #0969da !important;
  }

  /* Empty state */
  #roadmaps-empty {
    display: none;
    padding: 3rem 1rem;
    text-align: center;
  }
</style>

<div class="roadmaps-container">
  <!-- Header Title -->
  <div class="roadmaps-header">
    <h1 class="roadmaps-page-title">Cybersecurity Learning Roadmaps</h1>
    <p class="roadmaps-page-subtitle">
      A curated index of community-driven, structured learning paths and skill matrices across offensive security, mobile pentesting, reverse engineering, cloud security, and defensive engineering.
    </p>

    <!-- Essential Guiding Principle Disclaimer -->
    <div class="roadmap-disclaimer-card">
      <div class="disclaimer-badge-row">
        <span class="disclaimer-badge">
          <i class="fas fa-compass me-1"></i> Guiding Principle & Learning Purpose
        </span>
      </div>
      <p class="disclaimer-quote">
        "These roadmaps are not intended to recommend specific courses. Their purpose is to guide you through the required topics and practical skills. You can study from any resources you prefer, but the roadmap helps you identify what you may be missing and what your next steps should be."
      </p>
      <div class="disclaimer-attribution">
        <span>Curated with credit and appreciation to foundational platforms including</span>
        <a href="https://fahemsec.com/roadmaps" target="_blank" rel="noopener noreferrer">FahemSec</a>,
        <a href="https://roadmap.sh/cyber-security" target="_blank" rel="noopener noreferrer">roadmap.sh</a>,
        <span>and</span>
        <a href="https://owasp.org/" target="_blank" rel="noopener noreferrer">OWASP</a>.
      </div>
    </div>
  </div>

  <!-- Filter & Search Toolbar -->
  <div class="roadmap-toolbar">
    <div class="roadmap-search-wrap">
      <input
        type="search"
        id="roadmap-search"
        class="roadmap-search-input"
        placeholder="Filter by title, domain, or technology (e.g. Android, Kerberos, Ghidra)..."
        autocomplete="off"
      />
      <span class="roadmap-counter-pill" id="roadmap-counter">Showing all 18 roadmaps</span>
    </div>

    <div class="roadmap-filter-pills" id="roadmap-filters">
      <button type="button" class="rm-filter-btn active" data-category="all">
        <i class="fas fa-border-all"></i> All (18)
      </button>
      <button type="button" class="rm-filter-btn btn-featured" data-category="featured">
        <i class="fas fa-star"></i> Core Tracks (6)
      </button>
      <button type="button" class="rm-filter-btn" data-category="foundations">
        <i class="fas fa-graduation-cap"></i> Foundations
      </button>
      <button type="button" class="rm-filter-btn" data-category="offensive">
        <i class="fas fa-crosshairs"></i> Offensive Pentesting
      </button>
      <button type="button" class="rm-filter-btn" data-category="mobile">
        <i class="fas fa-mobile-alt"></i> Mobile & AppSec
      </button>
      <button type="button" class="rm-filter-btn" data-category="reverse">
        <i class="fas fa-microchip"></i> Reverse & Binary
      </button>
      <button type="button" class="rm-filter-btn" data-category="cloud">
        <i class="fas fa-cloud"></i> Cloud & DevSecOps
      </button>
      <button type="button" class="rm-filter-btn" data-category="defensive">
        <i class="fas fa-shield-alt"></i> Defensive & DFIR
      </button>
      <button type="button" class="rm-filter-btn" data-category="osint">
        <i class="fas fa-search"></i> OSINT & Crypto
      </button>
    </div>
  </div>

  <!-- Roadmaps Grid (100% English & External Direct Links Only) -->
  <div class="roadmaps-grid" id="roadmaps-grid">

    <!-- 0. Hack The Box Academy Masterclass & Flag Vault (Featured) -->
    <div class="roadmap-card is-featured" data-category="offensive" data-featured="true" data-keywords="hack the box htb academy cpts certified penetration testing specialist active directory privilege escalation web attacks command injection file transfers footprinting flags writeups">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(159, 239, 0, 0.15); color: #9fef00; border: 1px solid rgba(159, 239, 0, 0.35);">
            <i class="fas fa-cube"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-featured" style="background: rgba(159, 239, 0, 0.18); color: #9fef00; border-color: rgba(159, 239, 0, 0.4);"><i class="fas fa-flag"></i> 41-Part Series</span>
            <span class="rm-badge rm-badge-category">HTB & CPTS</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Hack The Box Academy Masterclass & Flag Vault</h2>
        <p class="roadmap-card-desc">
          The definitive 41-part technical field guide covering the entire Hack The Box Certified Penetration Testing Specialist (CPTS) and Web Exploitation syllabus: Getting Started, File Transfers, Web Recon, Footprinting, Linux/Windows Privilege Escalation, Login Brute Forcing, Broken Authentication, Command Injections, File Inclusion (LFI/RFI), Attacking Common Services & Applications, Active Directory Attacks, Enterprise Pivoting, Web Proxies, Shells & Payloads, SQLi Fundamentals & SQLMap, Password Attacks, Server-Side Attacks, API Exploitation, Metasploit, CrackMapExec, Linux/Windows x86 Buffer Overflows, WordPress CMS Hacking, File Uploads, XSS, Web Fuzzing, WSDL/SOAP Attacks, and Complete 802.11 / WEP / WPS Wireless Penetration Testing. Includes 700+ verified lab flags, exploit commands, and 3,600+ lab screenshots.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">HTB Academy & CPTS</span>
          <span class="skill-pill">700+ Flags Solved</span>
          <span class="skill-pill">Active Directory & Kerberos</span>
          <span class="skill-pill">x86 Buffer Overflows</span>
          <span class="skill-pill">Windows/Linux PrivEsc</span>
          <span class="skill-pill">Enterprise Pivoting</span>
          <span class="skill-pill">Web Exploitation & RCE</span>
          <span class="skill-pill">Wireless Pentesting (WEP/WPS)</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="/posts/htb-academy-part-1-getting-started/" class="rm-external-link-btn" style="border-color: rgba(159, 239, 0, 0.4); color: #9fef00;">
          <span>Explore 41-Part HTB Academy Guide</span>
          <i class="fas fa-arrow-right small"></i>
        </a>
      </div>
    </div>

    <!-- 0. eCPPT Penetration Testing Masterclass (Featured) -->
    <div class="roadmap-card is-featured" data-category="offensive" data-featured="true" data-keywords="ecppt ine certified professional penetration tester x86 assembly buffer overflow active directory pivoting c2 web pentesting client side powershell privilege escalation">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.35);">
            <i class="fas fa-shield-alt"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-featured" style="background: rgba(239, 68, 68, 0.18); color: #ef4444; border-color: rgba(239, 68, 68, 0.4);"><i class="fas fa-certificate"></i> 10-Part Series</span>
            <span class="rm-badge rm-badge-category">Offensive</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">eCPPT Penetration Testing Masterclass</h2>
        <p class="roadmap-card-desc">
          An exhaustive, 10-part hands-on guide covering the entire eCPPT syllabus: x86 assembly, stack-based & SEH buffer overflows, network attacks, Active Directory Kerberos exploitation, privilege escalation, multi-tier pivoting (Ligolo-ng), C2 infrastructure, web attacks, client-side weaponization, and PowerShell AMSI evasion.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">x86 & Buffer Overflows</span>
          <span class="skill-pill">Active Directory & Kerberos</span>
          <span class="skill-pill">Multi-Tier Pivoting</span>
          <span class="skill-pill">C2 & Starkiller</span>
          <span class="skill-pill">Privilege Escalation</span>
          <span class="skill-pill">AMSI Memory Patching</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="/posts/ecppt-v3-part-1-system-security-x86-assembly/" class="rm-external-link-btn" style="border-color: rgba(239, 68, 68, 0.4); color: #ef4444;">
          <span>Explore 10-Part eCPPT Guide</span>
          <i class="fas fa-arrow-right small"></i>
        </a>
      </div>
    </div>

    <!-- 1. Cybersecurity Essentials Roadmap (Featured) -->
    <div class="roadmap-card is-featured" data-category="foundations" data-featured="true" data-keywords="essentials foundations networking tcp ip linux cli bash windows internals dns osi security">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border: 1px solid rgba(88, 166, 255, 0.25);">
            <i class="fas fa-graduation-cap"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-featured"><i class="fas fa-star"></i> Core</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Cybersecurity Essentials Roadmap</h2>
        <p class="roadmap-card-desc">
          The essential technical bedrock: Computer networking (OSI model, TCP/IP, DNS, Routing), Linux command line & permission models, Windows OS architecture, and Python scripting.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">OSI & TCP/IP</span>
          <span class="skill-pill">Linux Permissions</span>
          <span class="skill-pill">Windows Internals</span>
          <span class="skill-pill">Python Automation</span>
          <span class="skill-pill">CIA Triad</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/essentials" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 2. Cyber Security Engineer Roadmap (Featured) -->
    <div class="roadmap-card is-featured" data-category="foundations" data-featured="true" data-keywords="roadmap.sh cybersecurity engineer career path security operations networking protocols cryptosystem compliance">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border: 1px solid rgba(88, 166, 255, 0.25);">
            <i class="fas fa-project-diagram"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-featured"><i class="fas fa-star"></i> Core</span>
            <span class="rm-badge rm-badge-source">roadmap.sh</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Cyber Security Engineer Roadmap</h2>
        <p class="roadmap-card-desc">
          Community-curated interactive career roadmap covering security architecture, offensive fundamentals, defense-in-depth, identity management, and governance standards.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Security Architecture</span>
          <span class="skill-pill">Threat Modeling</span>
          <span class="skill-pill">Zero Trust</span>
          <span class="skill-pill">Network Security</span>
          <span class="skill-pill">IAM</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://roadmap.sh/cyber-security" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on roadmap.sh</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 3. Android Security Roadmap (Featured) -->
    <div class="roadmap-card is-featured" data-category="mobile" data-featured="true" data-keywords="android security mobile penetration testing apk reversing smali frida hooking binder ipc masvs apktool jadx">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(63, 185, 80, 0.12); color: #3fb950; border: 1px solid rgba(63, 185, 80, 0.25);">
            <i class="fab fa-android"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-featured"><i class="fas fa-star"></i> Core</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Android Security Roadmap</h2>
        <p class="roadmap-card-desc">
          Comprehensive pathway for Android OS internals, APK reverse engineering (Smali & Jadx), Binder IPC subsystem, Deep Link hijacking, Frida dynamic hooking, and OWASP MASVS.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Binder IPC</span>
          <span class="skill-pill">Smali Patching</span>
          <span class="skill-pill">Frida Hooking</span>
          <span class="skill-pill">Deep Link Hijack</span>
          <span class="skill-pill">OWASP MASVS</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/android-security" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 4. Active Directory Pentesting Roadmap (Featured) -->
    <div class="roadmap-card is-featured" data-category="offensive" data-featured="true" data-keywords="active directory kerberos bloodhound mimikatz kerberoasting pass the ticket ad cs domain admin lateral movement">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(240, 136, 62, 0.12); color: #f0883e; border: 1px solid rgba(240, 136, 62, 0.25);">
            <i class="fas fa-sitemap"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-featured"><i class="fas fa-star"></i> Core</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Active Directory Pentesting Roadmap</h2>
        <p class="roadmap-card-desc">
          Systematic mastery of enterprise Windows environments: Kerberos protocol internals (Kerberoasting, AS-REP Roasting, Delegation), BloodHound graph analysis, AD CS certificate abuse, and Domain compromise.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Kerberos Attacks</span>
          <span class="skill-pill">BloodHound Graphs</span>
          <span class="skill-pill">AD CS Exploitation</span>
          <span class="skill-pill">Kerberoasting</span>
          <span class="skill-pill">Lateral Movement</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/active-directory" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 5. Reverse Engineering Roadmap (Featured) -->
    <div class="roadmap-card is-featured" data-category="reverse" data-featured="true" data-keywords="reverse engineering x86 x64 arm assembly ida pro ghidra windbg x64dbg kernel rootkits deobfuscation pe elf">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(163, 113, 247, 0.12); color: #a371f7; border: 1px solid rgba(163, 113, 247, 0.25);">
            <i class="fas fa-microchip"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-featured"><i class="fas fa-star"></i> Core</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Reverse Engineering Roadmap</h2>
        <p class="roadmap-card-desc">
          Low-level binary analysis mastery: x86/x64 and ARM assembly, calling conventions, PE/ELF executable headers, IDA Pro and Ghidra workflows, WinDbg kernel debugging, and rootkit internals.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">x86/x64 Assembly</span>
          <span class="skill-pill">ARM Architecture</span>
          <span class="skill-pill">IDA Pro & Ghidra</span>
          <span class="skill-pill">WinDbg Kernel</span>
          <span class="skill-pill">Deobfuscation</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/reverse-engineering" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 6. Web Security Roadmap (Featured) -->
    <div class="roadmap-card is-featured" data-category="offensive" data-featured="true" data-keywords="web security owasp top 10 burp suite sqli xss ssrf csrf idor auth bypass api testing">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(248, 81, 73, 0.12); color: #ff7b72; border: 1px solid rgba(248, 81, 73, 0.25);">
            <i class="fas fa-globe"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-featured"><i class="fas fa-star"></i> Core</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Web Security Roadmap</h2>
        <p class="roadmap-card-desc">
          Web application penetration testing: HTTP protocol mechanics, OWASP Top 10 vulnerabilities, Burp Suite mastery, SQL injection, XSS, SSRF, authorization bypass, and business logic flaws.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Burp Suite Pro</span>
          <span class="skill-pill">OWASP Top 10</span>
          <span class="skill-pill">SQLi / XSS / SSRF</span>
          <span class="skill-pill">IDOR Flaws</span>
          <span class="skill-pill">REST / GraphQL</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/web-security" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 7. OWASP Web & API Top 10 Standard -->
    <div class="roadmap-card" data-category="offensive" data-keywords="owasp web api top 10 standard appsec vulnerabilities broken access control injection security misconfiguration">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(248, 81, 73, 0.12); color: #ff7b72; border: 1px solid rgba(248, 81, 73, 0.25);">
            <i class="fas fa-shield-virus"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Web & API</span>
            <span class="rm-badge rm-badge-source">OWASP</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">OWASP Web & API Security Standards</h2>
        <p class="roadmap-card-desc">
          The global consensus standard on the most critical security risks for web applications and modern API architectures, complete with risk models and mitigation controls.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Broken Access Control</span>
          <span class="skill-pill">Cryptographic Failures</span>
          <span class="skill-pill">API Security Top 10</span>
          <span class="skill-pill">Insecure Design</span>
          <span class="skill-pill">Security Logging</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://owasp.org/www-project-top-ten/" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Standards on OWASP.org</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 8. OWASP Mobile Application Security (MASVS & MASTG) -->
    <div class="roadmap-card" data-category="mobile" data-keywords="owasp masvs mastg mobile appsec verification guide android ios testing standards">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(63, 185, 80, 0.12); color: #3fb950; border: 1px solid rgba(63, 185, 80, 0.25);">
            <i class="fas fa-mobile"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Mobile</span>
            <span class="rm-badge rm-badge-source">OWASP</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">OWASP MASVS & MASTG Standards</h2>
        <p class="roadmap-card-desc">
          The authoritative industry standard for mobile app security verification (MASVS) and comprehensive technical testing guide (MASTG) covering Android and iOS platforms.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">MASVS Storage</span>
          <span class="skill-pill">MASVS Crypto</span>
          <span class="skill-pill">Network Security</span>
          <span class="skill-pill">Resilience Testing</span>
          <span class="skill-pill">IPC Security</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://mas.owasp.org/" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Guide on mas.owasp.org</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 9. Binary Exploitation Roadmap -->
    <div class="roadmap-card" data-category="reverse" data-keywords="binary exploitation pwn buffer overflow rop return oriented programming shellcoding gdb pwntools aslr dep">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(248, 81, 73, 0.12); color: #ff7b72; border: 1px solid rgba(248, 81, 73, 0.25);">
            <i class="fas fa-bomb"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Exploit Dev</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Binary Exploitation (PWN) Roadmap</h2>
        <p class="roadmap-card-desc">
          Foundations of user-space exploit development: memory allocation mechanics, stack buffer overflows, ROP gadget chaining, shellcoding, format string flaws, and modern mitigation bypasses.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Stack Overflows</span>
          <span class="skill-pill">ROP Chaining</span>
          <span class="skill-pill">ASLR / DEP Bypass</span>
          <span class="skill-pill">Pwntools & GDB</span>
          <span class="skill-pill">Shellcoding</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/exploitation" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 10. iOS Security Roadmap -->
    <div class="roadmap-card" data-category="mobile" data-keywords="ios security mobile pentesting jailbreak frida objection swift objective c keychain mach o secure enclave">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(200, 200, 200, 0.12); color: #e6edf3; border: 1px solid rgba(200, 200, 200, 0.25);">
            <i class="fab fa-apple"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Mobile</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">iOS Security & Reversing Roadmap</h2>
        <p class="roadmap-card-desc">
          Apple mobile platform security: Mach-O binary dissection, Objective-C/Swift runtime manipulation, jailbreak mechanics, Frida instrumentation, Keychain storage, and Secure Enclave boundaries.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Mach-O Binaries</span>
          <span class="skill-pill">Swift / Obj-C Runtime</span>
          <span class="skill-pill">Keychain Security</span>
          <span class="skill-pill">Jailbreak Detection</span>
          <span class="skill-pill">Frida Hooking</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/ios-pentesting" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 11. Network Pentesting Roadmap -->
    <div class="roadmap-card" data-category="offensive" data-keywords="network pentesting nmap wireshark port scanning vulnerability assessment pivoting lateral movement metasploit">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border: 1px solid rgba(88, 166, 255, 0.25);">
            <i class="fas fa-network-wired"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Network</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Network Pentesting Roadmap</h2>
        <p class="roadmap-card-desc">
          Internal and perimeter network assessment: host enumeration, port scanning with Nmap, service vulnerability analysis, automated exploitation, pivoting techniques, and post-exploitation.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Nmap Scripting Engine</span>
          <span class="skill-pill">Wireshark Analysis</span>
          <span class="skill-pill">Network Pivoting</span>
          <span class="skill-pill">Metasploit</span>
          <span class="skill-pill">Privilege Escalation</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/network-pentesting" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 12. Cloud Security & Pentesting Roadmap -->
    <div class="roadmap-card" data-category="cloud" data-keywords="cloud security pentesting aws azure gcp iam privilege escalation s3 bucket misconfigurations serverless container security">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border: 1px solid rgba(88, 166, 255, 0.25);">
            <i class="fas fa-cloud"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Cloud</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Cloud Pentesting Roadmap</h2>
        <p class="roadmap-card-desc">
          Offensive cloud engineering across AWS, Azure, and Google Cloud Platform: IAM privilege escalation paths, cloud storage misconfigurations, serverless function security, and posture assessment.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">AWS / Azure / GCP</span>
          <span class="skill-pill">IAM Escalation</span>
          <span class="skill-pill">Storage Buckets</span>
          <span class="skill-pill">Serverless Pentesting</span>
          <span class="skill-pill">CSPM Assessment</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/cloud-security" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 13. DevSecOps Roadmap (roadmap.sh) -->
    <div class="roadmap-card" data-category="cloud" data-keywords="devsecops roadmap.sh sast dast iast rasp sca ci cd pipeline security docker kubernetes secrets scanning">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(63, 185, 80, 0.12); color: #3fb950; border: 1px solid rgba(63, 185, 80, 0.25);">
            <i class="fas fa-code-branch"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">DevSecOps</span>
            <span class="rm-badge rm-badge-source">roadmap.sh</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">DevSecOps & Pipeline Security Roadmap</h2>
        <p class="roadmap-card-desc">
          Integrating security into continuous integration and delivery: SAST, DAST, SCA dependency scanning, container image hardening (Docker/Kubernetes), and infrastructure as code (IaC) checks.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">CI/CD Security</span>
          <span class="skill-pill">SAST / DAST / SCA</span>
          <span class="skill-pill">Container Security</span>
          <span class="skill-pill">IaC Scanning</span>
          <span class="skill-pill">Secrets Management</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://roadmap.sh/devops" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on roadmap.sh</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 14. Incident Response & DFIR Roadmap -->
    <div class="roadmap-card" data-category="defensive" data-keywords="incident response dfir digital forensics memory forensics volatility event logs threat hunting blue team">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(63, 185, 80, 0.12); color: #3fb950; border: 1px solid rgba(63, 185, 80, 0.25);">
            <i class="fas fa-user-shield"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Defensive</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Incident Response & DFIR Roadmap</h2>
        <p class="roadmap-card-desc">
          Defensive security operations and forensic methodology: adversary tactics analysis, evidence acquisition, memory analysis (Volatility), event log timeline correlation, and enterprise containment.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Memory Forensics</span>
          <span class="skill-pill">Volatility Engine</span>
          <span class="skill-pill">Log Correlation</span>
          <span class="skill-pill">Threat Hunting</span>
          <span class="skill-pill">Incident Triage</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/incident-response" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 15. OSINT Roadmap -->
    <div class="roadmap-card" data-category="osint" data-keywords="osint open source intelligence reconnaissance shodan dorking digital footprints metadata profiling attribution">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(227, 179, 65, 0.12); color: #e3b341; border: 1px solid rgba(227, 179, 65, 0.25);">
            <i class="fas fa-search-location"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Intelligence</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">OSINT & Intelligence Roadmap</h2>
        <p class="roadmap-card-desc">
          Open Source Intelligence techniques: gathering and analyzing publicly available data, advanced search engine operators, Shodan network intelligence, metadata extraction, and threat attribution.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Search Dorking</span>
          <span class="skill-pill">Shodan Recon</span>
          <span class="skill-pill">Digital Footprinting</span>
          <span class="skill-pill">Metadata Analysis</span>
          <span class="skill-pill">Threat Attribution</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/osint" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 16. OSINT Framework Matrix -->
    <div class="roadmap-card" data-category="osint" data-keywords="osint framework tools matrix intel techniques domain ip geolocation social records darknet">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(227, 179, 65, 0.12); color: #e3b341; border: 1px solid rgba(227, 179, 65, 0.25);">
            <i class="fas fa-project-diagram"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Intelligence</span>
            <span class="rm-badge rm-badge-source">OSINT Framework</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">OSINT Framework Knowledge Base</h2>
        <p class="roadmap-card-desc">
          An exhaustive web-based taxonomy linking to open source intelligence resources, categorizing tools for username search, domain resolution, email verification, darknet, and geolocation.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Domain Resolution</span>
          <span class="skill-pill">IP Geolocation</span>
          <span class="skill-pill">Email Verification</span>
          <span class="skill-pill">Public Records</span>
          <span class="skill-pill">Darknet Search</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://osintframework.com/" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open OSINT Framework</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 17. Cryptography Roadmap -->
    <div class="roadmap-card" data-category="osint" data-keywords="cryptography aes rsa ecc hashing tls certificates math padding oracle public key cryptanalysis">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(163, 113, 247, 0.12); color: #a371f7; border: 1px solid rgba(163, 113, 247, 0.25);">
            <i class="fas fa-key"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Crypto</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Applied Cryptography Roadmap</h2>
        <p class="roadmap-card-desc">
          Mathematical foundations and practical security applications of modern cryptography: symmetric block ciphers (AES), asymmetric key exchange (RSA, ECC), hashing algorithms, and TLS protocols.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">AES & ChaCha20</span>
          <span class="skill-pill">RSA & Elliptic Curves</span>
          <span class="skill-pill">Cryptographic Hashes</span>
          <span class="skill-pill">TLS / PKI</span>
          <span class="skill-pill">Padding Oracles</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/cryptography" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

    <!-- 18. Desktop Application Pentesting Roadmap -->
    <div class="roadmap-card" data-category="offensive" data-keywords="desktop application pentesting thick client dll search hijacking named pipes local memory tampering net c++">
      <div>
        <div class="roadmap-card-top">
          <div class="roadmap-icon-box" style="background: rgba(88, 166, 255, 0.12); color: #58a6ff; border: 1px solid rgba(88, 166, 255, 0.25);">
            <i class="fas fa-desktop"></i>
          </div>
          <div class="card-badges-wrap">
            <span class="rm-badge rm-badge-category">Thick Client</span>
            <span class="rm-badge rm-badge-source">FahemSec</span>
          </div>
        </div>
        <h2 class="roadmap-card-title">Desktop App Pentesting Roadmap</h2>
        <p class="roadmap-card-desc">
          Thick client application security: DLL search-order hijacking, insecure IPC and named pipes, local memory tampering, reverse engineering .NET/C++ desktop software, and privilege escalation.
        </p>
        <div class="roadmap-skills-wrap">
          <span class="skill-pill">Thick Client Architecture</span>
          <span class="skill-pill">DLL Hijacking</span>
          <span class="skill-pill">Insecure IPC</span>
          <span class="skill-pill">Process Memory Tamper</span>
          <span class="skill-pill">.NET & C++ Reversing</span>
        </div>
      </div>
      <div class="roadmap-card-actions">
        <a href="https://fahemsec.com/roadmaps/desktop-app-pentesting" target="_blank" rel="noopener noreferrer" class="rm-external-link-btn">
          <span>Open Roadmap on FahemSec</span>
          <i class="fas fa-external-link-alt small"></i>
        </a>
      </div>
    </div>

  </div>

  <!-- Empty Search Results -->
  <div id="roadmaps-empty">
    <p class="text-muted mb-2">
      <i class="fas fa-search me-1"></i> No learning roadmaps found matching your query.
    </p>
    <button type="button" class="btn btn-sm btn-outline-primary mt-2" id="reset-roadmap-filter">
      Reset Filters & Show All (18)
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
          var isFeatured = card.getAttribute('data-featured') === 'true';
          var cardKeywords = (card.getAttribute('data-keywords') || '').toLowerCase();
          var cardText = (card.textContent || '').toLowerCase();

          var matchesCategory = false;
          if (currentCategory === 'all') {
            matchesCategory = true;
          } else if (currentCategory === 'featured') {
            matchesCategory = isFeatured;
          } else {
            matchesCategory = (cardCategory === currentCategory);
          }

          var matchesSearch = true;
          if (currentSearch.length > 0) {
            var fullSearchPool = cardKeywords + ' ' + cardText;
            matchesSearch = fullSearchPool.indexOf(currentSearch) !== -1;
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
            emptyNotice.style.display = 'block';
          } else {
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
