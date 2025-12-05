from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    sex = Column(String)
    city = Column(String)
    phone_number = Column(String, unique=True)
    email = Column(String, unique=True)
    nickname = Column(String, unique=True)

    # Column to store the image URL or path in object storage
    image_url = Column(String, nullable=True)

    # One-to-one relationship with User
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="profile")


# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship to Profile
    profile = relationship("Profile", back_populates="user", uselist=False)

    # Other relationships (e.g., bookmarks, notes)
    bookmarks = relationship("Bookmark", back_populates="owner")
    notes = relationship("Note", back_populates="owner")


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    value = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="bookmarks")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="notes")
