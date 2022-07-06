from fastapi import APIRouter, Depends, status, HTTPException, Header, Body
from sqlalchemy.orm import Session

from app.common.database.postgres.core import get_ro_db, get_db
from app.common.exceptions.user.login import LoginException
from app.common.exceptions.user.logout import LogoutException
from app.common.exceptions.user.reset_password import ResetPasswordException
from app.common.exceptions.user.signup import SignupException
from app.common.exceptions.user.validate import ValidateException
from app.schemas.sms import MessageType
from app.schemas.user import RequestUser, ResponseUser, RequestLogin, RequestReset
from app.service.user_service import (
    create,
    validate_phone_signup,
    validate_phone_reset_password,
    login_user,
    logout_user,
    reset_password,
)

router = APIRouter(prefix="/user/v1")


@router.get(
    "/validate",
    summary="핸드폰 번호 인증",
    responses=ValidateException.data
)
def validate(
    *, db_session: Session = Depends(get_ro_db), type: MessageType, phone_number: str, code: int
):
    if type == MessageType.signup:
        return validate_phone_signup(db_session=db_session, phone_number=phone_number, code=code)
    elif type == MessageType.reset:
        return validate_phone_reset_password(
            db_session=db_session, phone_number=phone_number, code=code
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="지원하지 않는 타입 입니다.")


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseUser,
    responses=SignupException.data
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


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUser,
    responses=LoginException.data
)
def login(*, req: RequestLogin, db_session: Session = Depends(get_db)):
    return login_user(
        login_type=req.login_type,
        user_info=req.user_info,
        password=req.password,
        db_session=db_session,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUser,
    responses=LogoutException.data
)
def logout(
    *, user_token: str = Header(..., description="유저 토큰"), db_session: Session = Depends(get_db)
):
    return logout_user(user_token=user_token, db_session=db_session)


@router.patch(
    "/reset",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUser,
    responses=ResetPasswordException.data
)
def reset(
    *,
    req: RequestReset,
    db_session: Session = Depends(get_db)
):
    return reset_password(
        phone_number=req.phone_number,
        password=req.password,
        db_session=db_session,
    )
