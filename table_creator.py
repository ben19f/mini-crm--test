from db_interaction import engine, Base, Operator
from db_interaction import Lead, Operator

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Таблица создана!")

if __name__ == "__main__":
    create_tables()
