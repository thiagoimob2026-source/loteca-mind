import asyncio
import os
from app.services import gemini_service
from app.models.match import MatchData, TeamData, ContextData

async def test_single_match():
    print("🚀 Testando Gemini 2.0 Flash em 1 jogo real...")
    
    # Criando um jogo mock realista
    match = MatchData(
        id=1,
        round_number=1280,
        competition="Brasileirão Série A",
        home_team=TeamData(name="Flamengo", xg_accumulated=1.85, clutch_factor=0.75, form_last_5=["W","W","D","W","L"]),
        away_team=TeamData(name="Palmeiras", xg_accumulated=1.62, clutch_factor=0.82, form_last_5=["W","D","D","W","W"]),
        home_context=ContextData(momentum="stable", away_resilience=0.0), # No mando
        away_context=ContextData(momentum="on_fire", away_resilience=0.7),
        venue="Maracanã",
        kickoff_time="2026-04-06T16:00:00-03:00",
        head_to_head={"home_wins": 35, "draws": 30, "away_wins": 38},
        is_verified=True
    )

    alpha_data = {
        "home_win_prob": 0.42,
        "draw_prob": 0.28,
        "away_win_prob": 0.30,
        "xg_differential": 0.23
    }
    
    psi_data = {
        "match_volatility": 45,
        "zebra_alert": False,
        "emotional_factors": ["Pressão da torcida no Maracanã", "Palmeiras muito resiliente fora"]
    }

    print(f"\n--- Analisando {match.home_team.name} vs {match.away_team.name} ---\n")
    
    analysis = await gemini_service.generate_match_analysis(
        match,
        alpha_data=alpha_data,
        psi_data=psi_data
    )

    if analysis:
        import json
        print("✅ Resultado do Gemini 2.0 Flash (JSON):\n")
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
        
        print("\n--- Texto Principal do Analista ---\n")
        print(analysis.get("deep_analysis", "Erro: Texto não gerado"))
    else:
        print("❌ Falha na análise. Verifique sua GEMINI_API_KEY no .env")

if __name__ == "__main__":
    asyncio.run(test_single_match())
