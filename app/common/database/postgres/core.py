from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{name}".format(
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_host,
    port=settings.database_port,
    name=settings.database_name,
)
SQLALCHEMY_RO_DATABASE_URI = (
    "postgresql+psycopg2://{username}:{password}@{host}:{port}/{name}".format(
        username=settings.ro_database_username,
        password=settings.ro_database_password,
        host=settings.database_host,
        port=settings.database_port,
        name=settings.database_name,
    )
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    max_overflow=settings.sqlalchemy_max_overflow,
    pool_size=settings.sqlalchemy_pool_size,
    pool_recycle=settings.sqlalchemy_pool_recycle,
    pool_timeout=settings.sqlalchemy_pool_timeout,
    connect_args={"application_name": settings.app_name},
)
ro_engine = create_engine(
    SQLALCHEMY_RO_DATABASE_URI,
    max_overflow=settings.sqlalchemy_max_overflow,
    pool_size=settings.sqlalchemy_pool_size,
    pool_recycle=settings.sqlalchemy_pool_recycle,
    pool_timeout=settings.sqlalchemy_pool_timeout,
    connect_args={"application_name": settings.app_name},
)

WARNING = "\33[{}mWARNING: YOU ARE CONNECTING TO THE ({}) DATABASE - {}.\33[0m"
if settings.env in ("staging", "prod"):
    print(WARNING.format("91", settings.env, engine.url.host))
elif settings.env in ("dev",):
    print(WARNING.format("33", settings.env, engine.url.host))
elif settings.env in ("local", "test"):
    print(WARNING.format("36", settings.env, engine.url.host))


SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
ROSessionLocal = sessionmaker(bind=ro_engine, autoflush=False, expire_on_commit=False)


Base = declarative_base()


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_ro_db() -> ROSessionLocal:
    db = ROSessionLocal()
    try:
        yield db
    finally:
        db.close()
