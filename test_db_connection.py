from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")
print("Using DATABASE_URL:", DATABASE_URL)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Test the connection
try:
    # Use the connection context manager
    with engine.connect() as connection:
        # Use text() to execute the raw SQL query
        result = connection.execute(text("SELECT 1"))
        print("Database connected:", result.fetchone())
except Exception as e:
    print("Error connecting to the database:", e)
