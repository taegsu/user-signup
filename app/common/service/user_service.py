from datetime import datetime, timedelta
import json
import re

from fastapi import HTTPException, status


def check_phone_verify(phone_number: str, redis_session) -> bool:
    verified_data = redis_session.get(phone_number)
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
    ) <= datetime.now() - timedelta(minutes=5):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="인증 유효시간이 지났습니다."
        )
    return True


def phone_verify(phone_number: str, code: int, redis_session) -> dict:
    verified_data = redis_session.get(phone_number)
    if not verified_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="인증정보가 존재하지 않습니다."
        )
    verified_data = dict(json.loads(verified_data.decode("utf-8")))
    if datetime.strptime(
        verified_data["created_at"], "%Y-%m-%d %H:%M:%S.%f"
    ) <= datetime.now() - timedelta(minutes=5):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="인증번호 유효시간이 지났습니다."
        )
    if verified_data["code"] != code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="인증번호가 올바르지 않습니다."
        )
    redis_session.set(
        name=phone_number,
        value=json.dumps({"verified_at": datetime.now()}, default=str),
    )
    return {phone_number: "verified"}


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

    if not re.findall("[A-Z]+", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="영문 대문자가 포함되어야 합니다."
        )

    if not re.findall("['~!@#$%^&*()_+,./<>?]+", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="특수문자가 포함되어야 합니다."
        )

    return True
