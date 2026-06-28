from pydantic import BaseModel, Field


class DocumentIndexResult(BaseModel):
    file_name: str
    total_pages: int = Field(ge=0)
    total_chunks: int = Field(ge=0)
    stored_chunks: int = Field(ge=0)

