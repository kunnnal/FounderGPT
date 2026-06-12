"""Shared helpers for deterministic agent outputs."""

from __future__ import annotations

from app.schemas.responses import AgentFinding, Citation
from app.utils.heuristics import clamp


def verdict_from_score(score: int) -> str:
    if score >= 80:
        return "Strong"
    if score >= 65:
        return "Promising"
    if score >= 50:
        return "Needs validation"
    return "High risk"


def clean_points(items: list[str], limit: int = 3) -> list[str]:
    return [item.strip() for item in items if item and item.strip()][:limit]


def make_finding(
    *,
    agent: str,
    focus_area: str,
    score: int,
    summary: str,
    strengths: list[str],
    concerns: list[str],
    next_steps: list[str],
    citations: list[Citation],
) -> AgentFinding:
    return AgentFinding(
        agent=agent,
        focus_area=focus_area,
        verdict=verdict_from_score(score),
        confidence=clamp(score, 30, 95),
        summary=summary,
        strengths=clean_points(strengths),
        concerns=clean_points(concerns),
        next_steps=clean_points(next_steps),
        citations=citations,
    )


def format_currency(amount: float) -> str:
    return f"${amount:,.0f}"
