from datetime import datetime, timedelta
import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repository.user_repo import get_user
from app.schemas.sms import MessageType

from app.common.database.redis.core import reset_session as reset_reids_session
from app.common.database.redis.core import signup_session as signup_redis_session


def validate_phone(*, db_session: Session, type: str, phone_number: int, code: int):
    if type == MessageType.signup:
        user = get_user(db_session=db_session, phone_number=phone_number)
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
            name=phone_number, value=json.dumps({"verified_at": datetime.now()}, default=str)
        )
    elif type == MessageType.reset:
        user = get_user(db_session, phone_number)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 유저입니다."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="지원하지 않는 타입 입니다."
        )
