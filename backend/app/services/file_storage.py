import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from backend.app.config.settings import Settings
from backend.app.schemas.document import DocumentUploadResponse, StoredDocument, build_document_response

PDF_CONTENT_TYPES = {"application/pdf", "application/x-pdf"}
PDF_EXTENSION = ".pdf"
SAFE_FILENAME_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


class PDFStorageService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def save_upload(self, upload: UploadFile) -> DocumentUploadResponse:
        original_filename = self._validate_filename(upload.filename)
        self._validate_content_type(upload.content_type)

        payload = await upload.read()
        size_bytes = len(payload)
        self._validate_size(size_bytes)
        self._validate_pdf_signature(payload)

        document_id = str(uuid4())
        stored_filename = f"{document_id}-{self._sanitize_filename(original_filename)}"
        stored_path = self.settings.upload_dir / stored_filename
        self._ensure_safe_storage_path(stored_path)

        self.settings.upload_dir.mkdir(parents=True, exist_ok=True)
        stored_path.write_bytes(payload)

        return build_document_response(
            document_id=document_id,
            original_filename=original_filename,
            stored_path=stored_path,
            content_type=upload.content_type or "application/pdf",
            size_bytes=size_bytes,
        )

    def list_documents(self) -> list[StoredDocument]:
        self.settings.upload_dir.mkdir(parents=True, exist_ok=True)
        documents = []

        for path in sorted(self.settings.upload_dir.glob("*.pdf")):
            if not path.is_file():
                continue

            stat = path.stat()
            documents.append(
                StoredDocument(
                    stored_filename=path.name,
                    size_bytes=stat.st_size,
                    modified_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                )
            )

        return documents

    def delete_document(self, stored_filename: str) -> bool:
        path = self._resolve_stored_pdf(stored_filename)
        if not path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document was not found.",
            )

        path.unlink()
        return True

    def _validate_filename(self, filename: str | None) -> str:
        if not filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A filename is required.",
            )

        name = Path(filename).name
        if Path(name).suffix.lower() != PDF_EXTENSION:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only PDF files are supported.",
            )
        return name

    def _validate_content_type(self, content_type: str | None) -> None:
        if content_type not in PDF_CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Upload must be a PDF file.",
            )

    def _validate_size(self, size_bytes: int) -> None:
        if size_bytes == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded PDF is empty.",
            )

        if size_bytes > self.settings.max_upload_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"PDF exceeds the {self.settings.max_upload_size_mb} MB upload limit.",
            )

    def _validate_pdf_signature(self, payload: bytes) -> None:
        if not payload.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Uploaded file is not a valid PDF.",
            )

    def _sanitize_filename(self, filename: str) -> str:
        sanitized = SAFE_FILENAME_PATTERN.sub("-", Path(filename).name).strip(".-")
        return sanitized or "document.pdf"

    def _ensure_safe_storage_path(self, stored_path: Path) -> None:
        upload_dir = self.settings.upload_dir.resolve()
        target = stored_path.resolve()
        if upload_dir not in target.parents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid upload path.",
            )

    def _resolve_stored_pdf(self, stored_filename: str) -> Path:
        if stored_filename != Path(stored_filename).name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid document filename.",
            )

        if Path(stored_filename).suffix.lower() != PDF_EXTENSION:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only PDF files are supported.",
            )

        path = self.settings.upload_dir / stored_filename
        self._ensure_safe_storage_path(path)
        return path
