from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.service.user_service import check_phone_verify, phone_verify, password_check
from app.repository.user_repo import (
    get_user_by_phone_number,
    get_user_by_email,
    get_user_by_nickname,
    create_user,
    get_user_by_user_token
)

from app.common.database.redis.core import reset_session as reset_reids_session
from app.common.database.redis.core import signup_session as signup_redis_session


def validate_phone_signup(*, db_session: Session, phone_number: int, code: int) -> dict:
    user = get_user_by_phone_number(db_session=db_session, phone_number=phone_number)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 가입한 유저입니다."
        )
    return phone_verify(phone_number=phone_number, code=code, redis_session=signup_redis_session)


def validate_phone_reset_password(
    *, db_session: Session, phone_number: int, code: int
) -> dict:
    user = get_user_by_phone_number(db_session, phone_number)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 유저입니다."
        )
    return phone_verify(phone_number=phone_number, code=code, redis_session=reset_reids_session)


def create(
    *,
    db_session: Session,
    phone_number: str,
    name: str,
    email: str,
    nickname: str,
    password: str
):
    check_phone_verify(phone_number=phone_number, redis_session=signup_redis_session)
    check_user_exist(
        db_session=db_session, phone_number=phone_number, email=email, nickname=nickname
    )
    password_check(password=password)

    user = create_user(
        db_session=db_session,
        phone_number=phone_number,
        name=name,
        email=email,
        nickname=nickname,
        password=password,
    )
    db_session.commit()
    db_session.refresh(user)
    return user


def login_user(*, db_session: Session, user_token: str):
    user = get_user_by_user_token(db_session, user_token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 유저입니다."
        )
    user.is_activate = True
    db_session.commit()
    db_session.refresh(user)
    return user


def check_user_exist(
    *, db_session: Session, phone_number: int, email: str, nickname: str
):
    user = get_user_by_phone_number(db_session=db_session, phone_number=phone_number)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="해당 번호는 이미 가입한 유저입니다."
        )
    user = get_user_by_email(db_session=db_session, email=email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="해당 이메일은 이미 가입한 유저입니다."
        )
    user = get_user_by_nickname(db_session=db_session, nickname=nickname)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="중복된 닉네임 입니다.")
