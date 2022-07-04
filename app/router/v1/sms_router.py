from fastapi import APIRouter, Query
from fastapi import status

from app.schemas.sms import PhoneNumber
from app.service.sms_service import send

router = APIRouter(prefix="/sms/v1")


@router.post(
    "/send",
    status_code=status.HTTP_200_OK,
    summary="SMS 전송",
)
def send_message(
    *,
    type: str = Query(..., description="메세지 종류(signup or reset)"),
    phone_number: PhoneNumber
):
    return send(type=type, phone_number=phone_number.phone_number)
