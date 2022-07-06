import pytest
from starlette.testclient import TestClient
from sqlalchemy import delete

from app.common.database.postgres.core import Base, engine, SessionLocal
from app.common.database.redis.core import signup_session as signup_redis_session
from app.common.database.redis.core import reset_session as reset_redis_session
from app.common.models.user import User
from app.main import app


@pytest.fixture(scope="session")
def session():
    db_session = SessionLocal()
    yield db_session


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)


@pytest.fixture(scope="class", autouse=True)
def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    db_session = SessionLocal()
    keys = signup_redis_session.keys('*')
    if keys:
        signup_redis_session.delete(*keys)
    keys = reset_redis_session.keys('*')
    if keys:
        reset_redis_session.delete(*keys)
    signup_redis_session.quit()
    reset_redis_session.quit()
    query = delete(User)
    db_session.execute(query)
    db_session.commit()
    db_session.close()
    return

