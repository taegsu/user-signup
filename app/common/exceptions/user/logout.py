class LogoutException:
    data = {
        404: {"content": {"application/json": {"example": {"description": "존재하지 않는 유저입니다."}}}},
    }
