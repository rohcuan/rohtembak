from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from auth import verify_token, TokenData
from routers import auth, profile, packages, purchase, circle, family, notification, transaction, xl_auth

app = FastAPI(
    title="RohTembak API",
    description="Web API for XL Axiata CLI Client",
    version="1.0.0"
)

# CORS Configuration
# Only needed for development. In production with Cloudflare Tunnel (path-based routing),
# frontend and backend are same-origin, so CORS is not an issue.
if os.getenv("ENVIRONMENT") == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Security
security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> TokenData:
    """Dependency to get current authenticated user"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = verify_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(xl_auth.router, prefix="/api/xl", tags=["XL Login"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"], dependencies=[Depends(get_current_user)])
app.include_router(packages.router, prefix="/api/packages", tags=["Packages"], dependencies=[Depends(get_current_user)])
app.include_router(purchase.router, prefix="/api/purchase", tags=["Purchase"], dependencies=[Depends(get_current_user)])
app.include_router(circle.router, prefix="/api/circle", tags=["Circle"], dependencies=[Depends(get_current_user)])
app.include_router(family.router, prefix="/api/family", tags=["Family Plan"], dependencies=[Depends(get_current_user)])
app.include_router(notification.router, prefix="/api/notifications", tags=["Notifications"], dependencies=[Depends(get_current_user)])
app.include_router(transaction.router, prefix="/api/transactions", tags=["Transactions"], dependencies=[Depends(get_current_user)])

@app.get("/")
async def root():
    return {"message": "RohTembak API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
