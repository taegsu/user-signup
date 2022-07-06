import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.sms import MessageType
from app.schemas.user import LoginType
from tests.conftest import dummy_signup, dummy_login


class TestSuccess:
    @pytest.mark.user_logout
    def test_유저_로그아웃_성공(self, test_client: TestClient):
        # 회원가입
        type = MessageType.signup
        login_type = LoginType.email
        phone_number = "01020608188"
        email = "sut606@gmail.com"
        name = "김택수"
        nickname = "테크수"
        password = "Rlehdeo1!"
        res = dummy_login(
            test_client=test_client,
            signup_type=type,
            login_type=login_type,
            phone_number=phone_number,
            email=email,
            name=name,
            nickname=nickname,
            password=password,
        )
        assert res["is_activate"] is True
        headers = {"user-token": res["user_token"]}

        # 로그아웃
        res = test_client.post("/user/v1/logout", headers=headers)
        assert res.ok

        response_data = res.json()
        assert response_data["is_activate"] is False


class TestFailure:
    @pytest.mark.user_logout
    def test_유저_로그아웃_실패(self, test_client: TestClient):
        headers = {"user-token": "test_user_token"}
        res = test_client.post("/user/v1/logout", headers=headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "존재하지 않는 유저입니다."
