"""
Agente Psi — O Psicólogo de Campo
Based on Ivarsson (2019) and Kaplánová (2024).

Analyzes psychological and emotional factors that can destabilize predictions.
Uses pure algorithmic logic (no LLM calls).
"""

from app.models.match import MatchData, ContextData, TeamMomentum
from app.models.prediction import PsiOutput


# Emotional factor weights (calibratable)
FACTOR_WEIGHTS = {
    "new_coach_bonus": 15,      # "Novo Ar" effect
    "consecutive_losses": 7,    # Per consecutive loss
    "var_stress": 4,            # Per VAR incident
    "ex_player_effect": 5,      # "Lei do Ex"
    "away_fragility": 10,       # Low away resilience
    "six_pointer_pressure": 12, # High-stakes match
    "negative_news": 8,         # Negative media sentiment
    "crisis_momentum": 20,      # Team in crisis
    "on_fire_stability": -10,   # Team on fire (reduces volatility)
}


def _calculate_team_volatility(ctx: ContextData) -> tuple[float, list[str]]:
    """Calculate emotional volatility for a single team."""
    volatility = 25.0  # Base volatility
    factors = []

    # New coach effect ("Novo Ar")
    if ctx.coach_change_days is not None and ctx.coach_change_days <= 30:
        bonus = FACTOR_WEIGHTS["new_coach_bonus"]
        if ctx.coach_change_days <= 7:
            bonus *= 1.5  # Extra boost for very recent change
        volatility += bonus
        factors.append(f"🔄 Novo treinador ({ctx.coach_change_days} dias) — efeito 'Novo Ar' ativo")

    # Consecutive losses
    if ctx.consecutive_losses >= 3:
        penalty = ctx.consecutive_losses * FACTOR_WEIGHTS["consecutive_losses"]
        volatility += penalty
        factors.append(f"📉 Sequência de {ctx.consecutive_losses} derrotas — pressão máxima")
    elif ctx.consecutive_losses >= 2:
        volatility += FACTOR_WEIGHTS["consecutive_losses"] * 2
        factors.append(f"⚠️ {ctx.consecutive_losses} derrotas seguidas — alerta de crise")

    # VAR stress
    if ctx.var_incidents_last_5 >= 3:
        stress = ctx.var_incidents_last_5 * FACTOR_WEIGHTS["var_stress"]
        volatility += stress
        factors.append(f"📺 Stress do VAR: {ctx.var_incidents_last_5} incidentes recentes")

    # Ex-player effect ("Lei do Ex")
    if ctx.ex_players_in_opponent > 0:
        effect = ctx.ex_players_in_opponent * FACTOR_WEIGHTS["ex_player_effect"]
        volatility += effect
        factors.append(f"👤 Lei do Ex: {ctx.ex_players_in_opponent} ex-jogador(es) no adversário")

    # Away fragility
    if ctx.away_resilience < 0.3:
        volatility += FACTOR_WEIGHTS["away_fragility"]
        factors.append("✈️ Fragilidade fora de casa — resiliência baixa")

    # Six-pointer pressure
    if ctx.is_six_pointer:
        volatility += FACTOR_WEIGHTS["six_pointer_pressure"]
        factors.append("🎯 Jogo de 6 pontos — pressão extrema")

    # News sentiment
    if ctx.recent_news_sentiment < -0.3:
        penalty = abs(ctx.recent_news_sentiment) * FACTOR_WEIGHTS["negative_news"]
        volatility += penalty
        factors.append("📰 Notícias negativas no vestiário")

    # Momentum
    if ctx.momentum == TeamMomentum.CRISIS:
        volatility += FACTOR_WEIGHTS["crisis_momentum"]
        factors.append("🔴 Time em CRISE de momentum")
    elif ctx.momentum == TeamMomentum.ON_FIRE:
        volatility += FACTOR_WEIGHTS["on_fire_stability"]
        factors.append("🔥 Time ON FIRE — confiança elevada")
    elif ctx.momentum == TeamMomentum.NEW_COACH:
        volatility += FACTOR_WEIGHTS["new_coach_bonus"] * 0.5
        factors.append("🆕 Efeito de novo treinador em andamento")

    # Clamp to 0-100
    volatility = max(0, min(100, volatility))

    return round(volatility, 1), factors


def analyze(match: MatchData) -> PsiOutput:
    """
    Analyze emotional and psychological factors for both teams.

    Produces:
    - Individual team volatility scores
    - Combined match volatility
    - Zebra alert if volatility is high
    - Textual insight for Zebra Hunter widget
    """
    home_vol, home_factors = _calculate_team_volatility(match.home_context)
    away_vol, away_factors = _calculate_team_volatility(match.away_context)

    # Match volatility = weighted average (higher weight to the more volatile team)
    match_vol = round((home_vol * 0.45 + away_vol * 0.45 + abs(home_vol - away_vol) * 0.1), 1)
    match_vol = max(0, min(100, match_vol))

    # Combine factors
    all_factors = []
    if home_factors:
        all_factors.extend([f"🏠 {match.home_team.name}: {f}" for f in home_factors])
    if away_factors:
        all_factors.extend([f"✈️ {match.away_team.name}: {f}" for f in away_factors])

    # Zebra detection
    zebra_alert = match_vol > 55
    zebra_insight = None

    if zebra_alert:
        # Generate insight based on the strongest emotional factor
        if any("CRISE" in f for f in all_factors):
            zebra_insight = (
                f"⚡ ZEBRA HUNTER: A estatística pode favorecer um lado, mas o vestiário conta "
                f"outra história. Com crise de momentum, este jogo é imprevisível."
            )
        elif any("Novo treinador" in f for f in all_factors):
            zebra_insight = (
                f"⚡ ZEBRA HUNTER: Efeito 'Novo Ar' detectado! Troca recente de técnico "
                f"pode inverter expectativas. Cuidado com a zebra."
            )
        elif any("Lei do Ex" in f for f in all_factors):
            zebra_insight = (
                f"⚡ ZEBRA HUNTER: A 'Lei do Ex' está em jogo. Motivação extra do ex-jogador "
                f"pode ser o fator surpresa desta partida."
            )
        else:
            zebra_insight = (
                f"⚡ ZEBRA HUNTER: Volatilidade emocional alta ({match_vol:.0f}/100). "
                f"A emoção pode superar a razão neste confronto."
            )

    return PsiOutput(
        home_volatility=home_vol,
        away_volatility=away_vol,
        match_volatility=match_vol,
        emotional_factors=all_factors,
        zebra_alert=zebra_alert,
        zebra_insight=zebra_insight,
    )
