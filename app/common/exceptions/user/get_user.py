class GetUserException:
    data = {
        403: {"content": {"application/json": {"example": {"description": "로그인 상태가 아닙니다."}}}},
        404: {"content": {"application/json": {"example": {"description": "존재하지 않는 유저입니다."}}}},
    }
