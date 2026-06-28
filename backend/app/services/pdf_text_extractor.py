from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from backend.app.schemas.pdf import ExtractedPDFDocument, ExtractedPDFPage
from backend.app.services.exceptions import DocumentProcessingError


class PDFTextExtractor:
    def __init__(self, allowed_root: Path) -> None:
        self.allowed_root = allowed_root

    def extract(self, file_path: Path) -> ExtractedPDFDocument:
        resolved_path = self._validate_path(file_path)

        try:
            reader = PdfReader(str(resolved_path))
        except (PdfReadError, OSError) as exc:
            raise DocumentProcessingError("PDF could not be read.") from exc

        pages: list[ExtractedPDFPage] = []
        for index, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            pages.append(
                ExtractedPDFPage(
                    page_number=index,
                    text=text,
                    character_count=len(text),
                )
            )

        return ExtractedPDFDocument(
            file_name=resolved_path.name,
            total_pages=len(pages),
            total_characters=sum(page.character_count for page in pages),
            pages=pages,
        )

    def _validate_path(self, file_path: Path) -> Path:
        resolved_root = self.allowed_root.resolve()
        resolved_path = file_path.resolve()

        if resolved_root != resolved_path and resolved_root not in resolved_path.parents:
            raise DocumentProcessingError("PDF path is outside the allowed directory.")

        if not resolved_path.exists():
            raise DocumentProcessingError("PDF file does not exist.")

        if not resolved_path.is_file():
            raise DocumentProcessingError("PDF path must point to a file.")

        if resolved_path.suffix.lower() != ".pdf":
            raise DocumentProcessingError("Only PDF files can be extracted.")

        return resolved_path

