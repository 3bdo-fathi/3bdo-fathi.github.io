---
title: "From Dark Web Fame to Digital Attribution: The Story of How OPSEC Failures Can Destroy Years of Anonymity"
date: 2026-05-28 12:14:00 +0300
categories: [Research, Security News]
tags: [INT3X, OPSEC, Threat Intelligence, OSINT, Quellostanco, Cyber Attribution, BlueKeep, Egyptian Cyber Threat]
image:
  path: /assets/images/posts/int3x-opsec-cover.jpg  
  alt: int3x-opsec-cover
---
Hello everyone,

I hope you're doing well and having a great day.

In today's article, we'll take a closer look at a real-world attribution case that attracted significant attention within the Egyptian cybersecurity community. Beyond the headlines, this case provides valuable lessons about Operational Security (OPSEC), Open-Source Intelligence (OSINT), and the reality of digital attribution.

My goal is not to focus on individuals, but rather to examine the investigative methodology, the mistakes that enabled attribution, and the lessons security professionals can learn from the process.

Whether you're interested in Threat Intelligence, OSINT, Digital Forensics, or Cyber Threat Attribution, this case demonstrates how small pieces of publicly available information can eventually form a much larger picture.

Let's get started.

Over the past several months, the Egyptian cybersecurity community has been closely following a series of attacks, breach claims, defacements, and data leak announcements targeting universities, educational platforms, government entities, and private organizations. During that period, one alias repeatedly appeared across underground forums, dark web marketplaces, breach announcements, and cybercrime communities: **Quellostanco**, a member of the **INT3X** group that became one of the most talked-about threat actor groups targeting Egyptian organizations throughout 2026. With every new breach claim, the group's reputation continued to grow, and many people began viewing them as highly sophisticated attackers who understood anonymity, operational security, and underground operations.

From the outside, the group looked exactly like what most people imagine when they think about cybercriminals. Anonymous identities, dark web activity, VPNs, encrypted messaging applications, underground communities, and public claims of major breaches all contributed to an image of individuals operating completely beyond reach. To many observers, it appeared that identifying the people behind these aliases would require advanced intelligence operations, highly sophisticated cyber investigations, or access to information unavailable to the public.

What happened next demonstrated something that cybersecurity professionals have been saying for years: **most threat actors are not exposed because someone hacks them. Most threat actors are exposed because they gradually expose themselves.**

## The Misconception About Attribution

One of the biggest misconceptions in cybersecurity is the belief that attribution begins with malware analysis, server exploitation, infrastructure compromises, or advanced digital forensics. In reality, many investigations begin with something much simpler. A username. An email address. A profile photo. A forum post. A writing style. A Git commit. A small artifact that seems completely meaningless on its own but becomes extremely valuable when combined with hundreds of other artifacts collected over time. Attribution is rarely about finding one massive mistake. It is usually about finding dozens of small mistakes and understanding how they connect together.


The investigation surrounding Quellostanco serves as an excellent example of this process. Researchers initially began by tracking the alias across different platforms and communities. The goal was straightforward: identify where the username appeared, determine whether variations of the name existed elsewhere, and understand whether the same individual was reusing digital identities across multiple services. Like many internet users, the actor appeared to have developed habits. Those habits eventually became one of the most valuable sources of intelligence throughout the entire investigation.

## Who is Quellostanco?

Quellostanco is a threat actor who gained attention in early 2026 after conducting and advertising multiple cyberattacks targeting Egyptian organizations, universities, and companies. The actor became particularly active across cybercrime forums, where they promoted stolen databases, leaked sensitive information, and claimed responsibility for several breaches and defacement operations.

The actor frequently collaborated with other threat actors, including CrowStealer and bigF, in breach sales and data leak operations under the INT3X team banner.

### Notable Activities Attributed to Quellostanco:

| Date | Target | Activity |
|------|--------|----------|
| 9 February | EgyptAir | Advertised database of ~104,000 records from HR and recruitment systems |
| 23 February | Egyptalum | Defaced website and claimed full control over systems |
| 25 February | General Authority for Roads and Bridges | Breached Contract Extract System |
| 10 May | Mansoura University | ~989,000 student records (2012-2026), photographs, internal documents |
| 14 May | mutreasury Payment Gateway | Claimed breach affecting 28+ universities with zero-day vulnerability |
| 17 May | pat.edu.eg | Compromised and defaced platform |

## The OSINT Methodology: How Attribution Really Works

As researchers expanded their analysis, they began discovering accounts across different platforms that appeared connected through remarkably similar characteristics. Username variations started appearing in multiple locations. Profile descriptions shared common themes. Writing styles exhibited similar patterns. Technical interests repeatedly overlapped. Certain behavioral indicators appeared again and again. None of these findings individually identified anyone, but attribution is not built upon isolated findings. Attribution is built through correlation. When independent sources repeatedly point toward the same conclusion, confidence increases. This is one of the most important principles in both OSINT and Threat Intelligence.

### Step 1: Username Correlation

First, researchers searched for the username across multiple breach datasets because a threat actor's chosen alias is often the simplest and most consistently reused identifier across platforms. Ironically, the forums where criminals operate get breached too — and when they do, the personal details criminals entered to register (IP addresses, emails, recovery info) are exposed just like anyone else's.

Several leaked IP addresses were identified tied to the Quellostanco account. Most were linked to VPN providers, which is common among threat actors attempting to conceal their real location. However, three of the identified IP addresses resolved to Egyptian networks, making them particularly noteworthy.

A common behavior among threat actors is reusing the same username across many platforms and email services — a habit formed long before they had a reason to be careful. Working from that assumption, researchers systematically combined `quellostanco` with common email domains. One result stood out: `quellostanco@outlook.com`. OSINT analysis of that address showed it was tied to an Egyptian Microsoft account and a phone number ending in **94**. Those two digits became a critical piece of evidence.

### Step 2: Persona Reuse Across Platforms

On one of the websites it breached, the actor signed the work "Quello$tanco" — the same name with a stylized "S." Small stylistic choices like this are habits, and habits travel between accounts.

A simple Google search for that variation led to a **HackerOne profile** using `quello_stanco`. The account used the INT3X group image as its profile picture and listed an address in Giza.

A **Bugcrowd account** was also identified using the same username, with a different bio. Using both bios as pivot points, researchers identified a **Reddit account** that appeared to combine elements from both profiles.

One post from the Reddit account contained an Arabic-language rant criticizing the cybersecurity and hacking scene in Egypt — which later played a role in gathering members for the INT3X group.

### Step 3: The Git Trail — Extracting Identity from Commit Metadata

Since `quellostanco` used `quello_stanco` as a username variation, additional variations were tested. One variation stood out, leading to a **GitHub account**.

Reviewing Git repositories and commit history is an important step during attribution investigations, as Git commits often contain metadata automatically attached by Git itself. This metadata can include usernames, email addresses, and timestamps that may unintentionally expose identifying information.

In one repository, a commit dated **11 November 2023** exposed a personal email address within the Git metadata. In another repository, the developer's **real name** appeared directly within the project files.

![Git Commit Metadata Exposure](/assets/images/posts/git-commit-exposure.png)   

### Step 4: Confirming Identity with Leaked Email and Phone Number

The exposed email address was searched against breach datasets and infostealer logs. The email appeared in the **2024 ULP dataset**, which also exposed a phone number used as the account password.

> **Significantly, that recovered number ended in 94** — exactly matching the digits flagged much earlier from the `quellostanco@outlook.com` correlation. Two completely independent paths converged on the same phone number.

Since ULP files are commonly derived from infostealer logs, the presence of the exposed credentials strongly suggested that Quellostanco's device had previously been compromised by infostealer malware. Records from infostealer log datasets also exposed a **residential address** linked to the device.

Additional OSINT analysis on the phone number found that the number had been saved by others as a contact under the actor's name together with the name of his institute, written in Arabic.

> **How a phone number reveals a name:** Crowdsourced caller-ID and contact-lookup services work by aggregating address-book entries that millions of users have uploaded. If enough people saved a number under the same name, that name becomes searchable — without the target having done anything.

### Step 5: Professional Profiles and LinkedIn

Further OSINT analysis of the exposed email address revealed an associated **Upwork profile** describing the individual as an "Expert Linux system administrator and Network & security specialist." This matched the Reddit account's posts in the FiverrGigs subreddit about Linux system administration.

Using the attributed data collected throughout the investigation, along with a CTF challenge the actor had previously published a write-up about, researchers identified a **LinkedIn profile** containing his photo and additional personal details.

Notably, the latest post on the profile referenced the same GitHub repository previously identified during the investigation. The profile also revealed a birth date of **26 March**.

### Step 6: Direct Communication with Quellostanco

To gather additional information, researchers contacted the actor directly using the previously identified Reddit account — under the pretext of being a potential client interested in obtaining services.

During the conversation, the actor provided his **Session ID** (encrypted messaging). The Session ID was associated with an account using the name **Quello$tanco**, further linking the Reddit account to the alias.

The actor claimed to be the **founder of the INT3X group** and stated that he had previously used Reddit to recruit potential members. He later invited researchers to a Discord channel, where the account used the same alias previously identified on the GitHub profile.

While sharing his screen using another account named `ettaproject`, the actor accidentally exposed his Discord interface, revealing the servers, channels, and users associated with the account.

## The Aftermath: Account Deletion

After Quellostanco defaced `pat.edu.eg` and left a message directed at the Egyptian community, multiple individuals began conducting OSINT investigations. Shortly afterward, Quellostanco started deleting and changing usernames across several accounts, including GitHub, Upwork, and HackerOne profiles.

However, by that stage, researchers had already attributed and documented the actor's identity and associated infrastructure before the accounts were modified or removed.

## The Bigger Picture: What This Case Teaches Us

Perhaps the most important lesson from this entire case is that **there was no single catastrophic failure**. There was no moment where the actor accidentally revealed everything. There was no dramatic mistake that immediately exposed an identity. Instead, there were countless small mistakes accumulated over years:

- Username reuse
- Metadata exposure
- Historical accounts
- Repeated interests
- Consistent behavioral patterns
- Similar communication styles
- Public technical discussions
- Digital footprints left across multiple platforms

Individually, each artifact appeared insignificant. Together, they became overwhelming.

## Technical Skills vs. Operational Security

This investigation also highlights a reality that many people entering cybersecurity fail to fully appreciate: **Technical capability and operational security are not the same thing.**

Someone can be exceptionally skilled in penetration testing, exploitation, networking, malware development, reverse engineering, or vulnerability research and still fail completely at operational security. Technical expertise does not automatically provide anonymity. In many cases, highly skilled individuals become overconfident and begin assuming that technology alone will protect them. Unfortunately, technology cannot compensate for years of poor habits.

## Why This Case Attracted Attention

One of the reasons this case attracted so much attention within the cybersecurity community is because it serves as a practical demonstration of how modern OSINT and Threat Intelligence operations actually work. There were no magical tools. No secret databases. No Hollywood-style cyber warfare. The investigation relied on **patience, research, verification, correlation, and analytical discipline.**

Publicly available information was collected, verified, and connected through multiple independent sources until a clear picture emerged. That methodology represents some of the best principles of modern digital investigations.

## Credits and Acknowledgements

Special recognition should be given to the researchers who contributed to documenting and analyzing the attribution process, including **Eng. Muhammad Matter**, **Eng. Mostafa Farghaly**, and **Eng. Nessam Abdellatef**, alongside everyone else who participated in the research, evidence collection, analysis, and correlation efforts.

This investigation was a collaborative effort between **DeXpose** and **Buguard**. The full uncensored attribution package, including all supporting evidence and the actor's real-world identity, was compiled and formally handed over to the relevant law enforcement authorities.

For the complete technical deep-dive, refer to the official article:  
**[Unmasking Quellostanco: How a Git Commit Exposed a Threat Actor Targeting Egyptian Infrastructure](https://www.dexpose.io/unmasking-quellostanco-how-a-git-commit-exposed-a-threat-actor-targeting-egyptian-infrastructure/)**

## Key Takeaways for Security Professionals

1. **Anonymity is a discipline, not a product** — No single tool (VPN, Tor, encrypted messenger) provides anonymity. It is the result of hundreds of decisions repeated consistently over time.

2. **Good habits strengthen anonymity; poor habits destroy it** — The internet remembers far more than most people realize.

3. **Every profile, repository, account, message, commit, and interaction contributes to a digital footprint** — This footprint can persist for years.

4. **Attribution is built through correlation** — Multiple independent sources supporting the same conclusion create confidence.

5. **False positives are the enemy** — Avoiding accusing the wrong person is the single most important discipline in attribution work.

## Conclusion

In the end, what transformed one of the most discussed aliases in Egypt's cybercrime scene into an attribution case study was not a zero-day vulnerability, advanced malware, or a sophisticated intelligence operation. It was years of small operational security mistakes quietly waiting for someone patient enough to connect the dots.

This case serves as a powerful reminder that anonymity is not achieved through a single tool, platform, or technology. It is the result of consistent habits, disciplined operational security, and a deep understanding of how digital footprints accumulate over time.

For security professionals, researchers, and OSINT practitioners, this investigation demonstrates the importance of patience, correlation, verification, and analytical thinking. The most valuable discoveries often come not from a single breakthrough, but from connecting dozens of seemingly insignificant pieces of information.

> **Technical skills may build a reputation. Operational security is what protects it.**

Thank you for taking the time to read this article.

I hope you found it useful and gained valuable insight into how modern attribution investigations are conducted.

Until the next article, stay curious and keep learning.

— Abdulrahman Mohamed

## Connect With Me

* [LinkedIn Profile](https://www.linkedin.com/in/3bdo-fathi)



---

## Resources and Further Reading

* [Unmasking Quellostanco - DeXpose (Official Article)](https://www.dexpose.io/unmasking-quellostanco-how-a-git-commit-exposed-a-threat-actor-targeting-egyptian-infrastructure/)



