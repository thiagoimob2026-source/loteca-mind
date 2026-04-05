"""
News Scraper Service — Busca de dados em tempo real para Grounding da IA.
Utiliza duckduckgo-search para capturar as informações mais cruciais (desfalques e goleiros).
"""

from duckduckgo_search import DDGS
from typing import Optional
import time

def fetch_latest_match_news(home_team: str, away_team: str) -> Optional[str]:
    """
    Busca notícias das últimas 24/48h focando em desfalques e goleiros dos times informados.
    Retorna uma string compilada das descrições dos links para ser usada como contexto do Gemini.
    """
    query = f'"{home_team}" OR "{away_team}" goleiro titular reserva desfalques ultimas noticias'
    
    scraped_text = ""
    try:
        results = DDGS().text(query, max_results=4, region='br-pt', safesearch='off', timelimit='d')
        
        if not results:
            # Fallback sem limitação de tempo (d = past day, w = past week)
            time.sleep(1)
            results_fallback = DDGS().text(query, max_results=3, region='br-pt')
            results = results_fallback if results_fallback else []

        for item in results:
            title = item.get('title', '')
            body = item.get('body', '')
            scraped_text += f"- [{title}]: {body}\n"
            
    except Exception as e:
        print(f"[NewsScraper] Erro ao buscar notícias para {home_team} vs {away_team}: {e}")
        return None

    return scraped_text.strip() if scraped_text else None
