"""What-if simulation engine for founder decisions."""

from __future__ import annotations

from app.schemas.requests import WarRoomRequest
from app.schemas.responses import ScenarioResult, ScoreCard
from app.utils.heuristics import clamp


def run_simulations(
    request: WarRoomRequest,
    scorecard: ScoreCard,
) -> list[ScenarioResult]:
    narrower_icp_gain = clamp((70 - scorecard.market) * 0.5 + 25, 25, 88)
    price_test_gain = clamp((65 - scorecard.financial) * 0.4 + 32, 20, 78)
    burn_cut_gain = clamp(request.runway_months * 4 + 18, 25, 92)
    pilot_conversion_gain = clamp((80 - scorecard.execution) * 0.45 + 28, 25, 84)

    return [
        ScenarioResult(
            name="Narrow the ICP",
            assumption="Focus only on mid-market B2B SaaS teams with complex implementation onboarding.",
            outcome=(
                "Positioning becomes sharper, discovery calls get cleaner, and the odds of a repeatable first use case rise."
            ),
            impact_score=narrower_icp_gain,
        ),
        ScenarioResult(
            name="Run a pricing test",
            assumption="Test a 20 percent higher pilot price anchored to activation lift and support savings.",
            outcome=(
                "If buyers still convert, the business model becomes more attractive without adding product complexity."
            ),
            impact_score=price_test_gain,
        ),
        ScenarioResult(
            name="Cut burn by 15 percent",
            assumption=f"Reduce monthly burn while protecting the core team, extending runway beyond {request.runway_months} months.",
            outcome=(
                "The team buys more learning cycles and reduces the chance that fundraising timing controls strategy."
            ),
            impact_score=burn_cut_gain,
        ),
        ScenarioResult(
            name="Convert design partners faster",
            assumption="Turn the next three pilots into case-study-backed expansion accounts.",
            outcome=(
                "Execution credibility improves because the product story is backed by proof, not only narrative."
            ),
            impact_score=pilot_conversion_gain,
        ),
    ]

