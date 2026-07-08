from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client.circle import Circle
from app.service.auth import Auth

router = APIRouter()

class InviteMember(BaseModel):
    phone_number: str

class RemoveMember(BaseModel):
    phone_number: str

class AcceptInvitation(BaseModel):
    invitation_id: str

class CreateCircle(BaseModel):
    name: str

@router.get("/status")
async def get_circle_status():
    """Get circle group status"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        circle = Circle(active)
        status = await circle.get_group_data()
        return {"success": True, "data": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/members")
async def get_circle_members():
    """Get circle members"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        circle = Circle(active)
        members = await circle.get_group_members()
        return {"success": True, "data": members}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/invite")
async def invite_member(request: InviteMember):
    """Invite member to circle"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        circle = Circle(active)
        result = await circle.invite_circle_member(request.phone_number)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/remove")
async def remove_member(request: RemoveMember):
    """Remove member from circle"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        circle = Circle(active)
        result = await circle.remove_circle_member(request.phone_number)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/accept")
async def accept_invitation(request: AcceptInvitation):
    """Accept circle invitation"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        circle = Circle(active)
        result = await circle.accept_circle_invitation(request.invitation_id)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create")
async def create_circle(request: CreateCircle):
    """Create new circle"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        circle = Circle(active)
        result = await circle.create_circle(request.name)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bonus")
async def get_circle_bonus():
    """Get circle bonus data"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        circle = Circle(active)
        bonus = await circle.get_bonus_data()
        return {"success": True, "data": bonus}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
