"""Failure prediction engine using deterministic heuristics."""

from __future__ import annotations

from app.schemas.requests import WarRoomRequest
from app.schemas.responses import FailureRisk, ScoreCard
from app.utils.heuristics import clamp, financial_pressure, has_sensitive_data_risk, specificity_score


def predict_failure_risks(
    request: WarRoomRequest,
    scorecard: ScoreCard,
) -> list[FailureRisk]:
    risks = [
        FailureRisk(
            risk="Weak ICP proof",
            probability=clamp(100 - scorecard.market + (12 if not request.traction_summary else 0), 20, 95),
            severity="high" if scorecard.market < 60 else "medium",
            mitigation="Narrow the ICP and collect direct willingness-to-pay evidence before expanding the feature set.",
        ),
        FailureRisk(
            risk="Runway compression",
            probability=clamp(financial_pressure(request), 15, 95),
            severity="high" if request.runway_months < 9 else "medium",
            mitigation="Tie spending to pilot proof and prepare a burn-reduction plan before cash becomes the decision-maker.",
        ),
        FailureRisk(
            risk="Product sprawl",
            probability=clamp(95 - scorecard.product + (8 if " and " in request.solution.lower() else 0), 15, 90),
            severity="medium",
            mitigation="Cut the MVP to one mission-critical workflow and one measurable value moment.",
        ),
        FailureRisk(
            risk="Trust and compliance drag",
            probability=clamp(40 + (20 if has_sensitive_data_risk(request) else 0), 10, 85),
            severity="medium" if has_sensitive_data_risk(request) else "low",
            mitigation="Define data boundaries, audit logs, and human review before touching customer-sensitive workflows.",
        ),
        FailureRisk(
            risk="Shallow defensibility",
            probability=clamp(100 - scorecard.defensibility + (10 if specificity_score(request.market_context) < 35 else 0), 20, 90),
            severity="medium",
            mitigation="Capture proprietary workflow insight or dataset leverage before better-funded competitors copy the positioning.",
        ),
    ]
    return sorted(risks, key=lambda risk: risk.probability, reverse=True)[:4]

