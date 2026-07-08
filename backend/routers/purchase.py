from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "cli"))

from app.service.auth import AuthInstance
from app.menus.purchase import purchase_by_family, purchase_n_times

router = APIRouter()

class PurchaseByFamilyRequest(BaseModel):
    family_code: str
    use_decoy: bool = False
    pause_on_success: bool = False
    delay_seconds: int = 0
    start_from_option: int = 1

class PurchaseNTimesRequest(BaseModel):
    package_code: str
    n: int
    use_decoy: bool = False
    delay_seconds: int = 0

@router.post("/by-family")
async def buy_by_family(request: PurchaseByFamilyRequest):
    """Purchase all packages in a family"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        result = purchase_by_family(
            request.family_code,
            request.use_decoy,
            request.pause_on_success,
            request.delay_seconds,
            request.start_from_option
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/n-times")
async def buy_n_times(request: PurchaseNTimesRequest):
    """Purchase the same package n times"""
    try:
        if not AuthInstance.active_user:
            raise HTTPException(status_code=401, detail="No active account")
        
        result = purchase_n_times(
            request.package_code,
            request.n,
            request.use_decoy,
            request.delay_seconds
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
