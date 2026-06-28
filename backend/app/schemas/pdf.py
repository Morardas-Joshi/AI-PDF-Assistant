from pydantic import BaseModel, Field


class ExtractedPDFPage(BaseModel):
    page_number: int = Field(ge=1)
    text: str
    character_count: int = Field(ge=0)


class ExtractedPDFDocument(BaseModel):
    file_name: str
    total_pages: int = Field(ge=0)
    total_characters: int = Field(ge=0)
    pages: list[ExtractedPDFPage]

