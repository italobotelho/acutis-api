import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load secret environment variables from the .env file
load_dotenv()

# Construct the database connection URL
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# The Engine is the core manager that communicates with PostgreSQL
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    print("[*] Database engine initialized successfully.")
except Exception as e:
    print(f"[!] Error initializing the database: {e}")

# SessionLocal will be used in API routes to open and close database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating SQL models in Python
Base = declarative_base()

# FastAPI dependency for database session injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()