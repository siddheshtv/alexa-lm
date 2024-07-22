from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = f'{DATABASE_PREFIX}://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}'

# DATABASE_URL = f'mysql+pymysql://sid:sample123@localhost/alexa_db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
