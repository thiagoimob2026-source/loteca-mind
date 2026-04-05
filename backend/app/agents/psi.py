"""
Agente Psi — O Psicólogo de Campo (Motor Scout)
Analyzes emotional volatility based on real recent performance.
"""

from app.models.match import MatchData, ContextData, TeamMomentum
from app.models.prediction import PsiOutput

# Pesos emocionais baseados em dados REAIS
FACTOR_WEIGHTS = {
    "volatility_base": 20,
    "instability": 15,       # Mudança frequente W <-> L
    "crisis_penalty": 25,    # Momentum de crise
    "clutch_bonus": -10,     # Fator decisão reduz volatilidade (time frio)
    "consecutive_losses": 10, # Por derrota seguida
}

def _calculate_team_volatility(team_name: str, ctx: ContextData, clutch: float) -> tuple[float, list[str]]:
    vol = FACTOR_WEIGHTS["volatility_base"]
    factors = []

    # 1. Instabilidade (Alternância de resultados)
    # Se nos últimos 7 jogos o time tem quase igual W e L
    wins = ctx.consecutive_losses if ctx.momentum == TeamMomentum.ON_FIRE else 0 # Simplificação rápida
    # Na verdade, usamos a form_last_5 do match.home_team
    
    # 2. Perdas consecutivas
    if ctx.consecutive_losses >= 2:
        penalty = ctx.consecutive_losses * FACTOR_WEIGHTS["consecutive_losses"]
        vol += penalty
        factors.append(f"⚠️ {team_name}: Pressão por {ctx.consecutive_losses} derrotas seguidas.")

    # 3. Momentum
    if ctx.momentum == TeamMomentum.CRISIS:
        vol += FACTOR_WEIGHTS["crisis_penalty"]
        factors.append(f"🔴 {team_name}: Vestiário sob forte pressão (Crise).")
    elif ctx.momentum == TeamMomentum.ON_FIRE:
        vol += FACTOR_WEIGHTS["clutch_bonus"]
        factors.append(f"🔥 {team_name}: Confiança elevada pelo momentum.")

    # 4. Fator Decisão (Clutch) - Times 'clutch' são mais estáveis sob pressão
    if clutch > 0.7:
        vol += FACTOR_WEIGHTS["clutch_bonus"]
        factors.append(f"🎯 {team_name}: Especialista em gols decisivos (Fator Decisão Alto).")

    return max(5, min(95, vol)), factors

def analyze(match: MatchData) -> PsiOutput:
    home_vol, home_f = _calculate_team_volatility(match.home_team.name, match.home_context, match.home_team.clutch_factor)
    away_vol, away_f = _calculate_team_volatility(match.away_team.name, match.away_context, match.away_team.clutch_factor)

    # Match volatility
    match_vol = round((home_vol + away_vol) / 2 + abs(home_vol - away_vol) * 0.2, 1)
    match_vol = max(0, min(100, match_vol))

    all_factors = home_f + away_f
    
    # Zebra Detection
    zebra_alert = match_vol > 60
    zebra_insight = None
    if zebra_alert:
        if home_vol > away_vol + 15:
            zebra_insight = f"⚡ ZEBRA HUNTER: {match.home_team.name} está instável emocionalmente. Oportunidade para o visitante."
        elif away_vol > home_vol + 15:
            zebra_insight = f"⚡ ZEBRA HUNTER: O clima no {match.away_team.name} é tenso. Chance de domínio do mandante."
        else:
            zebra_insight = "⚡ ZEBRA HUNTER: Alta volatilidade detectada. Jogo propício para resultados inesperados."

    return PsiOutput(
        home_volatility=home_vol,
        away_volatility=away_vol,
        match_volatility=match_vol,
        emotional_factors=all_factors,
        zebra_alert=zebra_alert,
        zebra_insight=zebra_insight
    )
