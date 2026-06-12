"""Critic agent for adversarial pressure testing."""

from __future__ import annotations

from app.agents.common import make_finding
from app.schemas.requests import WarRoomRequest
from app.schemas.responses import AgentFinding, ScoreCard
from app.utils.heuristics import clamp


def run_critic_agent(
    request: WarRoomRequest,
    scorecard: ScoreCard,
    specialist_findings: list[AgentFinding],
) -> object:
    weakest_dimension = min(
        {
            "market": scorecard.market,
            "product": scorecard.product,
            "execution": scorecard.execution,
            "financial": scorecard.financial,
            "defensibility": scorecard.defensibility,
        }.items(),
        key=lambda item: item[1],
    )
    borrowed_concerns = [
        concern
        for finding in specialist_findings
        for concern in finding.concerns[:1]
    ][:3]
    score = clamp(scorecard.overall - 6, 30, 88)
    summary = (
        f"The hardest objection is still in {weakest_dimension[0]}. If that area does not improve soon, "
        "the rest of the strategy becomes narrative rather than evidence."
    )
    strengths = [
        "The concept is coherent enough that the weak spots are diagnosable.",
        "Several risks can be tested cheaply in customer conversations and pilot design.",
    ]
    concerns = borrowed_concerns or [
        "The case is still too assumption-heavy to justify aggressive scaling."
    ]
    next_steps = [
        "Treat the weakest score dimension as the single operating priority for the next sprint.",
        "Write down the kill criteria for the next experiment before running it.",
        f"Do not expand the roadmap until {weakest_dimension[0]} improves materially.",
    ]
    return make_finding(
        agent="critic",
        focus_area="Adversarial review",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=[],
    )

