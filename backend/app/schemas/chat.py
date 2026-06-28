from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    limit: int = Field(default=5, ge=1, le=20)


class ChatCitation(BaseModel):
    id: str
    document_name: str
    page_number: int = Field(ge=1)
    chunk_index: int = Field(ge=0)
    text: str
    score: float | None = None


class ChatResponse(BaseModel):
    question: str
    answer: str
    citations: list[ChatCitation]


class ChatStreamEvent(BaseModel):
    event: str
    data: dict
