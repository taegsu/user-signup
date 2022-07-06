import pytest
from starlette.testclient import TestClient
from sqlalchemy import delete

from app.common.database.postgres.core import Base, engine, SessionLocal
from app.common.database.redis.core import signup_session as signup_redis_session
from app.common.database.redis.core import reset_session as reset_redis_session
from app.common.models.user import User
from app.main import app
from app.schemas.sms import MessageType
from app.schemas.user import LoginType


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
    keys = signup_redis_session.keys("*")
    if keys:
        signup_redis_session.delete(*keys)
    keys = reset_redis_session.keys("*")
    if keys:
        reset_redis_session.delete(*keys)
    signup_redis_session.quit()
    reset_redis_session.quit()
    query = delete(User)
    db_session.execute(query)
    db_session.commit()
    db_session.close()
    return


def dummy_send_validate_code(test_client: TestClient, type: MessageType, phone_number: str):
    params = {"phone_number": phone_number}
    res = test_client.post(f"/sms/v1/send?type={type}", json=params)
    code = res.json()["code"]
    return code


def dummy_verify_code(test_client: TestClient, type: MessageType, phone_number: str):
    code = dummy_send_validate_code(test_client=test_client, type=type, phone_number=phone_number)
    return test_client.get(f"/user/v1/validate?type={type}&phone_number={phone_number}&code={code}")


def dummy_signup(
    test_client: TestClient,
    type: MessageType,
    phone_number: str,
    name: str,
    email: str,
    nickname: str,
    password: str,
):
    dummy_verify_code(test_client=test_client, type=type, phone_number=phone_number)

    params = {
        "phone_number": phone_number,
        "name": name,
        "email": email,
        "nickname": nickname,
        "password": password,
    }
    res = test_client.post("/user/v1/signup", json=params)

    response_data = res.json()
    return response_data


def dummy_login(
    test_client: TestClient,
    signup_type: MessageType,
    login_type: LoginType,
    phone_number: str,
    name: str,
    email: str,
    nickname: str,
    password: str,
):
    res = dummy_signup(
        test_client=test_client,
        type=signup_type,
        phone_number=phone_number,
        email=email,
        name=name,
        nickname=nickname,
        password=password,
    )
    if login_type == LoginType.phone_number:
        params = {
            "login_type": login_type,
            "user_info": phone_number,
            "password": password,
        }
    elif login_type == LoginType.email:
        params = {
            "login_type": login_type,
            "user_info": email,
            "password": password,
        }
    res = test_client.post("/user/v1/login", json=params)
    return res.json()
