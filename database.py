from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

default_url = "postgresql://postgres:postgres@localhost:5432/geo_admin"

DATABASE_URL = os.getenv("DATABASE_URL", default_url)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)