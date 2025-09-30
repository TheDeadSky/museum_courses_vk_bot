from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from .actions import registration, RegistrationException, is_user_registered
from .schemas import RegistrationData, RegistrationResponse, RegistrationCheckResponse

router = APIRouter()


@router.post("/registration")
async def register(registration_data: RegistrationData, db: Session = Depends(get_db)) -> RegistrationResponse:
    """Register a new user"""
    try:
        return await registration(registration_data, db)
    except RegistrationException as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}")


@router.get("/registration")
async def is_registered(vk_id: int, db: Session = Depends(get_db)) -> RegistrationCheckResponse:
    """Check if a user is registered by email"""
    return await is_user_registered(vk_id, db)
