---
layout: page
icon: fas fa-award
order: 6
title: Thanks & Recognition
permalink: /thanks/
hide_stats: true
---

<style>
  .thanks-container {
    max-width: 820px;
    margin: 0.5rem auto 3rem;
  }

  /* ── Executive Header Banner ── */
  .thanks-hero {
    position: relative;
    padding: 2.25rem 2rem;
    border-radius: 12px;
    background: linear-gradient(145deg, rgba(88, 166, 255, 0.08) 0%, rgba(13, 17, 23, 0.95) 100%);
    border: 1px solid rgba(88, 166, 255, 0.2);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
    margin-bottom: 2rem;
    overflow: hidden;
  }

  html[data-mode="light"] .thanks-hero,
  html[data-bs-theme="light"] .thanks-hero {
    background: linear-gradient(145deg, rgba(9, 105, 218, 0.06) 0%, rgba(246, 248, 250, 0.95) 100%);
    border-color: rgba(9, 105, 218, 0.2);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  }

  .thanks-motto {
    font-size: 1.1rem;
    font-weight: 700;
    color: #58a6ff;
    line-height: 1.6;
    margin-bottom: 0.75rem;
    text-align: center;
    letter-spacing: -0.01em;
  }

  html[data-mode="light"] .thanks-motto,
  html[data-bs-theme="light"] .thanks-motto {
    color: #0969da;
  }

  .thanks-desc {
    font-size: 0.95rem;
    line-height: 1.75;
    color: var(--text-color, #c9d1d9);
    text-align: center;
    margin: 0;
  }

  /* ── Status Banner (Coming Soon / Under Curation) ── */
  .curation-badge-box {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 0.85rem 1.25rem;
    border-radius: 8px;
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.28);
    color: #f59e0b;
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 2.25rem;
    text-align: center;
  }

  html[data-mode="light"] .curation-badge-box,
  html[data-bs-theme="light"] .curation-badge-box {
    background: rgba(217, 119, 6, 0.08);
    border-color: rgba(217, 119, 6, 0.3);
    color: #b45309;
  }

  /* ── Categories of Gratitude Grid ── */
  .pillars-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.15rem;
    margin-bottom: 2.5rem;
  }

  @media (max-width: 820px) {
    .pillars-grid {
      grid-template-columns: 1fr;
    }
  }

  .pillar-card {
    padding: 1.4rem 1.25rem;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .pillar-card:hover {
    transform: translateY(-2px);
    border-color: rgba(88, 166, 255, 0.3);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  }

  html[data-mode="light"] .pillar-card,
  html[data-bs-theme="light"] .pillar-card {
    background: #ffffff;
    border-color: #d0d7de;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  }

  html[data-mode="light"] .pillar-card:hover,
  html[data-bs-theme="light"] .pillar-card:hover {
    border-color: #0969da;
    box-shadow: 0 4px 14px rgba(9, 105, 218, 0.12);
  }

  .pillar-icon {
    width: 38px;
    height: 38px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(88, 166, 255, 0.12);
    color: #58a6ff;
    font-size: 1.1rem;
    margin-bottom: 0.85rem;
  }

  html[data-mode="light"] .pillar-icon,
  html[data-bs-theme="light"] .pillar-icon {
    background: rgba(9, 105, 218, 0.1);
    color: #0969da;
  }

  .pillar-title {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.45rem;
    color: var(--heading-color, #f0f6fc);
  }

  .pillar-desc {
    font-size: 0.85rem;
    color: var(--text-muted-color, #8b949e);
    line-height: 1.6;
    margin: 0;
  }

  /* ── Placeholder Card Layout Ready for Names ── */
  .placeholder-showcase {
    border: 1px dashed rgba(255, 255, 255, 0.18);
    border-radius: 12px;
    padding: 2.25rem 1.5rem;
    text-align: center;
    background: rgba(255, 255, 255, 0.015);
  }

  html[data-mode="light"] .placeholder-showcase,
  html[data-bs-theme="light"] .placeholder-showcase {
    border-color: rgba(0, 0, 0, 0.18);
    background: rgba(0, 0, 0, 0.015);
  }

  .placeholder-showcase i {
    font-size: 2rem;
    color: #8b949e;
    margin-bottom: 0.85rem;
    opacity: 0.7;
  }

  .placeholder-showcase h3 {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.45rem;
  }

  .placeholder-showcase p {
    font-size: 0.88rem;
    color: var(--text-muted-color, #8b949e);
    line-height: 1.6;
    max-width: 540px;
    margin: 0 auto;
  }
</style>

<div class="thanks-container">
  <!-- Hero Section -->
  <div class="thanks-hero">
    <div class="thanks-motto">
      "He who does not thank people does not thank Allah."
    </div>
    <p class="thanks-desc">
      Cyber security engineering and offensive research are never solitary achievements. Growth is the product of generous mentorship, relentless peer discussions, and a community committed to open knowledge. This dedicated wall honors the teachers, colleagues, and researchers whose influence continues to shape my path.
    </p>
  </div>

  <!-- Status Notification -->
  <div class="curation-badge-box">
    <i class="fas fa-tools"></i>
    <span>Under Active Curation &mdash; Individual acknowledgments, mentor profiles, and contributor cards are currently being compiled and will be published here shortly.</span>
  </div>

  <!-- Pillars of Recognition -->
  <div class="pillars-grid">
    <!-- Mentors -->
    <div class="pillar-card">
      <div class="pillar-icon">
        <i class="fas fa-graduation-cap"></i>
      </div>
      <div class="pillar-title">Mentors & Instructors</div>
      <p class="pillar-desc">
        Those who established rigorous foundational methodologies, nurtured curiosity, and inspired an ethical, engineering-first mindset in offensive security.
      </p>
    </div>

    <!-- Peer Reviewers & Collaborators -->
    <div class="pillar-card">
      <div class="pillar-icon">
        <i class="fas fa-user-friends"></i>
      </div>
      <div class="pillar-title">Peers & Collaborators</div>
      <p class="pillar-desc">
        Colleagues and researchers who shared intensive lab breakdowns, reviewed exploit architectures, and pressure-tested red teaming playbooks.
      </p>
    </div>

    <!-- InfoSec Community -->
    <div class="pillar-card">
      <div class="pillar-icon">
        <i class="fas fa-globe-americas"></i>
      </div>
      <div class="pillar-title">InfoSec Community</div>
      <p class="pillar-desc">
        Open-source creators and community educators whose tools, publications, and advisory breakdowns continually elevate practitioner standards worldwide.
      </p>
    </div>
  </div>

  <!-- Showcase Placeholder -->
  <div class="placeholder-showcase">
    <i class="fas fa-heart"></i>
    <h3>Honor Roll & Dedications</h3>
    <p>
      Dedicated profile cards featuring honoree names, professional roles, portfolio links, and personalized appreciation statements will be populated right here.
    </p>
  </div>
</div>
