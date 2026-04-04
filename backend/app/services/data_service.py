"""
Data Service — Mock data for Phase 1.
Provides realistic match data for 14 games using real Brasileirão teams.
Will be replaced with real API data in Phase 2.
"""

import random
from app.models.match import MatchData, TeamData, ContextData, TeamMomentum


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


def _build_team(name: str) -> TeamData:
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


def get_current_matches() -> list[MatchData]:
    """Return the 14 mock matches for the current Loteca round."""
    matches = []

    for i, (home_name, away_name) in enumerate(MOCK_MATCHDAY):
        ctx = CONTEXT_SCENARIOS[i] if i < len(CONTEXT_SCENARIOS) else {"home": ContextData(), "away": ContextData()}
        h2h = HEAD_TO_HEAD_DATA[i] if i < len(HEAD_TO_HEAD_DATA) else {"home_wins": 5, "draws": 3, "away_wins": 4}
        venue = VENUES[i] if i < len(VENUES) else "Estádio"

        match = MatchData(
            id=i + 1,
            round_number=10,
            competition="Brasileirão Série A",
            home_team=_build_team(home_name),
            away_team=_build_team(away_name),
            home_context=ctx["home"],
            away_context=ctx["away"],
            venue=venue,
            kickoff_time=f"2026-04-06T{16 + (i % 4) * 2}:00:00-03:00",
            head_to_head=h2h,
        )
        matches.append(match)

    return matches
