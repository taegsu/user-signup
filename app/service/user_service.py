from datetime import datetime, timedelta
import json
import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repository.user_repo import (
    get_user_by_phone_number,
    get_user_by_email,
    get_user_by_nickname,
    create_user,
)
from app.schemas.sms import MessageType

from app.common.database.redis.core import reset_session as reset_reids_session
from app.common.database.redis.core import signup_session as signup_redis_session


def validate_phone(
    *, db_session: Session, type: str, phone_number: int, code: int
) -> dict:
    if type == MessageType.signup:
        user = get_user_by_phone_number(
            db_session=db_session, phone_number=phone_number
        )
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="이미 가입한 유저입니다."
            )
        verified_data = signup_redis_session.get(phone_number)
        if not verified_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="인증정보가 존재하지 않습니다."
            )
        verified_data = dict(json.loads(verified_data.decode("utf-8")))
        if datetime.strptime(
            verified_data["created_at"], "%Y-%m-%d %H:%M:%S.%f"
        ) >= datetime.now() - timedelta(minutes=5):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="인증번호 유효시간이 지났습니다."
            )
        if verified_data["code"] != code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="인증번호가 올바르지 않습니다."
            )
        signup_redis_session.set(
            name=phone_number,
            value=json.dumps({"verified_at": datetime.now()}, default=str),
        )
    elif type == MessageType.reset:
        user = get_user_by_phone_number(db_session, phone_number)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 유저입니다."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="지원하지 않는 타입 입니다."
        )
    return {phone_number: "verified"}


def create(
    *,
    db_session: Session,
    phone_number: str,
    name: str,
    email: str,
    nickname: str,
    password: str
):
    user = get_user_by_phone_number(db_session, phone_number=phone_number)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="해당 번호는 이미 가입한 유저입니다."
        )
    verified_data = signup_redis_session.get(phone_number)
    if not verified_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="인증정보가 존재하지 않습니다."
        )
    verified_data = dict(json.loads(verified_data.decode("utf-8")))
    if verified_data.get("verified_at", None) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="인증이 되지 않은 번호 입니다."
        )
    if datetime.strptime(
        verified_data["verified_at"], "%Y-%m-%d %H:%M:%S.%f"
    ) >= datetime.now() - timedelta(minutes=5):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="인증 유효시간이 지났습니다."
        )
    user = get_user_by_email(db_session, email=email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="해당 이메일은 이미 가입한 유저입니다."
        )
    user = get_user_by_nickname(db_session, nickname=nickname)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="중복된 닉네임 입니다.")
    password_check(password=password)

    user = create_user(
        phone_number=phone_number,
        name=name,
        email=email,
        nickname=nickname,
        password=password,
    )
    db_session.commit()
    db_session.refresh(user)
    return user


def password_check(password: str) -> bool:
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호는 최소 8자 이상이어야 합니다."
        )

    if len(password) > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호는 최대 20자 입니다."
        )

    if not re.findall("[0-9]+", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="숫자가 포함되어야 합니다."
        )

    if not re.findall("[a-z]+", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="영문 소문자가 포함되어야 합니다."
        )

    if not re.findall("['~!@#$%^&*()_+,./<>?]+", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="특수문자가 포함되어야 합니다."
        )

    return True
