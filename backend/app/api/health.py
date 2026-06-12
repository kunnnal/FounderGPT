"""Health API routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.config import settings

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
def health_check() -> dict[str, object]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }

