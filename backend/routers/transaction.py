from fastapi import APIRouter, HTTPException
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client.engsel import Engsel
from app.service.auth import Auth

router = APIRouter()

@router.get("/")
async def get_transactions():
    """Get transaction history"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        transactions = await engsel.get_transaction_history()
        return {"success": True, "data": transactions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
