from http.client import HTTPException

from database import SessionLocal
from db_models import Contact


def create_contact(
        db: SessionLocal,
        lead_id: int,
        source_id: int,
        operator_id: int
) -> Contact:
    """
    связывая лида с источником и оператором.

    """

    # Если оператор не передан — пытаемся выбрать автоматически
    if operator_id is None:

        raise HTTPException(status_code=404)


    contact = Contact(
        lead_id=lead_id,
        source_id=source_id,
        operator_id=operator_id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)  # получаем ID из БД

    return contact