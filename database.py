from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///home/ben/PycharmProjects/mini-crm--test/crm.db"
DATABASE_URL = "sqlite:///crm.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

#modeli
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)