from pypdf import PdfReader

pdf_path = "uploads/frontend.pdf"

reader = PdfReader(pdf_path)

print(f"Total Pages: {len(reader.pages)}")

all_text = ""

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text()

    print(f"\n========== PAGE {page_number} ==========\n")

    print(text)

    all_text += text + "\n"

print("\n========== COMPLETE TEXT ==========\n")

print(all_text)