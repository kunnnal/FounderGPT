"""API request schemas for the FounderGPT demo."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Stage = Literal["idea", "validation", "mvp", "pilot", "growth"]


class FounderProfileInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    role: str = Field(..., min_length=2, max_length=80)
    years_experience: int = Field(..., ge=0, le=40)
    domain_expertise: str = Field(..., min_length=2, max_length=120)
    previous_startup_exits: int = Field(0, ge=0, le=10)
    technical_strength: int = Field(5, ge=1, le=10)
    go_to_market_strength: int = Field(5, ge=1, le=10)


class WarRoomRequest(BaseModel):
    startup_name: str = Field(..., min_length=2, max_length=120)
    one_line_pitch: str = Field(..., min_length=10, max_length=280)
    problem: str = Field(..., min_length=20, max_length=800)
    solution: str = Field(..., min_length=20, max_length=800)
    target_customer: str = Field(..., min_length=10, max_length=200)
    business_model: str = Field(..., min_length=10, max_length=200)
    market_context: str = Field("", max_length=500)
    stage: Stage = "idea"
    traction_summary: str = Field("", max_length=400)
    monthly_revenue: float = Field(0, ge=0)
    monthly_burn: float = Field(0, ge=0)
    runway_months: int = Field(12, ge=0, le=60)
    team_size: int = Field(1, ge=1, le=200)
    founder: FounderProfileInput

