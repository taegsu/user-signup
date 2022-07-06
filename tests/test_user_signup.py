import pytest
from fastapi.testclient import TestClient

from app.schemas.sms import MessageType
from tests.conftest import init_redis


class TestSuccess:
    @pytest.fixture(autouse=True, scope="class")
    def setup(self):
        init_redis()

    @pytest.mark.user_signup
    def test_유저_회원가입(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": "01020608188"}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.ok
        code = res.json()["code"]

        res = test_client.get(
            f"/user/v1/validate?type={type}&phone_number={phone_number}&code={code}"
        )
        assert res.ok

        params = {"phone_number": phone_number,
                  "name": "김택수",
                  "email": "sut606@gmail.com",
                  "nickname": "테크수",
                  "password": "rlehdeo1!"}
        res = test_client.post("/user/v1/signup", json=params)
        assert res.ok

        response_data = res.json()
        assert response_data["phone_number"] == phone_number
        assert response_data["name"] == "김택수"
        assert response_data["email"] == "sut606@gmail.com"
        assert response_data["nickname"] == "테크수"
        assert response_data["password"] == "rlehdeo1!"
        assert response_data["is_activate"] is False
