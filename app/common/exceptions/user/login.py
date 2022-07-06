class LoginException:
    data = {
        400: {"content": {"application/json": {"example": {"description": "지원하지 않는 타입 입니다."}}}},
        404: {"content": {"application/json": {"example": {"description": "아이디 비밀번호를 확인해주세요."}}}},
    }
