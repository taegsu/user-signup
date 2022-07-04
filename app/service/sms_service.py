import json
from datetime import datetime, timedelta
from random import randint

from fastapi import HTTPException, status

from app.common.database.redis.core import reset_session as reset_reids_session
from app.common.database.redis.core import signup_session as signup_redis_session
from app.schemas.sms import MessageType


def send(*, type: str, phone_number: int):
    code = randint(1000, 9999)
    value_dict = {"created_at": datetime.now(), "code": code}
    value = json.dumps(value_dict, default=str)
    if type == MessageType.signup:
        signup_redis_session.set(name=phone_number, value=value, ex=60 * 3)
    elif type == MessageType.reset:
        reset_reids_session.set(key=phone_number, value=value, ex=60 * 3)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="지원하지 않는 타입 입니다."
        )
    return value_dict
