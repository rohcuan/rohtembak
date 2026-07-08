from fastapi import APIRouter, HTTPException
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client import engsel
from app.service.auth import AuthInstance

router = APIRouter()

@router.get("/")
async def get_transactions():
    """Get transaction history"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        transactions = engsel.get_transaction_history(AuthInstance.api_key, tokens)
        return {"success": True, "data": transactions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
