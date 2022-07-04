from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.database.postgres.core import get_ro_db
from app.service.user_service import validate_phone

router = APIRouter(prefix="/user/v1")


@router.get(
    "/validate",
    summary="핸드폰 번호 인증",
    responses={
        404: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "존재하지 않는 유저입니다.": {
                                "value": {"description": "존재하지 않는 유저입니다."}
                            }
                        },
                        {
                            "인증정보가 존재하지 않습니다.": {
                                "value": {"description": "인증정보가 존재하지 않습니다."}
                            }
                        },
                        {
                            "인증번호 유효시간이 지났습니다.": {
                                "value": {"description": "인증번호 유효시간이 지났습니다."}
                            }
                        },
                        {
                            "인증번호가 올바르지 않습니다.": {
                                "value": {"description": "인증번호가 올바르지 않습니다."}
                            }
                        },
                    ]
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
    *, db_session: Session = Depends(get_ro_db), type: str, phone_number: int, code: int
):
    return validate_phone(
        db_session=db_session, type=type, phone_number=phone_number, code=code
    )
