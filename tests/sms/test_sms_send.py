import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.common.database.redis.core import reset_session as reset_redis_session
from app.common.database.redis.core import signup_session as signup_redis_session
from app.schemas.sms import MessageType
from tests.conftest import dummy_signup


class TestSuccess:
    @pytest.mark.sms_send
    def test_유저_회원가입_핸드폰번호_전송(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.ok

        response_data = res.json()

        verified_data = signup_redis_session.get(phone_number)
        assert verified_data is not None

        verified_data = dict(json.loads(verified_data.decode("utf-8")))
        assert verified_data["code"] == response_data["code"]

    @pytest.mark.sms_send
    def test_유저_비밀번호_재설정_핸드폰번호_전송(self, test_client: TestClient):
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

        type = MessageType.reset
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.ok

        response_data = res.json()

        verified_data = reset_redis_session.get(phone_number)
        assert verified_data is not None

        verified_data = dict(json.loads(verified_data.decode("utf-8")))
        assert verified_data["code"] == response_data["code"]


class TestFailure:
    @pytest.mark.sms_send
    def test_회원가입_인증_번호_전송_실패(self, test_client: TestClient):
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

        type = MessageType.signup
        params = {"phone_number": phone_number}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.status_code == status.HTTP_409_CONFLICT

        response_data = res.json()
        assert response_data["description"] == "해당 번호는 이미 가입한 유저입니다."

    @pytest.mark.sms_send
    def test_유저_비밀번호_재설정_번호_전송_실패(self, test_client: TestClient):
        type = MessageType.reset
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "가입하지 않은 유저 입니다."
