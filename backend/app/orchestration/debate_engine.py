"""Debate engine that turns agent findings into a readable exchange."""

from __future__ import annotations

from app.schemas.responses import AgentFinding, DebateTurn, Recommendation, ScoreCard


def _first_text(items: list[str], fallback: str) -> str:
    return items[0] if items else fallback


def build_debate(
    agent_findings: list[AgentFinding],
    scorecard: ScoreCard,
    recommendation: Recommendation,
) -> list[DebateTurn]:
    lookup = {finding.agent: finding for finding in agent_findings}
    market = lookup.get("market")
    product = lookup.get("product")
    finance = lookup.get("finance")
    risk = lookup.get("risk")
    critic = lookup.get("critic")

    return [
        DebateTurn(
            speaker="market",
            counterparty="product",
            stance="challenge",
            message=_first_text(
                market.concerns if market else [],
                "The customer segment needs to be tighter before the product can claim repeatability.",
            ),
        ),
        DebateTurn(
            speaker="product",
            counterparty="market",
            stance="support",
            message=_first_text(
                product.strengths if product else [],
                "A focused MVP can prove the wedge quickly if it stays anchored to one high-friction workflow.",
            ),
        ),
        DebateTurn(
            speaker="finance",
            counterparty="gtm",
            stance="challenge",
            message=_first_text(
                finance.concerns if finance else [],
                "The team should protect runway until GTM proof becomes consistent.",
            ),
        ),
        DebateTurn(
            speaker="risk",
            counterparty="decision",
            stance="challenge",
            message=_first_text(
                risk.concerns if risk else [],
                "The biggest risk still needs explicit mitigation before scaling spend.",
            ),
        ),
        DebateTurn(
            speaker="critic",
            counterparty="founder",
            stance="synthesis",
            message=_first_text(
                critic.summary.split(". ") if critic else [],
                "The opportunity is real, but the weakest score dimension should dominate the next sprint plan.",
            ),
        ),
        DebateTurn(
            speaker="decision",
            counterparty="team",
            stance="synthesis",
            message=f"Overall score is {scorecard.overall}/100. Final call: {recommendation.decision}.",
        ),
    ]

