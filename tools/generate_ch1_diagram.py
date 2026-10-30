from PIL import Image, ImageDraw, ImageFont

def create_framework_diagram():
    width, height = 1100, 680
    img = Image.new("RGBA", (width, height), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_header = ImageFont.truetype("arialbd.ttf", 26)
        font_sub = ImageFont.truetype("arial.ttf", 16)
        font_card_title = ImageFont.truetype("arialbd.ttf", 18)
        font_card_body = ImageFont.truetype("arial.ttf", 14)
        font_badge = ImageFont.truetype("arialbd.ttf", 13)
    except:
        font_header = font_sub = font_card_title = font_card_body = font_badge = None

    # Title Banner
    draw.text((50, 40), "THE SOCIAL ENGINEERING LIFECYCLE & FRAMEWORK", fill=(255, 255, 255, 255), font=font_header)
    draw.text((50, 75), "Based on Christopher Hadnagy's 'The Art of Human Hacking' — Structural Architecture", fill=(139, 148, 158, 255), font=font_sub)

    # 4-stage pipeline boxes
    stages = [
        ("STAGE 1: RECONNAISSANCE", "Information Gathering", "OSINT, corporate web profiling, metadata analysis, dumpster diving, and employee footprinting.", (57, 197, 207, 30), (57, 197, 207, 255), 50),
        ("STAGE 2: ENGAGEMENT", "Pretexting & Elicitation", "Assuming believable personas, asking targeted open-ended questions without raising alarm.", (88, 166, 255, 30), (88, 166, 255, 255), 305),
        ("STAGE 3: MANIPULATION", "Psychology & Influence", "Triggering reciprocity, scarcity, authority, or causing a 'human buffer overflow' to command action.", (188, 140, 255, 30), (188, 140, 255, 255), 560),
        ("STAGE 4: EXECUTION", "Payload & Access", "Planting malicious media, extracting confidential assets, or pivoting into internal networks.", (248, 81, 73, 30), (248, 81, 73, 255), 815)
    ]

    card_y = 120
    card_w = 235
    card_h = 200

    for idx, (badge, title, desc, bg, accent, x) in enumerate(stages):
        # Card background & border
        draw.rounded_rectangle([(x, card_y), (x + card_w, card_y + card_h)], radius=10, fill=bg, outline=accent, width=2)
        # Stage badge
        draw.rounded_rectangle([(x + 12, card_y + 14), (x + card_w - 12, card_y + 36)], radius=4, fill=(20, 25, 35, 240), outline=accent, width=1)
        draw.text((x + 18, card_y + 18), badge, fill=accent, font=font_badge)
        # Title
        draw.text((x + 14, card_y + 50), title, fill=(255, 255, 255, 255), font=font_card_title)
        
        # Word wrap description
        words = desc.split()
        lines = []
        cur_line = []
        for word in words:
            cur_line.append(word)
            if len(" ".join(cur_line)) > 26:
                cur_line.pop()
                lines.append(" ".join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(" ".join(cur_line))
            
        ly = card_y + 85
        for line in lines:
            draw.text((x + 14, ly), line, fill=(201, 209, 217, 255), font=font_card_body)
            ly += 20

        # Flow arrow between stages
        if idx < 3:
            arrow_x = x + card_w + 5
            arrow_y = card_y + (card_h // 2)
            draw.line([(arrow_x, arrow_y), (arrow_x + 10, arrow_y)], fill=(139, 148, 158, 200), width=2)
            draw.polygon([(arrow_x + 12, arrow_y), (arrow_x + 7, arrow_y - 4), (arrow_x + 7, arrow_y + 4)], fill=(139, 148, 158, 200))

    # Bottom comparison table: Why Social Engineering Works vs Traditional Defenses
    table_y = 360
    draw.rounded_rectangle([(50, table_y), (1050, table_y + 270)], radius=10, fill=(22, 27, 34, 255), outline=(48, 54, 61, 255), width=1)
    
    # Header of table
    draw.line([(50, table_y + 50), (1050, table_y + 50)], fill=(48, 54, 61, 255), width=1)
    draw.line([(550, table_y), (550, table_y + 270)], fill=(48, 54, 61, 255), width=1)

    draw.text((70, table_y + 15), "TRADITIONAL PERIMETER DEFENSES", fill=(88, 166, 255, 255), font=font_card_title)
    draw.text((570, table_y + 15), "THE HUMAN ATTACK SURFACE (SE)", fill=(240, 136, 62, 255), font=font_card_title)

    left_points = [
        ("Firewalls & WAFs", "Blocks malicious network packets and automated port scans."),
        ("Multi-Factor Authentication", "Hardens credential login screens against pure brute force."),
        ("Encryption at Rest", "Secures server drives against raw hardware extraction."),
        ("Endpoint Antivirus", "Detects known signature payloads and unauthorized binaries.")
    ]

    right_points = [
        ("The Human Firewall Gap", "Employees willingly bypass controls when pressured or charmed."),
        ("Pretext Credential Harvesting", "Attackers simply call and ask for passwords or tokens."),
        ("Insider Trust Exploitation", "Physical tailgaters access unlocked server rooms in person."),
        ("Zero-Day Human Trust", "No patch exists for human sympathy, fear, or desire to help.")
    ]

    ty = table_y + 65
    for title, desc in left_points:
        draw.text((70, ty), f"• {title}:", fill=(255, 255, 255, 255), font=font_card_body)
        draw.text((230, ty), desc, fill=(139, 148, 158, 255), font=font_card_body)
        ty += 48

    ty = table_y + 65
    for title, desc in right_points:
        draw.text((570, ty), f"• {title}:", fill=(255, 255, 255, 255), font=font_card_body)
        draw.text((760, ty), desc, fill=(139, 148, 158, 255), font=font_card_body)
        ty += 48

    img.save("assets/images/posts/social-engineering/se-framework-diagram.png", "PNG")
    print("Framework diagram created successfully!")

if __name__ == "__main__":
    create_framework_diagram()
