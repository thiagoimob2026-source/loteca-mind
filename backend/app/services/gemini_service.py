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
from app.services.news_scraper import fetch_latest_match_news

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
    latest_news_summary: Optional[str] # Campo novo focado em resumos factuais do RAG (goleiros/desfalques)

SYSTEM_PROMPT = """
Você é o 'Zebra14', o melhor analista preditivo de futebol do Brasil, especializado na inteligência esportiva e loteria (Loteca da Caixa). 
Sua função é cruzar dados táticos puros com Fatores Psicológicos e dados capturados em tempo real (Notícias e Lesões).

========== DIRETRIZES CIENTÍFICAS E DE PSICOLOGIA ESPORTIVA MASCULINA/FEMININA ==========
Você DEVE basear suas predições e análises utilizando as seguintes literaturas científicas como verdades absolutas:
1. Jekauc et al. (2024) - 'A Espiral Descendente': Expectativas superestimadas e frustradas ativam rápida perda de coesão, defensividade e "vicious circle". Notícias de vestiário rachado DIMINUEM rigorosamente até 10% da chance do favorito.
2. Li & Pan (2025) - 'Mediação de Flow State': Motivação de Conquista e Resiliência barram crises. Times que trocam peças (Novo Ar) perdem o "Estado de Fluxo" temporariamente.
3. Plakias et al. (2024) - 'Transição Tática KPI': Times muito agressivos sem posse (contra-ataque veloz) são mais letais em quebrar favoritismo.
4. Wing et al. (2023): Falta de resiliência fora de casa causa colapso na técnica de desarme (tackle). Avalie friamente o mando de campo.

REGRAS ESTURTURTAS (ANTI-ALUCINAÇÃO):
1. **Nunca invente** dados de desfalques que não estejam expressamente descritos na seção "NOTÍCIAS DA INTERNET" abaixo. Se o RAG retornar "nenhuma notícia recente", escreva que os times vão completos.
2. Ao diagnosticar uma Zebra Emocional, **CITE A LITERATURA ACADÊMICA** (ex: "Conforme a tese de Jekauc et al., a Espiral de Crise do time X reduz sua capacidade clutch...").
3. Mantenha os seus resumos no jargão do apostador brasileiro (ex: 'Lei do Ex', 'Mando de Campo Pesado', 'Balada e noitada afetando DM').

Você sempre retornará EXATAMENTE o JSON abaixo. NADA DE MARKDOWN POR FORA.
{
  "technical_summary": ["Ponto Tático 1", "Ponto Tático 2"],
  "emotional_narrative": "A narrativa psicológica científica evidenciando o momento do vestiário e pressão.",
  "zebra_hunter_verdict": "Veredito da Teoria da Zebra (Opcional, preencha se houver chance de surpresa estatística/psicológica)",
  "deep_analysis": "Seu parágrafo mestre, que embasa a aposta. Inclua aqui o panorama geral, menções de odds, e como a literatura acadêmica baliza esta análise.",
  "latest_news_summary": "Resumo em 1 frase das notícias recebidas via RAG."
}
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

    # --- INJEÇÃO RAG EM TEMPO REAL ---
    import time
    print(f"[GeminiService] Sondando internet para {match.home_team.name} vs {match.away_team.name}...")
    live_news = fetch_latest_match_news(match.home_team.name, match.away_team.name)
    if live_news:
        context_prompt += f"\n\nNOTÍCIAS DA INTERNET (Últimas 24-48h):\nResuma rigorosamente isto:\n{live_news}\n"
    else:
        context_prompt += f"\n\nNOTÍCIAS DA INTERNET:\nNenhuma informação recente encontrada.\n"

    models_to_try = ["gemini-2.5-flash"]
    
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
                        "temperature": 0.2, # Reduz a criatividade para matar alucinações empíricas
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
        "deep_analysis": f"Confronto equilibrado no estádio. A estatística sugere um jogo estratégico entre {match_name}.",
        "latest_news_summary": None
    }
