import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.sms import MessageType
from app.schemas.user import LoginType
from tests.conftest import dummy_signup


class TestSuccess:
    @pytest.mark.user_login
    def test_유저_이메일_로그인_성공(self, test_client: TestClient):
        # 회원가입
        type = MessageType.signup
        phone_number = "01020608188"
        email = "sut606@gmail.com"
        name = "김택수"
        nickname = "테크수"
        password = "Rlehdeo1!"
        dummy_signup(
            test_client=test_client,
            type=type,
            phone_number=phone_number,
            email=email,
            name=name,
            nickname=nickname,
            password=password,
        )

        # 로그인
        params = {"login_type": LoginType.email, "user_info": email, "password": password}
        res = test_client.post("/user/v1/login", json=params)
        assert res.ok

        response_data = res.json()
        assert response_data["is_activate"] is True

    @pytest.mark.user_login
    def test_유저_핸드폰번호_로그인_성공(self, test_client: TestClient):
        # 회원가입
        type = MessageType.signup
        phone_number = "01020608188"
        email = "sut606@gmail.com"
        name = "김택수"
        nickname = "테크수"
        password = "Rlehdeo1!"
        dummy_signup(
            test_client=test_client,
            type=type,
            phone_number=phone_number,
            email=email,
            name=name,
            nickname=nickname,
            password=password,
        )

        # 로그인
        params = {
            "login_type": LoginType.phone_number,
            "user_info": phone_number,
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/login", json=params)
        assert res.ok

        response_data = res.json()
        assert response_data["is_activate"] is True


class TestFailure:
    @pytest.mark.user_signup
    def test_유저_로그인_타입_실패(self, test_client: TestClient):
        # 회원가입
        type = MessageType.signup
        phone_number = "01020608188"
        email = "sut606@gmail.com"
        name = "김택수"
        nickname = "테크수"
        password = "Rlehdeo1!"
        dummy_signup(
            test_client=test_client,
            type=type,
            phone_number=phone_number,
            email=email,
            name=name,
            nickname=nickname,
            password=password,
        )

        # 로그인
        params = {"login_type": "address", "user_info": "서울특별시", "password": "Rlehdeo1!"}
        res = test_client.post("/user/v1/login", json=params)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.user_signup
    def test_유저_로그인_실패(self, test_client: TestClient):
        # 회원가입
        type = MessageType.signup
        phone_number = "01020608188"
        email = "sut606@gmail.com"
        name = "김택수"
        nickname = "테크수"
        password = "Rlehdeo1!"
        dummy_signup(
            test_client=test_client,
            type=type,
            phone_number=phone_number,
            email=email,
            name=name,
            nickname=nickname,
            password=password,
        )

        # 로그인
        params = {
            "login_type": LoginType.phone_number,
            "user_info": phone_number,
            "password": "Rlehdeo1!!",
        }
        res = test_client.post("/user/v1/login", json=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "아이디 비밀번호를 확인해주세요."
