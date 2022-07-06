class ValidateException:
    data = {
        400: {"content": {"application/json": {"example": {"description": "지원하지 않는 타입 입니다."}}}},
        403: {"content": {"application/json": {"example": {"description": "인증번호 유효시간이 지났습니다."}}}},
        404: {
            "content": {
                "application/json": {
                    "examples": {
                        "존재하지 않는 유저입니다.": {"value": {"description": "존재하지 않는 유저입니다."}},
                        "인증정보가 존재하지 않습니다.": {"value": {"description": "인증정보가 존재하지 않습니다."}},
                        "인증번호가 올바르지 않습니다.": {"value": {"description": "인증번호가 올바르지 않습니다."}},
                    }
                }
            }
        },
        409: {"content": {"application/json": {"example": {"description": "이미 가입한 유저입니다."}}}},
    }
