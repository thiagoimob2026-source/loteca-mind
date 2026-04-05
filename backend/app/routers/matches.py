"""
Matches Router — Endpoints for the 14-game Loteca grid.
Tries real API-Football data first, falls back to mock data.
"""

from fastapi import APIRouter

from app.services.data_service import get_current_matches
from app.services.football_api import fetch_real_matches

router = APIRouter(prefix="/api/matches", tags=["matches"])

# In-memory cache for the current round
_cached_matches = None
_data_source = "mock"


@router.get("")
async def list_matches():
    """Get all matches for the current Loteca round."""
    global _cached_matches, _data_source

    # O data_service já cuida do fallback entre API e Mock
    matches = await get_current_matches()
    _cached_matches = matches
    
    if matches and matches[0].round_number != 10: # Round 10 is our mock round_number
        _data_source = "api-football"
        competition = "Brasileirão Série A"
    else:
        _data_source = "mock"
        competition = "Loteca (Mock Data)"

    return {
        "round_number": matches[0].round_number if matches else 10,
        "competition": competition,
        "total_matches": len(matches),
        "data_source": _data_source,
        "matches": [m.model_dump() for m in matches],
    }


@router.get("/source")
async def get_data_source():
    """Check current data source."""
    return {"source": _data_source}


@router.get("/{match_id}")
async def get_match(match_id: int):
    """Get details for a specific match."""
    global _cached_matches
    if _cached_matches is None:
        _cached_matches = await get_current_matches()
    
    for m in _cached_matches:
        if m.id == match_id:
            return m.model_dump()
    return {"error": "Match not found"}, 404
