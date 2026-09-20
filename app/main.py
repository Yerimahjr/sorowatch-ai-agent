from fastapi import FastAPI
from pydantic import BaseModel

from app.graph.pipeline import run_pipeline

app = FastAPI(
    title="SoroWatch AI Agent",
    description="Standalone risk-scoring service using a LangGraph pipeline.",
    version="0.1.0",
)


class ScoreRequest(BaseModel):
    address: str
    threshold: int = 50


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/score")
async def score_address(req: ScoreRequest):
    result = await run_pipeline(req.address, req.threshold)
    return {
        "address": result["address"],
        "score": result["score"],
        "flagged": result["flagged"],
        "operations_considered": len(result["operations"]),
    }
