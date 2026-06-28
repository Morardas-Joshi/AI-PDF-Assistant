import httpx
import pytest

from backend.app.config.settings import Settings
from backend.app.main import create_app


@pytest.mark.anyio
async def test_health_check_returns_application_status(tmp_path):
    settings = Settings(
        environment="test",
        upload_dir_name=str(tmp_path / "uploads"),
        chroma_dir_name=str(tmp_path / "chroma_db"),
    )
    transport = httpx.ASGITransport(app=create_app(settings))

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["app_name"] == "AI PDF Assistant"
    assert payload["environment"] == "test"
    assert payload["status"] == "ok"
    assert response.headers["x-request-id"]
