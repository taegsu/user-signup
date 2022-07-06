from datetime import datetime, timedelta
import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.common.database.redis.core import signup_session
from app.schemas.sms import MessageType


class TestSuccess:
    @pytest.mark.user_signup
    def test_유저_회원가입_성공(self, test_client: TestClient):
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

        params = {
            "phone_number": phone_number,
            "name": "김택수",
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.ok

        response_data = res.json()
        assert response_data["phone_number"] == phone_number
        assert response_data["name"] == "김택수"
        assert response_data["email"] == "sut606@gmail.com"
        assert response_data["nickname"] == "테크수"
        assert response_data["password"] == "Rlehdeo1!"
        assert response_data["is_activate"] is False


class TestFailure:
    @pytest.mark.user_signup
    def test_유저_회원가입_휴대폰인증전_실패(self, test_client: TestClient):
        phone_number = "01020608188"
        params = {
            "phone_number": phone_number,
            "name": "김택수",
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "rleh1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        response_data["description"] == "인증정보가 존재하지 않습니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_휴대폰인증전_실패2(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": "01020608188"}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.ok

        params = {
            "phone_number": phone_number,
            "name": "김택수",
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "rleh1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_404_NOT_FOUND

        response_data = res.json()
        response_data["description"] == "인증이 되지 않은 번호 입니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_인증유효시간_실패(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": "01020608188"}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.ok

        signup_session.set(
            name=phone_number,
            value=json.dumps({"verified_at": datetime.now() - timedelta(minutes=6)}, default=str),
        )

        params = {
            "phone_number": phone_number,
            "name": "김택수",
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "rleh1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_403_FORBIDDEN

        response_data = res.json()
        response_data["description"] == "인증 유효시간이 지났습니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_비밀번호_8자미만_실패(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "rleh1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        response_data = res.json()
        response_data["description"] == "비밀번호는 최소 8자 이상이어야 합니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_비밀번호_20자초과_실패(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "rlehdeo1!rlehdeo1!rlehdeo1!rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        response_data = res.json()
        response_data["description"] == "비밀번호는 최대 20자 입니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_비밀번호_숫자미포함_실패(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "rlehdeo!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        response_data = res.json()
        response_data["description"] == "숫자가 포함되어야 합니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_비밀번호_영어소문자_미포함_실패(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "R2345678!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        response_data = res.json()
        response_data["description"] == "영문 소문자가 포함되어야 합니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_비밀번호_영어대문자_미포함_실패(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        response_data = res.json()
        response_data["description"] == "영문 대문자가 포함되어야 합니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_비밀번호_특수문자_미포함_실패(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "Rlehdeo1",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        response_data = res.json()
        response_data["description"] == "특수문자가 포함되어야 합니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_핸드폰번호_존재함(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.ok

        params = {
            "phone_number": phone_number,
            "name": "택수",
            "email": "sut606@naver.com",
            "nickname": "테수",
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_409_CONFLICT

        response_data = res.json()
        assert response_data["description"] == "해당 번호는 이미 가입한 유저입니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_이메일_존재함(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.ok

        type = MessageType.signup
        phone_number2 = "01012345678"
        params = {"phone_number": phone_number2}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.ok
        code = res.json()["code"]

        res = test_client.get(
            f"/user/v1/validate?type={type}&phone_number={phone_number2}&code={code}"
        )
        assert res.ok

        params = {
            "phone_number": phone_number2,
            "name": "택수",
            "email": "sut606@gmail.com",
            "nickname": "테수",
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_409_CONFLICT

        response_data = res.json()
        assert response_data["description"] == "해당 이메일은 이미 가입한 유저입니다."

    @pytest.mark.user_signup
    def test_유저_회원가입_닉네임_존재함(self, test_client: TestClient):
        type = MessageType.signup
        phone_number = "01020608188"
        params = {"phone_number": phone_number}
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
            "email": "sut606@gmail.com",
            "nickname": "테크수",
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.ok

        phone_number2 = "01022608188"
        params = {"phone_number": phone_number2}
        res = test_client.post(f"/sms/v1/send?type={type}", json=params)
        assert res.ok
        code = res.json()["code"]

        res = test_client.get(
            f"/user/v1/validate?type={type}&phone_number={phone_number2}&code={code}"
        )
        assert res.ok

        params = {
            "phone_number": phone_number2,
            "name": "택수",
            "email": "sut606@naver.com",
            "nickname": "테크수",
            "password": "Rlehdeo1!",
        }
        res = test_client.post("/user/v1/signup", json=params)
        assert res.status_code == status.HTTP_409_CONFLICT

        response_data = res.json()
        assert response_data["description"] == "중복된 닉네임 입니다."