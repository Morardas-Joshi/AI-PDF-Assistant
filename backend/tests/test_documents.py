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
async def test_list_documents_returns_uploaded_pdfs(tmp_path):
    app = create_app(_settings(tmp_path))
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True)
    stored_pdf = upload_dir / "abc123-report.pdf"
    stored_pdf.write_bytes(b"%PDF-1.7\ncontent")
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/documents")

    assert response.status_code == 200
    payload = response.json()
    assert payload["documents"][0]["stored_filename"] == "abc123-report.pdf"
    assert payload["documents"][0]["size_bytes"] == len(b"%PDF-1.7\ncontent")


@pytest.mark.anyio
async def test_delete_document_removes_uploaded_pdf(tmp_path):
    app = create_app(_settings(tmp_path))
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True)
    stored_pdf = upload_dir / "abc123-report.pdf"
    stored_pdf.write_bytes(b"%PDF-1.7\ncontent")
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/api/v1/documents/abc123-report.pdf")

    assert response.status_code == 200
    assert response.json() == {"stored_filename": "abc123-report.pdf", "deleted": True}
    assert not stored_pdf.exists()


@pytest.mark.anyio
async def test_delete_document_rejects_path_traversal(tmp_path):
    app = create_app(_settings(tmp_path))
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/api/v1/documents/..%2Fsecret.pdf")

    assert response.status_code == 404


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
