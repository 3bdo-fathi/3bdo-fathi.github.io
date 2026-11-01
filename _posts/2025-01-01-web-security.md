---
title: "Web & API Penetration Testing Guide: OWASP Top 10, Business Logic & Modern Exploitation"
date: 2025-01-01 12:15:00 +0300
categories: [Cyber Security, Web Security]
tags: [web-security, api-security, owasp, pentesting, idor, ssrf, ssti, rce, business-logic, burp-suite]
description: "An in-depth technical manual for web and API penetration testing, covering modern attack vectors: IDOR, SSRF, SSTI, Race Conditions, JWT misconfigurations, GraphQL exploitation, and defensive architecture."
toc: true
schema:
  type: Article
  author: Abdulrahman Mohamed
---

Web applications and APIs represent the primary digital perimeter of modern enterprises, processing financial transactions, managing sensitive customer records, and coordinating complex distributed microservices. Because web applications are publicly accessible by design, identifying and mitigating security vulnerabilities before malicious actors can exploit them is one of the most critical responsibilities in offensive security.

Modern web penetration testing has evolved far beyond basic automated vulnerability scanners. Enterprise web applications today deploy multi-tier architectures, microservices, containerization, and Single Page Applications (SPAs) communicating via RESTful and GraphQL APIs. As security controls like Web Application Firewalls (WAFs) and framework-level input sanitizers mature, high-impact security findings increasingly stem from **broken authorization models**, **business logic flaws**, and **complex protocol misconfigurations**.

In this guide, we break down modern web and API penetration testing methodologies, analyze core vulnerability classes with practical exploitation scenarios, and provide authoritative architectural remediation roadmaps.

---

## 1. Broken Object Level Authorization (BOLA / IDOR)

Insecure Direct Object References (IDOR) and Broken Object Level Authorization (BOLA) consistently rank as the most prevalent and critical vulnerabilities in modern web applications and APIs.

### The Vulnerability Mechanics

BOLA occurs when an application receives a user-supplied identifier (such as an ID in a URL path, query parameter, or JSON request body) and accesses the corresponding database object without validating whether the requesting session possesses legitimate ownership or permission to access that specific object.

```http
GET /api/v1/users/1087/statement HTTP/1.1
Host: api.target.local
Authorization: Bearer <Victim_B_Token>
```

If replacing `1087` with `1088` returns User A's private financial statement, authorization enforcement is absent at the controller level.

### Advanced BOLA Testing Patterns:
1. **Identifier Permutations**: Testing with numeric IDs, UUIDs, Base64-encoded hashes, and email addresses.
2. **HTTP Method Switching**: If `GET /api/users/1087` returns `403 Forbidden`, testing `POST`, `PUT`, `PATCH`, or `DELETE` with custom headers (`X-HTTP-Method-Override: GET`).
3. **Array & JSON Parameter Pollution**:
   ```json
   { "userId": [1087, 1088] }
   ```
4. **API Version Downgrade**: If `api/v2/users/1087` enforces strict authorization, testing legacy endpoints (`api/v1/users/1087` or `api/beta/users/1087`) that may lack updated authorization checks.

---

## 2. Server-Side Request Forgery (SSRF)

Server-Side Request Forgery occurs when a web application fetches a remote resource (e.g., importing a profile picture from a URL, generating a PDF from an HTML page, or processing a webhook) without properly validating the destination host against internal network IP ranges.

### The Attack Vector: Cloud Metadata Extraction

In cloud-hosted environments (AWS, Azure, GCP, DigitalOcean), the primary target of SSRF exploitation is the link-local **Instance Metadata Service (IMDS)**:

```text
http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
```

If the server returns AWS access keys, secret keys, and temporary session tokens, an attacker can authenticate directly to the target's AWS cloud infrastructure.

### Advanced SSRF Filter Bypasses:
* **IPv6 Encodings**: `http://[::ffff:169.254.169.254]/`
* **Decimal & Hexadecimal IP Encodings**:
  * Decimal: `http://2852039166/` (translates to `169.254.169.254`)
  * Hexadecimal: `http://0xa9fea9fe/`
* **DNS Rebinding**: Configuring a custom domain whose DNS record initially resolves to a benign public IP to pass validation checks, then returns `127.0.0.1` or `169.254.169.254` when the server executes the HTTP request.
* **Protocol Smuggling & Redirects**: Pointing the URL to a controlled public server that issues an `HTTP 302` redirect to internal services (`gopher://`, `dict://`, or internal private subnets like `http://10.0.0.1/admin`).

---

## 3. Server-Side Template Injection (SSTI)

When applications use templating engines (Jinja2, Twig, Freemarker, Thymeleaf, Velocity) to generate dynamic HTML or email notifications, concatenating user-controlled input directly into the template string rather than passing it as a data context variable leads to **Server-Side Template Injection (SSTI)**, frequently escalating directly to **Remote Code Execution (RCE)**.

### Detection Methodology: Polyglot Arithmetic

To distinguish between different templating engines, testers inject mathematical evaluation payloads:

```text
${7*7}  -> If evaluates to 49: Java / Smarty / Freemarker
{{7*7}} -> If evaluates to 49: Jinja2 / Twig
<%= 7*7 %> -> If evaluates to 49: ERB (Ruby)
#{7*7}  -> If evaluates to 49: Java / Velocity / Thymeleaf
```

### Remote Code Execution in Python / Jinja2:
```jinja2
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
```

---

## 4. Business Logic Flaws & Race Conditions

Automated scanners rely on signature matching and regex checks; they have zero understanding of business rules, checkout workflows, discount coupons, or financial transactions.

### 1. Currency & Pricing Parameter Manipulation
* Negative quantities in e-commerce shopping carts (`quantity = -1`) resulting in negative totals or balance credits.
* Modifying parameter currencies from `USD` to lower-value currencies while maintaining raw integer prices.

### 2. Concurrency & Race Conditions (Limit Overrun)
When an application verifies an account balance or single-use gift card before recording the debit in the database, sending multiple HTTP requests simultaneously in a multi-threaded burst can exploit the time-of-check to time-of-use (TOCTOU) race window.

Using Burp Suite's **Repeater Parallel Request Engine** (HTTP/2 Single-Packet Attack), an attacker can send 20 requests arriving inside the exact same TCP packet, redeeming a single-use coupon 20 times simultaneously!

---

## 5. Modern API Security: REST, GraphQL & JWT

### GraphQL Security Auditing
Unlike traditional REST APIs that expose discrete endpoints, GraphQL provides a single endpoint (typically `/graphql`) accepting complex nested queries.

1. **Introspection Query Abuse**: Querying `__schema` to dump the entire API data model, hidden queries, mutations, and internal types:
   ```graphql
   query {
     __schema {
       types {
         name
         fields {
           name
         }
       }
     }
   }
   ```
2. **Batching & Denial-of-Service**: Sending queries nested 50 levels deep or bundling hundreds of queries inside a single HTTP payload to exhaust database connections.

### JSON Web Token (JWT) Vulnerability Checklist
* **Algorithm Confusion (None Algorithm)**: Modifying the header `{"alg": "none"}` and stripping the signature to verify if the server accepts unsigned tokens.
* **Key Confusion (RS256 to HS256)**: If the backend expects an RSA public key for verification, modifying the token header to `HS256` and signing the token using the server's public certificate as the HMAC secret key.
* **Weak Secret Cracking**: Extracting the signature and cracking HMAC secrets offline using Hashcat (Mode 16500) against standard wordlists.

---

## 6. Defensive Architecture & Secure Coding Principles

Securing modern web applications requires embedding defense-in-depth controls across the software development lifecycle:

1. **Context-Aware Encoding & Parameterized Queries**:
   * Always use prepared statements (`PreparedStatement` in Java, parameterized queries in Python/Node.js) to eliminate SQL injection.
   * Apply context-specific output encoding (HTML, JavaScript, CSS, URL) to neutralize Cross-Site Scripting.
2. **Centralized Policy-Based Authorization**:
   * Never rely on client-side state or hidden fields for authorization.
   * Implement centralized access control policies (Attribute-Based Access Control - ABAC) verified on every individual controller action.
3. **Hardened HTTP Security Headers**:
   ```http
   Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-random'; frame-ancestors 'none';
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   ```

---

## References & Authoritative Reading

1. [OWASP Top 10 — Application Security Risks](https://owasp.org/www-project-top-ten/)
2. [PortSwigger Web Security Academy — Interactive Research Labs](https://portswigger.net/web-security)
3. [OWASP Web Security Testing Guide (WSTG v4.2)](https://owasp.org/www-project-web-security-testing-guide/)
4. [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
5. Stuttard, Dafydd, and Pinto, Marcus. *The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws*. Wiley, 2nd Edition.

---

## Let's Connect

Have you audited complex web applications or identified novel business logic vulnerabilities? Feel free to reach out:

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) · [GitHub](https://github.com/3bdo-fathi) · [Contact Page](/contact-me/)

*— Abdulrahman M. Fathi*
