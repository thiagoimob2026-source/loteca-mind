"""
Auth Router — Verifica permissões de usuários VIP.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import supabase_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


class GrantVipRequest(BaseModel):
    email: str
    admin_token: str


@router.get("/check-vip/{email}")
async def check_vip(email: str):
    """
    Retorna se o e-mail solicitado possui assinatura ativa,
    permitindo que o Frontend exiba a tela de login ou bloqueie para compra.
    """
    is_vip = await supabase_service.check_vip_status(email.lower())
    return {"email": email, "is_vip": is_vip}


@router.post("/grant-vip")
async def grant_vip(body: GrantVipRequest):
    """Endpoint admin para conceder acesso VIP manualmente."""
    if body.admin_token != "zebra14admin":
        raise HTTPException(status_code=403, detail="Token inválido")
    success = await supabase_service.add_vip_user(body.email.lower())
    if success:
        return {"status": "success", "message": f"VIP concedido para {body.email}"}
    raise HTTPException(status_code=500, detail="Erro ao conceder VIP")
