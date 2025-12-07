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


def chek_lead(db, unique_id: str) -> Lead:
    """
    Ищет лида
    """
    lead = db.query(Lead).filter(Lead.unique_id == unique_id).first()

    if lead is None:
        add_lead(db, unique_id)
        print(f"Создан лид {unique_id}")
    else:
        print(f"лид {lead.unique_id} - уже есть")




# db = SessionLocal()
#
# chek_lead(db, 'егорТуапсер')
#
# db.close()