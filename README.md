# User SingUp API
- --
## Dependency
- Docker
- Python3.9
- sqlalchemy
- fastapi
- redis
- --
## 실행 방법
### 1. Set Docker (Postgresql & Redis)
```
# RUN postgresql Docker
$ docker run --name user-test-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=user -d postgres:12.2-alpine

# RUN Redis Docker
$ docker run --name user-test-redis -p 6379:6379 -d redis:6.2-alpine
```
### 2. Run Server
패키지에 대한 차이가 있을수 있기 때문에 python3.9 버전으로 실행 부탁 드리겠습니다.
```
# Create Virtualenv
$ python3.9 -m venv .venv
$ source .venv/bin/activate

# Install Package
$ poetry install -n

# Table Create
$ poetry run alembic upgrade head

# Run FastAPI Server
$ poetry run uvicorn app.main:app --host 0.0.0.0
```
- --
## 과제 설명
### 최종 구현된 범위
#### Swagger
- localhost:8000/docs
#### 1. 문자 전송 기능
- 회원가입, 비밀번호 재설정에 대한 type으로 보내게 설정했습니다.
- 인증 코드를 Redis에 3분 동안 저장하도록 설정 하였습니다.
- Query Parameter
  - type(Enum)
    - signup : 회원 가입
    - reset : 비밀번호 재설정
- Reqeust Body : phone_number: string
```
# Request URL
$ http://localhost:8000/sms/v1/send

## Example ##
# Curl Message
$ curl -X 'POST' \
  'http://localhost:8000/sms/v1/send?type=signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "phone_number": "01021618188"
}'
# Response Body
{
  "created_at": "2022-07-06T20:53:16.987232",
  "code": 8607
}
```
#### 2. 전화 번호 인증 기능
- Redis에 저장된 전화번호 값을 키값으로 전송시간과 code를 저장하고 있다.
- 인증 코드를 2분 내에 입력하지 않으면 유효시간에 대한 에러가 발생되도록 설정했습니다.
- 회원가입은 0번 DB, 비밀번호 재설정은 1번 DB에 저장하고 있습니다.
- Query Paramter
  - type
    - signup : 회원 가입
    - reset : 비밀번호 재설정
  - phone_number: 휴대폰 번호(str)
  - code: 인증코드(int)
```
# URL
$ http://localhost:8000/user/v1/validate

## Example ##
# Curl
$ curl -X 'GET' \
  'http://localhost:8000/user/v1/validate?type=signup&phone_number=01021618188&code=8607' \
  -H 'accept: application/json'
 
# Response Body
{
  "01021618188": "verified"
}
```

#### 3. 회원 가입 기능
- 전화 번호 인증이 된 휴대폰 번호만 회원가입이 진행되도록 하였다.
- 전화 번호 인증이 되어도 5분 내에 회원가입을 하지 않으면 에러가 발생되도록 설정했습니다.
- Request Body
  - email: string
  - nickname: string
  - password: string
  - name: string
  - phone_number: string
```
# URL
$ http://localhost:8000/user/v1/signup

## Example ##
# Curl
$ curl -X 'POST' \
  'http://localhost:8000/user/v1/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "abc@gamil.com",
  "nickname": "에이블리",
  "password": "Rlehdeo1!",
  "name": "택수킴킴",
  "phone_number": "01021618188"
}'

# Response Body
{
  "id": 4,
  "user_token": "f0dfc688-d693-4499-8332-09fb5b9e2837",
  "email": "abc@gamil.com",
  "nickname": "에이블리",
  "password": "Rlehdeo1!",
  "name": "택수킴킴",
  "phone_number": "01021618188",
  "is_activate": false,
  "created_at": "2022-07-06T12:21:56.982018",
  "updated_at": "2022-07-06T12:21:56.982018"
}
```

#### 4. 로그인 기능
- 이메일과, 전화번호로 로그인이 가능하도록 했다.
- 닉네임도 unique 하지만 적절하지 않은거 같아 활용하지 않았다.
- 결과값에서 is_activate(로그인 여부) 값이 True로 변경된다.
- Response Body
  - login_type(Enum)
    - email: 이메일
    - phone_number: 휴대폰 번호
  - user_info: (str) 이메일이나 휴대폰 번호 정보
  - password: str
```
# URL
$ http://localhost:8000/user/v1/login

## Example ##
# Curl
$ curl -X 'POST' \
  'http://localhost:8000/user/v1/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "login_type": "email",
  "user_info": "abc@gamil.com",
  "password": "Rlehdeo1!"
}'

# Response Body
{
  "id": 4,
  "user_token": "f0dfc688-d693-4499-8332-09fb5b9e2837",
  "email": "abc@gamil.com",
  "nickname": "에이블리",
  "password": "Rlehdeo1!",
  "name": "택수킴킴",
  "phone_number": "01021618188",
  "is_activate": true,
  "created_at": "2022-07-06T12:21:56.982018",
  "updated_at": "2022-07-06T12:26:11.954055"
}
```

#### 4. 로그아웃 기능
- 로그아웃은 로그인되었을때 호출이 가능하다는 걸로 가정을 하였다
- 그래서 uuid로 생성한 user_token 값을 Header로 활용한다.
- 결과값에서 is_activate(로그인 여부)값이 False로 변경된다.
```
# URL
$ http://localhost:8000/user/v1/logout

## Example ##
# Curl
$ curl -X 'POST' \
  'http://localhost:8000/user/v1/logout' \
  -H 'accept: application/json' \
  -H 'user-token: f0dfc688-d693-4499-8332-09fb5b9e2837' \
  -d ''
  
# Response Body
{
  "id": 4,
  "user_token": "f0dfc688-d693-4499-8332-09fb5b9e2837",
  "email": "abc@gamil.com",
  "nickname": "에이블리",
  "password": "Rlehdeo1!",
  "name": "택수킴킴",
  "phone_number": "01021618188",
  "is_activate": false,
  "created_at": "2022-07-06T12:21:56.982018",
  "updated_at": "2022-07-06T12:28:06.822316"
}
```

#### 5. 비밀번호 재설정 기능
- 전화 번호 인증이 된 휴대폰 번호만 비밀번호 재설정이 되도록 하였다.
- 전화 번호 인증이 되어도 5분 내에 비밀번호 재설정을 하지 않으면 에러가 발생되도록 설정했습니다.
- password에 대한 체크도 이루어진다. (기존이랑 같을 시에도 에러가남)
- Ruquest Body
  - phone_number: str
  - password: str
```
# URL
$ http://localhost:8000/user/v1/reset

## Example ##
$ curl -X 'PATCH' \
  'http://localhost:8000/user/v1/reset' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "phone_number": "01021618188",
  "password": "Eoehdrl1!"
}'

# Response Body
{
  "id": 4,
  "user_token": "9ddfb3a8-0b63-4af8-9bec-825d914261d9",
  "email": "abc@gamil.com",
  "nickname": "에이블리",
  "password": "Eoehdrl1!",
  "name": "택수킴킴",
  "phone_number": "01021618188",
  "is_activate": false,
  "created_at": "2022-07-06T12:43:40.892637",
  "updated_at": "2022-07-06T12:44:20.542745"
}
```

#### 6. 내 정보 보기 기능
- 로그인 시에만 이용할 수 있도록 설정
- user_token을 헤더로 이용함
```
# URL
$ http://localhost:8000/user/v1/

## Example ##
# Curl
$ curl -X 'GET' \
  'http://localhost:8000/user/v1' \
  -H 'accept: application/json' \
  -H 'user-token: 4db5dbc8-82ec-4f8e-9848-9fa6d5b1847e'
  
# Response Body
{
  "id": 4,
  "user_token": "4db5dbc8-82ec-4f8e-9848-9fa6d5b1847e",
  "email": "abc@gamil.com",
  "nickname": "에이블리",
  "password": "Rlehdeo1!",
  "name": "택수킴킴",
  "phone_number": "01021618188",
  "is_activate": true,
  "created_at": "2022-07-06T12:52:54.031766",
  "updated_at": "2022-07-06T12:53:04.713977"
}
```
- --