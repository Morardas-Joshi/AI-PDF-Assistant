import httpx
import pytest

from backend.app.api.routes.search import get_semantic_search_service
from backend.app.config.settings import Settings
from backend.app.main import create_app
from backend.app.schemas.chunk import ChunkSearchResult
from backend.app.services.search_service import SemanticSearchService


class StaticSearchRepository:
    def similarity_search(self, query: str, *, limit: int = 5) -> list[ChunkSearchResult]:
        return [
            ChunkSearchResult(
                id="sample.pdf:page-2:chunk-0",
                document_name="sample.pdf",
                page_number=2,
                chunk_index=0,
                text="Payment terminal setup.",
                score=0.2,
            )
        ][:limit]


@pytest.mark.anyio
async def test_semantic_search_api_returns_cited_chunks(tmp_path):
    settings = Settings(
        environment="test",
        upload_dir_name=str(tmp_path / "uploads"),
        chroma_dir_name=str(tmp_path / "chroma"),
    )
    app = create_app(settings)

    async def override_search_service() -> SemanticSearchService:
        return SemanticSearchService(repository=StaticSearchRepository())

    app.dependency_overrides[get_semantic_search_service] = override_search_service
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/search", json={"query": " payment ", "limit": 1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["query"] == "payment"
    assert payload["results"][0]["document_name"] == "sample.pdf"
    assert payload["results"][0]["page_number"] == 2


@pytest.mark.anyio
async def test_semantic_search_api_validates_query(tmp_path):
    settings = Settings(
        environment="test",
        upload_dir_name=str(tmp_path / "uploads"),
        chroma_dir_name=str(tmp_path / "chroma"),
    )
    app = create_app(settings)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/search", json={"query": "", "limit": 1})

    assert response.status_code == 422

