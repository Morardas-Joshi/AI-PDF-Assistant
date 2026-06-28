from pydantic import BaseModel, Field

from backend.app.schemas.chunk import ChunkSearchResult


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    limit: int = Field(default=5, ge=1, le=20)


class SearchResponse(BaseModel):
    query: str
    results: list[ChunkSearchResult]

