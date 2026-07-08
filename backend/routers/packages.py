from fastapi import APIRouter, HTTPException
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client import engsel
from app.service.auth import AuthInstance

router = APIRouter()

@router.get("/families")
async def get_families():
    """Get all package families"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        families = engsel.get_families(AuthInstance.api_key, tokens, "")
        return {"success": True, "data": families}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/family/{family_code}")
async def get_family(family_code: str):
    """Get packages in a family"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        family = engsel.get_package(AuthInstance.api_key, tokens, family_code)
        return {"success": True, "data": family}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/package/{option_code}")
async def get_package(option_code: str):
    """Get package details"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        package = engsel.get_package_details(
            AuthInstance.api_key, tokens, option_code, 
            AuthInstance.active_user["number"], 
            AuthInstance.active_user["subscriber_id"],
            AuthInstance.active_user["subscription_type"],
            ""
        )
        return {"success": True, "data": package}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/addons/{option_code}")
async def get_addons(option_code: str):
    """Get addons for a package"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        addons = engsel.get_addons(AuthInstance.api_key, tokens, option_code)
        return {"success": True, "data": addons}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my/active")
async def get_my_active_packages():
    """Get user's active packages"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        tokens = AuthInstance.active_user["tokens"]
        profile = engsel.get_profile(AuthInstance.api_key, tokens["access_token"], tokens["id_token"])
        return {"success": True, "data": profile.get("packages", [])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/hot/list")
async def get_hot_packages():
    """Get hot packages"""
    try:
        hot_data_path = os.path.join(os.path.dirname(__file__), "..", "..", "cli", "hot_data", "hot.json")
        with open(hot_data_path, "r") as f:
            hot = json.load(f)
        return {"success": True, "data": hot}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/hot/bundles")
async def get_hot_bundles():
    """Get hot bundles"""
    try:
        hot_data_path = os.path.join(os.path.dirname(__file__), "..", "..", "cli", "hot_data", "hot2.json")
        with open(hot_data_path, "r") as f:
            hot2 = json.load(f)
        return {"success": True, "data": hot2}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
