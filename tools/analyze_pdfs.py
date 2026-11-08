from pypdf import PdfReader
import json

paths = [
    r"d:\Download\tele\Mobile Penetration Testing Guide.pdf",
    r"d:\Download\tele\Android Penetration Testing -1.pdf",
    r"d:\Download\tele\Android Mobile App Pentesting.pdf"
]

for p in paths:
    print("=" * 60)
    print("File:", p)
    try:
        reader = PdfReader(p)
        print("Num pages:", len(reader.pages))
        meta = reader.metadata
        print("Title:", meta.title if meta else "None")
        print("Author:", meta.author if meta else "None")
        print("Subject:", meta.subject if meta else "None")
        
        # Check first 3 pages text
        for i in range(min(5, len(reader.pages))):
            text = reader.pages[i].extract_text()
            if text:
                first_lines = text.strip().split("\n")[:4]
                print(f"Page {i+1} preview:", " | ".join(first_lines))
                
        # Check outline / bookmarks
        try:
            outline = reader.outline
            print(f"Outline items count: {len(outline) if outline else 0}")
            if outline:
                def print_outline(items, level=0, limit=[25]):
                    for item in items:
                        if limit[0] <= 0:
                            return
                        if isinstance(item, list):
                            print_outline(item, level + 1, limit)
                        else:
                            title = getattr(item, 'title', str(item))
                            print("  " * level + "- " + str(title))
                            limit[0] -= 1
                print("Outline sample:")
                print_outline(outline)
        except Exception as e:
            print("Outline error:", e)

    except Exception as e:
        print("Error reading PDF:", e)

