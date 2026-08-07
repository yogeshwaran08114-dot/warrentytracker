import pytest
from fastapi import HTTPException

from app.core.security import decode_token
from app.schemas.user import UserCreate
from app.services import auth as auth_service


def make_user_create(email="alice@example.com", password="password123"):
    return UserCreate(
        email=email,
        password=password,
        confirm_password=password,
        full_name="Alice",
    )


def test_register_user_creates_account(db_session):
    user = auth_service.register_user(db_session, make_user_create())
    assert user.id is not None
    assert user.email == "alice@example.com"


def test_register_duplicate_email_raises(db_session):
    auth_service.register_user(db_session, make_user_create())
    with pytest.raises(HTTPException) as exc_info:
        auth_service.register_user(db_session, make_user_create())
    assert exc_info.value.status_code == 400


def test_login_returns_token(db_session):
    user = auth_service.register_user(db_session, make_user_create())
    result = auth_service.login(db_session, user.email, "password123")
    assert result["token_type"] == "bearer"
    payload = decode_token(result["access_token"])
    assert payload["sub"] == str(user.id)


def test_login_wrong_password_raises(db_session):
    auth_service.register_user(db_session, make_user_create())
    with pytest.raises(HTTPException) as exc_info:
        auth_service.login(db_session, "alice@example.com", "wrongpass")
    assert exc_info.value.status_code == 401


def test_login_unknown_email_raises(db_session):
    with pytest.raises(HTTPException) as exc_info:
        auth_service.login(db_session, "ghost@example.com", "password123")
    assert exc_info.value.status_code == 401


def test_get_current_user_returns_user(db_session):
    created = auth_service.register_user(db_session, make_user_create())
    result = auth_service.login(db_session, created.email, "password123")
    user = auth_service.get_current_user(db_session, result["access_token"])
    assert user.id == created.id


def test_get_current_user_invalid_token_raises(db_session):
    with pytest.raises(HTTPException) as exc_info:
        auth_service.get_current_user(db_session, "not-a-real-token")
    assert exc_info.value.status_code == 401
