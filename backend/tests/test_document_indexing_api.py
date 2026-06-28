import httpx
import pytest

from backend.app.api.routes.documents import get_document_indexing_service
from backend.app.config.settings import Settings
from backend.app.main import create_app
from backend.app.services.document_indexer import DocumentIndexingService
from backend.app.services.pdf_text_extractor import PDFTextExtractor
from backend.app.services.text_chunker import TextChunker
from backend.tests.fakes import InMemoryVectorRepository


@pytest.mark.anyio
async def test_index_document_returns_not_found_for_missing_pdf(tmp_path):
    settings = Settings(
        environment="test",
        upload_dir_name=str(tmp_path / "uploads"),
        chroma_dir_name=str(tmp_path / "chroma"),
    )
    app = create_app(settings)

    async def override_indexing_service() -> DocumentIndexingService:
        return DocumentIndexingService(
            extractor=PDFTextExtractor(allowed_root=settings.upload_dir),
            chunker=TextChunker(chunk_size=300, chunk_overlap=50),
            vector_repository=InMemoryVectorRepository(),
        )

    app.dependency_overrides[get_document_indexing_service] = override_indexing_service
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/documents/missing.pdf/index")

    assert response.status_code == 404
