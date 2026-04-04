"""
Agente Alpha — O Analista Tático
Based on Bai et al. (2021) and Plakias (2024).

Analyzes technical/statistical factors to produce match probabilities.
Uses pure algorithmic logic (no LLM calls) for cost efficiency.
"""

from app.models.match import MatchData
from app.models.prediction import AlphaOutput


# Calibratable weights (will be adjusted by calibration service)
WEIGHTS = {
    "xg_differential": 0.40,
    "vertical_passes": 0.15,
    "box_entries": 0.15,
    "counter_attack": 0.10,
    "clean_sheet": 0.10,
    "form": 0.10,
}


def _form_score(form: list[str]) -> float:
    """Convert W/D/L form to a 0-1 score."""
    points = {"W": 3, "D": 1, "L": 0}
    if not form:
        return 0.5
    total = sum(points.get(r, 0) for r in form)
    max_possible = len(form) * 3
    return total / max_possible


def _normalize_probs(home: float, draw: float, away: float) -> tuple[float, float, float]:
    """Normalize probabilities to sum to 1.0."""
    total = home + draw + away
    if total == 0:
        return (0.33, 0.34, 0.33)
    return (round(home / total, 3), round(draw / total, 3), round(away / total, 3))


def analyze(match: MatchData) -> AlphaOutput:
    """
    Produce tactical probabilities for a match.

    Algorithm:
    1. Calculate raw strength from xG, passes, entries, counter-attacks
    2. Apply form modifier
    3. Add home advantage bias (+8%)
    4. Normalize to probabilities
    """
    home = match.home_team
    away = match.away_team
    factors = []

    # 1. xG Differential (most important factor)
    xg_diff = home.xg_accumulated - away.xg_accumulated
    xg_score = max(0, min(1, 0.5 + xg_diff * 0.15))
    factors.append(f"xG Diff: {xg_diff:+.2f} ({'mandante' if xg_diff > 0 else 'visitante'} advantage)")

    # 2. Vertical passes + Box entries (attacking intent)
    home_attack = (home.vertical_passes_avg * 0.4 + home.box_entries_avg * 0.6) / 30
    away_attack = (away.vertical_passes_avg * 0.4 + away.box_entries_avg * 0.6) / 30
    attack_diff = home_attack - away_attack
    attack_score = max(0, min(1, 0.5 + attack_diff * 0.5))

    if abs(attack_diff) > 0.1:
        factors.append(f"Pressão ofensiva: {'mandante' if attack_diff > 0 else 'visitante'} domina as entradas na área")

    # 3. Counter-attack efficiency
    ca_diff = home.counter_attack_efficiency - away.counter_attack_efficiency
    ca_score = max(0, min(1, 0.5 + ca_diff * 0.5))

    if abs(ca_diff) > 0.1:
        factors.append(f"Contra-ataque: {'mandante' if ca_diff > 0 else 'visitante'} mais letal")

    # 4. Clean sheet rate (defensive strength)
    cs_diff = home.clean_sheet_rate - away.clean_sheet_rate
    cs_score = max(0, min(1, 0.5 + cs_diff * 0.5))

    # 5. Form
    home_form = _form_score(home.form_last_5)
    away_form = _form_score(away.form_last_5)
    form_diff = home_form - away_form
    form_score = max(0, min(1, 0.5 + form_diff * 0.5))

    if abs(form_diff) > 0.2:
        factors.append(f"Momento: {'mandante' if form_diff > 0 else 'visitante'} em melhor fase")

    # Composite score (0 = strong away, 0.5 = even, 1 = strong home)
    composite = (
        WEIGHTS["xg_differential"] * xg_score +
        WEIGHTS["vertical_passes"] * attack_score +
        WEIGHTS["box_entries"] * attack_score +
        WEIGHTS["counter_attack"] * ca_score +
        WEIGHTS["clean_sheet"] * cs_score +
        WEIGHTS["form"] * form_score
    )

    # Home advantage bias (+8%)
    composite = min(1, composite + 0.08)

    # Convert to probabilities
    if composite > 0.6:
        raw_home = 0.35 + (composite - 0.5) * 0.8
        raw_draw = 0.25 - (composite - 0.5) * 0.2
        raw_away = 1 - raw_home - raw_draw
    elif composite < 0.4:
        raw_away = 0.35 + (0.5 - composite) * 0.8
        raw_draw = 0.25 - (0.5 - composite) * 0.2
        raw_home = 1 - raw_away - raw_draw
    else:
        raw_draw = 0.30 + (0.5 - abs(composite - 0.5)) * 0.3
        raw_home = (1 - raw_draw) * (0.5 + (composite - 0.5) * 1.5)
        raw_away = 1 - raw_draw - raw_home

    # Ensure valid probabilities
    raw_home = max(0.05, raw_home)
    raw_draw = max(0.05, raw_draw)
    raw_away = max(0.05, raw_away)

    home_prob, draw_prob, away_prob = _normalize_probs(raw_home, raw_draw, raw_away)

    # Confidence based on how decisive the data is
    max_prob = max(home_prob, draw_prob, away_prob)
    confidence = min(0.95, max_prob + abs(xg_diff) * 0.05)

    # Head-to-head factor
    h2h = match.head_to_head
    total_h2h = h2h.get("home_wins", 0) + h2h.get("draws", 0) + h2h.get("away_wins", 0)
    if total_h2h > 0:
        h2h_home_rate = h2h.get("home_wins", 0) / total_h2h
        if h2h_home_rate > 0.6:
            factors.append(f"Histórico: mandante domina confronto direto ({h2h.get('home_wins', 0)} vitórias)")
        elif h2h_home_rate < 0.3:
            factors.append(f"Histórico: visitante domina confronto direto ({h2h.get('away_wins', 0)} vitórias)")

    return AlphaOutput(
        home_win_prob=home_prob,
        draw_prob=draw_prob,
        away_win_prob=away_prob,
        confidence=round(confidence, 3),
        key_factors=factors,
        xg_differential=round(xg_diff, 2),
    )
