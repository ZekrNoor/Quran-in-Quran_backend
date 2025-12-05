from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.database.schemas import UserCreate, User, Profile
from app.crud import create_user, get_user_by_id, get_user_by_username
from app.routers.auth import get_current_user
from app.database.database import SessionLocal, get_db
from app.upload_file import upload_file
import os

router = APIRouter()


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


# Update user's profile image without needing user_id in the request
@router.post("/upload-profile-image")
async def upload_profile_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get the current authenticated user
    db_user = current_user

    # Upload image and get URL
    image_url = upload_file(image, db_user.username)

    if image_url:
        # Find the user's profile and update the image URL
        profile = db.query(Profile).filter(Profile.user_id == db_user.id).first()
        if profile:
            profile.profile_image_url = image_url
            db.commit()
            db.refresh(profile)
            return {
                "message": "Profile image uploaded successfully!",
                "image_url": image_url,
            }
        else:
            raise HTTPException(status_code=404, detail="Profile not found")
    else:
        raise HTTPException(status_code=400, detail="Failed to upload image")
