import httpx
import pytest

from backend.app.api.routes.chat import get_rag_chat_service
from backend.app.config.settings import Settings
from backend.app.main import create_app
from backend.app.schemas.chunk import ChunkSearchResult
from backend.app.services.rag_chat_service import RAGChatService
from backend.tests.test_rag_chat_service import FakeChatModel, StaticRetrievalRepository


@pytest.mark.anyio
async def test_chat_api_returns_grounded_answer(tmp_path):
    settings = Settings(
        environment="test",
        upload_dir_name=str(tmp_path / "uploads"),
        chroma_dir_name=str(tmp_path / "chroma"),
    )
    app = create_app(settings)
    chunk = ChunkSearchResult(
        id="guide.pdf:page-3:chunk-1",
        document_name="guide.pdf",
        page_number=3,
        chunk_index=1,
        text="Use the payment screen to review totals.",
        score=0.2,
    )

    async def override_rag_service() -> RAGChatService:
        return RAGChatService(
            repository=StaticRetrievalRepository([chunk]),
            chat_model=FakeChatModel(),
        )

    app.dependency_overrides[get_rag_chat_service] = override_rag_service
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/chat", json={"question": "How do I review totals?", "limit": 1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["question"] == "How do I review totals?"
    assert payload["citations"][0]["document_name"] == "guide.pdf"


@pytest.mark.anyio
async def test_chat_api_validates_question(tmp_path):
    settings = Settings(
        environment="test",
        upload_dir_name=str(tmp_path / "uploads"),
        chroma_dir_name=str(tmp_path / "chroma"),
    )
    app = create_app(settings)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/chat", json={"question": "", "limit": 1})

    assert response.status_code == 422

