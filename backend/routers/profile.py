from fastapi import APIRouter, HTTPException
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client import engsel
from app.service.auth import AuthInstance

router = APIRouter()

@router.get("/")
async def get_profile():
    """Get user profile information"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        api_key = AuthInstance.api_key
        tokens = AuthInstance.active_user["tokens"]
        profile = engsel.get_profile(api_key, tokens["access_token"], tokens["id_token"])
        return {"success": True, "data": profile}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/balance")
async def get_balance():
    """Get user balance (pulsa & kuota)"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        balance = engsel.get_balance(AuthInstance.api_key, tokens["id_token"])
        return {"success": True, "data": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tiering")
async def get_tiering():
    """Get tiering information"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        tiering = engsel.get_tiering_info(AuthInstance.api_key, tokens)
        return {"success": True, "data": tiering}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dashboard")
async def get_dashboard():
    """Get dashboard segments"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        dashboard = engsel.dashboard_segments(AuthInstance.api_key, tokens)
        return {"success": True, "data": dashboard}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
