from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status

from backend.app.config.settings import Settings, get_settings
from backend.app.schemas.document import DocumentUploadResult
from backend.app.services.file_storage import PDFStorageService

router = APIRouter(prefix="/documents", tags=["Documents"])


async def get_pdf_storage_service(settings: Annotated[Settings, Depends(get_settings)]) -> PDFStorageService:
    return PDFStorageService(settings)


@router.post(
    "/upload",
    response_model=DocumentUploadResult,
    status_code=status.HTTP_201_CREATED,
)
async def upload_documents(
    files: Annotated[list[UploadFile], File(description="One or more PDF files.")],
    storage_service: Annotated[PDFStorageService, Depends(get_pdf_storage_service)],
) -> DocumentUploadResult:
    documents = []
    for file in files:
        documents.append(await storage_service.save_upload(file))
    return DocumentUploadResult(documents=documents)
