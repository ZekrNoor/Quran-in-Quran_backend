from fastapi import FastAPI
from dotenv import load_dotenv
from .routers import auth, users, bookmarks

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# Include the routers for auth, users, and bookmarks
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
