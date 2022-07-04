from sqlalchemy.orm import Session
from sqlalchemy import select

from app.common.models.user import User


def get_user(*, db_session: Session, phone_number: int):
    query = select(User).where(User.phone_number == phone_number)
    res = db_session.execute(query)
    return res.scalar()
