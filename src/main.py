from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from api.routers import v1_main_router
from core.config import settings


app = FastAPI(
    title="Social Net API",
    summary="API для сервиса по взаимодействию с участниками",
)

app.include_router(v1_main_router)


async def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
