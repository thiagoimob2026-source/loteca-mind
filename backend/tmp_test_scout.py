import asyncio
import os
from dotenv import load_dotenv

# Load env from the backend directory
load_dotenv(dotenv_path="c:/Users/thiag/OneDrive/Área de Trabalho/LOTECA/backend/.env")

# Mock the import path
import sys
sys.path.append("c:/Users/thiag/OneDrive/Área de Trabalho/LOTECA/backend")

from app.services.football_api import search_team, scout_match

async def test_scout():
    print("Iniciando teste de Scout com a nova chave...")
    # Test a common team for the user (South American priority)
    team_id = await search_team("Cusco-Per")
    print(f"ID encontrado para Cusco-Per: {team_id}")
    
    if team_id:
        print("Sucesso! O buscador dinâmico está funcionando.")
    else:
        print("Falha ao encontrar o time. Verifique a chave ou o nome.")

if __name__ == "__main__":
    asyncio.run(test_scout())
