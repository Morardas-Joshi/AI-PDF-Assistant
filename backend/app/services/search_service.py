from typing import Protocol

from backend.app.schemas.chunk import ChunkSearchResult
from backend.app.schemas.search import SearchResponse


class SearchRepository(Protocol):
    def similarity_search(self, query: str, *, limit: int = 5) -> list[ChunkSearchResult]:
        raise NotImplementedError


class SemanticSearchService:
    def __init__(self, repository: SearchRepository) -> None:
        self.repository = repository

    def search(self, *, query: str, limit: int = 5) -> SearchResponse:
        normalized_query = query.strip()
        if not normalized_query:
            return SearchResponse(query=normalized_query, results=[])

        return SearchResponse(
            query=normalized_query,
            results=self.repository.similarity_search(normalized_query, limit=limit),
        )

