from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from pydantic import BaseModel
from typing import List, Optional
from db_models import Operator

app = FastAPI(title="crm API")

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


class OperatorCreate(BaseModel):
    name: str
    active_status: bool = True
    workload_limit: int = 5

    class Config:
        orm_mode = True


class OperatorUpdate(BaseModel):
    active_status: Optional[bool] = None
    workload_limit: Optional[int] = None


    class Config:
        orm_mode = True


@app.get("/operators/list", response_model=List[OperatorResp])
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


@app.post("/operators/create", response_model=OperatorResp, status_code=201)
def create_operator(operator_data: OperatorCreate, db: Session = Depends(get_db)):
    # ищем повторы
    if db.query(Operator).filter(Operator.name == operator_data.name).first():
        raise HTTPException(
            status_code=400,
            detail="Оператор с таким именем уже существует"
        )
    operator = Operator(
        name=operator_data.name,
        active_status=operator_data.active_status,
        workload_limit=operator_data.workload_limit
    )
    db.add(operator)
    db.commit()
    db.refresh(operator)
    print('gotovo')
    return operator


@app.patch("/operators/{operator_id}", response_model=OperatorResp)
def update_operator(
        operator_id: int,
        update_data: OperatorUpdate,
        db: Session = Depends(get_db)
):
    """
    Обновляет лимит нагрузки.
    """
    operator = db.query(Operator).filter(Operator.id == operator_id).first()


# operators = list_operators(active=None, db=db)
# db.close()
#
# for op in operators:
#     print(f"ID: {op.id}, Имя: {op.name}, Активен: {op.active_status}, Лимит: {op.workload_limit}")


# test_data = OperatorCreate(
#     name="Десятый владислав",
#     active_status=True,
#     workload_limit=5
# )
#
# create_operator(operator_data=test_data, db=db)
#
# db.close()




# =================
# Добавление через
# curl -X POST "http://localhost:8000/operators/" \
#      -H "Content-Type: application/json" \
#      -d '{"name": "Анна", "active_status": true, "workload_limit": 10}'
# {"id":11,"name":"Анна","active_status":true,"workload_limit":10}



# ==================
# get list
# GET http://localhost:8000/operators/list

# get active list
# GET http://localhost:8000/operators/list/?active=true
