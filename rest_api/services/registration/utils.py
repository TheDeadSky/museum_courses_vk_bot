from sqlalchemy.orm import Session

from db.models import User
from .schemas import RegistrationData
from .exceptions import UserExistException


def raise_if_user_exist(registration_data: RegistrationData, db: Session) -> None:
    if get_user_by_vk_id(db, registration_data.vk_id):
        raise UserExistException(f"User with this social media ID({registration_data.vk_id}) already exists")


def get_user_by_vk_id(db: Session, vk_id: int):
    return db.query(User).filter(User.vk_id == vk_id).first()
