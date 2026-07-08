from fastapi import APIRouter, HTTPException
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client.engsel import Engsel
from app.service.auth import Auth

router = APIRouter()

@router.get("/")
async def get_notifications():
    """Get all notifications"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        notifications = await engsel.get_notifications()
        return {"success": True, "data": notifications}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{notification_id}")
async def get_notification_detail(notification_id: str):
    """Get notification detail"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        detail = await engsel.get_notification_detail(notification_id)
        return {"success": True, "data": detail}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
