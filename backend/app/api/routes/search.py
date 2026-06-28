from typing import Annotated

from fastapi import APIRouter, Depends
from langchain_ollama import OllamaEmbeddings

from backend.app.config.settings import Settings, get_settings
from backend.app.repositories.vector_store import ChromaVectorRepository
from backend.app.schemas.search import SearchRequest, SearchResponse
from backend.app.services.search_service import SemanticSearchService

router = APIRouter(prefix="/search", tags=["Search"])


async def get_semantic_search_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> SemanticSearchService:
    embeddings = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )
    return SemanticSearchService(
        repository=ChromaVectorRepository(
            persist_directory=settings.chroma_dir,
            embedding_function=embeddings,
        )
    )


@router.post("", response_model=SearchResponse)
async def semantic_search(
    payload: SearchRequest,
    search_service: Annotated[SemanticSearchService, Depends(get_semantic_search_service)],
) -> SearchResponse:
    return search_service.search(query=payload.query, limit=payload.limit)

