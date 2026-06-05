---
layout: page
icon: fas fa-envelope
order: 5
title: Contact Me
permalink: /contact-me/
image: /assets/images/preview.jpg
hide_stats: true
---

<style>
  /* ── GitHub-themed Contact Form ── */
  .gh-contact-wrapper {
    max-width: 680px;
    margin: 1.5rem auto;
    padding: 0 1rem;
  }

  .gh-contact-wrapper .gh-form-group {
    margin-bottom: 1.1rem;
  }

  .gh-contact-wrapper label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.45rem;
    color: #e6edf3;
    font-size: 0.9rem;
  }

  .gh-contact-wrapper input[type="text"],
  .gh-contact-wrapper input[type="email"],
  .gh-contact-wrapper input[type="tel"],
  .gh-contact-wrapper select,
  .gh-contact-wrapper textarea {
    width: 100%;
    padding: 0.65rem 0.9rem;
    border: 1px solid #30363d;
    border-radius: 6px;
    background-color: #0d1117;
    color: #e6edf3;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    outline: none;
  }

  .gh-contact-wrapper input:focus,
  .gh-contact-wrapper select:focus,
  .gh-contact-wrapper textarea:focus {
    border-color: #1f6feb;
    box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.2);
  }

  .gh-contact-wrapper textarea {
    min-height: 160px;
    resize: vertical;
  }

  /* Character Counter */
  .char-count {
    text-align: right;
    font-size: 0.85rem;
    margin-top: 0.3rem;
    font-weight: 500;
  }

  .char-count.warning {
    color: #f2c744;
  }

  .char-count.error {
    color: #f85149;
  }

  .gh-contact-wrapper .gh-btn-submit {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.5rem;
    background-color: #238636;
    color: #fff;
    font-weight: 600;
    border: 1px solid rgba(240,246,252,0.1);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .gh-contact-wrapper .gh-btn-submit:hover:not(:disabled) {
    background-color: #2ea043;
    transform: translateY(-1px);
    box-shadow: 0 0 0 3px rgba(46,160,67,0.25);
  }

  .gh-status {
    margin-top: 1rem;
    padding: 0.8rem 1rem;
    border-radius: 6px;
    font-size: 0.9rem;
    display: none;
    align-items: center;
    gap: 0.5rem;
  }

  .gh-status.success { background: rgba(35,134,54,0.15); color: #3fb950; border: 1px solid rgba(35,134,54,0.4); }
  .gh-status.error   { background: rgba(248,81,73,0.15); color: #f85149; border: 1px solid rgba(248,81,73,0.4); }
</style>

<div class="gh-contact-wrapper">
  <form id="gh-contact-form" action="https://formsubmit.co/abdulrahmanmohamedfathi@gmail.com" method="POST">
    <input type="hidden" name="_subject" value="New message from 0x3bdo Blog!">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_template" value="table">
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">

    <div class="gh-form-group">
      <label for="gh-name">Full Name</label>
      <input type="text" id="gh-name" name="name" placeholder="Your name" required autofocus>
    </div>

    <div class="gh-form-group">
      <label for="gh-email">Email Address</label>
      <input type="email" id="gh-email" name="email" placeholder="your@email.com" required>
    </div>

    <div class="gh-form-group">
      <label for="gh-phone">Phone Number <span style="font-weight:normal;opacity:0.6;">(optional)</span></label>
      <input type="tel" id="gh-phone" name="phone" placeholder="+20 1xx xxx xxxx">
    </div>

    <div class="gh-form-group">
      <label for="gh-type">Message Type</label>
      <select id="gh-type" name="type" required>
        <option value="">Select type...</option>
        <option value="General Inquiry">General Inquiry</option>
        <option value="Collaboration">Collaboration / Work</option>
        <option value="Feedback">Feedback</option>
        <option value="Bug Report">Bug Report</option>
        <option value="Other">Other</option>
      </select>
    </div>

    <div class="gh-form-group">
      <label for="gh-subject">Subject</label>
      <input type="text" id="gh-subject" name="subject" placeholder="Message subject" required>
    </div>

    <div class="gh-form-group">
      <label for="gh-message">
        Your Message <span style="font-weight:normal;opacity:0.7;">(Max 2000 characters)</span>
      </label>
      <textarea id="gh-message" name="message" placeholder="Write your message here..." maxlength="2000" required></textarea>
      <div id="char-count-container" class="char-count">0 / 2000</div>
    </div>

    <button type="submit" class="gh-btn-submit" id="gh-submit-btn">
      <i class="fas fa-paper-plane"></i> Send Message
    </button>

    <div id="gh-form-status" class="gh-status"></div>
  </form>
</div>

<script>
  const form = document.getElementById('gh-contact-form');
  const statusEl = document.getElementById('gh-form-status');
  const btn = document.getElementById('gh-submit-btn');
  const messageInput = document.getElementById('gh-message');
  const countContainer = document.getElementById('char-count-container');
  const MAX_LENGTH = 2000;

  // Character counter + warning
  function updateCharCount() {
    const length = messageInput.value.length;
    countContainer.textContent = `${length} / ${MAX_LENGTH}`;

    if (length > MAX_LENGTH - 200) {
      countContainer.classList.add('error');
    } else if (length > MAX_LENGTH - 400) {
      countContainer.classList.add('warning');
      countContainer.classList.remove('error');
    } else {
      countContainer.classList.remove('warning', 'error');
    }
  }

  messageInput.addEventListener('input', updateCharCount);

  form.addEventListener('submit', function(e) {
    e.preventDefault();

    if (messageInput.value.length > MAX_LENGTH) {
      statusEl.className = 'gh-status error';
      statusEl.innerHTML = `<i class="fas fa-exclamation-circle"></i> Message is too long! Maximum ${MAX_LENGTH} characters.`;
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
    .then(res => res.ok ? res : Promise.reject())
    .then(() => {
      statusEl.className = 'gh-status success';
      statusEl.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <div><strong>Message sent successfully!</strong><br>Thank you! I'll reply soon.</div>
      `;
      statusEl.style.display = 'flex';
      form.reset();
      updateCharCount();
    })
    .catch(() => {
      statusEl.className = 'gh-status error';
      statusEl.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        Failed to send. Please email me directly at <strong>abdulrahmanmohamedfathi@gmail.com</strong>
      `;
      statusEl.style.display = 'flex';
    })
    .finally(() => {
      btn.disabled = false;
      btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    });
  });
</script>