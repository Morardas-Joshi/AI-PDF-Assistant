from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from langchain_ollama import OllamaEmbeddings

from backend.app.config.settings import Settings, get_settings
from backend.app.repositories.vector_store import ChromaVectorRepository
from backend.app.schemas.document import DocumentUploadResult
from backend.app.schemas.indexing import DocumentIndexResult
from backend.app.services.document_indexer import DocumentIndexingService
from backend.app.services.exceptions import DocumentProcessingError
from backend.app.services.file_storage import PDFStorageService
from backend.app.services.pdf_text_extractor import PDFTextExtractor
from backend.app.services.text_chunker import TextChunker

router = APIRouter(prefix="/documents", tags=["Documents"])


async def get_pdf_storage_service(settings: Annotated[Settings, Depends(get_settings)]) -> PDFStorageService:
    return PDFStorageService(settings)


async def get_document_indexing_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> DocumentIndexingService:
    embeddings = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )
    return DocumentIndexingService(
        extractor=PDFTextExtractor(allowed_root=settings.upload_dir),
        chunker=TextChunker(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        ),
        vector_repository=ChromaVectorRepository(
            persist_directory=settings.chroma_dir,
            embedding_function=embeddings,
        ),
    )


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


@router.post(
    "/{stored_filename}/index",
    response_model=DocumentIndexResult,
)
async def index_document(
    stored_filename: str,
    settings: Annotated[Settings, Depends(get_settings)],
    indexing_service: Annotated[DocumentIndexingService, Depends(get_document_indexing_service)],
) -> DocumentIndexResult:
    if stored_filename != Path(stored_filename).name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document filename.",
        )

    try:
        return indexing_service.index_pdf(settings.upload_dir / stored_filename)
    except DocumentProcessingError as exc:
        if "does not exist" in str(exc):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
