"""Founder-facing helper routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.orchestration.war_room_pipeline import get_war_room_service
from app.schemas.responses import DemoPayload

router = APIRouter(prefix="/api/founder", tags=["founder"])


@router.get("/demo", response_model=DemoPayload)
def get_demo_request() -> DemoPayload:
    service = get_war_room_service()
    return DemoPayload(
        request=service.create_demo_request(),
        notes=[
            "Use this payload to drive the hackathon demo without typing everything manually.",
            "The sample is intentionally tuned to show debate, scoring, and runway tradeoffs.",
        ],
    )

