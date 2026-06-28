from fastapi import APIRouter, Depends

from backend.app.config.settings import Settings, get_settings
from backend.app.schemas.health import HealthResponse

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        status="ok",
        upload_dir=str(settings.upload_dir),
        chroma_dir=str(settings.chroma_dir),
    )
