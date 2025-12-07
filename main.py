from fastapi import FastAPI, HTTPException

from database import SessionLocal
from pydantic import BaseModel
from typing import List
from db_models import Operator

# app = FastAPI(title="crm API")

db = SessionLocal()

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




@app.post("/operators/", response_model=List(OperatorResp))
def list_operators(active: Optional[bool] = None,
        db):
    """
    ищем операторов список
    """
    query = db.query(Operator)
    if active is not None:
        query = query.filter(Operator.active_status == active)

    operators = query.all()
    return operators


print(list_operators(active=None, db=db))
db.close()