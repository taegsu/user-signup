# User SingUp API

## Dependency
- Docker
- Python3.9
- sqlalchemy
- fastapi
- redis

## Run Server
### 1. Set Docker (Postgresql & Redis)
```
# RUN postgresql Docker
$ docker run --name user-test-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=user -d postgres:12.2-alpine

# RUN Redis Docker
$ docker run --name user-test-redis -p 6379:6379 -d redis:6.2-alpine
```
### 2. Run uvicorn Server
```
# No Use Docker Version
$ python3 -m venv .venv
$ source .venv/bin/activate
$ poetry update
$ poetry run uvicorn app.main:app --host 0.0.0.0
```
