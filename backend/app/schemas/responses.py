"""API response schemas for the FounderGPT demo."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.requests import WarRoomRequest


class Citation(BaseModel):
    source: str
    title: str
    snippet: str


class AgentFinding(BaseModel):
    agent: str
    focus_area: str
    verdict: str
    confidence: int
    summary: str
    strengths: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)


class DebateTurn(BaseModel):
    speaker: str
    counterparty: str
    stance: str
    message: str


class ScoreCard(BaseModel):
    market: int
    product: int
    execution: int
    financial: int
    defensibility: int
    overall: int
    readiness_stage: str


class FailureRisk(BaseModel):
    risk: str
    probability: int
    severity: str
    mitigation: str


class ScenarioResult(BaseModel):
    name: str
    assumption: str
    outcome: str
    impact_score: int


class Recommendation(BaseModel):
    decision: str
    confidence: int
    rationale: str
    milestones: list[str] = Field(default_factory=list)
    investor_readiness: str


class WarRoomResponse(BaseModel):
    session_id: str
    created_at: str
    request: WarRoomRequest
    executive_summary: str
    routing: list[str]
    agent_findings: list[AgentFinding]
    debate: list[DebateTurn]
    scorecard: ScoreCard
    failure_risks: list[FailureRisk]
    scenarios: list[ScenarioResult]
    recommendation: Recommendation
    citations: list[Citation]


class DemoPayload(BaseModel):
    request: WarRoomRequest
    notes: list[str] = Field(default_factory=list)

