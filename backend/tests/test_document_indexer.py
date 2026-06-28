from pathlib import Path

from backend.app.repositories.vector_store import ChromaVectorRepository
from backend.app.services.document_indexer import DocumentIndexingService
from backend.app.services.pdf_text_extractor import PDFTextExtractor
from backend.app.services.text_chunker import TextChunker
from backend.tests.fakes import DeterministicEmbeddings


def test_document_indexing_service_indexes_pdf_chunks(tmp_path):
    sample_pdf = Path("docs/samples/frontend.pdf")
    repository = ChromaVectorRepository(
        persist_directory=tmp_path / "chroma",
        embedding_function=DeterministicEmbeddings(),
        collection_name="indexing_service",
    )
    service = DocumentIndexingService(
        extractor=PDFTextExtractor(allowed_root=sample_pdf.parent),
        chunker=TextChunker(chunk_size=300, chunk_overlap=50),
        vector_repository=repository,
    )

    result = service.index_pdf(sample_pdf)

    assert result.file_name == "frontend.pdf"
    assert result.total_pages == 3
    assert result.total_chunks > 0
    assert result.stored_chunks == result.total_chunks
    assert repository.count() == result.total_chunks

