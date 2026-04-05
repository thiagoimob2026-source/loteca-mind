"""
Gemini Service — O Analista Silencioso do Loteca Mind.
Gera narrativas premium baseadas nos dados dos agentes Alpha e Psi.
"""

import os
import json
from typing import Optional, List, Dict
from google import genai
from app.models.match import MatchData
from pydantic import BaseModel
from app.config import get_settings

settings = get_settings()

client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"[GeminiService] Erro ao inicializar cliente: {e}")

class MatchInsightSchema(BaseModel):
    technical_summary: List[str]
    emotional_narrative: str
    zebra_hunter_verdict: Optional[str]
    deep_analysis: str # New field for detailed narrative

SYSTEM_PROMPT = """
Você é o "Analista Sênior do Loteca Mind", um comentarista esportivo renomado que une estatística avançada com psicologia de vestiário. 
Sua função é gerar insights para um portal de análise da Loteca.

PERSONALIDADE:
- Especialista do Brasileirão.
- Fala de "xG", "Lei do Ex", "Tabus históricos" e "Pressão da torcida".
- Estilo: Jornalismo esportivo moderno (ex: ESPN ou Globo Esporte).
- Idioma: Português do Brasil.

INSTRUÇÕES:
1. Retorne sempre o JSON solicitado.
2. deep_analysis: um parágrafo envolvente (3-4 frases) conectando os dados táticos, o histórico de confrontos (H2H) e o local da partida.
3. technical_summary: máximo de 3 bullet points técnicos.
4. emotional_narrative: foco no "feeling" dos times (crise vs empolgação).
"""

async def generate_match_analysis(
    match: MatchData,
    alpha_data: Dict,
    psi_data: Dict
) -> Optional[Dict]:
    """
    Gera análise textual usando o contexto real da partida.
    """
    if not client:
        return None

    h2h = match.head_to_head
    context_prompt = f"""
    ANALISE ESTA PARTIDA: {match.home_team.name} vs {match.away_team.name}
    Local: {match.venue}
    Competição: {match.competition}
    
    HISTÓRICO H2H:
    - Vitórias {match.home_team.name}: {h2h.get('home_wins', 0)}
    - Vitórias {match.away_team.name}: {h2h.get('away_wins', 0)}
    - Empates: {h2h.get('draws', 0)}
    
    DADOS QUANTITATIVOS (Alpha):
    - Probabilidades: {alpha_data.get('home_win_prob')} / {alpha_data.get('draw_prob')} / {alpha_data.get('away_win_prob')}
    - xG Diff: {alpha_data.get('xg_differential')}
    
    DADOS QUALITATIVOS (Psi):
    - Volatilidade: {psi_data.get('match_volatility')}/100
    - Alerta Zebra: {psi_data.get('zebra_alert')}
    - Fatores: {psi_data.get('emotional_factors')}
    """

    import time
    models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash"]
    
    for model_name in models_to_try:
        max_retries = 2
        retry_delay = 30

        for attempt in range(max_retries):
            try:
                print(f"[GeminiService] Tentando análise com {model_name}...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=context_prompt,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "response_mime_type": "application/json",
                        "response_schema": MatchInsightSchema,
                    }
                )
                
                if response.text:
                    return json.loads(response.text)
                
            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str:
                    print(f"[GeminiService] Rate limit no {model_name}. Aguardando {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                elif "404" in error_str:
                    print(f"[GeminiService] Modelo {model_name} não encontrado. Pulando...")
                    break # Try next model
                
                print(f"[GeminiService] Erro inesperado no {model_name}: {e}")
                break # Try next model
                
    return None

def get_placeholder_insights(match_name: str, zebra_alert: bool) -> Dict:
    return {
        "technical_summary": ["Análise baseada em volume histórico."],
        "emotional_narrative": "Equilíbrio emocional esperado.",
        "zebra_hunter_verdict": None,
        "deep_analysis": f"Confronto equilibrado no estádio. A estatística sugere um jogo estratégico entre {match_name}."
    }
