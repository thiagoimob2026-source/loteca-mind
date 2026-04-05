from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Tuple
import os
import json

router = APIRouter(prefix="/api/admin", tags=["admin"])

CONCURSO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "concurso.json")

class ConcursoPayload(BaseModel):
    round_number: int
    matches: List[Tuple[str, str]]

@router.post("/concurso")
async def update_concurso(payload: ConcursoPayload):
    """
    Atualiza o arquivo oficial do concurso que o robô lerá para a próxima rodada.
    """
    if len(payload.matches) != 14:
        raise HTTPException(status_code=400, detail="A grade deve ter exatamente 14 jogos.")
    
    try:
        os.makedirs(os.path.dirname(CONCURSO_FILE), exist_ok=True)
        data_to_save = {
            "round_number": payload.round_number,
            "matches": payload.matches
        }
        with open(CONCURSO_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
            
        return {"status": "success", "message": f"Concurso {payload.round_number} atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
