from pydantic import BaseModel, Field
from typing import Optional


class AlphaOutput(BaseModel):
    """Output from Agent Alpha (Tactical Analyst)."""
    home_win_prob: float = Field(..., ge=0, le=1, description="Probabilidade vitória mandante")
    draw_prob: float = Field(..., ge=0, le=1, description="Probabilidade empate")
    away_win_prob: float = Field(..., ge=0, le=1, description="Probabilidade vitória visitante")
    confidence: float = Field(..., ge=0, le=1, description="Confiança na predição")
    key_factors: list[str] = Field(default_factory=list, description="Fatores técnicos determinantes")
    xg_differential: float = Field(0.0, description="Diferencial de xG entre times")


class PsiOutput(BaseModel):
    """Output from Agent Psi (Field Psychologist)."""
    home_volatility: float = Field(..., ge=0, le=100, description="Volatilidade emocional mandante (0-100)")
    away_volatility: float = Field(..., ge=0, le=100, description="Volatilidade emocional visitante (0-100)")
    match_volatility: float = Field(..., ge=0, le=100, description="Volatilidade geral do jogo (0-100)")
    emotional_factors: list[str] = Field(default_factory=list, description="Fatores emocionais detectados")
    zebra_alert: bool = Field(False, description="Alerta de zebra ativado")
    zebra_insight: Optional[str] = Field(None, description="Insight do Zebra Hunter")


class FusionResult(BaseModel):
    """Output from the Fusion Engine (Reason × Emotion)."""
    match_id: int
    home_team: str
    away_team: str

    # Adjusted probabilities
    home_win_prob: float = Field(..., ge=0, le=1)
    draw_prob: float = Field(..., ge=0, le=1)
    away_win_prob: float = Field(..., ge=0, le=1)

    # Balance Bar
    reason_score: float = Field(..., ge=0, le=100, description="Score de Razão (0-100)")
    emotion_score: float = Field(..., ge=0, le=100, description="Score de Emoção (0-100)")

    # Confidence & Suggestion
    overall_confidence: float = Field(..., ge=0, le=1)
    suggested_column: str = Field(..., description="Sugestão: '1', 'X', ou '2'")

    # Insights
    key_factors: list[str] = Field(default_factory=list)
    emotional_factors: list[str] = Field(default_factory=list)
    zebra_alert: bool = False
    zebra_insight: Optional[str] = None

    # Temperature
    home_temperature: str = Field("stable", description="on_fire | stable | cold")
    away_temperature: str = Field("stable", description="on_fire | stable | cold")

    # Clutch Factor
    clutch_factor: float = Field(0.5, ge=0, le=1, description="Fator decisivo do jogo")


class TicketSuggestion(BaseModel):
    """Suggestion for a single match in the ticket."""
    match_id: int
    home_team: str
    away_team: str
    columns: list[str] = Field(..., description="Colunas sugeridas: ['1'], ['1','X'], ['1','X','2']")
    bet_type: str = Field(..., description="simples | duplo | triplo")
    confidence: float = Field(..., ge=0, le=1)
    reason_score: float = Field(0, ge=0, le=100)
    emotion_score: float = Field(0, ge=0, le=100)


class StrategistOutput(BaseModel):
    """Output from Agent Strategist (Pocket Optimizer)."""
    suggestions: list[TicketSuggestion] = Field(..., description="14 sugestões")
    total_combinations: int = Field(..., description="Total de combinações")
    ticket_cost: float = Field(..., description="Custo estimado do ticket (R$)")
    target_budget: float = Field(49.90, description="Budget target")
    doubles_count: int = Field(0, description="Número de duplos")
    triples_count: int = Field(0, description="Número de triplos")
    expected_roi: Optional[float] = Field(None, description="ROI esperado")


class LotecaPrediction(BaseModel):
    """Complete prediction for the 14-game Loteca grid."""
    round_number: int
    competition: str = "Loteca"
    fusions: list[FusionResult] = Field(..., description="14 resultados de fusão")
    strategy: StrategistOutput
    analysis_summary: Optional[str] = Field(None, description="Resumo textual da análise (by Gemini)")
    generated_at: str = Field(..., description="Timestamp ISO")
