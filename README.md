# FounderGPT: Multi-Agent Startup War Room

FounderGPT is a hackathon project scaffold for a production-style multi-agent reasoning system that helps founders pressure-test startup ideas.

This repository is intentionally lightweight right now. It sets up the project structure, documentation, placeholder agent modules, frontend surfaces, synthetic data, and deployment notes needed to build quickly during the hackathon.

## Project Areas

- `docs/` - architecture, workflow, agents, demo, judging, and API planning.
- `backend/` - FastAPI service, agent placeholders, orchestration, scoring engines, retrieval, schemas, and tests.
- `frontend/` - dashboard-oriented Next.js placeholder structure.
- `knowledge_base/` - starter documents for grounded retrieval.
- `data/` - synthetic founder, startup, market, and demo session data.
- `deployment/` - Docker and Azure deployment planning files.

## First Milestone

Build a local MVP pipeline that accepts a startup idea, routes it through a planner and specialist agents, scores readiness, predicts failure risks, runs what-if scenarios, and produces a decision report.

