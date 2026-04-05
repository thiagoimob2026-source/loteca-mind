import os
import asyncio
import google.generativeai as genai
from supabase import create_client

def load_env_any_encoding(path):
    encodings = ['utf-16le', 'utf-16', 'utf-8', 'latin-1']
    content = ""
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
            # If it starts with BOM or looks like key=value, we found it
            if 'GEMINI_API_KEY' in content:
                print(f"--- Arquivo .env lido com sucesso usando encoding: {enc} ---")
                break
        except:
            continue
    
    env = {}
    for line in content.splitlines():
        if '=' in line and not line.startswith('#'):
            key, val = line.strip().split('=', 1)
            env[key.strip()] = val.strip()
    return env

async def test_all():
    env = load_env_any_encoding('.env')
    
    # Test Supabase
    try:
        url = env.get('SUPABASE_URL')
        key = env.get('SUPABASE_KEY')
        if url and key:
            supabase = create_client(url, key)
            supabase.table("profiles").select("*").limit(1).execute()
            print("✅ Conexão Supabase: OK")
        else:
            print("❌ Chaves Supabase não encontradas no .env")
    except Exception as e:
        print(f"❌ Erro Supabase: {e}")

    # Test Gemini
    try:
        g_key = env.get('GEMINI_API_KEY')
        if g_key:
            genai.configure(api_key=g_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Diga 'Pronto para a Loteca!'")
            print(f"✅ Conexão Gemini: OK ({response.text.strip()})")
        else:
            print("❌ Chave Gemini não encontrada no .env")
    except Exception as e:
        print(f"❌ Erro Gemini: {e}")

if __name__ == "__main__":
    asyncio.run(test_all())
