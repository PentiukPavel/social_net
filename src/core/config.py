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

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

DSN = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
