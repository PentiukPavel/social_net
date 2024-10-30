from fastapi import APIRouter

from api.endpoints import v1_users_router

v1_main_router = APIRouter()

v1_main_router.include_router(v1_users_router)
