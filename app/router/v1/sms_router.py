from fastapi import APIRouter, Query, Depends
from fastapi import status
from sqlalchemy.orm import Session

from app.common.database.postgres.core import get_ro_db
from app.schemas.sms import PhoneNumber, MessageType
from app.service.sms_service import send


router = APIRouter(prefix="/sms/v1")


@router.post(
    "/send",
    status_code=status.HTTP_200_OK,
    summary="SMS 전송",
    responses={
        400: {
            "content": {
                "application/json": {"example": {"description": "지원하지 않는 타입 입니다."}}
            }
        },
        404: {
            "content": {
                "application/json": {"example": {"description": "가입하지 않은 유저 입니다."}}
            }
        },
        409: {
            "content": {
                "application/json": {"example": {"description": "해당 번호는 이미 가입한 유저입니다."}}
            }
        },
    },
)
def send_message(
    *,
    db_session: Session = Depends(get_ro_db),
    type: MessageType = Query(..., description="메세지 종류(signup or reset)"),
    phone_number: PhoneNumber
):
    return send(
        db_session=db_session, type=type, phone_number=phone_number.phone_number
    )
