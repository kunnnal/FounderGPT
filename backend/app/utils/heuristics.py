"""Deterministic heuristics for the hackathon demo."""

from __future__ import annotations

import re
from typing import Iterable

from app.schemas.requests import WarRoomRequest

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}

AI_KEYWORDS = {"ai", "llm", "agent", "model", "copilot", "automation"}
SENSITIVE_DATA_KEYWORDS = {
    "health",
    "patient",
    "finance",
    "bank",
    "payroll",
    "biometric",
    "identity",
    "medical",
    "hr",
    "insurance",
}


def clamp(value: float, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(int(round(value)), maximum))


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS and len(token) > 2
    }


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    haystack = text.lower()
    return any(keyword.lower() in haystack for keyword in keywords)


def specificity_score(text: str) -> int:
    tokens = tokenize(text)
    if not tokens:
        return 0
    structural_bonus = 10 if "," in text or " for " in text.lower() else 0
    return clamp(len(tokens) * 4 + structural_bonus, 0, 100)


def stage_weight(stage: str) -> int:
    stage_map = {
        "idea": 28,
        "validation": 38,
        "mvp": 52,
        "pilot": 66,
        "growth": 78,
    }
    return stage_map.get(stage, 30)


def traction_bonus(request: WarRoomRequest) -> int:
    bonus = 0
    if request.monthly_revenue > 0:
        bonus += min(int(request.monthly_revenue // 1000) * 4, 20)
    if request.traction_summary.strip():
        bonus += 10
    return min(bonus, 25)


def founder_strength(request: WarRoomRequest) -> int:
    founder = request.founder
    experience_component = min(founder.years_experience * 2, 20)
    exits_component = min(founder.previous_startup_exits * 8, 16)
    skill_component = founder.technical_strength * 2 + founder.go_to_market_strength * 2
    return clamp(experience_component + exits_component + skill_component, 0, 100)


def financial_pressure(request: WarRoomRequest) -> int:
    if request.monthly_burn <= 0:
        return 20
    if request.monthly_revenue <= 0:
        return clamp(70 - request.runway_months * 2, 10, 95)
    burn_multiple = request.monthly_burn / max(request.monthly_revenue, 1)
    return clamp(burn_multiple * 18 - request.runway_months, 5, 95)


def is_ai_product(request: WarRoomRequest) -> bool:
    combined = " ".join(
        [
            request.one_line_pitch,
            request.problem,
            request.solution,
            request.business_model,
        ],
    )
    return contains_any(combined, AI_KEYWORDS)


def has_sensitive_data_risk(request: WarRoomRequest) -> bool:
    combined = " ".join(
        [
            request.one_line_pitch,
            request.problem,
            request.solution,
            request.target_customer,
            request.market_context,
        ],
    )
    return contains_any(combined, SENSITIVE_DATA_KEYWORDS)
