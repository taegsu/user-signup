class SignupException:
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
        403: {"content": {"application/json": {"example": {"description": "인증 유효시간이 지났습니다."}}}},
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
                    }
                }
            }
        },
        409: {
            "content": {
                "application/json": {
                    "examples": {
                        "해당 번호는 이미 가입한 유저입니다.": {
                            "value": {"description": "해당 번호는 이미 가입한 유저입니다."},
                        },
                        "해당 이메일은 이미 가입한 유저입니다.": {
                            "value": {"description": "해당 이메일은 이미 가입한 유저입니다."},
                        },
                        "중복된 닉네임 입니다.": {
                            "value": {"description": "중복된 닉네임 입니다."},
                        },
                    }
                }
            }
        },
    }
