from fastapi import FastAPI, HTTPException, Depends

from database import SessionLocal

app = FastAPI(title="crm API")

def get_db():
    """определяем БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


