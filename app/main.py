from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_path = "uploads/frontend.pdf"

reader = PdfReader(pdf_path)

print(f"Total Pages: {len(reader.pages)}")

all_text = ""

# Read every page
for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text()

    print(f"\n========== PAGE {page_number} ==========\n")
    print(text)

    all_text += text + "\n"

# Clean text
all_text = all_text.strip()

# Create smart chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_text(all_text)

print(f"\nTotal Chunks: {len(chunks)}")

# Print all chunks
for index, chunk in enumerate(chunks, start=1):
    print(f"\n========== CHUNK {index} ==========\n")
    print(chunk)