from db_models import Operator, Contact
from config import operator_dict
from database import SessionLocal
import random


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

def select_heaviest_operator(db, available_operators: list[Operator]) -> int | None:
    """
    Выбирает оператора с максимальной текущей нагрузкой.
    """
    if not available_operators:
        return None

    operator_loads = []
    for op in available_operators:
        current_load = get_current_workload(db, op.id)
        operator_loads.append((op.id, current_load))

    max_load = max(load for _, load in operator_loads)
    candidates = [op_id for op_id, load in operator_loads if load == max_load]
    selected_id = random.choice(candidates)
    return selected_id



db = SessionLocal()

# Ищем доступных операторов для источника 'bot01'
operators = get_available_operators(db, 'bot01')

if operators:
    print(f"Доступные операторы для bot01 ({len(operators)}):")
    for op in operators:
        print(f"- ID: {op.id}, Имя: {op.name}, Нагрузка: {op.workload_limit}")
else:
    print("Нет доступных операторов для bot01")

result_operator = select_heaviest_operator (db, operators)
print(result_operator)