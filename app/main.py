from pypdf import PdfReader

pdf_path = "uploads/frontend.pdf"

reader = PdfReader(pdf_path)

print(f"Total Pages: {len(reader.pages)}")

first_page = reader.pages[0]

text = first_page.extract_text()

print("\nFirst Page:\n")

print(text)