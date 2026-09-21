from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user, get_db
from app.schemas.user import UserResponse
from app.services.user import get_user, get_users

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_current_user(user=Depends(get_current_user)):
    return user


@router.get("", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
