from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client.engsel import Engsel
from app.service.auth import Auth
from app.menus.purchase import purchase_balance, purchase_qris, purchase_ewallet, purchase_decoy

router = APIRouter()

class PurchaseBalanceRequest(BaseModel):
    option_code: str

class PurchaseQRISRequest(BaseModel):
    option_code: str
    amount: int

class PurchaseEWalletRequest(BaseModel):
    option_code: str
    phone_number: str

class PurchaseDecoyRequest(BaseModel):
    option_code: str
    decoy_type: str  # "balance" or "qris"

@router.post("/balance")
async def buy_with_balance(request: PurchaseBalanceRequest):
    """Purchase package using balance (pulsa)"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        result = await purchase_balance(active, request.option_code)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/qris")
async def buy_with_qris(request: PurchaseQRISRequest):
    """Purchase package using QRIS"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        result = await purchase_qris(active, request.option_code, request.amount)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/ewallet")
async def buy_with_ewallet(request: PurchaseEWalletRequest):
    """Purchase package using e-wallet"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        result = await purchase_ewallet(active, request.option_code, request.phone_number)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/decoy")
async def buy_with_decoy(request: PurchaseDecoyRequest):
    """Purchase package using decoy method"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        result = await purchase_decoy(active, request.option_code, request.decoy_type)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
