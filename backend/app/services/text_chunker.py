from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.app.schemas.chunk import ChunkedDocument, TextChunk
from backend.app.schemas.pdf import ExtractedPDFDocument


class TextChunker:
    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def chunk_document(self, document: ExtractedPDFDocument) -> ChunkedDocument:
        chunks: list[TextChunk] = []

        for page in document.pages:
            page_chunks = self.splitter.split_text(page.text)
            for page_chunk_index, text in enumerate(page_chunks):
                clean_text = text.strip()
                if not clean_text:
                    continue

                chunks.append(
                    TextChunk(
                        id=self._build_chunk_id(
                            document_name=document.file_name,
                            page_number=page.page_number,
                            chunk_index=page_chunk_index,
                        ),
                        document_name=document.file_name,
                        page_number=page.page_number,
                        chunk_index=page_chunk_index,
                        text=clean_text,
                        character_count=len(clean_text),
                    )
                )

        return ChunkedDocument(
            document_name=document.file_name,
            total_chunks=len(chunks),
            chunks=chunks,
        )

    def _build_chunk_id(self, *, document_name: str, page_number: int, chunk_index: int) -> str:
        return f"{document_name}:page-{page_number}:chunk-{chunk_index}"

