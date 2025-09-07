from fastapi import FastAPI
from .routers import auth, users, bookmarks
from .database import init_db

app = FastAPI()

# Initialize database
init_db()

# Include the routers for auth, users, and bookmarks
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
