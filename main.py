from fastapi import FastAPI, HTTPException, Depends

from database import SessionLocal
from pydantic import BaseModel


app = FastAPI(title="crm API")

def get_db():
    """определяем БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OperatorResp(BaseModel):
    id: int
    name: str
    active_status: bool
    workload_limit: int

    class Config:
        orm_mode = True


@app.post("/operators/", response_model=OperatorResp, status_code=201)
def create_operator(

