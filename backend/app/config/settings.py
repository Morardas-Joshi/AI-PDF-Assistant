from functools import lru_cache
from pathlib import Path

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.requests import Request


class Settings(BaseSettings):
    app_name: str = "AI PDF Assistant"
    app_version: str = "0.1.0"
    environment: str = Field(default="development", pattern="^(development|test|staging|production)$")
    debug: bool = Field(default=True, validation_alias="APP_DEBUG")
    api_prefix: str = "/api/v1"

    backend_cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )

    upload_dir_name: str = "uploads"
    chroma_dir_name: str = "chroma_db"
    max_upload_size_mb: int = Field(default=25, ge=1, le=250)
    chunk_size: int = Field(default=1000, ge=100, le=8000)
    chunk_overlap: int = Field(default=150, ge=0, le=2000)

    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen3:4b"
    embedding_model: str = "nomic-embed-text"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[3] / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @computed_field
    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[4]

    @computed_field
    @property
    def backend_root(self) -> Path:
        return Path(__file__).resolve().parents[3]

    @computed_field
    @property
    def upload_dir(self) -> Path:
        return self.backend_root / self.upload_dir_name

    @computed_field
    @property
    def chroma_dir(self) -> Path:
        return self.backend_root / self.chroma_dir_name

    @computed_field
    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_cached_settings() -> Settings:
    return Settings()


async def get_settings(request: Request) -> Settings:
    return request.app.state.settings
