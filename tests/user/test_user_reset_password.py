import json
from datetime import datetime, timedelta

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.sms import MessageType
from app.schemas.user import LoginType
from app.common.database.redis.core import reset_session as reset_redis_session
from tests.conftest import dummy_signup, dummy_verify_code, dummy_login, dummy_send_validate_code


class TestSuccess:
    @pytest.mark.user_reset_password
    def test_유저_비밀번호_재설정_성공(self, test_client: TestClient):
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
        user_token = res["user_token"]

        # 비밀번호 재설정 전화번호 인증
        type = MessageType.reset
        dummy_verify_code(test_client=test_client, type=type, phone_number=phone_number)

        headers = {"user-token": user_token}
        params = {
            "password": "Rlehdeo1!",
            "reset_password": "Eoehdrl1!",
        }
        res = test_client.patch("/user/v1/reset", json=params, headers=headers)
        assert res.ok

        response_data = res.json()
        assert response_data["password"] == "Eoehdrl1!"


class TestFailure:
    @pytest.mark.user_reset_password
    def test_유저_비밀번호_재설정_실패_존재하지않은_유저(self, test_client: TestClient):
        headers = {"user-token": "test_user_token"}
        params = {
            "password": "Rlehdeo1!",
            "reset_password": "Eoehdrl1!",
        }
        res = test_client.patch("/user/v1/reset", json=params, headers=headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "존재하지 않는 유저입니다."

    @pytest.mark.user_reset_password
    def test_유저_로그인시_비밀번호_재설정_실패(self, test_client: TestClient):
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

        # 비밀번호 재설정 전화번호 인증
        type = MessageType.reset
        dummy_verify_code(test_client=test_client, type=type, phone_number=phone_number)

        # 비밀번호 재설정
        params = {
            "password": "Rlehdeo1!",
            "reset_password": "Eoehdrl1!",
        }
        res = test_client.patch("/user/v1/reset", json=params, headers=headers)
        assert res.status_code == status.HTTP_403_FORBIDDEN

        response_data = res.json()
        assert response_data["description"] == "로그인 상태에서는 변경할 수 없습니다."

    @pytest.mark.user_reset_password
    def test_유저_비밀번호_재설정_실패_인증정보_없음(self, test_client: TestClient):
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
        assert res["is_activate"] is False
        headers = {"user-token": res["user_token"]}

        # 비밀번호 재설정
        params = {
            "password": "Rlehdeo1!",
            "reset_password": "Eoehdrl1!",
        }
        res = test_client.patch("/user/v1/reset", json=params, headers=headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "인증정보가 존재하지 않습니다."

    @pytest.mark.user_reset_password
    def test_유저_비밀번호_재설정_실패_인증전(self, test_client: TestClient):
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
        assert res["is_activate"] is False
        headers = {"user-token": res["user_token"]}

        # 인증번호 전송
        type = MessageType.reset
        dummy_send_validate_code(test_client=test_client, type=type, phone_number=phone_number)

        # 비밀번호 재설정
        params = {
            "password": "Rlehdeo1!",
            "reset_password": "Eoehdrl1!",
        }
        res = test_client.patch("/user/v1/reset", json=params, headers=headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "인증이 되지 않은 번호 입니다."

    @pytest.mark.user_reset_password
    def test_유저_비밀번호_재설정_실패_인증시간_초과(self, test_client: TestClient):
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
        user_token = res["user_token"]

        # 비밀번호 재설정 전화번호 인증
        type = MessageType.reset
        dummy_verify_code(test_client=test_client, type=type, phone_number=phone_number)

        # 인증시간 변경
        reset_redis_session.set(
            name=phone_number,
            value=json.dumps({"verified_at": datetime.now() - timedelta(minutes=6)}, default=str),
        )

        headers = {"user-token": user_token}
        params = {
            "password": "Rlehdeo1!",
            "reset_password": "Eoehdrl1!",
        }
        res = test_client.patch("/user/v1/reset", json=params, headers=headers)
        assert res.status_code == status.HTTP_403_FORBIDDEN

        response_data = res.json()
        assert response_data["description"] == "인증 유효시간이 지났습니다."

    @pytest.mark.user_reset_password
    def test_유저_비밀번호_재설정_후_다시_재설정_실패(self, test_client: TestClient):
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
        user_token = res["user_token"]

        # 비밀번호 재설정 전화번호 인증
        type = MessageType.reset
        dummy_verify_code(test_client=test_client, type=type, phone_number=phone_number)

        headers = {"user-token": user_token}
        params = {
            "password": "Rlehdeo1!",
            "reset_password": "Eoehdrl1!",
        }
        res = test_client.patch("/user/v1/reset", json=params, headers=headers)
        assert res.ok

        response_data = res.json()
        assert response_data["password"] == "Eoehdrl1!"

        params = {
            "password": "Eoehdrl1!",
            "reset_password": "Rlehdeo1!",
        }
        res = test_client.patch("/user/v1/reset", json=params, headers=headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "인증정보가 존재하지 않습니다."
