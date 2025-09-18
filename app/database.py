from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Create tables in the database if they don't exist."""
    Base.metadata.create_all(bind=engine)

def test_db_connection():
    """Test the connection to the database."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Connected to the database! Tables: {tables}")
    except Exception as e:
        print(f"Error: Could not connect to the database: {e}")

# Test the DB connection (optional for debugging)
test_db_connection()

# Create the tables when the app starts
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()