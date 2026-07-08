from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add project root to path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client.ciam import Ciam
from app.service.auth import Auth

router = APIRouter()

class OTPRequest(BaseModel):
    msisdn: str  # Phone number e.g. "6281234567890"

class OTPVerify(BaseModel):
    msisdn: str
    otp: str

class AccountInfo(BaseModel):
    msisdn: str
    token: str

class SwitchAccount(BaseModel):
    msisdn: str

@router.post("/otp/request")
async def request_otp(request: OTPRequest):
    """Request OTP for XL login"""
    try:
        ciam = Ciam()
        result = await ciam.get_otp(request.msisdn)
        return {"success": True, "message": "OTP sent", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/otp/verify")
async def verify_otp(request: OTPVerify):
    """Verify OTP and save token"""
    try:
        ciam = Ciam()
        result = await ciam.submit_otp(request.msisdn, request.otp)
        
        # Save token using Auth
        auth = Auth()
        auth.save_refresh_token(request.msisdn, result.get("refresh_token", ""))
        auth.set_active_user(request.msisdn)
        
        return {"success": True, "message": "Login successful", "msisdn": request.msisdn}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/accounts")
async def list_accounts():
    """List all saved XL accounts"""
    try:
        auth = Auth()
        tokens = auth.load_tokens()
        active = auth.get_active_user()
        
        accounts = []
        for msisdn, token_data in tokens.items():
            accounts.append({
                "msisdn": msisdn,
                "is_active": msisdn == active,
                "has_token": bool(token_data.get("refresh_token"))
            })
        return {"accounts": accounts, "active": active}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/switch")
async def switch_account(request: SwitchAccount):
    """Switch active account"""
    try:
        auth = Auth()
        auth.set_active_user(request.msisdn)
        return {"success": True, "active": request.msisdn}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/accounts/{msisdn}")
async def remove_account(msisdn: str):
    """Remove a saved account"""
    try:
        auth = Auth()
        auth.remove_refresh_token(msisdn)
        return {"success": True, "message": f"Account {msisdn} removed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def auth_status():
    """Check if user is logged in"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        return {
            "logged_in": active is not None,
            "active_msisdn": active
        }
    except Exception as e:
        return {"logged_in": False, "active_msisdn": None}
