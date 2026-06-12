"""Compliance agent for AI, privacy, and data-handling risks."""

from __future__ import annotations

from app.agents.common import make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.utils.heuristics import clamp, has_sensitive_data_risk, is_ai_product


def run_compliance_agent(
    request: WarRoomRequest,
    knowledge_base: LocalKnowledgeBaseClient,
) -> object:
    ai_product = is_ai_product(request)
    sensitive = has_sensitive_data_risk(request)
    base_score = 82
    if ai_product:
        base_score -= 12
    if sensitive:
        base_score -= 18
    score = clamp(base_score, 30, 88)
    summary = (
        "Compliance is manageable for the demo, but any AI workflow touching customer data needs explicit logging, "
        "human review boundaries, and basic privacy hygiene before broader rollout."
    )
    strengths = [
        "The product use case is narrow enough to define acceptable model behavior.",
        "The team can add governance early because the architecture is still lightweight.",
        "Compliance exposure is lower when the MVP avoids storing unnecessary raw customer data."
        if sensitive
        else "The current idea does not appear to sit in a heavily regulated workflow by default.",
    ]
    concerns = [
        "AI-generated recommendations should be auditable and overridable by the human operator."
        if ai_product
        else "Automation logic still needs transparent rules even if it is not model-driven.",
        "Any ingestion of customer onboarding data should be minimized and access-controlled."
        if sensitive
        else "The team should define a basic privacy posture before collecting customer data at scale.",
    ]
    next_steps = [
        "Document what data enters the system, why it is needed, and how long it is retained.",
        "Add a human review step for high-impact automation paths.",
        "Create a lightweight checklist for privacy, bias, and auditability before every pilot.",
    ]
    citations = knowledge_base.retrieve(
        f"data privacy ai bias compliance ai product {request.solution} {request.target_customer}",
    )
    return make_finding(
        agent="compliance",
        focus_area="AI and privacy controls",
        score=score,
        summary=summary,
        strengths=strengths,
        concerns=concerns,
        next_steps=next_steps,
        citations=citations,
    )

