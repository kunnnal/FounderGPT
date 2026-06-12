"""Risk agent for surfacing the most likely failure modes."""

from __future__ import annotations

from app.agents.common import make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.utils.heuristics import clamp, financial_pressure, has_sensitive_data_risk, specificity_score


def run_risk_agent(
    request: WarRoomRequest,
    knowledge_base: LocalKnowledgeBaseClient,
) -> object:
    pressure = financial_pressure(request)
    market_blur = 100 - specificity_score(request.target_customer)
    score = clamp(
        78 - pressure * 0.25 - market_blur * 0.18 - (10 if has_sensitive_data_risk(request) else 0),
        25,
        88,
    )
    summary = (
        "The core failure risk is not technical novelty. It is whether the team can prove one painful use case "
        "fast enough before market ambiguity or runway pressure compounds."
    )
    strengths = [
        "The problem statement is real enough to create visible downside if ignored.",
        "The team is small, which makes it easier to correct course quickly.",
        "Risk is detectable early because the product affects measurable activation workflows.",
    ]
    concerns = [
        "The idea can drift into a broad AI assistant category if the wedge is not defended.",
        "Runway pressure will increase sharply if pilots take too long to close.",
        "Sensitive workflow or customer data raises downstream trust requirements."
        if has_sensitive_data_risk(request)
        else "Competitive pressure will rise once onboarding ROI is proven in-market.",
    ]
    next_steps = [
        "Rank risks by probability and by how quickly they can be disproven.",
        "Use the next month to kill the highest-uncertainty assumption first.",
        "Create a simple red-flag dashboard for runway, pilot conversion, and product activation.",
    ]
    citations = knowledge_base.retrieve(
        f"startup failure patterns ai product risks risk {request.problem} {request.solution}",
    )
    return make_finding(
        agent="risk",
        focus_area="Failure modes",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=citations,
    )

