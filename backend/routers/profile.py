from fastapi import APIRouter, HTTPException
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client.engsel import Engsel
from app.service.auth import Auth

router = APIRouter()

@router.get("/")
async def get_profile():
    """Get user profile information"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        profile = await engsel.get_profile()
        return {"success": True, "data": profile}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/balance")
async def get_balance():
    """Get user balance (pulsa & kuota)"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        balance = await engsel.get_balance()
        return {"success": True, "data": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tiering")
async def get_tiering():
    """Get tiering information"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        tiering = await engsel.get_tiering_info()
        return {"success": True, "data": tiering}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dashboard")
async def get_dashboard():
    """Get dashboard segments"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        dashboard = await engsel.dashboard_segments()
        return {"success": True, "data": dashboard}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
