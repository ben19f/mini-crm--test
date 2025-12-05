from database import SessionLocal
from db_models import Source


def add_source(db, source_name: str):
    """
    Добавляеm источник
    """
    source = Source(
        source_name=source_name
    )
    db.add(source)
    db.commit()



db = SessionLocal()


source = add_source(
    db=db,
    source_name="bot03"
)

db.close()
