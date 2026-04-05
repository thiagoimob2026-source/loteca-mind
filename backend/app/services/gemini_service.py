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

REGRAS ESTURTURTAS E PODER GRÁFICO (ANTI-ALUCINAÇÃO):
1. **Poder Absoluto das Barras (Reason/Emotion)**: Baseado na literatura acima, VOCÊ deciderá a pontuação final de Emoção (0 a 100) e Razão (0 a 100). Atenção: os dois DEVEM somar exatamente 100. Se houver crise brava ou pressão absurda de arquibancada com base nos dados/notícias, NÃO TENHA MEDO, coloque a Emoção entre 65 e 85. Se for um jogo frio, jogue a Razão para 80-90.
2. **Autoridade Caçador de Zebras**: Se você detectar clima para Zebra no item 1, você DEVE retornar a variável `trigger_zebra_alert` como `true`. O seu julgamento suplanta toda a matemática prévia do sistema.
3. Ao diagnosticar uma Zebra Emocional, **CITE A LITERATURA ACADÊMICA**.
4. **Nunca invente** dados de desfalques. Use os dados passados a você.

Você sempre retornará EXATAMENTE o JSON abaixo. NADA DE MARKDOWN POR FORA.
{
  "technical_summary": ["Ponto Tático 1", "Ponto Tático 2"],
  "emotional_narrative": "A narrativa psicológica científica evidenciando o momento do vestiário e pressão.",
  "zebra_hunter_verdict": "Veredito da Teoria da Zebra (Preencha sempre que trigger_zebra_alert for true)",
  "deep_analysis": "Seu parágrafo mestre, que embasa a aposta e como a literatura acadêmica guiou esta análise.",
  "latest_news_summary": "Resumo em 1 frase das notícias recebidas via RAG.",
  "reason_score_override": 70,
  "emotion_score_override": 30,
  "trigger_zebra_alert": false
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

    # --- INJEÇÃO RAG EM TEMPO REAL (Async Friendly) ---
    print(f"[GeminiService] Sondando internet para {match.home_team.name} vs {match.away_team.name}...")
    # News scraper é síncrono, rodamos em thread para não bloquear o loop de 14 jogos
    live_news = await asyncio.to_thread(fetch_latest_match_news, match.home_team.name, match.away_team.name)
    
    if live_news:
        context_prompt += f"\n\nNOTÍCIAS DA INTERNET (Últimas 24-48h):\nResuma rigorosamente isto:\n{live_news}\n"
    else:
        context_prompt += f"\n\nNOTÍCIAS DA INTERNET:\nNenhuma informação recente encontrada.\n"

    # Modelos estáveis (1.5-flash é o mais rápido e gratuito)
    models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro"]
    
    for model_name in models_to_try:
        max_retries = 2
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                print(f"[GeminiService] Analisando {match.home_team.name} com {model_name}...")
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
                    print(f"[GeminiService] Rate limit no {model_name} (Sinalizando tentativa {attempt+1}/{max_retries})...")
                    time.sleep(retry_delay)
                    continue
                elif "503" in error_str:
                    print(f"[GeminiService] Modelo {model_name} temporariamente indisponível. Pulando...")
                    break
                
                print(f"[GeminiService] Erro inesperado no {model_name}: {e}")
                break # Tenta o próximo modelo
                
    # Fallback final caso o Gemini falhe completamente
    return get_placeholder_insights(f"{match.home_team.name} vs {match.away_team.name}", psi_data.get('zebra_alert', False))

def get_placeholder_insights(match_name: str, zebra_alert: bool) -> Dict:
    return {
        "technical_summary": ["Análise baseada em volume histórico."],
        "emotional_narrative": "Equilíbrio emocional esperado.",
        "zebra_hunter_verdict": None,
        "deep_analysis": f"Confronto equilibrado no estádio. A estatística sugere um jogo estratégico entre {match_name}.",
        "latest_news_summary": None
    }
