from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import timezone, datetime
from database import Base


class Operator(Base):
    __tablename__ = "Operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    active_status = Column(Boolean, default=True)
    workload = Column(Integer, default=5)
    create_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Lead(Base):
    __tablename__ = "Leads"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String, nullable=False)
    create_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

