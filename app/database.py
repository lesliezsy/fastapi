# this file is to handle db connections

# import SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# create connection string / database URL
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<datadbase_name>"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# create a database engine to coonnect SQLAlchemy to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a session local class to create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# create a base class for the declarative model
Base = declarative_base()


# create a new session for each request
# every request has its own session, each request has its own connection to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# cursor_factory=RealDictCursor is to give the coliumn names and values
# RealDictCursor is a cursor that returns rows as dictionaries
# psycopg2 is a PostgreSQL adapter for Python
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root1234', cursor_factory=RealDictCursor)
    
#          # this is to execute SQL commands/statements
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error: ", error)
#         time.sleep(2)