# AI PDF Assistant

A production-oriented AI PDF Assistant built with FastAPI, LangChain, Ollama, ChromaDB, and a modern React frontend.

## Current Status

Module 1 is complete: project structure cleanup with a backend-first architecture, typed configuration, health checks, request tracing, CORS, and tests.

## Architecture

```text
AI-PDF-Assistant/
  backend/
    app/
      api/
        routes/
      config/
      core/
      database/
      middleware/
      models/
      repositories/
      schemas/
      services/
      utils/
    chroma_db/
    tests/
    uploads/
  docker/
  docs/
    samples/
  frontend/
    public/
    src/
  scripts/
```

```mermaid
flowchart LR
  Client[Frontend Client] --> API[FastAPI API]
  API --> Services[Service Layer]
  Services --> VectorStore[ChromaDB]
  Services --> Ollama[Ollama]
  API --> Storage[Uploads]
```

## Backend Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
uvicorn backend.app.main:app --reload
```

Health check:

```bash
curl http://localhost:8000/api/v1/health
```

## Tests

```bash
python -m pytest backend/tests
```

Expected result:

```text
1 passed
```

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `APP_NAME` | Public application name |
| `APP_VERSION` | Application version |
| `ENVIRONMENT` | `development`, `test`, `staging`, or `production` |
| `APP_DEBUG` | Enables debug logging and FastAPI debug mode |
| `BACKEND_CORS_ORIGINS` | Comma-separated frontend origins |
| `UPLOAD_DIR_NAME` | PDF upload storage directory |
| `CHROMA_DIR_NAME` | Local vector database directory |
| `MAX_UPLOAD_SIZE_MB` | Upload size limit |
| `OLLAMA_BASE_URL` | Local Ollama API URL |
| `LLM_MODEL` | Chat model name |
| `EMBEDDING_MODEL` | Embedding model name |

## Roadmap

- PDF text extraction service
- Multi-knowledge-base document model
- ChromaDB repository layer
- RAG chat endpoint with streaming responses
- React SaaS dashboard and chat UI
- Deployment guide and Docker Compose

## API

Upload one or more PDFs:

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "files=@docs/samples/frontend.pdf;type=application/pdf"
```

## Screenshots

Screenshots will be added after the frontend module is implemented.

## Troubleshooting

- If imports fail, run commands from the repository root.
- If Ollama calls fail in later modules, ensure Ollama is running and the configured models are pulled.
