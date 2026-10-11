from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, decode_token
from app.models.user import User
from app.services.user import (
    authenticate_user,
    create_user,
    get_user_by_email,
)


def register_user(db: Session, user_in) -> User:
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(db=db, user=user_in)


def login(db: Session, username: str, password: str) -> dict:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return create_token_response(user)


def create_token_response(user: User) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(db: Session, token: str) -> User:
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
