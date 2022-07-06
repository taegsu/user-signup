from uuid import uuid4

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.common.models.user import User


def get_user_by_phone_number(*, db_session: Session, phone_number: int) -> User:
    query = select(User).where(User.phone_number == phone_number)
    res = db_session.execute(query)
    return res.scalar()


def get_user_by_email(*, db_session: Session, email: str) -> User:
    query = select(User).where(User.email == email)
    res = db_session.execute(query)
    return res.scalar()


def get_user_by_nickname(*, db_session: Session, nickname: str) -> User:
    query = select(User).where(User.nickname == nickname)
    res = db_session.execute(query)
    return res.scalar()


def get_user_by_user_token(*, db_session: Session, user_token: str) -> User:
    query = select(User).where(User.user_token == user_token)
    res = db_session.execute(query)
    return res.scalar()


def get_user_by_email_password(*, db_session: Session, email: str, password: str) -> User:
    query = select(User).where(User.email == email, User.password == password)
    res = db_session.execute(query)
    return res.scalar()


def get_user_by_phone_password(*, db_session: Session, phone_number: str, password: str) -> User:
    query = select(User).where(User.phone_number == phone_number, User.password == password)
    res = db_session.execute(query)
    return res.scalar()


def create_user(
    *, db_session: Session, phone_number: str, name: str, email: str, nickname: str, password: str
) -> User:
    user = User(
        user_token=uuid4(),
        phone_number=phone_number,
        name=name,
        email=email,
        nickname=nickname,
        password=password,
    )
    db_session.add(user)
    return user
