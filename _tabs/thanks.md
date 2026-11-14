---
layout: page
icon: fas fa-heart
order: 6
title: Thanks & Recognition
permalink: /thanks/
hide_stats: true
---

<style>
  .thanks-container {
    max-width: 860px;
    margin: 0.25rem auto 3rem;
  }

  /* ── Header Banner ── */
  .thanks-hero {
    position: relative;
    padding: 1.6rem 1.75rem;
    border-radius: 12px;
    background: #000000;
    border: 1px solid #2f3336;
    box-shadow: 0 4px 18px rgba(1, 4, 9, 0.4);
    margin-bottom: 1.75rem;
  }

  html[data-mode="light"] .thanks-hero,
  html[data-bs-theme="light"] .thanks-hero {
    background: #ffffff;
    border-color: #d0d7de;
    box-shadow: 0 2px 10px rgba(140, 149, 159, 0.15);
  }

  .thanks-motto {
    font-size: 1.05rem;
    font-weight: 700;
    color: #58a6ff;
    line-height: 1.5;
    margin-bottom: 0.5rem;
    text-align: center;
    letter-spacing: -0.01em;
  }

  html[data-mode="light"] .thanks-motto,
  html[data-bs-theme="light"] .thanks-motto {
    color: #0969da;
  }

  .thanks-desc {
    font-size: 0.88rem;
    line-height: 1.65;
    color: var(--text-color, #c9d1d9);
    text-align: center;
    margin: 0;
  }

  /* ── Pillars Grid ── */
  .pillars-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
    margin-bottom: 2rem;
  }

  @media (max-width: 768px) {
    .pillars-grid {
      grid-template-columns: 1fr;
    }
  }

  .pillar-card {
    padding: 1rem 1.1rem;
    border-radius: 10px;
    background: #000000;
    border: 1px solid #2f3336;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .pillar-card:hover {
    transform: translateY(-2px);
    border-color: #58a6ff;
  }

  html[data-mode="light"] .pillar-card,
  html[data-bs-theme="light"] .pillar-card {
    background: #ffffff;
    border-color: #d0d7de;
  }

  html[data-mode="light"] .pillar-card:hover,
  html[data-bs-theme="light"] .pillar-card:hover {
    border-color: #0969da;
  }

  .pillar-icon {
    width: 32px;
    height: 32px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    background: rgba(56, 189, 248, 0.1);
    color: #58a6ff;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
  }

  html[data-mode="light"] .pillar-icon,
  html[data-bs-theme="light"] .pillar-icon {
    background: rgba(9, 105, 218, 0.08);
    color: #0969da;
  }

  .pillar-title {
    font-size: 0.92rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    color: var(--heading-color, #f0f6fc);
  }

  .pillar-desc {
    font-size: 0.78rem;
    color: var(--text-muted-color, #8b949e);
    line-height: 1.5;
    margin: 0;
  }

  /* ── Section Headers ── */
  .thanks-section-header {
    margin: 2rem 0 1rem;
  }

  .thanks-section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--heading-color, #f0f6fc);
    margin-bottom: 0.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .thanks-section-subtitle {
    font-size: 0.82rem;
    color: var(--text-muted-color, #8b949e);
  }

  /* ── Compact Multi-Item Resources Grid ── */
  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(370px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  @media (max-width: 600px) {
    .resources-grid {
      grid-template-columns: 1fr;
    }
  }

  .resource-card {
    padding: 1.15rem 1.25rem;
    border-radius: 10px;
    background: #000000;
    border: 1px solid #2f3336;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .resource-card:hover {
    transform: translateY(-2px);
    border-color: #58a6ff;
    box-shadow: 0 6px 20px rgba(1, 4, 9, 0.6);
  }

  html[data-mode="light"] .resource-card,
  html[data-bs-theme="light"] .resource-card {
    background: #ffffff;
    border-color: #d0d7de;
    box-shadow: 0 1px 4px rgba(140, 149, 159, 0.12);
  }

  html[data-mode="light"] .resource-card:hover,
  html[data-bs-theme="light"] .resource-card:hover {
    border-color: #0969da;
    box-shadow: 0 6px 16px rgba(140, 149, 159, 0.2);
  }

  .resource-card-top {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }

  .resource-icon-wrapper {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.25);
    color: #58a6ff;
    font-size: 1.15rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  html[data-mode="light"] .resource-icon-wrapper,
  html[data-bs-theme="light"] .resource-icon-wrapper {
    background: rgba(9, 105, 218, 0.08);
    border-color: rgba(9, 105, 218, 0.2);
    color: #0969da;
  }

  .resource-meta {
    flex: 1;
    min-width: 0;
  }

  .resource-title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.2rem;
  }

  .resource-title {
    font-size: 0.98rem;
    font-weight: 700;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .resource-title a {
    color: var(--heading-color, #f0f6fc) !important;
    text-decoration: none !important;
  }

  .resource-title a:hover {
    color: #58a6ff !important;
  }

  html[data-mode="light"] .resource-title a:hover,
  html[data-bs-theme="light"] .resource-title a:hover {
    color: #0969da !important;
  }

  .resource-badge {
    background: rgba(46, 160, 67, 0.15);
    color: #3fb950;
    border: 1px solid rgba(46, 160, 67, 0.3);
    font-size: 0.68rem;
    font-weight: 600;
    padding: 0.1rem 0.45rem;
    border-radius: 12px;
    white-space: nowrap;
  }

  html[data-mode="light"] .resource-badge,
  html[data-bs-theme="light"] .resource-badge {
    background: rgba(31, 136, 61, 0.1);
    color: #1a7f37;
    border-color: rgba(31, 136, 61, 0.25);
  }

  .resource-author {
    font-size: 0.8rem;
    color: var(--text-muted-color, #8b949e);
  }

  .resource-author a {
    color: #58a6ff !important;
    text-decoration: none !important;
    font-weight: 600;
  }

  html[data-mode="light"] .resource-author a,
  html[data-bs-theme="light"] .resource-author a {
    color: #0969da !important;
  }

  .resource-desc {
    font-size: 0.82rem;
    line-height: 1.55;
    color: var(--text-color, #c9d1d9);
    margin: 0 0 0.65rem;
  }

  .resource-quote {
    background: rgba(88, 166, 255, 0.04);
    border-left: 2px solid #58a6ff;
    padding: 0.45rem 0.75rem;
    border-radius: 2px 6px 6px 2px;
    font-size: 0.78rem;
    color: var(--text-color, #c9d1d9);
    margin: 0 0 0.75rem;
    font-style: italic;
    line-height: 1.5;
  }

  html[data-mode="light"] .resource-quote,
  html[data-bs-theme="light"] .resource-quote {
    background: rgba(9, 105, 218, 0.04);
    border-color: #0969da;
    color: #24292f;
  }

  .resource-card-bottom {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #2f3336;
    flex-wrap: wrap;
  }

  html[data-mode="light"] .resource-card-bottom,
  html[data-bs-theme="light"] .resource-card-bottom {
    border-top-color: #eaeef2;
  }

  .resource-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
  }

  .rtag {
    display: inline-block;
    padding: 0.12rem 0.45rem;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 500;
    background: rgba(110, 118, 129, 0.12);
    color: var(--text-muted-color, #8b949e);
    border: 1px solid rgba(110, 118, 129, 0.18);
  }

  .resource-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    background: #16181c;
    border: 1px solid #2f3336;
    color: #f0f6fc !important;
    font-size: 0.76rem;
    font-weight: 600;
    text-decoration: none !important;
    transition: all 0.2s ease;
  }

  .resource-btn:hover {
    background: #2f3336;
    color: #ffffff !important;
    border-color: #8b949e;
  }

  html[data-mode="light"] .resource-btn,
  html[data-bs-theme="light"] .resource-btn {
    background: #f6f8fa;
    border-color: #d0d7de;
    color: #24292f !important;
  }

  html[data-mode="light"] .resource-btn:hover,
  html[data-bs-theme="light"] .resource-btn:hover {
    background: #eaeef2;
    color: #0969da !important;
  }

  /* ── Companion Placeholder Slot ── */
  .resource-card-placeholder {
    padding: 1.15rem 1.25rem;
    border-radius: 10px;
    border: 1px dashed #2f3336;
    background: rgba(22, 27, 34, 0.4);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-height: 190px;
  }

  html[data-mode="light"] .resource-card-placeholder,
  html[data-bs-theme="light"] .resource-card-placeholder {
    border-color: #d0d7de;
    background: #fafbfc;
  }

  .resource-card-placeholder i {
    font-size: 1.5rem;
    color: #8b949e;
    margin-bottom: 0.5rem;
    opacity: 0.6;
  }

  .resource-card-placeholder h4 {
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: var(--heading-color, #f0f6fc);
  }

  .resource-card-placeholder p {
    font-size: 0.78rem;
    color: var(--text-muted-color, #8b949e);
    margin: 0;
    max-width: 280px;
    line-height: 1.45;
  }
</style>

<div class="thanks-container">
  <!-- Hero Section -->
  <div class="thanks-hero">
    <div class="thanks-motto">
      "He who does not thank people does not thank Allah."
    </div>
    <p class="thanks-desc">
      Offensive security engineering and security research are community-driven disciplines. This dedicated wall honors the teachers, colleagues, and open-source creators whose contributions and shared knowledge continue to elevate our industry.
    </p>
  </div>

  <!-- Pillars of Recognition -->
  <div class="pillars-grid">
    <!-- Mentors -->
    <div class="pillar-card">
      <div class="pillar-icon">
        <i class="fas fa-graduation-cap"></i>
      </div>
      <div class="pillar-title">Mentors &amp; Instructors</div>
      <p class="pillar-desc">
        Those who established rigorous foundational methodologies and inspired an engineering-first offensive mindset.
      </p>
    </div>

    <!-- Peer Reviewers & Collaborators -->
    <div class="pillar-card">
      <div class="pillar-icon">
        <i class="fas fa-user-shield"></i>
      </div>
      <div class="pillar-title">Peers &amp; Collaborators</div>
      <p class="pillar-desc">
        Colleagues who shared intensive lab breakdowns, reviewed exploit architectures, and pressure-tested playbooks.
      </p>
    </div>

    <!-- InfoSec Community -->
    <div class="pillar-card">
      <div class="pillar-icon">
        <i class="fas fa-globe-americas"></i>
      </div>
      <div class="pillar-title">InfoSec Community</div>
      <p class="pillar-desc">
        Open-source educators whose tools, writeups, and curriculum guides elevate practitioner standards worldwide.
      </p>
    </div>
  </div>

  <!-- Featured Community Resources & References -->
  <div class="thanks-section-header">
    <div class="thanks-section-title">
      <i class="fas fa-bookmark"></i>
      <span>Featured Community References</span>
    </div>
    <div class="thanks-section-subtitle">
      Essential open-source curriculums, repositories, and technical resources curated for the community.
    </div>
  </div>

  <div class="resources-grid">
    <!-- Muhab Nasser - CPTS Arabic Explanation -->
    <div class="resource-card">
      <div>
        <div class="resource-card-top">
          <div class="resource-icon-wrapper">
            <i class="fab fa-github"></i>
          </div>
          <div class="resource-meta">
            <div class="resource-title-row">
              <h3 class="resource-title">
                <a href="https://github.com/Muhabzz/CPTS-Arabic-Explanation" target="_blank" rel="noopener noreferrer">
                  CPTS Arabic Explanation
                </a>
              </h3>
              <span class="resource-badge">HTB CPTS</span>
            </div>
            <div class="resource-author">
              By <a href="https://github.com/Muhabzz" target="_blank" rel="noopener noreferrer">Muhab Nasser (@Muhabzz)</a>
            </div>
          </div>
        </div>
        <p class="resource-desc">
          An exhaustive, community-driven breakdown of the Hack The Box Certified Penetration Tester Specialist (CPTS) curriculum, bridging Active Directory exploitation, pivoting, and reporting.
        </p>
        <div class="resource-quote">
          Special recognition to <strong>Muhab Nasser</strong> for authoring this essential work and giving back to the offensive security community.
        </div>
      </div>
      <div class="resource-card-bottom">
        <div class="resource-tags">
          <span class="rtag">Hack The Box</span>
          <span class="rtag">CPTS</span>
          <span class="rtag">Active Directory</span>
        </div>
        <a href="https://github.com/Muhabzz/CPTS-Arabic-Explanation" target="_blank" rel="noopener noreferrer" class="resource-btn">
          <i class="fab fa-github"></i>
          <span>Repository</span>
        </a>
      </div>
    </div>

    <!-- Youssef El3anany - HTB Academy Lab Flag Solutions -->
    <div class="resource-card">
      <div>
        <div class="resource-card-top">
          <div class="resource-icon-wrapper">
            <i class="fas fa-flag-checkered"></i>
          </div>
          <div class="resource-meta">
            <div class="resource-title-row">
              <h3 class="resource-title">
                HTB Academy Lab Solutions &amp; Flags
              </h3>
              <span class="resource-badge">Lab Solver</span>
            </div>
            <div class="resource-author">
              By <strong>Youssef El3anany (@YoussefEl3anany)</strong>
            </div>
          </div>
        </div>
        <p class="resource-desc">
          The brilliant security researcher behind deciphering, solving, and validating the complex hands-on lab challenges and flags across the 41 Hack The Box Academy modules featured on this platform.
        </p>
        <div class="resource-quote">
          Deepest gratitude and special recognition to <strong>Youssef El3anany</strong> for his technical dedication, relentless problem-solving, and verified flag captures that powered this entire masterclass series.
        </div>
      </div>
      <div class="resource-card-bottom">
        <div class="resource-tags">
          <span class="rtag">Hack The Box</span>
          <span class="rtag">Flag Verification</span>
          <span class="rtag">CPTS</span>
          <span class="rtag">Lab Master</span>
        </div>
        <span class="resource-btn" style="cursor: default;">
          <i class="fas fa-award"></i>
          <span>Core Contributor</span>
        </span>
      </div>
    </div>

    <!-- Slot ready for next resource -->
    <div class="resource-card-placeholder">
      <i class="fas fa-plus-circle"></i>
      <h4>Curating Community References</h4>
      <p>
        Additional high-impact tools, research papers, and educational repositories are being actively compiled here.
      </p>
    </div>
  </div>
</div>
