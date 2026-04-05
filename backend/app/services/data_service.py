"""
Data Service — Mock data for Phase 1.
Provides realistic match data for 14 games using real Brasileirão teams.
Will be replaced with real API data in Phase 2.
"""

import os
import json
import random
from app.models.match import MatchData, TeamData, ContextData, TeamMomentum
from app.services import football_api


# Path to the manual contest file
CONCURSO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "concurso.json")


# Realistic Brasileirão team profiles
TEAM_PROFILES = {
    "Flamengo": {"xg": 1.85, "vp": 22, "be": 18, "ca": 0.35, "cs": 0.40, "form": ["W","W","D","W","L"]},
    "Palmeiras": {"xg": 1.72, "vp": 20, "be": 16, "ca": 0.30, "cs": 0.45, "form": ["W","W","W","D","W"]},
    "Botafogo": {"xg": 1.65, "vp": 19, "be": 15, "ca": 0.32, "cs": 0.35, "form": ["W","D","W","W","D"]},
    "Atlético-MG": {"xg": 1.55, "vp": 18, "be": 14, "ca": 0.28, "cs": 0.30, "form": ["L","W","D","W","W"]},
    "Fluminense": {"xg": 1.30, "vp": 16, "be": 13, "ca": 0.22, "cs": 0.25, "form": ["L","L","D","W","L"]},
    "São Paulo": {"xg": 1.50, "vp": 17, "be": 14, "ca": 0.25, "cs": 0.35, "form": ["D","W","W","L","D"]},
    "Internacional": {"xg": 1.60, "vp": 18, "be": 15, "ca": 0.27, "cs": 0.38, "form": ["W","W","D","D","W"]},
    "Grêmio": {"xg": 1.40, "vp": 16, "be": 13, "ca": 0.24, "cs": 0.30, "form": ["D","L","W","D","W"]},
    "Corinthians": {"xg": 1.35, "vp": 15, "be": 12, "ca": 0.20, "cs": 0.28, "form": ["L","D","L","W","D"]},
    "Cruzeiro": {"xg": 1.45, "vp": 17, "be": 14, "ca": 0.26, "cs": 0.32, "form": ["W","D","W","L","W"]},
    "Vasco": {"xg": 1.25, "vp": 14, "be": 11, "ca": 0.19, "cs": 0.22, "form": ["L","L","W","D","L"]},
    "Bahia": {"xg": 1.50, "vp": 17, "be": 14, "ca": 0.28, "cs": 0.33, "form": ["W","W","D","W","D"]},
    "Athletico-PR": {"xg": 1.38, "vp": 16, "be": 13, "ca": 0.23, "cs": 0.28, "form": ["D","W","L","D","W"]},
    "Fortaleza": {"xg": 1.55, "vp": 18, "be": 15, "ca": 0.30, "cs": 0.36, "form": ["W","W","W","D","D"]},
    "Santos": {"xg": 1.20, "vp": 14, "be": 11, "ca": 0.18, "cs": 0.20, "form": ["L","D","L","L","W"]},
    "Bragantino": {"xg": 1.42, "vp": 16, "be": 13, "ca": 0.25, "cs": 0.30, "form": ["D","W","D","W","L"]},
    "Juventude": {"xg": 1.10, "vp": 13, "be": 10, "ca": 0.16, "cs": 0.18, "form": ["L","L","D","L","D"]},
    "Cuiabá": {"xg": 1.05, "vp": 12, "be": 9, "ca": 0.15, "cs": 0.15, "form": ["L","D","L","L","L"]},
    "Vitória": {"xg": 1.15, "vp": 13, "be": 10, "ca": 0.17, "cs": 0.20, "form": ["D","L","W","L","D"]},
    "Criciúma": {"xg": 1.08, "vp": 12, "be": 9, "ca": 0.14, "cs": 0.16, "form": ["L","L","D","D","L"]},
    "Sport": {"xg": 1.18, "vp": 14, "be": 11, "ca": 0.19, "cs": 0.22, "form": ["W","D","L","W","D"]},
    "Mirassol": {"xg": 1.22, "vp": 14, "be": 11, "ca": 0.20, "cs": 0.24, "form": ["D","W","D","L","W"]},
    "Ceará": {"xg": 1.15, "vp": 13, "be": 10, "ca": 0.18, "cs": 0.21, "form": ["W","L","D","W","L"]},
    "Coritiba": {"xg": 1.12, "vp": 13, "be": 10, "ca": 0.17, "cs": 0.19, "form": ["L","D","L","D","W"]},
    "Goiás": {"xg": 1.18, "vp": 14, "be": 11, "ca": 0.19, "cs": 0.22, "form": ["D","L","W","L","D"]},
    "América-MG": {"xg": 1.20, "vp": 14, "be": 11, "ca": 0.20, "cs": 0.23, "form": ["L","W","D","L","W"]},
    "Ponte Preta": {"xg": 1.05, "vp": 12, "be": 9, "ca": 0.14, "cs": 0.16, "form": ["D","L","L","D","L"]},
    "Guarani": {"xg": 1.02, "vp": 11, "be": 8, "ca": 0.13, "cs": 0.14, "form": ["L","L","D","L","L"]},
}

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

# Context scenarios (to make analysis more interesting)
CONTEXT_SCENARIOS = [
    {"home": ContextData(momentum=TeamMomentum.ON_FIRE, is_six_pointer=True),
     "away": ContextData(momentum=TeamMomentum.STABLE, ex_players_in_opponent=1)},
    {"home": ContextData(momentum=TeamMomentum.STABLE, var_incidents_last_5=3),
     "away": ContextData(momentum=TeamMomentum.STABLE, away_resilience=0.7)},
    {"home": ContextData(momentum=TeamMomentum.STABLE, consecutive_losses=0),
     "away": ContextData(momentum=TeamMomentum.CRISIS, consecutive_losses=4, recent_news_sentiment=-0.6)},
    {"home": ContextData(momentum=TeamMomentum.STABLE),
     "away": ContextData(momentum=TeamMomentum.STABLE)},
    {"home": ContextData(momentum=TeamMomentum.CRISIS, consecutive_losses=3, recent_news_sentiment=-0.4),
     "away": ContextData(momentum=TeamMomentum.NEW_COACH, coach_change_days=5)},
    {"home": ContextData(momentum=TeamMomentum.ON_FIRE, is_six_pointer=True),
     "away": ContextData(momentum=TeamMomentum.CRISIS, consecutive_losses=5)},
    {"home": ContextData(momentum=TeamMomentum.STABLE, var_incidents_last_5=2),
     "away": ContextData(momentum=TeamMomentum.STABLE, away_resilience=0.8)},
    {"home": ContextData(momentum=TeamMomentum.CRISIS, consecutive_losses=2, coach_change_days=15),
     "away": ContextData(momentum=TeamMomentum.STABLE)},
    {"home": ContextData(momentum=TeamMomentum.STABLE),
     "away": ContextData(momentum=TeamMomentum.STABLE, away_resilience=0.2)},
    {"home": ContextData(momentum=TeamMomentum.STABLE, ex_players_in_opponent=2),
     "away": ContextData(momentum=TeamMomentum.STABLE)},
    {"home": ContextData(momentum=TeamMomentum.STABLE),
     "away": ContextData(momentum=TeamMomentum.NEW_COACH, coach_change_days=3)},
    {"home": ContextData(momentum=TeamMomentum.STABLE),
     "away": ContextData(momentum=TeamMomentum.STABLE)},
    {"home": ContextData(momentum=TeamMomentum.STABLE, is_six_pointer=True),
     "away": ContextData(momentum=TeamMomentum.STABLE, is_six_pointer=True)},
    {"home": ContextData(momentum=TeamMomentum.STABLE),
     "away": ContextData(momentum=TeamMomentum.STABLE, away_resilience=0.3)},
]

HEAD_TO_HEAD_DATA = [
    {"home_wins": 45, "draws": 22, "away_wins": 38},   # Fla x Pal
    {"home_wins": 18, "draws": 15, "away_wins": 12},   # Bot x CAM
    {"home_wins": 40, "draws": 25, "away_wins": 30},   # SAO x FLU
    {"home_wins": 55, "draws": 30, "away_wins": 50},   # INT x GRE (Grenal)
    {"home_wins": 35, "draws": 20, "away_wins": 28},   # COR x CRU
    {"home_wins": 12, "draws": 8, "away_wins": 10},    # BAH x VAS
    {"home_wins": 8, "draws": 6, "away_wins": 5},      # FOR x CAP
    {"home_wins": 10, "draws": 7, "away_wins": 8},     # SAN x BRA
    {"home_wins": 5, "draws": 4, "away_wins": 3},      # JUV x CUI
    {"home_wins": 6, "draws": 4, "away_wins": 5},      # VIT x SPO
    {"home_wins": 3, "draws": 2, "away_wins": 2},      # CRI x MIR
    {"home_wins": 8, "draws": 5, "away_wins": 6},      # CEA x CFC
    {"home_wins": 7, "draws": 5, "away_wins": 4},      # GOI x AME
    {"home_wins": 12, "draws": 8, "away_wins": 10},    # PON x GUA
]


VENUES = [
    "Maracanã, Rio de Janeiro",
    "Estádio Nilton Santos, Rio de Janeiro",
    "Morumbi, São Paulo",
    "Beira-Rio, Porto Alegre",
    "Neo Química Arena, São Paulo",
    "Arena Fonte Nova, Salvador",
    "Arena Castelão, Fortaleza",
    "Vila Belmiro, Santos",
    "Alfredo Jaconi, Caxias do Sul",
    "Barradão, Salvador",
    "Heriberto Hülse, Criciúma",
    "Arena Castelão, Fortaleza",
    "Hailé Pinheiro, Goiânia",
    "Moisés Lucarelli, Campinas",
]


def _build_team_mock(name: str) -> TeamData:
    """Build TeamData from profile."""
    profile = TEAM_PROFILES.get(name, TEAM_PROFILES["Guarani"])
    abbrev = name[:3].upper()
    return TeamData(
        name=name,
        abbreviation=abbrev,
        xg_accumulated=profile["xg"],
        vertical_passes_avg=profile["vp"],
        box_entries_avg=profile["be"],
        counter_attack_efficiency=profile["ca"],
        clean_sheet_rate=profile["cs"],
        form_last_5=profile["form"],
    )


async def get_current_matches() -> list[MatchData]:
    """
    Orchestrator: Priority 1 - Read from concurso.json (Manual Weekly Grid)
    Priority 2 - Try to enrich these teams with Real API Data
    Priority 3 - Fallback to Team Profiles (Mock)
    """
    manual_grid = []
    if os.path.exists(CONCURSO_FILE):
        try:
            with open(CONCURSO_FILE, "r", encoding="utf-8") as f:
                manual_grid = json.load(f)
        except Exception as e:
            print(f"[DataService] Erro ao ler concurso.json: {e}")

    if not manual_grid or len(manual_grid) < 14:
        print("[DataService] concurso.json vazio ou incompleto. Usando grade padrão.")
        manual_grid = MOCK_MATCHDAY

    try:
        # Pre-fetch ALL real matches for current Brasileirão rounds
        # This helps us "resolve" the teams in our manual grid
        all_real_matches = await football_api.fetch_real_matches()
        real_lookup = {}
        for m in all_real_matches:
            # Simple lookup keys
            real_lookup[m.home_team.name.lower()] = m
            real_lookup[m.away_team.name.lower()] = m
        
        matches = []
        for i, (home_name, away_name) in enumerate(manual_grid):
            # Try to find this game in real data
            resolved_match = None
            h_low, a_low = home_name.lower(), away_name.lower()
            
            # Check if any real match contains these teams
            for m in all_real_matches:
                if (m.home_team.name.lower() == h_low and m.away_team.name.lower() == a_low) or \
                   (m.home_team.name.lower() == a_low and m.away_team.name.lower() == h_low):
                    resolved_match = m
                    break
            
            if resolved_match:
                # Use real data but preserve the manual ID (1-14)
                match = resolved_match.model_copy()
                match.id = i + 1
                matches.append(match)
            else:
                # Use mock profile for this specific pair
                matches.append(_build_manual_match(i + 1, home_name, away_name))
        
        print(f"[DataService] Grade de 14 jogos carregada (Manual + API Enrichment) 🚀")
        return matches

    except Exception as e:
        print(f"[DataService] API Error during enrichment: {e}. Servindo grade manual pura.")
        return [_build_manual_match(i + 1, h, a) for i, (h, a) in enumerate(manual_grid)]


def _build_manual_match(id: int, home_name: str, away_name: str) -> MatchData:
    """Build a match from team names using local profiles (Fallback)."""
    return MatchData(
        id=id,
        round_number=10, # Current competition round
        competition="Loteca (Official Selection)",
        home_team=_build_team_mock(home_name),
        away_team=_build_team_mock(away_name),
        home_context=ContextData(), # Default context for manual grid
        away_context=ContextData(),
        venue="Estádio Nacional",
        kickoff_time=f"2026-04-06T16:00:00-03:00",
        head_to_head={"home_wins": 5, "draws": 3, "away_wins": 3},
    )


def _generate_mock_matches() -> list[MatchData]:
    """Retorna os 14 jogos mockados originais."""
    # (Obsoleto, agora usamos _build_manual_match loop)
    return [_build_manual_match(i+1, h, a) for i, (h, a) in enumerate(MOCK_MATCHDAY)]
