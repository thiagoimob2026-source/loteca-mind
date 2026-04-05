"""
Football Data Service — Integração com API-Football (api-sports.io)

Tier grátis: 100 requests/dia, 10 req/min.
Brasileirão Série A league_id = 71
"""

import httpx
import os
from typing import Optional
from datetime import datetime, timedelta
from app.models.match import TeamData, ContextData, MatchData

API_KEY = os.getenv("FOOTBALL_API_KEY", "")
API_HOST = os.getenv("FOOTBALL_API_HOST", "v3.football.api-sports.io")
BASE_URL = f"https://{API_HOST}"
BRASILEIRAO_LEAGUE_ID = 71
CURRENT_SEASON = 2026

# Cache simples em memória para economizar requests
_cache: dict = {}
_cache_ttl: dict = {}
CACHE_DURATION = timedelta(hours=2)


def _is_cached(key: str) -> bool:
    if key in _cache and key in _cache_ttl:
        return datetime.now() < _cache_ttl[key]
    return False


async def _api_request(endpoint: str, params: dict = {}) -> Optional[dict]:
    """Faz request à API-Football com cache."""
    cache_key = f"{endpoint}:{str(params)}"

    if _is_cached(cache_key):
        return _cache[cache_key]

    if not API_KEY:
        return None

    headers = {
        "x-apisports-key": API_KEY,
        "x-apisports-host": API_HOST,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(
                f"{BASE_URL}/{endpoint}",
                headers=headers,
                params=params,
            )
            resp.raise_for_status()
            data = resp.json()

            # Cache result
            _cache[cache_key] = data
            _cache_ttl[cache_key] = datetime.now() + CACHE_DURATION

            return data
        except Exception as e:
            print(f"[FootballAPI] Error: {e}")
            return None


async def get_current_round() -> Optional[int]:
    """Retorna a rodada atual do Brasileirão."""
    data = await _api_request("fixtures/rounds", {
        "league": BRASILEIRAO_LEAGUE_ID,
        "season": CURRENT_SEASON,
        "current": "true",
    })
    if data and data.get("response"):
        # Format: "Regular Season - 10"
        round_str = data["response"][0]
        try:
            return int(round_str.split(" - ")[1])
        except (IndexError, ValueError):
            return None
    return None


async def get_fixtures_by_round(round_number: int) -> list[dict]:
    """Retorna jogos de uma rodada específica."""
    data = await _api_request("fixtures", {
        "league": BRASILEIRAO_LEAGUE_ID,
        "season": CURRENT_SEASON,
        "round": f"Regular Season - {round_number}",
    })
    if data and data.get("response"):
        return data["response"]
    return []


async def get_team_statistics(team_id: int) -> Optional[dict]:
    """Retorna estatísticas do time na temporada."""
    data = await _api_request("teams/statistics", {
        "league": BRASILEIRAO_LEAGUE_ID,
        "season": CURRENT_SEASON,
        "team": team_id,
    })
    if data and data.get("response"):
        return data["response"]
    return None


async def get_team_form(team_id: int, last: int = 5) -> list[str]:
    """Retorna últimos resultados do time (W/D/L)."""
    data = await _api_request("fixtures", {
        "team": team_id,
        "last": last,
    })
    if not data or not data.get("response"):
        return ["D"] * last

    form = []
    for fixture in data["response"]:
        home_id = fixture["teams"]["home"]["id"]
        home_goals = fixture["goals"]["home"] or 0
        away_goals = fixture["goals"]["away"] or 0

        if team_id == home_id:
            if home_goals > away_goals:
                form.append("W")
            elif home_goals < away_goals:
                form.append("L")
            else:
                form.append("D")
        else:
            if away_goals > home_goals:
                form.append("W")
            elif away_goals < home_goals:
                form.append("L")
            else:
                form.append("D")

    return form[:last]


async def get_head_to_head(home_id: int, away_id: int, last: int = 10) -> dict:
    """Retorna histórico de confrontos."""
    data = await _api_request("fixtures/headtohead", {
        "h2h": f"{home_id}-{away_id}",
        "last": last,
    })
    h2h = {"home_wins": 0, "draws": 0, "away_wins": 0}
    if not data or not data.get("response"):
        return h2h

    for fixture in data["response"]:
        hg = fixture["goals"]["home"] or 0
        ag = fixture["goals"]["away"] or 0
        fh = fixture["teams"]["home"]["id"]

        if hg == ag:
            h2h["draws"] += 1
        elif (fh == home_id and hg > ag) or (fh == away_id and ag > hg):
            h2h["home_wins"] += 1
        else:
            h2h["away_wins"] += 1

    return h2h


def _build_team_data(team_info: dict, stats: Optional[dict], form: list[str]) -> TeamData:
    """Constrói TeamData a partir dos dados da API."""
    if stats:
        goals_for = stats.get("goals", {}).get("for", {}).get("average", {}).get("total", "1.2")
        clean_sheets = stats.get("clean_sheet", {}).get("total", 3)
        played = stats.get("fixtures", {}).get("played", {}).get("total", 10)
        cs_rate = clean_sheets / max(played, 1)
    else:
        goals_for = "1.2"
        cs_rate = 0.25

    return TeamData(
        name=team_info.get("name", "Unknown"),
        abbreviation=team_info.get("code", "UNK"),
        xg_accumulated=float(goals_for) * 1.05,  # Approximation
        vertical_passes_avg=round(12 + float(goals_for) * 3, 1),
        box_entries_avg=round(8 + float(goals_for) * 4, 1),
        counter_attack_efficiency=round(0.15 + float(goals_for) * 0.05, 2),
        clean_sheet_rate=round(cs_rate, 2),
        form_last_5=form,
    )


def _build_context(form: list[str]) -> ContextData:
    """Constrói ContextData baseado na forma recente."""
    losses = form.count("L")
    wins = form.count("W")

    if losses >= 3:
        momentum = "crisis"
    elif wins >= 4:
        momentum = "on_fire"
    else:
        momentum = "stable"

    return ContextData(
        momentum=momentum,
        coach_change_days=None,
        var_incidents_last_5=1,
        ex_players_in_opponent=0,
        away_resilience=0.5,
        consecutive_losses=losses,
        is_six_pointer=False,
        recent_news_sentiment=0.0,
    )


async def fetch_real_matches(round_number: Optional[int] = None) -> list[MatchData]:
    """
    Busca jogos reais do Brasileirão via API-Football.
    Se API_KEY não estiver configurada, retorna lista vazia (fallback para mock).
    """
    if not API_KEY:
        return []

    if round_number is None:
        round_number = await get_current_round()
        if round_number is None:
            return []

    fixtures = await get_fixtures_by_round(round_number)
    if not fixtures:
        return []

    matches = []
    for i, fixture in enumerate(fixtures, 1):
        home_info = fixture["teams"]["home"]
        away_info = fixture["teams"]["away"]
        home_id = home_info["id"]
        away_id = away_info["id"]

        # Fetch team data in parallel-ish fashion
        home_stats = await get_team_statistics(home_id)
        away_stats = await get_team_statistics(away_id)
        home_form = await get_team_form(home_id)
        away_form = await get_team_form(away_id)
        h2h = await get_head_to_head(home_id, away_id)

        venue_name = fixture.get("fixture", {}).get("venue", {}).get("name", "Estádio")
        kickoff = fixture.get("fixture", {}).get("date")

        match = MatchData(
            id=i,
            round_number=round_number,
            competition="Brasileirão Série A",
            home_team=_build_team_data(home_info, home_stats, home_form),
            away_team=_build_team_data(away_info, away_stats, away_form),
            home_context=_build_context(home_form),
            away_context=_build_context(away_form),
            venue=venue_name,
            kickoff_time=kickoff,
            head_to_head=h2h,
        )
        matches.append(match)

    return matches
