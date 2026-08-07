import pytest

from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import (
    authenticate_user,
    create_user,
    get_user,
    get_user_by_email,
    get_users,
    update_user,
)


def make_user_create(email="alice@example.com", password="password123"):
    return UserCreate(
        email=email,
        password=password,
        confirm_password=password,
        full_name="Alice",
        mobile_number="1234567890",
    )


def test_create_user_hashes_password(db_session):
    user = create_user(db_session, make_user_create())
    assert user.email == "alice@example.com"
    assert user.hashed_password != "password123"
    assert verify_password("password123", user.hashed_password)


def test_get_user_by_email_returns_user(db_session):
    create_user(db_session, make_user_create())
    user = get_user_by_email(db_session, "alice@example.com")
    assert user is not None
    assert user.full_name == "Alice"


def test_get_user_by_email_returns_none_for_unknown(db_session):
    assert get_user_by_email(db_session, "nobody@example.com") is None


def test_get_user_returns_user_by_id(db_session):
    created = create_user(db_session, make_user_create())
    user = get_user(db_session, created.id)
    assert user is not None
    assert user.email == "alice@example.com"


def test_get_user_returns_none_for_unknown_id(db_session):
    assert get_user(db_session, 999) is None


def test_get_users_returns_paginated(db_session):
    create_user(db_session, make_user_create(email="a@example.com"))
    create_user(db_session, make_user_create(email="b@example.com"))
    assert len(get_users(db_session, skip=0, limit=10)) == 2
    assert len(get_users(db_session, skip=1, limit=10)) == 1


def test_update_user(db_session):
    user = create_user(db_session, make_user_create())
    updated = update_user(db_session, user, UserUpdate(full_name="Alicia"))
    assert updated.full_name == "Alicia"
    assert updated.mobile_number == "1234567890"


def test_authenticate_user_success(db_session):
    create_user(db_session, make_user_create())
    user = authenticate_user(db_session, "alice@example.com", "password123")
    assert user is not None
    assert user.email == "alice@example.com"


def test_authenticate_user_wrong_password(db_session):
    create_user(db_session, make_user_create())
    assert authenticate_user(db_session, "alice@example.com", "wrongpass") is None


def test_authenticate_user_unknown_email(db_session):
    assert authenticate_user(db_session, "ghost@example.com", "password123") is None
