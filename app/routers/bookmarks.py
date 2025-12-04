from ast import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.routers.auth import get_current_user
from ..crud import (
    add_bookmark,
    get_user_bookmarks,
    get_user_by_username,
    remove_bookmark,
)
from ..auth_core import verify_token
from ..database.database import SessionLocal
from ..database.schemas import Bookmark
from typing import List
from ..database.models import User as DBUser


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get user's bookmarks
@router.get("/", response_model=list[Bookmark])
def get_bookmarks(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_user_by_username(db, token).id
    return get_user_bookmarks(db, user_id)


@router.post("/bookmarks", response_model=Bookmark)
def add_new_bookmark(
    value: str,
    type: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    user_id = get_user_by_username(db, token).id
    return add_bookmark(db, user_id, value, type)


@router.delete("/bookmarks/{bookmark_id}", response_model=Bookmark)
def remove_existing_bookmark(
    bookmark_id: int, token: str = Depends(verify_token), db: Session = Depends(get_db)
):
    user_id = get_user_by_username(db, token).id
    bookmark = remove_bookmark(db, bookmark_id, user_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark
