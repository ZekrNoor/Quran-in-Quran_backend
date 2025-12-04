from sqlalchemy.orm import Session
from .database.models import User as DBUser, Profile as DBProfile, Bookmark as DBBookmark
from .auth_core import get_password_hash


# Create a new user along with their profile
def create_user(db: Session, username: str, password: str, profile_data: dict):
    hashed_password = get_password_hash(password)
    db_user = DBUser(username=username, password=hashed_password)

    # Create the profile associated with the user
    db_profile = DBProfile(**profile_data)  # Unpack the profile data dict
    db_user.profile = db_profile

    db.add(db_user)
    db.add(db_profile)  # Make sure the profile is also added to the session
    db.commit()
    db.refresh(db_user)
    db.refresh(db_profile)

    return db_user  # Return the SQLAlchemy user model (FastAPI will convert it to Pydantic model)


# Get a user by phone number
def get_user_by_phone_number(db: Session, phone_number: str):
    return (
        db.query(DBUser).filter(DBUser.profile.has(phone_number=phone_number)).first()
    )


# Get a user by username
def get_user_by_username(db: Session, username: str):
    return db.query(DBUser).filter(DBUser.username == username).first()


# Get a user by ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()


# Get all bookmarks for a user
def get_user_bookmarks(db: Session, user_id: int):
    return db.query(DBBookmark).filter(DBBookmark.user_id == user_id).all()


# Add a bookmark
def add_bookmark(db: Session, user_id: int, value: str, type: str):
    db_bookmark = DBBookmark(value=value, type=type, user_id=user_id)
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


# Remove a bookmark
def remove_bookmark(db: Session, bookmark_id: int, user_id: int):
    db_bookmark = (
        db.query(DBBookmark)
        .filter(DBBookmark.id == bookmark_id, DBBookmark.user_id == user_id)
        .first()
    )
    if db_bookmark:
        db.delete(db_bookmark)
        db.commit()
        return db_bookmark
    return None
