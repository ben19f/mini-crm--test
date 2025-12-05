from sqlalchemy.orm import Session
from db_models import Operator

def add_operator(db: Session, name: str, active_status: bool = True, workload: int = 5):
    """
    Добавляеv оператора
    """
    operator = Operator(
        name=name,
        active_status=active_status,
        workload=workload
    )
    db.add(operator)
    db.commit()

operator = add_operator(
        db=db,
        name="первый опер",
        active_status=True,
        workload=5
    )