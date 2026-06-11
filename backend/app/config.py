"""Application configuration placeholders."""

from pydantic import BaseModel


class Settings(BaseModel):
    azure_ai_project_endpoint: str = ""
    azure_ai_model_deployment: str = ""
    foundry_iq_endpoint: str = ""
    database_url: str = ""


settings = Settings()

