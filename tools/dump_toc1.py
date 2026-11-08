from pypdf import PdfReader

reader = PdfReader(r"d:\Download\tele\Mobile Penetration Testing Guide.pdf")
print("=== FULL OUTLINE of Mobile Penetration Testing Guide ===")

def dump_outline(items, level=0):
    for item in items:
        if isinstance(item, list):
            dump_outline(item, level + 1)
        else:
            title = getattr(item, 'title', str(item))
            page_num = ""
            try:
                page_num = reader.get_destination_page_number(item) + 1
            except Exception:
                pass
            print(f"{'  ' * level}- {title} (page {page_num})")

try:
    dump_outline(reader.outline)
except Exception as e:
    print("Error:", e)

