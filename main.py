from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:/home/ben/PycharmProjects/mini-crm--test/crm.db"



#modeli
Base = declarative_base()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
