from fastapi import Depends
from app.db.connections import Session

def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()
    