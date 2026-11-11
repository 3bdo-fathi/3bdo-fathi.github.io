---
layout: page
icon: fas fa-envelope
order: 7
title: Contact Me
permalink: /contact-me/
image: /assets/images/site/preview.jpg
---

<style>
  .contact-container {
    max-width: 740px;
    margin: 0.5rem auto 2.5rem;
  }

  .contact-intro {
    font-size: 0.95rem;
    color: var(--text-muted-color, #8b949e);
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  /* ── Quick Channels Grid ── */
  .contact-channels-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 0.75rem;
    margin-bottom: 1.75rem;
  }

  .contact-channel-card {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding: 0.85rem 1rem;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    text-decoration: none !important;
    color: inherit;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .contact-channel-card:hover {
    background: rgba(88, 166, 255, 0.06);
    border-color: rgba(88, 166, 255, 0.35);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  }

  html[data-mode="light"] .contact-channel-card,
  html[data-bs-theme="light"] .contact-channel-card {
    background: #f6f8fa;
    border-color: #d0d7de;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  html[data-mode="light"] .contact-channel-card:hover,
  html[data-bs-theme="light"] .contact-channel-card:hover {
    background: #ffffff;
    border-color: #0969da;
    box-shadow: 0 4px 12px rgba(9, 105, 218, 0.1);
  }

  .contact-channel-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 8px;
    font-size: 1.05rem;
    flex-shrink: 0;
  }

  .channel-icon-email {
    background: rgba(88, 166, 255, 0.12);
    color: #58a6ff;
  }

  .channel-icon-linkedin {
    background: rgba(10, 102, 194, 0.15);
    color: #0a66c2;
  }

  .channel-icon-github {
    background: rgba(255, 255, 255, 0.1);
    color: #f0f6fc;
  }

  html[data-mode="light"] .channel-icon-github,
  html[data-bs-theme="light"] .channel-icon-github {
    background: rgba(0, 0, 0, 0.06);
    color: #24292f;
  }

  .contact-channel-info {
    overflow: hidden;
  }

  .contact-channel-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #8b949e;
    margin-bottom: 0.15rem;
  }

  .contact-channel-value {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--heading-color, #e6edf3);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* ── Form Card Container ── */
  .contact-form-card {
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 1.5rem 1.6rem;
  }

  html[data-mode="light"] .contact-form-card,
  html[data-bs-theme="light"] .contact-form-card {
    background: #ffffff;
    border-color: #d0d7de;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  .contact-form-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 0.9rem;
    margin-bottom: 1.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }

  html[data-mode="light"] .contact-form-header,
  html[data-bs-theme="light"] .contact-form-header {
    border-bottom-color: #e1e4e8;
  }

  .contact-form-title {
    font-size: 1rem;
    font-weight: 700;
    margin: 0;
    color: var(--heading-color, #ffffff);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .contact-form-badge {
    font-size: 0.7rem;
    padding: 0.15rem 0.5rem;
    border-radius: 20px;
    background: rgba(63, 185, 80, 0.15);
    color: #3fb950;
    border: 1px solid rgba(63, 185, 80, 0.3);
    font-weight: 600;
    font-family: monospace;
  }

  /* ── Responsive Form Grid ── */
  .contact-grid-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  @media (max-width: 600px) {
    .contact-grid-row {
      grid-template-columns: 1fr;
      gap: 0.9rem;
    }
    .contact-form-card {
      padding: 1.1rem 1rem;
    }
  }

  .contact-field-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }

  .contact-field-group label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #c9d1d9;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  html[data-mode="light"] .contact-field-group label,
  html[data-bs-theme="light"] .contact-field-group label {
    color: #24292f;
  }

  .contact-field-group input,
  .contact-field-group select,
  .contact-field-group textarea {
    width: 100%;
    padding: 0.62rem 0.85rem;
    border-radius: 6px;
    background: #000000;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #f0f6fc;
    font-size: 0.88rem;
    transition: all 0.18s ease;
    outline: none;
    font-family: inherit;
  }

  html[data-mode="light"] .contact-field-group input,
  html[data-mode="light"] .contact-field-group select,
  html[data-mode="light"] .contact-field-group textarea,
  html[data-bs-theme="light"] .contact-field-group input,
  html[data-bs-theme="light"] .contact-field-group select,
  html[data-bs-theme="light"] .contact-field-group textarea {
    background: #ffffff;
    border-color: #d0d7de;
    color: #24292f;
  }

  .contact-field-group input:focus,
  .contact-field-group select:focus,
  .contact-field-group textarea:focus {
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2);
  }

  html[data-mode="light"] .contact-field-group input:focus,
  html[data-mode="light"] .contact-field-group select:focus,
  html[data-mode="light"] .contact-field-group textarea:focus,
  html[data-bs-theme="light"] .contact-field-group input:focus,
  html[data-bs-theme="light"] .contact-field-group select:focus,
  html[data-bs-theme="light"] .contact-field-group textarea:focus {
    border-color: #0969da;
    box-shadow: 0 0 0 3px rgba(9, 105, 218, 0.2);
  }

  .contact-field-group select option {
    background: #0d1117;
    color: #f0f6fc;
  }

  html[data-mode="light"] .contact-field-group select option,
  html[data-bs-theme="light"] .contact-field-group select option {
    background: #ffffff;
    color: #24292f;
  }

  .contact-field-group textarea {
    min-height: 140px;
    resize: vertical;
  }

  .contact-meta-hint {
    font-size: 0.72rem;
    font-weight: 400;
    color: #8b949e;
  }

  .char-counter-pill {
    font-size: 0.74rem;
    font-family: monospace;
    color: #8b949e;
    text-align: right;
    margin-top: 0.35rem;
  }

  .char-counter-pill.warning {
    color: #e3b341;
  }

  .char-counter-pill.error {
    color: #ff7b72;
  }

  /* ── Submit Action Row ── */
  .contact-submit-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1.25rem;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .contact-submit-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.65rem 1.4rem;
    font-size: 0.88rem;
    font-weight: 600;
    color: #ffffff;
    background: #238636;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .contact-submit-btn:hover:not(:disabled) {
    background: #2ea043;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(46, 160, 67, 0.3);
  }

  .contact-submit-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .contact-security-notice {
    font-size: 0.74rem;
    color: #8b949e;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }

  .contact-status-alert {
    display: none;
    align-items: center;
    gap: 0.6rem;
    margin-top: 1.25rem;
    padding: 0.85rem 1rem;
    border-radius: 6px;
    font-size: 0.85rem;
  }

  .contact-status-alert.success {
    background: rgba(35, 134, 54, 0.15);
    color: #3fb950;
    border: 1px solid rgba(35, 134, 54, 0.4);
  }

  .contact-status-alert.error {
    background: rgba(248, 81, 73, 0.15);
    color: #ff7b72;
    border: 1px solid rgba(248, 81, 73, 0.4);
  }
</style>

<div class="contact-container">
  <p class="contact-intro">
    Have a security research inquiry, vulnerability report, offensive assessment request, or collaboration opportunity? You can reach out directly via the channels below or leave a message through the encrypted dispatch form.
  </p>

  <!-- ── Direct Channels ── -->
  <div class="contact-channels-grid">
    <a href="mailto:abdulrahmanmohamedfathi@gmail.com" class="contact-channel-card">
      <div class="contact-channel-icon channel-icon-email">
        <i class="fas fa-envelope"></i>
      </div>
      <div class="contact-channel-info">
        <div class="contact-channel-label">Direct Email</div>
        <div class="contact-channel-value" title="abdulrahmanmohamedfathi@gmail.com">abdulrahmanmohamedfathi@gmail.com</div>
      </div>
    </a>

    <a href="https://www.linkedin.com/in/3bdo-fathi" target="_blank" rel="noopener noreferrer" class="contact-channel-card">
      <div class="contact-channel-icon channel-icon-linkedin">
        <i class="fab fa-linkedin-in"></i>
      </div>
      <div class="contact-channel-info">
        <div class="contact-channel-label">LinkedIn</div>
        <div class="contact-channel-value">in/3bdo-fathi</div>
      </div>
    </a>

    <a href="https://github.com/3bdo-fathi" target="_blank" rel="noopener noreferrer" class="contact-channel-card">
      <div class="contact-channel-icon channel-icon-github">
        <i class="fab fa-github"></i>
      </div>
      <div class="contact-channel-info">
        <div class="contact-channel-label">GitHub</div>
        <div class="contact-channel-value">@3bdo-fathi</div>
      </div>
    </a>
  </div>

  <!-- ── Form Card ── -->
  <div class="contact-form-card">
    <div class="contact-form-header">
      <h2 class="contact-form-title">
        <i class="fas fa-paper-plane" style="color: #58a6ff;"></i> Send a Direct Message
      </h2>
      <span class="contact-form-badge">Encrypted Transit</span>
    </div>

    <form id="gh-contact-form" action="https://formsubmit.co/abdulrahmanmohamedfathi@gmail.com" method="POST">
      <input type="hidden" name="_subject" value="New Security Message from Abdulrahman M. Fathi Blog!">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_template" value="table">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">

      <div class="contact-grid-row">
        <div class="contact-field-group">
          <label for="gh-name">Full Name *</label>
          <input type="text" id="gh-name" name="name" placeholder="Abdulrahman / Your Name" required autofocus>
        </div>

        <div class="contact-field-group">
          <label for="gh-email">Email Address *</label>
          <input type="email" id="gh-email" name="email" placeholder="you@example.com" required>
        </div>
      </div>

      <div class="contact-grid-row">
        <div class="contact-field-group">
          <label for="gh-phone">
            <span>Phone Number</span>
            <span class="contact-meta-hint">(optional)</span>
          </label>
          <input type="tel" id="gh-phone" name="phone" placeholder="+20 1xx xxx xxxx">
        </div>

        <div class="contact-field-group">
          <label for="gh-type">Inquiry Type *</label>
          <select id="gh-type" name="type" required>
            <option value="">Select category...</option>
            <option value="Security Inquiry">Security Inquiry / Research</option>
            <option value="Penetration Testing">Penetration Testing / Audit</option>
            <option value="Collaboration">Collaboration / Hiring</option>
            <option value="Feedback">Feedback / Question</option>
            <option value="Bug Report">Vulnerability / Bug Report</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>

      <div class="contact-field-group">
        <label for="gh-subject">Subject *</label>
        <input type="text" id="gh-subject" name="subject" placeholder="Brief summary of your inquiry" required>
      </div>

      <div class="contact-field-group">
        <label for="gh-message">
          <span>Your Message *</span>
          <span class="contact-meta-hint">Max 2000 characters</span>
        </label>
        <textarea id="gh-message" name="message" placeholder="Provide detailed context regarding your assessment, question, or request..." maxlength="2000" required></textarea>
        <div id="char-count-container" class="char-counter-pill">0 / 2000</div>
      </div>

      <div class="contact-submit-row">
        <button type="submit" class="contact-submit-btn" id="gh-submit-btn">
          <i class="fas fa-paper-plane"></i> Send Message
        </button>

        <span class="contact-security-notice">
          <i class="fas fa-shield-alt text-success"></i> Dispatched via secure gateway
        </span>
      </div>

      <div id="gh-form-status" class="contact-status-alert"></div>
    </form>
  </div>
</div>

<script>
  (function () {
    const form = document.getElementById('gh-contact-form');
    const statusEl = document.getElementById('gh-form-status');
    const btn = document.getElementById('gh-submit-btn');
    const messageInput = document.getElementById('gh-message');
    const countContainer = document.getElementById('char-count-container');
    const MAX_LENGTH = 2000;

    if (!form || !messageInput) return;

    function updateCharCount() {
      const length = messageInput.value.length;
      if (countContainer) {
        countContainer.textContent = length + ' / ' + MAX_LENGTH;

        if (length > MAX_LENGTH - 200) {
          countContainer.className = 'char-counter-pill error';
        } else if (length > MAX_LENGTH - 400) {
          countContainer.className = 'char-counter-pill warning';
        } else {
          countContainer.className = 'char-counter-pill';
        }
      }
    }

    messageInput.addEventListener('input', updateCharCount);

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      if (messageInput.value.length > MAX_LENGTH) {
        statusEl.className = 'contact-status-alert error';
        statusEl.innerHTML = '<i class="fas fa-exclamation-circle"></i> Message exceeds the maximum limit of ' + MAX_LENGTH + ' characters.';
        statusEl.style.display = 'flex';
        return;
      }

      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Sending...';

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res;
      })
      .then(function () {
        statusEl.className = 'contact-status-alert success';
        statusEl.innerHTML = '<i class="fas fa-check-circle"></i> <div><strong>Message delivered successfully!</strong><br>Thank you for reaching out. I will get back to you shortly.</div>';
        statusEl.style.display = 'flex';
        form.reset();
        updateCharCount();
      })
      .catch(function () {
        statusEl.className = 'contact-status-alert error';
        statusEl.innerHTML = '<i class="fas fa-exclamation-circle"></i> <div>Failed to send via the web form. Please email me directly at <strong>abdulrahmanmohamedfathi@gmail.com</strong></div>';
        statusEl.style.display = 'flex';
      })
      .finally(function () {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
      });
    });
  })();
</script>
