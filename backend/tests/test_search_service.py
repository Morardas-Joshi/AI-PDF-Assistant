from backend.app.schemas.chunk import ChunkSearchResult
from backend.app.services.search_service import SemanticSearchService


class StaticSearchRepository:
    def similarity_search(self, query: str, *, limit: int = 5) -> list[ChunkSearchResult]:
        return [
            ChunkSearchResult(
                id="sample.pdf:page-1:chunk-0",
                document_name="sample.pdf",
                page_number=1,
                chunk_index=0,
                text=f"Result for {query}",
                score=0.1,
            )
        ][:limit]


def test_semantic_search_service_normalizes_query():
    service = SemanticSearchService(repository=StaticSearchRepository())

    response = service.search(query="  invoice total  ", limit=1)

    assert response.query == "invoice total"
    assert len(response.results) == 1
    assert response.results[0].document_name == "sample.pdf"


def test_semantic_search_service_returns_empty_results_for_blank_query():
    service = SemanticSearchService(repository=StaticSearchRepository())

    response = service.search(query="   ", limit=1)

    assert response.query == ""
    assert response.results == []

