"""Internal pipeline state for the FounderGPT demo."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.requests import WarRoomRequest
from app.schemas.responses import AgentFinding, Citation


class WarRoomState(BaseModel):
    request: WarRoomRequest
    routing: list[str] = Field(default_factory=list)
    knowledge_hits: dict[str, list[Citation]] = Field(default_factory=dict)
    agent_findings: list[AgentFinding] = Field(default_factory=list)

