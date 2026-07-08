from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client import ciam
from app.service.auth import AuthInstance

router = APIRouter()

class OTPRequest(BaseModel):
    msisdn: str

class OTPVerify(BaseModel):
    msisdn: str
    otp: str

@router.post("/otp/request")
async def request_otp(request: OTPRequest):
    """Request OTP for XL login"""
    try:
        # Validate contact first
        if not ciam.validate_contact(request.msisdn):
            raise HTTPException(status_code=400, detail="Invalid phone number format")
        
        # Request OTP
        request_id = ciam.get_otp(request.msisdn)
        return {"success": True, "message": "OTP sent", "request_id": request_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/otp/verify")
async def verify_otp(request: OTPVerify):
    """Verify OTP and login to XL"""
    try:
        # Submit OTP
        result = ciam.submit_otp(
            request.msisdn,
            request.otp,
            AuthInstance.api_key,
            ""
        )
        
        if result and "tokens" in result:
            # Add to AuthInstance
            AuthInstance.add_refresh_token(
                request.msisdn,
                result["tokens"]["refresh_token"],
                result.get("subscriber_id", ""),
                result.get("subscription_type", "")
            )
            
            # Set as active user
            AuthInstance.set_active_user(request.msisdn)
            
            return {"success": True, "message": "Login successful", "msisdn": request.msisdn}
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP or login failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/accounts")
async def get_accounts():
    """Get list of saved XL accounts"""
    try:
        accounts = []
        for token_data in AuthInstance.refresh_tokens:
            accounts.append({
                "msisdn": token_data.get("msisdn", ""),
                "subscriber_id": token_data.get("subscriber_id", ""),
                "subscription_type": token_data.get("subscription_type", ""),
                "is_active": AuthInstance.active_user and AuthInstance.active_user.get("msisdn") == token_data.get("msisdn")
            })
        return {"success": True, "data": accounts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/switch")
async def switch_account(msisdn: str):
    """Switch to a different XL account"""
    try:
        AuthInstance.set_active_user(msisdn)
        return {"success": True, "message": f"Switched to {msisdn}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/accounts/{msisdn}")
async def remove_account(msisdn: str):
    """Remove a saved XL account"""
    try:
        AuthInstance.remove_refresh_token(msisdn)
        return {"success": True, "message": f"Account {msisdn} removed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def get_login_status():
    """Get current login status"""
    try:
        if AuthInstance.active_user:
            return {
                "success": True,
                "logged_in": True,
                "msisdn": AuthInstance.active_user.get("msisdn", ""),
                "subscriber_id": AuthInstance.active_user.get("subscriber_id", "")
            }
        else:
            return {"success": True, "logged_in": False}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
