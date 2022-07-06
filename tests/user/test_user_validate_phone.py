from datetime import datetime, timedelta
import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.common.database.redis.core import signup_session as signup_redis_session
from app.common.database.redis.core import reset_session as reset_redis_session
from app.schemas.sms import MessageType
from tests.conftest import dummy_send_validate_code, dummy_signup


class TestSuccess:
    @pytest.mark.user_validate
    def test_회원가입_핸드폰번호_인증_성공(self, test_client: TestClient):
        # 인증코드 발송
        phone_number = "01020608188"
        type = MessageType.signup
        code = dummy_send_validate_code(
            test_client=test_client, phone_number=phone_number, type=type
        )

        params = {"type": type, "phone_number": phone_number, "code": code}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.ok

        verified_data = signup_redis_session.get(phone_number)
        assert verified_data is not None

        verified_data = dict(json.loads(verified_data.decode("utf-8")))
        assert verified_data.get("verified_at", None) is not None

    @pytest.mark.user_validate
    def test_비밀번호_재설정_핸드폰번호_인증_성공(self, test_client: TestClient):
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

        # 인증코드 발송
        type = MessageType.reset
        code = dummy_send_validate_code(
            test_client=test_client, phone_number=phone_number, type=type
        )

        params = {"type": type, "phone_number": phone_number, "code": code}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.ok

        verified_data = reset_redis_session.get(phone_number)
        assert verified_data is not None

        verified_data = dict(json.loads(verified_data.decode("utf-8")))
        assert verified_data.get("verified_at", None) is not None


class TestFailure:
    @pytest.mark.user_validate
    def test_핸드폰번호_인증_실패_지원하지_않는_타입(self, test_client: TestClient):
        # 인증코드 발송
        phone_number = "01020608188"

        params = {"type": "resignup", "phone_number": phone_number, "code": 1234}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.user_validate
    def test_회원가입_핸드폰번호_인증_실패_인증번호_없음(self, test_client: TestClient):
        # 인증코드 발송
        phone_number = "01020608188"
        type = MessageType.signup

        params = {"type": type, "phone_number": phone_number, "code": 1234}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "인증정보가 존재하지 않습니다."

    @pytest.mark.user_validate
    def test_비밀번호_재설정_핸드폰번호_인증_실패_인증번호_없음(self, test_client: TestClient):
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
        params = {"type": type, "phone_number": phone_number, "code": 1234}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "인증정보가 존재하지 않습니다."

    @pytest.mark.user_validate
    def test_핸드폰번호_인증_실패_인증번호_없음(self, test_client: TestClient):
        # 인증코드 발송
        phone_number = "01020608188"
        type = MessageType.signup

        params = {"type": type, "phone_number": phone_number, "code": 1234}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "인증정보가 존재하지 않습니다."

    @pytest.mark.user_validate
    def test_핸드폰번호_인증_실패_인증코드_다름(self, test_client: TestClient):
        # 인증코드 발송
        phone_number = "01020608188"
        type = MessageType.signup
        code = dummy_send_validate_code(
            test_client=test_client, phone_number=phone_number, type=type
        )

        params = {"type": type, "phone_number": phone_number, "code": code-1}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "인증번호가 올바르지 않습니다."

    @pytest.mark.user_validate
    def test_비밀번호_재설정_인증_실패_가입하지않은_유저(self, test_client: TestClient):
        # 인증코드 발송
        phone_number = "01020608188"
        type = MessageType.reset

        params = {"type": type, "phone_number": phone_number, "code": 1234}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        assert response_data["description"] == "존재하지 않는 유저입니다."

    @pytest.mark.user_validate
    def test_회원가입_인증_실패_이미_가입한_유저(self, test_client: TestClient):
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

        params = {"type": type, "phone_number": phone_number, "code": 1234}
        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_409_CONFLICT

        response_data = res.json()
        assert response_data["description"] == "이미 가입한 유저입니다."

    @pytest.mark.user_validate
    def test_회원가입_인증_실패_인증번호_유효시간_지남(self, test_client: TestClient):
        # 인증코드 발송
        phone_number = "01020608188"
        type = MessageType.signup
        code = dummy_send_validate_code(
            test_client=test_client, phone_number=phone_number, type=type
        )

        # 인증시간 변경
        signup_redis_session.set(
            name=phone_number,
            value=json.dumps({"created_at": datetime.now() - timedelta(minutes=2, seconds=30),
                              "code": code}, default=str),
        )
        params = {"type": type, "phone_number": phone_number, "code": code}

        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_403_FORBIDDEN

        response_data = res.json()
        assert response_data["description"] == "인증번호 유효시간이 지났습니다."

    @pytest.mark.user_validate
    def test_비밀번호_재설정_인증_실패_유효시간_지남(self, test_client: TestClient):
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
        code = dummy_send_validate_code(
            test_client=test_client, phone_number=phone_number, type=type
        )

        # 인증시간 변경
        reset_redis_session.set(
            name=phone_number,
            value=json.dumps({"created_at": datetime.now() - timedelta(minutes=2, seconds=30),
                              "code": code}, default=str),
        )

        params = {"type": type, "phone_number": phone_number, "code": code}

        res = test_client.get("/user/v1/validate", params=params)
        assert res.status_code == status.HTTP_403_FORBIDDEN

        response_data = res.json()
        assert response_data["description"] == "인증번호 유효시간이 지났습니다."
