import sys

modules = ['pypdf', 'PyPDF2', 'fitz', 'pdfplumber', 'pypdfium2']
for m in modules:
    try:
        __import__(m)
        print(f"Available: {m}")
    except ImportError:
        print(f"Not available: {m}")

