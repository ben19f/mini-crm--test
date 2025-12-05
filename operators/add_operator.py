from database import SessionLocal
from db_models import Operator

def add_operator(db , name: str, active_status: bool = True, workload: int = 5):
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

db = SessionLocal()

operator = add_operator(
        db=db,
        name="девятый оператор",
        active_status=True,
        workload=5
    )

