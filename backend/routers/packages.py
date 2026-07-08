from fastapi import APIRouter, HTTPException
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.client.engsel import Engsel
from app.service.auth import Auth

router = APIRouter()

@router.get("/families")
async def get_families():
    """Get all package families"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        families = await engsel.get_families()
        return {"success": True, "data": families}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/family/{family_code}")
async def get_family(family_code: str):
    """Get packages in a family"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        family = await engsel.get_family(family_code)
        return {"success": True, "data": family}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{option_code}")
async def get_package(option_code: str):
    """Get package details"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        package = await engsel.get_package(option_code)
        return {"success": True, "data": package}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{option_code}/addons")
async def get_addons(option_code: str):
    """Get package addons"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        addons = await engsel.get_addons(option_code)
        return {"success": True, "data": addons}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my/active")
async def get_my_packages():
    """Get user's active packages"""
    try:
        auth = Auth()
        active = auth.get_active_user()
        if not active:
            raise HTTPException(status_code=401, detail="No active account")
        
        engsel = Engsel(active)
        packages = await engsel.get_package()
        return {"success": True, "data": packages}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/hot/list")
async def get_hot_packages():
    """Get hot packages"""
    try:
        hot_data_path = os.path.join(os.path.dirname(__file__), "..", "hot_data", "hot.json")
        with open(hot_data_path, "r") as f:
            hot = json.load(f)
        return {"success": True, "data": hot}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/hot/bundles")
async def get_hot_bundles():
    """Get hot bundles"""
    try:
        hot_data_path = os.path.join(os.path.dirname(__file__), "..", "hot_data", "hot2.json")
        with open(hot_data_path, "r") as f:
            hot2 = json.load(f)
        return {"success": True, "data": hot2}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
