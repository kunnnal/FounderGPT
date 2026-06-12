"""Planner agent for structuring the founder's next milestones."""

from __future__ import annotations

from app.agents.common import make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.utils.heuristics import clamp, specificity_score, stage_weight, traction_bonus


def run_planner_agent(
    request: WarRoomRequest,
    knowledge_base: LocalKnowledgeBaseClient,
) -> object:
    score = clamp(
        (
            specificity_score(request.problem)
            + specificity_score(request.solution)
            + specificity_score(request.target_customer)
        )
        / 3
        + stage_weight(request.stage) * 0.25
        + traction_bonus(request) * 0.4,
        35,
        92,
    )
    summary = (
        f"{request.startup_name} has a clear enough wedge to run a staged plan, but the next "
        "milestone should stay tightly focused on demand proof and onboarding proof points."
    )
    strengths = [
        f"The pitch names a concrete customer set: {request.target_customer}.",
        f"The stage is explicit at {request.stage}, which helps keep execution scoped.",
        "The problem and solution can be translated into testable assumptions.",
    ]
    concerns = [
        "The riskiest assumption still looks like whether the target user will adopt the workflow consistently."
        if not request.traction_summary
        else "The early traction needs to be converted into repeatable proof, not just anecdotal wins.",
        "A broad roadmap would dilute learning in the next 30 days.",
    ]
    next_steps = [
        "Run 10 focused founder-led interviews with the exact ICP named in the pitch.",
        "Define one activation metric that proves the product reaches first value quickly.",
        "Limit the MVP to the top one or two onboarding moments that directly affect retention.",
    ]
    citations = knowledge_base.retrieve(
        f"idea validation mvp design {request.problem} {request.solution}",
    )
    return make_finding(
        agent="planner",
        focus_area="Execution plan",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=citations,
    )

