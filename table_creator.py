from database import engine, Base
from db_models import Lead, Operator, Contact, OperatorWeight, Source

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Таблица создана!")

if __name__ == "__main__":
    create_tables()
