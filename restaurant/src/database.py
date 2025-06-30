import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session
from contextlib import contextmanager
# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Function to create database tables


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Function to get database session


def get_session():
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_for_faker():
    with Session(engine) as session:
        yield session
