import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.sms import MessageType
from app.schemas.user import LoginType
from tests.conftest import dummy_login, dummy_signup


class TestSuccess:
    @pytest.mark.user_info
    def test_유저_정보_불러오기_성공(self, test_client: TestClient):
        # 로그인
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
        headers = {"user-token": res["user_token"]}
        res = test_client.get("/user/v1/", headers=headers)
        assert res.ok

        response_data = res.json()
        assert response_data["is_activate"] is True


class TestFailure:
    @pytest.mark.user_info
    def test_유저_정보_불러오기_실패_존재하지않은_유저(self, test_client: TestClient):
        headers = {"user-token": "test_user_token"}
        res = test_client.get("/user/v1/", headers=headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "존재하지 않는 유저입니다."

    @pytest.mark.user_info
    def test_유저_정보_불러오기_실패_로그인하지않은_유저(self, test_client: TestClient):
        # 회원가입
        type = MessageType.signup
        phone_number = "01020608188"
        email = "sut606@gmail.com"
        name = "김택수"
        nickname = "테크수"
        password = "Rlehdeo1!"
        res = dummy_signup(
            test_client=test_client,
            type=type,
            phone_number=phone_number,
            email=email,
            name=name,
            nickname=nickname,
            password=password,
        )

        headers = {"user-token": res["user_token"]}
        res = test_client.get("/user/v1/", headers=headers)
        assert res.status_code == status.HTTP_403_FORBIDDEN

        response_data = res.json()
        assert response_data["description"] == "로그인 상태가 아닙니다."
