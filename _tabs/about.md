---
icon: fas fa-user
order: 4
title: About Me
permalink: /about/
---

<div class="card mb-4 border-0 shadow-sm" style="background: var(--card-bg, rgba(22, 27, 34, 0.05)); border: 1px solid var(--border-color, rgba(88, 166, 255, 0.15)) !important; border-radius: 14px;">
  <div class="card-body p-4">
    <div class="d-flex flex-column flex-md-row align-items-center gap-4 text-center text-md-start">
      <img src="/assets/images/avatar.jpg" alt="Abdulrahman M. Fathi" class="rounded-circle shadow" style="width: 120px; height: 120px; object-fit: cover; border: 3px solid #58a6ff;">
      <div class="flex-grow-1">
        <h1 class="mb-1" style="font-weight: 700; font-size: 2.1rem; color: var(--heading-color);">Abdulrahman M. Fathi</h1>
        <p class="mb-2" style="font-size: 1.05rem;">
          <strong style="color: #58a6ff;">0x3bdo</strong> &bull; Cyber Security Engineer &amp; Penetration Tester
        </p>
        <p class="text-muted mb-3" style="font-size: 0.92rem;">
          Cairo, Egypt &nbsp;|&nbsp; Web, Mobile, API, Active Directory &amp; Binary Security
        </p>
        <div class="d-flex flex-wrap justify-content-center justify-content-md-start gap-2">
          <a href="https://www.linkedin.com/in/3bdo-fathi" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary btn-sm">
            <i class="fab fa-linkedin me-1"></i> LinkedIn
          </a>
          <a href="https://github.com/3bdo-fathi" target="_blank" rel="noopener noreferrer" class="btn btn-outline-secondary btn-sm">
            <i class="fab fa-github me-1"></i> GitHub
          </a>
          <a href="mailto:abdulrahmanmohamedfathi@gmail.com" class="btn btn-outline-info btn-sm">
            <i class="fas fa-envelope me-1"></i> Email
          </a>
          <a href="/contact-me/" class="btn btn-outline-dark btn-sm">
            <i class="fas fa-paper-plane me-1"></i> Contact
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

### Professional Overview

My journey in offensive security stems from a fundamental curiosity: *understanding how complex software and network systems function beneath high-level abstractions, and engineering practical methods to evaluate and harden their security boundaries.*

Today, I operate as an offensive security engineer and penetration tester. My primary focus centers on uncovering subtle architecture and logic vulnerabilities across modern web ecosystems, mobile applications, distributed APIs, Active Directory infrastructures, and compiled binaries. 

I believe effective penetration testing goes far beyond running automated scanners or checking compliance checkboxes. Automated tools flag common signatures; real-world adversaries understand context, business logic, trust relationships, and system internals. My methodology focuses on chained attack paths—combining minor misconfigurations into high-impact assessments—paired with engineering-driven remediation guidance that addresses root architectural causes.

---

### Core Technical Competencies

<div class="row g-3 my-2">
  <div class="col-md-6">
    <div class="p-3 rounded h-100" style="background: var(--card-bg, rgba(22, 27, 34, 0.03)); border: 1px solid var(--border-color, rgba(88, 166, 255, 0.15));">
      <h5 class="mb-2" style="color: #58a6ff; font-weight: 600;">
        <i class="fas fa-mobile-alt me-2"></i> Mobile Security &amp; Reverse Engineering
      </h5>
      <p class="text-muted small mb-0">
        In-depth auditing of Android and iOS applications. Static bytecode analysis (Smali, DEX), native C/C++ library reverse engineering (`.so`), dynamic instrumentation with Frida, objection, and custom scripts. Bypassing root detection, certificate pinning, and auditing cryptographic workflows.
      </p>
    </div>
  </div>

  <div class="col-md-6">
    <div class="p-3 rounded h-100" style="background: var(--card-bg, rgba(22, 27, 34, 0.03)); border: 1px solid var(--border-color, rgba(88, 166, 255, 0.15));">
      <h5 class="mb-2" style="color: #58a6ff; font-weight: 600;">
        <i class="fas fa-globe me-2"></i> Web Applications &amp; Modern APIs
      </h5>
      <p class="text-muted small mb-0">
        Assessing complex web applications, microservices, and API architectures (REST, GraphQL, gRPC). Specialized in nuanced business logic flaws, Broken Object-Level Authorization (BOLA/IDOR), SSRF targeting cloud metadata, and OAuth 2.0 token flaws.
      </p>
    </div>
  </div>

  <div class="col-md-6">
    <div class="p-3 rounded h-100" style="background: var(--card-bg, rgba(22, 27, 34, 0.03)); border: 1px solid var(--border-color, rgba(88, 166, 255, 0.15));">
      <h5 class="mb-2" style="color: #58a6ff; font-weight: 600;">
        <i class="fas fa-network-wired me-2"></i> Active Directory &amp; Enterprise Red Teaming
      </h5>
      <p class="text-muted small mb-0">
        Internal enterprise penetration testing. Graph-based attack path analysis using BloodHound, Kerberos exploitation (Kerberoasting, AS-REP Roasting), Active Directory Certificate Services (AD CS) template misconfigurations, and lateral movement tradecraft.
      </p>
    </div>
  </div>

  <div class="col-md-6">
    <div class="p-3 rounded h-100" style="background: var(--card-bg, rgba(22, 27, 34, 0.03)); border: 1px solid var(--border-color, rgba(88, 166, 255, 0.15));">
      <h5 class="mb-2" style="color: #58a6ff; font-weight: 600;">
        <i class="fas fa-terminal me-2"></i> Binary Analysis &amp; Automation
      </h5>
      <p class="text-muted small mb-0">
        Reverse engineering compiled x86, x64, and ARM binaries. Dynamic debugging with WinDbg, DbgEng scripting, kernel driver analysis, deobfuscation, and crafting custom offensive automation tooling using Python and Bash.
      </p>
    </div>
  </div>
</div>

---

### Featured Research & Book Summary Series

This blog hosts exhaustive, chapter-by-chapter technical deep-dives into industry-standard cybersecurity reference works:

1. [**Practical Reverse Engineering**](/categories/reverse-engineering/)
   An exhaustive 5-chapter series dissecting x86/x64 and ARM assembly, calling conventions, Windows kernel internals (KPCR, SSDT, IRPs, rootkits), WinDbg automation, and software obfuscation/deobfuscation (CFG flattening, custom VMs, symbolic execution).
2. [**Android Security Internals**](/categories/android-security/)
   A comprehensive 13-chapter breakdown of Nikolay Elenkov's classic work, exploring the Linux kernel sandbox, Binder IPC, permissions architecture, package management, cryptographic providers, device encryption, and root mechanics.
3. [**Social Engineering: The Art of Human Hacking**](/categories/social-engineering/)
   A 9-chapter analysis of Christopher Hadnagy's foundation on psychological attack surfaces, elicitation methodologies, nonverbal communication, persuasion models, and defensive enterprise engineering.

---

### Ongoing Charity & Knowledge Sharing | صدقة جارية وعلم يُنتفع به

<div class="p-4 my-3 rounded" style="background: var(--card-bg, rgba(22, 27, 34, 0.04)); border: 1px solid var(--border-color, rgba(88, 166, 255, 0.2)); border-radius: 12px;">
  <p class="text-center fw-bold mb-2" style="font-size: 1.05rem; color: #58a6ff;">
    هذا العمل صَدَقَةٌ جَارِيَةٌ وعِلْمٌ يُنتَفَعُ به — نسألكم الدعاء بظهر الغيب لي ولوالديّ
  </p>
  <p class="text-center text-muted small mb-3">
    Dedicated as an ongoing charity and enduring knowledge &bull; Please remember me and my family in your prayers
  </p>
  <hr style="border-top: 1px dashed var(--border-color, rgba(88, 166, 255, 0.2)); margin: 12px 0;">
  <p class="small text-muted mb-0" style="line-height: 1.6;">
    Every research paper, architectural breakdown, exploit analysis, and technical guide published on this blog is shared with a sincere intention: to serve as enduring, beneficial knowledge. Cybersecurity knowledge should never be gatekept behind commercial walls. If you find value in these materials, a sincere prayer in absentia for me and my family is all that is requested.
  </p>
</div>

---

### Education & Mentorship

Beyond security assessments, I actively contribute to technical education. I design hands-on simulation environments, author technical tutorials, and mentor developers and aspiring penetration testers. Helping others develop an intuitive understanding of low-level systems and defensive tradecraft remains one of the most rewarding aspects of my work.

If you would like to discuss security research, collaborate on a project, or connect, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) or through the [Contact Page](/contact-me/).
