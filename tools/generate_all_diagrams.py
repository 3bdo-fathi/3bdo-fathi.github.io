from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    try:
        font_header = ImageFont.truetype("arialbd.ttf", 24)
        font_sub = ImageFont.truetype("arial.ttf", 15)
        font_title = ImageFont.truetype("arialbd.ttf", 18)
        font_body = ImageFont.truetype("arial.ttf", 14)
        font_tag = ImageFont.truetype("arialbd.ttf", 12)
        return font_header, font_sub, font_title, font_body, font_tag
    except:
        return None, None, None, None, None

def base_canvas(w=1100, h=650, title="", subtitle=""):
    img = Image.new("RGBA", (w, h), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)
    fh, fs, _, _, _ = get_fonts()
    draw.text((50, 35), title, fill=(255, 255, 255, 255), font=fh)
    draw.text((50, 70), subtitle, fill=(139, 148, 158, 255), font=fs)
    draw.line([(50, 105), (w - 50, 105)], fill=(48, 54, 61, 200), width=1)
    return img, draw

def gen_ch2():
    img, draw = base_canvas(1100, 650, "CHAPTER 2: INFORMATION GATHERING & COMMUNICATION MODELING", "Shannon-Weaver Model & David Berlo's SMCR Framework in Social Engineering")
    _, _, ft, fb, ftag = get_fonts()

    # SMCR Columns
    cols = [
        ("SOURCE (S)", ["• Communication Skills", "• Attitude & Demeanor", "• Technical Knowledge", "• Social System", "• Culture"], (57, 197, 207, 255), (57, 197, 207, 25), 60),
        ("MESSAGE (M)", ["• Content & Data", "• Elements & Symbols", "• Treatment & Tone", "• Structure & Storyline", "• Code / Jargon"], (88, 166, 255, 255), (88, 166, 255, 25), 310),
        ("CHANNEL (C)", ["• Seeing (Visual Cues)", "• Hearing (Vocal Tone)", "• Touching (Kinesthetic)", "• Phone / Email / In-Person", "• Physical Media (USB/CD)"], (188, 140, 255, 255), (188, 140, 255, 25), 560),
        ("RECEIVER (R)", ["• Target Perception", "• Personal Reality & Biases", "• Current Emotional State", "• Social Obligation", "• Feedback / Compliance"], (63, 185, 80, 255), (63, 185, 80, 25), 810)
    ]

    for title, items, color, bg, x in cols:
        draw.rounded_rectangle([(x, 130), (x + 230, 380)], radius=10, fill=bg, outline=color, width=2)
        draw.text((x + 16, 145), title, fill=color, font=ft)
        draw.line([(x + 16, 175), (x + 214, 175)], fill=color, width=1)
        iy = 195
        for it in items:
            draw.text((x + 16, iy), it, fill=(201, 209, 217, 255), font=fb)
            iy += 32

    # Bottom Recon Source Matrix
    draw.rounded_rectangle([(60, 410), (1040, 610)], radius=10, fill=(22, 27, 34, 255), outline=(48, 54, 61, 255), width=1)
    draw.text((80, 425), "CORE INFORMATION SOURCES FOR TARGET PROFILING", fill=(240, 136, 62, 255), font=ft)
    
    sources = [
        ("Websites & Public Servers", "Whois records, IP ranges, job postings, executive bios, support forums."),
        ("Search Engine Recon (Google & Shodan)", "Google Dorks (filetype:pdf, doc, xls), exposed databases, open IIS/Apache."),
        ("Social Media & Digital Footprints", "LinkedIn hierarchy mapping, Facebook/Instagram geolocation EXIF data."),
        ("Physical Recon & Dumpster Diving", "Discarded invoices, shredded documents, badge styles, shift change schedules.")
    ]
    sy = 465
    for s_title, s_desc in sources:
        draw.text((80, sy), f"• {s_title}:", fill=(255, 255, 255, 255), font=fb)
        draw.text((370, sy), s_desc, fill=(139, 148, 158, 255), font=fb)
        sy += 34

    img.save("assets/images/posts/social-engineering/ch2-communication-model.png")
    print("Saved ch2-communication-model.png")

def gen_ch3():
    img, draw = base_canvas(1100, 650, "CHAPTER 3: THE ELICITATION PROCESS & QUESTIONING FUNNEL", "NSA Elicitation Guidelines, Psychological Triggers, and Conversational Preloading")
    _, _, ft, fb, _ = get_fonts()

    # Funnel steps
    funnel = [
        ("1. Neutral Opener", "Icebreakers, mutual environment, informal chit-chat", 80, 130, 940, (57, 197, 207, 255)),
        ("2. Open-Ended Questions", "How & Why inquiries that require narrative responses", 140, 200, 820, (88, 166, 255, 255)),
        ("3. Assumptive & Closed Questions", "Leading statements presupposing target knowledge", 200, 270, 700, (188, 140, 255, 255)),
        ("4. Direct Exploitation Inquiry", "Specific extraction of credentials, processes, or access", 260, 340, 580, (248, 81, 73, 255))
    ]

    for title, desc, x, y, w, color in funnel:
        draw.rounded_rectangle([(x, y), (x + w, y + 55)], radius=8, fill=(22, 27, 34, 255), outline=color, width=2)
        draw.text((x + 20, y + 15), title, fill=color, font=ft)
        draw.text((x + 320, y + 17), desc, fill=(201, 209, 217, 255), font=fb)

    # 4 Human Tendencies Exploit Table
    draw.rounded_rectangle([(80, 420), (1020, 610)], radius=10, fill=(22, 27, 34, 255), outline=(48, 54, 61, 255), width=1)
    draw.text((100, 435), "THE 4 PSYCHOLOGICAL TRIGGERS OF EXPERT ELICITATION", fill=(63, 185, 80, 255), font=ft)
    
    triggers = [
        ("Desire to Be Polite", "Strangers rarely want to seem rude; asking gently lowers natural defenses."),
        ("Professional Pride & Ego", "People love talking about their accomplishments and correcting mistakes."),
        ("The Need to Correct Misstatements", "Deliberately stating wrong facts triggers the target to correct with real data."),
        ("Reciprocal Disclosure", "Volunteering personal details compels the target to share equal information.")
    ]
    ty = 475
    for t_name, t_desc in triggers:
        draw.text((100, ty), f"• {t_name}:", fill=(255, 255, 255, 255), font=fb)
        draw.text((380, ty), t_desc, fill=(139, 148, 158, 255), font=fb)
        ty += 32

    img.save("assets/images/posts/social-engineering/ch3-elicitation-funnel.png")
    print("Saved ch3-elicitation-funnel.png")

def gen_ch4():
    img, draw = base_canvas(1100, 650, "CHAPTER 4: PRETEXTING — THE ARCHITECTURE OF IDENTITY", "Constructing Believable Characters, Cognitive Dissonance, and Operational Principles")
    _, _, ft, fb, _ = get_fonts()

    # 6 Principles of Pretexting
    boxes = [
        ("Thorough Research", "Depth of intel directly dictates believable persona creation.", 60, 130),
        ("Involve Personal Interests", "Align pretexts with hobbies you naturally speak of with confidence.", 390, 130),
        ("Practice Dialects & Lingo", "Master industry jargon without forcing fake, awkward accents.", 720, 130),
        ("Keep Pretext Simple", "Complex lies invite memory errors and suspicion. Simplicity wins.", 60, 270),
        ("Cultivate Spontaneity", "Rely on dynamic outlines rather than rigid, robotic scripts.", 390, 270),
        ("Provide Logical Conclusion", "Give the target closure or an exit justification so doubts don't linger.", 720, 270),
    ]

    for title, desc, x, y in boxes:
        draw.rounded_rectangle([(x, y), (x + 310, y + 110)], radius=8, fill=(22, 27, 34, 255), outline=(240, 136, 62, 255), width=2)
        draw.text((x + 14, y + 14), title, fill=(240, 136, 62, 255), font=ft)
        draw.text((x + 14, y + 45), desc, fill=(201, 209, 217, 255), font=fb)

    # Bottom case study breakdown
    draw.rounded_rectangle([(60, 410), (1030, 610)], radius=10, fill=(22, 27, 34, 255), outline=(48, 54, 61, 255), width=1)
    draw.text((80, 425), "CASE COMPARISON: STANLEY RIFKIN ($10.2M HEIST) VS HEWLETT-PACKARD SCANDAL", fill=(88, 166, 255, 255), font=ft)
    
    comparisons = [
        ("Rifkin's Bank Pretext (1978)", "Impersonated computer maintenance, walked into wire transfer room, memorized code of the day."),
        ("Flawless Telephone Execution", "Called transfer desk as 'Mike Hansen', spoke official bank jargon, wired funds to Swiss diamond dealers."),
        ("HP Pretexting Debacle (2006)", "Investigators used false pretenses to obtain private phone records of board members and journalists."),
        ("The Legal Boundary", "FTC Act & Privacy Protection Act of 2006 strictly criminalize obtaining telecom & banking data fraudulently.")
    ]
    cy = 465
    for c_title, c_desc in comparisons:
        draw.text((80, cy), f"• {c_title}:", fill=(255, 255, 255, 255), font=fb)
        draw.text((370, cy), c_desc, fill=(139, 148, 158, 255), font=fb)
        cy += 32

    img.save("assets/images/posts/social-engineering/ch4-pretexting-workflow.png")
    print("Saved ch4-pretexting-workflow.png")

def gen_ch5():
    img, draw = base_canvas(1100, 650, "CHAPTER 5: PSYCHOLOGICAL PRINCIPLES & MIND TRICKS", "Paul Ekman's 7 Microexpressions, NLP Embedding, and Human Buffer Overflows")
    _, _, ft, fb, _ = get_fonts()

    # Microexpression grid
    emotions = [
        ("Anger", "Lowered brows, glaring eyes, tight narrow lips.", (235, 87, 87, 255)),
        ("Disgust", "Wrinkled nose, raised upper lip, bared teeth.", (240, 136, 62, 255)),
        ("Contempt", "Unilateral (one-sided) mouth curl or smirk.", (210, 153, 34, 255)),
        ("Fear", "Raised straight eyebrows, wide open eyes, tense mouth.", (188, 140, 255, 255)),
        ("Surprise", "Arched high brows, relaxed dropped jaw, wide eyes.", (57, 197, 207, 255)),
        ("Sadness", "Inner brows drawn up, drooping eyelids, lip corners down.", (88, 166, 255, 255)),
        ("True Happiness", "Duchenne smile: eye crinkles (orbicularis oculi) + mouth.", (63, 185, 80, 255))
    ]

    gx, gy = 60, 130
    for idx, (name, cue, col) in enumerate(emotions):
        draw.rounded_rectangle([(gx, gy), (gx + 220, gy + 100)], radius=8, fill=(22, 27, 34, 255), outline=col, width=2)
        draw.text((gx + 12, gy + 12), name, fill=col, font=ft)
        draw.text((gx + 12, gy + 42), cue, fill=(201, 209, 217, 255), font=fb)
        gx += 245
        if (idx + 1) % 4 == 0:
            gx = 60
            gy += 120

    # The Human Buffer Overflow Equation
    draw.rounded_rectangle([(60, 420), (1040, 610)], radius=10, fill=(22, 27, 34, 255), outline=(235, 87, 87, 255), width=2)
    draw.text((80, 435), "THE HUMAN BUFFER OVERFLOW (HBO) EQUATION", fill=(235, 87, 87, 255), font=ft)
    draw.text((80, 470), "Human Buffer Overflow  =  Law of Expectations  +  Mental Padding  +  Embedded Commands", fill=(255, 255, 255, 255), font=ft)

    hbo_steps = [
        ("1. Cognitive Fuzzing", "Presenting input outside expected social schemas to force subconscious processing."),
        ("2. Mental Padding", "Using non-threatening conversational filler ('When you...', 'How do you feel when...')."),
        ("3. Command Injection", "Dropping vocal pitch on action words so the unconscious mind executes without resistance.")
    ]
    hy = 515
    for h_name, h_desc in hbo_steps:
        draw.text((80, hy), f"• {h_name}:", fill=(88, 166, 255, 255), font=fb)
        draw.text((270, hy), h_desc, fill=(139, 148, 158, 255), font=fb)
        hy += 30

    img.save("assets/images/posts/social-engineering/ch5-human-buffer-overflow.png")
    print("Saved ch5-human-buffer-overflow.png")

def gen_ch6():
    img, draw = base_canvas(1100, 650, "CHAPTER 6: INFLUENCE & THE POWER OF PERSUASION", "Robert Cialdini's Weapons of Influence, Reality Framing, and Manipulation Tactics")
    _, _, ft, fb, _ = get_fonts()

    # 4 Influence Columns
    cols = [
        ("RECIPROCITY", ["• Obligation to return favors", "• Creating indebted feelings", "• Unsolicited small gifts", "• Concessions in negotiation"], (63, 185, 80, 255), 60),
        ("SCARCITY & URGENCY", ["• Limited time or quantity", "• Fear of missing out (FOMO)", "• Artificial constraints", "• High perceived exclusivity"], (210, 153, 34, 255), 310),
        ("AUTHORITY", ["• Compliance with symbols", "• Uniforms, titles, business cards", "• Milgram / Cialdini nurse tests", "• Organizational hierarchy"], (88, 166, 255, 255), 560),
        ("SOCIAL PROOF", ["• Imitating group behavior", "• Salting the tip jar effect", "• High uncertainty compliance", "• Peer consensus pressure"], (188, 140, 255, 255), 810)
    ]

    for title, items, color, x in cols:
        draw.rounded_rectangle([(x, 130), (x + 230, 320)], radius=10, fill=(22, 27, 34, 255), outline=color, width=2)
        draw.text((x + 14, 145), title, fill=color, font=ft)
        draw.line([(x + 14, 175), (x + 216, 175)], fill=color, width=1)
        iy = 190
        for it in items:
            draw.text((x + 14, iy), it, fill=(201, 209, 217, 255), font=fb)
            iy += 28

    # Reality Framing Matrix
    draw.rounded_rectangle([(60, 360), (1040, 610)], radius=10, fill=(22, 27, 34, 255), outline=(48, 54, 61, 255), width=1)
    draw.text((80, 375), "THE 4 MECHANISMS OF FRAME ALIGNMENT (SNOW & BENFORD)", fill=(57, 197, 207, 255), font=ft)
    
    frames = [
        ("Frame Bridging", "Connecting two structurally unconnected frames to establish common mental ground."),
        ("Frame Amplification", "Highlighting, accenting, and exaggerating core existing values or anxieties."),
        ("Frame Extension", "Broadening the scope of an operation to encompass the target's personal interests."),
        ("Frame Transformation", "Completely redefining an established belief system into a new conceptual model.")
    ]
    fy = 415
    for f_title, f_desc in frames:
        draw.text((80, fy), f"• {f_title}:", fill=(255, 255, 255, 255), font=fb)
        draw.text((280, fy), f_desc, fill=(139, 148, 158, 255), font=fb)
        fy += 45

    img.save("assets/images/posts/social-engineering/ch6-influence-weapons.png")
    print("Saved ch6-influence-weapons.png")

def gen_ch7():
    img, draw = base_canvas(1100, 650, "CHAPTER 7: THE TOOLS OF THE SOCIAL ENGINEER", "Physical Infiltration Gear, Phone Spoofing, Recon Software, and Password Profilers")
    _, _, ft, fb, _ = get_fonts()

    # Left Box: Physical Infiltration Tools
    draw.rounded_rectangle([(60, 130), (530, 400)], radius=10, fill=(22, 27, 34, 255), outline=(240, 136, 62, 255), width=2)
    draw.text((80, 145), "PHYSICAL INFILTRATION ARSENAL", fill=(240, 136, 62, 255), font=ft)
    p_tools = [
        ("Lock Picks & Rakes", "Tension wrenches and rakes to bypass pin-tumbler locks in < 30 seconds."),
        ("Shove Knives", "Sliding between latch and strike plate to pop office and server room doors."),
        ("Padlock Shims", "Thin spring steel shims slipped into lock shackles to release pawls."),
        ("Bump Keys", "Special cut keys applying kinetic energy to align tumblers instantaneously."),
        ("Covert Cameras", "Hidden in ties, pens, hats, or smoke detectors for reconnaissance proof.")
    ]
    py = 180
    for t_name, t_desc in p_tools:
        draw.text((80, py), f"• {t_name}:", fill=(255, 255, 255, 255), font=fb)
        draw.text((240, py), t_desc, fill=(139, 148, 158, 255), font=fb)
        py += 40

    # Right Box: Digital & Telephony Tools
    draw.rounded_rectangle([(560, 130), (1040, 400)], radius=10, fill=(22, 27, 34, 255), outline=(88, 166, 255, 255), width=2)
    draw.text((580, 145), "DIGITAL & TELEPHONY TOOLKIT", fill=(88, 166, 255, 255), font=ft)
    d_tools = [
        ("Caller ID Spoofing", "SpoofCard, SpoofApp, and self-hosted Asterisk VoIP PBX servers."),
        ("Social Engineer Toolkit (SET)", "Dave Kennedy's suite: spear phishing, Java applets, website cloner."),
        ("Maltego (Paterva)", "Transform-based relationship mapping connecting domains, emails, and humans."),
        ("CUPP & CeWL", "Common User Password Profiler & website scraping dictionary generators."),
        ("GPS Trackers (SuperTrak)", "Magnetic covert loggers mapped directly into Google Earth trajectories.")
    ]
    dy = 180
    for t_name, t_desc in d_tools:
        draw.text((580, dy), f"• {t_name}:", fill=(255, 255, 255, 255), font=fb)
        draw.text((790, dy), t_desc, fill=(139, 148, 158, 255), font=fb)
        dy += 40

    # Bottom Core Takeaway
    draw.rounded_rectangle([(60, 430), (1040, 610)], radius=10, fill=(22, 27, 34, 255), outline=(63, 185, 80, 255), width=1)
    draw.text((80, 445), "THE GOLDEN AUDITOR PRINCIPLE: TOOLS DO NOT MAKE THE SOCIAL ENGINEER", fill=(63, 185, 80, 255), font=ft)
    draw.text((80, 485), "• A tool is only as effective as the pretext, confidence, and research backing it up.", fill=(201, 209, 217, 255), font=fb)
    draw.text((80, 520), "• Expensive surveillance devices fail if the operator cannot maintain poise during questioning.", fill=(201, 209, 217, 255), font=fb)
    draw.text((80, 555), "• Practice, operational timing, and situational adaptability remain paramount.", fill=(201, 209, 217, 255), font=fb)

    img.save("assets/images/posts/social-engineering/ch7-tools-arsenal.png")
    print("Saved ch7-tools-arsenal.png")

def gen_ch8():
    img, draw = base_canvas(1100, 650, "CHAPTER 8: CASE STUDIES — DISSECTING THE ATTACKS", "Real-World Social Engineering Exploits Dissected Through the SE Framework")
    _, _, ft, fb, _ = get_fonts()

    cases = [
        ("Mitnick: DMV Hack", "Local Sheriff teletype inquiry -> Nortel switch takeover -> call forwarding to burn phone -> identity harvesting of detectives.", (57, 197, 207, 255), 60, 130),
        ("Mitnick: SSA Hack", "Private investigator used POMS manual terminology, called Mod 3 as Inspector General, pulled detailed earnings query (DEQY).", (88, 166, 255, 255), 560, 130),
        ("Hadnagy: Overconfident CEO", "Target guarded servers personally; OSINT revealed cancer charity donation; pretexted raffle ticket with malicious PDF payload.", (210, 153, 34, 255), 60, 310),
        ("Hadnagy: Theme Park Ticket", "Pretexted distressed father with broken hotel printer; convinced ticket teller to log into Gmail & open infected receipt PDF.", (63, 185, 80, 255), 560, 310),
        ("Top Secret 1: Mission Not Impossible", "Dumpster dive revealed vendor contract; pretexted IT maintenance, booted target admin machine into BackTrack VM with keylogger.", (188, 140, 255, 255), 60, 490),
        ("Top Secret 2: SE a Rogue Hacker", "Pentester encountered live intruder on open VNC; opened Notepad, pretexted as 'n00b' hacker, extracted intruder's tools and email.", (248, 81, 73, 255), 560, 490)
    ]

    for title, desc, col, x, y in cases:
        draw.rounded_rectangle([(x, y), (x + 480, y + 140)], radius=8, fill=(22, 27, 34, 255), outline=col, width=2)
        draw.text((x + 14, y + 12), title, fill=col, font=ft)
        draw.text((x + 14, y + 44), desc, fill=(201, 209, 217, 255), font=fb)

    img.save("assets/images/posts/social-engineering/ch8-case-studies-breakdown.png")
    print("Saved ch8-case-studies-breakdown.png")

def gen_ch9():
    img, draw = base_canvas(1100, 650, "CHAPTER 9: PREVENTION, MITIGATION & SECURITY CULTURE", "Hardening the Human Attack Surface: Active Awareness, Verification Scripts & Auditing")
    _, _, ft, fb, _ = get_fonts()

    # 6 Steps of SE Defense
    steps = [
        ("1. Attack Identification", "Educate personnel on recognizing pretext indicators, urgency tactics, and emotional levers.", (57, 197, 207, 255)),
        ("2. Personal Security Awareness", "Connect security training to employees' personal lives, banking, and families so it resonates.", (88, 166, 255, 255)),
        ("3. Understanding Information Value", "Train staff that seemingly trivial data (cafeteria vendors, phone extensions) enables complex hacks.", (188, 140, 255, 255)),
        ("4. Keeping Software Updated", "Patch browsers, PDF readers, and operating systems to eliminate payload execution vectors.", (210, 153, 34, 255)),
        ("5. Standardized Response Scripts", "Provide clear, procedural outlines for employees to follow when authority figures make urgent demands.", (63, 185, 80, 255)),
        ("6. Ongoing Ethical SE Audits", "Continuously stress-test human defenses without punitive retaliation against tricked employees.", (248, 81, 73, 255))
    ]

    sy = 130
    for idx, (title, desc, col) in enumerate(steps):
        draw.rounded_rectangle([(60, sy), (1040, sy + 65)], radius=8, fill=(22, 27, 34, 255), outline=col, width=2)
        draw.text((80, sy + 18), title, fill=col, font=ft)
        draw.text((360, sy + 20), desc, fill=(201, 209, 217, 255), font=fb)
        sy += 78

    img.save("assets/images/posts/social-engineering/ch9-mitigation-blueprint.png")
    print("Saved ch9-mitigation-blueprint.png")

if __name__ == "__main__":
    gen_ch2()
    gen_ch3()
    gen_ch4()
    gen_ch5()
    gen_ch6()
    gen_ch7()
    gen_ch8()
    gen_ch9()
    print("All diagrams generated successfully!")
