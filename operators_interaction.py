from db_models import Operator, Contact
from config import operator_dict
from database import SessionLocal


def get_current_workload(db, operator_id: int) -> int:
    """
    Считает количество ОБРАЩЕНИЙ
    """
    count = db.query(Contact).filter(Contact.operator_id == operator_id).count()
    return count

def get_available_operators(db, source_key: str) -> list[Operator]:
    """Ищет доступных операторов."""
    if source_key not in operator_dict:
        return []

    assigned_operator_ids = operator_dict[source_key]
    available_operators = []

    # Получаем всех назначенных операторов из БД
    operators = db.query(Operator).filter(
        Operator.id.in_(assigned_operator_ids),
        Operator.active_status == True
    ).all()

    for operator in operators:
        current_load = get_current_workload(db, operator.id)
        if current_load < operator.workload_limit:
            available_operators.append(operator)

    return available_operators




db = SessionLocal()

# Ищем доступных операторов для источника 'bot01'
operators = get_available_operators(db, 'bot01')

if operators:
    print(f"Доступные операторы для bot01 ({len(operators)}):")
    for op in operators:
        print(f"- ID: {op.id}, Имя: {op.name}, Нагрузка: {op.workload_limit}")
else:
    print("Нет доступных операторов для bot01")