---
title: "Building an Advanced Reconnaissance & DNS Enumeration Framework"
date: 2026-05-20 12:06:00 +0300
categories: [Scripts, Bash]
tags: [reconnaissance, dns, pentesting, automation]
description: "A Bash-based reconnaissance framework automating DNS enumeration, subdomain discovery, HTTP probing, WAF detection, and vulnerability scanning for penetration testers."
image:
  path: /assets/images/Reconnaissance Framework.jpg
  alt: Reconnaissance Framework
---

Hello everyone,

I hope you're doing well and having a great day.

In today's article, I'd like to share a project I've been working on to improve efficiency during reconnaissance and attack surface analysis. As many security professionals know, reconnaissance is often one of the most time-consuming phases of any penetration test, requiring multiple tools, extensive data collection, and significant effort to keep results organized.

The goal of this project was not simply to automate individual tools, but to build a structured framework capable of handling the entire reconnaissance workflow while maintaining clean and organized outputs. By combining DNS enumeration, subdomain discovery, HTTP probing, technology fingerprinting, and vulnerability discovery into a single workflow, the framework helps reduce repetitive tasks and allows analysts to focus more on analysis rather than data collection.

In this article, I'll walk through the framework's architecture, explain the reasoning behind each component, and demonstrate how different reconnaissance stages can be automated effectively using Bash and several widely used security tools.

Let's get started.


Recently, I started building an advanced reconnaissance and DNS enumeration automation framework to improve workflow efficiency during external penetration testing and attack surface analysis.

During most assessments, reconnaissance quickly becomes repetitive:

* DNS enumeration
* Subdomain discovery
* HTTP probing
* WAF detection
* Technology fingerprinting
* URL collection
* Vulnerability discovery

Running these tools manually while organizing outputs can quickly become inefficient.

To solve this problem, I started developing a Bash-based framework capable of automating the entire reconnaissance workflow while keeping results structured, organized, and easy to analyze.

---

## Creating Structured Output Directories

One of the first challenges I wanted to solve was output organization.

Instead of generating random files and terminal outputs, the framework automatically creates a dedicated directory for every target.

```bash
OUTPUT=${OUTPUT:-recon-$DOMAIN}
mkdir -p $OUTPUT
```

This allows all generated files to remain categorized and organized throughout the assessment.

The framework automatically stores:

* DNS records
* Subdomains
* HTTP probing results
* Fingerprints
* SSL analysis
* URL collections
* Vulnerability scans

inside a dedicated output folder.

---

## Dependency Validation

Before starting reconnaissance, the framework validates all required tools to avoid runtime failures.

```bash
TOOLS=(
dig
subfinder
amass
httpx
ffuf
nuclei
whatweb
)

for tool in "${TOOLS[@]}"
do
    if ! command -v $tool &> /dev/null
    then
        echo "[!] $tool not installed"
    fi
done
```

This phase ensures the environment is properly configured before execution.

---

## DNS Enumeration

The reconnaissance workflow begins with DNS and infrastructure analysis.

The framework automatically performs:

* A record lookups
* AAAA enumeration
* MX analysis
* NS enumeration
* TXT extraction
* SOA analysis
* Reverse DNS lookups
* DNS trace analysis
* Zone transfer testing

```bash
RECORDS=(
A
AAAA
MX
NS
TXT
SOA
CNAME
CAA
SRV
ANY
)

for record in "${RECORDS[@]}"
do
    dig $DOMAIN $record > $OUTPUT/$record.txt
done
```

This phase helps identify:

* DNS providers
* Internal naming conventions
* Cloud infrastructure
* CDN usage
* Infrastructure exposure

---

## Resolver Testing

The framework also validates DNS responses across multiple public resolvers.

```bash
RESOLVERS=(
1.1.1.1
8.8.8.8
9.9.9.9
)

for resolver in "${RESOLVERS[@]}"
do
    dig @$resolver $DOMAIN
done
```

Comparing responses helps uncover inconsistencies and infrastructure exposure.

---

## Zone Transfer Testing

The framework automatically attempts DNS zone transfers against discovered name servers.

```bash
NS_SERVERS=$(dig +short NS $DOMAIN)

for ns in $NS_SERVERS
do
    dig axfr @$ns $DOMAIN
done
```

Successful zone transfers may expose:

* Subdomains
* Internal hostnames
* Infrastructure details
* Internal services

---

## Subdomain Enumeration

To maximize coverage, the framework integrates multiple passive discovery tools.

```bash
subfinder -d $DOMAIN -silent > $OUTPUT/subfinder.txt

assetfinder --subs-only $DOMAIN > $OUTPUT/assetfinder.txt

amass enum -passive -d $DOMAIN > $OUTPUT/amass.txt
```

Results are automatically merged and deduplicated.

```bash
cat \
$OUTPUT/subfinder.txt \
$OUTPUT/assetfinder.txt \
$OUTPUT/amass.txt \
| sort -u \
> $OUTPUT/all-subdomains.txt
```

---

## Live Host Discovery

After subdomain collection, active assets are resolved using dnsx.

```bash
dnsx \
-l $OUTPUT/all-subdomains.txt \
-a -resp \
> $OUTPUT/live-hosts.txt
```

This helps identify externally reachable infrastructure.

---

## HTTP Probing

HTTP probing is performed using httpx.

```bash
httpx \
-l $OUTPUT/all-subdomains.txt \
-tech-detect \
-title \
-status-code \
-follow-redirects \
-server \
-ip \
-cdn \
> $OUTPUT/httpx.txt
```

This phase identifies:

* Live web services
* Technologies
* CDN providers
* Response titles
* Server fingerprints
* Redirect chains

---

## WAF Detection

WAF and CDN fingerprinting is performed using wafw00f.

```bash
wafw00f https://$DOMAIN
```

This helps identify protections such as:

* Cloudflare
* Akamai
* Imperva
* AWS WAF

Understanding reverse proxy infrastructure is essential because it directly affects scanning behavior and fingerprinting accuracy.

---

## Technology Fingerprinting

Technology fingerprinting is performed using WhatWeb.

```bash
whatweb https://$DOMAIN -v
```

This phase identifies:

* Web servers
* Frontend frameworks
* JavaScript libraries
* CMS technologies
* Reverse proxies
* Security headers

---

## Historical URL Collection

The framework integrates:

* gau
* waybackurls
* katana

to collect historical and archived endpoints.

```bash
gau $DOMAIN > $OUTPUT/gau.txt

waybackurls $DOMAIN > $OUTPUT/waybackurls.txt
```

This helps uncover:

* Hidden routes
* Legacy APIs
* Archived functionality
* Forgotten endpoints

---

## Directory Enumeration

In Full Scan Mode, directory brute forcing is performed using ffuf.

```bash
ffuf \
-u https://$DOMAIN/FUZZ \
-w $WORDLIST \
-mc 200,204,301,302,307,401,403,405,500
```

This phase helps identify:

* Hidden directories
* Internal routes
* Debug endpoints
* Exposed resources

---

## Vulnerability Discovery

The framework integrates nuclei for automated vulnerability discovery.

```bash
nuclei \
-u https://$DOMAIN \
-severity low,medium,high
```

This allows rapid identification of:

* Misconfigurations
* Exposed services
* Known CVEs
* Common web vulnerabilities

---

## Framework Workflow

The overall execution flow looks like this:

```text
Target Domain
      ↓
Create Output Directory
      ↓
WHOIS Enumeration
      ↓
DNS Enumeration
      ↓
Subdomain Discovery
      ↓
Live Host Resolution
      ↓
HTTP Probing
      ↓
WAF Detection
      ↓
Technology Fingerprinting
      ↓
Historical URL Collection
      ↓
Directory Enumeration
      ↓
Vulnerability Discovery
```

Each phase automatically saves its results into categorized output files, transforming the framework into a structured reconnaissance platform rather than a simple automation script.

---

## Future Improvements

The framework is still under active development and will continue evolving over time.

Planned features include:

* Parallel execution
* HTML reporting
* JSON exports
* Screenshot automation
* Cloud asset enumeration
* GitHub secret discovery
* Advanced endpoint crawling
* AI-assisted finding classification
* Automated reporting support

The goal is to continuously improve reconnaissance efficiency while maintaining analyst-friendly and highly structured outputs during external penetration testing engagements.

---

## Conclusion

Reconnaissance remains one of the most important phases of any penetration testing engagement. The quality of information collected during this stage often determines the effectiveness of everything that follows.

By automating repetitive tasks and organizing results into a structured workflow, security professionals can spend less time gathering information and more time understanding attack surfaces, identifying weaknesses, and prioritizing potential findings.

This framework is still a work in progress, and several additional features are planned for future releases. As the project evolves, the primary objective will remain the same: creating a scalable, organized, and analyst-friendly reconnaissance platform capable of supporting real-world security assessments.

Thank you for taking the time to read this article.

I hope you found it useful and gained some ideas that may help improve your own reconnaissance workflow.

Until the next article, stay curious and keep learning.

— Abdulrahman Mohamed

---

## Let's Connect

Have a question, suggestion, or topic you'd like to discuss?

* [LinkedIn](https://www.linkedin.com/in/3bdo-fathi) · [Contact Page](/contact-me/)

*Abdulrahman M. Fathi*

