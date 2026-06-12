"""Market agent for ICP and demand evaluation."""

from __future__ import annotations

from app.agents.common import make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.utils.heuristics import clamp, specificity_score, traction_bonus


def run_market_agent(
    request: WarRoomRequest,
    knowledge_base: LocalKnowledgeBaseClient,
) -> object:
    score = clamp(
        28
        + specificity_score(request.target_customer) * 0.35
        + specificity_score(request.problem) * 0.25
        + traction_bonus(request),
        25,
        92,
    )
    summary = (
        "The market case is strongest when the team narrows the buyer, user, and measurable activation "
        "problem into one repeatable segment."
    )
    strengths = [
        f"The ICP is described as {request.target_customer}.",
        "The problem statement points to retention or workflow pain rather than vague productivity gains.",
        "Early traction is present." if request.traction_summary else "The market narrative is coherent even before traction is fully proven.",
    ]
    concerns = [
        "The pitch still needs more evidence that the problem is frequent enough to trigger budget.",
        "If the customer segment is too broad, interviews will create noisy signals and slow positioning.",
    ]
    next_steps = [
        "Name the first narrow sub-segment that can buy fastest.",
        "Collect five explicit willingness-to-pay signals before expanding the feature set.",
        "Track a before-and-after metric tied to the problem, not just user sentiment.",
    ]
    citations = knowledge_base.retrieve(
        f"idea validation first 100 customers pricing strategy {request.target_customer} {request.problem}",
    )
    return make_finding(
        agent="market",
        focus_area="ICP and demand",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=citations,
    )

