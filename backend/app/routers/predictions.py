"""
Predictions Router — Endpoints for AI analysis and predictions.
"""

from datetime import datetime, timezone
from fastapi import APIRouter

from app.services.data_service import get_current_matches
from app.services import gemini_service, supabase_service
from app.agents import alpha, psi
from app.agents.fusion import fuse
from app.agents.strategist import optimize
from app.models.prediction import LotecaPrediction

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

# Cache the latest prediction in memory (Phase 1)
_latest_prediction: dict | None = None


@router.post("/analyze")
async def analyze_round(target_budget: float = 49.90, use_ai: bool = True):
    """
    Run full AI analysis pipeline:
    1. Get match data
    2. Run Alpha (tactical) on each match
    3. Run Psi (psychological) on each match
    4. Fuse results
    5. Generate AI Narratives (Phase 2C - Internal Site Analyst)
    6. Optimize ticket with Strategist
    """
    global _latest_prediction

    matches = await get_current_matches()
    fusions = []

    for match in matches:
        # 1-3. Run agents
        alpha_result = alpha.analyze(match)
        psi_result = psi.analyze(match)
        
        # 4. Fuse
        fusion_result = fuse(match, alpha_result, psi_result)
        
        # 5. Gemini AI Insight (Service for the Site)
        if use_ai:
            ai_insight = await gemini_service.generate_match_analysis(
                match, # Pass full match object
                alpha_data=alpha_result.model_dump(),
                psi_data=psi_result.model_dump()
            )
            
            if ai_insight:
                # Update fusion result with premium AI text
                fusion_result.key_factors = ai_insight.get("technical_summary", fusion_result.key_factors)
                fusion_result.emotional_factors = [ai_insight.get("emotional_narrative", "")]
                fusion_result.deep_analysis = ai_insight.get("deep_analysis")
                
                # RAG Zebra Override
                if ai_insight.get("trigger_zebra_alert"):
                    fusion_result.zebra_alert = True
                
                if fusion_result.zebra_alert:
                    fusion_result.zebra_insight = ai_insight.get("zebra_hunter_verdict", fusion_result.zebra_insight)
                
                # RAG Override for Visual Gauges
                if "reason_score_override" in ai_insight and "emotion_score_override" in ai_insight:
                    fusion_result.reason_score = float(ai_insight["reason_score_override"])
                    fusion_result.emotion_score = float(ai_insight["emotion_score_override"])

        fusions.append(fusion_result)

    # 6. Optimize ticket
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
    
    # Persistir no Supabase (Deploy Readiness)
    await supabase_service.save_round_analysis(prediction.round_number, _latest_prediction)
    
    return _latest_prediction


@router.get("/latest")
async def get_latest_prediction():
    """Return the most recent prediction (from Cache or Supabase)."""
    global _latest_prediction
    
    # 1. Check Cache
    if _latest_prediction:
        return _latest_prediction
    
    # 2. Check Supabase
    db_prediction = await supabase_service.get_latest_analysis()
    if db_prediction:
        _latest_prediction = db_prediction
        return _latest_prediction
        
    # 3. Last resort: Generate new
    return await analyze_round()


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
