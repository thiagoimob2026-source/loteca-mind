"""
Motor de Fusão — Razão × Emoção
Crosses Alpha (tactical) output with Psi (psychological) output.
Produces adjusted probabilities and the Balance Bar.
"""

from app.models.match import MatchData, TeamMomentum
from app.models.prediction import AlphaOutput, PsiOutput, FusionResult


def fuse(match: MatchData, alpha: AlphaOutput, psi: PsiOutput) -> FusionResult:
    """
    Fuse tactical and emotional analysis.

    Logic:
    - If volatility > 60: emotional factors increase weight (max 40%)
    - If volatility < 30: pure statistics dominate (emotion weight ~10%)
    - Middle ground: balanced 75% reason, 25% emotion
    """
    vol = psi.match_volatility

    # Dynamic weight allocation
    if vol > 60:
        emotion_weight = 0.25 + (vol - 60) * 0.004  # Up to 0.41
    elif vol < 30:
        emotion_weight = 0.10
    else:
        emotion_weight = 0.15 + (vol - 30) * 0.003  # 0.15 to 0.24

    emotion_weight = min(0.45, emotion_weight)
    reason_weight = 1 - emotion_weight

    # Calculate emotion-based probability adjustments
    # High home volatility = less reliable for home team
    home_emotion_adj = 0.0
    away_emotion_adj = 0.0

    if psi.home_volatility > 50:
        home_emotion_adj = -(psi.home_volatility - 50) * 0.003
    elif psi.home_volatility < 20:
        home_emotion_adj = (20 - psi.home_volatility) * 0.002

    if psi.away_volatility > 50:
        away_emotion_adj = -(psi.away_volatility - 50) * 0.003
    elif psi.away_volatility < 20:
        away_emotion_adj = (20 - psi.away_volatility) * 0.002

    # Adjusted probabilities
    adj_home = alpha.home_win_prob * reason_weight + (alpha.home_win_prob + home_emotion_adj) * emotion_weight
    adj_away = alpha.away_win_prob * reason_weight + (alpha.away_win_prob + away_emotion_adj) * emotion_weight
    adj_draw = 1.0 - adj_home - adj_away

    # Ensure valid range
    adj_home = max(0.05, min(0.90, adj_home))
    adj_away = max(0.05, min(0.90, adj_away))
    adj_draw = max(0.05, min(0.90, adj_draw))

    # Re-normalize
    total = adj_home + adj_draw + adj_away
    adj_home = round(adj_home / total, 3)
    adj_draw = round(adj_draw / total, 3)
    adj_away = round(adj_away / total, 3)

    # Balance Bar (0-100 each)
    reason_score = round(reason_weight * 100, 1)
    emotion_score = round(emotion_weight * 100, 1)

    # Overall confidence
    max_prob = max(adj_home, adj_draw, adj_away)
    vol_penalty = vol * 0.003
    overall_confidence = round(max(0.15, min(0.95, alpha.confidence - vol_penalty)), 3)

    # Suggested column
    if adj_home >= adj_draw and adj_home >= adj_away:
        suggested_column = "1"
    elif adj_away >= adj_draw:
        suggested_column = "2"
    else:
        suggested_column = "X"

    # Temperature assessment
    def assess_temp(ctx, form):
        if ctx.momentum == TeamMomentum.ON_FIRE:
            return "on_fire"
        if ctx.momentum == TeamMomentum.CRISIS or ctx.consecutive_losses >= 3:
            return "cold"
        wins = sum(1 for r in form if r == "W")
        if wins >= 4:
            return "on_fire"
        if wins <= 1:
            return "cold"
        return "stable"

    home_temp = assess_temp(match.home_context, match.home_team.form_last_5)
    away_temp = assess_temp(match.away_context, match.away_team.form_last_5)

    # Clutch factor
    clutch = 0.5
    if match.home_context.is_six_pointer or match.away_context.is_six_pointer:
        clutch = 0.8
    if vol > 60:
        clutch = min(1.0, clutch + 0.15)

    return FusionResult(
        match_id=match.id,
        home_team=match.home_team.name,
        away_team=match.away_team.name,
        home_win_prob=adj_home,
        draw_prob=adj_draw,
        away_win_prob=adj_away,
        reason_score=reason_score,
        emotion_score=emotion_score,
        overall_confidence=overall_confidence,
        suggested_column=suggested_column,
        key_factors=alpha.key_factors,
        emotional_factors=psi.emotional_factors,
        zebra_alert=psi.zebra_alert,
        zebra_insight=psi.zebra_insight,
        home_temperature=home_temp,
        away_temperature=away_temp,
        clutch_factor=round(clutch, 2),
    )
