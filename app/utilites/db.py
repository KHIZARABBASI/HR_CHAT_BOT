from app.database.database import Sessionlocal

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
        

db_depandency = Annotated[Session, Depends(get_db)]
        