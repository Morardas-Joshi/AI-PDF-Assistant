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

# Remove extra spaces at the beginning and end
all_text = all_text.strip()

# Split text into chunks of 500 characters
chunk_size = 500

chunks = []

for i in range(0, len(all_text), chunk_size):
    chunk = all_text[i:i + chunk_size]
    chunks.append(chunk)

print(f"\nTotal Chunks: {len(chunks)}\n")

for index, chunk in enumerate(chunks, start=1):
    print(f"\n========== CHUNK {index} ==========\n")
    print(chunk)

