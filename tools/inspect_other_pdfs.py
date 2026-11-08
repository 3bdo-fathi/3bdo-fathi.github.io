from pypdf import PdfReader

for path in [r"d:\Download\tele\Android Penetration Testing -1.pdf", r"d:\Download\tele\Android Mobile App Pentesting.pdf"]:
    print("=" * 60)
    print("Inspecting:", path)
    reader = PdfReader(path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        header = " | ".join(lines[:3]) if lines else "EMPTY"
        print(f"Page {i+1}: {header[:120]}")

