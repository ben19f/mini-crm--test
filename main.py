from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime


DATABASE_URL = "sqlite:///home/ben/PycharmProjects/mini-crm--test/crm.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

#modeli
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    active_status = Column(Boolean, default=True)
    workload = Column(Integer, default=5)
    create_time = Column(DateTime, default=datetime.utcnow)
