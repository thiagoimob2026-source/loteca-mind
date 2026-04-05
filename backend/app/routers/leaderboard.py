from fastapi import APIRouter
from app.services import supabase_service
from app.models.user import LeaderboardEntry, UserProfile, Badge, BadgeType

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("")
async def get_leaderboard():
    """Get global leaderboard (Real or Mock)."""
    real_data = await supabase_service.get_leaderboard_data()
    
    if real_data:
        entries = [
            LeaderboardEntry(
                rank=i + 1,
                user_id=row["id"],
                display_name=row["display_name"] or "Analista Anônimo",
                avatar_url=row["avatar_url"],
                total_points=row["total_points"],
                accuracy_rate=row["accuracy_rate"],
                badges_count=0, # To be implemented (count join)
                tier=row["tier"]
            )
            for i, row in enumerate(real_data)
        ]
        return {
            "total_users": len(real_data),
            "entries": [e.model_dump() for e in entries],
            "data_source": "supabase"
        }

    # Fallback para Mock se o banco estiver vazio/desconectado
    return {
        "total_users": len(MOCK_LEADERBOARD),
        "entries": [e.model_dump() for e in MOCK_LEADERBOARD],
        "data_source": "mock"
    }

# Mock leaderboard data (Fallback)
MOCK_LEADERBOARD = [
    # ... (existing mock data)
]


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
