from typing import Annotated
import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langchain_ollama import OllamaEmbeddings

from backend.app.config.settings import Settings, get_settings
from backend.app.repositories.vector_store import ChromaVectorRepository
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.llm import OllamaChatModel
from backend.app.services.rag_chat_service import RAGChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


async def get_rag_chat_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> RAGChatService:
    embeddings = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )
    repository = ChromaVectorRepository(
        persist_directory=settings.chroma_dir,
        embedding_function=embeddings,
    )
    chat_model = OllamaChatModel(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
    )
    return RAGChatService(repository=repository, chat_model=chat_model)


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    rag_service: Annotated[RAGChatService, Depends(get_rag_chat_service)],
) -> ChatResponse:
    return rag_service.answer(question=payload.question, limit=payload.limit)


@router.post("/stream")
async def stream_chat(
    payload: ChatRequest,
    rag_service: Annotated[RAGChatService, Depends(get_rag_chat_service)],
) -> StreamingResponse:
    async def event_stream():
        for event in rag_service.stream_answer(question=payload.question, limit=payload.limit):
            yield _format_sse(event=event.event, data=event.data)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def _format_sse(*, event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
