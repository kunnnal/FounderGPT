"""Product agent for MVP scope and delivery risk."""

from __future__ import annotations

from app.agents.common import make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.utils.heuristics import clamp, specificity_score, stage_weight


def run_product_agent(
    request: WarRoomRequest,
    knowledge_base: LocalKnowledgeBaseClient,
) -> object:
    solution_score = specificity_score(request.solution)
    complexity_penalty = 10 if " and " in request.solution.lower() else 0
    score = clamp(
        30
        + solution_score * 0.4
        + request.founder.technical_strength * 2.5
        + stage_weight(request.stage) * 0.2
        - complexity_penalty,
        25,
        94,
    )
    summary = (
        "The product thesis is demoable now, but the MVP must stay pointed at a single moment of user value "
        "instead of becoming a general AI assistant."
    )
    strengths = [
        "The solution maps directly to the stated problem rather than introducing an unrelated workflow.",
        f"Technical founder strength of {request.founder.technical_strength}/10 is adequate for an early build.",
        "The current stage suggests a lightweight MVP is still acceptable."
        if request.stage in {"idea", "validation", "mvp"}
        else "The team can justify product hardening because it is already beyond raw ideation.",
    ]
    concerns = [
        "Feature creep is the fastest way to lose the learning loop in a hackathon MVP.",
        "The product should prove time-to-value before investing in broader automation layers.",
    ]
    next_steps = [
        "Reduce the MVP to one core journey and one outcome metric.",
        "Instrument activation events from day one.",
        "Use pilot feedback to cut steps from onboarding, not to add optional intelligence everywhere.",
    ]
    citations = knowledge_base.retrieve(
        f"mvp design activation onboarding {request.solution} {request.problem}",
    )
    return make_finding(
        agent="product",
        focus_area="MVP scope",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=citations,
    )

