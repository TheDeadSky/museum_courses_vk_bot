from sqlalchemy.orm import Session
from db.models import User
from typing import Optional
from sqlalchemy import or_


def get_user_by_vk_id(db: Session, vk_id: int) -> Optional[User]:
    """Get user by social media ID (telegram_id or vk_id)"""
    return db.query(User).filter(
        or_(
            User.vk_id == sm_id
        )
    ).first()
