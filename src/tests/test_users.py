import http

import pytest
from sqlalchemy import select

from main import app
from models import User


@pytest.mark.asyncio
async def test_registry(async_client, get_session):
    email = "string1@string.exmpl"
    request_data = {
        "email": email,
        "password": "string",
        "last_name": "string",
        "first_name": "string",
        "is_active": True,
        "sex": 1,
        "is_superuser": False,
        "is_verified": True,
    }
    response = await async_client.post(
        "api/clients/register", json=request_data
    )
    assert response.status_code == http.HTTPStatus.CREATED
    user_query = select(User).filter_by(email=email)
    result = await get_session.execute(user_query)
    user = result.scalar_one_or_none()
    assert user is not None


@pytest.mark.asyncio
async def test_get_services(async_authorized_client, create_user):
    user = create_user
    response = await async_authorized_client.get(
        app.url_path_for("get_users_endpoint"),
    )
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()[0]["email"] == user.email
