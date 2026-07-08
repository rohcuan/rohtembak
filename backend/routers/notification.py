from fastapi import APIRouter, HTTPException
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client import engsel
from app.service.auth import AuthInstance

router = APIRouter()

@router.get("/")
async def get_notifications():
    """Get all notifications"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        notifications = engsel.get_notifications(AuthInstance.api_key, tokens)
        return {"success": True, "data": notifications}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{notification_id}")
async def get_notification_detail(notification_id: str):
    """Get notification detail"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        detail = engsel.get_notification_detail(AuthInstance.api_key, tokens, notification_id)
        return {"success": True, "data": detail}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
