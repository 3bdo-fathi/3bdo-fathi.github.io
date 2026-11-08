import os
import pypdf # or fitz if available, let's test pypdf / pypdf2 / pdfplumber or fitz

paths = [
    r"d:\Download\tele\Mobile Penetration Testing Guide.pdf",
    r"d:\Download\tele\Android Penetration Testing -1.pdf",
    r"d:\Download\tele\Android Mobile App Pentesting.pdf"
]

for p in paths:
    print("Checking:", p)
    print("Exists:", os.path.exists(p))
    if os.path.exists(p):
        print("Size in bytes:", os.path.getsize(p))

