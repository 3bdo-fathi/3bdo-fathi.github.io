---
layout: page
icon: fas fa-envelope
order: 5
title: Contact Me
---

<style>
  .contact-form-wrapper {
    max-width: 700px;
    margin: 2rem auto;
    padding: 0 1rem;
  }

  .contact-form-wrapper .form-group {
    margin-bottom: 1.25rem;
  }

  .contact-form-wrapper label {
    display: block;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #e8e6e3;
    font-size: 0.95rem;
    letter-spacing: 0.02em;
  }

  .contact-form-wrapper input[type="text"],
  .contact-form-wrapper input[type="email"],
  .contact-form-wrapper textarea {
    width: 100%;
    padding: 0.85rem 1rem;
    border: 1.5px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    background-color: rgba(30, 30, 45, 0.7);
    color: #e8e6e3;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
    outline: none;
    box-sizing: border-box;
  }

  .contact-form-wrapper input[type="text"]:focus,
  .contact-form-wrapper input[type="email"]:focus,
  .contact-form-wrapper textarea:focus {
    border-color: rgba(131, 123, 199, 0.6);
    box-shadow: 0 0 0 3px rgba(131, 123, 199, 0.15);
    background-color: rgba(35, 35, 55, 0.85);
  }

  .contact-form-wrapper input[type="text"]::placeholder,
  .contact-form-wrapper input[type="email"]::placeholder,
  .contact-form-wrapper textarea::placeholder {
    color: rgba(255, 255, 255, 0.3);
  }

  .contact-form-wrapper textarea {
    min-height: 180px;
    resize: vertical;
  }

  .contact-form-wrapper .btn-submit {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 2rem;
    background: linear-gradient(135deg, #6c5ce7, #a855f7);
    color: #ffffff;
    font-size: 1rem;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.3s ease, opacity 0.3s ease;
    letter-spacing: 0.02em;
    margin-top: 0.5rem;
  }

  .contact-form-wrapper .btn-submit:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(108, 92, 231, 0.4);
    opacity: 0.95;
  }

  .contact-form-wrapper .btn-submit:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(108, 92, 231, 0.3);
  }

  .contact-form-wrapper .form-status {
    margin-top: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 0.9rem;
    display: none;
  }

  .contact-form-wrapper .form-status.success {
    display: block;
    background-color: rgba(46, 213, 115, 0.15);
    color: #2ed573;
    border: 1px solid rgba(46, 213, 115, 0.3);
  }

  .contact-form-wrapper .form-status.error {
    display: block;
    background-color: rgba(255, 71, 87, 0.15);
    color: #ff4757;
    border: 1px solid rgba(255, 71, 87, 0.3);
  }

  /* Light mode overrides */
  [data-mode="light"] .contact-form-wrapper label {
    color: #2d3436;
  }

  [data-mode="light"] .contact-form-wrapper input[type="text"],
  [data-mode="light"] .contact-form-wrapper input[type="email"],
  [data-mode="light"] .contact-form-wrapper textarea {
    background-color: rgba(245, 245, 250, 0.9);
    border-color: rgba(0, 0, 0, 0.1);
    color: #2d3436;
  }

  [data-mode="light"] .contact-form-wrapper input[type="text"]:focus,
  [data-mode="light"] .contact-form-wrapper input[type="email"]:focus,
  [data-mode="light"] .contact-form-wrapper textarea:focus {
    background-color: #ffffff;
    border-color: rgba(108, 92, 231, 0.5);
    box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.1);
  }

  [data-mode="light"] .contact-form-wrapper input[type="text"]::placeholder,
  [data-mode="light"] .contact-form-wrapper input[type="email"]::placeholder,
  [data-mode="light"] .contact-form-wrapper textarea::placeholder {
    color: rgba(0, 0, 0, 0.35);
  }
</style>

<div class="contact-form-wrapper">
  <form id="contact-form" action="https://formsubmit.co/abdulrahmanmohamedfathi@gmail.com" method="POST">
    <!-- FormSubmit configuration -->
    <input type="hidden" name="_subject" value="New message from 0x3bdo Blog!">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_template" value="table">
    <input type="text" name="_honey" style="display:none">
    <div class="form-group">
      <label for="contact-name">Name</label>
      <input type="text" id="contact-name" name="name" placeholder="Your name" required>
    </div>
    <div class="form-group">
      <label for="contact-email">Email</label>
      <input type="email" id="contact-email" name="email" placeholder="Your email address" required>
    </div>
    <div class="form-group">
      <label for="contact-message">Message</label>
      <textarea id="contact-message" name="message" placeholder="Write your message here..." required></textarea>
    </div>
    <button type="submit" class="btn-submit">
      <i class="fas fa-paper-plane"></i> Send Message
    </button>
    <div id="form-status" class="form-status"></div>
  </form>
</div>

<script>
  document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = e.target;
    const status = document.getElementById('form-status');
    const btn = form.querySelector('.btn-submit');
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    }).then(response => {
      if (response.ok) {
        status.className = 'form-status success';
        status.textContent = '✓ Message sent successfully! I will get back to you soon.';
        form.reset();
      } else {
        throw new Error('Form submission failed');
      }
    }).catch(error => {
      status.className = 'form-status error';
      status.textContent = '✗ Oops! Something went wrong. Please try again or email me directly.';
    }).finally(() => {
      btn.disabled = false;
      btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    });
  });
</script>
