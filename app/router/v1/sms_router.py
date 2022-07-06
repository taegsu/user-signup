from fastapi import APIRouter, Query, Depends
from fastapi import status
from sqlalchemy.orm import Session

from app.common.database.postgres.core import get_ro_db
from app.common.exceptions.sms.sms import SmsSendException
from app.schemas.sms import PhoneNumber, MessageType
from app.service.sms_service import send


router = APIRouter(prefix="/sms/v1")


@router.post(
    "/send", status_code=status.HTTP_200_OK, summary="SMS 전송", responses=SmsSendException.data
)
def send_message(
    *,
    db_session: Session = Depends(get_ro_db),
    type: MessageType = Query(..., description="메세지 종류(signup or reset)"),
    phone_number: PhoneNumber
):
    return send(db_session=db_session, type=type, phone_number=phone_number.phone_number)
