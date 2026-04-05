"""
Data Service — Mock data for Phase 1.
Provides realistic match data for 14 games using real Brasileirão teams.
Will be replaced with real API data in Phase 2.
"""

import os
import json
import asyncio
from app.models.match import MatchData, TeamData, ContextData, TeamMomentum
from app.services import football_api


# Path to the manual contest file
CONCURSO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "concurso.json")


# Predefined matchday for the mock
MOCK_MATCHDAY = [
    ("Flamengo", "Palmeiras"),
    ("Botafogo", "Atlético-MG"),
    ("São Paulo", "Fluminense"),
    ("Internacional", "Grêmio"),
    ("Corinthians", "Cruzeiro"),
    ("Bahia", "Vasco"),
    ("Fortaleza", "Athletico-PR"),
    ("Santos", "Bragantino"),
    ("Juventude", "Cuiabá"),
    ("Vitória", "Sport"),
    ("Criciúma", "Mirassol"),
    ("Ceará", "Coritiba"),
    ("Goiás", "América-MG"),
    ("Ponte Preta", "Guarani"),
]

async def get_current_round() -> int:
    """Helper to get the current contest round."""
    if os.path.exists(CONCURSO_FILE):
        try:
            with open(CONCURSO_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("round_number", 10)
        except: return 10
    return 10

async def get_current_matches() -> list[MatchData]:
    """
    Orchestrator: Scouts all 14 matches on-demand from API-Sports.
    If a team isn't found, it fallbacks to a minimal verified=False match.
    """
    manual_grid = []
    concurso_round = 10
    
    if os.path.exists(CONCURSO_FILE):
        try:
            with open(CONCURSO_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                manual_grid = data.get("matches", [])
                concurso_round = data.get("round_number", 10)
        except Exception as e:
            print(f"[DataService] Error: {e}")

    if not manual_grid or len(manual_grid) < 14:
        print("[DataService] Using default MOCK_MATCHDAY grid.")
        manual_grid = MOCK_MATCHDAY

    # Semáforo para controlar o fluxo de saída e evitar crashes de rede
    semaphore = asyncio.Semaphore(5)

    async def get_single_match_scout(idx, home, away, round_num):
        async with semaphore:
            # 1. Tentar ler do Cache do Banco Primeiro
            cached_data = await get_scout_cache(home, away, round_num)
            if cached_data:
                return MatchData(**cached_data)
            
            # 2. Se não houver, chama a API Real
            match_scout = await football_api.scout_match(idx, home, away, round_num)
            
            # 3. Se a API retornou dados reais, salva no cache para não gastar mais
            if match_scout.is_verified:
                await save_scout_cache(home, away, round_num, match_scout.model_dump())
            
            return match_scout

    print(f"[DataService] Iniciando Scout Paralelo (Batch de 5) de 14 jogos... 🕵️‍♂️")
    
    tasks = [get_single_match_scout(i + 1, home, away, concurso_round) for i, (home, away) in enumerate(manual_grid)]
    matches = await asyncio.gather(*tasks)
    
    # Check coverage
    verified_count = sum(1 for m in matches if m.is_verified)
    print(f"[DataService] Scout concluído! {verified_count}/14 jogos verificados com dados REAIS.")
    
    return matches
