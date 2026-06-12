"""War room API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.orchestration.war_room_pipeline import get_war_room_service
from app.schemas.requests import WarRoomRequest
from app.schemas.responses import WarRoomResponse

router = APIRouter(prefix="/api/war-room", tags=["war-room"])


@router.post("/analyze", response_model=WarRoomResponse)
def analyze_startup(payload: WarRoomRequest) -> WarRoomResponse:
    service = get_war_room_service()
    return service.run_analysis(payload)


@router.get("/sessions/{session_id}", response_model=WarRoomResponse)
def get_session(session_id: str) -> WarRoomResponse:
    service = get_war_room_service()
    session = service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session


@router.get("/demo", response_model=WarRoomResponse)
def run_demo_analysis() -> WarRoomResponse:
    service = get_war_room_service()
    return service.run_analysis(service.create_demo_request())

