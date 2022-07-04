from redis import Redis

from app.config import settings

signup_session = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.sign_up_redis_db,
)
reset_session = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.reset_password_redis_db,
)
