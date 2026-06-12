"""Founder profile agent for evaluating execution fit."""

from __future__ import annotations

from app.agents.common import make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.utils.heuristics import clamp, founder_strength, specificity_score


def run_founder_profile_agent(
    request: WarRoomRequest,
    knowledge_base: LocalKnowledgeBaseClient,
) -> object:
    founder = request.founder
    score = clamp(
        founder_strength(request) * 0.65
        + specificity_score(founder.domain_expertise) * 0.25
        + min(request.team_size * 3, 15),
        30,
        93,
    )
    summary = (
        f"{founder.name} has a credible operator profile for this problem, with strongest signals in "
        f"{founder.domain_expertise} and a {founder.role} lens."
    )
    strengths = [
        f"{founder.years_experience} years of experience lowers basic execution risk.",
        f"Technical strength {founder.technical_strength}/10 and GTM strength {founder.go_to_market_strength}/10 are balanced enough for an early team.",
        f"Team size of {request.team_size} is appropriate for a focused MVP.",
    ]
    concerns = [
        "The team still needs sharper evidence that founder expertise matches a painful, urgent buying process.",
        "If founder-led sales is weak, customer discovery may stall before product quality becomes the bottleneck."
        if founder.go_to_market_strength < 6
        else "The team should document repeatable founder-led sales scripts before delegating GTM.",
    ]
    next_steps = [
        "Turn founder insight into a point of view memo on the exact workflow being fixed.",
        "Track every customer conversation in a simple objection log.",
        "Recruit one advisor or pilot champion from the target segment to speed trust.",
    ]
    citations = knowledge_base.retrieve(
        f"customer discovery investor readiness founder strength {founder.domain_expertise}",
    )
    return make_finding(
        agent="founder_profile",
        focus_area="Founder-market fit",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=citations,
    )

