import json
from datetime import datetime, timedelta
from random import randint

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.database.redis.core import reset_session as reset_redis_session
from app.common.database.redis.core import signup_session as signup_redis_session
from app.repository.user_repo import get_user_by_phone_number
from app.schemas.sms import MessageType


def send(*, db_session: Session, type: str, phone_number: str):
    code = randint(1000, 9999)
    value_dict = {"created_at": datetime.now(), "code": code}
    value = json.dumps(value_dict, default=str)
    if type == MessageType.signup:
        user = get_user_by_phone_number(db_session=db_session, phone_number=phone_number)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="해당 번호는 이미 가입한 유저입니다."
            )
        signup_redis_session.set(
            name=phone_number, value=value, ex=timedelta(seconds=60 * 3)
        )
    elif type == MessageType.reset:
        user = get_user_by_phone_number(db_session=db_session, phone_number=phone_number)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="가입하지 않은 유저 입니다."
            )
        reset_redis_session.set(
            name=phone_number, value=value, ex=timedelta(seconds=60 * 3)
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="지원하지 않는 타입 입니다."
        )
    return value_dict
