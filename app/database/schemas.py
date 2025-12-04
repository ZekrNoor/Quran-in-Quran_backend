from pydantic import BaseModel
from typing import List, Optional


# Profile Pydantic model for input and output
class ProfileBase(BaseModel):
    age: Optional[int] = None
    sex: Optional[str] = None
    city: Optional[str] = None
    image_url: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None


class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = (
            True  # Allow FastAPI to convert SQLAlchemy models into Pydantic models
        )


# User Pydantic schema
class UserBase(BaseModel):
    username: str
    phone_number: Optional[str] = None  # Phone number can also be used for login


class UserCreate(UserBase):
    password: str
    profile: ProfileBase


class User(UserBase):
    id: int
    profile: Optional[Profile] = None  # Include profile in the user response

    class Config:
        orm_mode = (
            True  # Allow FastAPI to convert SQLAlchemy models into Pydantic models
        )


class User(UserBase):
    id: int
    bookmarks: List["Bookmark"] = []

    class Config:
        orm_mode = True


# Bookmark Pydantic schema
class BookmarkBase(BaseModel):
    type: str
    value: str


class Bookmark(BookmarkBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Token schema for login
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
