---
icon: fas fa-user
order: 4
title: About Me
permalink: /about/
---

<div class="mb-4">
  <h1 class="mb-1" style="color: #f0f6fc; font-weight: 700; font-size: 2.2rem;">Abdulrahman M. Fathi</h1>
  <p class="text-muted mb-2" style="font-size: 1.1rem;">
    <strong style="color: #58a6ff;">0x3bdo</strong> | Cyber Security Engineer & Penetration Tester
  </p>
  <p class="text-secondary mb-3" style="font-size: 0.95rem;">
    Cairo, Egypt &nbsp;|&nbsp; Web, Mobile, API & Infrastructure Security Assessments
  </p>
  <div class="d-flex flex-wrap gap-2">
    <a href="https://www.linkedin.com/in/3bdo-fathi" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary btn-sm">
      <i class="fab fa-linkedin me-1"></i> LinkedIn
    </a>
    <a href="https://github.com/3bdo-fathi" target="_blank" rel="noopener noreferrer" class="btn btn-outline-dark btn-sm">
      <i class="fab fa-github me-1"></i> GitHub
    </a>
    <a href="mailto:abdulrahmanmohamedfathi@gmail.com" class="btn btn-outline-info btn-sm">
      <i class="fas fa-envelope me-1"></i> Email
    </a>
    <a href="/contact-me/" class="btn btn-outline-secondary btn-sm">
      <i class="fas fa-paper-plane me-1"></i> Contact Page
    </a>
  </div>
</div>

---

### الغاية والرسالة: صدقةٌ جارية وعِلمٌ يُنتَفَعُ به
#### Core Purpose: Enduring Knowledge & Ongoing Charity

> عَنْ أَبِي هُرَيْرَةَ رَضِيَ اللَّهُ عَنْهُ، أَنَّ رَسُولَ اللَّهِ ﷺ قَالَ:  
> **«إِذَا مَاتَ الْإِنْسَانُ انْقَطَعَ عَنْهُ عَمَلُهُ إِلَّا مِنْ ثَلَاثَةٍ: إِلَّا مِنْ صَدَقَةٍ جَارِيَةٍ، أَوْ عِلْمٍ يُنْتَفَعُ بِهِ، أَوْ وَلَدٍ صَالِحٍ يَدْعُو لَهُ»**  
> *(رواه مسلم)*
>
> ---
>
> Abu Hurairah (may Allah be pleased with him) reported that the Messenger of Allah (peace be upon him) said:  
> **"When a human being dies, all their deeds come to an end except for three: an ongoing charity, beneficial knowledge, or a righteous child who prays for them."**  
> *(Narrated by Muslim)*

كل ما يُنشر في هذه المدونة — من أبحاث تقنية، وتلخيصات للكتب التخصصية، ومخططات معمارية، وتحليلات أمنية، وأدوات برمجية — تم إعداده بنية خالصة وصادقة: **أن يكون عِلْمًا يُنتَفَعُ به وصَدَقَةً جاريةً عني وعن والديّ وأهلي**، ليبقى هذا المحتوى أثرًا طيبًا ومرجعًا نافعًا لكل باحث وطالب علم في هذا المجال حتى بعد أن ألقى الله وانقطاع عملي.

إن زكاة العلم نشره وبذله للناس، ومجال الأمن السيبراني يجب ألا يُحتكر أو يُحجب خلف أسوار مادية. ورجائي الوحيد من كل قارئ وباحث يستفيد من أي محتوى أو تحليل كُتب هنا أن يذكرني وأهلي بصالح الدعاء بظهر الغيب.

---

Everything published across this blog—every technical breakdown, architectural diagram, exploit analysis, and security guide—is shared with a singular, sincere intention: **to serve as enduring beneficial knowledge and an ongoing charity (Sadaqah Jariyah)** that continues to assist students, engineers, and researchers long after my time in this world.

Information security shouldn't be hidden behind paywalls or obscure corporate silos. Documenting and sharing knowledge unconditionally is my personal mission and lasting contribution. If you ever find value in this research, please remember me and my family in your sincere prayers.

---

### Hello, I'm Abdulrahman M. Fathi

My journey in cybersecurity started with a fundamental question: *"How do complex digital systems actually work under the hood, and how can they be broken or resiliently defended?"*

What began as an insatiable curiosity quickly transformed into a deep, lasting passion and a full-time commitment to offensive security. Today, I operate as an offensive security engineer and penetration tester, focusing on uncovering hidden attack vectors, understanding complex application workflows, and helping organizations fortify their defenses by actively thinking like an adversary.

---

### Philosophy & The Offensive Mindset

True security cannot be evaluated through automated point-and-click scanners or superficial compliance checklists. Automated tools identify known signatures and superficial misconfigurations; real human adversaries understand context, business logic, system architecture, and trust boundaries.

My objective on every assessment is to adopt the perspective of a creative, persistent adversary—identifying subtle, overlooked anomalies, chaining seemingly minor logic flaws into full-impact compromises, and treating systems as interconnected living architectures rather than isolated endpoints.

Every assessment concludes not merely with a list of vulnerabilities, but with practical, engineering-driven remediation roadmaps designed to help developers and infrastructure teams eliminate security weaknesses at their architectural root.

---

### What Drives My Technical Work

My technical focus spans the full spectrum of offensive security, driven by hands-on experimentation, reverse engineering, and deep protocol analysis:

* **Mobile Security & Binary Dissection**: A profound fascination with mobile operating system internals, primarily Android architecture and iOS ecosystems. I spend extensive time analyzing compiled DEX bytecode, reading Smali, auditing native shared libraries (`.so`), and understanding low-level IPC mechanics (such as Android Binder and Content Providers). Utilizing dynamic instrumentation frameworks like **Frida**, **Objection**, and **Medusa**, I examine application behavior at runtime, bypass SSL Pinning, defeat integrity and root detection mechanisms, and audit cryptographic implementations.
* **Web Applications & Modern API Ecosystems**: In-depth security assessments of complex web applications, microservices architectures, and modern API endpoints (REST, GraphQL, OAuth 2.0). My focus lies in uncovering nuanced business logic flaws, Broken Object-Level Authorization (BOLA/IDOR), Server-Side Request Forgery (SSRF) targeting cloud metadata services, and subtle session management vulnerabilities.
* **Enterprise Infrastructure & Active Directory Red Teaming**: Dissecting corporate enterprise environments through graph-based attack path analysis, identity exploitation (such as Kerberoasting, AS-REP Roasting, and Pass-the-Hash), and enumerating Active Directory Certificate Services (AD CS) template misconfigurations to understand how adversaries maneuver across complex networks.
* **Offensive Tooling & Automation**: Crafting purpose-built automation pipelines and reconnaissance tools in **Python** and **Bash** to streamline discovery, automate repetitive assessment tasks, and map wide attack surfaces.

---

### Beyond Technical Assessments: Education & Mentorship

Beyond performing penetration tests and vulnerability research, one of the most rewarding dimensions of my work is **cybersecurity education and mentorship**.

I actively dedicate time to designing and delivering cybersecurity training courses, creating realistic hands-on simulation labs, and mentoring aspiring practitioners and developers. Demystifying complex technical topics—whether it is mobile reverse engineering, memory hooking, or network exploitation—and helping others develop their technical intuition and break into offensive security is a continuous source of inspiration.

---

### Why This Blog Exists

This blog is my personal technical workshop and living digital garden—a space where I document real-world penetration testing insights, chapter-by-chapter dissections of classic cybersecurity texts (such as *Android Security Internals* and *Social Engineering: The Art of Human Hacking*), vulnerability research, automation scripts, and practical lessons learned from the field.

This is not a commercial portfolio. It is an enduring, growing archive of knowledge, open unconditionally to anyone seeking to learn, build, and defend.

---

**Thank you for visiting.**  
Whether you are just taking your first steps into cybersecurity or are already deep in the field, I hope you find something here that inspires your journey and sharpens your craft.

*Abdulrahman M. Fathi (0x3bdo)*
