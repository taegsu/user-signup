import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.sms import MessageType
from app.schemas.user import LoginType


class TestSuccess:
    @pytest.mark.user_logout
    def test_유저_로그아웃_성공(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": "01020608188"}
        email = "sut606@gmail.com"
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.ok
        code = res.json()["code"]

        res = test_client.get(
            f"/user/v1/validate?type={type}&phone_number={phone_number}&code={code}"
        )
        assert res.ok

        params = {
            "phone_number": phone_number,
            "name": "김택수",
            "email": email,
            "nickname": "테크수",
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.ok

        headers = {"user-token": res.json()["user_token"]}
        params = {
            "login_type": LoginType.email,
            "user_info": email,
            "password": "Rlehdeo1!"
        }
        res = test_client.post("/user/v1/login", json=params)
        assert res.ok

        response_data = res.json()
        response_data["is_activate"] is True

        res = test_client.post("/user/v1/logout", headers=headers)
        print(res.text)
        assert res.ok

        response_data = res.json()
        response_data["is_activate"] is False


class TestFailure:
    @pytest.mark.user_logout
    def test_유저_로그아웃_실패(self, test_client: TestClient):
        headers = {"user-token": "test_user_token"}
        res = test_client.post("/user/v1/logout", headers=headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "존재하지 않는 유저입니다."
