from sqlalchemy.orm import Session

from db.models import User
from db.utils import get_user_by_vk_id
from .schemas import RegistrationData, RegistrationResponse, RegistrationCheckResponse
from .utils import raise_if_user_exist
from .exceptions import RegistrationException, UserExistException


async def registration(registration_data: RegistrationData, db: Session) -> RegistrationResponse:
    try:
        raise_if_user_exist(registration_data, db)
    except UserExistException:
        return RegistrationResponse(
            success=False,
            message="Пользователь с таким ID уже зарегистрирован.",
        )

    new_user = User(
        vk_id=registration_data.vk_id,
        firstname=registration_data.firstname,
        lastname=registration_data.lastname,
        is_museum_worker=registration_data.is_museum_worker,
        how_long_museum_worker=registration_data.how_long_museum_worker,
        occupation=registration_data.occupation
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return RegistrationResponse(
            success=True,
            message="Регистрация прошла успешно"
        )
    except Exception as e:
        db.rollback()
        raise RegistrationException(f"Failed to register user: {e}")


async def is_user_registered(vk_id: int, db: Session) -> RegistrationCheckResponse:
    user = get_user_by_vk_id(db, vk_id)

    if user:
        return RegistrationCheckResponse(
            is_registered=True,
            vk_id=vk_id,
            firstname=user.firstname,
            lastname=user.lastname
        )

    return RegistrationCheckResponse(
        is_registered=False,
        vk_id=vk_id,
        firstname=None,
        lastname=None
    )
