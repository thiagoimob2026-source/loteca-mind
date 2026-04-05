"""
Agente Alpha — O Analista Tático (Motor Scout)
Real-time statistical engine for tactical probabilities.
"""

from app.models.match import MatchData
from app.models.prediction import AlphaOutput

# Pesos calibrados para dados REAIS
WEIGHTS = {
    "xg_differential": 0.45,
    "box_entries": 0.20,
    "clean_sheet": 0.15,
    "form": 0.20,
}

def _form_score(form: list[str]) -> float:
    """Calcula pontuação baseada nos últimos 7 jogos (conforme pedido)."""
    if not form: return 0.5
    points = {"W": 3, "D": 1, "L": 0}
    total = sum(points.get(r, 0) for r in form)
    return total / (len(form) * 3)

def _normalize_probs(home: float, draw: float, away: float) -> tuple[float, float, float]:
    total = home + draw + away
    if total == 0: return (0.33, 0.34, 0.33)
    return (round(home/total, 3), round(draw/total, 3), round(away/total, 3))

def analyze(match: MatchData) -> AlphaOutput:
    home, away = match.home_team, match.away_team
    factors = []

    # 1. xG Differential
    xg_diff = home.xg_accumulated - away.xg_accumulated
    xg_score = max(0, min(1, 0.5 + xg_diff * 0.2))
    if abs(xg_diff) > 0.3:
        factors.append(f"Superioridade em xG: {home.name if xg_diff > 0 else away.name} cria chances mais claras.")

    # 2. Volume Ofensivo (Box Entries)
    be_diff = home.box_entries_avg - away.box_entries_avg
    be_score = max(0, min(1, 0.5 + (be_diff / 10)))
    if abs(be_diff) > 3:
        factors.append(f"Volume de Jogo: {home.name if be_diff > 0 else away.name} frequenta mais a área adversária.")

    # 3. Solidez Defensiva
    cs_diff = home.clean_sheet_rate - away.clean_sheet_rate
    cs_score = max(0, min(1, 0.5 + cs_diff))

    # 4. Forma Recente (Janela de 7 jogos)
    home_f = _form_score(home.form_last_5)
    away_f = _form_score(away.form_last_5)
    form_diff = home_f - away_f
    form_score = max(0, min(1, 0.5 + form_diff))

    # Fator Decisão Tático (Clutch)
    match_clutch = (home.clutch_factor + away.clutch_factor) / 2

    # Cálculo Composto
    composite = (
        WEIGHTS["xg_differential"] * xg_score +
        WEIGHTS["box_entries"] * be_score +
        WEIGHTS["clean_sheet"] * cs_score +
        WEIGHTS["form"] * form_score
    )

    # Home Advantage (+10%)
    composite = min(1.0, composite + 0.10)

    # Mapping to Probs
    raw_home = 0.33 + (composite - 0.5) * 0.8
    raw_draw = 0.28 - abs(composite - 0.5) * 0.2
    raw_away = 1.0 - raw_home - raw_draw

    h_prob, d_prob, a_prob = _normalize_probs(max(0.05, raw_home), max(0.05, raw_draw), max(0.05, raw_away))

    return AlphaOutput(
        home_win_prob=h_prob,
        draw_prob=d_prob,
        away_win_prob=a_prob,
        confidence=round(0.6 + abs(composite - 0.5) * 0.4, 3),
        key_factors=factors,
        xg_differential=round(xg_diff, 2),
        clutch_factor=round(match_clutch, 2)
    )
