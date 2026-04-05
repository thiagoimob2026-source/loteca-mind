from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TeamMomentum(str, Enum):
    ON_FIRE = "on_fire"
    STABLE = "stable"
    CRISIS = "crisis"
    NEW_COACH = "new_coach"


class TeamData(BaseModel):
    """Core team statistics for a match."""
    name: str = "Unknown"
    abbreviation: str = "UNK"
    xg_accumulated: float = Field(0.0, description="Expected Goals acumulado últimos jogos")
    vertical_passes_avg: float = Field(0.0, description="Média de passes verticais por jogo")
    box_entries_avg: float = Field(0.0, description="Entradas na área adversária por jogo")
    counter_attack_efficiency: float = Field(0.5, ge=0, le=1, description="Eficácia de contra-ataques (0-1)")
    clean_sheet_rate: float = Field(0.0, ge=0, le=1, description="Taxa de jogos sem sofrer gols")
    form_last_5: list[str] = Field(default_factory=list, description="Resultados últimos 7 jogos (W/D/L)")
    clutch_factor: float = Field(0.5, ge=0, le=1, description="Fator Decisão (Gols no final)")


class ContextData(BaseModel):
    """Psychological and contextual factors."""
    momentum: TeamMomentum = TeamMomentum.STABLE
    coach_change_days: Optional[int] = Field(None, description="Dias desde troca de técnico")
    var_incidents_last_5: int = Field(0, description="Incidentes VAR nos últimos 5 jogos")
    ex_players_in_opponent: int = Field(0, description="Nº de ex-jogadores no adversário")
    away_resilience: float = Field(0.5, ge=0, le=1, description="Resiliência em jogos fora (0-1)")
    consecutive_losses: int = Field(0, description="Derrotas consecutivas")
    is_six_pointer: bool = Field(False, description="É um jogo de 6 pontos?")
    recent_news_sentiment: float = Field(0.0, ge=-1, le=1, description="Sentimento notícias (-1 a 1)")


class MatchData(BaseModel):
    """Complete match data for the 14-game grid."""
    id: int
    round_number: int
    competition: str = "Brasileirão Série A"
    home_team: TeamData
    away_team: TeamData
    home_context: ContextData = ContextData()
    away_context: ContextData = ContextData()
    venue: str = ""
    kickoff_time: Optional[str] = None
    head_to_head: dict = Field(default_factory=lambda: {"home_wins": 0, "draws": 0, "away_wins": 0})
    is_verified: bool = Field(False, description="Dados confirmados via API-Sports")
