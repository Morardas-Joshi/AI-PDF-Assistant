from backend.app.repositories.vector_store import ChromaVectorRepository
from backend.app.schemas.chunk import TextChunk
from backend.tests.fakes import DeterministicEmbeddings


def test_vector_repository_upserts_and_searches_chunks(tmp_path):
    repository = ChromaVectorRepository(
        persist_directory=tmp_path / "chroma",
        embedding_function=DeterministicEmbeddings(),
        collection_name="test_chunks",
    )
    chunks = [
        TextChunk(
            id="sample.pdf:page-1:chunk-0",
            document_name="sample.pdf",
            page_number=1,
            chunk_index=0,
            text="Invoice total and payment information.",
            character_count=38,
        ),
        TextChunk(
            id="sample.pdf:page-2:chunk-0",
            document_name="sample.pdf",
            page_number=2,
            chunk_index=0,
            text="Cafe menu and table layout.",
            character_count=27,
        ),
    ]

    stored_count = repository.upsert_chunks(chunks)
    results = repository.similarity_search("invoice payment", limit=1)

    assert stored_count == 2
    assert repository.count() == 2
    assert len(results) == 1
    assert results[0].id == "sample.pdf:page-1:chunk-0"
    assert results[0].document_name == "sample.pdf"
    assert results[0].page_number == 1


def test_vector_repository_handles_empty_inputs(tmp_path):
    repository = ChromaVectorRepository(
        persist_directory=tmp_path / "chroma",
        embedding_function=DeterministicEmbeddings(),
        collection_name="empty_inputs",
    )

    assert repository.upsert_chunks([]) == 0
    assert repository.similarity_search("   ") == []
