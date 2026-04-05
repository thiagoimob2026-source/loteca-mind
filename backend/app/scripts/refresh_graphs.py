import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.services.data_service import get_current_matches
from app.agents import alpha, psi, fusion
from app.services import supabase_service

async def main():
    print("Atualizando apenas a matemática local...")
    matches = await get_current_matches()
    fusions = []
    
    for m in matches:
        a = alpha.analyze(m)
        p = psi.analyze(m)
        f = fusion.fuse(m, a, p)
        fusions.append(f)
        print(f"{m.home_team.name}: Razão {f.reason_score}% | Emoção {f.emotion_score}%")
    
    last = await supabase_service.get_latest_analysis()
    if last:
        for i, _ in enumerate(last.get('fusions', [])):
            if i < len(fusions):
                last['fusions'][i]['reason_score'] = fusions[i].reason_score
                last['fusions'][i]['emotion_score'] = fusions[i].emotion_score
        
        await supabase_service.save_round_analysis(last['round_number'], last)
        print(f"🎉 SUCESSO! Barras dinâmicas aplicadas no banco de dados para a rodada {last['round_number']}.")
    else:
        print("Erro: Nenhuma análise anterior encontrada no Supabase para sobrescrever. Rode a geração completa primeiro.")

if __name__ == "__main__":
    asyncio.run(main())
