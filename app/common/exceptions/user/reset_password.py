class ResetPasswordException:
    data = {
        400: {
            "content": {
                "application/json": {
                    "examples": {
                        "비밀번호는 최소 8자 이상이어야 합니다.": {
                            "value": {"description": "비밀번호는 최소 8자 이상이어야 합니다."},
                        },
                        "비밀번호는 최대 20자 입니다.": {
                            "value": {"description": "비밀번호는 최대 20자 입니다."},
                        },
                        "숫자가 포함되어야 합니다.": {
                            "value": {"description": "숫자가 포함되어야 합니다."},
                        },
                        "영문 소문자가 포함되어야 합니다.": {
                            "value": {"description": "영문 소문자가 포함되어야 합니다."},
                        },
                        "영문 대문자가 포함되어야 합니다.": {
                            "value": {"description": "영문 대문자가 포함되어야 합니다."},
                        },
                        "특수문자가 포함되어야 합니다.": {
                            "value": {"description": "특수문자가 포함되어야 합니다."},
                        },
                    }
                }
            }
        },
        403: {
            "content": {
                "application/json": {
                    "examples": {
                        "인증 유효시간이 지났습니다.": {
                            "value": {"description": "인증 유효시간이 지났습니다."},
                        },
                        "로그인 상태에서는 변경할 수 없습니다.": {
                            "value": {"description": "로그인 상태에서는 변경할 수 없습니다."},
                        },
                    }
                }
            }
        },
        404: {
            "content": {
                "application/json": {
                    "examples": {
                        "인증정보가 존재하지 않습니다.": {
                            "value": {"description": "인증정보가 존재하지 않습니다."},
                        },
                        "인증이 되지 않은 번호 입니다.": {
                            "value": {"description": "인증이 되지 않은 번호 입니다."},
                        },
                        "존재하지 않는 유저입니다.": {
                            "value": {"description": "존재하지 않는 유저입니다."},
                        },
                    }
                }
            }
        },
        409: {
            "content": {"application/json": {"example": {"description": "같은 비밀번호로 변경할 수 없습니다."}}}
        },
    }
