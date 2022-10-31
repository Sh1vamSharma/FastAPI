from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<dataase_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# database  
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# establishes session to dataase
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# to create tables
Base = declarative_base()

# Dependency,  this session is responsible to communicate with databbase
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



