"""
Predictions Router — Endpoints for AI analysis and predictions.
"""

from datetime import datetime, timezone
from fastapi import APIRouter

from app.services.data_service import get_current_matches
from app.agents import alpha, psi
from app.agents.fusion import fuse
from app.agents.strategist import optimize
from app.models.prediction import LotecaPrediction

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

# Cache the latest prediction in memory (Phase 1)
_latest_prediction: dict | None = None


@router.post("/analyze")
async def analyze_round(target_budget: float = 49.90):
    """
    Run full AI analysis pipeline:
    1. Get match data
    2. Run Alpha (tactical) on each match
    3. Run Psi (psychological) on each match
    4. Fuse results
    5. Optimize ticket with Strategist
    """
    global _latest_prediction

    matches = get_current_matches()
    fusions = []

    for match in matches:
        # Run agents in parallel (conceptually — they're pure functions)
        alpha_result = alpha.analyze(match)
        psi_result = psi.analyze(match)

        # Fuse
        fusion_result = fuse(match, alpha_result, psi_result)
        fusions.append(fusion_result)

    # Optimize ticket
    strategy = optimize(fusions, target_budget=target_budget)

    # Build complete prediction
    prediction = LotecaPrediction(
        round_number=10,
        competition="Loteca",
        fusions=fusions,
        strategy=strategy,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    _latest_prediction = prediction.model_dump()
    return _latest_prediction


@router.get("/latest")
async def get_latest_prediction():
    """Return the most recent prediction (or generate one if none exists)."""
    global _latest_prediction
    if _latest_prediction is None:
        return await analyze_round()
    return _latest_prediction


@router.get("/{match_id}")
async def get_match_prediction(match_id: int):
    """Get the prediction for a specific match."""
    global _latest_prediction
    if _latest_prediction is None:
        await analyze_round()

    for fusion in _latest_prediction.get("fusions", []):
        if fusion["match_id"] == match_id:
            # Find corresponding strategy
            strategy_match = None
            for sug in _latest_prediction.get("strategy", {}).get("suggestions", []):
                if sug["match_id"] == match_id:
                    strategy_match = sug
                    break
            return {
                "fusion": fusion,
                "suggestion": strategy_match,
            }
    return {"error": "Match prediction not found"}, 404
