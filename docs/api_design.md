# API Design

The backend API will expose the war room workflow to the frontend.

## Planned Endpoints

- `GET /` - service metadata.
- `GET /health` - health check.
- `POST /war-room/run` - run startup idea analysis.
- `GET /founder/{founder_id}` - retrieve founder profile.
- `GET /war-room/{session_id}` - retrieve a previous session.

