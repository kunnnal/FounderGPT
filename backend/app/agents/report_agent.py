"""Report agent for the founder-facing summary."""

from __future__ import annotations

from app.agents.common import make_finding
from app.schemas.requests import WarRoomRequest
from app.schemas.responses import AgentFinding, FailureRisk, Recommendation, ScoreCard
from app.utils.heuristics import clamp


def run_report_agent(
    request: WarRoomRequest,
    scorecard: ScoreCard,
    recommendation: Recommendation,
    agent_findings: list[AgentFinding],
    failure_risks: list[FailureRisk],
) -> tuple[object, str]:
    strongest_signal = next(
        (
            finding.strengths[0]
            for finding in agent_findings
            if finding.strengths
        ),
        "The opportunity is coherent enough to test quickly.",
    )
    top_risk = failure_risks[0] if failure_risks else None
    executive_summary = (
        f"{request.startup_name} is a {scorecard.readiness_stage.lower()} opportunity with an overall readiness "
        f"score of {scorecard.overall}/100. Strongest signal: {strongest_signal} Biggest risk: "
        f"{top_risk.risk.lower() if top_risk else 'unstructured execution risk'}. Recommendation: {recommendation.decision}."
    )
    finding = make_finding(
        agent="report",
        focus_area="Founder readout",
        score=clamp(scorecard.overall, 35, 94),
        summary=executive_summary,
        strengths=[
            f"Recommendation confidence is {recommendation.confidence}/100.",
            f"Investor readiness: {recommendation.investor_readiness}",
        ],
        concerns=[
            top_risk.mitigation if top_risk else "The team still needs clearer proof before scaling.",
        ],
        next_steps=recommendation.milestones,
        citations=[],
    )
    return finding, executive_summary

