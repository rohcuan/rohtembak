from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from auth import create_access_token, check_subscription_expired
from subscription_service import subscription_service

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    subscription_expiry: str
    is_expired: bool

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate with subscription credentials"""
    # Authenticate against GitHub-hosted subscription list
    sub_data = await subscription_service.authenticate(request.username, request.password)
    
    if sub_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Check if subscription is expired
    is_expired = check_subscription_expired(sub_data["subscription_expiry"])
    
    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": sub_data["username"],
            "subscription_expiry": sub_data["subscription_expiry"]
        }
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=sub_data["username"],
        subscription_expiry=sub_data["subscription_expiry"],
        is_expired=is_expired
    )

@router.get("/refresh")
async def refresh_subscriptions():
    """Force refresh subscription data from GitHub"""
    success = await subscription_service.fetch_subscriptions()
    if success:
        return {"message": "Subscriptions refreshed", "count": len(subscription_service.subscriptions)}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch subscriptions from GitHub"
        )
