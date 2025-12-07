from typing import Optional

from db_models import Operator, Contact, Lead
from sources.config import operator_dict
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



# db = SessionLocal()
#
# # Ищем доступных операторов для источника 'bot01'
# operators = get_available_operators(db, 'bot01')
#
# if operators:
#     print(f"Доступные операторы для bot01 ({len(operators)}):")
#     for op in operators:
#         print(f"- ID: {op.id}, Имя: {op.name}, Нагрузка: {op.workload_limit}")
# else:
#     print("Нет доступных операторов для bot01")

# result_operator = select_heaviest_operator (db, operators)


def assign_operator_for_lead(
        db: SessionLocal,
        lead_id: int,
        source_key: str
) -> Optional[int]:
    """
    Назначает оператора мсвязь лида.
    1. Проверяет существование лида
    2. Находит доступных операторов для источника
    3. Выбирает самого загруженного из доступных
    4. Создаёт связь (контакт)
    Returns:
        ID назначенного оператора или None при ошибке
    """

    # Проверяем лида
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        print(f"Ошибка: Лид с ID={lead_id} не найден")
        return None
    print('я тут 1')
    # Получаем операторов
    available_operators = get_available_operators(db, source_key)
    if not available_operators:
        print(f"Нет доступных операторов для источника '{source_key}'")
        return None
    print('я тут 2')
    #Выбираем лучшего оператора чтобы быстрее закончил свою слену
    selected_operator_id = select_heaviest_operator(db, available_operators)
    if not selected_operator_id:
        print("Не удалось выбрать оператора (список пуст)")
        return None
    print('я тут 3')
    # Создаём связь лид-оператор
    try:
        contact = Contact(
            lead_id=lead_id,
            source_key=source_key,
            operator_id=selected_operator_id
        )
        db.add(contact)
        db.commit()
        print(f"Оператор ID={selected_operator_id} назначен для лида ID={lead_id}")
        return selected_operator_id
    except Exception as e:
        print(f"Ошибка при создании контакта: {e}")
        db.rollback()
        return None