"""
Auth Router — Verifica permissões de usuários VIP.
"""

from fastapi import APIRouter
from app.services import supabase_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/check-vip/{email}")
async def check_vip(email: str):
    """
    Retorna se o e-mail solicitado possui assinatura ativa,
    permitindo que o Frontend exiba a tela de login ou bloqueie para compra.
    """
    is_vip = await supabase_service.check_vip_status(email.lower())
    return {"email": email, "is_vip": is_vip}
