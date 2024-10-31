from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from core.config import settings
from core.user_manager import get_user_manager
from models import User

cookie_transport = CookieTransport(cookie_max_age=3600 * 24)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.AUTH_SECRET, lifetime_seconds=3600 * 24)


auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
optional_current_user = fastapi_users.current_user(optional=True)
