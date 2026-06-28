from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    id: str
    original_filename: str
    stored_filename: str
    content_type: str
    size_bytes: int = Field(ge=0)
    uploaded_at: datetime


class DocumentUploadResult(BaseModel):
    documents: list[DocumentUploadResponse]


def build_document_response(
    *,
    document_id: str,
    original_filename: str,
    stored_path: Path,
    content_type: str,
    size_bytes: int,
) -> DocumentUploadResponse:
    return DocumentUploadResponse(
        id=document_id,
        original_filename=original_filename,
        stored_filename=stored_path.name,
        content_type=content_type,
        size_bytes=size_bytes,
        uploaded_at=datetime.now(timezone.utc),
    )

