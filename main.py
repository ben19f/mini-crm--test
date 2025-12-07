from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from pydantic import BaseModel
from typing import List, Optional
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




# @app.post("/operators/", response_model=List[OperatorResp])
def list_operators(active: Optional[bool] = None,
        db: Session = Depends(get_db)):
    """
    ищем операторов список
    """
    query = db.query(Operator)
    if active is not None:
        query = query.filter(Operator.active_status == active)

    operators = query.all()
    return operators


# print(list_operators(active=None, db=db))
operators = list_operators(active=None, db=db)
db.close()

for op in operators:
    print(f"ID: {op.id}, Имя: {op.name}, Активен: {op.active_status}, Лимит: {op.workload_limit}")