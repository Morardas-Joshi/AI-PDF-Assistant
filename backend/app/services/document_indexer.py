from pathlib import Path
from typing import Protocol

from backend.app.schemas.chunk import TextChunk
from backend.app.schemas.indexing import DocumentIndexResult
from backend.app.services.pdf_text_extractor import PDFTextExtractor
from backend.app.services.text_chunker import TextChunker


class VectorRepository(Protocol):
    def upsert_chunks(self, chunks: list[TextChunk]) -> int:
        raise NotImplementedError


class DocumentIndexingService:
    def __init__(
        self,
        *,
        extractor: PDFTextExtractor,
        chunker: TextChunker,
        vector_repository: VectorRepository,
    ) -> None:
        self.extractor = extractor
        self.chunker = chunker
        self.vector_repository = vector_repository

    def index_pdf(self, file_path: Path) -> DocumentIndexResult:
        extracted_document = self.extractor.extract(file_path)
        chunked_document = self.chunker.chunk_document(extracted_document)
        stored_chunks = self.vector_repository.upsert_chunks(chunked_document.chunks)

        return DocumentIndexResult(
            file_name=extracted_document.file_name,
            total_pages=extracted_document.total_pages,
            total_chunks=chunked_document.total_chunks,
            stored_chunks=stored_chunks,
        )

