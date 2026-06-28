import httpx
import pytest

from backend.app.config.settings import Settings
from backend.app.main import create_app


def _settings(tmp_path) -> Settings:
    return Settings(
        environment="test",
        upload_dir_name=str(tmp_path / "uploads"),
        chroma_dir_name=str(tmp_path / "chroma_db"),
        max_upload_size_mb=1,
    )


@pytest.mark.anyio
async def test_upload_pdf_stores_file_securely(tmp_path):
    app = create_app(_settings(tmp_path))
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/documents/upload",
            files=[
                (
                    "files",
                    ("../../invoice.pdf", b"%PDF-1.7\ncontent", "application/pdf"),
                )
            ],
        )

    assert response.status_code == 201
    payload = response.json()
    document = payload["documents"][0]
    assert document["original_filename"] == "invoice.pdf"
    assert document["stored_filename"].endswith("-invoice.pdf")
    assert (tmp_path / "uploads" / document["stored_filename"]).exists()


@pytest.mark.anyio
async def test_upload_rejects_non_pdf_content_type(tmp_path):
    app = create_app(_settings(tmp_path))
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/documents/upload",
            files=[("files", ("notes.txt", b"hello", "text/plain"))],
        )

    assert response.status_code == 415


@pytest.mark.anyio
async def test_upload_rejects_invalid_pdf_payload(tmp_path):
    app = create_app(_settings(tmp_path))
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/documents/upload",
            files=[("files", ("fake.pdf", b"not a pdf", "application/pdf"))],
        )

    assert response.status_code == 415

