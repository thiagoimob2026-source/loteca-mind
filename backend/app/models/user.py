from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class BadgeType(str, Enum):
    ZEBRA_MASTER = "zebra_master"
    MATH_STRATEGIST = "math_strategist"
    THE_SENSITIVE = "the_sensitive"
    PERFECT_ROUND = "perfect_round"
    STREAK_3 = "streak_3"
    FIRST_WIN = "first_win"


class Badge(BaseModel):
    type: BadgeType
    name: str
    description: str
    icon: str
    earned_at: Optional[str] = None


class UserProfile(BaseModel):
    id: str
    email: str
    display_name: str = ""
    avatar_url: Optional[str] = None
    total_points: int = 0
    correct_predictions: int = 0
    total_predictions: int = 0
    accuracy_rate: float = 0.0
    badges: list[Badge] = Field(default_factory=list)
    rank: int = 0
    tier: str = "Bronze"  # Bronze, Silver, Gold, Diamond, Master


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    display_name: str
    avatar_url: Optional[str] = None
    total_points: int
    accuracy_rate: float
    badges_count: int
    tier: str
