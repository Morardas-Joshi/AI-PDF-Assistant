from typing import Protocol

from backend.app.schemas.chat import ChatCitation, ChatResponse, ChatStreamEvent
from backend.app.schemas.chunk import ChunkSearchResult
from backend.app.services.llm import ChatModel


class RetrievalRepository(Protocol):
    def similarity_search(self, query: str, *, limit: int = 5) -> list[ChunkSearchResult]:
        raise NotImplementedError


class RAGChatService:
    def __init__(self, *, repository: RetrievalRepository, chat_model: ChatModel) -> None:
        self.repository = repository
        self.chat_model = chat_model

    def answer(self, *, question: str, limit: int = 5) -> ChatResponse:
        normalized_question = question.strip()
        chunks = self.repository.similarity_search(normalized_question, limit=limit)

        if not chunks:
            return ChatResponse(
                question=normalized_question,
                answer="I could not find relevant information in the indexed PDFs.",
                citations=[],
            )

        prompt = self._build_prompt(question=normalized_question, chunks=chunks)
        answer = self.chat_model.generate(prompt).strip()

        return ChatResponse(
            question=normalized_question,
            answer=answer,
            citations=[
                ChatCitation(
                    id=chunk.id,
                    document_name=chunk.document_name,
                    page_number=chunk.page_number,
                    chunk_index=chunk.chunk_index,
                    text=chunk.text,
                    score=chunk.score,
                )
                for chunk in chunks
            ],
        )

    def stream_answer(self, *, question: str, limit: int = 5):
        normalized_question = question.strip()
        chunks = self.repository.similarity_search(normalized_question, limit=limit)
        citations = [
            ChatCitation(
                id=chunk.id,
                document_name=chunk.document_name,
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                score=chunk.score,
            )
            for chunk in chunks
        ]

        yield ChatStreamEvent(
            event="citations",
            data={
                "question": normalized_question,
                "citations": [citation.model_dump() for citation in citations],
            },
        )

        if not chunks:
            yield ChatStreamEvent(
                event="token",
                data={"text": "I could not find relevant information in the indexed PDFs."},
            )
            yield ChatStreamEvent(event="done", data={})
            return

        prompt = self._build_prompt(question=normalized_question, chunks=chunks)
        for token in self.chat_model.stream(prompt):
            yield ChatStreamEvent(event="token", data={"text": token})

        yield ChatStreamEvent(event="done", data={})

    def _build_prompt(self, *, question: str, chunks: list[ChunkSearchResult]) -> str:
        context = "\n\n".join(
            (
                f"Source {index} "
                f"({chunk.document_name}, page {chunk.page_number}, chunk {chunk.chunk_index}):\n"
                f"{chunk.text}"
            )
            for index, chunk in enumerate(chunks, start=1)
        )

        return f"""You are a careful AI PDF assistant.
Answer the question using only the provided PDF context.
If the context does not contain the answer, say that the indexed PDFs do not provide enough information.
Keep the answer concise and factual.

Context:
{context}

Question:
{question}

Answer:"""
