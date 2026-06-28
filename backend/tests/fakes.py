from langchain_core.embeddings import Embeddings

from backend.app.schemas.chunk import TextChunk


class DeterministicEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        lowered = text.lower()
        return [
            float(lowered.count("invoice")),
            float(lowered.count("menu")),
            float(lowered.count("payment")),
        ]


class InMemoryVectorRepository:
    def __init__(self) -> None:
        self.chunks: list[TextChunk] = []

    def upsert_chunks(self, chunks: list[TextChunk]) -> int:
        self.chunks.extend(chunks)
        return len(chunks)
