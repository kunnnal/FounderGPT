# Backend

FastAPI service for the FounderGPT multi-agent war room.

## What It Does

- Accepts a structured startup brief.
- Runs planner, founder-profile, market, product, GTM, finance, risk, compliance, critic, decision, and report passes.
- Produces readiness scores, failure risks, simulations, debate output, and a final recommendation.
- Stores generated sessions in memory for report-route lookup.

## Run

Requires Python 3.11+ installed locally.

```powershell
cd backend
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test

```powershell
cd backend
.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -t .
```

## Important Routes

- `GET /api/health`
- `GET /api/founder/demo`
- `POST /api/war-room/analyze`
- `GET /api/war-room/sessions/{session_id}`
- `GET /api/war-room/demo`

