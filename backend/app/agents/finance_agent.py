"""Finance agent for runway and business-model pressure."""

from __future__ import annotations

from app.agents.common import format_currency, make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.utils.heuristics import clamp, financial_pressure


def run_finance_agent(
    request: WarRoomRequest,
    knowledge_base: LocalKnowledgeBaseClient,
) -> object:
    pressure = financial_pressure(request)
    score = clamp(
        82
        - pressure * 0.6
        + min(request.runway_months * 1.8, 18)
        + (10 if request.monthly_revenue > 0 else 0),
        20,
        92,
    )
    summary = (
        f"The company is carrying {format_currency(request.monthly_burn)} of monthly burn against "
        f"{format_currency(request.monthly_revenue)} in monthly revenue, so capital discipline is part of the product strategy."
    )
    strengths = [
        f"Declared runway is {request.runway_months} months, which gives a visible planning horizon.",
        "Revenue already exists." if request.monthly_revenue > 0 else "The model is still pre-revenue, which is normal but should be treated as a constraint.",
        "The business model can support recurring revenue if the product truly improves activation.",
    ]
    concerns = [
        "Burn should stay tightly aligned to proof milestones rather than feature ambition.",
        "If pilots do not convert quickly, the team may need to extend runway by cutting scope before raising capital.",
    ]
    next_steps = [
        "Track gross margin and payback assumptions even before they are perfect.",
        "Set a hard runway checkpoint tied to pilot conversion and retention proof.",
        "Model what happens if fundraising takes six months longer than expected.",
    ]
    citations = knowledge_base.retrieve(
        f"unit economics runway planning investor readiness burn revenue {request.business_model}",
    )
    return make_finding(
        agent="finance",
        focus_area="Runway and unit economics",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=citations,
    )

