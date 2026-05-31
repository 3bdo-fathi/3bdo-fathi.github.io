---
layout: page
icon: fas fa-envelope
order: 5
title: Contact Me
image: /assets/images/preview.jpg
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
    letter-spacing: 0.01em;
  }

  .gh-contact-wrapper input[type="text"],
  .gh-contact-wrapper input[type="email"],
  .gh-contact-wrapper textarea {
    width: 100%;
    padding: 0.6rem 0.85rem;
    border: 1px solid #30363d;
    border-radius: 6px;
    background-color: #0d1117;
    color: #e6edf3;
    font-size: 0.95rem;
    font-family: inherit;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    outline: none;
    box-sizing: border-box;
  }

  .gh-contact-wrapper input[type="text"]:focus,
  .gh-contact-wrapper input[type="email"]:focus,
  .gh-contact-wrapper textarea:focus {
    border-color: #1f6feb;
    box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.2);
  }

  .gh-contact-wrapper input::placeholder,
  .gh-contact-wrapper textarea::placeholder {
    color: #484f58;
  }

  .gh-contact-wrapper textarea {
    min-height: 175px;
    resize: vertical;
  }

  /* GitHub green button */
  .gh-contact-wrapper .gh-btn-submit {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.55rem 1.4rem;
    background-color: #238636;
    color: #ffffff;
    font-size: 0.9rem;
    font-weight: 600;
    border: 1px solid rgba(240,246,252,0.1);
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
    letter-spacing: 0.01em;
    margin-top: 0.4rem;
  }

  .gh-contact-wrapper .gh-btn-submit:hover {
    background-color: #2ea043;
    border-color: rgba(240,246,252,0.1);
    box-shadow: 0 0 0 3px rgba(46,160,67,0.25);
    transform: translateY(-1px);
  }

  .gh-contact-wrapper .gh-btn-submit:active {
    background-color: #238636;
    transform: translateY(0);
    box-shadow: none;
  }

  .gh-contact-wrapper .gh-btn-submit:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  /* Status messages */
  .gh-contact-wrapper .gh-status {
    margin-top: 0.85rem;
    padding: 0.65rem 0.9rem;
    border-radius: 6px;
    font-size: 0.875rem;
    display: none;
    align-items: center;
    gap: 0.5rem;
  }

  .gh-contact-wrapper .gh-status.success {
    display: flex;
    background-color: rgba(35, 134, 54, 0.15);
    color: #3fb950;
    border: 1px solid rgba(35, 134, 54, 0.4);
  }

  .gh-contact-wrapper .gh-status.error {
    display: flex;
    background-color: rgba(248, 81, 73, 0.15);
    color: #f85149;
    border: 1px solid rgba(248, 81, 73, 0.4);
  }

  /* Light mode overrides — keep GitHub light feel */
  [data-mode="light"] .gh-contact-wrapper label {
    color: #24292f;
  }

  [data-mode="light"] .gh-contact-wrapper input[type="text"],
  [data-mode="light"] .gh-contact-wrapper input[type="email"],
  [data-mode="light"] .gh-contact-wrapper textarea {
    background-color: #ffffff;
    border-color: #d0d7de;
    color: #24292f;
  }

  [data-mode="light"] .gh-contact-wrapper input::placeholder,
  [data-mode="light"] .gh-contact-wrapper textarea::placeholder {
    color: #6e7781;
  }

  [data-mode="light"] .gh-contact-wrapper input[type="text"]:focus,
  [data-mode="light"] .gh-contact-wrapper input[type="email"]:focus,
  [data-mode="light"] .gh-contact-wrapper textarea:focus {
    border-color: #0969da;
    box-shadow: 0 0 0 3px rgba(9, 105, 218, 0.2);
  }
</style>

<div class="gh-contact-wrapper">
  <form id="gh-contact-form" action="https://formsubmit.co/abdulrahmanmohamedfathi@gmail.com" method="POST">
    <!-- FormSubmit config -->
    <input type="hidden" name="_subject" value="New message from 0x3bdo Blog!">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_template" value="table">
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">

    <div class="gh-form-group">
      <label for="gh-name">Name</label>
      <input type="text" id="gh-name" name="name" placeholder="Your name" required>
    </div>

    <div class="gh-form-group">
      <label for="gh-email">Email</label>
      <input type="email" id="gh-email" name="email" placeholder="your@email.com" required>
    </div>

    <div class="gh-form-group">
      <label for="gh-message">Message</label>
      <textarea id="gh-message" name="message" placeholder="Write your message here..." required></textarea>
    </div>

    <button type="submit" class="gh-btn-submit" id="gh-submit-btn">
      <i class="fas fa-paper-plane"></i> Send Message
    </button>

    <div id="gh-form-status" class="gh-status"></div>
  </form>
</div>

<script>
  document.getElementById('gh-contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = e.target;
    const status = document.getElementById('gh-form-status');
    const btn = document.getElementById('gh-submit-btn');

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Sending...';
    status.className = 'gh-status';
    status.style.display = 'none';

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    })
    .then(res => {
      if (res.ok) {
        status.className = 'gh-status success';
        status.innerHTML = '<i class="fas fa-check-circle"></i> Message sent! I\'ll get back to you soon.';
        form.reset();
      } else {
        throw new Error('failed');
      }
    })
    .catch(() => {
      status.className = 'gh-status error';
      status.innerHTML = '<i class="fas fa-exclamation-circle"></i> Something went wrong. Please email me directly at <strong>abdulrahmanmohamedfathi@gmail.com</strong>.';
    })
    .finally(() => {
      btn.disabled = false;
      btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    });
  });
</script>
