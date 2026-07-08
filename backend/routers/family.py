from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client.famplan import FamPlan
from app.service.auth import Auth

router = APIRouter()

class ValidateMsisdn(BaseModel):
    phone_number: str
    nik: str  # National ID number

class ChangeMember(BaseModel):
    old_number: str
    new_number: str
    nik: str

class RemoveMember(BaseModel):
    phone_number: str

class SetQuotaLimit(BaseModel):
    phone_number: str
    quota_limit: int

@router.get("/data")
async def get_family_data():
    """Get family plan data"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        famplan = FamPlan(active)
        data = await famplan.get_family_data()
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate")
async def validate_msisdn(request: ValidateMsisdn):
    """Validate phone number against Dukcapil"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        famplan = FamPlan(active)
        result = await famplan.validate_msisdn(request.phone_number, request.nik)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/change-member")
async def change_member(request: ChangeMember):
    """Change family member"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        famplan = FamPlan(active)
        result = await famplan.change_member(
            request.old_number, 
            request.new_number, 
            request.nik
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/remove-member")
async def remove_member(request: RemoveMember):
    """Remove family member"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        famplan = FamPlan(active)
        result = await famplan.remove_member(request.phone_number)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/quota-limit")
async def set_quota_limit(request: SetQuotaLimit):
    """Set quota limit for family member"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        famplan = FamPlan(active)
        result = await famplan.set_quota_limit(
            request.phone_number, 
            request.quota_limit
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
