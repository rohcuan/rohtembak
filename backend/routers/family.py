from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client import famplan
from app.service.auth import AuthInstance

router = APIRouter()

class ValidateMsisdn(BaseModel):
    phone_number: str

class ChangeMember(BaseModel):
    old_phone_number: str
    new_phone_number: str

class RemoveMember(BaseModel):
    phone_number: str

class SetQuotaLimit(BaseModel):
    phone_number: str
    quota_limit: int

@router.get("/data")
async def get_family_data():
    """Get family plan data"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        data = famplan.get_family_data(AuthInstance.api_key, tokens)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate")
async def validate_member(request: ValidateMsisdn):
    """Validate a phone number for family plan"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        result = famplan.validate_msisdn(AuthInstance.api_key, tokens, request.phone_number)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/change-member")
async def change_member(request: ChangeMember):
    """Change a member in family plan"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        result = famplan.change_member(
            AuthInstance.api_key,
            tokens,
            request.old_phone_number,
            request.new_phone_number,
            AuthInstance.active_user["number"],
            AuthInstance.active_user["subscriber_id"],
            AuthInstance.active_user["subscription_type"],
            ""
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/remove-member")
async def remove_member(request: RemoveMember):
    """Remove a member from family plan"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        result = famplan.remove_member(
            AuthInstance.api_key,
            tokens,
            request.phone_number,
            AuthInstance.active_user["number"]
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/quota-limit")
async def set_quota_limit(request: SetQuotaLimit):
    """Set quota limit for a family member"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        result = famplan.set_quota_limit(
            AuthInstance.api_key,
            tokens,
            request.phone_number,
            request.quota_limit,
            AuthInstance.active_user["number"],
            AuthInstance.active_user["subscriber_id"]
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
