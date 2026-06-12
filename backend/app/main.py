from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.founder import router as founder_router
from app.api.health import router as health_router
from app.api.war_room import router as war_room_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Multi-agent startup war room demo API for hackathon use.",
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(founder_router)
app.include_router(war_room_router)


@app.get("/")
def read_root() -> dict[str, object]:
    return {
        "name": "FounderGPT",
        "status": "ready",
        "message": "Multi-Agent Startup War Room API",
        "routes": [
            "/api/health",
            "/api/founder/demo",
            "/api/war-room/analyze",
            "/api/war-room/demo",
        ],
    }

