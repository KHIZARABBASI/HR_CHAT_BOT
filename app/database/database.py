from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "postgresql://postgres:465249802@localhost:5000/HR Management System"

engine = create_engine(URL_DATABASE)
Sessionlocal = sessionmaker(bind=engine, autoflush= False, autocommit= False)

Base = declarative_base()
