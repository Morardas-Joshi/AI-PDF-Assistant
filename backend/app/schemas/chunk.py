from pydantic import BaseModel, Field


class TextChunk(BaseModel):
    id: str
    document_name: str
    page_number: int = Field(ge=1)
    chunk_index: int = Field(ge=0)
    text: str = Field(min_length=1)
    character_count: int = Field(ge=1)


class ChunkedDocument(BaseModel):
    document_name: str
    total_chunks: int = Field(ge=0)
    chunks: list[TextChunk]

