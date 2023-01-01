from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 #PostgreSQL adapter for python
from psycopg2.extras import RealDictCursor #mapping col name to its value
import time
from .config import settings

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) #responsible fr establishing the connection

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base =declarative_base()


def get_db(): #dependency: get a session to db
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

