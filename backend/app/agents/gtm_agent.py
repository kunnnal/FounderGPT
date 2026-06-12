"""Go-to-market agent for distribution and pricing logic."""

from __future__ import annotations

from app.agents.common import make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.utils.heuristics import clamp, specificity_score, traction_bonus


def run_gtm_agent(
    request: WarRoomRequest,
    knowledge_base: LocalKnowledgeBaseClient,
) -> object:
    pricing_bonus = 8 if "subscription" in request.business_model.lower() else 3
    score = clamp(
        26
        + request.founder.go_to_market_strength * 3
        + specificity_score(request.target_customer) * 0.2
        + pricing_bonus
        + traction_bonus(request) * 0.6,
        25,
        94,
    )
    summary = (
        "The GTM path is credible if the founder keeps sales founder-led, sells to one segment first, and "
        "uses onboarding ROI as the opening wedge."
    )
    strengths = [
        f"The business model is defined as {request.business_model}.",
        f"GTM strength is {request.founder.go_to_market_strength}/10, which is workable for early outbound and design-partner selling.",
        "The pitch is naturally tied to activation and support-cost outcomes, which are budget-relevant.",
    ]
    concerns = [
        "Without a narrow wedge, GTM messaging will sound like another generic AI efficiency tool.",
        "The team needs a repeatable way to reach the first 10 customers before scaling content or paid channels.",
    ]
    next_steps = [
        "Write a one-paragraph ROI narrative for the buyer.",
        "Build a target list of 30 accounts that match the ideal implementation pain.",
        "Test one pricing experiment with pilots before locking a public price page.",
    ]
    citations = knowledge_base.retrieve(
        f"first 100 customers pricing strategy gtm {request.business_model} {request.target_customer}",
    )
    return make_finding(
        agent="gtm",
        focus_area="Distribution and pricing",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=citations,
    )

