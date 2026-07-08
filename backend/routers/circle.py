from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client import circle
from app.service.auth import AuthInstance

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
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        status = circle.get_group_data(AuthInstance.api_key, tokens)
        return {"success": True, "data": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/members")
async def get_circle_members():
    """Get circle group members"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        # First get group data to get group_id
        group_data = circle.get_group_data(AuthInstance.api_key, tokens)
        group_id = group_data.get("group_id", "")
        
        members = circle.get_group_members(AuthInstance.api_key, tokens, group_id)
        return {"success": True, "data": members}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/invite")
async def invite_member(request: InviteMember):
    """Invite a member to circle"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        # Validate member first
        validation = circle.validate_circle_member(AuthInstance.api_key, tokens, request.phone_number)
        
        # Get group data
        group_data = circle.get_group_data(AuthInstance.api_key, tokens)
        group_id = group_data.get("group_id", "")
        
        # Invite member
        result = circle.invite_circle_member(
            AuthInstance.api_key,
            tokens,
            request.phone_number,
            group_id,
            AuthInstance.active_user["number"],
            AuthInstance.active_user["subscriber_id"],
            AuthInstance.active_user["subscription_type"]
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/remove")
async def remove_member(request: RemoveMember):
    """Remove a member from circle"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        # Get group data
        group_data = circle.get_group_data(AuthInstance.api_key, tokens)
        group_id = group_data.get("group_id", "")
        
        result = circle.remove_circle_member(
            AuthInstance.api_key,
            tokens,
            request.phone_number,
            group_id,
            AuthInstance.active_user["number"],
            AuthInstance.active_user["subscriber_id"],
            AuthInstance.active_user["subscription_type"]
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/accept")
async def accept_invitation(request: AcceptInvitation):
    """Accept circle invitation"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        result = circle.accept_circle_invitation(
            AuthInstance.api_key,
            tokens,
            request.invitation_id,
            AuthInstance.active_user["number"],
            AuthInstance.active_user["subscriber_id"],
            AuthInstance.active_user["subscription_type"]
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create")
async def create_circle(request: CreateCircle):
    """Create a new circle"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        result = circle.create_circle(
            AuthInstance.api_key,
            tokens,
            request.name,
            AuthInstance.active_user["number"],
            AuthInstance.active_user["subscriber_id"],
            AuthInstance.active_user["subscription_type"],
            ""
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bonus")
async def get_circle_bonus():
    """Get circle bonus data"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        # Get group data first
        group_data = circle.get_group_data(AuthInstance.api_key, tokens)
        group_id = group_data.get("group_id", "")
        
        bonus = circle.get_bonus_data(
            AuthInstance.api_key,
            tokens,
            group_id,
            AuthInstance.active_user["number"],
            AuthInstance.active_user["subscriber_id"]
        )
        return {"success": True, "data": bonus}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
