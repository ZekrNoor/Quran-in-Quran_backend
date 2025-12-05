from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database.models import *
import os
import argparse

# Get the DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine and session
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create tables in the database if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized!")


def rebuild_db():
    """Drop and recreate tables in the database."""
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped!")
    init_db()  # Recreate tables
    print("Database tables recreated!")


def test_db_connection():
    """Test the connection to the database."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Connected to the database! Tables: {tables}")
    except Exception as e:
        print(f"Error: Could not connect to the database: {e}")


# Command-line interface (CLI) functionality
def run_cli():
    parser = argparse.ArgumentParser(description="Database management scripts")
    parser.add_argument(
        "command",
        choices=["init", "rebuild", "test"],
        help="Command to run: init (initialize db), rebuild (drop & recreate db), test (test connection)",
    )
    args = parser.parse_args()

    if args.command == "init":
        init_db()
    elif args.command == "rebuild":
        rebuild_db()
    elif args.command == "test":
        test_db_connection()


if __name__ == "__main__":
    run_cli()
