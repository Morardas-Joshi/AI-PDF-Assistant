from backend.app.schemas.pdf import ExtractedPDFDocument, ExtractedPDFPage
from backend.app.services.text_chunker import TextChunker


def test_text_chunker_creates_page_scoped_chunks():
    document = ExtractedPDFDocument(
        file_name="sample.pdf",
        total_pages=2,
        total_characters=88,
        pages=[
            ExtractedPDFPage(page_number=1, text="Alpha beta gamma delta epsilon zeta eta theta.", character_count=46),
            ExtractedPDFPage(page_number=2, text="One two three four five six seven eight.", character_count=42),
        ],
    )
    chunker = TextChunker(chunk_size=24, chunk_overlap=6)

    result = chunker.chunk_document(document)

    assert result.document_name == "sample.pdf"
    assert result.total_chunks >= 4
    assert {chunk.page_number for chunk in result.chunks} == {1, 2}
    assert result.chunks[0].id == "sample.pdf:page-1:chunk-0"


def test_text_chunker_skips_empty_pages():
    document = ExtractedPDFDocument(
        file_name="empty-page.pdf",
        total_pages=1,
        total_characters=0,
        pages=[ExtractedPDFPage(page_number=1, text="", character_count=0)],
    )
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)

    result = chunker.chunk_document(document)

    assert result.total_chunks == 0
    assert result.chunks == []


def test_text_chunker_rejects_invalid_overlap():
    try:
        TextChunker(chunk_size=100, chunk_overlap=100)
    except ValueError as exc:
        assert "chunk_overlap" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid chunk overlap.")

