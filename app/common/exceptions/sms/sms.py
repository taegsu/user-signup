class SmsSendException:
    data = {
        400: {"content": {"application/json": {"example": {"description": "지원하지 않는 타입 입니다."}}}},
        404: {"content": {"application/json": {"example": {"description": "가입하지 않은 유저 입니다."}}}},
        409: {
            "content": {"application/json": {"example": {"description": "해당 번호는 이미 가입한 유저입니다."}}}
        },
    }

