from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import timezone, datetime

from sqlalchemy.orm import relationship

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

class Source(Base):
    __tablename__ = "Sources"

    id = Column(Integer, primary_key=True, index=True)
    souce_name = Column(String, nullable=False)
    create_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class OperatorWeight(Base):
    __tablename__ = "Operators"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source")
    operator_id = Column(Integer, ForeignKey("operators.id"))
    operator = relationship("Operator")
    weight = Column(Integer, default=10)

class Contact(Base):
    __tablename__ = "Contacts"

    id = Column(Integer, primary_key=True, index=True)
    lead_id =
    source_id =
    operator_id =
    create_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))