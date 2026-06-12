"""Decision agent for the final operating recommendation."""

from __future__ import annotations

from app.agents.common import make_finding
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import WarRoomRequest
from app.schemas.responses import FailureRisk, Recommendation, ScoreCard
from app.utils.heuristics import clamp


def run_decision_agent(
    request: WarRoomRequest,
    scorecard: ScoreCard,
    failure_risks: list[FailureRisk],
    knowledge_base: LocalKnowledgeBaseClient,
) -> tuple[object, Recommendation]:
    top_risk = failure_risks[0] if failure_risks else None
    if scorecard.overall >= 78 and scorecard.financial >= 55:
        decision = "Push into a paid pilot motion"
        readiness = "Reasonable for early investor conversations once pilots become repeatable."
    elif scorecard.overall >= 64:
        decision = "Build a tighter MVP and win design partners"
        readiness = "Too early for fundraising; focus on pilot proof and retention evidence first."
    elif scorecard.overall >= 50:
        decision = "Pause buildout and run deeper customer discovery"
        readiness = "Not ready for investors; prove pain and willingness to pay before expanding scope."
    else:
        decision = "Do not scale this idea yet"
        readiness = "Investor readiness is low until the team changes the wedge or the evidence base."

    rationale = (
        f"{request.startup_name} scores {scorecard.overall}/100 overall. The business is most ready in "
        f"{scorecard.readiness_stage.lower()}, but the top drag is {top_risk.risk.lower() if top_risk else 'execution uncertainty'}."
    )
    milestones = [
        "Close three to five high-fit design partners with a shared problem pattern.",
        "Show one measurable activation or retention lift from the MVP.",
        "Hold spend flat until learning velocity justifies expansion.",
    ]
    confidence = clamp((scorecard.overall + (100 - (top_risk.probability if top_risk else 40))) / 2, 35, 94)
    recommendation = Recommendation(
        decision=decision,
        confidence=confidence,
        rationale=rationale,
        milestones=milestones,
        investor_readiness=readiness,
    )
    citations = knowledge_base.retrieve(
        f"investor readiness runway planning startup failure patterns {request.business_model}",
    )
    finding = make_finding(
        agent="decision",
        focus_area="Go or no-go",
        score=confidence,
        summary=decision,
        strengths=[
            f"Overall readiness is {scorecard.overall}/100.",
            f"The current stage recommendation is {scorecard.readiness_stage}.",
        ],
        concerns=[
            top_risk.mitigation if top_risk else "The next milestone must reduce uncertainty, not add breadth.",
        ],
        next_steps=milestones,
        citations=citations,
    )
    return finding, recommendation

