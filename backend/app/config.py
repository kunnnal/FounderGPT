"""Application configuration for the local hackathon demo."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "backend" / ".env")


def _parse_origins(raw_value: str | None) -> list[str]:
    if not raw_value:
        return ["http://localhost:3000", "http://127.0.0.1:3000"]
    return [origin.strip() for origin in raw_value.split(",") if origin.strip()]


class Settings(BaseModel):
    app_name: str = "FounderGPT API"
    app_version: str = "0.1.0"
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    allowed_origins: list[str] = Field(
        default_factory=lambda: _parse_origins(os.getenv("ALLOWED_ORIGINS")),
    )
    azure_ai_project_endpoint: str = os.getenv("AZURE_AI_PROJECT_ENDPOINT", "")
    azure_ai_model_deployment: str = os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "")
    foundry_iq_endpoint: str = os.getenv("FOUNDRY_IQ_ENDPOINT", "")
    database_url: str = os.getenv("DATABASE_URL", "")
    knowledge_base_dir: Path = PROJECT_ROOT / "knowledge_base"
    data_dir: Path = PROJECT_ROOT / "data"


settings = Settings()

