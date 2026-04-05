import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client
import google.generativeai as genai

# Load env from backend/.env
env_path = r"c:\Users\thiag\OneDrive\Área de Trabalho\LOTECA\backend\.env"
load_dotenv(env_path)

async def test_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    print(f"\n--- Testando Supabase ---")
    if not url or not key:
        print("❌ Chaves do Supabase não encontradas no .env")
        return
    
    try:
        supabase = create_client(url, key)
        # Test query to profiles
        res = supabase.table("profiles").select("*").limit(1).execute()
        print("✅ Conexão com Supabase: OK")
    except Exception as e:
        print(f"❌ Erro no Supabase: {e}")

async def test_gemini():
    key = os.getenv("GEMINI_API_KEY")
    print(f"\n--- Testando Gemini ---")
    if not key:
        print("❌ Chave do Gemini não encontrada no .env")
        return
    
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Diga 'Gol da Loteca!' se você estiver funcionando.")
        print(f"✅ Gemini Respondeu: {response.text.strip()}")
    except Exception as e:
        print(f"❌ Erro no Gemini: {e}")

if __name__ == "__main__":
    asyncio.run(test_supabase())
    asyncio.run(test_gemini())
