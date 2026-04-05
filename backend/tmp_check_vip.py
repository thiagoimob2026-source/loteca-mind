import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Use the specific LOTECA .env path
load_dotenv(r"c:\Users\thiag\OneDrive\Área de Trabalho\LOTECA\backend\.env")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Missig Supabase secrets!")
    sys.exit(1)

sb: Client = create_client(url, key)

try:
    response = sb.table("vip_users").select("*").execute()
    users = response.data
    if users:
        print("🎉 SUCESSO! A tabela vip_users existe e contém os seguintes emails:")
        for u in users:
            print(f"- {u['email']} (Status: {u['status']})")
    else:
        print("✅ A tabela 'vip_users' existe, mas ainda está vazia (Testes do formato webhook da Kiwify podem ser ignorados pelo código se o Kiwify não enviar o campo 'email' na payload de teste).")
except Exception as e:
    print(f"❌ ERRO: {e}")
    print("A tabela 'vip_users' provavelmente não foi criada no Supabase ainda.")
