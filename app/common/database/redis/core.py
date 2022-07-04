from redis import Redis

from app.config import settings

session = Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
