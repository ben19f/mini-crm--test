from database import SessionLocal
from db_models import Lead
from datetime import datetime


def add_lead(db, unique_id: str) -> Lead:
    """
    Добавляем лида в таблицу
    """
    lead = Lead(
        unique_id=unique_id,
        create_time=datetime.utcnow()
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

# def add_lead(db: Session, unique_id: str) -> Lead:
#     lead = Lead(unique_id=unique_id)
#     db.add(lead)
#     db.commit()
#     db.refresh(lead)  # ← важно: обновляем объект из БД
#     return lead


# def chek_and_lead(db, unique_id: str) -> Lead:
#     """
#     Ищет лида
#     """
#     lead = db.query(Lead).filter(Lead.unique_id == unique_id).first()
#
#     if lead is None:
#         add_lead(db, unique_id)
#         return unique_id
#     else:
#         return False

def chek_and_lead(db, unique_id: str) -> Lead | None:
    lead = db.query(Lead).filter(Lead.unique_id == unique_id).first()
    if lead is None:
        lead = add_lead(db, unique_id)
        return lead
    else:
        return None







# db = SessionLocal()
#
# chek_lead(db, 'егорТуапсер')
#
# db.close()

# curl -X POST "http://localhost:8000/leads/"
# -H "Content-Type: application/json" -d '
# { "unique_id": "user_12345",
# "name": "Иван Петров",
# "phone": "+79991234567",
# "source_key": "bot01"}'
