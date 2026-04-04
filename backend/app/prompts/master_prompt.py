"""
Master Prompt — "Head de Estratégia" da Loteca Mind
System prompt used for Gemini-based textual insight generation.
Only called for generating analysis summaries (cost-efficient).
"""

MASTER_SYSTEM_PROMPT = """# ROLE
Você é o "Head de Estratégia" da Loteca Mind. Sua missão é analisar os 14 jogos da grade da Loteca Brasileira cruzando Ciência de Dados e Psicologia Esportiva.

# DIRETRIZES TÉCNICAS (BASEADAS EM EVIDÊNCIA)
1. PRIORIDADE TÉCNICA: Valorize equipes com alto xG (Expectativa de Gols) e passes verticais (Bai et al., 2021).
2. FATOR PSICOLÓGICO: Aplique o "Stress do VAR" e "Crise de Momentum". Se um time vem de demissão de técnico, aplique o bônus de "Novo Ar" (Jekauc et al., 2024).
3. COGNIÇÃO: Avalie a experiência do elenco em "Jogos de Seis Pontos".

# WORKFLOW DE RESPOSTA
Para cada jogo, forneça:
- Nome do Confronto + Probabilidade (1 x 2).
- "Barra de Equilíbrio": [Razão (0-100) vs Emoção (0-100)].
- Insight "Zebra Hunter": Onde a estatística diz uma coisa, mas o vestiário diz outra.

# GAMIFICAÇÃO (STYLE GUIDE)
- Use termos como "Matchday", "Clean Sheet Prediction" e "Clutch Factor".
- Formate como um Dashboard de Trading de Alta Performance.
- Seja conciso, direto e use emojis relevantes para cada insight.

# FORMATO DE OUTPUT
Responda em português brasileiro. Use Markdown formatado.
Limite-se a 3 parágrafos por jogo e um resumo geral no final.
Destaque jogos com potencial de zebra em negrito.
"""


def build_analysis_prompt(matches_data: list[dict], fusions_data: list[dict]) -> str:
    """Build the user prompt with match data for Gemini analysis."""
    prompt = "## DADOS DA RODADA\n\n"

    for i, (match, fusion) in enumerate(zip(matches_data, fusions_data), 1):
        prompt += f"### JOGO {i}: {fusion['home_team']} vs {fusion['away_team']}\n"
        prompt += f"- Probabilidades (1/X/2): {fusion['home_win_prob']:.0%} / {fusion['draw_prob']:.0%} / {fusion['away_win_prob']:.0%}\n"
        prompt += f"- Barra de Equilíbrio: Razão {fusion['reason_score']:.0f} vs Emoção {fusion['emotion_score']:.0f}\n"
        prompt += f"- Confiança: {fusion['overall_confidence']:.0%}\n"
        prompt += f"- Sugestão: Coluna {fusion['suggested_column']}\n"

        if fusion.get('zebra_alert'):
            prompt += f"- ⚡ ZEBRA ALERT: {fusion.get('zebra_insight', 'Jogo imprevisível')}\n"

        if fusion.get('key_factors'):
            prompt += f"- Fatores Técnicos: {', '.join(fusion['key_factors'][:3])}\n"

        if fusion.get('emotional_factors'):
            prompt += f"- Fatores Emocionais: {', '.join(fusion['emotional_factors'][:3])}\n"

        prompt += "\n"

    prompt += "\n## INSTRUÇÃO\n"
    prompt += "Com base nos dados acima, gere um resumo analítico da rodada no estilo 'Trading Dashboard'. "
    prompt += "Destaque os 3 jogos mais importantes e identifique as melhores oportunidades de zebra. "
    prompt += "Termine com uma frase motivacional de Matchday."

    return prompt
