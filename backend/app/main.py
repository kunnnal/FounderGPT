from fastapi import FastAPI


app = FastAPI(
    title="FounderGPT API",
    description="Initial API scaffold for the Multi-Agent Startup War Room.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": "FounderGPT",
        "status": "scaffold",
        "message": "Multi-Agent Startup War Room API",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

