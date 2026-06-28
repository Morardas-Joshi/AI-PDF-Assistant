from pydantic import BaseModel


class HealthResponse(BaseModel):
    app_name: str
    version: str
    environment: str
    status: str
    upload_dir: str
    chroma_dir: str

