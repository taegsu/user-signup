from os import getenv

from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str = "local"
    debug_mode: bool = False
    secret_key: str = "5ecret"
    app_name: str = "user_api"

    # Postgres
    database_username: str = "postgres"
    database_password: str = "postgres"
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "user"
    ro_database_username: str = "postgres"
    ro_database_password: str = "postgres"
    ro_database_host: str = "localhost"

    # Redis
    sign_up_redis_db: int = 0
    reset_password_redis_db: int = 1
    redis_host: str = "localhost"
    redis_port: int = 6379

    # SQLAlchemy
    sqlalchemy_max_overflow: int = 10
    sqlalchemy_pool_size: int = 8
    sqlalchemy_pool_recycle: int = 3600
    sqlalchemy_pool_timeout: int = 30


class DevSettings(Settings):
    env: str = "dev"


class StagingSettings(Settings):
    env: str = "staging"


class ProdSettings(StagingSettings):
    env: str = "prod"


class TestSettings(Settings):
    env: str = "test"


def get_settings(env: str) -> Settings:
    if env == "local":
        return Settings()
    if env == "dev":
        return DevSettings()
    if env == "staging":
        return StagingSettings()
    if env == "prod":
        return ProdSettings()
    if env == "test":
        return TestSettings()
    raise RuntimeError("Wrong ENV")


settings = get_settings(getenv("ENV", "local"))
