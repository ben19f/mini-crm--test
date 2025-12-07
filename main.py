from time import sleep

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from pydantic import BaseModel
from typing import List, Optional
from db_models import Operator, Lead
from leads_interaction import chek_and_lead
from operators.operators_interaction import assign_operator_for_lead

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
def update_limit(
        operator_id: int,
        update_data: OperatorUpdate,
        db: Session = Depends(get_db)
):
    """
    Обновляет лимит нагрузки.
    """
    operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail="Оператор не найден")


    if update_data.active_status is not None:
        operator.active_status = update_data.active_status
    if update_data.workload_limit is not None:
        if update_data.workload_limit < 1:
            raise HTTPException(
                status_code=400,
                detail="Лимит нагрузки должен быть ≥ 1"
            )
        operator.workload_limit = update_data.workload_limit

    db.commit()
    db.refresh(operator)
    return operator



class LeadCreate(BaseModel):
    name: str
    phone: str
    source_key: str
    unique_id: str

class LeadResponse(BaseModel):
    id: int
    unique_id: str
    name: str
    phone: str
    # create_time: datetime
    source_key: str
    operator_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True  # для datetime




@app.post("/leads/", response_model=LeadResponse, status_code=201)
def create_lead_and_assign_operator(
    lead_data: LeadCreate,
    db: Session = Depends(get_db)):
    """
    Создаёт лида и автоматически назначает ему оператора.
    """
    # Создаём
    # лида

    result = chek_and_lead(db, lead_data.unique_id)

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Уникальное имя лида уже занято"
        )

    # Если лид создан/найден, получаем его из БД
    sleep(1)
    lead = db.query(Lead).filter(Lead.unique_id == lead_data.unique_id).first()
    if not lead:
        raise HTTPException(
            status_code=500,
            detail="Ошибка: лид не найден после создания"
        )

    # чаем оператора
    operator_id = assign_operator_for_lead(db, lead.id, lead_data.source_key)
    if not operator_id:
        raise HTTPException(
            status_code=400,
            detail="Не удалось назначить оператора для лида"
        )

    # ответ
    return LeadResponse(
        id=lead.id,
        unique_id=lead.unique_id,
        name=lead.name,
        phone=lead.phone,
        # create_time=lead.create_time,
        source_key=lead_data.source_key,
        operator_id=operator_id
    )


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

# ===============
# curl -X PATCH "http://localhost:8000/operators/6" -H "Content-Type: application/json" -d '{"workload_limit": 3}'



# ================
# добавим лида
# curl -X POST "http://localhost:8000/leads/" -H "Content-Type: application/json" -d '{ "unique_id": "user_12345", "name": "Иван Петров", "phone": "+79991234567", "source_key": "bot01"}'
