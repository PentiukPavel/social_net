from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App config
    AUTH_SECRET: str
    STORAGE_LOCATION: str = "media/"

    # Data Base config
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    # e-mail config
    SMTP_PASSWORD: str
    SMTP_USER: str
    SMTP_HOST: str
    SMTP_PORT: str

    # Redis config
    REDIS_HOST: str
    REDIS_PORT: str

    # Test Data Base config
    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

DSN = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{settings.DB_USER_TEST}:{settings.DB_PASS_TEST}"
    f"@{settings.DB_HOST_TEST}:{settings.DB_PORT_TEST}/{settings.DB_NAME_TEST}"
)
