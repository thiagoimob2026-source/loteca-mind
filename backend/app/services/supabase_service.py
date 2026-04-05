"""
Supabase Service — Database Persistence & User Management
"""

import json
from typing import Optional, List, Dict
from supabase import create_client, Client
from app.config import get_settings

settings = get_settings()

# Initialize Supabase Client
supabase: Optional[Client] = None
if settings.SUPABASE_URL and settings.SUPABASE_KEY:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def is_active() -> bool:
    return supabase is not None

async def save_round_analysis(round_number: int, prediction_data: Dict):
    """Persist the 14-game analysis to the DB."""
    if not supabase:
        return
    
    try:
        data = {
            "round_number": round_number,
            "full_prediction_json": prediction_data,
        }
        supabase.table("analysis_history").insert(data).execute()
        print(f"[Supabase] Analysis for round {round_number} saved.")
    except Exception as e:
        print(f"[Supabase] Error saving analysis: {e}")

async def get_latest_analysis() -> Optional[Dict]:
    """Retrieve the most recent analysis from DB."""
    if not supabase:
        return None
    
    try:
        response = supabase.table("analysis_history") \
            .select("full_prediction_json") \
            .order("generated_at", desc=True) \
            .limit(1) \
            .execute()
        
        if response.data:
            return response.data[0]["full_prediction_json"]
        return None
    except Exception as e:
        print(f"[Supabase] Error fetching latest analysis: {e}")
        return None

async def get_leaderboard_data() -> List[Dict]:
    """Fetch user rankings from the profiles table."""
    if not supabase:
        return []
    
    try:
        response = supabase.table("profiles") \
            .select("id, display_name, avatar_url, total_points, accuracy_rate, tier") \
            .order("total_points", desc=True) \
            .limit(10) \
            .execute()
        
        return response.data
    except Exception as e:
        print(f"[Supabase] Error fetching leaderboard: {e}")
        return []

async def update_user_score(user_id: str, points_earned: int, correct_count: int):
    """Increment user stats after a round concludes."""
    if not supabase:
        return
    
    try:
        # Get current stats
        user = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        if user.data:
            new_total = user.data["total_points"] + points_earned
            new_correct = user.data["correct_predictions"] + correct_count
            new_total_pred = user.data["total_predictions"] + 14 # 14 games per round
            
            data = {
                "total_points": new_total,
                "correct_predictions": new_correct,
                "total_predictions": new_total_pred,
                "accuracy_rate": round(new_correct / new_total_pred, 3)
            }
            supabase.table("profiles").update(data).eq("id", user_id).execute()
    except Exception as e:
        print(f"[Supabase] Error updating user score: {e}")
