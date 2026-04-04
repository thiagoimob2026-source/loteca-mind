"""
Leaderboard Router — Gamification endpoints.
Phase 1: Mock leaderboard data. Phase 2: Supabase integration.
"""

from fastapi import APIRouter
from app.models.user import LeaderboardEntry, UserProfile, Badge, BadgeType

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


# Mock leaderboard data
MOCK_LEADERBOARD = [
    LeaderboardEntry(rank=1, user_id="u1", display_name="ZebraKing_BR", total_points=2450,
                     accuracy_rate=0.72, badges_count=5, tier="Diamond"),
    LeaderboardEntry(rank=2, user_id="u2", display_name="xGMaster", total_points=2320,
                     accuracy_rate=0.68, badges_count=4, tier="Diamond"),
    LeaderboardEntry(rank=3, user_id="u3", display_name="LotecaPro2026", total_points=2180,
                     accuracy_rate=0.65, badges_count=4, tier="Gold"),
    LeaderboardEntry(rank=4, user_id="u4", display_name="TáticoGuru", total_points=1950,
                     accuracy_rate=0.63, badges_count=3, tier="Gold"),
    LeaderboardEntry(rank=5, user_id="u5", display_name="PalpiteiroChefe", total_points=1820,
                     accuracy_rate=0.61, badges_count=3, tier="Gold"),
    LeaderboardEntry(rank=6, user_id="u6", display_name="BolaMurcha99", total_points=1680,
                     accuracy_rate=0.58, badges_count=2, tier="Silver"),
    LeaderboardEntry(rank=7, user_id="u7", display_name="ClueFactor", total_points=1550,
                     accuracy_rate=0.55, badges_count=2, tier="Silver"),
    LeaderboardEntry(rank=8, user_id="u8", display_name="DataStrike", total_points=1420,
                     accuracy_rate=0.52, badges_count=1, tier="Silver"),
    LeaderboardEntry(rank=9, user_id="u9", display_name="GolDePenal", total_points=1300,
                     accuracy_rate=0.50, badges_count=1, tier="Bronze"),
    LeaderboardEntry(rank=10, user_id="u10", display_name="CraqueDoSofá", total_points=1180,
                      accuracy_rate=0.48, badges_count=1, tier="Bronze"),
]


@router.get("")
async def get_leaderboard():
    """Get global leaderboard."""
    return {
        "total_users": 1247,
        "entries": [e.model_dump() for e in MOCK_LEADERBOARD],
    }


@router.get("/badges/{user_id}")
async def get_user_badges(user_id: str):
    """Get badges for a specific user."""
    # Mock badges
    all_badges = [
        Badge(type=BadgeType.ZEBRA_MASTER, name="Mestre das Zebras",
              description="Acertou 5 zebras em uma temporada", icon="🦓"),
        Badge(type=BadgeType.MATH_STRATEGIST, name="Estrategista Matemático",
              description="Usou análise estatística para acertar 10 rodadas", icon="📊"),
        Badge(type=BadgeType.THE_SENSITIVE, name="O Sensitivo",
              description="Acertou 3 jogos baseado em fatores emocionais", icon="🔮"),
        Badge(type=BadgeType.PERFECT_ROUND, name="Rodada Perfeita",
              description="Acertou todos os 14 jogos de uma rodada", icon="🏆"),
        Badge(type=BadgeType.STREAK_3, name="Hat-trick de Rodadas",
              description="Acertou 13+ em 3 rodadas seguidas", icon="🔥"),
        Badge(type=BadgeType.FIRST_WIN, name="Primeira Vitória",
              description="Acertou sua primeira Loteca", icon="⭐"),
    ]
    return {"user_id": user_id, "badges": [b.model_dump() for b in all_badges[:3]]}
