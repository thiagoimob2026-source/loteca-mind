"""
Agente Estrategista — O Otimizador de Bolso
Transforms fusion results into optimal Loteca ticket suggestions.
Optimizes for a target budget of R$ 49.90.
"""

import math
from app.models.prediction import FusionResult, TicketSuggestion, StrategistOutput


# Loteca pricing: base cost per combination
LOTECA_BASE_BET = 4.00  # R$ per simple bet (14 simples)


def _classify_bet(confidence: float, fusion: FusionResult) -> tuple[list[str], str]:
    """
    Classify how many columns to bet based on confidence.

    Rules:
    - confidence > 0.70: simples (1 column)
    - 0.45 <= confidence <= 0.70: duplo (2 columns)
    - confidence < 0.45: triplo (3 columns)
    """
    probs = [
        ("1", fusion.home_win_prob),
        ("X", fusion.draw_prob),
        ("2", fusion.away_win_prob),
    ]
    # Sort by probability descending
    probs.sort(key=lambda x: x[1], reverse=True)

    if confidence > 0.70:
        return [probs[0][0]], "simples"
    elif confidence >= 0.45:
        return [probs[0][0], probs[1][0]], "duplo"
    else:
        return ["1", "X", "2"], "triplo"


def optimize(fusions: list[FusionResult], target_budget: float = 49.90) -> StrategistOutput:
    """
    Generate optimal Loteca ticket.

    Algorithm:
    1. Classify each match by confidence
    2. Calculate total combinations
    3. If over budget, convert weakest duplos to simples
    4. If under budget, convert strongest simples to duplos
    """
    # Step 1: Initial classification
    suggestions = []
    for fusion in fusions:
        columns, bet_type = _classify_bet(fusion.overall_confidence, fusion)
        suggestions.append(TicketSuggestion(
            match_id=fusion.match_id,
            home_team=fusion.home_team,
            away_team=fusion.away_team,
            columns=columns,
            bet_type=bet_type,
            confidence=fusion.overall_confidence,
            reason_score=fusion.reason_score,
            emotion_score=fusion.emotion_score,
        ))

    # Step 2: Calculate combinations
    def calc_combinations(sugs):
        result = 1
        for s in sugs:
            result *= len(s.columns)
        return result

    total_combos = calc_combinations(suggestions)
    ticket_cost = total_combos * LOTECA_BASE_BET

    # Step 3: Budget optimization
    max_iterations = 20
    iteration = 0

    while ticket_cost > target_budget * 1.2 and iteration < max_iterations:
        # Find the weakest duplo or triplo and downgrade
        candidates = [(i, s) for i, s in enumerate(suggestions)
                      if s.bet_type in ("duplo", "triplo")]
        if not candidates:
            break
        # Pick the one with highest confidence (safest to downgrade)
        candidates.sort(key=lambda x: x[1].confidence, reverse=True)
        idx, sug = candidates[0]

        if sug.bet_type == "triplo":
            # Downgrade to duplo
            probs = [
                ("1", fusions[idx].home_win_prob),
                ("X", fusions[idx].draw_prob),
                ("2", fusions[idx].away_win_prob),
            ]
            probs.sort(key=lambda x: x[1], reverse=True)
            suggestions[idx].columns = [probs[0][0], probs[1][0]]
            suggestions[idx].bet_type = "duplo"
        else:
            # Downgrade to simples
            probs = [
                ("1", fusions[idx].home_win_prob),
                ("X", fusions[idx].draw_prob),
                ("2", fusions[idx].away_win_prob),
            ]
            probs.sort(key=lambda x: x[1], reverse=True)
            suggestions[idx].columns = [probs[0][0]]
            suggestions[idx].bet_type = "simples"

        total_combos = calc_combinations(suggestions)
        ticket_cost = total_combos * LOTECA_BASE_BET
        iteration += 1

    while ticket_cost < target_budget * 0.6 and iteration < max_iterations:
        # Find the strongest simples and upgrade to duplo
        candidates = [(i, s) for i, s in enumerate(suggestions) if s.bet_type == "simples"]
        if not candidates:
            break
        # Pick the one with lowest confidence (most benefit from duplo)
        candidates.sort(key=lambda x: x[1].confidence)
        idx, sug = candidates[0]

        probs = [
            ("1", fusions[idx].home_win_prob),
            ("X", fusions[idx].draw_prob),
            ("2", fusions[idx].away_win_prob),
        ]
        probs.sort(key=lambda x: x[1], reverse=True)
        suggestions[idx].columns = [probs[0][0], probs[1][0]]
        suggestions[idx].bet_type = "duplo"

        new_combos = calc_combinations(suggestions)
        new_cost = new_combos * LOTECA_BASE_BET
        if new_cost > target_budget * 1.2:
            # Revert
            suggestions[idx].columns = [probs[0][0]]
            suggestions[idx].bet_type = "simples"
            break

        total_combos = new_combos
        ticket_cost = new_cost
        iteration += 1

    doubles_count = sum(1 for s in suggestions if s.bet_type == "duplo")
    triples_count = sum(1 for s in suggestions if s.bet_type == "triplo")

    return StrategistOutput(
        suggestions=suggestions,
        total_combinations=total_combos,
        ticket_cost=round(ticket_cost, 2),
        target_budget=target_budget,
        doubles_count=doubles_count,
        triples_count=triples_count,
    )
