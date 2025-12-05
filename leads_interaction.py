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

db = SessionLocal()

db.close()