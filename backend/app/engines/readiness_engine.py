"""Readiness scoring engine for the local demo."""

from __future__ import annotations

from app.schemas.requests import WarRoomRequest
from app.schemas.responses import ScoreCard
from app.utils.heuristics import clamp, founder_strength, specificity_score, stage_weight, traction_bonus


def calculate_readiness_score(request: WarRoomRequest) -> ScoreCard:
    market = clamp(
        24
        + specificity_score(request.target_customer) * 0.35
        + specificity_score(request.problem) * 0.25
        + traction_bonus(request),
        20,
        95,
    )
    product = clamp(
        26
        + specificity_score(request.solution) * 0.35
        + request.founder.technical_strength * 3
        + stage_weight(request.stage) * 0.15,
        20,
        95,
    )
    execution = clamp(
        24
        + founder_strength(request) * 0.45
        + min(request.team_size * 4, 20)
        + stage_weight(request.stage) * 0.15,
        20,
        95,
    )
    financial = clamp(
        22
        + min(request.runway_months * 2.5, 24)
        + (16 if request.monthly_revenue > 0 else 0)
        - min(request.monthly_burn / 1500, 18),
        20,
        95,
    )
    defensibility = clamp(
        18
        + specificity_score(request.founder.domain_expertise) * 0.3
        + specificity_score(request.market_context) * 0.2
        + (10 if request.monthly_revenue > 0 else 0),
        20,
        92,
    )
    overall = clamp(
        market * 0.25
        + product * 0.22
        + execution * 0.22
        + financial * 0.16
        + defensibility * 0.15,
        20,
        95,
    )
    if overall >= 80:
        readiness_stage = "Pilot and fundraising prep"
    elif overall >= 68:
        readiness_stage = "Focused MVP"
    elif overall >= 55:
        readiness_stage = "Customer validation"
    else:
        readiness_stage = "Discovery"
    return ScoreCard(
        market=market,
        product=product,
        execution=execution,
        financial=financial,
        defensibility=defensibility,
        overall=overall,
        readiness_stage=readiness_stage,
    )

