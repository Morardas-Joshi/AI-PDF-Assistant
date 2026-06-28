from pathlib import Path

import pytest

from backend.app.services.exceptions import DocumentProcessingError
from backend.app.services.pdf_text_extractor import PDFTextExtractor


def test_pdf_text_extractor_reads_sample_pdf():
    sample_path = Path("docs/samples/frontend.pdf")
    extractor = PDFTextExtractor(allowed_root=sample_path.parent)

    document = extractor.extract(sample_path)

    assert document.file_name == "frontend.pdf"
    assert document.total_pages == 3
    assert document.total_characters > 500
    assert document.pages[0].page_number == 1
    assert "Cafe POS" in document.pages[0].text


def test_pdf_text_extractor_rejects_paths_outside_allowed_root(tmp_path):
    sample_path = Path("docs/samples/frontend.pdf")
    extractor = PDFTextExtractor(allowed_root=tmp_path)

    with pytest.raises(DocumentProcessingError, match="outside the allowed directory"):
        extractor.extract(sample_path)


def test_pdf_text_extractor_rejects_non_pdf_file(tmp_path):
    text_file = tmp_path / "notes.txt"
    text_file.write_text("not a pdf", encoding="utf-8")
    extractor = PDFTextExtractor(allowed_root=tmp_path)

    with pytest.raises(DocumentProcessingError, match="Only PDF files"):
        extractor.extract(text_file)

