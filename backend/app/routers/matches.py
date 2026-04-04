"""
Matches Router — Endpoints for the 14-game Loteca grid.
"""

from fastapi import APIRouter

from app.services.data_service import get_current_matches

router = APIRouter(prefix="/api/matches", tags=["matches"])


@router.get("")
async def list_matches():
    """Get all 14 matches for the current Loteca round."""
    matches = get_current_matches()
    return {
        "round_number": 10,
        "competition": "Loteca",
        "total_matches": len(matches),
        "matches": [m.model_dump() for m in matches],
    }


@router.get("/{match_id}")
async def get_match(match_id: int):
    """Get details for a specific match."""
    matches = get_current_matches()
    for m in matches:
        if m.id == match_id:
            return m.model_dump()
    return {"error": "Match not found"}, 404
