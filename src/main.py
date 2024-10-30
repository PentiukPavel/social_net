from fastapi import FastAPI

from api.routers import v1_main_router


app = FastAPI(
    title="Social Net API",
    summary="API для сервиса по взаимодействию с участниками",
)

app.include_router(v1_main_router)
