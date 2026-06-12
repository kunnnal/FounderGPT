"""Agent routing for the demo pipeline."""

from __future__ import annotations

from app.schemas.requests import WarRoomRequest


def build_routing_plan(_: WarRoomRequest) -> list[str]:
    return [
        "planner",
        "founder_profile",
        "market",
        "product",
        "gtm",
        "finance",
        "risk",
        "compliance",
        "critic",
        "decision",
        "report",
    ]

