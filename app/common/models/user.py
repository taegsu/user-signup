from sqlalchemy import Column, String, Integer, DateTime, func, Boolean

from app.common.database.postgres.core import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_token = Column(String, nullable=False, comment="유저 토큰", unique=True, index=True)
    email = Column(String, nullable=False, comment="이메일", unique=True)
    nickname = Column(String, nullable=False, comment="닉네임", unique=True)
    password = Column(String, nullable=False, comment="비밀번호")
    name = Column(String, nullable=False, comment="이름")
    phone_number = Column(Integer, nullable=False, comment="전화번호", unique=True)
    is_activate = Column(Boolean, default=False, comment="로그인 여부")
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
