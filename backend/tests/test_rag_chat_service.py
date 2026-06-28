from backend.app.schemas.chunk import ChunkSearchResult
from backend.app.services.rag_chat_service import RAGChatService


class StaticRetrievalRepository:
    def __init__(self, results: list[ChunkSearchResult]) -> None:
        self.results = results

    def similarity_search(self, query: str, *, limit: int = 5) -> list[ChunkSearchResult]:
        return self.results[:limit]


class FakeChatModel:
    def __init__(self) -> None:
        self.prompt = ""

    def generate(self, prompt: str) -> str:
        self.prompt = prompt
        return "The payment total appears in the invoice context."

    def stream(self, prompt: str):
        self.prompt = prompt
        yield "The payment "
        yield "total appears."


def test_rag_chat_service_answers_with_citations():
    chunk = ChunkSearchResult(
        id="invoice.pdf:page-1:chunk-0",
        document_name="invoice.pdf",
        page_number=1,
        chunk_index=0,
        text="The invoice payment total is $42.",
        score=0.12,
    )
    chat_model = FakeChatModel()
    service = RAGChatService(
        repository=StaticRetrievalRepository([chunk]),
        chat_model=chat_model,
    )

    response = service.answer(question=" What is the payment total? ", limit=1)

    assert response.question == "What is the payment total?"
    assert response.answer == "The payment total appears in the invoice context."
    assert response.citations[0].document_name == "invoice.pdf"
    assert "invoice payment total" in chat_model.prompt


def test_rag_chat_service_handles_no_context_without_calling_model():
    chat_model = FakeChatModel()
    service = RAGChatService(
        repository=StaticRetrievalRepository([]),
        chat_model=chat_model,
    )

    response = service.answer(question="What is the total?", limit=1)

    assert response.citations == []
    assert "could not find" in response.answer
    assert chat_model.prompt == ""


def test_rag_chat_service_streams_citations_tokens_and_done():
    chunk = ChunkSearchResult(
        id="invoice.pdf:page-1:chunk-0",
        document_name="invoice.pdf",
        page_number=1,
        chunk_index=0,
        text="The invoice payment total is $42.",
        score=0.12,
    )
    chat_model = FakeChatModel()
    service = RAGChatService(
        repository=StaticRetrievalRepository([chunk]),
        chat_model=chat_model,
    )

    events = list(service.stream_answer(question="What is the payment total?", limit=1))

    assert [event.event for event in events] == ["citations", "token", "token", "done"]
    assert events[0].data["citations"][0]["document_name"] == "invoice.pdf"
    assert events[1].data["text"] == "The payment "
    assert "invoice payment total" in chat_model.prompt
