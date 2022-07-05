from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.database.postgres.core import get_ro_db, get_db
from app.schemas.sms import MessageType
from app.schemas.user import RequestUser, ResponseUser
from app.service.user_service import validate_phone, create


router = APIRouter(prefix="/user/v1")


@router.get(
    "/validate",
    summary="핸드폰 번호 인증",
    responses={
        400: {
            "content": {
                "application/json": {"example": {"description": "지원하지 않는 타입 입니다."}}
            }
        },
        404: {
            "content": {
                "application/json": {
                    "examples": {
                        "존재하지 않는 유저입니다.": {"value": {"description": "존재하지 않는 유저입니다."}},
                        "인증정보가 존재하지 않습니다.": {
                            "value": {"description": "인증정보가 존재하지 않습니다."}
                        },
                        "인증번호 유효시간이 지났습니다.": {
                            "value": {"description": "인증번호 유효시간이 지났습니다."}
                        },
                        "인증번호가 올바르지 않습니다.": {
                            "value": {"description": "인증번호가 올바르지 않습니다."}
                        },
                    }
                }
            }
        },
        409: {
            "content": {
                "application/json": {"example": {"description": "이미 가입한 유저입니다."}}
            }
        },
    },
)
def validate(
    *,
    db_session: Session = Depends(get_ro_db),
    type: MessageType,
    phone_number: int,
    code: int
):
    return validate_phone(
        db_session=db_session, type=type, phone_number=phone_number, code=code
    )


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseUser,
    responses={
        400: {
            "content": {
                "application/json": {
                    "examples": {
                        "비밀번호는 최소 8자 이상이어야 합니다.": {
                            "value": {"description": "비밀번호는 최소 8자 이상이어야 합니다."},
                        },
                        "비밀번호는 최대 20자 입니다.": {
                            "value": {"description": "비밀번호는 최대 20자 입니다."},
                        },
                        "숫자가 포함되어야 합니다.": {
                            "value": {"description": "숫자가 포함되어야 합니다."},
                        },
                        "영문 소문자가 포함되어야 합니다.": {
                            "value": {"description": "숫자가 포함되어야 합니다."},
                        },
                        "특수문자가 포함되어야 합니다.": {
                            "value": {"description": "특수문자가 포함되어야 합니다."},
                        },
                    }
                }
            }
        },
        404: {
            "content": {
                "application/json": {
                    "examples": {
                        "인증정보가 존재하지 않습니다.": {
                            "value": {"description": "인증정보가 존재하지 않습니다."},
                        },
                        "인증이 되지 않은 번호 입니다.": {
                            "value": {"description": "인증이 되지 않은 번호 입니다."},
                        },
                        "인증 유효시간이 지났습니다.": {
                            "value": {"description": "인증 유효시간이 지났습니다."},
                        },
                    }
                }
            }
        },
        409: {
            "content": {
                "application/json": {
                    "examples": {
                        "해당 번호는 이미 가입한 유저입니다.": {
                            "value": {"description": "해당 번호는 이미 가입한 유저입니다."},
                        },
                        "해당 이메일은 이미 가입한 유저입니다.": {
                            "value": {"description": "해당 이메일은 이미 가입한 유저입니다."},
                        },
                        "중복된 닉네임 입니다.": {
                            "value": {"description": "중복된 닉네임 입니다."},
                        },
                    }
                }
            }
        },
    },
)
def signup(*, db_session: Session = Depends(get_db), req: RequestUser):
    return create(
        db_session=db_session,
        phone_number=req.phone_number,
        name=req.name,
        email=req.email,
        nickname=req.nickname,
        password=req.password,
    )
