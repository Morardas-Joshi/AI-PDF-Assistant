from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from backend.app.schemas.chunk import ChunkSearchResult, TextChunk


class ChromaVectorRepository:
    def __init__(
        self,
        *,
        persist_directory: Path,
        embedding_function: Embeddings,
        collection_name: str = "pdf_chunks",
    ) -> None:
        self.persist_directory = persist_directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_function,
            persist_directory=str(self.persist_directory),
        )

    def upsert_chunks(self, chunks: list[TextChunk]) -> int:
        if not chunks:
            return 0

        documents = [
            Document(
                page_content=chunk.text,
                metadata={
                    "id": chunk.id,
                    "document_name": chunk.document_name,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    "character_count": chunk.character_count,
                },
            )
            for chunk in chunks
        ]

        self.vector_store.add_documents(
            documents=documents,
            ids=[chunk.id for chunk in chunks],
        )
        return len(chunks)

    def similarity_search(self, query: str, *, limit: int = 5) -> list[ChunkSearchResult]:
        if not query.strip():
            return []

        results = self.vector_store.similarity_search_with_score(query=query, k=limit)
        return [
            ChunkSearchResult(
                id=str(document.metadata["id"]),
                document_name=str(document.metadata["document_name"]),
                page_number=int(document.metadata["page_number"]),
                chunk_index=int(document.metadata["chunk_index"]),
                text=document.page_content,
                score=float(score),
            )
            for document, score in results
        ]

    def count(self) -> int:
        return self.vector_store._collection.count()

