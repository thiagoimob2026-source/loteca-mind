import asyncio
import os
import sys
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.services.data_service import get_current_matches
from app.agents import alpha, psi, fusion
from app.services import gemini_service, supabase_service
from app.config import get_settings

settings = get_settings()

async def generate_initial_round():
    print("🚀 Iniciando Geração da Rodada Loteca Mind...")
    
    # 1. Pegar os 14 jogos (concurso.json ou mock)
    matches = await get_current_matches()
    print(f"✅ {len(matches)} jogos carregados.")

    full_analysis = []

    for i, match in enumerate(matches, 1):
        print(f"🔄 Analisando jogo {i}/14: {match.home_team.name} vs {match.away_team.name}...")
        
        # 2. Rodar Agentes Alpha (Tático) e Psi (Psicológico)
        alpha_report = alpha.analyze(match)
        psi_report = psi.analyze(match)
        
        # 3. Rodar Fusão (Estatística + Emoção)
        fusion_report = fusion.fuse(match, alpha_report, psi_report)
        
        # 4. Chamar Gemini para narrativas premium
        # Se GEMINI_API_KEY estiver vazia, usará mock interno do serviço
        insights = await gemini_service.generate_match_analysis(
            match, alpha_report.model_dump(), psi_report.model_dump()
        )
        
        if not insights:
            insights = gemini_service.get_placeholder_insights(
                f"{match.home_team.name} vs {match.away_team.name}",
                psi_report.zebra_alert
            )

        # 5. Montar o objeto completo da partida
        match_prediction = {
            "match": match.model_dump(),
            "reports": {
                "alpha": alpha_report.model_dump(),
                "psi": psi_report.model_dump(),
                "fusion": fusion_report.model_dump()
            },
            "insights": insights
        }
        full_analysis.append(match_prediction)
        
        # 6. Delay para evitar Rate Limit da API do Gemini
        if i < 14:
            print(f"⏳ Aguardando 10s para o próximo jogo...")
            await asyncio.sleep(10)

    # 6. Salvar no Supabase
    round_number = matches[0].round_number if matches else 10
    
    analysis_data = {
        "round": round_number,
        "timestamp": "2026-04-06T10:00:00Z",
        "matches": full_analysis
    }

    if supabase_service.is_active():
        await supabase_service.save_round_analysis(round_number, analysis_data)
        print(f"🎉 SUCESSO! Rodada {round_number} salva no Supabase.")
    else:
        # Fallback: salvar localmente se o Supabase não estiver pronto
        output_file = "backend/app/data/last_analysis.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        print(f"📂 Supabase inativo. Análise salva localmente em {output_file}")

if __name__ == "__main__":
    asyncio.run(generate_initial_round())
