from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.routers.auth import get_current_user
from ..schemas import UserCreate, User, Bookmark
from ..crud import create_user, get_user_by_id, get_user_bookmarks, get_user_by_username
from ..auth import verify_token
from ..database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new user
@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create the user and the associated profile
    profile_data = user.profile.dict()  # Convert the profile field into a dictionary
    new_user = create_user(db, user.username, user.password, profile_data)
    
    return new_user

# Get user profile
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
