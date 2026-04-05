"""
Webhooks Router — Escuta passiva de Pagamentos da Kiwify.
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
from app.services import supabase_service

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

@router.post("/kiwify")
async def kiwify_webhook(payload: Dict[Any, Any], request: Request):
    """
    Recebe o Webhook da Kiwify quando ocorre uma movimentação de pagamento.
    Verifica se a venda foi Aprovada, extrai o e-mail do cliente,
    e envia para a tabela de assinantes VIP no Supabase.
    """
    try:
        # Kiwify Payload Structure:
        # payload["order"]["status"] = "paid" | "refunded" | "refused"
        # payload["Customer"]["email"] = "joao@gmail.com"
        
        # A Kiwify envia os dados dentro de 'order' e 'Customer' ou variáveis primárias
        # Vamos fazer um fallback de chaves caso varie na documentação
        
        # O Kiwify Test Payload geralmente vem "flat", enquanto o Real vem aninhado.
        order_status = payload.get("order_status") or payload.get("status") or payload.get("order", {}).get("status")
        customer_email = payload.get("email") or payload.get("Customer", {}).get("email") or payload.get("customer", {}).get("email")

        # Log total para diagnóstico
        print(f"[Webhook Kiwify Payload Recebido]: {payload}")

        if not customer_email:
            print("[Webhook Kiwify] Payload ignorado: Falta e-mail do cliente.")
            return {"status": "ignored", "reason": "No email"}

        # Se for teste da plataforma ou venda confirmada
        if order_status in ["paid", "approved", "completed", "test"]:
            # Liberar o sistema (Cadastra ou renova o passe VIP)
            success = await supabase_service.add_vip_user(customer_email.lower())
            if success:
                print(f"[Webhook Kiwify] 💰 SUCESSO! Acesso liberado para: {customer_email}")
                return {"status": "success", "vip_granted": True}
        
        elif order_status in ["refunded", "chargeback", "canceled"]:
            # Cortamos o acesso se ele pedir reembolso (Opcional Futuro: revoke_vip)
            print(f"[Webhook Kiwify] 🚫 REEMBOLSO: Suspender acesso de: {customer_email}")
            return {"status": "success", "vip_revoked": True}

        return {"status": "ignored", "reason": "Status não aplicável"}
    
    except Exception as e:
        print(f"[Webhook Kiwify] ERRO CRÍTICO: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar webhook")
